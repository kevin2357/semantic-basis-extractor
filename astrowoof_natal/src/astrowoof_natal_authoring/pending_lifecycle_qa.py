"""Installed-wheel, provider-free provider-pending lifecycle qualification."""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from .closure import load_json, normalized_path, public_run_state, write_workspace_snapshot
from .deployed_qa import _wave
from .initial_wave import (
    ProviderCreateResult, build_wave_authorization, execute_initial_wave_creates,
)
from .lifecycle import inspect_lifecycle
from .lifecycle_contracts import validate_lifecycle_inspection_v05
from .reconciliation import reconcile_provider_cycle


RECEIPT_SCHEMA = "astrowoof.provider_pending_lifecycle_qualification.v1"


def _sha(value: dict[str, Any]) -> str:
    body = {key: item for key, item in value.items() if key != "receipt_sha256"}
    encoded = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def run_provider_pending_lifecycle_qualification() -> dict[str, Any]:
    """Exercise create, detach, due selection, bounded retrieval, and replay safety."""
    with tempfile.TemporaryDirectory(prefix="sbe-pending-lifecycle-qa-") as temporary:
        root = Path(temporary).resolve()
        wave, documents = _wave("exact_natal")
        authorization = build_wave_authorization(
            wave, documents,
            reservation_set_reference="qualification-only:no-reservation",
            issuer="sbe-installed-qualification",
            authorized_at="1970-01-01T00:00:00Z",
        )
        creates: list[str] = []
        outcomes: list[dict[str, Any]] = []

        def submit(member: dict[str, Any], _timeout: int) -> ProviderCreateResult:
            provider_id = f"resp_pending_qa_{member['pass_number']:02d}"
            creates.append(provider_id)
            return ProviderCreateResult(provider_id)

        result = execute_initial_wave_creates(
            wave, authorization=authorization, member_authorizations=documents,
            submit=submit,
            persist_member_outcome=lambda _member, outcome: outcomes.append(
                copy.deepcopy(dict(outcome))
            ),
        )
        by_action = {item["action_id"]: item for item in outcomes}
        actions = []
        passes = {}
        for number, document in enumerate(documents, 1):
            action_id = document["action_id"]
            provider_id = by_action[action_id]["provider"]["id"]
            actions.append({
                "action_id": action_id, "state": "WAITING",
                "binding": document["binding"], "authorization": document,
                "consumption": {
                    "consumer_id": "installed-qualification",
                    "consumed_at": "1970-01-01T00:00:01Z",
                },
                "provider": {"id": provider_id, "kind": "response"},
                "provider_reconciliation": {
                    "policy_version": "astrowoof.provider_reconciliation_policy.v0.2",
                    "provider_retrieval_attempt_count": 0,
                    "last_attempt_at": None,
                    "last_outcome": "provider_identity_recorded",
                    "resume_not_before": "1970-01-01T00:00:15Z",
                },
                "reported": None,
            })
            passes[f"pass-{number}"] = {
                "pass_id": f"pass-{number}", "state": "WAITING_FOR_RESPONSE",
                "attempts": [{"attempt": 1, "state": "WAITING_FOR_RESPONSE"}],
            }
        state = {
            "schema_version": "astrowoof.semantic_closure_run.v0.9",
            "run_id": wave["run_id"], "state_revision": 1,
            "status": "WAITING_FOR_RESPONSE",
            "workspace_contract": {
                "mode": "stable_logical_absolute_path",
                "logical_root": normalized_path(root),
            },
            "spend_ledger": {"actions": actions}, "passes": passes,
            "initial_authoring_wave": {"state": "DETACHED"},
            "subjects": {}, "provenance": {},
        }
        (root / "run.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        (root / "public-run.json").write_text(
            json.dumps(public_run_state(state), indent=2) + "\n", encoding="utf-8"
        )
        write_workspace_snapshot(root)

        not_due = inspect_lifecycle(
            root, native_exclusive_access="declared",
            observed_at="1970-01-01T00:00:10Z",
        )
        due = inspect_lifecycle(
            root, native_exclusive_access="declared",
            observed_at="1970-01-01T00:00:15Z",
        )
        contradictory = copy.deepcopy(due)
        contradictory["terminal"]["local_continuation_remains"] = True
        contradiction_refused = False
        try:
            validate_lifecycle_inspection_v05(contradictory)
        except ValueError:
            contradiction_refused = True

        retrieves: list[str] = []

        def retrieve(provider_id: str, _timeout: float) -> dict[str, Any]:
            retrieves.append(provider_id)
            return {"id": provider_id, "status": "completed", "output": []}

        first = reconcile_provider_cycle(
            root, observed_at="1970-01-01T00:00:15Z", retrieve=retrieve,
        )
        # The production command performs deterministic local ingestion/fan-in
        # between bounded retrieval waves. Model that provider-free checkpoint
        # from the exact durable completed-action evidence before restoring a
        # fresh worker for the remaining due members.
        restored = load_json(root / "run.json")
        completed = set(first["cycle"]["completed_action_ids"])
        for action in restored["spend_ledger"]["actions"]:
            if action["action_id"] in completed:
                action["state"] = "REPORTED"
                action["reported"] = {"estimated_micro_usd": 0}
        restored["state_revision"] += 1
        (root / "run.json").write_text(
            json.dumps(restored, indent=2) + "\n", encoding="utf-8"
        )
        (root / "public-run.json").write_text(
            json.dumps(public_run_state(restored), indent=2) + "\n", encoding="utf-8"
        )
        write_workspace_snapshot(root)
        second = reconcile_provider_cycle(
            root, observed_at="1970-01-01T00:01:00Z", retrieve=retrieve,
        )
        evidence = list((root / "lifecycle" / "provider-reconciliation").glob("*.response.json"))
        assertions = {
            "six_member_create_detach": (
                result["outcome"] == "detached_provider_pending"
                and len(creates) == 6 and len(set(creates)) == 6
            ),
            "not_due_release": (
                not_due["execution_branch"]["command"] == "provider_reconciliation_cycle"
                and not not_due["execution_branch"]["eligible_now"]
                and not_due["terminal"]["local_continuation_remains"] is False
            ),
            "direct_due_selection": (
                due["execution_branch"]["command"] == "provider_reconciliation_cycle"
                and due["execution_branch"]["eligible_now"]
                and len(due["execution_branch"]["action_ids"]) == 4
            ),
            "bounded_four_then_two_retrieval": (
                first["cycle"]["provider_retrieval_count"] == 4
                and second["cycle"]["provider_retrieval_count"] == 2
            ),
            "all_six_durable_fan_in_evidence": len(evidence) == 6,
            "no_duplicate_create_or_retrieval": (
                len(creates) == len(set(creates)) == 6
                and len(retrieves) == len(set(retrieves)) == 6
            ),
            "contradictory_projection_refused": contradiction_refused,
        }
        receipt = {
            "schema_version": RECEIPT_SCHEMA,
            "status": "pass" if all(assertions.values()) else "fail",
            "qualification_only": True, "provider_free": True,
            "network_required": False, "production_authority": False,
            "create_count": len(creates), "retrieve_count": len(retrieves),
            "first_cycle_retrieval_count": first["cycle"]["provider_retrieval_count"],
            "second_cycle_retrieval_count": second["cycle"]["provider_retrieval_count"],
            "not_due_branch": not_due["execution_branch"],
            "due_branch": due["execution_branch"], "assertions": assertions,
        }
        receipt["receipt_sha256"] = _sha(receipt)
        if receipt["status"] != "pass":
            raise RuntimeError(
                "Provider-pending lifecycle qualification failed: "
                f"{assertions}; first={first['cycle']}; second={second['cycle']}; "
                f"retrieves={retrieves}; evidence={len(evidence)}"
            )
        return receipt


def main() -> None:
    print(json.dumps(run_provider_pending_lifecycle_qualification(), indent=2))


if __name__ == "__main__":
    main()
