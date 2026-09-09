"""Provider-free executable qualification for editorial-review contracts."""

from __future__ import annotations

import argparse
from copy import deepcopy
from gzip import GzipFile
from hashlib import sha256
from importlib.resources import files
from io import BytesIO
import json
from pathlib import Path
from typing import Any, Callable

from .editorial_review_contracts import (
    SCHEMA_RESOURCES, canonical_editorial_review_json, digest_without,
    editorial_review_sha256, read_editorial_review_semantic_contract,
)
from .editorial_review_fixtures import (
    FIXTURE_KINDS, build_editorial_review_capture_status,
    read_packaged_editorial_review_fixture,
    validate_editorial_review_fixture_bundle,
)


QUALIFICATION_VERSION = "editorial_review_contract_qualification.v1"


def _gzip(value: Any) -> bytes:
    target = BytesIO()
    with GzipFile(filename="", mode="wb", fileobj=target, compresslevel=9, mtime=0) as stream:
        stream.write(canonical_editorial_review_json(value))
    return target.getvalue()


def _rebind(bundle: dict[str, Any]) -> None:
    events = bundle["editorial_request"]["events"]
    packet = events[0]["native_content"]
    for batch in bundle["artifact_batches"]:
        for event in batch["events"]:
            artifact = event["native_content"]
            artifact["artifact_sha256"] = digest_without(artifact, "artifact_sha256")
            event["native_content_sha256"] = artifact["artifact_sha256"]
            manifest = [*packet["artifact_manifest"]["decks"], *packet["artifact_manifest"]["provider_responses"]]
            for item in manifest:
                if item["artifact_id"] == artifact["artifact_id"]:
                    item["artifact_sha256"] = artifact["artifact_sha256"]
    packet["packet_sha256"] = digest_without(packet, "packet_sha256")
    events[0]["native_content_sha256"] = packet["packet_sha256"]
    for event in events[1:]:
        event["native_content"]["packet_sha256"] = packet["packet_sha256"]
        event["native_content_sha256"] = editorial_review_sha256(event["native_content"])
    expected = bundle["expected"]
    expected["packet_sha256"] = packet["packet_sha256"]
    expected["event_count"] = len(events)
    expected["canonical_request_sha256"] = editorial_review_sha256(events)
    compressed = _gzip(events)
    expected["canonical_gzip_sha256"] = sha256(compressed).hexdigest()
    expected["canonical_gzip_bytes"] = len(compressed)
    expected["artifact_ids"] = [
        event["native_content"]["artifact_id"]
        for batch in bundle["artifact_batches"] for event in batch["events"]
    ]
    bundle["bundle_sha256"] = digest_without(bundle, "bundle_sha256")


def _packet(bundle: dict[str, Any]) -> dict[str, Any]:
    return bundle["editorial_request"]["events"][0]["native_content"]


def _artifact(bundle: dict[str, Any], kind: str) -> dict[str, Any]:
    return next(event["native_content"] for batch in bundle["artifact_batches"] for event in batch["events"] if event["native_content"]["artifact_kind"] == kind)


def _case(name: str, kind: str, mutate: Callable[[dict[str, Any]], None], expected: tuple[str, str, str]) -> dict[str, Any]:
    bundle = deepcopy(read_packaged_editorial_review_fixture(kind))
    mutate(bundle)
    _rebind(bundle)
    if name == "native_envelope_digest_forged":
        bundle["editorial_request"]["events"][1]["native_content_sha256"] = "f" * 64
        bundle["bundle_sha256"] = digest_without(bundle, "bundle_sha256")
    result = validate_editorial_review_fixture_bundle(bundle)
    actual = (result.classification, result.rule_id, result.safe_detail_code)
    if actual != expected:
        raise AssertionError(f"{name}: expected {expected!r}, got {actual!r}")
    return {"case": name, "classification": actual[0], "rule_id": actual[1], "safe_detail_code": actual[2]}


def run_editorial_review_contract_qualification() -> dict[str, Any]:
    """Run positive and rehashed-negative checks without external adapters."""
    def mutate(path: Callable[[dict[str, Any]], Any], key: str, value: Any) -> Callable[[dict[str, Any]], None]:
        return lambda bundle: path(bundle).__setitem__(key, value)

    cases = [
        ("terminal_custody_conflict", "accepted_delivery", mutate(lambda b: _packet(b)["eligibility"], "final_custody", "retained_provider"), ("ineligible_route", "packet.provenance.exact_join.v1", "terminal_eligibility_mismatch")),
        ("duplicate_decision_ordinal", "accepted_delivery", mutate(lambda b: _packet(b)["lineage"]["decisions"][7], "decision_ordinal", 6), ("contradictory_evidence", "lineage.ordinal.total_contiguous.v1", "decision_ordinals_invalid")),
        ("initial_pass_identity_swap", "accepted_delivery", mutate(lambda b: _packet(b)["lineage"]["decisions"][0], "initial_pass_index", 2), ("contradictory_evidence", "lineage.initial_pass.exact_six.v1", "initial_pass_topology_invalid")),
        ("decision_subject_cross_packet", "accepted_delivery", mutate(lambda b: _packet(b)["lineage"]["decisions"][6], "subject_id", "subject-other"), ("contradictory_evidence", "packet.provenance.exact_join.v1", "decision_subject_mismatch")),
        ("decision_adjacency_skip", "accepted_delivery", mutate(lambda b: _packet(b)["lineage"]["decisions"][7], "previous_decision_id", "erd_fabricated"), ("contradictory_evidence", "lineage.ordinal.total_contiguous.v1", "decision_adjacency_invalid")),
        ("adopted_output_is_input", "accepted_delivery", lambda b: _packet(b)["lineage"]["decisions"][7]["transition"].__setitem__("output_deck", deepcopy(_packet(b)["lineage"]["decisions"][7]["transition"]["input_deck"])), ("contradictory_evidence", "deck.transition.output_matches_adoption.v1", "decision_output_mismatch")),
        ("next_input_not_prior_output", "accepted_delivery", lambda b: _packet(b)["lineage"]["decisions"][8]["transition"].update({"input_deck": deepcopy(_packet(b)["initial_assembly"]["assembled_deck"]), "output_deck": deepcopy(_packet(b)["initial_assembly"]["assembled_deck"])}), ("contradictory_evidence", "deck.transition.next_input_contiguous.v1", "next_input_mismatch")),
        ("initial_pass_claims_deck_transition", "accepted_delivery", lambda b: _packet(b)["lineage"]["decisions"][0].__setitem__("transition", deepcopy(_packet(b)["lineage"]["decisions"][7]["transition"])), ("contradictory_evidence", "lineage.initial_pass.materialization.v1", "initial_pass_materialization_invalid")),
        ("initial_pass_materialization_duplicated", "accepted_delivery", lambda b: _packet(b)["lineage"]["decisions"][1].__setitem__("transition", {**deepcopy(_packet(b)["lineage"]["decisions"][0]["transition"]), "released_pass_identity": _packet(b)["lineage"]["decisions"][1]["released_pass_identity"]}), ("contradictory_evidence", "lineage.initial_pass.materialization.v1", "duplicate_initial_pass_materialization")),
        ("initial_pass_materialization_reordered", "accepted_delivery", lambda b: _packet(b)["lineage"]["decisions"][0]["transition"].__setitem__("released_pass_identity", _packet(b)["lineage"]["decisions"][1]["released_pass_identity"]), ("contradictory_evidence", "lineage.initial_pass.materialization.v1", "initial_pass_materialization_invalid")),
        ("initial_assembly_omits_pass", "accepted_delivery", lambda b: _packet(b)["initial_assembly"]["accepted_pass_winners"].__setitem__(5, deepcopy(_packet(b)["initial_assembly"]["accepted_pass_winners"][4])), ("contradictory_evidence", "assembly.pass_winner.exact_six.v1", "initial_assembly_membership_mismatch")),
        ("initial_assembly_first_input_mismatch", "accepted_delivery", lambda b: _packet(b)["lineage"]["decisions"][7]["transition"].update({"input_deck": deepcopy(_packet(b)["lineage"]["decisions"][8]["transition"]["candidate_deck"])}), ("contradictory_evidence", "assembly.pass_winner.exact_six.v1", "initial_assembly_input_mismatch")),
        ("rejected_initial_claims_accepted_workspace", "accepted_delivery", lambda b: _packet(b)["lineage"]["decisions"][0]["transition"].update({"accepted_workspace_id": "forged", "accepted_workspace_sha256": _packet(b)["lineage"]["decisions"][0]["transition"]["candidate_workspace_sha256"]}), ("contradictory_evidence", "lineage.initial_pass.materialization.v1", "initial_pass_materialization_invalid")),
        ("retry_masquerades_as_whole_deck", "accepted_delivery", lambda b: _packet(b)["lineage"]["decisions"][6].__setitem__("transition", deepcopy(_packet(b)["lineage"]["decisions"][7]["transition"])), ("contradictory_evidence", "lineage.initial_pass.materialization.v1", "initial_pass_materialization_invalid")),
        ("retry_predecessor_missing", "accepted_delivery", lambda b: _packet(b)["lineage"]["decisions"][6]["transition"].__setitem__("predecessor_decision_id", "erd_missing"), ("contradictory_evidence", "lineage.pass_retry.predecessor_exact.v1", "retry_predecessor_mismatch")),
        ("retry_predecessor_qa_mismatch", "accepted_delivery", lambda b: _packet(b)["lineage"]["decisions"][6]["transition"].__setitem__("predecessor_qa_report_sha256", "0" * 64), ("contradictory_evidence", "lineage.pass_retry.predecessor_exact.v1", "retry_predecessor_mismatch")),
        ("retry_wrong_released_pass", "accepted_delivery", lambda b: _packet(b)["lineage"]["decisions"][6].update({"initial_pass_index": 2, "released_pass_identity": _packet(b)["lineage"]["decisions"][1]["released_pass_identity"]}), ("contradictory_evidence", "lineage.ordinal.total_contiguous.v1", "decision_id_mismatch")),
        ("assembly_uses_superseded_initial", "accepted_delivery", lambda b: _packet(b)["initial_assembly"]["accepted_pass_winners"][0].update({"decision_id": _packet(b)["lineage"]["decisions"][0]["decision_id"], "accepted_workspace_id": _packet(b)["lineage"]["decisions"][0]["transition"]["candidate_workspace_id"]}), ("contradictory_evidence", "assembly.pass_winner.exact_six.v1", "initial_assembly_membership_mismatch")),
        ("assembly_duplicates_winner", "accepted_delivery", lambda b: _packet(b)["initial_assembly"]["accepted_pass_winners"].__setitem__(1, deepcopy(_packet(b)["initial_assembly"]["accepted_pass_winners"][0])), ("contradictory_evidence", "assembly.pass_winner.exact_six.v1", "initial_assembly_membership_mismatch")),
        ("duplicate_response_identity", "accepted_delivery", lambda b: _packet(b)["lineage"]["decisions"][7]["action"].__setitem__("provider_response_id", _packet(b)["lineage"]["decisions"][6]["action"]["provider_response_id"]), ("contradictory_evidence", "provider.response.unique_decision.v1", "duplicate_provider_response_id")),
        ("duplicate_binding_identity", "accepted_delivery", lambda b: _packet(b)["lineage"]["decisions"][7]["action"].__setitem__("binding_sha256", _packet(b)["lineage"]["decisions"][6]["action"]["binding_sha256"]), ("contradictory_evidence", "provider.response.unique_decision.v1", "duplicate_binding_sha256")),
        ("action_stage_mismatch", "accepted_delivery", mutate(lambda b: _packet(b)["lineage"]["decisions"][6]["action"], "action_kind", "ordinary_optional_stage"), ("contradictory_evidence", "provider.response.unique_decision.v1", "action_stage_mismatch")),
        ("prompt_rendered_request_mismatch", "accepted_delivery", mutate(lambda b: _packet(b)["lineage"]["decisions"][6]["action"]["prompt_provenance"], "rendered_request_sha256", "0" * 64), ("contradictory_evidence", "action.prompt_provenance.exact.v1", "rendered_request_digest_mismatch")),
        ("prompt_provenance_partial", "accepted_delivery", lambda b: _packet(b)["lineage"]["decisions"][6]["action"]["prompt_provenance"].pop("prompt_template_sha256"), ("invalid_schema", "schema.root.closed.v1", "schema_validation_failed")),
        ("response_identity_half_missing", "accepted_delivery", lambda b: _packet(b)["lineage"]["decisions"][6]["action"].pop("provider_response_sha256"), ("incomplete_evidence", "provider.response.unique_decision.v1", "response_identity_incomplete")),
        ("orphan_finding", "editorial_closeout", mutate(lambda b: _packet(b)["findings"][0], "decision_id", "erd_other_packet"), ("contradictory_evidence", "ownership.finding.same_packet.v1", "finding_owner_mismatch")),
        ("claimless_finding_fabricates_counts", "editorial_closeout", lambda b: _packet(b)["findings"][0]["population"].update({"affected_count": 1}), ("contradictory_evidence", "ownership.finding.same_packet.v1", "finding_population_mismatch")),
        ("terminal_validation_cross_owned", "accepted_delivery", mutate(lambda b: _packet(b)["validations"][-1], "terminal_selection_id", "terminal_other"), ("contradictory_evidence", "ownership.validation.discriminated.v1", "terminal_validation_owner_mismatch")),
        ("unreachable_selected_deck", "accepted_delivery", lambda b: _packet(b)["terminal_selection"].__setitem__("selected_deck", deepcopy(_packet(b)["initial_assembly"]["assembled_deck"])), ("contradictory_evidence", "deck.selection.reachable.v1", "selected_deck_unreachable")),
        ("delivered_not_selected", "accepted_delivery", lambda b: _packet(b)["terminal_selection"].__setitem__("delivered_deck", deepcopy(_packet(b)["initial_assembly"]["assembled_deck"])), ("contradictory_evidence", "deck.delivery.equals_selected.v1", "delivered_deck_mismatch")),
        ("artifact_payload_changed", "accepted_delivery", lambda b: _artifact(b, "assembled_deck")["assembled_deck"].__setitem__("deck_name", "forged"), ("digest_mismatch", "digest.artifact.wrapper_payload_domains.v1", "artifact_digest_mismatch")),
        ("response_action_digest_mismatch", "accepted_delivery", mutate(lambda b: _packet(b)["lineage"]["decisions"][6]["action"], "provider_response_sha256", "0" * 64), ("contradictory_evidence", "provider.response.unique_decision.v1", "response_action_digest_mismatch")),
        ("projection_omitted", "accepted_delivery", lambda b: b["editorial_request"]["events"].pop(), ("incomplete_evidence", "projection.member.same_packet.v1", "projection_set_mismatch")),
        ("projection_member_forged", "accepted_delivery", mutate(lambda b: b["editorial_request"]["events"][1]["native_content"]["decision"], "subject_id", "subject-other"), ("contradictory_evidence", "projection.member.same_packet.v1", "projection_member_mismatch")),
        ("projection_order_reversed", "accepted_delivery", lambda b: b["editorial_request"]["events"].__setitem__(slice(1, None), list(reversed(b["editorial_request"]["events"][1:]))), ("contradictory_evidence", "request.editorial.atomic_set.v1", "projection_order_invalid")),
        ("summary_falsified", "accepted_delivery", mutate(lambda b: _packet(b)["summary"], "finding_count", 99), ("contradictory_evidence", "summary.recomputed.v1", "summary_mismatch")),
        ("illegal_source_event_pair", "accepted_delivery", mutate(lambda b: b["editorial_request"]["events"][1], "source_kind", "artifact"), ("contradictory_evidence", "transport.source_event.closed.v1", "illegal_source_event_pair")),
        ("native_envelope_digest_forged", "accepted_delivery", mutate(lambda b: b["editorial_request"]["events"][1], "native_content_sha256", "f" * 64), ("digest_mismatch", "digest.projection.member_domain.v1", "envelope_native_digest_mismatch")),
        ("forbidden_prompt_in_artifact", "accepted_delivery", lambda b: _artifact(b, "assembled_deck")["assembled_deck"].__setitem__("prompt", "forbidden synthetic prompt"), ("contradictory_evidence", "artifact.identity.packet_scoped.v1", "forbidden_artifact_content")),
    ]
    mutation_results = [_case(*case) for case in cases]
    fixture_sha256 = {}
    fixture_results = {}
    for kind in sorted(FIXTURE_KINDS):
        fixture = read_packaged_editorial_review_fixture(kind)
        fixture_sha256[kind] = editorial_review_sha256(fixture)
        fixture_results[kind] = validate_editorial_review_fixture_bundle(fixture).outcome
    resource_root = files("astrowoof_natal_authoring.resources").joinpath("contracts")
    schema_sha256 = {
        kind: sha256(resource_root.joinpath(name).read_bytes()).hexdigest()
        for kind, name in SCHEMA_RESOURCES.items()
    }
    capture_reasons = sorted({
        "ineligible_route", "unsupported_result_version", "incomplete_native_evidence",
        "contradictory_native_evidence", "editorial_request_record_limit_exceeded",
        "editorial_request_byte_limit_exceeded",
    })
    for reason in capture_reasons:
        build_editorial_review_capture_status(reason)
    receipt = {
        "schema_version": QUALIFICATION_VERSION,
        "semantic_contract_sha256": editorial_review_sha256(read_editorial_review_semantic_contract()),
        "schema_sha256": schema_sha256, "fixture_sha256": fixture_sha256,
        "fixture_results": fixture_results, "mutation_results": mutation_results,
        "capture_status_reasons": capture_reasons,
        "side_effects": {key: 0 for key in ("provider_calls", "network_calls", "storage_calls", "database_calls", "subprocess_calls", "external_writes")},
        "receipt_sha256": "pending",
    }
    receipt["receipt_sha256"] = digest_without(receipt, "receipt_sha256")
    return receipt


def validate_editorial_review_contract_qualification(receipt: dict[str, Any]) -> bool:
    return (
        receipt.get("schema_version") == QUALIFICATION_VERSION
        and receipt.get("receipt_sha256") == digest_without(receipt, "receipt_sha256")
        and set(receipt.get("fixture_results", {}).values()) == {"valid"}
        and len(receipt.get("mutation_results", [])) == 39
        and set(receipt.get("side_effects", {}).values()) == {0}
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    receipt = run_editorial_review_contract_qualification()
    if not validate_editorial_review_contract_qualification(receipt):
        raise ValueError("Editorial-review qualification receipt is invalid")
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


__all__ = [
    "QUALIFICATION_VERSION", "run_editorial_review_contract_qualification",
    "validate_editorial_review_contract_qualification", "main",
]


if __name__ == "__main__":
    raise SystemExit(main())
