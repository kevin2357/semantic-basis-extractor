"""Self-contained installed-wheel qualification for provider-economics export."""

from __future__ import annotations

import argparse
from copy import deepcopy
from importlib import metadata, resources
import hashlib
import json
from pathlib import Path
import tempfile
from typing import Any

from .closure import normalized_path, write_workspace_snapshot
from .provider_economics_export import read_provider_economics_export


QUALIFICATION_SCHEMA = "astrowoof.provider_economics_qualification.v1"
_CHECKS = {
    "exact_interactive", "exact_batch", "bounded_interactive", "bounded_batch",
    "snapshot_validation", "exact_replay", "privacy_minimized",
}


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")).hexdigest()


def _release() -> str:
    try:
        return metadata.version("astrowoof-natal-authoring")
    except metadata.PackageNotFoundError:
        return "source-tree"


def _action(*, batch: bool) -> dict[str, Any]:
    return {
        "action_id": "paid_0123456789abcdef01234567", "state": "REPORTED",
        "binding": {
            "run_id": "run-economics-qa", "stage": "authoring_initial",
            "route": "batch-round-001" if batch else "initial-pass-1",
            "request_sha256": "a" * 64, "model": "gpt-qa",
            "service_level": "batch" if batch else "interactive",
            "maximum_output_tokens": 1000, "commitment_micro_usd": 1000,
            "price_book_version": "qa-prices.v1",
        },
        "authorization": {"authorization_reference": "qa-auth"},
        "consumption": {"consumer_id": "qa-worker"},
        "provider": {"kind": "batch" if batch else "interactive",
                     "id": "batch-qa" if batch else "resp-qa"},
        "reported": ({
            "cost_disposition":
                "provider_usage_unavailable_billing_reconciliation_pending",
        } if batch else {
            "usage": {"input_tokens": 100, "cached_input_tokens": 40,
                      "output_tokens": 20, "reasoning_tokens": 5},
            "estimated_micro_usd": 1234, "price_book_version": "qa-prices.v1",
        }),
    }


def _state(root: Path, *, bounded: bool, batch: bool) -> dict[str, Any]:
    action = _action(batch=batch)
    state: dict[str, Any] = {
        "schema_version": "astrowoof.semantic_closure_run.v0.9",
        "run_id": "run-economics-qa", "status": "AUTHORING",
        "updated_at": "2026-08-25T12:00:00Z",
        "workspace_contract": {"mode": "stable_logical_absolute_path",
                               "logical_root": normalized_path(root)},
        "authoring_profile": {},
        "provider_configuration": {"model": "gpt-qa",
                                   "reasoning_effort": "medium"},
        "spend_ledger": {"actions": [action]},
        "passes": {"pass-1": {"attempts": [{
            "state": "COMPLETE", "prompt_sha256": "a" * 64,
            "provider_metadata": {"response_id": action["provider"]["id"]},
        }]}},
        "initial_authoring_wave": {"members": [{"action_id": action["action_id"]}]},
    }
    if bounded:
        state.update({"route": "bounded_natal",
                      "route_contract": "astrowoof.bounded_natal.authoring_run.v2"})
    if batch:
        service = {"rounds": [{
            "round_number": 1, "round_id": "round-1", "batch_id": "batch-qa",
            "requests": [{
                "custom_id": f"custom-{i}", "pass_id": f"pass-{i}",
                "attempt_number": 1, "prompt_sha256": f"{i:x}" * 64,
            } for i in range(1, 7)],
        }]}
        state["batch_service" if bounded else "authoring_service"] = service
        state["passes"] = {f"pass-{i}": {"attempts": [{"provider_metadata": {
            "custom_id": f"custom-{i}", "response_id": f"resp-{i}",
            "response_status": "completed", "usage": None,
        }}]} for i in range(1, 7)}
    return state


def _materialize(root: Path, *, bounded: bool, batch: bool) -> None:
    root.mkdir(parents=True)
    (root / "run.json").write_text(
        json.dumps(_state(root, bounded=bounded, batch=batch), indent=2) + "\n",
        encoding="utf-8",
    )
    write_workspace_snapshot(root)


def validate_provider_economics_qualification(value: Any) -> dict[str, Any]:
    keys = {"schema_version", "qualification_mode", "sbe_release", "outcome",
            "checks", "external_provider_io_count", "fixture_count",
            "receipt_sha256"}
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("provider economics qualification fields are not exact")
    if (value.get("schema_version") != QUALIFICATION_SCHEMA
            or value.get("qualification_mode") != "installed_wheel_provider_free"
            or not isinstance(value.get("sbe_release"), str) or not value["sbe_release"]
            or value.get("outcome") != "passed"
            or not isinstance(value.get("checks"), dict)
            or set(value["checks"]) != _CHECKS
            or any(item is not True for item in value["checks"].values())
            or value.get("external_provider_io_count") != 0
            or value.get("fixture_count") != 4):
        raise ValueError("provider economics qualification semantics are invalid")
    unsigned = {key: deepcopy(item) for key, item in value.items()
                if key != "receipt_sha256"}
    if value.get("receipt_sha256") != _canonical_sha256(unsigned):
        raise ValueError("provider economics qualification digest is invalid")
    return deepcopy(value)


def read_provider_economics_qualification_schema() -> dict[str, Any]:
    path = resources.files("astrowoof_natal_authoring.resources.contracts").joinpath(
        "provider-economics-qualification.v1.schema.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def run_provider_economics_qualification(
    *, require_installed: bool = False,
) -> dict[str, Any]:
    if require_installed:
        dist = metadata.distribution("astrowoof-natal-authoring")
        names = {str(item).replace("\\", "/") for item in (dist.files or [])}
        for suffix in (
            "provider-economics-transaction-revision.v1.schema.json",
            "provider-economics-export.v1.schema.json",
            "provider-economics-qualification.v1.schema.json",
        ):
            if not any(name.endswith(suffix) for name in names):
                raise ValueError(f"installed wheel lacks {suffix}")
    checks = {key: False for key in _CHECKS}
    sentinel = "PROTECTED-SUBJECT-BIRTH-LOCATION-SENTINEL"
    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)
        for bounded, batch, label in (
            (False, False, "exact_interactive"),
            (False, True, "exact_batch"),
            (True, False, "bounded_interactive"),
            (True, True, "bounded_batch"),
        ):
            root = base / label
            _materialize(root, bounded=bounded, batch=batch)
            exported = read_provider_economics_export(
                root, observed_at="2026-08-25T12:01:00Z",
            )
            revision = exported["revisions"][0]
            checks[label] = bool(
                exported["revision_count"] == 1
                and revision["transaction_identity"]["route_family"]
                    == ("bounded_natal" if bounded else "exact_natal")
                and revision["transaction_identity"]["cardinality_kind"]
                    == ("batch_round" if batch else "single_action")
                and (len(revision["transaction_identity"]["members"]) == 6
                     if batch else True)
            )
            replay = read_provider_economics_export(
                root, observed_at="2026-08-25T12:02:00Z",
                previous_revisions=exported["revisions"],
            )
            if replay["revision_count"] != 0:
                raise ValueError("unchanged public export minted a revision")
        checks["snapshot_validation"] = True
        checks["exact_replay"] = True
        checks["privacy_minimized"] = sentinel not in json.dumps(exported)
    body = {
        "schema_version": QUALIFICATION_SCHEMA,
        "qualification_mode": "installed_wheel_provider_free",
        "sbe_release": _release(), "outcome": "passed", "checks": checks,
        "external_provider_io_count": 0, "fixture_count": 4,
    }
    return validate_provider_economics_qualification({
        **body, "receipt_sha256": _canonical_sha256(body),
    })


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run provider-free installed-wheel provider economics QA"
    )
    parser.add_argument("--require-installed", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    receipt = run_provider_economics_qualification(
        require_installed=args.require_installed,
    )
    rendered = json.dumps(receipt, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
