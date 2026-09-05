"""Provider-free qualification for packaged decision-evidence trace summaries."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import logging
from importlib.metadata import PackageNotFoundError, version
from importlib.resources import files
from pathlib import Path
from typing import Any

from .application_logging import configure_logging
from .run_report import parse_trace_text
from .trace_observability import (
    log_publication_evidence_summary,
    log_stage_evidence_summary,
    log_validation_evidence_summary,
)


QUALIFICATION_SCHEMA = "astrowoof.decision_evidence_observability_qualification.v1"
SCHEMA_RESOURCE = "decision-evidence-observability-qualification.v1.schema.json"
TRACE_UNITS = [
    "native_stage_evidence_summary",
    "native_validation_evidence_summary",
    "native_publication_evidence_summary",
]
CASE_CLASSIFICATIONS = [
    {"name": "accepted_polish_residual_findings", "logs_sufficient": True},
    {"name": "polish_stage_exception", "logs_sufficient": True},
    {"name": "completed_evidence_awaiting_adoption", "logs_sufficient": True},
    {"name": "provider_pending_due_or_not_due", "logs_sufficient": True},
    {"name": "ambiguous_submission", "logs_sufficient": True},
    {"name": "pre_provider_refusal", "logs_sufficient": True},
    {"name": "published_review_with_custody", "logs_sufficient": True},
    {"name": "interrupted_finalization_publication", "logs_sufficient": False},
]


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def _release() -> str:
    try:
        return version("astrowoof-natal-authoring")
    except PackageNotFoundError:
        from . import __version__
        return __version__


def read_decision_evidence_observability_qualification_schema() -> dict[str, Any]:
    return json.loads(files(
        "astrowoof_natal_authoring.resources.contracts"
    ).joinpath(SCHEMA_RESOURCE).read_text(encoding="utf-8"))


def validate_decision_evidence_observability_qualification(
    value: object,
) -> dict[str, Any]:
    required = {
        "schema_version", "sbe_release", "provider_mode",
        "external_network_calls", "provider_create_calls",
        "provider_retrieval_calls", "trace_units", "parsed_event_count",
        "code_distributions_visible", "case_classifications", "privacy",
        "qualification_sha256",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ValueError("Decision-evidence qualification shape is invalid")
    if value["schema_version"] != QUALIFICATION_SCHEMA:
        raise ValueError("Decision-evidence qualification schema is invalid")
    if value["provider_mode"] != "provider_free":
        raise ValueError("Decision-evidence qualification must be provider-free")
    for field in (
        "external_network_calls", "provider_create_calls", "provider_retrieval_calls",
    ):
        if value[field] != 0:
            raise ValueError(f"Decision-evidence qualification {field} must be zero")
    if value["trace_units"] != TRACE_UNITS or value["parsed_event_count"] != 3:
        raise ValueError("Decision-evidence trace unit inventory is invalid")
    if value["code_distributions_visible"] is not True:
        raise ValueError("Decision-evidence code distributions are not visible")
    if value["case_classifications"] != CASE_CLASSIFICATIONS:
        raise ValueError("Decision-evidence replay matrix is invalid")
    if value["privacy"] != {
        "protected_sentinel_absent": True,
        "payloads_absent": True,
        "finding_prose_absent": True,
        "absolute_workspace_path_absent": True,
    }:
        raise ValueError("Decision-evidence privacy assertions are invalid")
    basis = {key: item for key, item in value.items() if key != "qualification_sha256"}
    if value["qualification_sha256"] != _digest(basis):
        raise ValueError("Decision-evidence qualification digest is invalid")
    return value


def run_decision_evidence_observability_qualification() -> dict[str, Any]:
    protected = "PROTECTED-DECISION-EVIDENCE-SENTINEL"
    stream = io.StringIO()
    configure_logging(stream=stream, force=True)
    logger = logging.getLogger("decision-evidence-qualification")
    log_stage_evidence_summary(logger, {
        "attempt_number": 2, "state": "POLISH_ERROR", "accepted": False,
        "error": {"type": "ValueError", "message": protected},
        "private_payload": protected,
    }, stage="polish", subject_id="dog-qualification")
    log_validation_evidence_summary(
        logger, subject_id="dog-qualification",
        validation_report={"status": "pass", "errors": [], "warnings": []},
        lint_report={
            "status": "warn", "warning_count": 1,
            "decks": [{
                "warnings": [{"code": "repeated_opening", "message": protected}],
                "authoring_pass_acceptance": {
                    "status": "reject",
                    "rejection_reasons": [{
                        "code": "cross_card_exact_duplicate", "message": protected,
                    }],
                },
            }],
        },
    )
    log_publication_evidence_summary(
        logger,
        {
            "status": "FINAL_QA_REQUIRES_REVIEW", "state_revision": 12,
            "spend_ledger": {"actions": [{
                "action_id": "paid_0123456789abcdef01234567", "state": "WAITING",
                "provider": {"id": "resp_qualification"},
            }]},
            "subjects": {}, "private_payload": protected,
        },
        {
            "run_id": "run-qualification", "outcome": "review_required",
            "cause_code": "final_qa_requires_review",
            "result_id": "nres_0123456789abcdef01234567",
            "result_sha256": "a" * 64,
        },
        {
            "receipt_id": "nreceipt_0123456789abcdef01234567",
            "receipt_sha256": "b" * 64,
        },
    )
    raw = stream.getvalue()
    rendered = "\n".join(
        f"2026-09-04T12:00:00Z {line}" for line in raw.splitlines()
    )
    trace = parse_trace_text(rendered, source_name="qualification.log")
    events = trace["events"]
    units = [event["event"] for event in events]
    if units != TRACE_UNITS:
        raise ValueError(f"Decision-evidence trace units are incomplete: {units}")
    validation = events[1]["fields"]
    visible = (
        "codes:repeated_opening:1" in validation.get("lint_warning_codes", "")
        and "codes:cross_card_exact_duplicate:1"
        in validation.get("rejection_codes", "")
    )
    if protected in raw or protected in json.dumps(trace, sort_keys=True):
        raise ValueError("Decision-evidence trace leaked protected material")
    value = {
        "schema_version": QUALIFICATION_SCHEMA,
        "sbe_release": _release(),
        "provider_mode": "provider_free",
        "external_network_calls": 0,
        "provider_create_calls": 0,
        "provider_retrieval_calls": 0,
        "trace_units": units,
        "parsed_event_count": len(events),
        "code_distributions_visible": visible,
        "case_classifications": CASE_CLASSIFICATIONS,
        "privacy": {
            "protected_sentinel_absent": True,
            "payloads_absent": True,
            "finding_prose_absent": True,
            "absolute_workspace_path_absent": True,
        },
    }
    value["qualification_sha256"] = _digest(value)
    return validate_decision_evidence_observability_qualification(value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    value = run_decision_evidence_observability_qualification()
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
