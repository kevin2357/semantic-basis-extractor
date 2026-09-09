"""Read-only runtime ingress for native editorial-review packet construction."""

from __future__ import annotations

from pathlib import Path
from hashlib import sha256
import json
from typing import Any, Callable, Mapping

from .editorial_review_fixtures import (
    build_editorial_review_capture_status,
    validate_editorial_review_packet,
)
from .native_transitions import NativeTransitionResultView, read_native_transition_result
from .editorial_review_contracts import (
    canonical_editorial_review_json,
    derive_artifact_id,
    derive_decision_id,
    derive_editorial_review_id,
    derive_finding_id,
    derive_packet_id,
    derive_projection_id,
    derive_validation_id,
    digest_without,
    editorial_review_sha256,
)


DELIVERY_RESULT_VERSION = "astrowoof.native_execution_result.v0.1"
REVIEW_RESULT_VERSION = "astrowoof.native_execution_result.v0.2"
RECEIPT_VERSION = "astrowoof.native_publication_receipt.v0.1"


def read_eligible_editorial_result(
    run_dir: Path | str,
    result_id: str,
    *,
    exact_reader: Callable[[Path, str], NativeTransitionResultView] = read_native_transition_result,
) -> tuple[str, NativeTransitionResultView | dict[str, Any]]:
    """Read one explicit result ID and classify the closed editorial branches.

    The exact reader always runs before eligibility dispatch.  This helper does
    not discover results and returns no partial packet when the validated result
    falls outside the closed capture surface.
    """
    root = Path(run_dir).resolve()
    view = exact_reader(root, result_id)
    result: Mapping[str, Any] = view["result"]
    receipt: Mapping[str, Any] = view["receipt"]
    if receipt.get("schema_version") != RECEIPT_VERSION:
        return "unsupported", build_editorial_review_capture_status(
            "unsupported_result_version"
        )
    version = result.get("schema_version")
    outcome = result.get("outcome")
    route = result.get("route_binding") or {}
    if version == DELIVERY_RESULT_VERSION and outcome == "delivery_complete":
        return "delivery", view
    if (
        version == REVIEW_RESULT_VERSION
        and outcome == "review_required"
        and route.get("route_family") == "exact_natal"
        and route.get("provider_mechanism") == "response"
        and result.get("custody_finality") == "final"
    ):
        return "editorial_review", view
    if version not in {DELIVERY_RESULT_VERSION, REVIEW_RESULT_VERSION}:
        reason = "unsupported_result_version"
    else:
        reason = "ineligible_route"
    return "unsupported", build_editorial_review_capture_status(reason)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Editorial runtime evidence must be a JSON object")
    return value


def _logical_path(root: Path, logical_root: str, value: str) -> Path:
    logical = Path(value.replace("\\", "/"))
    if not logical.is_absolute():
        candidate = (root / logical).resolve()
        if root not in candidate.parents and candidate != root:
            raise ValueError("Editorial evidence path escapes the restored workspace")
        return candidate
    base = Path(logical_root.replace("\\", "/"))
    try:
        relative = logical.relative_to(base)
    except ValueError as exc:
        raise ValueError("Editorial evidence path escapes the logical workspace") from exc
    candidate = (root / relative).resolve()
    if root not in candidate.parents and candidate != root:
        raise ValueError("Editorial evidence path escapes the restored workspace")
    return candidate


def _tree_digest(path: Path) -> str:
    members = []
    for item in sorted((p for p in path.rglob("*") if p.is_file()), key=lambda p: p.relative_to(path).as_posix()):
        members.append({
            "path": item.relative_to(path).as_posix(),
            "sha256": sha256(item.read_bytes()).hexdigest(),
        })
    if not members:
        raise ValueError("Editorial candidate workspace is empty")
    return sha256(canonical_editorial_review_json(members)).hexdigest()


def collect_editorial_review_runtime_evidence(
    run_dir: Path | str,
    result_id: str,
    *,
    exact_reader: Callable[[Path, str], NativeTransitionResultView] = read_native_transition_result,
) -> tuple[str, dict[str, Any]]:
    """Collect bounded identity evidence after exact-result eligibility succeeds."""
    root = Path(run_dir).resolve()
    branch, selected = read_eligible_editorial_result(
        root, result_id, exact_reader=exact_reader,
    )
    if branch == "unsupported":
        return branch, selected
    view = selected
    result = view["result"]
    receipt = view["receipt"]
    state = _load(root / "run.json")
    if state.get("run_id") != result.get("run_id"):
        return "unsupported", build_editorial_review_capture_status(
            "contradictory_native_evidence"
        )
    if state.get("service_level") != "interactive" or len(state.get("subjects") or {}) != 1:
        return "unsupported", build_editorial_review_capture_status("ineligible_route")
    subject_id, subject = next(iter(state["subjects"].items()))
    post_checkpoint = result.get("post_checkpoint") or {}
    provenance = state.get("provenance") or {}
    runtime = provenance.get("runtime") or {}
    resources = provenance.get("resources") or {}
    profile = state.get("authoring_profile") or {}
    if (
        state.get("state_revision") != post_checkpoint.get("native_state_revision")
        or post_checkpoint.get("checkpoint_basis_sha256") != receipt.get("checkpoint_basis_sha256")
        or not isinstance(receipt.get("snapshot_sha256"), str)
        or result.get("sbe_release") != runtime.get("version")
        or runtime.get("distribution") != "astrowoof-natal-authoring"
        or not isinstance(profile.get("profile_id"), str)
        or not isinstance(resources.get("aggregate_sha256"), str)
    ):
        return "unsupported", build_editorial_review_capture_status(
            "contradictory_native_evidence"
        )
    logical_root = receipt["logical_workspace_root"]
    action_rows = (state.get("spend_ledger") or {}).get("actions", [])
    actions = {item.get("action_id"): item for item in action_rows}
    if len(actions) != len(action_rows) or None in actions:
        return "unsupported", build_editorial_review_capture_status(
            "contradictory_native_evidence"
        )
    result_dispositions: dict[tuple[str, str], Mapping[str, Any]] = {}
    if branch == "editorial_review":
        dispositions = result.get("action_dispositions")
        if not isinstance(dispositions, list):
            return "unsupported", build_editorial_review_capture_status(
                "incomplete_native_evidence"
            )
        for disposition in dispositions:
            key = (disposition.get("action_id"), disposition.get("binding_sha256"))
            if None in key or key in result_dispositions:
                return "unsupported", build_editorial_review_capture_status(
                    "contradictory_native_evidence"
                )
            result_dispositions[key] = disposition
    pass_attempts = []
    for record in sorted((state.get("passes") or {}).values(), key=lambda item: item["pass_number"]):
        for attempt in record.get("attempts") or []:
            qa = attempt.get("qa") or {}
            report = qa.get("report") or {}
            workspace = _logical_path(root, logical_root, attempt["response_workspace"])
            action = actions.get(attempt.get("paid_action_id"))
            if action is None:
                raise ValueError("Pass attempt has no exact paid-action join")
            binding = action.get("binding") or {}
            binding_digest = sha256(canonical_editorial_review_json(binding)).hexdigest()
            if branch == "editorial_review" and (
                action["action_id"], binding_digest
            ) not in result_dispositions:
                return "unsupported", build_editorial_review_capture_status(
                    "contradictory_native_evidence"
                )
            provider = action.get("provider") or {}
            report_path = workspace.parents[1] / "authoring-pass-acceptance.json"
            authored_path = workspace.parents[1] / "openai-authored-fields.json"
            if not report_path.is_file() or not authored_path.is_file():
                raise ValueError("Pass attempt evidence is incomplete")
            pass_attempts.append({
                "pass_id": record["pass_id"], "pass_number": record["pass_number"],
                "attempt_number": attempt["attempt_number"], "state": attempt["state"],
                "accepted": bool(qa.get("accepted") and report.get("status") == "accept"),
                "source_sha256": record["source_sha256"],
                "candidate_workspace_id": attempt["response_workspace"],
                "candidate_workspace_sha256": _tree_digest(workspace),
                "authored_claim_set_sha256": sha256(authored_path.read_bytes()).hexdigest(),
                "qa_report_sha256": sha256(report_path.read_bytes()).hexdigest(),
                "paid_action_id": action["action_id"],
                "binding_sha256": binding_digest,
                "request_sha256": binding["request_sha256"],
                "provider_response_id": provider.get("id"),
            })
    if len({item["pass_number"] for item in pass_attempts if item["accepted"]}) != 6:
        return "unsupported", build_editorial_review_capture_status(
            "incomplete_native_evidence"
        )
    optional_history = bool(subject.get("polish_attempts") or subject.get("qualitative_review"))
    initial_assembled_deck = subject.get("initial_assembled_deck")
    initial_assembled_digest = subject.get("initial_assembled_deck_sha256")
    if optional_history:
        if not isinstance(initial_assembled_deck, str) or not isinstance(initial_assembled_digest, str):
            return "unsupported", build_editorial_review_capture_status(
                "incomplete_native_evidence"
            )
        initial_path = _logical_path(root, logical_root, initial_assembled_deck)
        if not initial_path.is_file():
            return "unsupported", build_editorial_review_capture_status(
                "incomplete_native_evidence"
            )
        if editorial_review_sha256(_load(initial_path)) != initial_assembled_digest:
            return "unsupported", build_editorial_review_capture_status(
                "contradictory_native_evidence"
            )
    return branch, {
        "result": result, "receipt": receipt, "subject_id": subject_id,
        "state_revision": state.get("state_revision"),
        "native_correlations": {
            "native_run_id": state["run_id"], "subject_id": subject_id,
            "native_state_revision": state["state_revision"],
            "checkpoint_basis_sha256": post_checkpoint["checkpoint_basis_sha256"],
            "snapshot_sha256": receipt["snapshot_sha256"],
        },
        "producer": {
            "package": "astrowoof-natal-authoring", "version": result["sbe_release"],
            "profile_id": profile["profile_id"],
            "profile_sha256": sha256(canonical_editorial_review_json(profile)).hexdigest(),
            "resource_set_sha256": resources["aggregate_sha256"],
        },
        "pass_attempts": pass_attempts,
        "assembly": {
            "deck_path": subject.get("deck"),
            "assembly_report_path": subject.get("assembly_report"),
            "initial_assembled_deck_path": initial_assembled_deck,
            "initial_assembled_deck_sha256": initial_assembled_digest,
        },
        "polish_attempts": list(subject.get("polish_attempts") or []),
        "qualitative_review": subject.get("qualitative_review"),
    }


def _artifact(packet_id: str, packet: Mapping[str, Any], kind: str,
              payload: Mapping[str, Any], uses: list[dict[str, Any]]) -> dict[str, Any]:
    object_digest = editorial_review_sha256(payload)
    value = {
        "schema_version": "editorial_review_artifact.v2",
        "artifact_id": derive_artifact_id(packet_id, kind, object_digest),
        "artifact_sha256": "pending", "artifact_kind": kind,
        "object_sha256": object_digest, "media_type": "application/json",
        "native_correlations": {
            "native_run_id": packet["native_correlations"]["native_run_id"],
            "subject_id": packet["native_correlations"]["subject_id"],
            "packet_id": packet_id,
        },
        "relations": {"uses": uses}, kind: dict(payload),
    }
    value["artifact_sha256"] = digest_without(value, "artifact_sha256")
    return value


def _projection(packet: Mapping[str, Any], kind: str,
                member: Mapping[str, Any], ordinal: int) -> dict[str, Any]:
    native_id = member[f"{kind}_id"]
    return {
        "schema_version": "editorial_review_projection.v5",
        "projection_id": derive_projection_id(packet["packet_id"], kind, native_id),
        "projection_kind": kind, "packet_id": packet["packet_id"],
        "packet_sha256": packet["packet_sha256"], "owner_ordinal": ordinal,
        "projected_native_id": native_id,
        "projected_native_sha256": editorial_review_sha256(member),
        kind: dict(member),
    }


def build_editorial_review_runtime_capture(
    run_dir: Path | str,
    result_id: str,
    *,
    exact_reader: Callable[[Path, str], NativeTransitionResultView] = read_native_transition_result,
) -> tuple[str, dict[str, Any]]:
    """Build the first closed runtime packet branch or one typed no-packet status.

    This first branch intentionally accepts only a completed six-pass lineage
    with no optional-stage records.  Richer ordinary-live-exact histories are
    refused as incomplete until their persisted stage evidence is translated;
    they are never approximated by a partial packet.
    """
    root = Path(run_dir).resolve()
    branch, evidence = collect_editorial_review_runtime_evidence(
        root, result_id, exact_reader=exact_reader,
    )
    if branch == "unsupported":
        return branch, evidence
    try:
        result = evidence["result"]
        receipt = evidence["receipt"]
        logical_root = receipt["logical_workspace_root"]
        state = _load(root / "run.json")
        subject = state["subjects"][evidence["subject_id"]]
        deck_path = _logical_path(root, logical_root, subject["deck"])
        report_path = _logical_path(root, logical_root, subject["assembly_report"])
        selected_deck = _load(deck_path)
        initial_path_value = evidence["assembly"].get("initial_assembled_deck_path")
        initial_path = (
            _logical_path(root, logical_root, initial_path_value)
            if evidence["polish_attempts"] else deck_path
        )
        initial_deck = _load(initial_path)
        if not report_path.is_file():
            raise ValueError("Initial assembly report is absent")
        deck_digest = editorial_review_sha256(selected_deck)
        disposition = "delivered" if branch == "delivery" else "retained_for_editorial_review"
        terminal_id = derive_editorial_review_id(
            "erts", "terminal_selection_id.v1",
            [result["result_id"], evidence["subject_id"], deck_digest, disposition],
        )
        packet: dict[str, Any] = {
            "schema_version": "editorial_review_packet.v5",
            "eligibility": {
                "route": "ordinary_live_exact",
                "terminal_outcome": "delivery_complete" if branch == "delivery" else "editorial_review_required",
                "final_custody": "resolved",
                "native_result_schema_version": result["schema_version"],
                "native_result_id": result["result_id"],
                "native_result_sha256": result["result_sha256"],
                "canonical_receipt_schema_version": receipt["schema_version"],
                "canonical_receipt_id": receipt["receipt_id"],
                "canonical_receipt_sha256": receipt["receipt_sha256"],
            },
            "native_correlations": evidence["native_correlations"],
            "producer": evidence["producer"],
            "terminal_selection": {
                "terminal_selection_id": terminal_id, "selection_origin": "assembly",
                "selected_deck": {}, "delivery_disposition": disposition,
                "validation_ids": [],
            },
        }
        packet["packet_id"] = derive_packet_id(packet)
        packet_id = packet["packet_id"]
        deck_payloads: dict[str, dict[str, Any]] = {}
        def deck_reference(value: Mapping[str, Any]) -> dict[str, str]:
            digest = editorial_review_sha256(value)
            deck_payloads[digest] = dict(value)
            return {
                "artifact_id": derive_artifact_id(packet_id, "assembled_deck", digest),
                "sha256": digest,
            }
        initial_deck_ref = deck_reference(initial_deck)
        selected_deck_ref = deck_reference(selected_deck)
        packet["terminal_selection"]["selected_deck"] = dict(selected_deck_ref)
        if branch == "delivery":
            packet["terminal_selection"]["delivered_deck"] = dict(selected_deck_ref)

        decisions: list[dict[str, Any]] = []
        findings: list[dict[str, Any]] = []
        validations: list[dict[str, Any]] = []
        response_payloads: dict[str, dict[str, Any]] = {}
        actions = {
            item.get("action_id"): item
            for item in (state.get("spend_ledger") or {}).get("actions", [])
        }
        disposition_keys = {
            (item.get("action_id"), item.get("binding_sha256"))
            for item in result.get("action_dispositions") or []
        }

        def action_for_response(response_id: str) -> Mapping[str, Any]:
            matches = [
                item for item in actions.values()
                if (item.get("provider") or {}).get("id") == response_id
            ]
            if len(matches) != 1:
                raise ValueError("Provider response does not select one exact action")
            return matches[0]

        def packet_action(action_state: Mapping[str, Any], response_id: str,
                          response: Mapping[str, Any], kind: str) -> dict[str, Any]:
            binding = action_state.get("binding") or {}
            binding_digest = sha256(canonical_editorial_review_json(binding)).hexdigest()
            if branch == "editorial_review" and (
                action_state["action_id"], binding_digest
            ) not in disposition_keys:
                raise ValueError("Optional-stage action disposition is contradictory")
            return {
                "paid_action_id": action_state["action_id"], "action_kind": kind,
                "binding_sha256": binding_digest,
                "request_sha256": binding["request_sha256"],
                "provider_response_id": response_id,
                "provider_response_sha256": editorial_review_sha256(response),
            }
        prior_by_pass: dict[int, dict[str, Any]] = {}
        ordered_attempts = sorted(
            evidence["pass_attempts"],
            key=lambda item: (
                0 if item["attempt_number"] == 1 else 1,
                item["attempt_number"], item["pass_number"],
            ),
        )
        for row in ordered_attempts:
            attempt_root = _logical_path(root, logical_root, row["candidate_workspace_id"]).parents[1]
            response = _load(attempt_root / "openai-response.json")
            response_id = row["provider_response_id"]
            if not response_id or response.get("id") != response_id:
                raise ValueError("Provider response identity is incomplete")
            response_payloads[response_id] = response
            action = {
                "paid_action_id": row["paid_action_id"],
                "action_kind": "initial_pass" if row["attempt_number"] == 1 else "ordinary_creative_retry",
                "binding_sha256": row["binding_sha256"],
                "request_sha256": row["request_sha256"],
                "provider_response_id": response_id,
                "provider_response_sha256": editorial_review_sha256(response),
            }
            prior = prior_by_pass.get(row["pass_number"])
            transition = {
                "relation_kind": "initial_pass_materialization" if prior is None else "pass_retry_materialization",
                "attempt_identity": f'{row["pass_id"]}:attempt:{row["attempt_number"]}',
                "released_pass_identity": row["pass_id"],
                "source_basis_sha256": row["source_sha256"] if prior is None else prior["transition"]["candidate_workspace_sha256"],
                "candidate_workspace_id": row["candidate_workspace_id"],
                "candidate_workspace_sha256": row["candidate_workspace_sha256"],
                "authored_claim_set_sha256": row["authored_claim_set_sha256"],
                "qa_report_sha256": row["qa_report_sha256"],
                "acceptance_outcome": "accepted" if row["accepted"] else "rejected",
                "materialization_outcome": "materialized",
            }
            if row["accepted"]:
                transition.update({
                    "accepted_workspace_id": row["candidate_workspace_id"],
                    "accepted_workspace_sha256": row["candidate_workspace_sha256"],
                })
            decision = {
                "schema_version": "editorial_review_decision.v5", "decision_id": "pending",
                "decision_ordinal": len(decisions),
                "stage": "initial_pass" if prior is None else "creative_retry",
                "stage_attempt": row["attempt_number"], "initial_pass_index": row["pass_number"],
                "released_pass_identity": row["pass_id"], "subject_id": evidence["subject_id"],
                "action": action, "transition": transition,
                "finding_ids": [], "validation_ids": [],
            }
            decision["decision_id"] = derive_decision_id(packet_id, decision)
            if prior is not None:
                transition.update({
                    "predecessor_decision_id": prior["decision_id"],
                    "predecessor_attempt_identity": prior["transition"]["attempt_identity"],
                    "predecessor_acceptance_outcome": prior["transition"]["acceptance_outcome"],
                    "predecessor_qa_report_sha256": prior["transition"]["qa_report_sha256"],
                })
            prior_by_pass[row["pass_number"]] = decision
            decisions.append(decision)

        current_deck = initial_deck
        current_ref = initial_deck_ref
        for attempt in evidence["polish_attempts"]:
            attempt_number = int(attempt["attempt_number"])
            validation_path = _logical_path(root, logical_root, attempt["validation_report"])
            attempt_root = validation_path.parent
            candidate_path = attempt_root / f"natal.{evidence['subject_id']}.cards.json"
            materialized = candidate_path.is_file()
            candidate = _load(candidate_path) if materialized else None
            candidate_ref = deck_reference(candidate) if candidate is not None else None
            adopted = bool(attempt.get("accepted") or attempt.get("improved"))
            if adopted and candidate_ref is None:
                raise ValueError("Adopted optional-stage candidate is absent")
            output_ref = candidate_ref if adopted else current_ref
            action_state = actions.get(attempt.get("paid_action_id"))
            if action_state is None:
                raise ValueError("Optional-stage attempt has no exact paid action")
            metadata = attempt.get("provider_metadata") or {}
            response_id = metadata.get("response_id") or (action_state.get("provider") or {}).get("id")
            response = _load(attempt_root / "openai-response.json")
            if not response_id or response.get("id") != response_id:
                raise ValueError("Optional-stage response identity is incomplete")
            response_payloads[response_id] = response
            action = packet_action(
                action_state, response_id, response, "ordinary_optional_stage"
            )
            transition = {
                "relation_kind": "whole_deck_transition",
                "input_deck": dict(current_ref),
                "output_deck": dict(output_ref),
                "materialization_outcome": "materialized" if materialized else "not_materialized",
                "adoption_outcome": "candidate_adopted" if adopted else "candidate_not_adopted",
            }
            if candidate_ref is not None:
                transition["candidate_deck"] = dict(candidate_ref)
            decision = {
                "schema_version": "editorial_review_decision.v5", "decision_id": "pending",
                "decision_ordinal": len(decisions), "stage": "polish",
                "stage_attempt": attempt_number, "subject_id": evidence["subject_id"],
                "action": action, "transition": transition,
                "finding_ids": [], "validation_ids": [],
            }
            decision["decision_id"] = derive_decision_id(packet_id, decision)
            report_findings: list[dict[str, Any]] = []
            validation_report = _load(validation_path)
            lint_report = _load(_logical_path(root, logical_root, attempt["lint_report"]))
            for severity, collection in (
                ("error", validation_report.get("errors") or []),
                ("warning", validation_report.get("warnings") or []),
            ):
                for item in collection:
                    report_findings.append({
                        "kind": "deterministic_qa", "code": f"validation_{severity}",
                        "severity": severity, "message": str(item),
                        "population": {"mode": "not_claim_scoped"},
                        "source": item,
                    })
            for deck_report in lint_report.get("decks") or []:
                for item in deck_report.get("warnings") or []:
                    details = item.get("details") or {}
                    claim_ids = details.get("claim_ids") or []
                    population = (
                        {
                            "mode": "claim_ids",
                            "evaluated_count": int(deck_report.get("reader_facing_field_count") or 0),
                            "affected_count": len(claim_ids),
                            "affected_claim_ids": list(claim_ids),
                        }
                        if claim_ids else {"mode": "not_claim_scoped"}
                    )
                    report_findings.append({
                        "kind": "lint", "code": item.get("code") or "lint_finding",
                        "severity": "warning", "message": str(item.get("message") or item),
                        "population": population, "source": item,
                    })
            for local_ordinal, spec in enumerate(report_findings):
                finding = {
                    "schema_version": "editorial_review_finding.v1", "finding_id": "pending",
                    "decision_id": decision["decision_id"],
                    "decision_ordinal": decision["decision_ordinal"],
                    "finding_kind": spec["kind"], "code": spec["code"],
                    "severity": spec["severity"], "phase": "post_polish",
                    "message": spec["message"][:1024], "population": spec["population"],
                    "field_context": [], "evidence_sha256": editorial_review_sha256(spec["source"]),
                }
                finding["finding_id"] = derive_finding_id(
                    decision["decision_id"], finding, local_ordinal
                )
                decision["finding_ids"].append(finding["finding_id"])
                findings.append(finding)
            validation = {
                "schema_version": "editorial_review_validation.v1", "validation_id": "pending",
                "owner_kind": "decision", "decision_id": decision["decision_id"],
                "decision_ordinal": decision["decision_ordinal"],
                "validation_kind": "candidate_adoption",
                "code": "polish_candidate_evaluated",
                "outcome": "passed" if adopted else "failed",
                "path": f'$.lineage.decisions[{decision["decision_ordinal"]}]',
                "report_id": attempt["validation_report"],
                "report_sha256": sha256(validation_path.read_bytes()).hexdigest(),
                "finding_ids": list(decision["finding_ids"]),
            }
            validation["validation_id"] = derive_validation_id(
                decision["decision_id"], validation, 0
            )
            decision["validation_ids"].append(validation["validation_id"])
            validations.append(validation)
            decisions.append(decision)
            if adopted:
                current_deck = candidate
                current_ref = candidate_ref

        qualitative = evidence.get("qualitative_review") or {}
        critic_record = qualitative.get("critic") if isinstance(qualitative, dict) else None
        if critic_record:
            critic_artifact_path = _logical_path(root, logical_root, critic_record["artifact"])
            critic_artifact = _load(critic_artifact_path)
            critic_provenance = critic_artifact.get("provenance") or {}
            raw_descriptor = critic_provenance.get("raw_provider_response") or {}
            response_id = (critic_provenance.get("provider") or {}).get("response_id")
            response_path = _logical_path(root, logical_root, raw_descriptor["path"])
            response = _load(response_path)
            if sha256(response_path.read_bytes()).hexdigest() != raw_descriptor.get("sha256"):
                raise ValueError("Critic response artifact digest is contradictory")
            action_state = action_for_response(response_id)
            response_payloads[response_id] = response
            decision = {
                "schema_version": "editorial_review_decision.v5", "decision_id": "pending",
                "decision_ordinal": len(decisions), "stage": "critic", "stage_attempt": 1,
                "subject_id": evidence["subject_id"],
                "action": packet_action(action_state, response_id, response, "ordinary_optional_stage"),
                "transition": {
                    "relation_kind": "whole_deck_transition",
                    "input_deck": dict(current_ref), "output_deck": dict(current_ref),
                    "materialization_outcome": "not_applicable",
                    "adoption_outcome": "not_applicable",
                },
                "finding_ids": [], "validation_ids": [],
            }
            decision["decision_id"] = derive_decision_id(packet_id, decision)
            for source_finding in (critic_artifact.get("critic") or {}).get("findings") or []:
                contexts = []
                for field_path in source_finding.get("target_paths") or []:
                    value: Any = current_deck
                    try:
                        for part in field_path.split("."):
                            value = value[int(part)] if isinstance(value, list) else value[part]
                    except (KeyError, IndexError, TypeError, ValueError):
                        raise ValueError("Critic finding path is absent from criticized deck")
                    contexts.append({
                        "field_path": field_path, "before_state": "present",
                        "before": str(value), "after_state": "present", "after": str(value),
                    })
                finding = {
                    "schema_version": "editorial_review_finding.v1", "finding_id": "pending",
                    "decision_id": decision["decision_id"],
                    "decision_ordinal": decision["decision_ordinal"],
                    "finding_kind": "editorial",
                    "code": source_finding["quality_dimension"],
                    "severity": "advisory" if source_finding.get("priority") == "low" else "warning",
                    "phase": "post_critic", "message": source_finding["diagnosis"][:1024],
                    "population": {"mode": "not_claim_scoped"},
                    "field_context": contexts,
                    "evidence_sha256": editorial_review_sha256(source_finding),
                }
                finding["finding_id"] = derive_finding_id(
                    decision["decision_id"], finding, len(decision["finding_ids"])
                )
                decision["finding_ids"].append(finding["finding_id"])
                findings.append(finding)
            decisions.append(decision)

        candidate_record = qualitative.get("candidate") if isinstance(qualitative, dict) else None
        if candidate_record and (candidate_record.get("provider_metadata") or {}).get("response_id"):
            response_id = candidate_record["provider_metadata"]["response_id"]
            candidate_root = root / "final" / evidence["subject_id"] / "qualitative" / "candidate"
            response = _load(candidate_root / "openai-response.json")
            action_state = action_for_response(response_id)
            response_payloads[response_id] = response
            candidate_path_value = candidate_record.get("artifact")
            candidate = (
                _load(_logical_path(root, logical_root, candidate_path_value))
                if candidate_path_value else None
            )
            candidate_ref = deck_reference(candidate) if candidate is not None else None
            transition = {
                "relation_kind": "whole_deck_transition",
                "input_deck": dict(current_ref), "output_deck": dict(current_ref),
                "materialization_outcome": "materialized" if candidate_ref else "not_materialized",
                "adoption_outcome": "candidate_not_adopted",
            }
            if candidate_ref:
                transition["candidate_deck"] = dict(candidate_ref)
            decision = {
                "schema_version": "editorial_review_decision.v5", "decision_id": "pending",
                "decision_ordinal": len(decisions), "stage": "candidate", "stage_attempt": 1,
                "subject_id": evidence["subject_id"],
                "action": packet_action(action_state, response_id, response, "ordinary_optional_stage"),
                "transition": transition, "finding_ids": [], "validation_ids": [],
            }
            decision["decision_id"] = derive_decision_id(packet_id, decision)
            decisions.append(decision)
        if current_ref != selected_deck_ref:
            raise ValueError("Terminal deck does not equal optional-stage output")
        for index, decision in enumerate(decisions):
            if index:
                decision["previous_decision_id"] = decisions[index - 1]["decision_id"]
            if index + 1 < len(decisions):
                decision["next_decision_id"] = decisions[index + 1]["decision_id"]
        winners = [prior_by_pass[index] for index in range(1, 7)]
        if any(item["transition"]["acceptance_outcome"] != "accepted" for item in winners):
            raise ValueError("Initial pass winner evidence is incomplete")
        packet["lineage"] = {
            "decision_count": len(decisions), "first_decision_id": decisions[0]["decision_id"],
            "last_decision_id": decisions[-1]["decision_id"], "decisions": decisions,
        }
        winner_rows = [{
            "released_pass_identity": item["released_pass_identity"],
            "decision_id": item["decision_id"],
            "accepted_workspace_id": item["transition"]["accepted_workspace_id"],
            "accepted_workspace_sha256": item["transition"]["accepted_workspace_sha256"],
            "authored_claim_set_sha256": item["transition"]["authored_claim_set_sha256"],
        } for item in winners]
        packet["initial_assembly"] = {
            "assembly_id": derive_editorial_review_id(
                "erasm", "initial_assembly_id.v1",
                [packet_id, *[item["decision_id"] for item in winner_rows], initial_deck_ref["sha256"]],
            ),
            "accepted_pass_winners": winner_rows, "assembled_deck": dict(initial_deck_ref),
            "report_id": subject["assembly_report"],
            "report_sha256": sha256(report_path.read_bytes()).hexdigest(),
        }
        artifacts = []
        for digest, payload in deck_payloads.items():
            reference = deck_reference(payload)
            uses: list[dict[str, Any]] = []
            if reference == initial_deck_ref:
                uses.append({"role": "initial_assembled"})
            for decision in decisions:
                transition = decision["transition"]
                for field, role in (
                    ("input_deck", "decision_input"),
                    ("candidate_deck", "materialized_candidate"),
                    ("output_deck", "decision_output"),
                ):
                    if transition.get(field) == reference:
                        uses.append({
                            "role": role, "decision_id": decision["decision_id"],
                            "stage": decision["stage"], "stage_attempt": decision["stage_attempt"],
                        })
            if reference == selected_deck_ref:
                uses.append({"role": "terminal_selected"})
                if branch == "delivery":
                    uses.append({"role": "delivered"})
            artifacts.append(_artifact(packet_id, packet, "assembled_deck", payload, uses))
        for decision in decisions:
            action = decision["action"]
            artifacts.append(_artifact(packet_id, packet, "provider_response",
                response_payloads[action["provider_response_id"]], [{
                    "role": "provider_response", "decision_id": decision["decision_id"],
                    "stage": decision["stage"], "stage_attempt": decision["stage_attempt"],
                    "paid_action_id": action["paid_action_id"],
                    "binding_sha256": action["binding_sha256"],
                    "provider_response_id": action["provider_response_id"],
                }]))
        packet["findings"] = findings
        packet["validations"] = validations
        packet["artifact_manifest"] = {
            "decks": [{key: item[key] for key in ("artifact_id", "artifact_kind", "object_sha256", "artifact_sha256")} for item in artifacts if item["artifact_kind"] == "assembled_deck"],
            "provider_responses": [{
                **{key: item[key] for key in ("artifact_id", "artifact_kind", "object_sha256", "artifact_sha256")},
                "provider_response_id": item["relations"]["uses"][0]["provider_response_id"],
            } for item in artifacts if item["artifact_kind"] == "provider_response"],
        }
        packet["summary"] = {
            "decision_count": len(decisions), "finding_count": len(findings), "validation_count": len(validations),
            "creative_retry_count": sum(item["stage"] == "creative_retry" for item in decisions),
            "optional_stage_count": sum(item["stage"] in {"polish", "critic", "candidate"} for item in decisions),
        }
        packet["packet_sha256"] = digest_without(packet, "packet_sha256")
        projections = [
            *[_projection(packet, "decision", item, item["decision_ordinal"]) for item in decisions],
            *[_projection(packet, "finding", item, item["decision_ordinal"]) for item in findings],
            *[_projection(packet, "validation", item, item["decision_ordinal"]) for item in validations],
        ]
        validation = validate_editorial_review_packet(packet, projections, artifacts)
        if validation.outcome != "valid":
            return "unsupported", build_editorial_review_capture_status(
                "contradictory_native_evidence"
            )
        return branch, {"packet": packet, "projections": projections, "artifacts": artifacts}
    except (KeyError, TypeError, ValueError, OSError, json.JSONDecodeError):
        return "unsupported", build_editorial_review_capture_status(
            "incomplete_native_evidence"
        )


__all__ = [
    "DELIVERY_RESULT_VERSION", "RECEIPT_VERSION", "REVIEW_RESULT_VERSION",
    "read_eligible_editorial_result",
    "collect_editorial_review_runtime_evidence",
    "build_editorial_review_runtime_capture",
]
