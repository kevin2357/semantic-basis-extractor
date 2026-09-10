"""Deterministic provider-free editorial-review contract fixtures."""

from __future__ import annotations

from copy import deepcopy
from gzip import GzipFile
from hashlib import sha256
from io import BytesIO
from importlib.resources import files
from typing import Any, Mapping

from .editorial_review_contracts import (
    EditorialReviewValidationResult,
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
    read_editorial_review_semantic_contract,
    validate_closed_root,
)


FIXTURE_SCHEMA_VERSION = "editorial_review_contract_fixture_bundle.v1"
FIXTURE_KINDS = frozenset({"accepted_delivery", "editorial_closeout"})
FIXTURE_RESOURCES = {
    kind: f"editorial-review-{kind}.v5.json" for kind in FIXTURE_KINDS
}
_OBSERVED_AT = "2026-01-01T00:00:00Z"


def _hex(label: str) -> str:
    return sha256(label.encode("utf-8")).hexdigest()


def _gzip(value: Any) -> bytes:
    target = BytesIO()
    with GzipFile(
        filename="", mode="wb", fileobj=target, compresslevel=9, mtime=0,
    ) as stream:
        stream.write(canonical_editorial_review_json(value))
    return target.getvalue()


def _deck(label: str) -> dict[str, Any]:
    return {
        "schema_version": "astrowoof.synthetic_editorial_deck.v1",
        "deck_name": label,
        "cards": [
            {"card_id": f"{label}-card", "text": f"Synthetic {label} text."}
        ],
    }


def _action(label: str, kind: str, with_response: bool = True) -> dict[str, Any]:
    request_sha256 = _hex(label + ":request-bytes")
    value = {
        "paid_action_id": f"paid_{_hex(label + ':action')[:24]}",
        "action_kind": kind,
        "binding_sha256": _hex(label + ":binding-bytes"),
        "request_sha256": request_sha256,
        "prompt_provenance": {
            "prompt_template_id": f"synthetic.{kind}",
            "prompt_template_version": "1.0.0",
            "prompt_template_sha256": _hex(label + ":prompt-template"),
            "rendered_request_sha256": request_sha256,
        },
    }
    if with_response:
        value.update({
            "provider_response_id": f"resp_{_hex(label + ':response')[:24]}",
            "provider_response_sha256": _hex(label + ":response-bytes"),
        })
    return value


def _deck_ref(packet_id: str, deck: Mapping[str, Any]) -> dict[str, str]:
    digest = editorial_review_sha256(deck)
    return {
        "artifact_id": derive_artifact_id(packet_id, "assembled_deck", digest),
        "sha256": digest,
    }


def _base_packet(kind: str) -> dict[str, Any]:
    accepted = kind == "accepted_delivery"
    label = "accepted" if accepted else "closeout"
    terminal_id = f"terminal_{_hex(label + ':terminal')[:24]}"
    return {
        "schema_version": "editorial_review_packet.v5",
        "eligibility": {
            "route": "ordinary_live_exact",
            "terminal_outcome": "delivery_complete" if accepted else "editorial_review_required",
            "final_custody": "resolved",
            "native_result_schema_version": (
                "astrowoof.native_execution_result.v0.1"
                if accepted else "astrowoof.native_execution_result.v0.2"
            ),
            "native_result_id": f"result_{_hex(label + ':result')[:24]}",
            "native_result_sha256": _hex(label + ":result-bytes"),
            "canonical_receipt_schema_version": "astrowoof.native_publication_receipt.v0.1",
            "canonical_receipt_id": f"receipt_{_hex(label + ':receipt')[:24]}",
            "canonical_receipt_sha256": _hex(label + ":receipt-bytes"),
        },
        "native_correlations": {
            "native_run_id": f"native-{label}-fixture",
            "subject_id": f"subject-{label}-fixture",
            "native_state_revision": 8,
            "checkpoint_basis_sha256": _hex(label + ":checkpoint-basis"),
            "snapshot_sha256": _hex(label + ":snapshot"),
        },
        "producer": {
            "package": "astrowoof-natal-authoring",
            "version": "fixture",
            "profile_id": "synthetic-editorial-profile.v1",
            "profile_sha256": _hex(label + ":profile"),
            "resource_set_sha256": _hex(label + ":resources"),
        },
        "terminal_selection": {
            "terminal_selection_id": terminal_id,
            "selection_origin": "decision" if accepted else "assembly",
            "selected_deck": {},
            "delivery_disposition": "delivered" if accepted else "retained_for_editorial_review",
            "validation_ids": [],
        },
    }


def _build_packet(kind: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    accepted = kind == "accepted_delivery"
    packet = _base_packet(kind)
    packet["packet_id"] = derive_packet_id(packet)
    packet_id = packet["packet_id"]

    assembled = _deck(f"{kind}-assembled")
    adopted = _deck(f"{kind}-adopted")
    rejected = _deck(f"{kind}-rejected")
    decks = [assembled, adopted, rejected]
    refs = {editorial_review_sha256(deck): _deck_ref(packet_id, deck) for deck in decks}
    ref = lambda deck: deepcopy(refs[editorial_review_sha256(deck)])

    decisions: list[dict[str, Any]] = []
    for index in range(1, 7):
        accepted_initial = index != 1
        transition = {
            "relation_kind": "initial_pass_materialization",
            "attempt_identity": f"{kind}-pass-{index}-attempt-1",
            "released_pass_identity": f"ordinary-initial-pass-{index}.v1",
            "source_basis_sha256": _hex(f"{kind}:pass:{index}:source-basis"),
            "candidate_workspace_id": f"{kind}-pass-{index}-attempt-1-candidate",
            "candidate_workspace_sha256": _hex(f"{kind}:pass:{index}:attempt-1-candidate"),
            "authored_claim_set_sha256": _hex(f"{kind}:pass:{index}:attempt-1-authored-claims"),
            "qa_report_sha256": _hex(f"{kind}:pass:{index}:attempt-1-qa"),
            "acceptance_outcome": "accepted" if accepted_initial else "rejected",
            "materialization_outcome": "materialized",
        }
        if accepted_initial:
            transition.update({
                "accepted_workspace_id": f"{kind}-pass-{index}-accepted",
                "accepted_workspace_sha256": transition["candidate_workspace_sha256"],
            })
        decisions.append({
            "schema_version": "editorial_review_decision.v5",
            "decision_id": "pending",
            "decision_ordinal": index - 1,
            "stage": "initial_pass",
            "stage_attempt": 1,
            "initial_pass_index": index,
            "released_pass_identity": f"ordinary-initial-pass-{index}.v1",
            "subject_id": packet["native_correlations"]["subject_id"],
            "action": _action(f"{kind}:pass:{index}", "initial_pass"),
            "transition": transition,
            "finding_ids": [], "validation_ids": [],
        })

    predecessor = decisions[0]
    retry_transition = {
        "relation_kind": "pass_retry_materialization",
        "attempt_identity": f"{kind}-pass-1-attempt-2",
        "released_pass_identity": "ordinary-initial-pass-1.v1",
        "source_basis_sha256": predecessor["transition"]["candidate_workspace_sha256"],
        "candidate_workspace_id": f"{kind}-pass-1-attempt-2-candidate",
        "candidate_workspace_sha256": _hex(f"{kind}:pass:1:attempt-2-candidate"),
        "accepted_workspace_id": f"{kind}-pass-1-accepted",
        "accepted_workspace_sha256": _hex(f"{kind}:pass:1:attempt-2-candidate"),
        "authored_claim_set_sha256": _hex(f"{kind}:pass:1:attempt-2-authored-claims"),
        "qa_report_sha256": _hex(f"{kind}:pass:1:attempt-2-qa"),
        "acceptance_outcome": "accepted", "materialization_outcome": "materialized",
        "predecessor_decision_id": "pending",
        "predecessor_attempt_identity": predecessor["transition"]["attempt_identity"],
        "predecessor_acceptance_outcome": "rejected",
        "predecessor_qa_report_sha256": predecessor["transition"]["qa_report_sha256"],
    }
    decisions.append({
        "schema_version": "editorial_review_decision.v5", "decision_id": "pending",
        "decision_ordinal": 6, "stage": "creative_retry", "stage_attempt": 2,
        "initial_pass_index": 1, "released_pass_identity": "ordinary-initial-pass-1.v1",
        "subject_id": packet["native_correlations"]["subject_id"],
        "action": _action(f"{kind}:pass:1:retry:2", "ordinary_creative_retry"),
        "transition": retry_transition, "finding_ids": [], "validation_ids": [],
    })

    first_stage = "polish"
    first_action = _action(f"{kind}:{first_stage}:1", "ordinary_optional_stage")
    if accepted:
        first_transition = {
            "relation_kind": "whole_deck_transition",
            "input_deck": ref(assembled), "candidate_deck": ref(adopted),
            "output_deck": ref(adopted), "materialization_outcome": "materialized",
            "adoption_outcome": "candidate_adopted",
        }
        second_input = adopted
    else:
        first_transition = {
            "relation_kind": "whole_deck_transition",
            "input_deck": ref(assembled), "output_deck": ref(assembled),
            "materialization_outcome": "not_materialized",
            "adoption_outcome": "candidate_not_adopted",
        }
        second_input = assembled
    decisions.append({
        "schema_version": "editorial_review_decision.v5", "decision_id": "pending",
        "decision_ordinal": 7, "stage": first_stage, "stage_attempt": 1,
        "subject_id": packet["native_correlations"]["subject_id"],
        "action": first_action, "transition": first_transition,
        "finding_ids": [], "validation_ids": [],
    })
    decisions.append({
        "schema_version": "editorial_review_decision.v5", "decision_id": "pending",
        "decision_ordinal": 8, "stage": "polish",
        "stage_attempt": 1 if accepted else 2,
        "subject_id": packet["native_correlations"]["subject_id"],
        "action": _action(f"{kind}:later", "ordinary_optional_stage"),
        "transition": {
            "relation_kind": "whole_deck_transition",
            "input_deck": ref(second_input), "candidate_deck": ref(rejected),
            "output_deck": ref(second_input), "materialization_outcome": "materialized",
            "adoption_outcome": "candidate_not_adopted",
        },
        "finding_ids": [], "validation_ids": [],
    })
    for decision in decisions:
        decision["decision_id"] = derive_decision_id(packet_id, decision)
    decisions[6]["transition"]["predecessor_decision_id"] = decisions[0]["decision_id"]
    for index, decision in enumerate(decisions):
        if index:
            decision["previous_decision_id"] = decisions[index - 1]["decision_id"]
        if index + 1 < len(decisions):
            decision["next_decision_id"] = decisions[index + 1]["decision_id"]

    finding_specs = [
        (7, "lint", "synthetic_repetition", "advisory", "post_polish", "claim_ids"),
    ] if accepted else [
        (7, "materialization", "provider_output_invalid", "error", "post_polish", "not_claim_scoped"),
        (8, "deterministic_qa", "residual_repetition", "error", "post_polish", "count_only"),
        (8, "editorial", "claim_wording_unresolved", "warning", "terminal", "claim_ids"),
    ]
    findings: list[dict[str, Any]] = []
    per_decision_findings: dict[int, int] = {}
    for ordinal, fkind, code, severity, phase, mode in finding_specs:
        population: dict[str, Any] = {"mode": mode}
        if mode == "claim_ids":
            population.update({"evaluated_count": 2, "affected_count": 1, "affected_claim_ids": ["claim-synthetic-1"]})
        elif mode == "count_only":
            population.update({"evaluated_count": 2, "affected_count": 1})
        finding = {
            "schema_version": "editorial_review_finding.v1", "finding_id": "pending",
            "decision_id": decisions[ordinal]["decision_id"], "decision_ordinal": ordinal,
            "finding_kind": fkind, "code": code, "severity": severity, "phase": phase,
            "message": f"Synthetic finding: {code}.", "population": population,
            "field_context": [{
                "field_path": "$.cards[0].text",
                "before_state": "present", "before": "Synthetic before text.",
                "after_state": "candidate_not_materialized" if ordinal == 7 and not accepted else "present",
                **({} if ordinal == 7 and not accepted else {"after": "Synthetic after text."}),
            }],
            "evidence_sha256": _hex(f"{kind}:finding:{code}"),
        }
        local = per_decision_findings.get(ordinal, 0)
        finding["finding_id"] = derive_finding_id(finding["decision_id"], finding, local)
        per_decision_findings[ordinal] = local + 1
        decisions[ordinal]["finding_ids"].append(finding["finding_id"])
        findings.append(finding)

    validations: list[dict[str, Any]] = []
    validation_specs = [
        ("decision", 7, "candidate_adoption", "polish_candidate_evaluated", "passed" if accepted else "failed"),
        ("terminal_selection", None, "terminal_disposition", "terminal_outcome_valid", "passed"),
    ]
    owner_counts: dict[str, int] = {}
    for owner_kind, ordinal, vkind, code, outcome in validation_specs:
        owner_id = decisions[ordinal]["decision_id"] if ordinal is not None else packet["terminal_selection"]["terminal_selection_id"]
        validation = {
            "schema_version": "editorial_review_validation.v1", "validation_id": "pending",
            "owner_kind": owner_kind, "validation_kind": vkind, "code": code,
            "outcome": outcome, "path": "$.terminal_selection" if ordinal is None else f"$.lineage.decisions[{ordinal}]",
            "report_id": f"report-{kind}-{code}", "report_sha256": _hex(f"{kind}:report:{code}"),
            "finding_ids": [] if ordinal is None else list(decisions[ordinal]["finding_ids"]),
        }
        if ordinal is None:
            validation["terminal_selection_id"] = owner_id
        else:
            validation.update({"decision_id": owner_id, "decision_ordinal": ordinal})
        local = owner_counts.get(owner_id, 0)
        validation["validation_id"] = derive_validation_id(owner_id, validation, local)
        owner_counts[owner_id] = local + 1
        if ordinal is None:
            packet["terminal_selection"]["validation_ids"].append(validation["validation_id"])
        else:
            decisions[ordinal]["validation_ids"].append(validation["validation_id"])
        validations.append(validation)

    selected = adopted if accepted else assembled
    packet["terminal_selection"]["selected_deck"] = ref(selected)
    if accepted:
        packet["terminal_selection"]["selected_by_decision_id"] = decisions[7]["decision_id"]
        packet["terminal_selection"]["delivered_deck"] = ref(selected)

    artifacts: list[dict[str, Any]] = []
    for deck in decks:
        deck_ref = ref(deck)
        uses: list[dict[str, Any]] = []
        if deck is assembled:
            uses.append({"role": "initial_assembled"})
        for decision in decisions:
            transition = decision["transition"]
            role_fields = (
                ("input_deck", "decision_input"),
                ("candidate_deck", "materialized_candidate"),
                ("output_deck", "decision_output"),
            )
            for field, role in role_fields:
                if transition.get(field) == deck_ref:
                    uses.append({"role": role, "decision_id": decision["decision_id"], "stage": decision["stage"], "stage_attempt": decision["stage_attempt"]})
        if packet["terminal_selection"]["selected_deck"] == deck_ref:
            uses.append({"role": "terminal_selected"})
        if packet["terminal_selection"].get("delivered_deck") == deck_ref:
            uses.append({"role": "delivered"})
        if not uses:
            continue
        artifact = {
            "schema_version": "editorial_review_artifact.v2",
            "artifact_id": deck_ref["artifact_id"], "artifact_sha256": "pending",
            "artifact_kind": "assembled_deck", "object_sha256": deck_ref["sha256"],
            "media_type": "application/json",
            "native_correlations": {
                "native_run_id": packet["native_correlations"]["native_run_id"],
                "subject_id": packet["native_correlations"]["subject_id"],
                "packet_id": packet_id,
            },
            "relations": {"uses": uses}, "assembled_deck": deck,
        }
        artifact["artifact_sha256"] = digest_without(artifact, "artifact_sha256")
        artifacts.append(artifact)
    for decision in decisions:
        action = decision["action"]
        if not action.get("provider_response_id"):
            continue
        response = {
            "schema_version": "astrowoof.synthetic_provider_response.v1",
            "response_id": action["provider_response_id"],
            "output": {"status": "synthetic", "decision_ordinal": decision["decision_ordinal"]},
        }
        object_digest = editorial_review_sha256(response)
        action["provider_response_sha256"] = object_digest
        artifact = {
            "schema_version": "editorial_review_artifact.v2",
            "artifact_id": derive_artifact_id(packet_id, "provider_response", object_digest),
            "artifact_sha256": "pending", "artifact_kind": "provider_response",
            "object_sha256": object_digest, "media_type": "application/json",
            "native_correlations": {
                "native_run_id": packet["native_correlations"]["native_run_id"],
                "subject_id": packet["native_correlations"]["subject_id"],
                "packet_id": packet_id,
            },
            "relations": {"uses": [{
                "role": "provider_response", "decision_id": decision["decision_id"],
                "stage": decision["stage"], "stage_attempt": decision["stage_attempt"],
                "paid_action_id": action["paid_action_id"], "binding_sha256": action["binding_sha256"],
                "provider_response_id": action["provider_response_id"],
            }]},
            "provider_response": response,
        }
        artifact["artifact_sha256"] = digest_without(artifact, "artifact_sha256")
        artifacts.append(artifact)

    packet["lineage"] = {
        "decision_count": len(decisions), "first_decision_id": decisions[0]["decision_id"],
        "last_decision_id": decisions[-1]["decision_id"], "decisions": decisions,
    }
    winners = []
    for pass_index in range(1, 7):
        winner = next(
            item for item in decisions
            if item.get("initial_pass_index") == pass_index
            and item["transition"].get("acceptance_outcome") == "accepted"
        )
        transition = winner["transition"]
        winners.append({
            "released_pass_identity": winner["released_pass_identity"],
            "decision_id": winner["decision_id"],
            "accepted_workspace_id": transition["accepted_workspace_id"],
            "accepted_workspace_sha256": transition["accepted_workspace_sha256"],
            "authored_claim_set_sha256": transition["authored_claim_set_sha256"],
        })
    packet["initial_assembly"] = {
        "assembly_id": derive_editorial_review_id(
            "erasm", "initial_assembly_id.v1",
            [packet_id, *[item["decision_id"] for item in winners], ref(assembled)["sha256"]],
        ),
        "accepted_pass_winners": winners,
        "assembled_deck": ref(assembled),
        "report_id": f"assembly-report-{kind}",
        "report_sha256": _hex(f"{kind}:assembly-report"),
    }
    packet["findings"] = findings
    packet["validations"] = validations
    packet["artifact_manifest"] = {
        "decks": [
            {key: artifact[key] for key in ("artifact_id", "artifact_kind", "object_sha256", "artifact_sha256")}
            for artifact in artifacts if artifact["artifact_kind"] == "assembled_deck"
        ],
        "provider_responses": [
            {**{key: artifact[key] for key in ("artifact_id", "artifact_kind", "object_sha256", "artifact_sha256")},
             "provider_response_id": artifact["relations"]["uses"][0]["provider_response_id"]}
            for artifact in artifacts if artifact["artifact_kind"] == "provider_response"
        ],
    }
    packet["summary"] = {
        "decision_count": len(decisions), "finding_count": len(findings),
        "validation_count": len(validations),
        "creative_retry_count": sum(d["stage"] == "creative_retry" for d in decisions),
        "optional_stage_count": sum(d["stage"] in {"polish", "critic", "candidate"} for d in decisions),
    }
    packet["packet_sha256"] = digest_without(packet, "packet_sha256")
    return packet, artifacts


def _projection(packet: Mapping[str, Any], kind: str, member: Mapping[str, Any], owner_ordinal: int) -> dict[str, Any]:
    id_field = f"{kind}_id"
    native_id = member[id_field]
    return {
        "schema_version": "editorial_review_projection.v5",
        "projection_id": derive_projection_id(packet["packet_id"], kind, native_id),
        "projection_kind": kind, "packet_id": packet["packet_id"],
        "packet_sha256": packet["packet_sha256"], "owner_ordinal": owner_ordinal,
        "projected_native_id": native_id,
        "projected_native_sha256": editorial_review_sha256(member),
        kind: deepcopy(member),
    }


def _envelope(packet: Mapping[str, Any], event_kind: str, native: Mapping[str, Any], source: str = "editorial") -> dict[str, Any]:
    native_digest = packet["packet_sha256"] if event_kind == "packet" else (
        native["artifact_sha256"] if event_kind == "artifact" else editorial_review_sha256(native)
    )
    return {
        "transport_schema_version": "editorial_review_transport.v5",
        "source_kind": source, "event_kind": event_kind,
        "native_content": deepcopy(native), "native_content_sha256": native_digest,
        "correlations": {
            "native": {
                "native_run_id": packet["native_correlations"]["native_run_id"],
                "subject_id": packet["native_correlations"]["subject_id"],
                "packet_id": packet["packet_id"],
            },
            "api_observation": {
                "api_run_id": "synthetic-api-run", "api_job_id": "synthetic-api-job",
                "terminal_transition_id": "synthetic-terminal-transition",
            },
        },
        "observed_at": _OBSERVED_AT,
    }


def build_editorial_review_fixture_bundle(kind: str) -> dict[str, Any]:
    if kind not in FIXTURE_KINDS:
        raise ValueError("Unknown editorial review fixture kind")
    packet, artifacts = _build_packet(kind)
    projections = [
        *[_projection(packet, "decision", item, item["decision_ordinal"]) for item in packet["lineage"]["decisions"]],
        *[_projection(packet, "finding", item, item["decision_ordinal"]) for item in sorted(packet["findings"], key=lambda item: (item["decision_ordinal"], item["finding_id"]))],
        *[_projection(packet, "validation", item, item.get("decision_ordinal", len(packet["lineage"]["decisions"]))) for item in sorted(packet["validations"], key=lambda item: (item.get("decision_ordinal", len(packet["lineage"]["decisions"])), item["validation_id"]))],
    ]
    editorial_events = [_envelope(packet, "packet", packet)] + [
        _envelope(packet, "projection", item) for item in projections
    ]
    artifact_events = [
        _envelope(packet, "artifact", item, "artifact")
        for item in sorted(artifacts, key=lambda item: (item["artifact_kind"], item["artifact_id"]))
    ]
    contract_bytes = canonical_editorial_review_json(read_editorial_review_semantic_contract())
    request_bytes = canonical_editorial_review_json(editorial_events)
    gzip_bytes = _gzip(editorial_events)
    bundle = {
        "schema_version": FIXTURE_SCHEMA_VERSION,
        "fixture_id": f"editorial-review-{kind}-v1",
        "fixture_kind": kind,
        "semantic_contract_sha256": sha256(contract_bytes).hexdigest(),
        "editorial_request": {"events": editorial_events},
        "artifact_batches": [{"batch_ordinal": 0, "events": artifact_events}],
        "expected": {
            "packet_id": packet["packet_id"], "packet_sha256": packet["packet_sha256"],
            "event_count": len(editorial_events),
            "canonical_request_sha256": sha256(request_bytes).hexdigest(),
            "canonical_gzip_sha256": sha256(gzip_bytes).hexdigest(),
            "canonical_gzip_bytes": len(gzip_bytes),
            "artifact_ids": [event["native_content"]["artifact_id"] for event in artifact_events],
            "validation_result": {"outcome": "valid"},
        },
        "bundle_sha256": "pending",
    }
    bundle["bundle_sha256"] = digest_without(bundle, "bundle_sha256")
    return bundle


def build_editorial_review_runtime_capture_status(
    reason: str,
    *,
    native_run_id: str,
    subject_id: str,
    native_result_id: str,
) -> dict[str, Any]:
    """Build a closed status from explicit, caller-validated native identity."""
    detail_codes = {
        "ineligible_route": "route_not_supported",
        "unsupported_result_version": "result_version_not_supported",
        "incomplete_native_evidence": "required_native_join_missing",
        "contradictory_native_evidence": "native_join_conflict",
        "editorial_request_record_limit_exceeded": "editorial_event_limit_exceeded",
        "editorial_request_byte_limit_exceeded": "compressed_request_limit_exceeded",
    }
    try:
        detail_code = detail_codes[reason]
    except KeyError as exc:
        raise ValueError("Unknown editorial review capture-status reason") from exc
    native = {
        "native_run_id": native_run_id,
        "subject_id": subject_id,
        "native_result_id": native_result_id,
    }
    if not all(isinstance(value, str) and value for value in native.values()):
        raise ValueError("Capture-status native correlations must be non-empty strings")
    return {
        "schema_version": "editorial_review_capture_status.v1",
        "capture_id": derive_editorial_review_id(
            "erc", "capture_id.v1",
            [native_run_id, native_result_id, reason, detail_code],
        ),
        "outcome": "not_captured",
        "reason": reason,
        "native_correlations": native,
        "detail_code": detail_code,
    }


def build_editorial_review_capture_status(reason: str) -> dict[str, Any]:
    """Build the backwards-compatible synthetic contract-fixture status."""
    return build_editorial_review_runtime_capture_status(
        reason,
        native_run_id="native-capture-status-fixture",
        subject_id="subject-capture-status-fixture",
        native_result_id="result-capture-status-fixture",
    )


def validate_editorial_review_capture_status_against_native(
    status: Mapping[str, Any],
    *,
    selected_result_id: str,
    result: Mapping[str, Any],
    receipt: Mapping[str, Any],
    subject_id: str,
) -> EditorialReviewValidationResult:
    """Validate one status against its exact selected native publication."""
    closed = validate_closed_root(status, "capture_status")
    if closed.outcome != "valid":
        return closed
    native = status["native_correlations"]
    if not (
        selected_result_id == result.get("result_id") == receipt.get("result_id")
        and native.get("native_result_id") == selected_result_id
        and native.get("native_run_id") == result.get("run_id") == receipt.get("run_id")
        and native.get("subject_id") == subject_id
    ):
        return EditorialReviewValidationResult(
            "invalid", "contradictory_evidence",
            "packet.provenance.exact_join.v1", "native_correlations",
            "capture_status_native_join_mismatch",
        )
    expected = build_editorial_review_runtime_capture_status(
        status["reason"],
        native_run_id=native["native_run_id"],
        subject_id=native["subject_id"],
        native_result_id=native["native_result_id"],
    )
    if status != expected:
        return EditorialReviewValidationResult(
            "invalid", "digest_mismatch", "artifact.id.derivation.v1",
            "capture_id", "capture_status_identity_mismatch",
        )
    return EditorialReviewValidationResult("valid")


def read_editorial_review_fixture_bundle(source: bytes | str) -> dict[str, Any]:
    from .editorial_review_contracts import parse_editorial_review_json_strict
    value = parse_editorial_review_json_strict(source)
    if not isinstance(value, dict):
        raise ValueError("Editorial review fixture bundle must be an object")
    result = validate_editorial_review_fixture_bundle(value)
    if result.outcome != "valid":
        raise ValueError(
            f"Editorial review fixture bundle is invalid: {result.classification}/{result.safe_detail_code}"
        )
    return deepcopy(value)


def read_packaged_editorial_review_fixture(kind: str) -> dict[str, Any]:
    try:
        name = FIXTURE_RESOURCES[kind]
    except KeyError as exc:
        raise ValueError("Unknown editorial review fixture kind") from exc
    raw = files("astrowoof_natal_authoring.resources").joinpath(
        "fixtures", "editorial_review", name,
    ).read_bytes()
    return read_editorial_review_fixture_bundle(raw)


def validate_editorial_review_request(events: list[Mapping[str, Any]]) -> EditorialReviewValidationResult:
    """Validate the atomic editorial event set independently of artifacts."""
    try:
        packet = events[0]["native_content"]
        projections = [event["native_content"] for event in events[1:]]
        return validate_editorial_review_packet(packet, projections, None)
    except (KeyError, TypeError, IndexError):
        return _bad("invalid_schema", "schema.root.closed.v1", "$.events", "request_shape_invalid")


def validate_editorial_review_fixture_bundle(bundle: Mapping[str, Any]) -> EditorialReviewValidationResult:
    try:
        if bundle.get("schema_version") != FIXTURE_SCHEMA_VERSION:
            return _bad("unsupported_version", "schema.version.closed.v1", "$.schema_version", "unsupported_version")
        if set(bundle) != {"schema_version", "fixture_id", "fixture_kind", "semantic_contract_sha256", "editorial_request", "artifact_batches", "expected", "bundle_sha256"}:
            return _bad("invalid_schema", "schema.root.closed.v1", "$", "bundle_shape_invalid")
        if bundle["fixture_kind"] not in FIXTURE_KINDS:
            return _bad("invalid_schema", "schema.version.closed.v1", "$.fixture_kind", "fixture_kind_invalid")
        if bundle["bundle_sha256"] != digest_without(bundle, "bundle_sha256"):
            return _bad("digest_mismatch", "digest.packet.self_domain.v1", "$.bundle_sha256", "bundle_digest_mismatch")
        contract_digest = editorial_review_sha256(read_editorial_review_semantic_contract())
        if bundle["semantic_contract_sha256"] != contract_digest:
            return _bad("digest_mismatch", "packet.provenance.exact_join.v1", "$.semantic_contract_sha256", "semantic_contract_digest_mismatch")
        events = bundle["editorial_request"]["events"]
        if len(events) > read_editorial_review_semantic_contract()["cardinalities"]["editorial_event_maximum"]:
            return _bad("record_limit_exceeded", "request.editorial.atomic_set.v1", "$.editorial_request.events", "event_limit_exceeded")
        if not events or events[0].get("source_kind") != "editorial" or events[0].get("event_kind") != "packet":
            return _bad("contradictory_evidence", "request.editorial.atomic_set.v1", "$.editorial_request.events", "packet_event_not_first")
        for index, event in enumerate(events):
            expected_kind = "packet" if index == 0 else "projection"
            if event.get("source_kind") != "editorial" or event.get("event_kind") != expected_kind:
                return _bad("contradictory_evidence", "transport.source_event.closed.v1", f"$.editorial_request.events[{index}]", "illegal_source_event_pair")
            native = event.get("native_content")
            native_digest = native.get("packet_sha256") if expected_kind == "packet" else editorial_review_sha256(native)
            if event.get("native_content_sha256") != native_digest:
                return _bad("digest_mismatch", "digest.projection.member_domain.v1", f"$.editorial_request.events[{index}].native_content_sha256", "envelope_native_digest_mismatch")
        packet = events[0]["native_content"]
        projections = [event["native_content"] for event in events[1:]]
        artifacts = [event["native_content"] for batch in bundle["artifact_batches"] for event in batch["events"]]
        result = validate_editorial_review_packet(packet, projections, artifacts)
        if result.outcome != "valid":
            return result
        kind_rank = {"decision": 0, "finding": 1, "validation": 2}
        projection_order = [
            (kind_rank[item["projection_kind"]], item["owner_ordinal"], item["projected_native_id"])
            for item in projections
        ]
        if projection_order != sorted(projection_order):
            return _bad("contradictory_evidence", "request.editorial.atomic_set.v1", "$.editorial_request.events", "projection_order_invalid")
        expected = bundle["expected"]
        compressed = _gzip(events)
        actual = {
            "packet_id": packet["packet_id"], "packet_sha256": packet["packet_sha256"],
            "event_count": len(events),
            "canonical_request_sha256": editorial_review_sha256(events),
            "canonical_gzip_sha256": sha256(compressed).hexdigest(),
            "canonical_gzip_bytes": len(compressed),
            "artifact_ids": [item["artifact_id"] for item in artifacts],
            "validation_result": {"outcome": "valid"},
        }
        if actual != expected:
            return _bad("contradictory_evidence", "summary.recomputed.v1", "$.expected", "fixture_expectation_mismatch")
        return EditorialReviewValidationResult("valid")
    except (KeyError, TypeError, ValueError, IndexError):
        return _bad("invalid_schema", "schema.root.closed.v1", "$", "fixture_shape_invalid")


def validate_editorial_review_packet(packet: Mapping[str, Any], projections: list[Mapping[str, Any]], artifacts: list[Mapping[str, Any]] | None) -> EditorialReviewValidationResult:
    try:
        root = validate_closed_root(packet, "packet")
        if root.outcome != "valid":
            return root
        if packet["packet_id"] != derive_packet_id(packet):
            return _bad("contradictory_evidence", "packet.provenance.exact_join.v1", "$.packet_id", "packet_id_mismatch")
        if packet["packet_sha256"] != digest_without(packet, "packet_sha256"):
            return _bad("digest_mismatch", "digest.packet.self_domain.v1", "$.packet_sha256", "packet_digest_mismatch")
        decisions = packet["lineage"]["decisions"]
        eligibility = packet["eligibility"]
        terminal = packet["terminal_selection"]
        expected_disposition = "delivered" if eligibility["terminal_outcome"] == "delivery_complete" else "retained_for_editorial_review"
        if eligibility["route"] != "ordinary_live_exact" or eligibility["final_custody"] != "resolved" or terminal["delivery_disposition"] != expected_disposition:
            return _bad("ineligible_route", "packet.provenance.exact_join.v1", "$.eligibility", "terminal_eligibility_mismatch")
        if len(decisions) < 6 or [item["decision_ordinal"] for item in decisions] != list(range(len(decisions))):
            return _bad("contradictory_evidence", "lineage.ordinal.total_contiguous.v1", "$.lineage.decisions", "decision_ordinals_invalid")
        actions = [item["action"] for item in decisions if item["action"]]
        for field in ("paid_action_id", "binding_sha256", "provider_response_id"):
            values = [action[field] for action in actions if field in action]
            if len(values) != len(set(values)):
                return _bad("contradictory_evidence", "provider.response.unique_decision.v1", "$.lineage.decisions", f"duplicate_{field}")
        initial_decisions = [item for item in decisions if item["stage"] == "initial_pass"]
        pass_decisions = [item for item in decisions if item["stage"] in {"initial_pass", "creative_retry"}]
        post_decisions = [item for item in decisions if item["stage"] in {"polish", "critic", "candidate"}]
        if (
            len(initial_decisions) != 6
            or sorted(item["initial_pass_index"] for item in initial_decisions) != list(range(1, 7))
            or any(item["stage_attempt"] != 1 for item in initial_decisions)
            or decisions != [*pass_decisions, *post_decisions]
        ):
            return _bad("contradictory_evidence", "lineage.initial_pass.exact_six.v1", "$.lineage.decisions", "initial_pass_topology_invalid")
        for index, decision in enumerate(decisions):
            if decision["subject_id"] != packet["native_correlations"]["subject_id"]:
                return _bad("contradictory_evidence", "packet.provenance.exact_join.v1", f"$.lineage.decisions[{index}].subject_id", "decision_subject_mismatch")
            if decision["decision_id"] != derive_decision_id(packet["packet_id"], decision):
                return _bad("contradictory_evidence", "lineage.ordinal.total_contiguous.v1", f"$.lineage.decisions[{index}].decision_id", "decision_id_mismatch")
            expected_previous = decisions[index - 1]["decision_id"] if index else None
            expected_next = decisions[index + 1]["decision_id"] if index + 1 < len(decisions) else None
            if decision.get("previous_decision_id") != expected_previous or decision.get("next_decision_id") != expected_next:
                return _bad("contradictory_evidence", "lineage.ordinal.total_contiguous.v1", f"$.lineage.decisions[{index}]", "decision_adjacency_invalid")
            transition = decision["transition"]
            action = decision["action"]
            expected_action_kind = "initial_pass" if decision["stage"] == "initial_pass" else ("ordinary_creative_retry" if decision["stage"] == "creative_retry" else "ordinary_optional_stage")
            if action and action.get("action_kind") != expected_action_kind:
                return _bad("contradictory_evidence", "provider.response.unique_decision.v1", f"$.lineage.decisions[{index}].action", "action_stage_mismatch")
            if action and (("provider_response_id" in action) != ("provider_response_sha256" in action)):
                return _bad("incomplete_evidence", "provider.response.unique_decision.v1", f"$.lineage.decisions[{index}].action", "response_identity_incomplete")
            prompt = action.get("prompt_provenance") if action else None
            if prompt is not None:
                if set(prompt) != {
                    "prompt_template_id", "prompt_template_version",
                    "prompt_template_sha256", "rendered_request_sha256",
                }:
                    return _bad("invalid_schema", "schema.root.closed.v1", f"$.lineage.decisions[{index}].action.prompt_provenance", "schema_validation_failed")
                if prompt["rendered_request_sha256"] != action["request_sha256"]:
                    return _bad("contradictory_evidence", "action.prompt_provenance.exact.v1", f"$.lineage.decisions[{index}].action.prompt_provenance", "rendered_request_digest_mismatch")
            if decision["stage"] in {"initial_pass", "creative_retry"}:
                expected_kind = (
                    "initial_pass_materialization"
                    if decision["stage"] == "initial_pass"
                    else "pass_retry_materialization"
                )
                if (
                    transition["relation_kind"] != expected_kind
                    or transition["released_pass_identity"] != decision["released_pass_identity"]
                    or transition["materialization_outcome"] != "materialized"
                    or ((transition["acceptance_outcome"] == "accepted") != ("accepted_workspace_id" in transition and "accepted_workspace_sha256" in transition))
                    or (transition.get("accepted_workspace_sha256") not in {None, transition["candidate_workspace_sha256"]})
                ):
                    return _bad("contradictory_evidence", "lineage.initial_pass.materialization.v1", f"$.lineage.decisions[{index}].transition", "initial_pass_materialization_invalid")
                if decision["stage"] == "creative_retry":
                    same_pass_prior = [
                        prior for prior in decisions[:index]
                        if prior.get("released_pass_identity") == decision["released_pass_identity"]
                    ]
                    predecessor = same_pass_prior[-1] if same_pass_prior else None
                    if (
                        predecessor is None
                        or transition["predecessor_decision_id"] != predecessor["decision_id"]
                        or transition["predecessor_attempt_identity"] != predecessor["transition"]["attempt_identity"]
                        or transition["predecessor_acceptance_outcome"] != predecessor["transition"]["acceptance_outcome"]
                        or transition["predecessor_qa_report_sha256"] != predecessor["transition"]["qa_report_sha256"]
                        or predecessor["transition"]["acceptance_outcome"] != "rejected"
                        or decision["stage_attempt"] != predecessor["stage_attempt"] + 1
                    ):
                        return _bad("contradictory_evidence", "lineage.pass_retry.predecessor_exact.v1", f"$.lineage.decisions[{index}].transition", "retry_predecessor_mismatch")
                continue
            if transition.get("relation_kind") != "whole_deck_transition":
                return _bad("contradictory_evidence", "deck.transition.discriminated.v1", f"$.lineage.decisions[{index}].transition", "whole_deck_transition_required")
            materialized = transition["materialization_outcome"] == "materialized"
            if materialized != ("candidate_deck" in transition):
                return _bad("contradictory_evidence", "deck.transition.candidate_iff_materialized.v1", f"$.lineage.decisions[{index}].transition", "candidate_materialization_mismatch")
            expected_output = transition.get("candidate_deck") if transition["adoption_outcome"] == "candidate_adopted" else transition["input_deck"]
            if transition["output_deck"] != expected_output:
                return _bad("contradictory_evidence", "deck.transition.output_matches_adoption.v1", f"$.lineage.decisions[{index}].transition.output_deck", "decision_output_mismatch")
            if decision is post_decisions[0] and transition["input_deck"] != packet["initial_assembly"]["assembled_deck"]:
                return _bad("contradictory_evidence", "assembly.pass_winner.exact_six.v1", f"$.lineage.decisions[{index}].transition.input_deck", "initial_assembly_input_mismatch")
            if decision is not post_decisions[0] and transition["input_deck"] != decisions[index - 1]["transition"]["output_deck"]:
                return _bad("contradictory_evidence", "deck.transition.next_input_contiguous.v1", f"$.lineage.decisions[{index}].transition.input_deck", "next_input_mismatch")
        assembly = packet["initial_assembly"]
        initial_materialization_keys = [
            (
                item["transition"]["candidate_workspace_id"],
                item["transition"]["candidate_workspace_sha256"],
                item["transition"]["authored_claim_set_sha256"],
            )
            for item in pass_decisions
        ]
        if len(set(initial_materialization_keys)) != len(pass_decisions):
            return _bad("contradictory_evidence", "lineage.initial_pass.materialization.v1", "$.lineage.decisions", "duplicate_initial_pass_materialization")
        accepted = [item for item in pass_decisions if item["transition"]["acceptance_outcome"] == "accepted"]
        if (
            len(accepted) != 6
            or sorted(item["initial_pass_index"] for item in accepted) != list(range(1, 7))
            or len({item["released_pass_identity"] for item in accepted}) != 6
        ):
            return _bad("contradictory_evidence", "assembly.pass_winner.exact_six.v1", "$.lineage.decisions", "accepted_pass_winners_invalid")
        expected_winners = [{
            "released_pass_identity": item["released_pass_identity"],
            "decision_id": item["decision_id"],
            "accepted_workspace_id": item["transition"]["accepted_workspace_id"],
            "accepted_workspace_sha256": item["transition"]["accepted_workspace_sha256"],
            "authored_claim_set_sha256": item["transition"]["authored_claim_set_sha256"],
        } for item in sorted(accepted, key=lambda item: item["initial_pass_index"])]
        if assembly["accepted_pass_winners"] != expected_winners:
            return _bad("contradictory_evidence", "assembly.pass_winner.exact_six.v1", "$.initial_assembly.accepted_pass_winners", "initial_assembly_membership_mismatch")
        winner_ids = [item["decision_id"] for item in expected_winners]
        expected_assembly_id = derive_editorial_review_id(
            "erasm", "initial_assembly_id.v1",
            [packet["packet_id"], *winner_ids, assembly["assembled_deck"]["sha256"]],
        )
        if assembly["assembly_id"] != expected_assembly_id:
            return _bad("contradictory_evidence", "assembly.pass_winner.exact_six.v1", "$.initial_assembly.assembly_id", "initial_assembly_id_mismatch")
        decision_index = {item["decision_id"]: item for item in decisions}
        findings = packet["findings"]
        finding_index = {item["finding_id"]: item for item in findings}
        if len(finding_index) != len(findings):
            return _bad("contradictory_evidence", "ownership.finding.same_packet.v1", "$.findings", "duplicate_finding_id")
        for decision in decisions:
            if set(decision["finding_ids"]) != {item["finding_id"] for item in findings if item["decision_id"] == decision["decision_id"]}:
                return _bad("contradictory_evidence", "ownership.finding.same_packet.v1", "$.findings", "finding_owner_mismatch")
        for finding in findings:
            population = finding["population"]
            mode = population["mode"]
            has_ids = "affected_claim_ids" in population
            has_counts = "affected_count" in population or "evaluated_count" in population
            if (mode == "claim_ids" and not has_ids) or (mode == "count_only" and (has_ids or not has_counts)) or (mode == "not_claim_scoped" and (has_ids or has_counts)):
                return _bad("contradictory_evidence", "ownership.finding.same_packet.v1", "$.findings", "finding_population_mismatch")
        validations = packet["validations"]
        for validation in validations:
            if validation["owner_kind"] == "decision":
                owner = decision_index.get(validation["decision_id"])
                if owner is None or owner["decision_ordinal"] != validation["decision_ordinal"] or validation["validation_id"] not in owner["validation_ids"]:
                    return _bad("contradictory_evidence", "ownership.validation.discriminated.v1", "$.validations", "decision_validation_owner_mismatch")
            elif validation["terminal_selection_id"] != packet["terminal_selection"]["terminal_selection_id"] or validation["validation_id"] not in packet["terminal_selection"]["validation_ids"]:
                return _bad("contradictory_evidence", "ownership.validation.discriminated.v1", "$.validations", "terminal_validation_owner_mismatch")
        terminal = packet["terminal_selection"]
        if terminal["selection_origin"] == "decision":
            owner = decision_index.get(terminal.get("selected_by_decision_id"))
            if owner is None or owner["transition"]["output_deck"] != terminal["selected_deck"]:
                return _bad("contradictory_evidence", "deck.selection.reachable.v1", "$.terminal_selection", "selected_deck_unreachable")
        elif terminal["selected_deck"] != (
            post_decisions[-1]["transition"]["output_deck"]
            if post_decisions else assembly["assembled_deck"]
        ):
            return _bad("contradictory_evidence", "deck.selection.reachable.v1", "$.terminal_selection", "assembly_selected_deck_unreachable")
        if terminal["delivery_disposition"] == "delivered" and terminal.get("delivered_deck") != terminal["selected_deck"]:
            return _bad("contradictory_evidence", "deck.delivery.equals_selected.v1", "$.terminal_selection.delivered_deck", "delivered_deck_mismatch")
        if artifacts is not None:
            artifact_index = {item["artifact_id"]: item for item in artifacts}
            manifest_items = [*packet["artifact_manifest"]["decks"], *packet["artifact_manifest"]["provider_responses"]]
            if set(artifact_index) != {item["artifact_id"] for item in manifest_items}:
                return _bad("incomplete_evidence", "artifact.identity.packet_scoped.v1", "$.artifact_manifest", "artifact_set_mismatch")
            for artifact in artifacts:
                payload = artifact[artifact["artifact_kind"]]
                def contains_forbidden(value: Any) -> bool:
                    if isinstance(value, dict):
                        return any(str(key).lower() in {"prompt", "provider_request_body", "endpoint_token", "credential"} or contains_forbidden(item) for key, item in value.items())
                    if isinstance(value, list):
                        return any(contains_forbidden(item) for item in value)
                    return False
                if contains_forbidden(payload):
                    return _bad("contradictory_evidence", "artifact.identity.packet_scoped.v1", "$.artifact_batches", "forbidden_artifact_content")
                if artifact["object_sha256"] != editorial_review_sha256(payload) or artifact["artifact_sha256"] != digest_without(artifact, "artifact_sha256"):
                    return _bad("digest_mismatch", "digest.artifact.wrapper_payload_domains.v1", "$.artifact_batches", "artifact_digest_mismatch")
                if artifact["artifact_id"] != derive_artifact_id(packet["packet_id"], artifact["artifact_kind"], artifact["object_sha256"]):
                    return _bad("contradictory_evidence", "artifact.id.derivation.v1", "$.artifact_batches", "artifact_id_mismatch")
            response_artifacts = {
                item["relations"]["uses"][0]["provider_response_id"]: item
                for item in artifacts if item["artifact_kind"] == "provider_response"
            }
            for decision in decisions:
                action = decision["action"]
                if "provider_response_id" not in action:
                    continue
                artifact = response_artifacts.get(action["provider_response_id"])
                if artifact is None or artifact["object_sha256"] != action["provider_response_sha256"]:
                    return _bad("contradictory_evidence", "provider.response.unique_decision.v1", "$.artifact_manifest.provider_responses", "response_action_digest_mismatch")
                use = artifact["relations"]["uses"][0]
                if any(use[key] != expected for key, expected in {
                    "decision_id": decision["decision_id"], "paid_action_id": action["paid_action_id"],
                    "binding_sha256": action["binding_sha256"], "stage": decision["stage"],
                    "stage_attempt": decision["stage_attempt"],
                }.items()):
                    return _bad("contradictory_evidence", "provider.response.unique_decision.v1", "$.artifact_manifest.provider_responses", "response_action_join_mismatch")
        members = {
            **{item["decision_id"]: ("decision", item, item["decision_ordinal"]) for item in decisions},
            **{item["finding_id"]: ("finding", item, item["decision_ordinal"]) for item in findings},
            **{item["validation_id"]: ("validation", item, item.get("decision_ordinal", len(decisions))) for item in validations},
        }
        if len(projections) != len(members) or {item["projected_native_id"] for item in projections} != set(members):
            return _bad("incomplete_evidence", "projection.member.same_packet.v1", "$.editorial_request.events", "projection_set_mismatch")
        for projection in projections:
            kind, member, owner_ordinal = members[projection["projected_native_id"]]
            if projection["projection_id"] != derive_projection_id(packet["packet_id"], kind, projection["projected_native_id"]) or projection[kind] != member or projection["projected_native_sha256"] != editorial_review_sha256(member) or projection["packet_sha256"] != packet["packet_sha256"] or projection["owner_ordinal"] != owner_ordinal:
                return _bad("contradictory_evidence", "projection.member.same_packet.v1", "$.editorial_request.events", "projection_member_mismatch")
        summary = packet["summary"]
        recomputed = {
            "decision_count": len(decisions), "finding_count": len(findings),
            "validation_count": len(validations),
            "creative_retry_count": sum(d["stage"] == "creative_retry" for d in decisions),
            "optional_stage_count": sum(d["stage"] in {"polish", "critic", "candidate"} for d in decisions),
        }
        if summary != recomputed or packet["lineage"]["decision_count"] != len(decisions) or packet["lineage"]["first_decision_id"] != decisions[0]["decision_id"] or packet["lineage"]["last_decision_id"] != decisions[-1]["decision_id"]:
            return _bad("contradictory_evidence", "summary.recomputed.v1", "$.summary", "summary_mismatch")
        return EditorialReviewValidationResult("valid")
    except (KeyError, TypeError, ValueError, IndexError):
        return _bad("invalid_schema", "schema.root.closed.v1", "$", "packet_shape_invalid")


def _bad(classification: str, rule_id: str, location: str, detail: str) -> EditorialReviewValidationResult:
    return EditorialReviewValidationResult("invalid", classification, rule_id, location, detail)


__all__ = [
    "FIXTURE_KINDS", "FIXTURE_RESOURCES", "FIXTURE_SCHEMA_VERSION",
    "build_editorial_review_fixture_bundle",
    "build_editorial_review_capture_status",
    "build_editorial_review_runtime_capture_status",
    "read_editorial_review_fixture_bundle",
    "read_packaged_editorial_review_fixture",
    "validate_editorial_review_request",
    "validate_editorial_review_fixture_bundle",
    "validate_editorial_review_capture_status_against_native",
    "validate_editorial_review_packet",
]
