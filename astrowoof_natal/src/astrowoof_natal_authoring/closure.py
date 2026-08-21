#!/usr/bin/env python3
"""Orchestrate AstroWoof semantic-closure extraction and authoring.

The runner supports a deterministic fake provider for token-free workflow
tests and concurrent OpenAI Responses workers for live authoring.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Protocol

from . import __version__
from . import editorial_lint as editorial_lint_module
from . import validation as validation_module
from .assembly import assemble
from .application_logging import (
    add_logging_arguments,
    bind_logging_context,
    configure_logging_from_args,
    logging_context,
)
from .basis_policies import AXIS_AWARE_POLICY_ID, LEGACY_ATOMIC_POLICY_ID
from .contracts import (
    DELIVERY_MANIFEST_SCHEMA,
    authoring_profile,
    discover_projected_input,
    public_run_state,
)
from .editorial_lint import reader_facing_items
from .execution_events import (
    ExecutionEventEmitter,
    JsonlEventSink,
    StdoutJsonlSink,
    command_result_envelope,
)
from .pass_acceptance import CONTEXT_FILTER_VOCABULARY
from .pass_protocol import bind_logical_pass_request
from .initial_wave import (
    INITIAL_WAVE_BINDING_BUNDLE_FILENAME,
    InitialWaveError,
    InitialWaveMemberSpec,
    ProviderCreateResult as InitialWaveProviderCreateResult,
    build_initial_wave,
    build_initial_wave_binding_bundle,
    build_wave_authorization,
    execute_initial_wave_creates,
    preflight_wave_authorization,
    validate_initial_wave,
    validate_initial_wave_binding_bundle_against_wave,
)
from .provenance import (
    artifact_descriptor,
    initial_provenance,
    migrated_run_provenance,
    refresh_execution_provenance,
)
from .reconciliation import initial_timing, record_attempt
from .response_diagnostics import sanitize_error_message, sanitized_endpoint
from .spend import (
    AmbiguousProviderSubmission,
    AwaitingSpendAuthorization,
    BudgetExhausted,
    PRICE_BOOK_VERSION,
    PRICE_BOOK_USD_PER_MILLION,
    action_binding,
    append_reconciliation_reference,
    authorize_action,
    begin_submission,
    classify_prepared_budget,
    conservative_commitment_micros,
    digest as spend_digest,
    mark_ambiguous,
    new_ledger,
    prepare_action,
    profile_digest as spend_profile_digest,
    record_provider_id,
    record_reported_cost,
    validate_policy,
)


logger = logging.getLogger(__name__)


SCHEMA_VERSION = "astrowoof.semantic_closure_run.v0.9"
SNAPSHOT_SCHEMA = "astrowoof.semantic_closure_snapshot.v0.1"
SNAPSHOT_NAME = "workspace-snapshot.json"
PASS_COUNT = 6
TERMINAL_STATES = {"PASS_QA_ACCEPTED", "FAILED_REQUIRES_REVIEW"}
FINAL_SUCCESS_STATES = {"DELIVERY_COMPLETE", "DELIVERY_COMPLETE_WITH_WARNINGS"}
WRITABLE_FILE_NAMES = {
    "WRITE WHOLE DOG PROFILE.md",
    "WRITE SUMMARY THESIS PLAN.md",
    "WRITE THIS CARD.md",
    "WRITE THIS SUMMARY.md",
    "ASSIGN THEME GROUPS.md",
}
RETRYABLE_HTTP_STATUSES = {408, 409, 429, 500, 502, 503, 504}
MODEL_PRICING_USD_PER_MILLION = {
    model: {name: float(value) for name, value in rates.items()}
    for model, rates in PRICE_BOOK_USD_PER_MILLION.items()
}
TOKEN_ESTIMATE_METHOD = "utf8_bytes_divided_by_4"
STATIC_AUTHORING_FILES = {
    "AUTHORING BRIEF.md",
    "GUIDING LIGHTS.md",
}
SUBJECT_AUTHORING_FILES = {
    "DOG DETAILS.md",
    "FULL CHART BASIS.md",
    "WRITE WHOLE DOG PROFILE.md",
}
PROVIDER_VISIBLE_SUBJECT_FIELDS = (
    "subject_id",
    "display_name",
    "subject_type",
    "gender",
    "pronouns",
    "breed",
)
PROTECTED_SUBJECT_FIELDS = (
    "birth_date",
    "birth_datetime",
    "birth_latitude",
    "birth_longitude",
    "birth_location",
    "birth_date_precision",
)
FIELD_PATTERN = re.compile(
    r"(<!-- BEGIN FIELD: ([a-zA-Z0-9_.]+) -->\s*\n)"
    r"(.*?)"
    r"(\n<!-- END FIELD: \2 -->)",
    re.DOTALL,
)
_SNAPSHOT_HASH_CACHE: dict[str, tuple[int, int, str]] = {}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        temporary = Path(handle.name)
        handle.write(rendered)
        handle.flush()
    for attempt in range(5):
        try:
            temporary.replace(path)
            break
        except PermissionError:
            if attempt == 4:
                raise
            # Windows virus scanners and indexers can briefly hold either the
            # destination or freshly flushed temporary file. Preserve atomic
            # replacement while tolerating that transient lock.
            time.sleep(0.05 * (attempt + 1))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_path(path: Path) -> str:
    return str(path.resolve())


def provider_visible_subject(subject: Any) -> dict[str, Any]:
    """Return the explicit editorial identity view permitted to providers."""
    if not isinstance(subject, dict):
        return {}
    return {
        field: deepcopy(subject[field])
        for field in PROVIDER_VISIBLE_SUBJECT_FIELDS
        if field in subject
    }


def provider_visible_markdown(relative: str, text: str) -> str:
    """Remove protected DOG DETAILS lines at the final prompt boundary."""
    if relative != "DOG DETAILS.md":
        return text
    protected_labels = {
        "Birth date",
        "Birth datetime",
        "Birth latitude",
        "Birth longitude",
        "Birth location",
        "Birth-date precision",
    }
    return "\n".join(
        line
        for line in text.splitlines()
        if not any(line.startswith(f"- **{label}:**") for label in protected_labels)
    ) + ("\n" if text.endswith("\n") else "")


def estimated_text_tokens(value: str) -> int:
    """Return a dependency-free planning estimate, never API billing usage."""
    byte_count = len(value.encode("utf-8"))
    return (byte_count + 3) // 4


def text_measurement(value: str) -> dict[str, Any]:
    return {
        "characters": len(value),
        "utf8_bytes": len(value.encode("utf-8")),
        "estimated_tokens": estimated_text_tokens(value),
        "token_estimate_method": TOKEN_ESTIMATE_METHOD,
        "sha256": hashlib.sha256(value.encode("utf-8")).hexdigest(),
    }


def safe_extract_zip(archive_path: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    destination_root = destination.resolve()
    with zipfile.ZipFile(archive_path) as archive:
        for member in archive.infolist():
            target = (destination / member.filename).resolve()
            try:
                target.relative_to(destination_root)
            except ValueError as exc:
                raise ValueError(
                    f"Unsafe ZIP member in {archive_path}: {member.filename}"
                ) from exc
        archive.extractall(destination)


def find_workspace_root(extracted: Path, expected_name: str) -> Path:
    direct = extracted / expected_name
    if (direct / "START HERE.md").is_file():
        return direct
    matches = [
        path.parent
        for path in extracted.rglob("START HERE.md")
        if path.parent.name == expected_name
    ]
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one {expected_name!r} workspace in {extracted}; "
            f"found {len(matches)}"
        )
    return matches[0]


@dataclass(frozen=True)
class PassSpec:
    pass_id: str
    subject: str
    pass_number: int
    source_zip: Path
    source_sha256: str


@dataclass(frozen=True)
class ProviderResult:
    workspace: Path
    metadata: dict[str, Any]


class AuthoringProvider(Protocol):
    name: str

    def author(
        self,
        source_workspace: Path,
        response_workspace: Path,
        spec: PassSpec,
        attempt_number: int,
        feedback: dict[str, Any] | None = None,
        before_submit: Any = None,
        provider_created: Any = None,
    ) -> ProviderResult:
        """Author one fresh pass workspace."""


def _fake_field_value(
    *,
    pass_id: str,
    relative_file: str,
    field: str,
    occurrence: int,
) -> str:
    stable_identity = "\n".join(
        (pass_id, relative_file.replace("\\", "/"), field, str(occurrence))
    )
    identity = re.sub(
        r"[^a-z0-9]+",
        " ",
        f"{pass_id} {relative_file} {field} {occurrence}".lower(),
    ).strip()
    identity_digest = hashlib.sha256(stable_identity.encode("utf-8")).hexdigest()
    identity_token = "".join(
        chr(ord("a") + int(nibble, 16))
        for nibble in identity_digest[:16]
    )
    if field in {
        "context_filter_groups.high_level",
        "context_filter_groups.detail_level",
    }:
        return (
            "Personality"
            if field.endswith("high_level")
            else "Core Personality"
        )
    if field.startswith("theme_group_registry."):
        section = field.split(".")[1]
        titles = {
            "interdogpendence": [
                ("bond_dynamics", "Bond Dynamics", "Bonds", "🔗", "How closeness, trust, and mutual attention shape the relationship."),
                ("shared_rhythms", "Shared Rhythms", "Rhythms", "🐾", "How dog and handler find a workable pace together."),
                ("productive_tensions", "Productive Tensions", "Tensions", "⚡", "Where friction can become useful information and growth."),
                ("mutual_adjustments", "Mutual Adjustments", "Adjustments", "🤝", "How both sides adapt without losing what matters."),
            ],
            "takeaways": [
                ("essential_character", "Essential Character", "Character", "✨", "The qualities that make this dog unmistakably herself."),
                ("daily_wisdom", "Daily Wisdom", "Daily Life", "🏡", "What everyday life reveals about her natural operating style."),
                ("growth_lessons", "Growth Lessons", "Growth", "🌱", "Where practice and support can help potential unfold."),
                ("lasting_gifts", "Lasting Gifts", "Gifts", "🎁", "The strengths she brings to the people and places she loves."),
            ],
        }
        return json.dumps([
            {
                "id": item[0],
                "title": item[1],
                "short_title": item[2],
                "emoji": item[3],
                "subtitle": item[4],
                "order": index,
            }
            for index, item in enumerate(titles[section], start=1)
        ], ensure_ascii=False)
    if field.startswith("theme_group.interdogpendence."):
        return ["bond_dynamics", "shared_rhythms", "productive_tensions", "mutual_adjustments"][(occurrence - 1) % 4]
    if field.startswith("theme_group.takeaways."):
        return ["essential_character", "daily_wisdom", "growth_lessons", "lasting_gifts"][(occurrence - 1) % 4]
    if field.startswith("plan."):
        return (
            f"Editorial plan {identity} follows a singular behavioral doorway "
            f"and keeps this assignment distinct."
        )
    if ".headline." in field:
        return f"A Singular Portrait {identity.title()}"
    if ".body." in field:
        return (
            f"Insight {identity_token} reveals one memorable behavior through "
            f"an independent cadence."
        )
    if field.startswith("dos."):
        return f"Encourage the specific strength described by {identity}."
    if field.startswith("donts."):
        return f"Do not flatten the distinctive need described by {identity}."
    if "quotes." in field:
        return f"I have reviewed the evidence for {identity}, and request snacks."
    if "jokes." in field:
        return f"The comic premise for {identity} has excellent treat potential."
    return f"Authored value for {identity}."


def fill_fake_workspace(workspace: Path) -> None:
    pass_id = workspace.name
    for path in sorted(workspace.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if "__WRITE__" not in text:
            continue
        relative_file = path.relative_to(workspace).as_posix()
        field_occurrences: dict[str, int] = {}

        def replace(match: re.Match[str]) -> str:
            field = match.group(2)
            occurrence_key = (
                field.rsplit(".", 1)[0]
                if field.startswith("theme_group.")
                else field
            )
            occurrence = field_occurrences.get(occurrence_key, 0) + 1
            field_occurrences[occurrence_key] = occurrence
            value = _fake_field_value(
                pass_id=pass_id,
                relative_file=relative_file,
                field=field,
                occurrence=occurrence,
            )
            return f"{match.group(1)}{value}{match.group(4)}"

        rendered = FIELD_PATTERN.sub(replace, text)
        unfinished_fields = [
            field
            for _, field, value, _ in FIELD_PATTERN.findall(rendered)
            if "__WRITE__" in value
        ]
        if unfinished_fields:
            raise ValueError(
                f"Marked placeholders remain in {path}: "
                f"{', '.join(unfinished_fields)}"
            )
        path.write_text(rendered, encoding="utf-8")


class FakeAuthoringProvider:
    """Deterministic local provider used to prove orchestration behavior."""

    name = "fake"

    def __init__(
        self,
        *,
        reject_attempts: dict[str, int] | None = None,
        error_attempts: dict[str, int] | None = None,
    ) -> None:
        self.reject_attempts = reject_attempts or {}
        self.error_attempts = error_attempts or {}

    def author(
        self,
        source_workspace: Path,
        response_workspace: Path,
        spec: PassSpec,
        attempt_number: int,
        feedback: dict[str, Any] | None = None,
        before_submit: Any = None,
        provider_created: Any = None,
    ) -> ProviderResult:
        if attempt_number <= self.error_attempts.get(spec.pass_id, 0):
            raise RuntimeError(
                f"Injected provider error for {spec.pass_id} attempt "
                f"{attempt_number}"
            )
        shutil.copytree(source_workspace, response_workspace)
        fill_fake_workspace(response_workspace)
        if attempt_number <= self.reject_attempts.get(spec.pass_id, 0):
            writing_files = sorted(
                response_workspace.rglob("WRITE THIS CARD.md")
            )
            if len(writing_files) >= 2:
                duplicate = (
                    "This deliberately duplicated sentence makes the local "
                    "acceptance gate reject the simulated authoring attempt."
                )
                for path in writing_files[:2]:
                    text = path.read_text(encoding="utf-8")
                    body_match = re.search(
                        r"(<!-- BEGIN FIELD: [^.]+\.body\.[^ ]+ -->\s*\n)"
                        r"(.*?)"
                        r"(\n<!-- END FIELD: [^.]+\.body\.[^ ]+ -->)",
                        text,
                        re.DOTALL,
                    )
                    if body_match:
                        text = (
                            text[:body_match.start(2)]
                            + duplicate
                            + text[body_match.end(2):]
                        )
                        path.write_text(text, encoding="utf-8")
        return ProviderResult(
            workspace=response_workspace,
            metadata={
                "provider": self.name,
                "deterministic": True,
                "injected_rejection": (
                    attempt_number
                    <= self.reject_attempts.get(spec.pass_id, 0)
                ),
            },
        )


class OpenAIServiceError(RuntimeError):
    """An OpenAI service or protocol failure."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        request_id: str | None = None,
        retryable: bool = False,
        fatal: bool = False,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.request_id = request_id
        self.retryable = retryable
        self.fatal = fatal


class AuthoringProviderError(RuntimeError):
    """A completed provider attempt that carries billable metadata."""

    def __init__(
        self,
        message: str,
        *,
        metadata: dict[str, Any],
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.metadata = metadata
        self.details = details or {}


class BackgroundResponsePending(RuntimeError):
    """A durable background response outlived this local polling window."""

    def __init__(self, message: str, *, metadata: dict[str, Any]) -> None:
        super().__init__(message)
        self.metadata = metadata


class IncompleteAuthoringDelivery(RuntimeError):
    """A response workspace is missing required files or authored fields."""

    def __init__(
        self,
        message: str,
        *,
        missing_files: list[str] | None = None,
        missing_fields: dict[str, list[str]] | None = None,
    ) -> None:
        super().__init__(message)
        self.details = {
            "issue_code": "incomplete_delivery",
            "missing_files": missing_files or [],
            "missing_fields": missing_fields or {},
        }


class JsonHttpTransport(Protocol):
    def request_json(
        self,
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any] | None,
        timeout_seconds: float,
    ) -> dict[str, Any]:
        """Send one JSON request and return one decoded JSON object."""


class UrllibJsonTransport:
    """Small dependency-free JSON transport for the OpenAI REST API."""

    def request_json(
        self,
        *,
        method: str,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any] | None,
        timeout_seconds: float,
    ) -> dict[str, Any]:
        body = (
            json.dumps(payload, ensure_ascii=False).encode("utf-8")
            if payload is not None
            else None
        )
        request = urllib.request.Request(
            url=url,
            data=body,
            headers=headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(
                request,
                timeout=timeout_seconds,
            ) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            message = raw[:2000] or str(exc)
            try:
                decoded = json.loads(raw)
                message = (
                    decoded.get("error", {}).get("message")
                    or decoded.get("message")
                    or message
                )
            except (json.JSONDecodeError, AttributeError):
                pass
            raise OpenAIServiceError(
                f"OpenAI HTTP {exc.code}: {message}",
                status_code=exc.code,
                request_id=(
                    exc.headers.get("x-request-id")
                    if exc.headers is not None else None
                ),
                retryable=exc.code in RETRYABLE_HTTP_STATUSES,
                fatal=exc.code in {401, 403, 422},
            ) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise OpenAIServiceError(
                f"OpenAI transport error: {exc}",
                retryable=True,
            ) from exc
        try:
            decoded = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise OpenAIServiceError(
                "OpenAI returned a non-JSON response",
                retryable=False,
            ) from exc
        if not isinstance(decoded, dict):
            raise OpenAIServiceError(
                "OpenAI returned a JSON value that was not an object",
                retryable=False,
            )
        return decoded


def writable_fields(workspace: Path) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for path in sorted(workspace.rglob("*.md")):
        if path.name not in WRITABLE_FILE_NAMES:
            continue
        fields = [
            match.group(2)
            for match in FIELD_PATTERN.finditer(
                path.read_text(encoding="utf-8")
            )
        ]
        if not fields:
            raise ValueError(f"Writable file has no field markers: {path}")
        if len(fields) != len(set(fields)):
            raise ValueError(f"Writable file repeats a field marker: {path}")
        result[path.relative_to(workspace).as_posix()] = fields
    if not result:
        raise ValueError(f"No writable Markdown files found in {workspace}")
    return result


def authoring_output_schema(
    expected_fields: dict[str, list[str]],
) -> dict[str, Any]:
    file_properties: dict[str, Any] = {}
    for relative_path, fields in expected_fields.items():
        file_properties[relative_path] = {
            "type": "object",
            "properties": {
                field: {
                    "type": "string",
                    "description": (
                        "Finished field content only, without marker comments."
                    ),
                }
                for field in fields
            },
            "required": fields,
            "additionalProperties": False,
        }
    return {
        "type": "object",
        "properties": {
            "files": {
                "type": "object",
                "properties": file_properties,
                "required": list(file_properties),
                "additionalProperties": False,
            },
        },
        "required": ["files"],
        "additionalProperties": False,
    }


def render_workspace_input(workspace: Path) -> str:
    return render_workspace_files(workspace, sorted(workspace.rglob("*.md")))


def render_workspace_files(workspace: Path, paths: list[Path]) -> str:
    sections = []
    for path in paths:
        relative = path.relative_to(workspace).as_posix()
        visible_text = provider_visible_markdown(
            relative, path.read_text(encoding="utf-8")
        )
        sections.append(
            f"\n===== BEGIN FILE: {relative} =====\n"
            f"{visible_text}"
            f"\n===== END FILE: {relative} =====\n"
        )
    if not sections:
        raise ValueError(f"No Markdown input files found in {workspace}")
    return "".join(sections)


def partition_workspace_prompt(workspace: Path) -> dict[str, str]:
    """Split generated Markdown into cache-stable prompt tiers."""
    tiers: dict[str, list[Path]] = {
        "static": [],
        "subject": [],
        "assignment": [],
    }
    for path in sorted(workspace.rglob("*.md")):
        relative = path.relative_to(workspace).as_posix()
        if relative in STATIC_AUTHORING_FILES:
            tiers["static"].append(path)
        elif relative in SUBJECT_AUTHORING_FILES:
            tiers["subject"].append(path)
        else:
            tiers["assignment"].append(path)
    if not tiers["static"] or not tiers["subject"] or not tiers["assignment"]:
        raise ValueError(
            f"Workspace cannot be partitioned into cache tiers: {workspace}"
        )
    return {
        name: render_workspace_files(workspace, paths)
        for name, paths in tiers.items()
    }


def workspace_file_inventory(workspace: Path) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for path in sorted(workspace.rglob("*.md")):
        relative = path.relative_to(workspace).as_posix()
        tier = (
            "static"
            if relative in STATIC_AUTHORING_FILES
            else "subject"
            if relative in SUBJECT_AUTHORING_FILES
            else "assignment"
        )
        result.append(
            {
                "path": relative,
                "tier": tier,
                **text_measurement(path.read_text(encoding="utf-8")),
            }
        )
    return result


def retry_feedback_from_record(
    record: dict[str, Any],
) -> dict[str, Any] | None:
    if not record.get("attempts"):
        return None
    attempt = record["attempts"][-1]
    qa_report = (attempt.get("qa") or {}).get("report") or {}
    if qa_report.get("status") == "reject":
        rejected_reports = []
        issue_codes: list[str] = []
        affected_claim_ids: list[str] = []
        for prior_attempt in record["attempts"]:
            prior_report = (prior_attempt.get("qa") or {}).get("report") or {}
            if prior_report.get("status") != "reject":
                continue
            prior_codes = prior_report.get("editorial_issue_codes", [])
            prior_claims = prior_report.get("affected_claim_ids", [])
            rejected_reports.append(
                {
                    "attempt_number": prior_attempt.get("attempt_number"),
                    "editorial_issue_codes": prior_codes,
                    "affected_claim_ids": prior_claims,
                }
            )
            for code in prior_codes:
                if code not in issue_codes:
                    issue_codes.append(code)
            for claim_id in prior_claims:
                if claim_id not in affected_claim_ids:
                    affected_claim_ids.append(claim_id)
        return {
            "kind": "editorial_qa_rejection",
            "editorial_issue_codes": issue_codes,
            "affected_claim_ids": affected_claim_ids,
            "prior_rejections": rejected_reports,
            "guidance": qa_report.get("guidance"),
        }
    error = attempt.get("error")
    if error:
        details = error.get("details") or {}
        return {
            "kind": (
                "incomplete_delivery"
                if details.get("issue_code") == "incomplete_delivery"
                else "malformed_or_failed_attempt"
            ),
            "error_type": error.get("type"),
            "missing_files": details.get("missing_files", []),
            "missing_fields": details.get("missing_fields", {}),
            "guidance": (
                "The prior response could not be reconstructed or validated. "
                "Return every required field exactly once in the requested "
                "structured output."
            ),
        }
    return None


def apply_authored_fields(
    source_workspace: Path,
    response_workspace: Path,
    authored: dict[str, Any],
) -> None:
    expected = writable_fields(source_workspace)
    files = authored.get("files")
    if not isinstance(files, dict):
        raise ValueError("Structured output lacks the required files object")
    if set(files) != set(expected):
        missing = sorted(set(expected) - set(files))
        extra = sorted(set(files) - set(expected))
        raise ValueError(
            f"Structured output file mismatch; missing={missing}, extra={extra}"
        )
    if response_workspace.exists():
        shutil.rmtree(response_workspace)
    shutil.copytree(source_workspace, response_workspace)
    for relative_path, fields in expected.items():
        values = files[relative_path]
        if not isinstance(values, dict) or set(values) != set(fields):
            missing = sorted(set(fields) - set(values or {}))
            extra = sorted(set(values or {}) - set(fields))
            raise ValueError(
                f"{relative_path}: field mismatch; "
                f"missing={missing}, extra={extra}"
            )
        target = response_workspace / Path(relative_path)
        text = target.read_text(encoding="utf-8")
        seen: set[str] = set()

        def replace(match: re.Match[str]) -> str:
            field = match.group(2)
            if field not in values:
                return match.group(0)
            value = values[field]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{relative_path}: field {field} is not a non-empty string"
                )
            if "__WRITE__" in value:
                raise ValueError(
                    f"{relative_path}: field {field} retains a placeholder"
                )
            if "<!-- BEGIN FIELD:" in value or "<!-- END FIELD:" in value:
                raise ValueError(
                    f"{relative_path}: field {field} contains marker comments"
                )
            seen.add(field)
            return f"{match.group(1)}{value.strip()}{match.group(4)}"

        rendered = FIELD_PATTERN.sub(replace, text)
        if seen != set(fields):
            raise ValueError(
                f"{relative_path}: source markers changed during reconstruction"
            )
        target.write_text(rendered, encoding="utf-8")


def repair_workspace_context_filters(workspace: Path) -> list[dict[str, Any]]:
    """Remove unregistered card-filter labels without touching authored prose."""
    repairs: list[dict[str, Any]] = []
    cards_root = workspace / "cards"
    if not cards_root.is_dir():
        return repairs
    for story_dir in sorted(path for path in cards_root.iterdir() if path.is_dir()):
        target = story_dir / "WRITE THIS CARD.md"
        if not target.is_file():
            continue
        text = target.read_text(encoding="utf-8")
        claim_id = story_dir.name.split(" -- ", 1)[-1]

        def replace(match: re.Match[str]) -> str:
            field = match.group(2)
            allowed = CONTEXT_FILTER_VOCABULARY.get(field)
            if allowed is None:
                return match.group(0)
            retained: list[str] = []
            removed: list[str] = []
            for line in match.group(3).splitlines():
                value = re.sub(r"^\s*[-*]\s+", "", line).strip()
                if not value:
                    continue
                if value in allowed and value not in retained:
                    retained.append(value)
                else:
                    removed.append(value)
            if not removed:
                return match.group(0)
            repairs.append({
                "claim_id": claim_id,
                "field": field,
                "removed": removed,
                "retained": retained,
            })
            rendered = "\n".join(f"- {value}" for value in retained)
            return f"{match.group(1)}{rendered}{match.group(4)}"

        rendered = FIELD_PATTERN.sub(replace, text)
        if rendered != text:
            target.write_text(rendered, encoding="utf-8")
    return repairs


def require_complete_authored_workspace(
    source_workspace: Path,
    response_workspace: Path,
) -> None:
    """Reject incomplete delivery before the opaque editorial checker runs."""
    expected = writable_fields(source_workspace)
    missing_files: list[str] = []
    missing_fields: dict[str, list[str]] = {}
    for relative_path, fields in expected.items():
        target = response_workspace / Path(relative_path)
        if not target.is_file():
            missing_files.append(relative_path)
            continue
        text = target.read_text(encoding="utf-8")
        parsed = {
            match.group(2): match.group(3).strip()
            for match in FIELD_PATTERN.finditer(text)
        }
        absent = [
            field
            for field in fields
            if not parsed.get(field) or "__WRITE__" in parsed[field]
        ]
        if absent:
            missing_fields[relative_path] = absent
    if missing_files or missing_fields:
        raise IncompleteAuthoringDelivery(
            "Authored workspace is incomplete; "
            f"missing_files={missing_files}, missing_fields={missing_fields}",
            missing_files=missing_files,
            missing_fields=missing_fields,
        )


def response_output_text(response: dict[str, Any]) -> str:
    direct = response.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct
    texts: list[str] = []
    for item in response.get("output", []):
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if not isinstance(content, dict):
                continue
            if content.get("type") == "output_text":
                text = content.get("text")
                if isinstance(text, str):
                    texts.append(text)
            elif content.get("type") == "refusal":
                refusal = content.get("refusal")
                if isinstance(refusal, str):
                    raise OpenAIServiceError(
                        f"OpenAI refused the authoring request: {refusal}"
                    )
    if not texts:
        raise OpenAIServiceError("Completed response contains no output text")
    return "".join(texts)


def reconciled_response_evidence(
    attempt_root: Path, response_id: str,
) -> dict[str, Any] | None:
    """Load a completed response already retrieved by a bounded native cycle."""
    run_dir = next(
        (parent for parent in attempt_root.parents if (parent / "run.json").is_file()),
        None,
    )
    if run_dir is None:
        return None
    run_json = run_dir / "run.json"
    state = load_json(run_json)
    action = next((
        item for item in (state.get("spend_ledger") or {}).get("actions", [])
        if (item.get("provider") or {}).get("id") == response_id
    ), None)
    if action is None:
        return None
    timing = action.get("provider_reconciliation") or {}
    if timing.get("last_outcome") != "completed":
        return None
    path = (
        run_dir / "lifecycle" / "provider-reconciliation" /
        f"{action['action_id']}.response.json"
    )
    if not path.is_file():
        raise ValueError("Completed reconciliation evidence is missing")
    response = load_json(path)
    if response.get("id") != response_id or response.get("status") != "completed":
        raise ValueError("Completed reconciliation evidence identity is invalid")
    return response


def normalized_usage(response: dict[str, Any]) -> dict[str, int]:
    usage = response.get("usage") or {}
    input_details = usage.get("input_tokens_details") or {}
    return {
        "input_tokens": int(usage.get("input_tokens") or 0),
        "cached_input_tokens": int(
            input_details.get("cached_tokens") or 0
        ),
        "cache_write_tokens": int(
            input_details.get("cache_write_tokens") or 0
        ),
        "output_tokens": int(usage.get("output_tokens") or 0),
        "reasoning_tokens": int(
            (usage.get("output_tokens_details") or {}).get(
                "reasoning_tokens"
            )
            or 0
        ),
        "total_tokens": int(usage.get("total_tokens") or 0),
    }


def estimated_cost(
    model: str,
    usage: dict[str, int],
) -> dict[str, Any] | None:
    pricing = MODEL_PRICING_USD_PER_MILLION.get(model)
    if not pricing:
        return None
    cached = min(
        usage["cached_input_tokens"],
        usage["input_tokens"],
    )
    cache_write = min(
        usage.get("cache_write_tokens", 0),
        max(usage["input_tokens"] - cached, 0),
    )
    uncached = max(usage["input_tokens"] - cached - cache_write, 0)
    rates = {
        **pricing,
        "cache_write": pricing.get("cache_write", pricing["input"] * 1.25),
    }
    components = {
        "uncached_input": uncached * rates["input"] / 1_000_000,
        "cached_input": cached * rates["cached_input"] / 1_000_000,
        "cache_write": cache_write * rates["cache_write"] / 1_000_000,
        "output": usage["output_tokens"] * rates["output"] / 1_000_000,
    }
    amount = sum(components.values())
    return {
        "currency": "USD",
        "estimated_amount": round(amount, 8),
        "pricing_version": "2026-07-31",
        "rates_per_million_tokens": rates,
        "billable_tokens": {
            "uncached_input": uncached,
            "cached_input": cached,
            "cache_write": cache_write,
            "output": usage["output_tokens"],
        },
        "components": {
            key: round(value, 8) for key, value in components.items()
        },
        "note": (
            "Estimate includes explicit cache writes at 1.25x ordinary input; "
            "the OpenAI usage dashboard remains authoritative."
        ),
    }


def batch_estimated_cost(model: str, usage: dict[str, int]) -> dict[str, Any] | None:
    """Apply the documented 50% Batch API discount to a normal estimate."""
    ordinary = estimated_cost(model, usage)
    if ordinary is None:
        return None
    discounted = deepcopy(ordinary)
    discounted["estimated_amount"] = round(
        float(ordinary["estimated_amount"]) * 0.5, 8
    )
    discounted["components"] = {
        key: round(float(value) * 0.5, 8)
        for key, value in ordinary["components"].items()
    }
    discounted["service_level"] = "batch"
    discounted["discount_ratio"] = 0.5
    discounted["note"] = (
        "Estimate applies the documented Batch API 50% discount; actual "
        "usage and billing remain authoritative. Prompt-cache savings are "
        "reported from returned cached-token usage, not assumed."
    )
    return discounted


class OpenAIResponsesProvider:
    """Author a pass with one fresh OpenAI Responses API job."""

    name = "openai"

    def __init__(
        self,
        *,
        api_key: str,
        model: str = "gpt-5.6-terra",
        reasoning_effort: str = "medium",
        base_url: str = "https://api.openai.com/v1",
        background: bool = True,
        poll_interval_seconds: float = 2.0,
        response_timeout_seconds: float = 1800.0,
        http_timeout_seconds: float = 60.0,
        max_transport_retries: int = 4,
        transport_backoff_seconds: float = 1.0,
        max_output_tokens: int = 100_000,
        safety_identifier: str | None = None,
        prompt_cache_mode: str = "explicit",
        prompt_cache_ttl: str = "30m",
        transport: JsonHttpTransport | None = None,
        sleep: Any = time.sleep,
        require_spend_authorization: bool = False,
    ) -> None:
        if not api_key:
            raise ValueError("OpenAI API key is required")
        self.api_key = api_key
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.base_url = base_url.rstrip("/")
        self.background = background
        self.poll_interval_seconds = poll_interval_seconds
        self.response_timeout_seconds = response_timeout_seconds
        self.http_timeout_seconds = http_timeout_seconds
        self.max_transport_retries = max_transport_retries
        self.transport_backoff_seconds = transport_backoff_seconds
        self.max_output_tokens = max_output_tokens
        self.safety_identifier = safety_identifier
        if prompt_cache_mode not in {"disabled", "implicit", "explicit"}:
            raise ValueError(f"Unsupported prompt cache mode: {prompt_cache_mode}")
        self.prompt_cache_mode = prompt_cache_mode
        self.prompt_cache_ttl = prompt_cache_ttl
        self.transport = transport or UrllibJsonTransport()
        self.sleep = sleep
        self.require_spend_authorization = require_spend_authorization

    def _request_with_retry(
        self,
        *,
        method: str,
        url: str,
        payload: dict[str, Any] | None,
        idempotency_key: str | None = None,
        timeout_seconds: float | None = None,
    ) -> tuple[dict[str, Any], int]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        for transport_attempt in range(1, self.max_transport_retries + 2):
            timeout = (
                self.http_timeout_seconds
                if timeout_seconds is None else timeout_seconds
            )
            payload_bytes = None
            if payload is not None and logger.isEnabledFor(logging.DEBUG):
                payload_bytes = len(json.dumps(
                    payload, ensure_ascii=False, separators=(",", ":")
                ).encode("utf-8"))
            logger.info(
                "provider_request_start method=%s endpoint=%s attempt=%s timeout_s=%s",
                method, sanitized_endpoint(url), transport_attempt, timeout,
            )
            if payload_bytes is not None:
                logger.debug(
                    "provider_request_payload_summary method=%s bytes=%s idempotency=%s",
                    method, payload_bytes, bool(idempotency_key),
                )
            started = time.monotonic()
            try:
                response = self.transport.request_json(
                    method=method,
                    url=url,
                    headers=headers,
                    payload=payload,
                    timeout_seconds=timeout,
                )
                logger.info(
                    "provider_request_complete method=%s endpoint=%s attempt=%s "
                    "duration_ms=%s provider_status=%s provider_operation_id=%s",
                    method, sanitized_endpoint(url), transport_attempt,
                    round((time.monotonic() - started) * 1000),
                    response.get("status") if isinstance(response, dict) else None,
                    response.get("id") if isinstance(response, dict) else None,
                )
                return response, transport_attempt
            except OpenAIServiceError as exc:
                logger.warning(
                    "provider_request_error method=%s endpoint=%s attempt=%s "
                    "duration_ms=%s http_status=%s request_id=%s retryable=%s "
                    "error_class=%s error=%s",
                    method, sanitized_endpoint(url), transport_attempt,
                    round((time.monotonic() - started) * 1000), exc.status_code,
                    exc.request_id, exc.retryable, type(exc).__name__,
                    sanitize_error_message(exc, secret=self.api_key),
                )
                if (
                    method == "POST"
                    and exc.status_code in {400, 404}
                ):
                    exc.fatal = True
                if method == "POST" and self.require_spend_authorization:
                    raise
                if (
                    not exc.retryable
                    or transport_attempt > self.max_transport_retries
                ):
                    raise
                delay = self.transport_backoff_seconds * (
                    2 ** (transport_attempt - 1)
                )
                logger.info(
                    "provider_request_retry_scheduled method=%s attempt=%s delay_s=%s",
                    method, transport_attempt, delay,
                )
                self.sleep(delay)
        raise AssertionError("unreachable")

    def create_response_only(
        self,
        request_payload: dict[str, Any],
        *,
        idempotency_key: str,
        timeout_seconds: float,
    ) -> tuple[dict[str, Any], int]:
        """Create one background Response without polling or workspace mutation."""
        response, attempts = self._request_with_retry(
            method="POST",
            url=f"{self.base_url}/responses",
            payload=request_payload,
            idempotency_key=idempotency_key,
            timeout_seconds=timeout_seconds,
        )
        response_id = response.get("id")
        if not isinstance(response_id, str) or not response_id:
            raise OpenAIServiceError("OpenAI response has no response ID")
        return response, attempts

    def _prompt(
        self,
        *,
        spec: PassSpec,
        workspace: Path,
        feedback: dict[str, Any] | None,
    ) -> tuple[str, dict[str, str]]:
        system = (
            "You are the author of one bounded AstroWoof authoring pass. "
            "Treat each supplied card or summary as an independent finished "
            "writing assignment while keeping the dog recognizable across "
            "the pass. Read START HERE.md first and follow the workspace's "
            "own guidance as authoritative. Do not borrow wording, templates, "
            "or content from any prior AstroWoof deck. Return only the field "
            "values required by the response schema. Do not include marker "
            "comments in field values."
        )
        retry_section = ""
        if feedback:
            retry_section = (
                "\n\nA prior fresh attempt did not clear local processing. "
                "Use this broad editorial signal, then author the entire pass "
                "again from its source materials:\n"
                + json.dumps(feedback, ensure_ascii=False, indent=2)
            )
        tiers = partition_workspace_prompt(workspace)
        static = (
            "Use the following shared AstroWoof editorial guidance for this "
            "bounded authoring pass. These documents govern every subject "
            "and every pass.\n\nSTATIC GUIDANCE FILES:\n"
            f"{tiers['static']}"
        )
        subject = (
            f"The following full-chart context describes {spec.subject} and "
            "is shared by all six passes for this subject. Use it for coherent "
            "characterization while keeping each assignment bounded to its "
            "own evidence.\n\nSUBJECT CONTEXT FILES:\n"
            f"{tiers['subject']}"
        )
        assignment = (
            f"Author pass {spec.pass_number} of 6 for {spec.subject}. "
            "Complete every marked writing field in every supplied writable "
            "file. Preserve evidence boundaries and follow the requested "
            "voice and astrology-density distinctions. The structured "
            "response is transport only; experience the work as the set of "
            "individual writing assignments described by the files."
            f"{retry_section}\n\n"
            "PASS-SPECIFIC ASSIGNMENT FILES:\n"
            f"{tiers['assignment']}"
        )
        return system, {
            "static_prefix": static,
            "subject_prefix": subject,
            "pass_assignment": assignment,
        }

    def _input_text_block(
        self,
        text: str,
        *,
        breakpoint: bool = False,
    ) -> dict[str, Any]:
        block: dict[str, Any] = {"type": "input_text", "text": text}
        if breakpoint and self.prompt_cache_mode != "disabled":
            block["prompt_cache_breakpoint"] = {"mode": "explicit"}
        return block

    def prompt_layout(
        self,
        *,
        spec: PassSpec,
        workspace: Path,
        feedback: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Describe the current request geometry without making an API call."""
        fields = writable_fields(workspace)
        system, prompt_segments = self._prompt(
            spec=spec,
            workspace=workspace,
            feedback=feedback,
        )
        schema_text = json.dumps(
            authoring_output_schema(fields),
            ensure_ascii=False,
            separators=(",", ":"),
        )
        segments = {
            "system_instructions": text_measurement(system),
            **{
                name: text_measurement(value)
                for name, value in prompt_segments.items()
            },
            "response_schema": text_measurement(schema_text),
        }
        return {
            "pass_id": spec.pass_id,
            "subject": spec.subject,
            "pass_number": spec.pass_number,
            "source_sha256": spec.source_sha256,
            "writable_field_count": len(fields),
            "segments": segments,
            "request_estimated_tokens": sum(
                segment["estimated_tokens"] for segment in segments.values()
            ),
            "note": (
                "Token counts are dependency-free planning estimates, not "
                "Responses API billing measurements."
            ),
        }

    def author(
        self,
        source_workspace: Path,
        response_workspace: Path,
        spec: PassSpec,
        attempt_number: int,
        feedback: dict[str, Any] | None = None,
        before_submit: Any = None,
        provider_created: Any = None,
    ) -> ProviderResult:
        request_payload, prompt_layout, prompt_segments = (
            build_interactive_authoring_request(
                self, spec=spec, workspace=source_workspace,
                feedback=feedback, attempt_number=attempt_number,
            )
        )
        attempt_root = response_workspace.parents[1]
        write_json_atomic(
            attempt_root / "openai-request.json",
            {
                **request_payload,
                "input": [
                    request_payload["input"][0],
                    {
                        "role": "user",
                        "content": (
                            "[workspace prompt persisted separately as "
                            "openai-workspace-prompt.txt]"
                        ),
                    },
                ],
            },
        )
        rendered_prompt = "\n\n".join(prompt_segments.values())
        (attempt_root / "openai-workspace-prompt.txt").write_text(
            rendered_prompt,
            encoding="utf-8",
        )
        idempotency_key = hashlib.sha256(
            (
                f"{spec.source_sha256}:{spec.pass_id}:{attempt_number}:"
                f"{self.model}"
            ).encode("utf-8")
        ).hexdigest()
        started = time.monotonic()
        background_path = attempt_root / "openai-background-response.json"
        if background_path.is_file():
            background_record = load_json(background_path)
            response_id = background_record.get("id")
            if not isinstance(response_id, str) or not response_id:
                raise OpenAIServiceError(
                    f"Invalid persisted background response: {background_path}",
                    fatal=True,
                )
            if provider_created is not None:
                provider_created(response_id, "response")
            response = reconciled_response_evidence(attempt_root, response_id)
            if response is None:
                response, retrieval_attempts = self._request_with_retry(
                    method="GET",
                    url=f"{self.base_url}/responses/{response_id}",
                    payload=None,
                )
            else:
                retrieval_attempts = 0
            create_transport_attempts = 0
            retrieve_transport_attempts = retrieval_attempts
        else:
            if self.require_spend_authorization and before_submit is None:
                raise ValueError("Paid Responses creation requires spend authorization")
            if before_submit is not None:
                before_submit(request_payload)
            response, create_transport_attempts = self._request_with_retry(
                method="POST",
                url=f"{self.base_url}/responses",
                payload=request_payload,
                idempotency_key=idempotency_key,
            )
            response_id = response.get("id")
            if not isinstance(response_id, str) or not response_id:
                raise OpenAIServiceError("OpenAI response has no response ID")
            write_json_atomic(
                background_path,
                {
                    "id": response_id,
                    "status": response.get("status"),
                    "created_at": utc_now(),
                },
            )
            if provider_created is not None:
                provider_created(response_id, "response")
            retrieve_transport_attempts = 0
        response_id = response.get("id")
        if not isinstance(response_id, str) or not response_id:
            raise OpenAIServiceError("OpenAI response has no response ID")
        polls = 0
        while response.get("status") in {"queued", "in_progress"}:
            if time.monotonic() - started > self.response_timeout_seconds:
                pending_metadata = {
                    "provider": self.name,
                    "response_id": response_id,
                    "response_status": response.get("status"),
                    "model": response.get("model") or self.model,
                    "requested_model": self.model,
                    "reasoning_effort": self.reasoning_effort,
                    "background": self.background,
                    "poll_count": polls,
                    "transport_attempts": {
                        "create": create_transport_attempts,
                        "retrieve": retrieve_transport_attempts,
                    },
                    "prompt_layout": prompt_layout,
                    "elapsed_seconds": round(
                        time.monotonic() - started, 3
                    ),
                    "request_path": normalized_path(
                        attempt_root / "openai-request.json"
                    ),
                    "background_response_path": normalized_path(
                        background_path
                    ),
                }
                write_json_atomic(
                    background_path,
                    {
                        "id": response_id,
                        "status": response.get("status"),
                        "last_polled_at": utc_now(),
                    },
                )
                raise BackgroundResponsePending(
                    "Background response is still running after the local "
                    f"polling window: {response_id}",
                    metadata=pending_metadata,
                )
            self.sleep(self.poll_interval_seconds)
            response, retrieval_attempts = self._request_with_retry(
                method="GET",
                url=f"{self.base_url}/responses/{response_id}",
                payload=None,
            )
            polls += 1
            retrieve_transport_attempts += retrieval_attempts
        status = response.get("status")
        write_json_atomic(attempt_root / "openai-response.json", response)
        usage = normalized_usage(response)
        cost = estimated_cost(self.model, usage)
        metadata = {
            "provider": self.name,
            "response_id": response_id,
            "response_status": status,
            "model": response.get("model") or self.model,
            "requested_model": self.model,
            "reasoning_effort": self.reasoning_effort,
            "background": self.background,
            "poll_count": polls,
            "transport_attempts": {
                "create": create_transport_attempts,
                "retrieve": retrieve_transport_attempts,
            },
            "usage": usage,
            "estimated_cost": cost,
            "prompt_layout": prompt_layout,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "request_path": normalized_path(
                attempt_root / "openai-request.json"
            ),
            "response_path": normalized_path(
                attempt_root / "openai-response.json"
            ),
            "authored_fields_path": normalized_path(
                attempt_root / "openai-authored-fields.json"
            ),
        }
        if status != "completed":
            error = response.get("error") or response.get(
                "incomplete_details"
            )
            raise AuthoringProviderError(
                f"OpenAI response {response_id} ended with status "
                f"{status!r}: {error}",
                metadata=metadata,
            )
        try:
            output_text = response_output_text(response)
            authored = json.loads(output_text)
            write_json_atomic(
                attempt_root / "openai-authored-fields.json",
                authored,
            )
            apply_authored_fields(
                source_workspace,
                response_workspace,
                authored,
            )
            require_complete_authored_workspace(
                source_workspace,
                response_workspace,
            )
        except Exception as exc:
            raise AuthoringProviderError(
                f"OpenAI output could not reconstruct the workspace: {exc}",
                metadata=metadata,
                details=getattr(exc, "details", None),
            ) from exc
        return ProviderResult(
            workspace=response_workspace,
            metadata=metadata,
        )

    def complete_json(
        self,
        *,
        system: str,
        user: str,
        schema: dict[str, Any],
        schema_name: str,
        attempt_root: Path,
        idempotency_material: str,
        before_submit: Any = None,
        provider_created: Any = None,
    ) -> tuple[Any, dict[str, Any]]:
        """Run one resumable structured-output response for final polish."""
        payload: dict[str, Any] = {
            "model": self.model,
            "input": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "background": self.background,
            "reasoning": {"effort": self.reasoning_effort},
            "text": {
                "verbosity": "high",
                "format": {
                    "type": "json_schema",
                    "name": schema_name,
                    "strict": True,
                    "schema": schema,
                },
            },
            "max_output_tokens": self.max_output_tokens,
        }
        if self.safety_identifier:
            payload["safety_identifier"] = self.safety_identifier
        attempt_root.mkdir(parents=True, exist_ok=True)
        write_json_atomic(attempt_root / "openai-request.json", payload)
        key = hashlib.sha256(idempotency_material.encode("utf-8")).hexdigest()
        background_path = attempt_root / "openai-background-response.json"
        started = time.monotonic()
        if background_path.is_file():
            response_id = load_json(background_path).get("id")
            if not isinstance(response_id, str) or not response_id:
                raise OpenAIServiceError(
                    f"Invalid persisted background response: {background_path}",
                    fatal=True,
                )
            if provider_created is not None:
                provider_created(response_id, "response")
            response = reconciled_response_evidence(attempt_root, response_id)
            if response is None:
                response, retrieve_attempts = self._request_with_retry(
                    method="GET",
                    url=f"{self.base_url}/responses/{response_id}",
                    payload=None,
                )
            else:
                retrieve_attempts = 0
            create_attempts = 0
        else:
            if self.require_spend_authorization and before_submit is None:
                raise ValueError("Paid Responses creation requires spend authorization")
            if before_submit is not None:
                before_submit(payload)
            response, create_attempts = self._request_with_retry(
                method="POST",
                url=f"{self.base_url}/responses",
                payload=payload,
                idempotency_key=key,
            )
            response_id = response.get("id")
            if not isinstance(response_id, str) or not response_id:
                raise OpenAIServiceError("OpenAI response has no response ID")
            write_json_atomic(
                background_path,
                {"id": response_id, "status": response.get("status")},
            )
            if provider_created is not None:
                provider_created(response_id, "response")
            retrieve_attempts = 0
        response_id = response.get("id")
        polls = 0
        while response.get("status") in {"queued", "in_progress"}:
            if time.monotonic() - started > self.response_timeout_seconds:
                raise OpenAIServiceError(
                    f"Timed out waiting for polish response {response_id}",
                    retryable=True,
                )
            self.sleep(self.poll_interval_seconds)
            response, count = self._request_with_retry(
                method="GET",
                url=f"{self.base_url}/responses/{response_id}",
                payload=None,
            )
            retrieve_attempts += count
            polls += 1
        write_json_atomic(attempt_root / "openai-response.json", response)
        usage = normalized_usage(response)
        metadata = {
            "provider": self.name,
            "response_id": response_id,
            "response_status": response.get("status"),
            "model": response.get("model") or self.model,
            "requested_model": self.model,
            "reasoning_effort": self.reasoning_effort,
            "usage": usage,
            "estimated_cost": estimated_cost(self.model, usage),
            "poll_count": polls,
            "transport_attempts": {
                "create": create_attempts,
                "retrieve": retrieve_attempts,
            },
        }
        if response.get("status") != "completed":
            raise AuthoringProviderError(
                f"Polish response {response_id} did not complete",
                metadata=metadata,
            )
        try:
            result = json.loads(response_output_text(response))
        except Exception as exc:
            raise AuthoringProviderError(
                f"Polish response was not valid JSON: {exc}",
                metadata=metadata,
            ) from exc
        write_json_atomic(attempt_root / "polished-deck.json", result)
        return result, metadata


class RoutedOpenAIProvider:
    """Escalate rejected authoring attempts without repricing clean passes."""

    name = "openai"

    def __init__(
        self,
        *,
        initial: OpenAIResponsesProvider,
        retry: OpenAIResponsesProvider,
        policy: str = "cost_optimized",
    ) -> None:
        self.initial = initial
        self.retry = retry
        self.policy = policy
        self.model = initial.model
        self.reasoning_effort = initial.reasoning_effort
        self.background = initial.background
        self.base_url = initial.base_url
        self.max_output_tokens = initial.max_output_tokens
        self.prompt_cache_mode = initial.prompt_cache_mode
        self.prompt_cache_ttl = initial.prompt_cache_ttl

    def author(
        self,
        source_workspace: Path,
        response_workspace: Path,
        spec: PassSpec,
        attempt_number: int,
        feedback: dict[str, Any] | None = None,
        before_submit: Any = None,
        provider_created: Any = None,
    ) -> ProviderResult:
        route = "initial" if attempt_number == 1 else "creative_retry"
        provider = self.initial if attempt_number == 1 else self.retry
        try:
            result = provider.author(
                source_workspace,
                response_workspace,
                spec,
                attempt_number,
                feedback,
                before_submit,
                provider_created,
            )
        except AuthoringProviderError as exc:
            exc.metadata["routing"] = {
                "policy": self.policy,
                "route": route,
                "model": provider.model,
                "reasoning_effort": provider.reasoning_effort,
            }
            raise
        metadata = {**result.metadata, "routing": {
            "policy": self.policy,
            "route": route,
            "model": provider.model,
            "reasoning_effort": provider.reasoning_effort,
        }}
        return ProviderResult(workspace=result.workspace, metadata=metadata)

    def configuration(self) -> dict[str, Any]:
        return {
            "routing_policy": self.policy,
            "initial": provider_configuration(self.initial),
            "creative_retry": provider_configuration(self.retry),
        }

    def provider_for_attempt(self, attempt_number: int) -> OpenAIResponsesProvider:
        return self.initial if attempt_number == 1 else self.retry


def openai_provider_for_attempt(
    provider: AuthoringProvider,
    attempt_number: int,
) -> OpenAIResponsesProvider:
    if isinstance(provider, RoutedOpenAIProvider):
        return provider.provider_for_attempt(attempt_number)
    if isinstance(provider, OpenAIResponsesProvider):
        return provider
    raise TypeError("Batch service level requires an OpenAI provider")


def build_interactive_authoring_request(
    provider: OpenAIResponsesProvider,
    *,
    spec: PassSpec,
    workspace: Path,
    feedback: dict[str, Any] | None,
    attempt_number: int = 1,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    """Build the exact interactive request without provider I/O or mutation."""
    expected_fields = writable_fields(workspace)
    system, segments = provider._prompt(
        spec=spec, workspace=workspace, feedback=feedback,
    )
    payload: dict[str, Any] = {
        "model": provider.model,
        "input": [
            {"role": "system", "content": [provider._input_text_block(system)]},
            {"role": "user", "content": [
                provider._input_text_block(segments["static_prefix"], breakpoint=True),
                provider._input_text_block(segments["subject_prefix"], breakpoint=True),
                provider._input_text_block(segments["pass_assignment"]),
            ]},
        ],
        "background": provider.background,
        "reasoning": {"effort": provider.reasoning_effort},
        "text": {"verbosity": "high", "format": {
            "type": "json_schema", "name": "astrowoof_authoring_pass",
            "strict": True, "schema": authoring_output_schema(expected_fields),
        }},
        "max_output_tokens": provider.max_output_tokens,
    }
    if provider.prompt_cache_mode != "disabled":
        payload["prompt_cache_options"] = {
            "mode": provider.prompt_cache_mode, "ttl": provider.prompt_cache_ttl,
        }
        subject_hash = hashlib.sha256(
            segments["subject_prefix"].encode("utf-8")
        ).hexdigest()
        payload["prompt_cache_key"] = (
            f"astrowoof:{provider.model}:{subject_hash[:32]}"
        )
    if provider.safety_identifier:
        payload["safety_identifier"] = provider.safety_identifier
    bind_logical_pass_request(
        route_family="exact_natal", route_contract=SCHEMA_VERSION,
        assignment_sha256=spec.source_sha256, pass_id=spec.pass_id,
        pass_number=spec.pass_number, pass_count=PASS_COUNT,
        attempt_number=attempt_number,
        stage=("authoring_initial" if attempt_number == 1 else "creative_retry"),
        resource_identity={"source_sha256": spec.source_sha256},
        prompt=payload["input"], output_schema=payload["text"]["format"]["schema"],
        maximum_output_tokens=provider.max_output_tokens,
    )
    return payload, provider.prompt_layout(
        spec=spec, workspace=workspace, feedback=feedback,
    ), segments


def build_batch_authoring_request(
    provider: OpenAIResponsesProvider,
    *,
    spec: PassSpec,
    workspace: Path,
    feedback: dict[str, Any] | None,
    attempt_number: int = 1,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    """Build the same structured authoring request for Batch transport."""
    expected_fields = writable_fields(workspace)
    system, segments = provider._prompt(
        spec=spec,
        workspace=workspace,
        feedback=feedback,
    )
    payload: dict[str, Any] = {
        "model": provider.model,
        "input": [
            {
                "role": "system",
                "content": [provider._input_text_block(system)],
            },
            {
                "role": "user",
                "content": [
                    provider._input_text_block(segments["static_prefix"]),
                    provider._input_text_block(segments["subject_prefix"]),
                    provider._input_text_block(segments["pass_assignment"]),
                ],
            },
        ],
        "reasoning": {"effort": provider.reasoning_effort},
        "text": {
            "verbosity": "high",
            "format": {
                "type": "json_schema",
                "name": "astrowoof_authoring_pass",
                "strict": True,
                "schema": authoring_output_schema(expected_fields),
            },
        },
        "max_output_tokens": provider.max_output_tokens,
    }
    if provider.safety_identifier:
        payload["safety_identifier"] = provider.safety_identifier
    bind_logical_pass_request(
        route_family="exact_natal",
        route_contract=SCHEMA_VERSION,
        assignment_sha256=spec.source_sha256,
        pass_id=spec.pass_id,
        pass_number=spec.pass_number,
        pass_count=PASS_COUNT,
        attempt_number=attempt_number,
        stage=("authoring_initial" if attempt_number == 1 else "creative_retry"),
        resource_identity={"source_sha256": spec.source_sha256},
        prompt=payload["input"],
        output_schema=payload["text"]["format"]["schema"],
        maximum_output_tokens=provider.max_output_tokens,
    )
    return payload, provider.prompt_layout(
        spec=spec,
        workspace=workspace,
        feedback=feedback,
    ), segments


class OpenAIBatchTransport(Protocol):
    def upload_jsonl(self, content: bytes, filename: str) -> dict[str, Any]: ...
    def create_batch(self, payload: dict[str, Any]) -> dict[str, Any]: ...
    def retrieve_batch(self, batch_id: str) -> dict[str, Any]: ...
    def download_file(self, file_id: str) -> str: ...


class UrllibOpenAIBatchTransport:
    """Dependency-free Files and Batch API transport."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        timeout_seconds: float,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def _open(self, request: urllib.request.Request) -> bytes:
        endpoint = sanitized_endpoint(request.full_url)
        method = request.get_method()
        logger.info(
            "provider_request_start mechanism=batch method=%s endpoint=%s "
            "timeout_s=%s request_bytes=%s",
            method, endpoint, self.timeout_seconds,
            len(request.data) if request.data is not None else 0,
        )
        started = time.monotonic()
        try:
            with urllib.request.urlopen(
                request, timeout=self.timeout_seconds
            ) as response:
                content = response.read()
                logger.info(
                    "provider_request_complete mechanism=batch method=%s endpoint=%s "
                    "http_status=%s request_id=%s duration_ms=%s response_bytes=%s",
                    method, endpoint, getattr(response, "status", None),
                    response.headers.get("x-request-id"),
                    round((time.monotonic() - started) * 1000), len(content),
                )
                return content
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:2000]
            request_id = (
                exc.headers.get("x-request-id") if exc.headers is not None else None
            )
            logger.warning(
                "provider_request_error mechanism=batch method=%s endpoint=%s "
                "http_status=%s request_id=%s duration_ms=%s error_class=%s error=%s",
                method, endpoint, exc.code, request_id,
                round((time.monotonic() - started) * 1000), type(exc).__name__,
                sanitize_error_message(detail or exc, secret=self.api_key),
            )
            raise OpenAIServiceError(
                f"OpenAI HTTP {exc.code}: {detail or exc}",
                status_code=exc.code,
                request_id=request_id,
                retryable=exc.code in RETRYABLE_HTTP_STATUSES,
                fatal=exc.code in {401, 403, 422},
            ) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            logger.warning(
                "provider_request_error mechanism=batch method=%s endpoint=%s "
                "duration_ms=%s error_class=%s error=%s",
                method, endpoint, round((time.monotonic() - started) * 1000),
                type(exc).__name__, sanitize_error_message(exc, secret=self.api_key),
            )
            raise OpenAIServiceError(
                f"OpenAI transport error: {exc}", retryable=True
            ) from exc

    def _json(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=body,
            method=method,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        decoded = json.loads(self._open(request).decode("utf-8"))
        if not isinstance(decoded, dict):
            raise OpenAIServiceError("OpenAI returned a non-object JSON value")
        return decoded

    def upload_jsonl(self, content: bytes, filename: str) -> dict[str, Any]:
        boundary = f"astrowoof-{hashlib.sha256(content).hexdigest()[:24]}"
        parts = [
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"purpose\"\r\n\r\nbatch\r\n".encode(),
            (
                f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
                f"filename=\"{filename}\"\r\nContent-Type: application/jsonl\r\n\r\n"
            ).encode(),
            content,
            f"\r\n--{boundary}--\r\n".encode(),
        ]
        request = urllib.request.Request(
            f"{self.base_url}/files",
            data=b"".join(parts),
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
        )
        return json.loads(self._open(request).decode("utf-8"))

    def create_batch(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._json("POST", "/batches", payload)

    def retrieve_batch(self, batch_id: str) -> dict[str, Any]:
        return self._json("GET", f"/batches/{urllib.parse.quote(batch_id)}")

    def download_file(self, file_id: str) -> str:
        request = urllib.request.Request(
            f"{self.base_url}/files/{urllib.parse.quote(file_id)}/content",
            method="GET",
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        return self._open(request).decode("utf-8")


def parse_attempt_map(values: list[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for value in values:
        try:
            pass_id, attempts_text = value.rsplit(":", 1)
            attempts = int(attempts_text)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(
                f"Expected PASS_ID:COUNT, received {value!r}"
            ) from exc
        if not pass_id or attempts < 0:
            raise argparse.ArgumentTypeError(
                f"Expected PASS_ID:COUNT with COUNT >= 0, received {value!r}"
            )
        result[pass_id] = attempts
    return result


def run_sbe(
    *,
    input_package: Path,
    subject: str | None,
    sbe_script: Path | None,
    python_executable: Path,
    output_dir: Path,
    bundle_dir: Path,
    split_assignment_policy: str = "stratified-v1",
    full_chart_basis_format: str = "legacy",
    exact_natal_policy: str = LEGACY_ATOMIC_POLICY_ID,
) -> dict[str, Any]:
    command = [str(python_executable)]
    if sbe_script is None:
        command.extend(["-m", "astrowoof_natal_authoring.extractor"])
    else:
        command.append(str(sbe_script))
    command.extend([
        "--input-package",
        str(input_package),
        "--output-dir",
        str(output_dir),
        "--bundle-dir",
        str(bundle_dir),
        "--handoff-profile",
        "authoring-workspace",
        "--workspace-layout",
        "split",
        "--workspace-card-limit",
        "50",
        "--split-assignment-policy",
        split_assignment_policy,
        "--full-chart-basis-format",
        full_chart_basis_format,
        "--exact-natal-policy",
        exact_natal_policy,
        "--fail-fast",
    ])
    if subject:
        command.extend(["--subject", subject])
    logger.info(
        "subprocess_start operation=basis_extraction executable=%s argument_count=%s",
        command[0], len(command) - 1,
    )
    started = time.monotonic()
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    logger.info(
        "subprocess_complete operation=basis_extraction returncode=%s duration_ms=%s",
        completed.returncode, round((time.monotonic() - started) * 1000),
    )
    log = {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    write_json_atomic(output_dir.parent / "sbe-invocation.json", log)
    if completed.returncode != 0:
        raise RuntimeError(
            "SBE generation failed; see "
            f"{output_dir.parent / 'sbe-invocation.json'}"
        )
    manifest_path = output_dir / "run-manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"SBE did not emit {manifest_path}")
    manifest = load_json(manifest_path)
    if manifest.get("status") != "pass":
        raise RuntimeError(f"SBE run manifest did not pass: {manifest_path}")
    return manifest


def discover_passes(
    sbe_manifest: dict[str, Any],
    bundle_dir: Path,
) -> list[PassSpec]:
    specs: list[PassSpec] = []
    for subject_record in sbe_manifest.get("subjects", []):
        if subject_record.get("status") != "pass":
            continue
        subject = subject_record["subject"]
        for pass_number in range(1, PASS_COUNT + 1):
            pass_id = f"{subject}_{pass_number}"
            source_zip = bundle_dir / f"{pass_id}.zip"
            if not source_zip.is_file():
                raise FileNotFoundError(
                    f"Missing SBE authoring pass archive: {source_zip}"
                )
            with zipfile.ZipFile(source_zip) as archive:
                bad_member = archive.testzip()
                if bad_member:
                    raise ValueError(
                        f"Corrupt SBE archive {source_zip}: {bad_member}"
                    )
                expected = f"{pass_id}/START HERE.md"
                if expected not in archive.namelist():
                    raise ValueError(
                        f"{source_zip} does not contain {expected}"
                    )
            specs.append(
                PassSpec(
                    pass_id=pass_id,
                    subject=subject,
                    pass_number=pass_number,
                    source_zip=source_zip,
                    source_sha256=sha256_file(source_zip),
                )
            )
    if not specs:
        raise ValueError("SBE manifest contains no passing subjects")
    return specs


def initial_run_state(
    *,
    input_package: Path,
    run_dir: Path,
    provider: AuthoringProvider,
    max_attempts: int,
    sbe_manifest: dict[str, Any],
    specs: list[PassSpec],
    service_level: str = "interactive",
    input_contract: dict[str, Any] | None = None,
    profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    now = utc_now()
    state = {
        "schema_version": SCHEMA_VERSION,
        "state_revision": 0,
        "run_id": hashlib.sha256(
            f"{normalized_path(run_dir)}:{now}".encode("utf-8")
        ).hexdigest(),
        "status": "AUTHORING",
        "created_at": now,
        "updated_at": now,
        "input_package": normalized_path(input_package),
        "input_contract": input_contract,
        "authoring_profile": profile,
        "run_dir": normalized_path(run_dir),
        "workspace_contract": {
            "mode": "stable_logical_absolute_path",
            "logical_root": normalized_path(run_dir),
            "snapshot_schema": SNAPSHOT_SCHEMA,
            "snapshot_manifest": SNAPSHOT_NAME,
        },
        "provider_disclosure": {
            "schema_version": "astrowoof.provider_disclosure.v0.1",
            "subject_fields_allowed": list(PROVIDER_VISIBLE_SUBJECT_FIELDS),
            "subject_fields_protected": list(PROTECTED_SUBJECT_FIELDS),
        },
        "provider": provider.name,
        "service_level": service_level,
        "provider_configuration": provider_configuration(provider),
        "max_attempts": max_attempts,
        "sbe": {
            "status": "pass",
            "subject_count": sbe_manifest.get("subject_count"),
            "manifest": normalized_path(
                run_dir / "sbe" / "semantic-basis-output" / "run-manifest.json"
            ),
        },
        "passes": {
            spec.pass_id: {
                "pass_id": spec.pass_id,
                "subject": spec.subject,
                "pass_number": spec.pass_number,
                "source_zip": normalized_path(spec.source_zip),
                "source_sha256": spec.source_sha256,
                "state": "GENERATED",
                "attempts": [],
                "accepted_workspace": None,
                "accepted_attempt": None,
            }
            for spec in specs
        },
        "subjects": {},
    }
    if provider.name == "openai":
        spend_policy = (profile or {}).get("spend_policy")
        state["spend_ledger"] = new_ledger(validate_policy(spend_policy))
    return state


def prompt_cache_manifest(specs: list[PassSpec]) -> dict[str, Any]:
    """Verify and fingerprint the shared prompt tiers before authoring."""
    pass_records: dict[str, dict[str, str]] = {}
    with tempfile.TemporaryDirectory(prefix="astrowoof-cache-manifest-") as temp:
        root = Path(temp)
        for spec in specs:
            extracted = root / spec.pass_id
            safe_extract_zip(spec.source_zip, extracted)
            workspace = find_workspace_root(extracted, spec.pass_id)
            tiers = partition_workspace_prompt(workspace)
            pass_records[spec.pass_id] = {
                name: hashlib.sha256(value.encode("utf-8")).hexdigest()
                for name, value in tiers.items()
            }
    static_hashes = {item["static"] for item in pass_records.values()}
    if len(static_hashes) != 1:
        raise ValueError("Static authoring guidance differs between passes")
    subjects: dict[str, set[str]] = {}
    for spec in specs:
        subjects.setdefault(spec.subject, set()).add(
            pass_records[spec.pass_id]["subject"]
        )
    inconsistent = {
        subject: sorted(hashes)
        for subject, hashes in subjects.items()
        if len(hashes) != 1
    }
    if inconsistent:
        raise ValueError(
            f"Subject prompt context differs between passes: {inconsistent}"
        )
    return {
        "mode": "tiered_prefix",
        "static_protocol_sha256": next(iter(static_hashes)),
        "subject_context_sha256": {
            subject: next(iter(hashes))
            for subject, hashes in sorted(subjects.items())
        },
        "passes": pass_records,
    }


def provider_configuration(
    provider: AuthoringProvider,
) -> dict[str, Any]:
    configuration = getattr(provider, "configuration", None)
    if callable(configuration):
        return configuration()
    return {
        key: value
        for key, value in {
            "model": getattr(provider, "model", None),
            "reasoning_effort": getattr(provider, "reasoning_effort", None),
            "background": getattr(provider, "background", None),
            "base_url": getattr(provider, "base_url", None),
            "max_output_tokens": getattr(provider, "max_output_tokens", None),
            "prompt_cache_mode": getattr(provider, "prompt_cache_mode", None),
            "prompt_cache_ttl": getattr(provider, "prompt_cache_ttl", None),
            "require_spend_authorization": getattr(
                provider, "require_spend_authorization", None
            ),
        }.items()
        if value is not None
    }


def specs_from_state(state: dict[str, Any]) -> list[PassSpec]:
    return [
        PassSpec(
            pass_id=record["pass_id"],
            subject=record["subject"],
            pass_number=record["pass_number"],
            source_zip=Path(record["source_zip"]),
            source_sha256=record["source_sha256"],
        )
        for record in sorted(
            state["passes"].values(),
            key=lambda item: (item["subject"], item["pass_number"]),
        )
    ]


def update_run_status(state: dict[str, Any]) -> None:
    states = {record["state"] for record in state["passes"].values()}
    spend_states = {
        action.get("state")
        for action in (state.get("spend_ledger") or {}).get("actions", [])
    }
    final_states = {
        record["state"] for record in state.get("subjects", {}).values()
    }
    terminal_transition = state.get("terminal_transition") or {}
    if terminal_transition.get("outcome") == "terminalized":
        state["status"] = terminal_transition["resulting_status"]
    elif final_states and final_states <= FINAL_SUCCESS_STATES:
        # Concrete delivery evidence may close a previously reviewed run. The
        # preservation rule below only blocks weaker pass-derived regressions.
        state["status"] = (
            "DELIVERY_COMPLETE_WITH_WARNINGS"
            if "DELIVERY_COMPLETE_WITH_WARNINGS" in final_states
            else "DELIVERY_COMPLETE"
        )
    elif state.get("status") in {"FINAL_QA_FAILED", "FINAL_QA_REQUIRES_REVIEW"}:
        # Final-deck QA is stronger than pass-derived authoring completeness.
        # Once reached, ordinary persistence must not reopen optional stages.
        pass
    elif "AMBIGUOUS_PROVIDER_SUBMISSION" in spend_states:
        state["status"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
    elif "BUDGET_EXHAUSTED" in spend_states:
        state["status"] = "BUDGET_EXHAUSTED"
    elif "PREPARED" in spend_states:
        state["status"] = "AWAITING_SPEND_AUTHORIZATION"
    elif "FINAL_QA_FAILED" in final_states:
        state["status"] = "FINAL_QA_FAILED"
    elif "FINAL_QA_WARN" in final_states:
        state["status"] = "FINAL_QA_REQUIRES_REVIEW"
    elif states == {"PASS_QA_ACCEPTED"}:
        state["status"] = "AUTHORING_COMPLETE"
    elif "FAILED_REQUIRES_REVIEW" in states:
        state["status"] = "FAILED_REQUIRES_REVIEW"
    elif "WAITING_FOR_RESPONSE" in states:
        state["status"] = "WAITING_FOR_RESPONSE"
    else:
        state["status"] = "AUTHORING"
    usage_totals = {
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "cache_write_tokens": 0,
        "output_tokens": 0,
        "reasoning_tokens": 0,
        "total_tokens": 0,
    }
    estimated_cost_total = 0.0
    priced_attempt_count = 0
    response_ids: list[str] = []
    model_totals: dict[str, dict[str, Any]] = {}
    service_totals: dict[str, dict[str, Any]] = {}
    stage_attempts: dict[str, list[dict[str, Any]]] = {
        "authoring_initial": [],
        "creative_retries": [],
        "polish": [],
        "qualitative_critic": [],
        "qualitative_candidate": [],
    }
    for record in state["passes"].values():
        for index, attempt in enumerate(record.get("attempts", [])):
            stage_attempts[
                "authoring_initial" if index == 0 else "creative_retries"
            ].append(attempt)
    for record in state.get("subjects", {}).values():
        stage_attempts["polish"].extend(record.get("polish_attempts", []))
        review = record.get("qualitative_review") or {}
        critic = review.get("critic") or {}
        candidate = review.get("candidate") or {}
        if critic.get("provider_metadata"):
            stage_attempts["qualitative_critic"].append({
                "provider_metadata": critic["provider_metadata"],
                "accepted": review.get("state") != "QUALITATIVE_REVIEW_ERROR",
            })
        if candidate.get("provider_metadata"):
            stage_attempts["qualitative_candidate"].append({
                "provider_metadata": candidate["provider_metadata"],
                "accepted": review.get("state") == "CANDIDATE_READY_FOR_REVIEW",
            })

    def summarize_attempts(attempts: list[dict[str, Any]]) -> dict[str, Any]:
        nonlocal estimated_cost_total, priced_attempt_count
        stage_usage = {key: 0 for key in usage_totals}
        stage_cost = 0.0
        stage_priced = 0
        stage_responses: list[str] = []
        accepted = 0
        prompt_estimates: list[int] = []
        for attempt in attempts:
            metadata = attempt.get("provider_metadata") or {}
            usage = metadata.get("usage") or {}
            for key in usage_totals:
                usage_totals[key] += int(usage.get(key) or 0)
                stage_usage[key] += int(usage.get(key) or 0)
            cost = (
                metadata.get("estimated_cost")
                or estimated_cost(
                    str(metadata.get("requested_model") or metadata.get("model")),
                    {key: int(usage.get(key) or 0) for key in usage_totals},
                )
                or {}
            )
            if cost.get("estimated_amount") is not None:
                estimated_cost_total += float(cost["estimated_amount"])
                priced_attempt_count += 1
                stage_cost += float(cost["estimated_amount"])
                stage_priced += 1
            model_name = str(
                metadata.get("requested_model")
                or metadata.get("model")
                or "unreported"
            )
            model_record = model_totals.setdefault(
                model_name,
                {
                    "attempt_count": 0,
                    "usage": {key: 0 for key in usage_totals},
                    "estimated_cost_usd": 0.0,
                },
            )
            model_record["attempt_count"] += 1
            for key in usage_totals:
                model_record["usage"][key] += int(usage.get(key) or 0)
            if cost.get("estimated_amount") is not None:
                model_record["estimated_cost_usd"] += float(
                    cost["estimated_amount"]
                )
            service_name = str(metadata.get("service_level") or "interactive")
            service_record = service_totals.setdefault(
                service_name,
                {
                    "attempt_count": 0,
                    "usage": {key: 0 for key in usage_totals},
                    "estimated_cost_usd": 0.0,
                },
            )
            service_record["attempt_count"] += 1
            for key in usage_totals:
                service_record["usage"][key] += int(usage.get(key) or 0)
            if cost.get("estimated_amount") is not None:
                service_record["estimated_cost_usd"] += float(
                    cost["estimated_amount"]
                )
            if metadata.get("response_id"):
                response_ids.append(metadata["response_id"])
                stage_responses.append(metadata["response_id"])
            if (
                attempt.get("accepted")
                or attempt.get("state") == "PASS_QA_ACCEPTED"
                or (attempt.get("qa") or {}).get("accepted") is True
            ):
                accepted += 1
            estimate = (metadata.get("prompt_layout") or {}).get(
                "request_estimated_tokens"
            )
            if estimate is not None:
                prompt_estimates.append(int(estimate))
        input_tokens = stage_usage["input_tokens"]
        cached = stage_usage["cached_input_tokens"]
        return {
            "attempt_count": len(attempts),
            "accepted_attempt_count": accepted,
            "priced_attempt_count": stage_priced,
            "response_ids": stage_responses,
            "usage": stage_usage,
            "cache_hit_ratio": round(cached / input_tokens, 6)
            if input_tokens
            else None,
            "estimated_prompt_tokens": sum(prompt_estimates),
            "estimated_cost": {
                "currency": "USD",
                "estimated_amount": round(stage_cost, 8),
            },
        }

    stage_summaries = {
        name: summarize_attempts(attempts)
        for name, attempts in stage_attempts.items()
    }
    delivered_deck_count = sum(
        1
        for record in state.get("subjects", {}).values()
        if record.get("state") in FINAL_SUCCESS_STATES
    )
    delivered_card_count = delivered_deck_count * 50
    state["accounting"] = {
        "usage": usage_totals,
        "estimated_cost": {
            "currency": "USD",
            "estimated_amount": round(estimated_cost_total, 8),
            "priced_attempt_count": priced_attempt_count,
            "note": (
                "Attempt-level estimates use the configured model rate table; "
                "the OpenAI usage dashboard remains authoritative."
            ),
        },
        "response_ids": response_ids,
        "stages": stage_summaries,
        "models": {
            model: {
                **record,
                "estimated_cost_usd": round(
                    record["estimated_cost_usd"], 8
                ),
            }
            for model, record in sorted(model_totals.items())
        },
        "service_levels": {
            service: {
                **record,
                "estimated_cost_usd": round(
                    record["estimated_cost_usd"], 8
                ),
                "cache_hit_ratio": round(
                    record["usage"]["cached_input_tokens"]
                    / record["usage"]["input_tokens"],
                    6,
                ) if record["usage"]["input_tokens"] else None,
            }
            for service, record in sorted(service_totals.items())
        },
        "cost_per_accepted_card": (
            round(estimated_cost_total / delivered_card_count, 8)
            if delivered_card_count and estimated_cost_total
            else None
        ),
        "cost_per_delivered_deck": (
            round(
                estimated_cost_total
                / delivered_deck_count,
                8,
            )
            if delivered_deck_count
            else None
        ),
    }
    state["updated_at"] = utc_now()


def persist_state(run_json: Path, state: dict[str, Any]) -> None:
    """Persist operator/public/authorization state without attesting workspace."""
    old_revision = int(state.get("state_revision") or 0)
    old_status = state.get("status")
    state["state_revision"] = int(state.get("state_revision") or 0) + 1
    update_run_status(state)
    bind_logging_context(
        run_id=state.get("run_id"), current_state=state.get("status")
    )
    if old_status != state.get("status"):
        logger.info(
            "run_state_transition old_state=%s new_state=%s old_revision=%s "
            "new_revision=%s",
            old_status, state.get("status"), old_revision,
            state.get("state_revision"),
        )
    else:
        logger.debug(
            "run_state_persist state=%s old_revision=%s new_revision=%s",
            state.get("status"), old_revision, state.get("state_revision"),
        )
    refresh_execution_provenance(state)
    write_json_atomic(run_json, state)
    write_json_atomic(run_json.with_name("public-run.json"), public_run_state(state))
    ledger = state.get("spend_ledger") or {}
    write_json_atomic(
        run_json.with_name("spend-authorization-requests.json"),
        {
            "schema_version": "astrowoof.provider_spend_authorization_requests.v0.1",
            "run_id": state.get("run_id"),
            "state_revision": state.get("state_revision"),
            "actions": [
                {
                    "action_id": action["action_id"],
                    "binding": action["binding"],
                }
                for action in ledger.get("actions", [])
                if action.get("state") == "PREPARED"
            ],
        },
    )
    # Project authoritative ledger mutations only after the state is durable and
    # before an enclosing command publishes its workspace snapshot.
    from .native_transitions import sync_provider_transition_journal
    sync_provider_transition_journal(run_json.parent, state)
    logger.debug(
        "run_state_durable state_revision=%s run_path=%s",
        state.get("state_revision"), run_json,
    )


def save_state(run_json: Path, state: dict[str, Any]) -> None:
    """Persist state and publish a coordinator-owned quiescent checkpoint."""
    if threading.current_thread() is not threading.main_thread():
        persist_state(run_json, state)
        return
    persist_state(run_json, state)
    write_workspace_snapshot(run_json.parent)
    logger.info(
        "checkpoint_committed state_revision=%s snapshot=%s",
        state.get("state_revision"), run_json.parent / SNAPSHOT_NAME,
    )


@contextmanager
def checkpoint_spend_boundary(run_json: Path, state: dict[str, Any]):
    """Publish one complete checkpoint after a paid-stage pause unwinds."""
    try:
        yield
    except (AwaitingSpendAuthorization, BudgetExhausted, AmbiguousProviderSubmission) as exc:
        logger.warning(
            "spend_boundary_handoff error_class=%s error=%s state_revision=%s",
            type(exc).__name__, sanitize_error_message(exc),
            state.get("state_revision"),
        )
        save_state(run_json, state)
        from . import __version__
        from .native_transitions import publish_native_execution_result
        publish_native_execution_result(
            run_json.parent, command_kind="ordinary_authoring",
            sbe_release=__version__, published_at=utc_now(),
        )
        raise


def snapshot_inventory(
    run_dir: Path, *, use_process_cache: bool = True
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(item for item in run_dir.rglob("*") if item.is_file()):
        relative = path.relative_to(run_dir).as_posix()
        if (
            relative == SNAPSHOT_NAME
            or relative.startswith("native-publication-receipts/")
            or relative.endswith(".lock")
            or path.name.startswith(".") and path.name.endswith(".tmp")
        ):
            continue
        stat = path.stat()
        cache_key = normalized_path(path)
        cached = _SNAPSHOT_HASH_CACHE.get(cache_key)
        if (
            use_process_cache
            and cached
            and cached[0] == stat.st_size
            and cached[1] == stat.st_mtime_ns
        ):
            checksum = cached[2]
        else:
            checksum = sha256_file(path)
            _SNAPSHOT_HASH_CACHE[cache_key] = (
                stat.st_size,
                stat.st_mtime_ns,
                checksum,
            )
        records.append({
            "path": relative,
            "bytes": stat.st_size,
            "sha256": checksum,
        })
    return records


def write_workspace_snapshot(run_dir: Path) -> None:
    members = snapshot_inventory(run_dir)
    write_json_atomic(
        run_dir / SNAPSHOT_NAME,
        {
            "schema_version": SNAPSHOT_SCHEMA,
            "logical_root": normalized_path(run_dir),
            "members": members,
        },
    )
    logger.debug(
        "workspace_snapshot_written member_count=%s path=%s",
        len(members), run_dir / SNAPSHOT_NAME,
    )


def validate_workspace_snapshot(run_dir: Path, state: dict[str, Any]) -> None:
    contract = state.get("workspace_contract") or {}
    expected_root = contract.get("logical_root")
    actual_root = normalized_path(run_dir)
    if contract.get("mode") != "stable_logical_absolute_path" or not expected_root:
        raise ValueError("Run lacks the durable stable-path workspace contract")
    if expected_root != actual_root:
        raise ValueError(
            "Run workspace must be restored at its original logical absolute "
            f"path: expected {expected_root!r}, got {actual_root!r}"
        )
    manifest_path = run_dir / SNAPSHOT_NAME
    if not manifest_path.is_file():
        raise ValueError(f"Run snapshot is incomplete: missing {manifest_path}")
    manifest = load_json(manifest_path)
    if (
        manifest.get("schema_version") != SNAPSHOT_SCHEMA
        or manifest.get("logical_root") != expected_root
    ):
        raise ValueError("Run snapshot manifest does not match its workspace contract")
    expected = manifest.get("members")
    actual = snapshot_inventory(run_dir, use_process_cache=False)
    if expected != actual:
        logger.error(
            "workspace_snapshot_invalid expected_members=%s actual_members=%s run_dir=%s",
            len(expected) if isinstance(expected, list) else None,
            len(actual), run_dir,
        )
        raise ValueError(
            "Run snapshot is incomplete or changed; restore the complete exact "
            "snapshot before resuming"
        )
    logger.debug(
        "workspace_snapshot_valid member_count=%s run_dir=%s", len(actual), run_dir
    )


def save_state_locked(
    run_json: Path,
    state: dict[str, Any],
    state_lock: threading.Lock,
) -> None:
    with state_lock:
        persist_state(run_json, state)


class SpendController:
    """Prepare and consume exact paid actions under one durable run ledger."""

    def __init__(
        self,
        *,
        state: dict[str, Any],
        run_json: Path,
        state_lock: threading.Lock,
        consumer_id: str,
        event_emitter: ExecutionEventEmitter | None = None,
        reconciliation_only: bool = False,
    ) -> None:
        self.state = state
        self.run_json = run_json
        self.state_lock = state_lock
        self.consumer_id = consumer_id
        self.event_emitter = event_emitter
        self.reconciliation_only = reconciliation_only
        self.local = threading.local()

    @property
    def ledger(self) -> dict[str, Any]:
        ledger = self.state.get("spend_ledger")
        if not isinstance(ledger, dict):
            raise ValueError("OpenAI run has no durable spend ledger")
        return ledger

    @contextmanager
    def _consumption_lock(self):
        """Serialize authorization consumption across local worker processes."""
        path = self.run_json.with_name("spend-consumption.lock")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a+b") as handle:
            handle.seek(0)
            if handle.tell() == 0 and path.stat().st_size == 0:
                handle.write(b"0")
                handle.flush()
            handle.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                handle.seek(0)
                if os.name == "nt":
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def callbacks(
        self,
        *,
        stage: str,
        route: str,
        model: str,
        service_level: str,
        maximum_output_tokens: int,
    ) -> tuple[Any, Any]:
        resumed = next(
            (
                item for item in self.ledger["actions"]
                if item["binding"]["stage"] == stage
                and item["binding"]["route"] == route
                and item["binding"]["model"] == model
                and (
                    item.get("provider")
                    or item.get("state") == "SUBMITTING"
                )
            ),
            None,
        )
        if resumed is not None:
            self.local.active_action = resumed["action_id"]

        def emit(name: str, data: dict[str, Any]) -> None:
            if self.event_emitter is not None:
                action_id = data.get("action_id")
                self.event_emitter.emit(
                    name, data=data,
                    correlation={"action_id": str(action_id)} if action_id else None,
                )

        def before_submit(payload: dict[str, Any]) -> None:
            request_sha256 = spend_digest(payload)
            with self._consumption_lock(), self.state_lock:
                existing = next(
                    (
                        item for item in self.ledger["actions"]
                        if item["binding"]["stage"] == stage
                        and item["binding"]["route"] == route
                        and item["binding"]["request_sha256"] == request_sha256
                        and item["binding"]["model"] == model
                        and item["binding"]["service_level"] == service_level
                        and item["binding"]["maximum_output_tokens"]
                        == maximum_output_tokens
                    ),
                    None,
                )
                if existing is None:
                    input_tokens = estimated_text_tokens(
                        json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
                    )
                    commitment = conservative_commitment_micros(
                        model=model,
                        input_tokens=input_tokens,
                        maximum_output_tokens=maximum_output_tokens,
                        service_level=service_level,
                    )
                    binding = action_binding(
                        run_id=self.state["run_id"],
                        profile_sha256=spend_profile_digest(
                            self.state.get("authoring_profile")
                        ),
                        prepared_state_revision=int(
                            self.state.get("state_revision") or 0
                        ),
                        stage=stage,
                        route=route,
                        request_sha256=request_sha256,
                        model=model,
                        service_level=service_level,
                        maximum_output_tokens=maximum_output_tokens,
                        commitment_micro_usd=commitment,
                        price_book_version=PRICE_BOOK_VERSION,
                    )
                    existing = prepare_action(self.ledger, binding)
                    persist_state(self.run_json, self.state)
                if existing["state"] == "DENIED_PROVIDERLESS":
                    transition = (existing.get("negative_authorization") or {}).get(
                        "run_transition"
                    ) or {}
                    if transition.get("outcome") == "optional_stage_skipped":
                        skipped = deepcopy(existing)
                        skipped["state"] = "SKIPPED_BUDGET_EXHAUSTED"
                        raise BudgetExhausted(
                            "Optional paid stage skipped after providerless denial",
                            action=skipped,
                        )
                    raise AwaitingSpendAuthorization(
                        "Required paid action was denied providerlessly",
                        action=existing,
                    )
                prior_state = existing["state"]
                classify_prepared_budget(self.ledger, existing)
                if existing["state"] != prior_state:
                    update_run_status(self.state)
                    persist_state(self.run_json, self.state)
                if existing["state"] == "PREPARED":
                    emit("authorization.awaiting", {
                        "action_id": existing["action_id"], "stage": stage,
                        "commitment_micro_usd": existing["binding"]["commitment_micro_usd"],
                    })
                    raise AwaitingSpendAuthorization(
                        "Paid action requires external authorization",
                        action=existing,
                    )
                if existing["state"] == "BUDGET_EXHAUSTED":
                    raise BudgetExhausted(
                        "Paid action exhausted its frozen budget", action=existing
                    )
                if existing["state"] == "SKIPPED_BUDGET_EXHAUSTED":
                    raise BudgetExhausted(
                        "Optional paid stage skipped under frozen generation profile",
                        action=existing,
                    )
                if self.reconciliation_only and not existing.get("provider"):
                    raise AwaitingSpendAuthorization(
                        "Bounded reconciliation cannot submit new provider work",
                        action=existing,
                    )
                if existing["state"] in {
                    "SUBMITTING", "AMBIGUOUS_PROVIDER_SUBMISSION",
                    "PROVIDER_ID_RECORDED", "WAITING",
                }:
                    if not existing.get("provider"):
                        mark_ambiguous(
                            existing,
                            reason=(
                                "execution resumed after SUBMITTING without a "
                                "durable provider operation ID"
                            ),
                        )
                        persist_state(self.run_json, self.state)
                    raise AmbiguousProviderSubmission(
                        "Provider submission outcome requires reconciliation",
                        action=existing,
                    )
                persisted_revision = int(
                    load_json(self.run_json).get("state_revision") or 0
                )
                memory_revision = int(self.state.get("state_revision") or 0)
                if persisted_revision != memory_revision:
                    raise RuntimeError(
                        "Paid-action authorization consumption lost the "
                        "single-writer state-revision compare"
                    )
                begin_submission(
                    existing,
                    consumer_id=self.consumer_id,
                    state_revision=int(self.state.get("state_revision") or 0),
                )
                self.local.active_action = existing["action_id"]
                persist_state(self.run_json, self.state)
                emit("authorization.granted", {
                    "action_id": existing["action_id"], "stage": stage,
                    "commitment_micro_usd": existing["binding"]["commitment_micro_usd"],
                })
                emit("provider.submission_started", {
                    "action_id": existing["action_id"], "stage": stage,
                    "attempt": int(route.split(":")[-1]) if route.split(":")[-1].isdigit() else 1,
                })

        def provider_created(provider_id: str | None, kind: str) -> None:
            with self.state_lock:
                action = self.active_action()
                recorded = action.get("provider") or {}
                if recorded:
                    if (
                        recorded.get("id") == str(provider_id or "")
                        and recorded.get("kind") == kind
                    ):
                        return
                    mark_ambiguous(
                        action,
                        reason="persisted provider identity conflicts with local marker",
                    )
                    persist_state(self.run_json, self.state)
                    raise AmbiguousProviderSubmission(
                        "Provider identity conflict requires reconciliation",
                        action=action,
                    )
                record_provider_id(
                    action,
                    provider_id=str(provider_id or ""),
                    kind=kind,
                )
                if service_level in {"interactive", "batch"}:
                    action["provider_reconciliation"] = initial_timing(
                        recorded_at=utc_now().replace("+00:00", "Z"),
                        mechanism=("batch" if service_level == "batch" else "response"),
                    )
                try:
                    persist_state(self.run_json, self.state)
                except Exception as exc:
                    mark_ambiguous(
                        action,
                        reason=(
                            "provider returned an operation ID but durable "
                            f"state persistence failed: {exc}"
                        ),
                    )
                    raise AmbiguousProviderSubmission(
                        "Provider ID could not be durably persisted",
                        action=action,
                    ) from exc
                emit("provider.identity_recorded", {
                    "action_id": action["action_id"],
                    "provider_operation_id": str(provider_id),
                })

        return before_submit, provider_created

    def active_action(self) -> dict[str, Any]:
        action_id = getattr(self.local, "active_action", None)
        if not action_id:
            raise ValueError("No paid action is active in this worker")
        return next(
            item for item in self.ledger["actions"]
            if item["action_id"] == action_id
        )

    def mark_active_ambiguous(self, reason: str) -> None:
        action_id = getattr(self.local, "active_action", None)
        if not action_id:
            return
        with self.state_lock:
            action = self.active_action()
            if action["state"] == "SUBMITTING":
                mark_ambiguous(action, reason=reason)
                persist_state(self.run_json, self.state)

    def mark_active_waiting(self) -> None:
        action_id = getattr(self.local, "active_action", None)
        if not action_id:
            return
        with self.state_lock:
            action = self.active_action()
            if action["state"] == "PROVIDER_ID_RECORDED":
                action["state"] = "WAITING"
            elif action["state"] == "WAITING":
                timing = action.get("provider_reconciliation")
                if not isinstance(timing, dict):
                    raise ValueError(
                        "Interactive provider wait lacks reconciliation timing"
                    )
                record_attempt(
                    timing,
                    attempted_at=utc_now().replace("+00:00", "Z"),
                    outcome="pending",
                )
            else:
                return
            persist_state(self.run_json, self.state)
            if self.event_emitter is not None:
                self.event_emitter.emit("provider.waiting", data={
                    "action_id": action["action_id"],
                    "provider_operation_id": action["provider"]["id"],
                }, correlation={"action_id": action["action_id"]})

    def settle_active(self, metadata: dict[str, Any]) -> None:
        action_id = getattr(self.local, "active_action", None)
        if not action_id:
            return
        estimate = (metadata.get("estimated_cost") or {}).get("estimated_amount")
        estimated_micro_usd = int(
            (Decimal(str(estimate or 0)) * Decimal(1_000_000)).to_integral_value()
        )
        with self.state_lock:
            action = self.active_action()
            if action.get("state") == "WAITING":
                timing = action.get("provider_reconciliation")
                if not isinstance(timing, dict):
                    raise ValueError(
                        "Completed interactive response lacks reconciliation timing"
                    )
                if timing.get("last_outcome") != "completed":
                    record_attempt(
                        timing,
                        attempted_at=utc_now().replace("+00:00", "Z"),
                        outcome="completed",
                    )
            record_reported_cost(
                action,
                usage=metadata.get("usage") or {},
                estimated_micro_usd=estimated_micro_usd,
            )
            persist_state(self.run_json, self.state)
            if self.event_emitter is not None:
                provider = action.get("provider") or {}
                self.event_emitter.emit("provider.completed", data={
                    "action_id": action["action_id"],
                    "provider_operation_id": str(provider.get("id") or ""),
                    "duration_ms": int(metadata.get("duration_ms") or 0),
                }, correlation={"action_id": action["action_id"]})


def prepare_source_workspace(spec: PassSpec, pass_root: Path) -> Path:
    source_root = pass_root / "source"
    if source_root.exists():
        workspace = find_workspace_root(source_root, spec.pass_id)
        return workspace
    safe_extract_zip(spec.source_zip, source_root)
    return find_workspace_root(source_root, spec.pass_id)


_INITIAL_WAVE_NATIVE_KEYS = (
    "schema_version", "wave_id", "wave_sha256", "run_id", "route_family",
    "route_contract", "assignment_sha256", "profile_sha256",
    "preparation_basis_revision", "price_book_version", "member_count",
    "ordered_members", "aggregate_maximum_commitment_micro_usd", "timing",
)


def _initial_lineage_refusal(categories: set[str], message: str) -> InitialWaveError:
    return InitialWaveError(
        "initial_wave_lineage_unjoinable", message,
        evidence_categories=tuple(sorted(categories or {"native_evidence_conflict"})),
    )


def _orphaned_initial_lineage_categories(
    state: dict[str, Any], run_dir: Path,
) -> set[str]:
    """Return closed redacted evidence categories when no stored wave exists."""
    categories: set[str] = set()
    actions = [
        action for action in (state.get("spend_ledger") or {}).get("actions", [])
        if isinstance(action, dict)
        and (action.get("binding") or {}).get("stage") == "authoring_initial"
    ]
    if actions:
        categories.add("prior_initial_action")
    if any((action.get("provider") or {}).get("id") for action in actions):
        categories.add("prior_provider_identity")
    if any(
        action.get("consumption") is not None or action.get("reported") is not None
        for action in actions
    ):
        categories.add("prior_consumption")
    if any(action.get("state") == "AMBIGUOUS_PROVIDER_SUBMISSION" for action in actions):
        categories.add("ambiguous_lineage")
    attempts = [
        attempt
        for record in (state.get("passes") or {}).values()
        if isinstance(record, dict)
        for attempt in record.get("attempts", [])
        if isinstance(attempt, dict)
    ]
    if attempts:
        categories.add("native_evidence_conflict")
    if any(
        attempt.get("provider_metadata") is not None
        or attempt.get("state") in {
            "WAITING_FOR_RESPONSE", "AMBIGUOUS_PROVIDER_SUBMISSION", "COMPLETED",
        }
        for attempt in attempts
    ):
        categories.add("response_evidence")
    if (run_dir / INITIAL_WAVE_BINDING_BUNDLE_FILENAME).exists():
        categories.add("missing_join_artifact")
    attempt_artifacts = [
        path for path in (run_dir / "passes").rglob("*")
        if path.is_file() and any(
            part.startswith("attempt-") for part in path.relative_to(run_dir).parts
        )
    ]
    if attempt_artifacts:
        categories.add("missing_join_artifact")
    if any(
        path.name in {"openai-background-response.json", "openai-response.json"}
        for path in attempt_artifacts
    ):
        categories.add("response_evidence")
    return categories


def _validate_stored_exact_initial_wave(
    state: dict[str, Any], run_dir: Path,
) -> dict[str, Any]:
    """Prove that stored native evidence joins to exactly one reusable wave."""
    stored = state.get("initial_authoring_wave")
    if not isinstance(stored, dict):
        raise _initial_lineage_refusal(
            {"missing_join_artifact"}, "Stored initial wave is absent",
        )
    try:
        wave = {key: stored[key] for key in _INITIAL_WAVE_NATIVE_KEYS}
        validate_initial_wave(wave)
        if wave["route_family"] != "exact_natal":
            raise InitialWaveError("route_mismatch", "Stored wave is not exact Natal")
        bundle_path = run_dir / INITIAL_WAVE_BINDING_BUNDLE_FILENAME
        if not bundle_path.is_file():
            raise InitialWaveError("binding_mismatch", "Binding bundle is absent")
        bundle = load_json(bundle_path)
        validate_initial_wave_binding_bundle_against_wave(bundle, wave)
        members = wave["ordered_members"]
        member_ids = [member["action_id"] for member in members]
        ledger_actions = (state.get("spend_ledger") or {}).get("actions", [])
        requests = stored.get("requests")
        if not isinstance(requests, dict) or set(requests) != set(member_ids):
            raise InitialWaveError("member_inventory_mismatch", "Wave requests do not join")
        for member, bundle_member in zip(
            members, bundle["ordered_members"], strict=True,
        ):
            matches = [
                action for action in ledger_actions
                if isinstance(action, dict) and action.get("action_id") == member["action_id"]
            ]
            if len(matches) != 1 or matches[0].get("binding") != bundle_member["binding"]:
                raise InitialWaveError("binding_mismatch", "Wave ledger does not join")
            request = requests[member["action_id"]]
            payload_path = Path(str(request.get("request_payload_path") or ""))
            if (
                request.get("request_sha256") != member["request_sha256"]
                or not payload_path.is_file()
                or spend_digest(load_json(payload_path)) != member["request_sha256"]
            ):
                raise InitialWaveError("digest_mismatch", "Wave request bytes do not join")
            pass_record = (state.get("passes") or {}).get(member["pass_id"])
            attempts = pass_record.get("attempts", []) if isinstance(pass_record, dict) else []
            if not any(
                isinstance(attempt, dict)
                and attempt.get("paid_action_id") == member["action_id"]
                for attempt in attempts
            ):
                raise InitialWaveError("member_inventory_mismatch", "Wave pass attempt is absent")
        return stored
    except (InitialWaveError, KeyError, TypeError, ValueError) as exc:
        categories = {"native_evidence_conflict"}
        if not (run_dir / INITIAL_WAVE_BINDING_BUNDLE_FILENAME).is_file():
            categories.add("missing_join_artifact")
        actions = (state.get("spend_ledger") or {}).get("actions", [])
        if any((action.get("provider") or {}).get("id") for action in actions):
            categories.add("prior_provider_identity")
        if any(
            action.get("consumption") is not None or action.get("reported") is not None
            for action in actions
        ):
            categories.add("prior_consumption")
        if any(action.get("state") == "AMBIGUOUS_PROVIDER_SUBMISSION" for action in actions):
            categories.add("ambiguous_lineage")
        raise _initial_lineage_refusal(
            categories, "Stored initial-wave evidence cannot prove one exact reusable wave",
        ) from exc


def prepare_exact_interactive_initial_wave(
    *, state: dict[str, Any], provider: AuthoringProvider,
    run_dir: Path, run_json: Path,
) -> dict[str, Any] | None:
    """Prepare all six fresh exact-interactive actions at one state basis."""
    if state.get("initial_authoring_wave"):
        return _validate_stored_exact_initial_wave(state, run_dir)
    orphaned = _orphaned_initial_lineage_categories(state, run_dir)
    if orphaned:
        raise _initial_lineage_refusal(
            orphaned,
            "Historical initial-authoring evidence cannot be joined to one exact wave",
        )
    specs = specs_from_state(state)
    if len(specs) != PASS_COUNT or any(
        state["passes"][spec.pass_id].get("attempts") for spec in specs
    ):
        return None
    routed = openai_provider_for_attempt(provider, 1)
    ledger = state.get("spend_ledger")
    if not isinstance(ledger, dict):
        raise ValueError("OpenAI initial wave requires a durable spend ledger")
    basis_revision = int(state.get("state_revision") or 0)
    profile_sha256 = spend_profile_digest(state.get("authoring_profile"))
    members: list[InitialWaveMemberSpec] = []
    request_index: dict[str, dict[str, Any]] = {}
    for spec in specs:
        pass_root = run_dir / "passes" / spec.pass_id
        source_workspace = prepare_source_workspace(spec, pass_root)
        payload, prompt_layout, segments = build_interactive_authoring_request(
            routed, spec=spec, workspace=source_workspace,
            feedback=None, attempt_number=1,
        )
        request_sha256 = spend_digest(payload)
        commitment = conservative_commitment_micros(
            model=routed.model,
            input_tokens=estimated_text_tokens(json.dumps(
                payload, ensure_ascii=False, separators=(",", ":"),
            )),
            maximum_output_tokens=routed.max_output_tokens,
            service_level="interactive",
        )
        binding = action_binding(
            run_id=state["run_id"], profile_sha256=profile_sha256,
            prepared_state_revision=basis_revision,
            stage="authoring_initial", route=f"{spec.pass_id}:attempt-001",
            request_sha256=request_sha256, model=routed.model,
            service_level="interactive",
            maximum_output_tokens=routed.max_output_tokens,
            commitment_micro_usd=commitment,
        )
        action = prepare_action(ledger, binding)
        if action["state"] != "PREPARED":
            raise BudgetExhausted(
                "Complete initial wave exceeds frozen spend authority", action=action,
            )
        members.append(InitialWaveMemberSpec(
            action_id=action["action_id"], binding=binding,
            pass_id=spec.pass_id, pass_number=spec.pass_number,
        ))
        attempt_root = pass_root / "attempt-001"
        response_workspace = attempt_root / "response" / spec.pass_id
        write_json_atomic(attempt_root / "openai-request.json", {
            **payload, "input": [payload["input"][0], {
                "role": "user", "content": (
                    "[workspace prompt persisted separately as "
                    "openai-workspace-prompt.txt]"
                ),
            }],
        })
        request_payload_path = attempt_root / "openai-request-payload.private.json"
        write_json_atomic(request_payload_path, payload)
        (attempt_root / "openai-workspace-prompt.txt").write_text(
            "\n\n".join(segments.values()), encoding="utf-8",
        )
        attempt = {
            "attempt_number": 1, "state": "AWAITING_SPEND_AUTHORIZATION",
            "started_at": utc_now(), "finished_at": None,
            "response_workspace": normalized_path(response_workspace),
            "provider_metadata": None, "qa": None, "error": None,
            "paid_action_id": action["action_id"],
        }
        record = state["passes"][spec.pass_id]
        record["attempts"].append(attempt)
        record["state"] = "AWAITING_SPEND_AUTHORIZATION"
        request_index[action["action_id"]] = {
            "request_payload_path": normalized_path(request_payload_path),
            "request_sha256": request_sha256,
            "prompt_layout": prompt_layout,
            "attempt_root": normalized_path(attempt_root),
            "pass_id": spec.pass_id,
        }
    assignment_sha256 = spend_digest([
        {"pass_id": spec.pass_id, "source_sha256": spec.source_sha256}
        for spec in specs
    ])
    aggregate_commitment = sum(
        member.binding["commitment_micro_usd"] for member in members
    )
    policy = ledger["policy"]
    if (
        aggregate_commitment > policy["run_ceiling_micro_usd"]
        or aggregate_commitment
        > policy["stage_ceilings_micro_usd"]["authoring_initial"]
    ):
        for member in members:
            action = next(item for item in ledger["actions"]
                          if item["action_id"] == member.action_id)
            action["state"] = "BUDGET_EXHAUSTED"
            record = state["passes"][member.pass_id]
            record["state"] = "BUDGET_EXHAUSTED"
            record["attempts"][-1]["state"] = "BUDGET_EXHAUSTED"
        persist_state(run_json, state)
        raise BudgetExhausted(
            "Complete initial wave exceeds frozen spend ceiling",
            action=next(item for item in ledger["actions"]
                        if item["action_id"] == members[0].action_id),
        )
    wave = build_initial_wave(
        run_id=state["run_id"], route_family="exact_natal",
        route_contract=SCHEMA_VERSION, assignment_sha256=assignment_sha256,
        profile_sha256=profile_sha256,
        preparation_basis_revision=basis_revision, members=members,
    )
    state["initial_authoring_wave"] = {
        **wave, "state": "AWAITING_SPEND_AUTHORIZATION",
        "requests": request_index,
    }
    write_json_atomic(
        run_dir / INITIAL_WAVE_BINDING_BUNDLE_FILENAME,
        build_initial_wave_binding_bundle(
            wave, [member.binding for member in members],
        ),
    )
    persist_state(run_json, state)
    return state["initial_authoring_wave"]


def authorize_exact_interactive_initial_wave(
    *, state: dict[str, Any], run_json: Path,
    envelope: dict[str, Any], member_authorizations: list[dict[str, Any]],
) -> None:
    """Apply the complete external authority set, or mutate nothing."""
    stored = state.get("initial_authoring_wave")
    if not isinstance(stored, dict):
        raise InitialWaveError("wave_missing", "No prepared initial wave exists")
    wave = {key: value for key, value in stored.items() if key not in {"state", "requests"}}
    preflight_wave_authorization(wave, envelope, member_authorizations)
    candidate = deepcopy(state["spend_ledger"])
    for document in member_authorizations:
        authorize_action(candidate, document)
    state["spend_ledger"] = candidate
    stored["state"] = "AUTHORIZED"
    stored["authorization"] = deepcopy(envelope)
    persist_state(run_json, state)


def execute_exact_interactive_initial_wave(
    *, state: dict[str, Any], provider: AuthoringProvider,
    run_json: Path, event_emitter: ExecutionEventEmitter | None = None,
    constrained_intent_token: str | None = None,
    _failure_injector: Any | None = None,
) -> dict[str, Any]:
    """Create six exact Responses concurrently and durably bind each identity."""
    stored = state.get("initial_authoring_wave")
    constrained = constrained_intent_token is not None
    if not isinstance(stored, dict) or stored.get("state") != (
        "SUBMITTING" if constrained else "AUTHORIZED"
    ):
        raise InitialWaveError("authorization_missing", "Initial wave is not authorized")
    if constrained:
        intent = stored.get("constrained_submission_intent") or {}
        if intent.get("token_sha256") != hashlib.sha256(
            constrained_intent_token.encode("utf-8")
        ).hexdigest():
            raise InitialWaveError(
                "provider_submission_ambiguous", "Submission intent capability is absent"
            )
    wave = {key: value for key, value in stored.items() if key not in {
        "state", "requests", "authorization", "result",
        "constrained_submission_intent",
    }}
    documents = [
        next(action["authorization"] for action in state["spend_ledger"]["actions"]
             if action["action_id"] == member["action_id"])
        for member in wave["ordered_members"]
    ]
    routed = openai_provider_for_attempt(provider, 1)
    mutation_lock = threading.Lock()

    def inject(point: str) -> None:
        if _failure_injector is not None:
            _failure_injector(point)

    # All six SUBMITTING decisions become durable before any HTTP POST begins.
    # The barrier action publishes one coherent checkpoint, avoiding six serial
    # workspace scans while preserving the identity-less provider atomicity gap.
    pre_post_barrier = threading.Barrier(
        PASS_COUNT,
        action=lambda: (
            inject("before_pre_post_snapshot"),
            write_workspace_snapshot(run_json.parent),
            inject("after_pre_post_snapshot"),
        ),
        timeout=20.0,
    )

    def action_for(action_id: str) -> dict[str, Any]:
        return next(item for item in state["spend_ledger"]["actions"]
                    if item["action_id"] == action_id)

    def submit(member: dict[str, Any], timeout_seconds: int) -> InitialWaveProviderCreateResult:
        action_id = member["action_id"]
        request = stored["requests"][action_id]
        payload = load_json(Path(request["request_payload_path"]))
        if spend_digest(payload) != member["request_sha256"]:
            raise InitialWaveError(
                "request_digest_mismatch",
                "Prepared initial-wave request changed before submission",
            )
        with mutation_lock:
            action = action_for(action_id)
            recorded = action.get("provider") or {}
            if recorded.get("id"):
                return InitialWaveProviderCreateResult(
                    provider_id=str(recorded["id"]),
                    metadata={"resumed_from_durable_identity": True},
                )
            if action.get("state") == "SUBMITTING" and not constrained:
                raise RuntimeError(
                    "submission resumed without a durable provider identity"
                )
            if action.get("state") not in (
                {"SUBMITTING"} if constrained else {"AUTHORIZED"}
            ):
                raise RuntimeError(
                    f"initial-wave action is not submit-eligible: {action.get('state')}"
                )
            if not constrained:
                begin_submission(
                    action, consumer_id=f"pid:{os.getpid()}",
                    state_revision=int(state.get("state_revision") or 0),
                )
                persist_state(run_json, state)
        inject(f"after_submitting:{action_id}")
        pre_post_barrier.wait()
        inject(f"before_provider_create:{action_id}")
        response, attempts = routed.create_response_only(
            payload,
            idempotency_key=hashlib.sha256((
                f"{member['request_sha256']}:{action_id}"
            ).encode("utf-8")).hexdigest(),
            timeout_seconds=float(timeout_seconds),
        )
        inject(f"after_provider_create_before_identity:{action_id}")
        return InitialWaveProviderCreateResult(
            provider_id=response["id"], metadata={
                "status": response.get("status"),
                "create_transport_attempts": attempts,
            },
        )

    def persist_outcome(member: dict[str, Any], outcome: dict[str, Any]) -> None:
        # Other create workers may still be crossing their pre-submit boundary.
        # Serialize this immediate ID commit with those ledger mutations.
        from .lifecycle import _exclusive_lifecycle_lock
        with _exclusive_lifecycle_lock(run_json.parent), mutation_lock:
            persisted_revision = int(
                load_json(run_json).get("state_revision") or 0
            )
            if persisted_revision != int(state.get("state_revision") or 0):
                raise AmbiguousProviderSubmission(
                    "Initial-wave state changed before provider identity persistence",
                    action=action_for(member["action_id"]),
                )
            action = action_for(member["action_id"])
            request = stored["requests"][member["action_id"]]
            attempt = state["passes"][member["pass_id"]]["attempts"][-1]
            if outcome["outcome"] == "provider_bound":
                provider_id = outcome["provider"]["id"]
                if not action.get("provider"):
                    record_provider_id(action, provider_id=provider_id, kind="response")
                elif action["provider"] != {"kind": "response", "id": provider_id}:
                    raise AmbiguousProviderSubmission(
                        "Initial-wave provider identity conflicts with durable ledger",
                        action=action,
                    )
                if not isinstance(action.get("provider_reconciliation"), dict):
                    action["provider_reconciliation"] = initial_timing(
                        recorded_at=utc_now().replace("+00:00", "Z"),
                        mechanism="response",
                    )
                action["state"] = "WAITING"
                write_json_atomic(Path(request["attempt_root"]) / "openai-background-response.json", {
                    "id": provider_id,
                    "status": (outcome.get("provider_create_metadata") or {}).get("status"),
                    "created_at": utc_now(),
                })
                attempt["state"] = "WAITING_FOR_RESPONSE"
                attempt["provider_metadata"] = outcome.get("provider_create_metadata")
                state["passes"][member["pass_id"]]["state"] = "WAITING_FOR_RESPONSE"
                if event_emitter is not None:
                    event_emitter.emit("provider.identity_recorded", data={
                        "action_id": action["action_id"],
                        "provider_operation_id": provider_id,
                    }, correlation={"action_id": action["action_id"]})
                    event_emitter.emit("provider.waiting", data={
                        "action_id": action["action_id"],
                        "provider_operation_id": provider_id,
                    }, correlation={"action_id": action["action_id"]})
            elif outcome["outcome"] == "ambiguous_submission":
                mark_ambiguous(action, reason=outcome.get("reason") or "create outcome ambiguous")
                attempt["state"] = "AMBIGUOUS_PROVIDER_SUBMISSION"
                state["passes"][member["pass_id"]]["state"] = attempt["state"]
            persist_state(run_json, state)
            # Returned provider identities are not considered recoverably durable
            # until the complete native workspace checkpoint includes them.
            write_workspace_snapshot(run_json.parent)
            inject(f"after_identity_checkpoint:{member['action_id']}")

    result = execute_initial_wave_creates(
        wave, authorization=stored["authorization"],
        member_authorizations=documents, submit=submit,
        persist_member_outcome=persist_outcome,
    )
    stored["state"] = "DETACHED" if result["outcome"] == "detached_provider_pending" else "FAILED"
    stored["result"] = result
    save_state(run_json, state)
    inject("after_final_wave_snapshot")
    return result


def execute_exact_initial_wave_with_external_authority(
    *, run_dir: Path, request: dict[str, Any], grant: dict[str, Any],
    member_authorizations: list[dict[str, Any]], provider: AuthoringProvider,
    event_emitter: ExecutionEventEmitter | None = None,
    _failure_injector: Any | None = None,
) -> dict[str, Any]:
    """Fence one exact initial wave through durable intent before provider I/O."""
    from .external_authority import (
        read_external_authority_request,
        validate_external_authority_grant,
    )
    from .lifecycle import _exclusive_lifecycle_lock

    root = Path(run_dir).resolve()
    run_json = root / "run.json"
    token = os.urandom(32).hex()
    logger.info(
        "external_authority_fence_start request=%s grant=%s",
        request.get("external_authority_request_sha256"), grant.get("grant_sha256"),
    )
    with _exclusive_lifecycle_lock(root):
        state = load_json(run_json)
        validate_workspace_snapshot(root, state)
        try:
            current_request = read_external_authority_request(
                root, observation=request.get("observation"),
            )
        except InitialWaveError as exc:
            if event_emitter is not None:
                event_emitter.emit(
                    "external_authority.refused",
                    data={
                        "reason_code": exc.reason_code,
                        "category": "request_mismatch",
                        "selected_command": "none",
                        "action_count": len(request.get("ordered_action_ids") or []),
                    }, correlation={"native_run_id": request.get("run_id")},
                    severity="warning",
                )
            raise
        if event_emitter is not None:
            event_emitter.emit(
                "external_authority.request_selected",
                data={
                    "request_sha256": current_request[
                        "external_authority_request_sha256"
                    ],
                    "request_kind": current_request["request_kind"],
                    "action_count": current_request["action_count"],
                    "selected_command": "exact_initial_wave_create",
                },
                correlation={"native_run_id": current_request["run_id"]},
            )
        if current_request != request:
            if event_emitter is not None:
                event_emitter.emit(
                    "external_authority.refused",
                    data={
                        "reason_code": "stale_observation",
                        "category": "request_mismatch",
                        "selected_command": "none",
                        "action_count": current_request["action_count"],
                    }, correlation={"native_run_id": current_request["run_id"]},
                    severity="warning",
                )
            raise InitialWaveError(
                "stale_observation", "External-authority request is not current"
            )
        try:
            validate_external_authority_grant(
                current_request, grant, member_authorizations,
            )
        except InitialWaveError as exc:
            if event_emitter is not None:
                event_emitter.emit(
                    "external_authority.refused",
                    data={
                        "reason_code": exc.reason_code,
                        "category": "grant_validation",
                        "selected_command": "none",
                        "action_count": current_request["action_count"],
                    }, correlation={"native_run_id": current_request["run_id"]},
                    severity="warning",
                )
            raise
        if event_emitter is not None:
            event_emitter.emit(
                "external_authority.fence_validated",
                data={
                    "request_sha256": current_request[
                        "external_authority_request_sha256"
                    ],
                    "grant_sha256": grant["grant_sha256"],
                    "action_count": current_request["action_count"],
                }, correlation={"native_run_id": current_request["run_id"]},
            )
        if _failure_injector is not None:
            _failure_injector("after_request_and_grant_validation")
        if current_request["request_kind"] != "initial_wave_admission":
            raise InitialWaveError(
                "unsupported_contract", "This operation requires an initial wave"
            )
        stored = state.get("initial_authoring_wave")
        if not isinstance(stored, dict) or stored.get("state") != (
            "AWAITING_SPEND_AUTHORIZATION"
        ):
            raise InitialWaveError(
                "request_unavailable", "Initial wave is no longer admissible"
            )
        wave = {key: value for key, value in stored.items() if key not in {
            "state", "requests", "authorization", "result",
            "constrained_submission_intent",
        }}
        if wave.get("route_family") != "exact_natal":
            raise InitialWaveError(
                "unsupported_contract", "Bounded constrained execution is deferred"
            )
        legacy_envelope = build_wave_authorization(
            wave, member_authorizations,
            reservation_set_reference=grant["api_decision_id"],
            issuer=grant["issuer"], authorized_at=grant["issued_at"],
        )
        preflight_wave_authorization(
            wave, legacy_envelope, member_authorizations,
        )
        candidate = deepcopy(state["spend_ledger"])
        for document in member_authorizations:
            authorize_action(candidate, document)
        for action_id in current_request["ordered_action_ids"]:
            action = next(
                item for item in candidate["actions"]
                if item["action_id"] == action_id
            )
            begin_submission(
                action, consumer_id=f"external-grant:{grant['api_decision_id']}",
                state_revision=int(state.get("state_revision") or 0),
            )
        state["spend_ledger"] = candidate
        stored["state"] = "SUBMITTING"
        stored["authorization"] = legacy_envelope
        stored["constrained_submission_intent"] = {
            "external_authority_request_sha256": request[
                "external_authority_request_sha256"
            ],
            "grant_sha256": grant["grant_sha256"],
            "ordered_action_ids": list(request["ordered_action_ids"]),
            "token_sha256": hashlib.sha256(token.encode("utf-8")).hexdigest(),
            "created_at": utc_now(),
        }
        if _failure_injector is not None:
            _failure_injector("before_durable_pre_submit_intent")
        save_state(run_json, state)
        if event_emitter is not None:
            event_emitter.emit(
                "external_authority.intent_committed",
                data={
                    "request_sha256": request["external_authority_request_sha256"],
                    "grant_sha256": grant["grant_sha256"],
                    "action_count": len(request["ordered_action_ids"]),
                    "state_revision": state["state_revision"],
                }, correlation={"native_run_id": request["run_id"]},
            )
        logger.info(
            "external_authority_intent_committed request=%s actions=%d revision=%s",
            request["external_authority_request_sha256"],
            len(request["ordered_action_ids"]), state.get("state_revision"),
        )
    if _failure_injector is not None:
        _failure_injector("after_durable_pre_submit_intent")
    logger.info(
        "external_authority_provider_io_start request=%s actions=%d",
        request["external_authority_request_sha256"],
        len(request["ordered_action_ids"]),
    )
    if event_emitter is not None:
        event_emitter.emit(
            "external_authority.provider_create_permitted",
            data={
                "request_sha256": request["external_authority_request_sha256"],
                "action_count": len(request["ordered_action_ids"]),
                "selected_command": "exact_initial_wave_create",
            }, correlation={"native_run_id": request["run_id"]},
        )
    return execute_exact_interactive_initial_wave(
        state=state, provider=provider, run_json=run_json,
        event_emitter=event_emitter, constrained_intent_token=token,
        _failure_injector=_failure_injector,
    )


def run_pass_acceptance(
    workspace: Path,
    report_path: Path,
    *,
    python_executable: Path,
    source_workspace: Path | None = None,
) -> tuple[bool, dict[str, Any]]:
    if source_workspace is not None:
        require_complete_authored_workspace(source_workspace, workspace)
    checker = workspace / "lint_authoring_pass.py"
    if not checker.is_file():
        raise FileNotFoundError(f"Authored workspace lacks checker: {checker}")
    logger.info(
        "subprocess_start operation=pass_acceptance executable=%s workspace=%s",
        python_executable, workspace.name,
    )
    started = time.monotonic()
    completed = subprocess.run(
        [
            str(python_executable),
            str(checker),
            str(workspace),
            "--output",
            str(report_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    logger.info(
        "subprocess_complete operation=pass_acceptance returncode=%s "
        "duration_ms=%s report=%s",
        completed.returncode, round((time.monotonic() - started) * 1000),
        report_path,
    )
    if not report_path.is_file():
        raise RuntimeError(
            f"Acceptance checker emitted no report (exit {completed.returncode}): "
            f"{completed.stderr.strip()}"
        )
    report = load_json(report_path)
    accepted = completed.returncode == 0 and report.get("status") == "accept"
    return accepted, {
        "accepted": accepted,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "report": report,
    }


def author_one_pass(
    *,
    spec: PassSpec,
    record: dict[str, Any],
    provider: AuthoringProvider,
    run_dir: Path,
    max_attempts: int,
    python_executable: Path,
    run_json: Path,
    state: dict[str, Any],
    state_lock: threading.Lock,
    spend_controller: SpendController | None = None,
) -> None:
    logger.info(
        "authoring_pass_start pass_id=%s pass_number=%s existing_state=%s "
        "completed_attempts=%s",
        spec.pass_id, spec.pass_number, record.get("state"),
        len(record.get("attempts") or []),
    )
    if record["state"] == "PASS_QA_ACCEPTED":
        accepted = Path(record["accepted_workspace"])
        if not accepted.is_dir():
            raise FileNotFoundError(
                f"Accepted workspace is missing for {spec.pass_id}: {accepted}"
            )
        return
    if record["state"] == "FAILED_REQUIRES_REVIEW":
        return
    if sha256_file(spec.source_zip) != spec.source_sha256:
        raise ValueError(
            f"Source pass changed since run creation: {spec.source_zip}"
        )

    pass_root = run_dir / "passes" / spec.pass_id
    source_workspace = prepare_source_workspace(spec, pass_root)
    completed_attempts = len(record["attempts"])
    interrupted_attempt = (
        record["attempts"][-1]
        if record["attempts"]
        and record["attempts"][-1]["state"]
        in {
            "SUBMITTED", "RESPONSE_RECEIVED", "WAITING_FOR_RESPONSE",
            "AWAITING_SPEND_AUTHORIZATION",
        }
        and record["attempts"][-1].get("finished_at") is None
        else None
    )
    first_attempt_number = (
        interrupted_attempt["attempt_number"]
        if interrupted_attempt
        else completed_attempts + 1
    )
    for attempt_number in range(first_attempt_number, max_attempts + 1):
        logger.info(
            "authoring_attempt_start pass_id=%s attempt=%s max_attempts=%s",
            spec.pass_id, attempt_number, max_attempts,
        )
        feedback = retry_feedback_from_record(record)
        attempt_root = pass_root / f"attempt-{attempt_number:03d}"
        response_workspace = attempt_root / "response" / spec.pass_id
        if (
            interrupted_attempt
            and interrupted_attempt["attempt_number"] == attempt_number
        ):
            attempt = interrupted_attempt
            interrupted_attempt = None
            feedback = None
            with state_lock:
                attempt["state"] = "SUBMITTED"
                record["state"] = "SUBMITTED"
                save_state(run_json, state)
        else:
            attempt = {
                "attempt_number": attempt_number,
                "state": "SUBMITTED",
                "started_at": utc_now(),
                "finished_at": None,
                "response_workspace": normalized_path(response_workspace),
                "provider_metadata": None,
                "qa": None,
                "error": None,
            }
            with state_lock:
                record["state"] = "SUBMITTED"
                record["attempts"].append(attempt)
                save_state(run_json, state)
        try:
            before_submit = None
            provider_created = None
            if spend_controller is not None:
                routed = openai_provider_for_attempt(provider, attempt_number)
                stage = (
                    "authoring_initial" if attempt_number == 1
                    else "creative_retry"
                )
                before_submit, provider_created = spend_controller.callbacks(
                    stage=stage,
                    route=f"{spec.pass_id}:attempt-{attempt_number:03d}",
                    model=routed.model,
                    service_level="interactive",
                    maximum_output_tokens=routed.max_output_tokens,
                )
            if spend_controller is None:
                result = provider.author(
                    source_workspace,
                    response_workspace,
                    spec,
                    attempt_number,
                    feedback,
                )
            else:
                result = provider.author(
                    source_workspace,
                    response_workspace,
                    spec,
                    attempt_number,
                    feedback,
                    before_submit,
                    provider_created,
                )
            if spend_controller is not None:
                spend_controller.settle_active(result.metadata)
            with state_lock:
                attempt["state"] = "RESPONSE_RECEIVED"
                attempt["provider_metadata"] = result.metadata
                record["state"] = "RESPONSE_RECEIVED"
                save_state(run_json, state)

            metadata_repairs = repair_workspace_context_filters(result.workspace)
            with state_lock:
                attempt["metadata_repairs"] = metadata_repairs
                save_state(run_json, state)
            report_path = attempt_root / "authoring-pass-acceptance.json"
            accepted, qa = run_pass_acceptance(
                result.workspace,
                report_path,
                python_executable=python_executable,
                source_workspace=source_workspace,
            )
            with state_lock:
                attempt["qa"] = qa
                attempt["finished_at"] = utc_now()
            if accepted:
                accepted_root = pass_root / "accepted"
                if accepted_root.exists():
                    shutil.rmtree(accepted_root)
                shutil.copytree(result.workspace, accepted_root)
                with state_lock:
                    attempt["state"] = "PASS_QA_ACCEPTED"
                    record["state"] = "PASS_QA_ACCEPTED"
                    record["accepted_workspace"] = normalized_path(
                        accepted_root
                    )
                    record["accepted_attempt"] = attempt_number
                    save_state(run_json, state)
                logger.info(
                    "authoring_attempt_accepted pass_id=%s attempt=%s",
                    spec.pass_id, attempt_number,
                )
                return
            with state_lock:
                attempt["state"] = "PASS_QA_REJECTED"
                record["state"] = "PASS_QA_REJECTED"
                save_state(run_json, state)
            logger.warning(
                "authoring_attempt_rejected pass_id=%s attempt=%s",
                spec.pass_id, attempt_number,
            )
        except BackgroundResponsePending as exc:
            if spend_controller is not None:
                spend_controller.mark_active_waiting()
            with state_lock:
                attempt["state"] = "WAITING_FOR_RESPONSE"
                attempt["provider_metadata"] = exc.metadata
                attempt["error"] = None
                record["state"] = "WAITING_FOR_RESPONSE"
                save_state(run_json, state)
            logger.info(
                "authoring_attempt_detached pass_id=%s attempt=%s "
                "provider_id=%s",
                spec.pass_id, attempt_number,
                (exc.metadata or {}).get("response_id"),
            )
            return
        except (AwaitingSpendAuthorization, BudgetExhausted) as exc:
            with state_lock:
                attempt["state"] = exc.state
                attempt["paid_action_id"] = (
                    exc.action or {}
                ).get("action_id")
                attempt["error"] = None
                record["state"] = exc.state
                save_state(run_json, state)
            logger.info(
                "authoring_attempt_external_authority_handoff pass_id=%s "
                "attempt=%s outcome=%s action_id=%s",
                spec.pass_id, attempt_number, exc.state,
                (exc.action or {}).get("action_id"),
            )
            return
        except AmbiguousProviderSubmission as exc:
            with state_lock:
                attempt["state"] = exc.state
                attempt["paid_action_id"] = (
                    exc.action or {}
                ).get("action_id")
                record["state"] = exc.state
                save_state(run_json, state)
            logger.error(
                "authoring_attempt_ambiguous pass_id=%s attempt=%s action_id=%s",
                spec.pass_id, attempt_number,
                (exc.action or {}).get("action_id"),
            )
            return
        except Exception as exc:
            logger.exception(
                "authoring_attempt_error pass_id=%s attempt=%s "
                "error_class=%s error=%s",
                spec.pass_id, attempt_number, type(exc).__name__,
                sanitize_error_message(str(exc)),
            )
            if spend_controller is not None:
                spend_controller.mark_active_ambiguous(str(exc))
            with state_lock:
                attempt["state"] = "ATTEMPT_ERROR"
                attempt["finished_at"] = utc_now()
                if getattr(exc, "metadata", None):
                    attempt["provider_metadata"] = exc.metadata
                attempt["error"] = {
                    "type": type(exc).__name__,
                    "message": str(exc),
                }
                if getattr(exc, "details", None):
                    attempt["error"]["details"] = exc.details
                record["state"] = "ATTEMPT_ERROR"
                save_state(run_json, state)
            if getattr(exc, "fatal", False):
                with state_lock:
                    record["state"] = "FAILED_REQUIRES_REVIEW"
                    save_state(run_json, state)
                return

    with state_lock:
        record["state"] = "FAILED_REQUIRES_REVIEW"
        save_state(run_json, state)
    logger.error(
        "authoring_pass_requires_review pass_id=%s attempts=%s",
        spec.pass_id, max_attempts,
    )


def author_pending_passes(
    *,
    state: dict[str, Any],
    provider: AuthoringProvider,
    run_dir: Path,
    max_attempts: int,
    python_executable: Path,
    run_json: Path,
    stop_after_attempts: int | None = None,
    max_workers: int = 1,
    spend_controller: SpendController | None = None,
    only_pass_ids: set[str] | None = None,
) -> None:
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")
    if stop_after_attempts is not None and max_workers != 1:
        raise ValueError(
            "stop_after_attempts is only supported with max_workers=1"
        )
    state_lock = threading.Lock()
    if spend_controller is not None:
        spend_controller.state_lock = state_lock
    attempts_before = sum(
        len(record["attempts"]) for record in state["passes"].values()
    )
    specs = [
        spec
        for spec in specs_from_state(state)
        if state["passes"][spec.pass_id]["state"] not in TERMINAL_STATES
        and (only_pass_ids is None or spec.pass_id in only_pass_ids)
    ]
    logger.info(
        "authoring_wave_start mechanism=response pass_count=%s max_workers=%s "
        "selected_passes=%s",
        len(specs), max_workers, ",".join(spec.pass_id for spec in specs) or "-",
    )

    def run_spec(spec: PassSpec) -> None:
        with logging_context(
            run_id=state.get("native_run_id") or state.get("run_id"),
            current_state=(state.get("machine") or {}).get("state")
            or state.get("status"),
        ):
            record = state["passes"][spec.pass_id]
            author_one_pass(
                spec=spec,
                record=record,
                provider=provider,
                run_dir=run_dir,
                max_attempts=max_attempts,
                python_executable=python_executable,
                run_json=run_json,
                state=state,
                state_lock=state_lock,
                spend_controller=spend_controller,
            )

    cache_warmer: PassSpec | None = None
    if (
        max_workers > 1
        and getattr(provider, "name", None) == "openai"
        and provider.prompt_cache_mode != "disabled"
        and len(specs) > 1
        and not any(
            state["passes"][spec.pass_id].get("attempts") for spec in specs
        )
    ):
        cache_warmer = select_cache_warmer(specs)
        warming = {
            "pass_id": cache_warmer.pass_id,
            "selection": "smallest_source_archive",
            "state": "RUNNING",
            "started_at": utc_now(),
            "finished_at": None,
        }
        state.setdefault("prompt_cache", {})["warming"] = warming
        save_state_locked(run_json, state, state_lock)
        run_spec(cache_warmer)
        warming["state"] = state["passes"][cache_warmer.pass_id]["state"]
        warming["finished_at"] = utc_now()
        save_state_locked(run_json, state, state_lock)
        if warming["state"] == "WAITING_FOR_RESPONSE":
            save_state(run_json, state)
            return
        specs = [spec for spec in specs if spec != cache_warmer]

    if max_workers == 1:
        for spec in specs:
            run_spec(spec)
            attempts_after = sum(
                len(item["attempts"]) for item in state["passes"].values()
            )
            if (
                stop_after_attempts is not None
                and attempts_after - attempts_before >= stop_after_attempts
            ):
                break
    else:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(max_workers, len(specs) or 1),
            thread_name_prefix="astrowoof-author",
        ) as executor:
            futures = {
                executor.submit(run_spec, spec): spec
                for spec in specs
            }
            for future in concurrent.futures.as_completed(futures):
                future.result()
    save_state(run_json, state)
    logger.info(
        "authoring_wave_complete mechanism=response pass_count=%s",
        len(specs) + (1 if cache_warmer is not None else 0),
    )


def _batch_jsonl_records(text: str) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        custom_id = value.get("custom_id")
        if not isinstance(custom_id, str) or not custom_id:
            raise ValueError(f"Batch output line {line_number} has no custom_id")
        if custom_id in records:
            raise ValueError(f"Batch output repeats custom_id {custom_id!r}")
        records[custom_id] = value
    return records


def author_pending_passes_batch(
    *,
    state: dict[str, Any],
    provider: AuthoringProvider,
    transport: OpenAIBatchTransport,
    run_dir: Path,
    max_attempts: int,
    python_executable: Path,
    run_json: Path,
    poll_interval_seconds: float = 30.0,
    detach: bool = False,
    sleep: Any = time.sleep,
    spend_controller: SpendController | None = None,
    reconciliation_only: bool = False,
) -> bool:
    """Author pending passes in model-homogeneous, resumable Batch rounds."""
    service = state.setdefault(
        "batch_service",
        {"service_level": "batch", "rounds": []},
    )
    terminal_batch_states = {"completed", "failed", "expired", "cancelled"}
    logger.info(
        "authoring_batch_cycle_start existing_rounds=%s detach=%s "
        "reconciliation_only=%s",
        len(service["rounds"]), detach, reconciliation_only,
    )

    while True:
        pending = [
            spec for spec in specs_from_state(state)
            if state["passes"][spec.pass_id]["state"] not in TERMINAL_STATES
        ]
        if not pending:
            save_state(run_json, state)
            return True

        resumable = next(
            (
                item for item in service["rounds"]
                if item.get("state") not in {"INGESTED", "FAILED"}
            ),
            None,
        )
        if resumable is None:
            candidates: list[tuple[PassSpec, dict[str, Any], int]] = []
            for spec in pending:
                record = state["passes"][spec.pass_id]
                attempt_number = len(record["attempts"]) + 1
                if attempt_number <= max_attempts:
                    candidates.append((spec, record, attempt_number))
                else:
                    record["state"] = "FAILED_REQUIRES_REVIEW"
            if not candidates:
                save_state(run_json, state)
                return True
            first_provider = openai_provider_for_attempt(
                provider, candidates[0][2]
            )
            candidates = [
                item for item in candidates
                if openai_provider_for_attempt(provider, item[2]).model
                == first_provider.model
                and (item[2] == 1) == (candidates[0][2] == 1)
            ]
            round_number = len(service["rounds"]) + 1
            round_root = run_dir / "batches" / f"round-{round_number:03d}"
            round_root.mkdir(parents=True, exist_ok=True)
            lines: list[str] = []
            requests: list[dict[str, Any]] = []
            for spec, record, attempt_number in candidates:
                pass_root = run_dir / "passes" / spec.pass_id
                source_workspace = prepare_source_workspace(spec, pass_root)
                attempt_root = pass_root / f"attempt-{attempt_number:03d}"
                response_workspace = attempt_root / "response" / spec.pass_id
                routed = openai_provider_for_attempt(provider, attempt_number)
                payload, layout, segments = build_batch_authoring_request(
                    routed,
                    spec=spec,
                    workspace=source_workspace,
                    feedback=retry_feedback_from_record(record),
                    attempt_number=attempt_number,
                )
                custom_id = f"{spec.pass_id}:attempt-{attempt_number:03d}"
                line = {
                    "custom_id": custom_id,
                    "method": "POST",
                    "url": "/v1/responses",
                    "body": payload,
                }
                lines.append(json.dumps(line, ensure_ascii=False))
                attempt = {
                    "attempt_number": attempt_number,
                    "state": "BATCH_SUBMITTED",
                    "started_at": utc_now(),
                    "finished_at": None,
                    "response_workspace": normalized_path(response_workspace),
                    "provider_metadata": None,
                    "qa": None,
                    "error": None,
                }
                record["attempts"].append(attempt)
                record["state"] = "BATCH_SUBMITTED"
                requests.append({
                    "custom_id": custom_id,
                    "pass_id": spec.pass_id,
                    "attempt_number": attempt_number,
                    "model": routed.model,
                    "reasoning_effort": routed.reasoning_effort,
                    "prompt_layout": layout,
                    "prompt_sha256": hashlib.sha256(
                        "\n\n".join(segments.values()).encode("utf-8")
                    ).hexdigest(),
                })
            input_text = "\n".join(lines) + "\n"
            input_path = round_root / "batch-input.jsonl"
            input_path.write_text(input_text, encoding="utf-8")
            resumable = {
                "round_number": round_number,
                "state": "PREPARED",
                "model": first_provider.model,
                "created_at": utc_now(),
                "input_path": normalized_path(input_path),
                "requests": requests,
                "input_file_id": None,
                "batch_id": None,
                "batch_status": None,
            }
            service["rounds"].append(resumable)
            save_state(run_json, state)
            logger.info(
                "batch_round_prepared round=%s member_count=%s model=%s",
                round_number, len(requests), first_provider.model,
            )
            uploaded = transport.upload_jsonl(
                input_text.encode("utf-8"), input_path.name
            )
            resumable["input_file_id"] = uploaded["id"]
            resumable["state"] = "UPLOADED"
            save_state(run_json, state)
            logger.info(
                "batch_input_uploaded round=%s input_file_id=%s",
                round_number, uploaded.get("id"),
            )
            batch_payload = {
                "input_file_id": uploaded["id"],
                "endpoint": "/v1/responses",
                "completion_window": "24h",
                "metadata": {
                    "workflow": "astrowoof_semantic_closure",
                    "round": str(round_number),
                },
            }
            batch_before = batch_created = None
            if spend_controller is not None:
                batch_before, batch_created = spend_controller.callbacks(
                    stage=(
                        "authoring_initial"
                        if candidates[0][2] == 1
                        else "creative_retry"
                    ),
                    route=f"batch-round-{round_number:03d}",
                    model=first_provider.model,
                    service_level="batch",
                    maximum_output_tokens=(
                        first_provider.max_output_tokens * len(requests)
                    ),
                )
                batch_before({
                    "batch": batch_payload,
                    "input_sha256": hashlib.sha256(
                        input_path.read_bytes()
                    ).hexdigest(),
                })
            batch = transport.create_batch(batch_payload)
            if batch_created is not None:
                batch_created(batch.get("id"), "batch")
            resumable["batch_id"] = batch["id"]
            resumable["batch_status"] = batch.get("status")
            resumable["state"] = "SUBMITTED"
            save_state(run_json, state)
            logger.info(
                "batch_round_submitted round=%s batch_id=%s status=%s "
                "member_count=%s",
                round_number, batch.get("id"), batch.get("status"),
                len(requests),
            )
        else:
            input_path = Path(resumable["input_path"])
            resume_attempts = [
                int(request["attempt_number"])
                for request in resumable["requests"]
            ]
            resume_provider = openai_provider_for_attempt(
                provider, resume_attempts[0]
            )
            if spend_controller is not None:
                spend_controller.callbacks(
                    stage=(
                        "authoring_initial"
                        if resume_attempts[0] == 1
                        else "creative_retry"
                    ),
                    route=f"batch-round-{resumable['round_number']:03d}",
                    model=resumable["model"],
                    service_level="batch",
                    maximum_output_tokens=(
                        resume_provider.max_output_tokens
                        * len(resumable["requests"])
                    ),
                )
            if resumable["state"] == "PREPARED":
                uploaded = transport.upload_jsonl(
                    input_path.read_bytes(), input_path.name
                )
                resumable["input_file_id"] = uploaded["id"]
                resumable["state"] = "UPLOADED"
                save_state(run_json, state)
            if resumable["state"] == "UPLOADED":
                batch_payload = {
                    "input_file_id": resumable["input_file_id"],
                    "endpoint": "/v1/responses",
                    "completion_window": "24h",
                    "metadata": {
                        "workflow": "astrowoof_semantic_closure",
                        "round": str(resumable["round_number"]),
                    },
                }
                batch_before = batch_created = None
                if spend_controller is not None:
                    batch_before, batch_created = spend_controller.callbacks(
                        stage=(
                            "authoring_initial"
                            if resume_attempts[0] == 1
                            else "creative_retry"
                        ),
                        route=f"batch-round-{resumable['round_number']:03d}",
                        model=resumable["model"],
                        service_level="batch",
                        maximum_output_tokens=(
                            resume_provider.max_output_tokens
                            * len(resumable["requests"])
                        ),
                    )
                    batch_before({
                        "batch": batch_payload,
                        "input_sha256": hashlib.sha256(
                            input_path.read_bytes()
                        ).hexdigest(),
                    })
                batch = transport.create_batch(batch_payload)
                if batch_created is not None:
                    batch_created(batch.get("id"), "batch")
                resumable["batch_id"] = batch["id"]
                resumable["batch_status"] = batch.get("status")
                resumable["state"] = "SUBMITTED"
                save_state(run_json, state)
            else:
                batch = transport.retrieve_batch(resumable["batch_id"])

        if detach and batch.get("status") not in terminal_batch_states:
            resumable["batch_status"] = batch.get("status")
            save_state(run_json, state)
            logger.info(
                "batch_round_detached round=%s batch_id=%s status=%s",
                resumable["round_number"], resumable.get("batch_id"),
                batch.get("status"),
            )
            return False
        while batch.get("status") not in terminal_batch_states:
            sleep(poll_interval_seconds)
            batch = transport.retrieve_batch(resumable["batch_id"])
            resumable["batch_status"] = batch.get("status")
            resumable["request_counts"] = batch.get("request_counts")
            save_state(run_json, state)
            logger.info(
                "batch_round_pending round=%s batch_id=%s status=%s "
                "request_counts=%s",
                resumable["round_number"], resumable.get("batch_id"),
                batch.get("status"), batch.get("request_counts"),
            )
        resumable["batch_status"] = batch.get("status")
        write_json_atomic(
            Path(resumable["input_path"]).parent / "batch-object.json", batch
        )
        if batch.get("status") != "completed":
            logger.error(
                "batch_round_terminal_failure round=%s batch_id=%s status=%s",
                resumable["round_number"], resumable.get("batch_id"),
                batch.get("status"),
            )
            resumable["state"] = "FAILED"
            resumable["finished_at"] = utc_now()
            for request in resumable["requests"]:
                record = state["passes"][request["pass_id"]]
                attempt = record["attempts"][request["attempt_number"] - 1]
                attempt["state"] = "ATTEMPT_ERROR"
                attempt["finished_at"] = utc_now()
                attempt["error"] = {
                    "type": "OpenAIBatchError",
                    "message": f"Batch ended with status {batch.get('status')}",
                }
                record["state"] = "ATTEMPT_ERROR"
            save_state(run_json, state)
            continue

        output_path = Path(resumable["input_path"]).parent / "batch-output.jsonl"
        output_text = (
            transport.download_file(batch["output_file_id"])
            if batch.get("output_file_id")
            else ""
        )
        output_path.write_text(output_text, encoding="utf-8")
        outputs = _batch_jsonl_records(output_text)
        error_outputs: dict[str, dict[str, Any]] = {}
        if batch.get("error_file_id"):
            error_text = transport.download_file(batch["error_file_id"])
            (output_path.parent / "batch-errors.jsonl").write_text(
                error_text, encoding="utf-8"
            )
            error_outputs = _batch_jsonl_records(error_text)

        for request in resumable["requests"]:
            spec = next(
                item for item in specs_from_state(state)
                if item.pass_id == request["pass_id"]
            )
            record = state["passes"][spec.pass_id]
            attempt = record["attempts"][request["attempt_number"] - 1]
            item = outputs.get(request["custom_id"])
            if item is None:
                error_item = error_outputs.get(request["custom_id"])
                attempt["state"] = "ATTEMPT_ERROR"
                attempt["finished_at"] = utc_now()
                attempt["error"] = {
                    "type": "OpenAIBatchRequestError",
                    "message": json.dumps(error_item or "missing batch output"),
                }
                record["state"] = "ATTEMPT_ERROR"
                continue
            envelope = item.get("response") or {}
            response = envelope.get("body") or {}
            attempt_root = (
                run_dir / "passes" / spec.pass_id
                / f"attempt-{request['attempt_number']:03d}"
            )
            write_json_atomic(attempt_root / "openai-response.json", response)
            usage = normalized_usage(response)
            metadata = {
                "provider": "openai",
                "service_level": "batch",
                "batch_id": resumable["batch_id"],
                "custom_id": request["custom_id"],
                "response_id": response.get("id"),
                "response_status": response.get("status"),
                "model": response.get("model") or request["model"],
                "requested_model": request["model"],
                "reasoning_effort": request["reasoning_effort"],
                "usage": usage,
                "provider_usage_reported": isinstance(response.get("usage"), dict),
                "estimated_cost": batch_estimated_cost(request["model"], usage),
                "prompt_layout": request["prompt_layout"],
            }
            if isinstance(provider, RoutedOpenAIProvider):
                metadata["routing"] = {
                    "policy": provider.policy,
                    "route": (
                        "initial"
                        if request["attempt_number"] == 1
                        else "creative_retry"
                    ),
                    "model": request["model"],
                    "reasoning_effort": request["reasoning_effort"],
                }
            attempt["provider_metadata"] = metadata
            response_workspace = Path(attempt["response_workspace"])
            try:
                authored = json.loads(response_output_text(response))
                write_json_atomic(
                    attempt_root / "openai-authored-fields.json", authored
                )
                source_workspace = prepare_source_workspace(
                    spec, run_dir / "passes" / spec.pass_id
                )
                apply_authored_fields(
                    source_workspace, response_workspace, authored
                )
                require_complete_authored_workspace(
                    source_workspace, response_workspace
                )
                attempt["metadata_repairs"] = repair_workspace_context_filters(
                    response_workspace
                )
                accepted, qa = run_pass_acceptance(
                    response_workspace,
                    attempt_root / "authoring-pass-acceptance.json",
                    python_executable=python_executable,
                    source_workspace=source_workspace,
                )
                attempt["qa"] = qa
                attempt["finished_at"] = utc_now()
                if accepted:
                    accepted_root = run_dir / "passes" / spec.pass_id / "accepted"
                    if accepted_root.exists():
                        shutil.rmtree(accepted_root)
                    shutil.copytree(response_workspace, accepted_root)
                    attempt["state"] = "PASS_QA_ACCEPTED"
                    record["state"] = "PASS_QA_ACCEPTED"
                    record["accepted_workspace"] = normalized_path(accepted_root)
                    record["accepted_attempt"] = request["attempt_number"]
                else:
                    attempt["state"] = "PASS_QA_REJECTED"
                    record["state"] = "PASS_QA_REJECTED"
            except Exception as exc:
                logger.exception(
                    "batch_member_ingest_error round=%s custom_id=%s "
                    "error_class=%s error=%s",
                    resumable["round_number"], request["custom_id"],
                    type(exc).__name__, sanitize_error_message(str(exc)),
                )
                attempt["state"] = "ATTEMPT_ERROR"
                attempt["finished_at"] = utc_now()
                attempt["error"] = {
                    "type": type(exc).__name__, "message": str(exc)
                }
                if getattr(exc, "details", None):
                    attempt["error"]["details"] = exc.details
                record["state"] = "ATTEMPT_ERROR"
        resumable["state"] = "INGESTED"
        resumable["finished_at"] = utc_now()
        if spend_controller is not None:
            usage_complete = all(
                bool((
                    state["passes"][request["pass_id"]]["attempts"]
                    [request["attempt_number"] - 1].get("provider_metadata") or {}
                ).get("provider_usage_reported"))
                for request in resumable["requests"]
            )
            aggregate_usage = {
                key: sum(
                    int(
                        (
                            state["passes"][request["pass_id"]]["attempts"]
                            [request["attempt_number"] - 1]
                            .get("provider_metadata") or {}
                        ).get("usage", {}).get(key) or 0
                    )
                    for request in resumable["requests"]
                )
                for key in (
                    "input_tokens", "cached_input_tokens", "cache_write_tokens",
                    "output_tokens", "reasoning_tokens", "total_tokens",
                )
            }
            aggregate_cost = sum(
                float(
                    (
                        (
                            state["passes"][request["pass_id"]]["attempts"]
                            [request["attempt_number"] - 1]
                            .get("provider_metadata") or {}
                        ).get("estimated_cost") or {}
                    ).get("estimated_amount") or 0
                )
                for request in resumable["requests"]
            )
            if usage_complete:
                resumable["cost_disposition"] = "provider_usage_reported"
                spend_controller.settle_active({
                    "usage": aggregate_usage,
                    "estimated_cost": {"estimated_amount": aggregate_cost},
                })
            else:
                resumable["cost_disposition"] = (
                    "provider_usage_unavailable_billing_reconciliation_pending"
                )
                action = spend_controller.active_action()
                action["reported"] = {
                    "usage": None, "estimated_micro_usd": None,
                    "cost_disposition": resumable["cost_disposition"],
                }
                action["state"] = "REPORTED"
        save_state(run_json, state)
        logger.info(
            "batch_round_ingested round=%s batch_id=%s member_count=%s "
            "cost_disposition=%s",
            resumable["round_number"], resumable.get("batch_id"),
            len(resumable["requests"]), resumable.get("cost_disposition", "-"),
        )
        if reconciliation_only:
            return False


def select_cache_warmer(specs: list[PassSpec]) -> PassSpec:
    if not specs:
        raise ValueError("Cannot select a cache warmer from no passes")
    return min(
        specs,
        key=lambda item: (item.source_zip.stat().st_size, item.pass_number),
    )


def run_json_command(
    command: list[str],
    report_path: Path,
    *,
    accepted_returncodes: set[int],
) -> dict[str, Any]:
    """Run a repository QA command and require its JSON report."""
    logger.info(
        "subprocess_start operation=qa_json_command executable=%s "
        "argument_count=%s report=%s",
        command[0], len(command) - 1, report_path,
    )
    started = time.monotonic()
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    logger.info(
        "subprocess_complete operation=qa_json_command returncode=%s "
        "duration_ms=%s report=%s",
        completed.returncode, round((time.monotonic() - started) * 1000),
        report_path,
    )
    if not report_path.is_file():
        raise RuntimeError(
            f"QA command emitted no report (exit {completed.returncode}): "
            f"{completed.stderr.strip()}"
        )
    report = load_json(report_path)
    return {
        "accepted": completed.returncode in accepted_returncodes,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "report": report,
    }


def subject_records(state: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for record in state["passes"].values():
        grouped.setdefault(record["subject"], []).append(record)
    for records in grouped.values():
        records.sort(key=lambda item: item["pass_number"])
    return grouped


def assemble_subject(
    *,
    state: dict[str, Any],
    subject: str,
    run_dir: Path,
    python_executable: Path,
) -> dict[str, Any]:
    logger.info("subject_assembly_start subject=%s", subject)
    """Assemble six accepted passes and run final deterministic QA."""
    records = subject_records(state)[subject]
    if len(records) != PASS_COUNT or any(
        record["state"] != "PASS_QA_ACCEPTED" for record in records
    ):
        raise ValueError(
            f"{subject} cannot be assembled until all six passes are accepted"
        )
    final_root = run_dir / "final" / subject
    workspace_root = final_root / "accepted-passes"
    if workspace_root.exists():
        shutil.rmtree(workspace_root)
    workspace_root.mkdir(parents=True)
    for record in records:
        source = Path(record["accepted_workspace"])
        if not source.is_dir():
            raise FileNotFoundError(
                f"Accepted workspace is missing for {record['pass_id']}: {source}"
            )
        shutil.copytree(source, workspace_root / record["pass_id"])

    packet_path = (
        run_dir
        / "sbe"
        / "semantic-basis-output"
        / subject
        / f"{subject}.selected-authoring-packet.json"
    )
    packet = load_json(packet_path)
    deck, assembly_report = assemble(
        packet,
        workspace_root,
        allow_partial=False,
    )
    filter_repairs = sanitize_context_filters(deck)
    assembly_report["deterministic_context_filter_repairs"] = filter_repairs
    deck_path = final_root / f"natal.{subject}.cards.json"
    assembly_path = final_root / f"natal.{subject}.assembly-report.json"
    write_json_atomic(deck_path, deck)
    write_json_atomic(assembly_path, assembly_report)

    validator_path = Path(validation_module.__file__).resolve()
    validation_path = final_root / f"natal.{subject}.validation-report.json"
    validation = run_json_command(
        [
            str(python_executable),
            str(validator_path),
            str(packet_path),
            str(deck_path),
            "--report",
            str(validation_path),
        ],
        validation_path,
        accepted_returncodes={0},
    )
    linter_path = Path(editorial_lint_module.__file__).resolve()
    lint_path = final_root / f"natal.{subject}.lint-report.json"
    lint = run_json_command(
        [
            str(python_executable),
            str(linter_path),
            str(deck_path),
            "--output",
            str(lint_path),
        ],
        lint_path,
        accepted_returncodes={0, 2},
    )
    ordinary_lint_warning_count = int(
        lint["report"].get("warning_count") or 0
    )
    lint_warning_count = lint_finding_count(lint["report"])
    authoring_rejection_count = (
        lint_warning_count - ordinary_lint_warning_count
    )
    validation_warning_count = len(
        validation["report"].get("warnings") or []
    )
    warning_count = lint_warning_count
    status = (
        "FINAL_QA_PASSED"
        if validation["accepted"] and warning_count == 0
        else "FINAL_QA_WARN"
        if validation["accepted"]
        else "FINAL_QA_FAILED"
    )
    result = {
        "subject": subject,
        "state": status,
        "packet": normalized_path(packet_path),
        "deck": normalized_path(deck_path),
        "assembly_report": normalized_path(assembly_path),
        "validation_report": normalized_path(validation_path),
        "lint_report": normalized_path(lint_path),
        "validation": validation,
        "lint": lint,
        "baseline_warning_count": warning_count,
        "baseline_warning_components": {
            "validation": validation_warning_count,
            "lint": ordinary_lint_warning_count,
            "authoring_rejections": authoring_rejection_count,
        },
        "polish_attempts": [],
        "delivery": None,
    }
    logger.info(
        "subject_assembly_complete subject=%s qa_state=%s "
        "validation_errors=%s lint_findings=%s",
        subject, status,
        len(validation["report"].get("errors") or []), warning_count,
    )
    return result


def package_subject_delivery(
    record: dict[str, Any],
    *,
    run_dir: Path,
) -> Path:
    subject = record["subject"]
    logger.info(
        "delivery_packaging_start subject=%s delivery_state=%s",
        subject, record.get("state"),
    )
    final_root = run_dir / "final" / subject
    final_root.mkdir(parents=True, exist_ok=True)
    delivery = final_root / f"astrowoof-{subject}-delivery.zip"
    included = [
        Path(record["deck"]),
        Path(record["assembly_report"]),
        Path(record["validation_report"]),
        Path(record["lint_report"]),
    ]
    run_state_path = run_dir / "run.json"
    run_state = load_json(run_state_path) if run_state_path.is_file() else {}
    run_provenance = run_state.get("provenance") or {}
    resource_provenance = run_provenance.get("resources") or {}
    input_subject = next(
        (
            item
            for item in (run_provenance.get("input") or {}).get("subjects", [])
            if item.get("subject_id") == subject
        ),
        None,
    )
    delivery_deck = load_json(Path(record["deck"]))
    evidence_scopes = {
        "selected_cards": {
            "scope": "claim_local_selected_evidence",
            "claim_ids": [
                card.get("claim_id")
                for card in delivery_deck.get("cards", [])
                if card.get("claim_id")
            ],
        },
        "summary_and_whole_dog": {
            "scope": "broader_synthesis_evidence",
            "sources": [
                "selected_cards",
                "unselected_claims",
                "whole_graph_analysis",
                "projected_term_registry",
            ],
            "unselected_claim_count": len(
                delivery_deck.get("unselected_claims", [])
            ),
        },
    }
    delivery_manifest = {
        "schema_version": DELIVERY_MANIFEST_SCHEMA,
        "subject_id": subject,
        "status": record["state"],
        "created_at": utc_now(),
        "run_contract": run_state.get("schema_version", SCHEMA_VERSION),
        "authoring_profile": run_state.get("authoring_profile"),
        "provenance": {
            "schema_version": run_provenance.get("schema_version"),
            "runtime": run_provenance.get("runtime"),
            "resources": {
                "schema_version": resource_provenance.get("schema_version"),
                "aggregate_sha256": resource_provenance.get("aggregate_sha256"),
                "resource_count": resource_provenance.get("resource_count"),
            },
            "input_subject": input_subject,
            "evidence_scopes": evidence_scopes,
        },
        "artifacts": [
            artifact_descriptor(path, role=role)
            for role, path in zip(
                ("deck", "assembly_report", "validation_report", "lint_report"),
                included,
                strict=True,
            )
        ],
    }
    manifest_path = final_root / f"natal.{subject}.delivery-manifest.json"
    write_json_atomic(manifest_path, delivery_manifest)
    included.append(manifest_path)
    with zipfile.ZipFile(
        delivery,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:
        for path in included:
            archive.write(path, path.name)
    with zipfile.ZipFile(delivery) as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise ValueError(f"Corrupt delivery archive member: {bad_member}")
    record["delivery"] = normalized_path(delivery)
    record["delivery_manifest"] = normalized_path(manifest_path)
    record["delivery_artifact"] = artifact_descriptor(
        delivery,
        role="delivery_zip",
    )
    logger.info(
        "delivery_packaging_complete subject=%s artifact=%s sha256=%s",
        subject, delivery, record["delivery_artifact"].get("sha256"),
    )
    return delivery


def sanitize_context_filters(deck: dict[str, Any]) -> list[dict[str, Any]]:
    """Remove impossible filter labels while preserving valid LLM choices."""
    registered = {
        level: {
            item["name"]
            for item in deck.get("context_filter_groups", [])
            if item.get("level") == level and isinstance(item.get("name"), str)
        }
        for level in ("high", "detail")
    }
    repairs: list[dict[str, Any]] = []
    for index, card in enumerate(deck.get("cards", []), 1):
        filters = card.get("context_filter_groups")
        if not isinstance(filters, dict):
            continue
        for key, level in (("high_level", "high"), ("detail_level", "detail")):
            values = filters.get(key)
            if not isinstance(values, list):
                continue
            kept: list[str] = []
            removed: list[Any] = []
            for value in values:
                if value in registered[level] and value not in kept:
                    kept.append(value)
                else:
                    removed.append(value)
            if removed:
                filters[key] = kept
                repairs.append({
                    "card": index,
                    "claim_id": card.get("claim_id"),
                    "field": key,
                    "removed": removed,
                    "retained": kept,
                })
    return repairs


def editable_deck_fields(
    deck: dict[str, Any],
    *,
    include_theme_groups: bool = False,
) -> dict[str, str]:
    """Flatten only reader-facing prose into a strict polish transport."""
    fields: dict[str, str] = {}

    def collect_card(prefix: str, card: dict[str, Any]) -> None:
        for name in (
            "funny_dog_quotes",
            "imperative_dog_quotes",
            "applicable_canine_jokes",
        ):
            for index, value in enumerate(card[name]):
                fields[f"{prefix}.{name}.{index}"] = value
        for density in ("no_astro", "light_astro", "full_astro"):
            for part in ("headline", "body"):
                for voice in ("handler", "direct_to_dog", "hybrid"):
                    path = f"{prefix}.{density}.{part}.{voice}"
                    fields[path] = card[density][part][voice]

    for card_index, claim in enumerate(deck["cards"]):
        prefix = f"cards.{card_index}"
        if include_theme_groups and "theme_group_id" in claim:
            fields[f"{prefix}.theme_group_id"] = claim["theme_group_id"]
        for name in ("dos", "donts"):
            for item_index, value in enumerate(claim[name]):
                fields[f"{prefix}.{name}.{item_index}"] = value
        collect_card(f"{prefix}.card", claim["card"])
    for key, summary in deck["summary"].items():
        prefix = f"summary.{key}"
        for name in ("dos", "donts"):
            for item_index, value in enumerate(summary[name]):
                fields[f"{prefix}.{name}.{item_index}"] = value
        collect_card(prefix, summary)
    if include_theme_groups:
        for section, entries in deck.get("theme_group_registry", {}).items():
            for index, entry in enumerate(entries):
                for name in (
                    "id", "title", "short_title", "emoji", "subtitle"
                ):
                    if name not in entry:
                        continue
                    fields[
                        f"theme_group_registry.{section}.{index}.{name}"
                    ] = entry[name]
    return fields


def apply_deck_fields(
    deck: dict[str, Any],
    authored: dict[str, Any],
    *,
    include_theme_groups: bool = False,
) -> dict[str, Any]:
    expected = editable_deck_fields(
        deck,
        include_theme_groups=include_theme_groups,
    )
    actual = authored.get("fields") if isinstance(authored, dict) else None
    if not isinstance(actual, dict) or set(actual) != set(expected):
        raise ValueError("Polish field map does not exactly match the deck")
    result = deepcopy(deck)
    for path, value in actual.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Polish field {path} must be a nonempty string")
        current: Any = result
        parts = path.split(".")
        for part in parts[:-1]:
            current = (
                current[int(part)]
                if isinstance(current, list)
                else current[part]
            )
        last = parts[-1]
        if isinstance(current, list):
            current[int(last)] = value
        else:
            current[last] = value
    return result


def polish_output_schema(fields: dict[str, str]) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "fields": {
                "type": "object",
                "properties": {
                    path: {"type": "string"} for path in fields
                },
                "required": list(fields),
                "additionalProperties": False,
            }
        },
        "required": ["fields"],
        "additionalProperties": False,
    }


def _lint_item_editable_path(
    deck: dict[str, Any],
    item: dict[str, str],
) -> str | None:
    location = item["location"]
    field = item["field"].replace("[", ".").replace("]", "")
    if location.startswith("card:"):
        claim_id = location.removeprefix("card:")
        index = next(
            (
                index
                for index, card in enumerate(deck["cards"])
                if card["claim_id"] == claim_id
            ),
            None,
        )
        if index is None:
            return None
        card_prefix = f"cards.{index}"
        return (
            f"{card_prefix}.{field}"
            if item["kind"] in {"dos", "donts"}
            else f"{card_prefix}.card.{field}"
        )
    if location.startswith("summary:"):
        summary_key = location.removeprefix("summary:")
        return f"summary.{summary_key}.{field}"
    return None


def polish_target_paths(
    deck: dict[str, Any],
    *,
    lint_report: dict[str, Any],
    validation_report: dict[str, Any],
    include_theme_groups: bool,
    expand_related: bool = False,
) -> list[str]:
    """Resolve machine findings to the smallest safe prose edit allowlist."""
    all_fields = editable_deck_fields(
        deck,
        include_theme_groups=include_theme_groups,
    )
    items = reader_facing_items(deck)
    item_paths = {
        (item["location"], item["field"]): _lint_item_editable_path(deck, item)
        for item in items
    }
    targets: set[str] = set()

    def add_location_field(location: str, field: str) -> None:
        path = item_paths.get((location, field))
        if path in all_fields:
            targets.add(path)

    warnings = [
        warning
        for deck_report in lint_report.get("decks", [])
        for warning in deck_report.get("warnings", [])
    ]
    warnings.extend(lint_report.get("cross_subject_warnings", []))
    for warning in warnings:
        code = warning.get("code")
        details = warning.get("details") or {}
        if code == "repeated_opening":
            for claim_id in details.get("claim_ids", []):
                add_location_field(f"card:{claim_id}", details.get("field", ""))
        elif code == "claim_type_template":
            expected_field = (
                f"{details.get('density')}.body.{details.get('voice')}"
            )
            opening = str(details.get("opening") or "")
            for item in items:
                if (
                    item["claim_type"] == details.get("claim_type")
                    and item["field"] == expected_field
                    and item["text"].lower().startswith(opening.lower())
                ):
                    add_location_field(item["location"], item["field"])
        elif code == "duplicate_body":
            for location_field in details.get("locations", []):
                location, field = location_field.rsplit(":", 1)
                add_location_field(location, field)
        elif code == "repeated_sentence":
            excerpt = str(details.get("excerpt") or "").lower()
            claims = set(details.get("claim_ids", []))
            for item in items:
                if (
                    item["kind"] == "body"
                    and item["claim_id"] in claims
                    and excerpt in item["text"].lower()
                ):
                    add_location_field(item["location"], item["field"])
        elif code and code.startswith("duplicate_"):
            excerpt = str(details.get("excerpt") or "").lower()
            claims = set(details.get("claim_ids", []))
            for item in items:
                if (
                    item["claim_id"] in claims
                    and item["text"].lower().startswith(excerpt)
                ):
                    add_location_field(item["location"], item["field"])
        elif code == "failure_signature":
            add_location_field(
                str(details.get("location") or ""),
                str(details.get("field") or ""),
            )
        elif code in {"repeated_failure_signature", "cross_subject_duplicate"}:
            locations = details.get("locations", [])
            locations += details.get("left_locations", [])
            locations += details.get("right_locations", [])
            for location_field in locations:
                location, field = location_field.rsplit(":", 1)
                add_location_field(location, field)

    for deck_report in lint_report.get("decks", []):
        acceptance = deck_report.get("authoring_pass_acceptance") or {}
        for group in acceptance.get("exact_duplicate_groups", []):
            for location_field in group.get("locations", []):
                location, field = location_field.rsplit(":", 1)
                add_location_field(location, field)
        for group in acceptance.get("repeated_ngrams", []):
            excerpt = str(group.get("text") or "").lower()
            claims = set(group.get("claim_ids", []))
            for item in items:
                if (
                    item["kind"] == "body"
                    and item["claim_id"] in claims
                    and excerpt in item["text"].lower()
                ):
                    add_location_field(item["location"], item["field"])
        for artifact in acceptance.get("suspicious_artifacts", []):
            claim_id = artifact.get("claim_id")
            field = artifact.get("field")
            for item in items:
                if item["claim_id"] == claim_id and item["field"] == field:
                    add_location_field(item["location"], item["field"])
        for opening in acceptance.get("dominant_openings", []):
            field = opening.get("field")
            prefix = str(opening.get("opening") or "").lower()
            claims = set(opening.get("claim_ids", []))
            for item in items:
                if (
                    item["claim_id"] in claims
                    and item["field"] == field
                    and item["text"].lower().startswith(prefix)
                ):
                    add_location_field(item["location"], item["field"])

    validation_errors = [
        str(error) for error in validation_report.get("errors", [])
    ]
    if include_theme_groups:
        targets.update(
            path
            for path in all_fields
            if path.endswith(".theme_group_id")
            or path.startswith("theme_group_registry.")
        )
    for error in validation_errors:
        card_match = re.search(r"\bCard\s+(\d+)\b", error, re.IGNORECASE)
        field_match = re.search(
            r"\b(no_astro|light_astro|full_astro)\."
            r"(headline|body)\.(handler|direct_to_dog|hybrid)\b",
            error,
        )
        if card_match and field_match:
            path = (
                f"cards.{int(card_match.group(1)) - 1}.card."
                f"{field_match.group(0)}"
            )
            if path in all_fields:
                targets.add(path)

    if expand_related and targets:
        prefixes = {
            ".".join(path.split(".")[:2])
            for path in targets
            if path.startswith("cards.")
        }
        targets.update(
            path
            for path in all_fields
            if any(path.startswith(f"{prefix}.") for prefix in prefixes)
        )
    return sorted(targets)


def lint_finding_count(lint_report: dict[str, Any]) -> int:
    """Count ordinary warnings plus unresolved deck-level rejection classes."""
    rejection_count = sum(
        len(
            (deck_report.get("authoring_pass_acceptance") or {}).get(
                "rejection_reasons", []
            )
        )
        for deck_report in lint_report.get("decks", [])
    )
    return int(lint_report.get("warning_count") or 0) + rejection_count


def sparse_polish_context(
    deck: dict[str, Any],
    target_paths: list[str],
) -> dict[str, str]:
    """Supply nearby prose as read-only context without making it editable."""
    all_fields = editable_deck_fields(deck, include_theme_groups=True)
    selected = set(target_paths)
    for target in target_paths:
        parts = target.split(".")
        if target.startswith("cards."):
            card_index = int(parts[1])
            card_prefix = f"cards.{card_index}"
            if target.endswith(".theme_group_id") or target.startswith(
                "theme_group_registry."
            ):
                continue
            if len(parts) >= 6 and parts[2] == "card" and parts[3] in {
                "no_astro",
                "light_astro",
                "full_astro",
            }:
                density = parts[3]
                for path in all_fields:
                    if path.startswith(f"{card_prefix}.card.{density}."):
                        selected.add(path)
                suffix = ".".join(parts[3:])
                for neighbor in (card_index - 1, card_index + 1):
                    neighbor_path = f"cards.{neighbor}.card.{suffix}"
                    if neighbor_path in all_fields:
                        selected.add(neighbor_path)
            elif parts[2] in {"dos", "donts"}:
                selected.update(
                    path
                    for path in all_fields
                    if path.startswith(f"{card_prefix}.dos.")
                    or path.startswith(f"{card_prefix}.donts.")
                )
            elif parts[2] == "card":
                selected.update(
                    path
                    for path in all_fields
                    if path.startswith(f"{card_prefix}.card.")
                    and not any(
                        f".{density}." in path
                        for density in ("no_astro", "light_astro", "full_astro")
                    )
                )
        elif target.startswith("summary."):
            summary_prefix = ".".join(parts[:2])
            selected.update(
                path
                for path in all_fields
                if path.startswith(f"{summary_prefix}.")
            )
    return {
        path: all_fields[path]
        for path in sorted(selected)
        if path in all_fields
    }


def sparse_polish_basis(
    deck: dict[str, Any],
    target_paths: list[str],
) -> dict[str, Any]:
    def compact_evidence(card: dict[str, Any]) -> list[dict[str, Any]]:
        compact: list[dict[str, Any]] = []
        attribute_keys = (
            "canonical_object_name",
            "source_sign",
            "source_house",
            "doghouse_number",
            "projected_mode",
            "projected_domain",
            "canonical_aspect",
            "orb",
            "source_canine_subsystem",
            "target_canine_subsystem",
            "source_mode",
            "target_mode",
            "source_doghouse",
            "target_doghouse",
            "interaction_mode",
            "projection_composition",
            "projection_first_reasoning",
        )
        for evidence in card.get("evidence", []):
            item: dict[str, Any] = {
                key: evidence[key]
                for key in (
                    "kind",
                    "role",
                    "generation_rule",
                    "shared_key",
                    "supporting_candidate_ids",
                    "claim_ids",
                    "priority_ids",
                )
                if evidence.get(key) not in (None, [], {})
            }
            records = evidence.get("context_records") or {}
            context = records.get("general") or next(
                iter(records.values()), {}
            )
            record = context.get("record") or {}
            if record:
                attributes = record.get("attributes") or {}
                item["projected_record"] = {
                    key: value
                    for key, value in {
                        "name": record.get("name"),
                        "relationship_type": record.get("relationship_type"),
                        "operators": record.get("operators"),
                        "theme_tags": record.get("theme_tags"),
                        "attributes": {
                            key: attributes.get(key)
                            for key in attribute_keys
                            if attributes.get(key) is not None
                        },
                    }.items()
                    if value not in (None, [], {})
                }
            summaries = evidence.get("source_record_summaries")
            if summaries:
                item["source_record_summaries"] = [
                    {
                        key: summary[key]
                        for key in (
                            "relationship_type",
                            "interaction_mode",
                            "theme_tags",
                        )
                        if summary.get(key) not in (None, [], {})
                    }
                    for summary in summaries
                ]
            if item:
                compact.append(item)
        return compact

    card_indexes = sorted({
        int(path.split(".")[1])
        for path in target_paths
        if path.startswith("cards.")
    })
    return {
        "subject": provider_visible_subject(deck.get("subject")),
        "cards": [
            {
                "index": index,
                "claim_id": deck["cards"][index].get("claim_id"),
                "claim_type": deck["cards"][index].get("claim_type"),
                "canonical_claim": deck["cards"][index].get("canonical_claim"),
                "categories": deck["cards"][index].get("categories", []),
                "behavioral_domains": deck["cards"][index].get(
                    "behavioral_domains", []
                ),
                "semantic_evidence": compact_evidence(deck["cards"][index]),
                "evidence_sources": [
                    {
                        "kind": evidence.get("kind"),
                        "role": evidence.get("role"),
                        "source_refs": evidence.get("source_refs", []),
                        "claim_ids": evidence.get("claim_ids", []),
                    }
                    for evidence in deck["cards"][index].get("evidence", [])
                ],
            }
            for index in card_indexes
        ],
    }


def sparse_polish_transport_metrics(
    deck: dict[str, Any],
    *,
    target_paths: list[str],
    include_theme_groups: bool,
) -> dict[str, Any]:
    all_fields = editable_deck_fields(
        deck,
        include_theme_groups=include_theme_groups,
    )
    targets = {path: all_fields[path] for path in target_paths}
    context = sparse_polish_context(deck, target_paths)
    basis = sparse_polish_basis(deck, target_paths)
    full_text = json.dumps(all_fields, ensure_ascii=False, separators=(",", ":"))
    sparse_text = json.dumps(
        {"targets": targets, "context": context, "basis": basis},
        ensure_ascii=False,
        separators=(",", ":"),
    )
    full_output_text = json.dumps(
        {"fields": all_fields}, ensure_ascii=False, separators=(",", ":")
    )
    target_output_text = json.dumps(
        {"edits": [
            {
                "field_path": path,
                "replacement": value,
                "reason_codes": [],
            }
            for path, value in targets.items()
        ]},
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return {
        "mode": "sparse_patch",
        "editable_target_count": len(target_paths),
        "reference_field_count": len(context),
        "full_field_count": len(all_fields),
        "input_estimated_tokens": {
            "full_map": estimated_text_tokens(full_text),
            "sparse_transport": estimated_text_tokens(sparse_text),
        },
        "output_estimated_tokens": {
            "full_map": estimated_text_tokens(full_output_text),
            "target_ceiling": estimated_text_tokens(target_output_text),
        },
    }


def sparse_polish_output_schema(target_paths: list[str]) -> dict[str, Any]:
    if not target_paths:
        raise ValueError("Sparse polish requires at least one editable target")
    return {
        "type": "object",
        "properties": {
            "edits": {
                "type": "array",
                "minItems": 0,
                "maxItems": len(target_paths),
                "items": {
                    "type": "object",
                    "properties": {
                        "field_path": {
                            "type": "string",
                            "enum": target_paths,
                        },
                        "replacement": {"type": "string"},
                        "reason_codes": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": [
                        "field_path",
                        "replacement",
                        "reason_codes",
                    ],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["edits"],
        "additionalProperties": False,
    }


QUALITATIVE_DIMENSIONS = (
    "summary_thesis_overlap",
    "conceptual_card_overlap",
    "repeated_comic_mechanism",
    "repeated_rhetorical_posture",
    "exchangeable_headline",
    "over_explained_body",
    "incomplete_compound_semantics",
    "insufficient_audience_distinction",
    "insufficient_astrology_density_progression",
    "other_editorial_quality",
)
CRITIC_FINDINGS_SCHEMA = "astrowoof.qualitative_critic_findings.v0.1"
CRITIC_SCOPES = ("summary", "card", "deck")
CRITIC_PRIORITIES = ("high", "medium", "low")
CRITIC_REPAIRABILITIES = (
    "local_repair", "upstream_reconception", "advisory_only",
)
CRITIC_REQUIRED_CONTEXT = (
    "nearby_prose", "claim_evidence", "whole_chart", "none",
)
CRITIC_SELECTION_REASONS = (
    "eligible",
    "not_locally_repairable",
    "low_priority",
    "confidence_below_0.70",
    "field_cap",
    "card_cap",
)


def qualitative_critic_output_schema(max_findings: int) -> dict[str, Any]:
    """Strict diagnosis-only response; paths are validated after decoding."""
    if max_findings < 1:
        raise ValueError("Qualitative critic requires a positive finding cap")
    return {
        "type": "object",
        "properties": {
            "deck_assessment": {
                "type": "object",
                "properties": {
                    "strengths": {
                        "type": "array",
                        "maxItems": 4,
                        "items": {"type": "string"},
                    },
                    "primary_risks": {
                        "type": "array",
                        "maxItems": 4,
                        "items": {"type": "string"},
                    },
                },
                "required": ["strengths", "primary_risks"],
                "additionalProperties": False,
            },
            "findings": {
                "type": "array",
                "maxItems": max_findings,
                "items": {
                    "type": "object",
                    "properties": {
                        "finding_id": {"type": "string"},
                        "quality_dimension": {
                            "type": "string",
                            "enum": list(QUALITATIVE_DIMENSIONS),
                        },
                        "scope": {
                            "type": "string",
                            "enum": list(CRITIC_SCOPES),
                        },
                        "priority": {
                            "type": "string",
                            "enum": list(CRITIC_PRIORITIES),
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                        },
                        "repairability": {
                            "type": "string",
                            "enum": list(CRITIC_REPAIRABILITIES),
                        },
                        "target_paths": {
                            "type": "array",
                            "minItems": 1,
                            "maxItems": 4,
                            "items": {"type": "string"},
                        },
                        "comparison_paths": {
                            "type": "array",
                            "maxItems": 8,
                            "items": {"type": "string"},
                        },
                        "diagnosis": {"type": "string"},
                        "rewrite_objective": {"type": "string"},
                        "required_context": {
                            "type": "array",
                            "maxItems": 4,
                            "items": {
                                "type": "string",
                                "enum": list(CRITIC_REQUIRED_CONTEXT),
                            },
                        },
                    },
                    "required": [
                        "finding_id",
                        "quality_dimension",
                        "scope",
                        "priority",
                        "confidence",
                        "repairability",
                        "target_paths",
                        "comparison_paths",
                        "diagnosis",
                        "rewrite_objective",
                        "required_context",
                    ],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["deck_assessment", "findings"],
        "additionalProperties": False,
    }


def qualitative_critic_transport(deck: dict[str, Any]) -> dict[str, Any]:
    """Build a complete but provenance-light read-only editorial deck view."""
    fields = editable_deck_fields(deck, include_theme_groups=False)
    basis_targets = [
        f"cards.{index}.card.no_astro.body.handler"
        for index in range(len(deck.get("cards", [])))
    ]
    semantic_cards = sparse_polish_basis(deck, basis_targets)["cards"]
    cards = [
        {
            "index": index,
            "claim_id": card.get("claim_id"),
            "claim_type": card.get("claim_type"),
            "canonical_claim": card.get("canonical_claim"),
            "categories": card.get("categories", []),
            "behavioral_domains": card.get("behavioral_domains", []),
            "priority_id": card.get("priority_id"),
            "semantic_evidence": semantic_cards[index].get(
                "semantic_evidence", []
            ),
        }
        for index, card in enumerate(deck.get("cards", []))
    ]
    return {
        "subject": provider_visible_subject(deck.get("subject")),
        "card_descriptors": cards,
        "reader_facing_fields": fields,
    }


def critic_findings_artifact(
    selection: dict[str, Any],
    *,
    run_dir: Path,
    deck_path: Path,
    response_path: Path,
    metadata: dict[str, Any],
    run_state: dict[str, Any] | None,
) -> dict[str, Any]:
    """Bind normalized critic findings to exact private run evidence."""
    state = run_state or {}
    provenance = state.get("provenance") or {}
    profile = state.get("authoring_profile") or {}
    result = deepcopy(selection)
    result["schema_version"] = CRITIC_FINDINGS_SCHEMA
    result["artifact_kind"] = "normalized_qualitative_critic_findings"
    result["provenance"] = {
        "criticized_deck": {
            "path": deck_path.relative_to(run_dir).as_posix(),
            **artifact_descriptor(deck_path, role="criticized_final_deck"),
        },
        "raw_provider_response": {
            "path": response_path.relative_to(run_dir).as_posix(),
            **artifact_descriptor(response_path, role="raw_critic_provider_response"),
        },
        "provider": {
            "kind": "response",
            "response_id": metadata.get("response_id"),
            "model": metadata.get("requested_model") or metadata.get("model"),
            "reasoning_effort": (
                (metadata.get("routing") or {}).get("reasoning_effort")
                or metadata.get("reasoning_effort")
            ),
            "service_level": metadata.get("service_level") or "interactive",
        },
        "run": {
            "run_id": state.get("run_id"),
            "operator_schema_version": state.get("schema_version"),
            "state_revision": state.get("state_revision"),
            "authoring_profile": {
                "schema_version": profile.get("schema_version"),
                "profile_id": profile.get("profile_id"),
                "sha256": spend_profile_digest(profile),
            },
            "runtime": provenance.get("runtime"),
            "resources": provenance.get("resources"),
        },
    }
    return result


def validate_critic_findings_artifact(value: dict[str, Any]) -> dict[str, Any]:
    """Fail closed on unsupported normalized critic consumer artifacts."""
    if value.get("schema_version") != CRITIC_FINDINGS_SCHEMA:
        raise ValueError("Unsupported critic-findings schema_version")
    findings = ((value.get("critic") or {}).get("findings"))
    if not isinstance(findings, list):
        raise ValueError("critic-findings artifact has no normalized findings")
    required = {
        "finding_id", "quality_dimension", "scope", "priority", "confidence",
        "repairability", "target_paths", "comparison_paths", "diagnosis",
        "rewrite_objective", "required_context", "selected_for_candidate",
        "selection_reason",
    }
    for finding in findings:
        if not isinstance(finding, dict) or not required <= set(finding):
            raise ValueError("critic-findings artifact has incomplete finding")
        if finding["quality_dimension"] not in QUALITATIVE_DIMENSIONS:
            raise ValueError("critic-findings artifact has unknown quality_dimension")
        if finding["scope"] not in CRITIC_SCOPES:
            raise ValueError("critic-findings artifact has unknown scope")
        if finding["priority"] not in CRITIC_PRIORITIES:
            raise ValueError("critic-findings artifact has unknown priority")
        if finding["repairability"] not in CRITIC_REPAIRABILITIES:
            raise ValueError("critic-findings artifact has unknown repairability")
        if any(item not in CRITIC_REQUIRED_CONTEXT for item in finding["required_context"]):
            raise ValueError("critic-findings artifact has unknown required_context")
        reason = finding["selection_reason"]
        if reason is not None and reason not in CRITIC_SELECTION_REASONS:
            raise ValueError("critic-findings artifact has unknown selection_reason")
    provenance = value.get("provenance") or {}
    if not (provenance.get("criticized_deck") or {}).get("sha256"):
        raise ValueError("critic-findings artifact lacks criticized-deck identity")
    if not (provenance.get("raw_provider_response") or {}).get("sha256"):
        raise ValueError("critic-findings artifact lacks provider-response identity")
    if not (provenance.get("provider") or {}).get("response_id"):
        raise ValueError("critic-findings artifact lacks provider Response ID")
    run = provenance.get("run") or {}
    if not run.get("run_id") or not run.get("operator_schema_version"):
        raise ValueError("critic-findings artifact lacks run identity")
    if not (run.get("authoring_profile") or {}).get("sha256"):
        raise ValueError("critic-findings artifact lacks authoring-profile identity")
    if not run.get("runtime") or not run.get("resources"):
        raise ValueError("critic-findings artifact lacks runtime/resource identity")
    return value


def validate_qualitative_critic_response(
    deck: dict[str, Any],
    response: dict[str, Any],
    *,
    max_findings: int,
    max_target_fields: int,
    max_target_cards: int,
) -> dict[str, Any]:
    """Reject invented paths and cap the critic before it can imply a rewrite."""
    if not isinstance(response, dict):
        raise ValueError("Qualitative critic response must be an object")
    findings = response.get("findings")
    if not isinstance(findings, list) or len(findings) > max_findings:
        raise ValueError("Qualitative critic exceeded its finding cap")
    fields = editable_deck_fields(deck, include_theme_groups=False)
    valid_paths = set(fields)
    finding_ids: set[str] = set()
    eligible: list[dict[str, Any]] = []
    selected_paths: list[str] = []
    selected_cards: set[str] = set()
    normalized = deepcopy(response)
    for finding in normalized["findings"]:
        finding_id = finding.get("finding_id")
        if not isinstance(finding_id, str) or not finding_id.strip():
            raise ValueError("Qualitative finding ID must be nonempty")
        if finding_id in finding_ids:
            raise ValueError(f"Duplicate qualitative finding ID: {finding_id}")
        finding_ids.add(finding_id)
        targets = finding.get("target_paths") or []
        comparisons = finding.get("comparison_paths") or []
        unknown = [
            path for path in [*targets, *comparisons] if path not in valid_paths
        ]
        if unknown:
            raise ValueError(
                f"Qualitative critic invented reader-facing paths: {unknown}"
            )
        if len(set(targets)) != len(targets):
            raise ValueError(
                f"Qualitative finding {finding_id} repeats target paths"
            )
        finding["selected_for_candidate"] = False
        finding["selection_reason"] = None
        if finding.get("repairability") != "local_repair":
            finding["selection_reason"] = "not_locally_repairable"
            continue
        if finding.get("priority") == "low":
            finding["selection_reason"] = "low_priority"
            continue
        if float(finding.get("confidence") or 0.0) < 0.70:
            finding["selection_reason"] = "confidence_below_0.70"
            continue
        candidate_new_paths = [path for path in targets if path not in selected_paths]
        candidate_cards = {
            ".".join(path.split(".")[:2])
            if path.startswith(("cards.", "summary."))
            else path
            for path in candidate_new_paths
        }
        if len(selected_paths) + len(candidate_new_paths) > max_target_fields:
            finding["selection_reason"] = "field_cap"
            continue
        if len(selected_cards | candidate_cards) > max_target_cards:
            finding["selection_reason"] = "card_cap"
            continue
        finding["selected_for_candidate"] = True
        finding["selection_reason"] = "eligible"
        selected_paths.extend(candidate_new_paths)
        selected_cards.update(candidate_cards)
        eligible.append(finding)
    return {
        "critic": normalized,
        "eligible_findings": eligible,
        "selected_target_paths": selected_paths,
        "selected_location_count": len(selected_cards),
        "limits": {
            "max_findings": max_findings,
            "max_target_fields": max_target_fields,
            "max_target_cards": max_target_cards,
            "minimum_confidence": 0.70,
            "eligible_priorities": ["high", "medium"],
            "eligible_repairability": "local_repair",
        },
    }


def apply_sparse_polish(
    deck: dict[str, Any],
    authored: dict[str, Any],
    *,
    target_paths: list[str],
    include_theme_groups: bool,
) -> dict[str, Any]:
    edits = authored.get("edits") if isinstance(authored, dict) else None
    if not isinstance(edits, list):
        raise ValueError("Sparse polish response must contain an edit list")
    allowed = set(target_paths)
    seen: set[str] = set()
    result = deepcopy(deck)
    for edit in edits:
        if not isinstance(edit, dict):
            raise ValueError("Sparse polish edit must be an object")
        path = edit.get("field_path")
        replacement = edit.get("replacement")
        if path not in allowed:
            raise ValueError(f"Sparse polish field is not editable: {path}")
        if path in seen:
            raise ValueError(f"Sparse polish repeats field: {path}")
        if not isinstance(replacement, str) or not replacement.strip():
            raise ValueError(f"Sparse polish field {path} must be nonempty")
        if (
            path.endswith(".theme_group_id")
            or path.startswith("theme_group_registry.")
        ) and not include_theme_groups:
            raise ValueError("Theme groups are locked for this polish attempt")
        current: Any = result
        parts = path.split(".")
        for part in parts[:-1]:
            current = current[int(part)] if isinstance(current, list) else current[part]
        last = parts[-1]
        if isinstance(current, list):
            current[int(last)] = replacement.strip()
        else:
            current[last] = replacement.strip()
        seen.add(path)
    return result


def polish_subject(
    *,
    record: dict[str, Any],
    provider: OpenAIResponsesProvider,
    run_dir: Path,
    python_executable: Path,
    max_attempts: int,
    spend_controller: SpendController | None = None,
) -> None:
    """Try bounded whole-deck polish; retain baseline unless QA improves."""
    subject = record["subject"]
    logger.info(
        "polish_start subject=%s max_attempts=%s baseline_state=%s",
        subject, max_attempts, record.get("state"),
    )
    baseline_path = Path(record["deck"])
    baseline = load_json(baseline_path)
    current_lint_report = load_json(Path(record["lint_report"]))
    current_validation_report = load_json(Path(record["validation_report"]))
    best_warning_count = lint_finding_count(current_lint_report)
    best_validation_passed = current_validation_report.get("status") == "pass"
    best_validation_error_count = len(
        current_validation_report.get("errors") or []
    )
    best_path = baseline_path
    final_root = run_dir / "final" / subject
    validator_path = Path(validation_module.__file__).resolve()
    linter_path = Path(editorial_lint_module.__file__).resolve()
    polish_attempts = record.setdefault("polish_attempts", [])
    pending_attempt = (
        polish_attempts[-1]
        if polish_attempts and polish_attempts[-1].get("state") == "SUBMITTED"
        else None
    )
    first_attempt_number = (
        int(pending_attempt["attempt_number"])
        if pending_attempt is not None
        else len(polish_attempts) + 1
    )
    for attempt_number in range(
        first_attempt_number,
        max_attempts + 1,
    ):
        resuming_attempt = (
            pending_attempt is not None
            and attempt_number == int(pending_attempt["attempt_number"])
        )
        attempt_root = final_root / "polish" / f"attempt-{attempt_number:03d}"
        lint_report = load_json(Path(record["lint_report"]))
        validation_report = load_json(Path(record["validation_report"]))
        allow_theme_group_edits = any(
            "theme group" in str(error).lower()
            for error in validation_report.get("errors", [])
        )
        prior_attempts = (
            polish_attempts[:-1] if resuming_attempt else polish_attempts
        )
        expand_related = (
            bool(prior_attempts)
            and not bool(prior_attempts[-1].get("improved"))
            and not allow_theme_group_edits
        )
        system = (
            "You are performing a surgical whole-deck editorial polish. "
            "Return only a sparse list of necessary replacements chosen from "
            "the supplied editable target paths. Omit a target when its current "
            "prose is already the best editorial choice; an empty edit list is "
            "correct when every finding is advisory or a false positive. "
            "Preserve every factual, evidentiary, structural, selection, "
            "category, filter, and identity value. Edit only "
            "reader-facing prose needed to resolve the supplied lint findings. "
            "Every replacement must repair the named mechanism while retaining "
            "the field's strongest image, behavioral insight, useful guidance, "
            "and all semantic contributions in the repair basis. Concision means "
            "removing duplicated labor, not automatically shortening prose. "
            "Theme groups may change only when validation explicitly requires "
            "rebalancing. Summary prose may change only when its path is "
            "explicitly included in the editable targets. "
            "Do not homogenize distinct cards or rewrite clean material."
        )
        current_deck = load_json(best_path)
        target_paths = polish_target_paths(
            current_deck,
            lint_report=lint_report,
            validation_report=validation_report,
            include_theme_groups=allow_theme_group_edits,
            expand_related=expand_related,
        )
        allow_summary_edits = any(
            path.startswith("summary.") for path in target_paths
        )
        if not target_paths:
            record["polish_unaddressable"] = {
                "validation_errors": validation_report.get("errors", []),
                "lint_finding_count": lint_finding_count(lint_report),
                "reason": "No validator-controlled editable fields matched.",
            }
            break
        current_fields = editable_deck_fields(
            current_deck,
            include_theme_groups=allow_theme_group_edits,
        )
        target_fields = {path: current_fields[path] for path in target_paths}
        reference_context = sparse_polish_context(
            current_deck,
            target_paths,
        )
        repair_basis = sparse_polish_basis(current_deck, target_paths)
        user = (
            f"Polish the AstroWoof deck for {subject}. Reduce the deterministic "
            "lint findings while retaining the same dog, meanings, evidence "
            "boundaries, voice distinctions, and astrology-density levels. "
            "A candidate is accepted only if structural validation passes and "
            "its warning count is lower than the current best.\n\n"
            "VALIDATION REPORT:\n"
            f"{json.dumps(validation_report, ensure_ascii=False)}\n\n"
            f"LINT REPORT:\n{json.dumps(lint_report, ensure_ascii=False)}\n\n"
            "REPAIR BASIS:\n"
            f"{json.dumps(repair_basis, ensure_ascii=False)}\n\n"
            "EDITABLE TARGETS (only these paths may be replaced):\n"
            f"{json.dumps(target_fields, ensure_ascii=False)}\n\n"
            "READ-ONLY NEARBY PROSE:\n"
            f"{json.dumps(reference_context, ensure_ascii=False)}"
        )
        if resuming_attempt:
            attempt = pending_attempt
        else:
            attempt = {
                "attempt_number": attempt_number,
                "state": "SUBMITTED",
                "started_at": utc_now(),
                "finished_at": None,
                "provider_metadata": None,
                "validation_report": None,
                "lint_report": None,
                "warning_count": None,
                "accepted": False,
                "transport": {
                    **sparse_polish_transport_metrics(
                        current_deck,
                        target_paths=target_paths,
                        include_theme_groups=allow_theme_group_edits,
                    ),
                    "editable_target_paths": target_paths,
                },
                "error": None,
            }
            polish_attempts.append(attempt)
        try:
            before_submit = provider_created = None
            if spend_controller is not None:
                before_submit, provider_created = spend_controller.callbacks(
                    stage="polish",
                    route=f"{subject}:polish:{attempt_number:03d}",
                    model=provider.model,
                    service_level="interactive",
                    maximum_output_tokens=provider.max_output_tokens,
                )
            authored, metadata = provider.complete_json(
                system=system,
                user=user,
                schema=sparse_polish_output_schema(target_paths),
                schema_name="astrowoof_sparse_polish",
                attempt_root=attempt_root,
                idempotency_material=(
                    f"{sha256_file(best_path)}:{subject}:polish:"
                    f"{attempt_number}:{provider.model}"
                ),
                before_submit=before_submit,
                provider_created=provider_created,
            )
            if spend_controller is not None:
                spend_controller.settle_active(metadata)
            metadata["routing"] = {
                "route": "polish",
                "model": provider.model,
                "reasoning_effort": getattr(
                    provider, "reasoning_effort", "unreported"
                ),
            }
            if (
                "fields" not in authored
                and isinstance(authored.get("edits"), list)
                and not authored["edits"]
            ):
                if not best_validation_passed:
                    raise ValueError(
                        "Polish may not return no-op while structural "
                        "validation errors remain"
                    )
                attempt.update(
                    {
                        "state": "POLISH_NO_CHANGE",
                        "finished_at": utc_now(),
                        "provider_metadata": metadata,
                        "warning_count": best_warning_count,
                        "accepted": False,
                        "improved": False,
                        "edited_field_count": 0,
                        "omitted_target_count": len(target_paths),
                    }
                )
                break
            candidate = (
                apply_deck_fields(
                    current_deck,
                    authored,
                    include_theme_groups=allow_theme_group_edits,
                )
                if "fields" in authored
                else apply_sparse_polish(
                    current_deck,
                    authored,
                    target_paths=target_paths,
                    include_theme_groups=allow_theme_group_edits,
                )
            )
            candidate_path = attempt_root / f"natal.{subject}.cards.json"
            write_json_atomic(candidate_path, candidate)
            validation_path = attempt_root / "validation-report.json"
            validation_command = [
                    str(python_executable),
                    str(validator_path),
                    str(best_path),
                    str(candidate_path),
                    "--phase",
                    "polish",
                    "--report",
                    str(validation_path),
                ]
            if allow_theme_group_edits:
                validation_command.append("--allow-theme-group-edits")
            if allow_summary_edits:
                validation_command.append("--allow-summary-edits")
            validation = run_json_command(
                validation_command,
                validation_path,
                accepted_returncodes={0},
            )
            lint_path = attempt_root / "lint-report.json"
            lint = run_json_command(
                [
                    str(python_executable),
                    str(linter_path),
                    str(candidate_path),
                    "--output",
                    str(lint_path),
                ],
                lint_path,
                accepted_returncodes={0, 2},
            )
            ordinary_lint_warning_count = int(
                lint["report"].get("warning_count") or 0
            )
            lint_warning_count = lint_finding_count(lint["report"])
            authoring_rejection_count = (
                lint_warning_count - ordinary_lint_warning_count
            )
            validation_warning_count = len(
                validation["report"].get("warnings") or []
            )
            validation_error_count = len(
                validation["report"].get("errors") or []
            )
            warning_count = lint_warning_count
            improved = (
                validation_error_count < best_validation_error_count
                or (
                    validation_error_count == best_validation_error_count
                    and warning_count < best_warning_count
                )
            )
            accepted = validation["accepted"] and (
                not best_validation_passed
                or warning_count < best_warning_count
            )
            attempt.update(
                {
                    "state": (
                        "POLISH_ACCEPTED"
                        if accepted
                        else "POLISH_IMPROVED_PARTIAL"
                        if improved
                        else "POLISH_REJECTED"
                    ),
                    "finished_at": utc_now(),
                    "provider_metadata": metadata,
                    "validation_report": normalized_path(validation_path),
                    "lint_report": normalized_path(lint_path),
                    "warning_count": warning_count,
                    "warning_components": {
                        "validation": validation_warning_count,
                        "lint": ordinary_lint_warning_count,
                        "authoring_rejections": authoring_rejection_count,
                    },
                    "accepted": accepted,
                    "improved": improved or accepted,
                    "validation_error_count": validation_error_count,
                    "edited_field_count": (
                        len(authored.get("edits", []))
                        if isinstance(authored, dict)
                        else None
                    ),
                    "omitted_target_count": (
                        len(target_paths) - len(authored.get("edits", []))
                        if isinstance(authored, dict)
                        and isinstance(authored.get("edits"), list)
                        else None
                    ),
                }
            )
            if accepted or improved:
                best_path = candidate_path
                best_warning_count = warning_count
                best_validation_passed = validation["accepted"]
                best_validation_error_count = validation_error_count
                shutil.copy2(candidate_path, baseline_path)
                shutil.copy2(validation_path, record["validation_report"])
                shutil.copy2(lint_path, record["lint_report"])
                if best_validation_passed and warning_count == 0:
                    break
        except Exception as exc:
            if isinstance(exc, AwaitingSpendAuthorization):
                raise
            if isinstance(exc, (BudgetExhausted, AmbiguousProviderSubmission)):
                action_state = (exc.action or {}).get("state")
                if action_state != "SKIPPED_BUDGET_EXHAUSTED":
                    raise
                attempt.update({
                    "state": "POLISH_SKIPPED_BUDGET_EXHAUSTED",
                    "finished_at": utc_now(),
                    "paid_action_id": (exc.action or {}).get("action_id"),
                    "error": None,
                })
                break
            attempt.update(
                {
                    "state": "POLISH_ERROR",
                    "finished_at": utc_now(),
                    "provider_metadata": getattr(exc, "metadata", None),
                    "error": {"type": type(exc).__name__, "message": str(exc)},
                }
            )
            if isinstance(exc, (OSError, RuntimeError)):
                logger.exception(
                    "polish_error subject=%s error_class=%s error=%s",
                    subject, type(exc).__name__,
                    sanitize_error_message(str(exc)),
                )
                raise
            if getattr(exc, "fatal", False):
                logger.error(
                    "polish_fatal subject=%s error_class=%s error=%s",
                    subject, type(exc).__name__,
                    sanitize_error_message(str(exc)),
                )
                break
    record["final_warning_count"] = best_warning_count
    if not best_validation_passed:
        record["state"] = "FINAL_QA_FAILED"
    else:
        record["state"] = (
            "DELIVERY_COMPLETE"
            if best_warning_count == 0
            else "FINAL_QA_WARN"
        )
    if record["state"] == "DELIVERY_COMPLETE":
        package_subject_delivery(record, run_dir=run_dir)
    logger.info(
        "polish_complete subject=%s final_state=%s warning_count=%s",
        subject, record.get("state"), best_warning_count,
    )


def qualitative_whole_deck_context(deck: dict[str, Any]) -> dict[str, Any]:
    """Compact behavioral overview for the rare repair needing deck context."""
    fields = editable_deck_fields(deck, include_theme_groups=False)
    selected = {
        path: value
        for path, value in fields.items()
        if (
            path.startswith("summary.")
            and ".no_astro." in path
            and (".headline.handler" in path or ".body.handler" in path)
        )
        or (
            path.startswith("cards.")
            and ".card.no_astro." in path
            and (".headline.handler" in path or ".body.handler" in path)
        )
    }
    return {
        "subject": provider_visible_subject(deck.get("subject")),
        "behavioral_handler_view": selected,
    }


def run_qualitative_review(
    *,
    record: dict[str, Any],
    critic_provider: OpenAIResponsesProvider,
    editor_provider: OpenAIResponsesProvider | None,
    run_dir: Path,
    python_executable: Path,
    max_findings: int,
    max_target_fields: int,
    max_target_cards: int,
    spend_controller: SpendController | None = None,
    run_state: dict[str, Any] | None = None,
) -> None:
    """Diagnose a complete deck and optionally preserve a sparse candidate."""
    logger.info(
        "qualitative_review_start subject=%s candidate_enabled=%s",
        record.get("subject"), editor_provider is not None,
    )
    existing = record.get("qualitative_review") or {}
    resume_diagnosis = (
        existing.get("state") == "DIAGNOSIS_COMPLETE"
        and editor_provider is not None
    )
    if existing.get("state") in {
        "NO_ELIGIBLE_FINDINGS",
        "CANDIDATE_READY_FOR_REVIEW",
        "CANDIDATE_REJECTED",
        "CANDIDATE_NO_CHANGE",
    } or (
        existing.get("state") == "DIAGNOSIS_COMPLETE"
        and not resume_diagnosis
    ):
        return
    subject = record["subject"]
    baseline_path = Path(record["deck"])
    deck = load_json(baseline_path)
    final_root = run_dir / "final" / subject
    qualitative_root = final_root / "qualitative"
    critic_root = qualitative_root / "critic"
    review = existing if resume_diagnosis else {
        "state": "CRITIC_SUBMITTED",
        "started_at": utc_now(),
        "finished_at": None,
        "baseline_deck": normalized_path(baseline_path),
        "baseline_sha256": sha256_file(baseline_path),
        "critic": None,
        "selection": None,
        "candidate": None,
        "error": None,
    }
    record["qualitative_review"] = review
    try:
        if resume_diagnosis:
            selection = validate_critic_findings_artifact(
                load_json(Path(review["critic"]["artifact"]))
            )
            review["state"] = "CANDIDATE_SUBMITTED"
            review["finished_at"] = None
            review["error"] = None
        else:
            transport = qualitative_critic_transport(deck)
            system = (
                "You are a read-only senior editorial critic for an AstroWoof "
                "natal claim deck. Diagnose only substantive, reader-visible "
                "quality problems; do not rewrite prose, invent defects to fill "
                "the quota, or penalize intentional recurring characterization. "
                "Distinguish lexical difference from conceptual difference. "
                "Exact paths must come from the supplied reader-facing field "
                "map. Prefer a small number of concrete, comparative findings "
                "over generic advice. Report the root editorial cause rather "
                "than separately counting its obvious headline, body, or joke "
                "symptoms unless those symptoms require materially different "
                "repair decisions. Classify missing conception as "
                "upstream_reconception rather than pretending it is safely "
                "editable."
            )
            user = (
                f"Review the complete AstroWoof deck for {subject}. Look "
                "specifically for overlapping summary theses, repeated comic "
                "machinery or rhetorical posture, exchangeable headlines, "
                "bodies whose explanation outlives their insight, incomplete "
                "compound meaning, insufficiently distinct audiences, and weak "
                "astrology-density progression. Return at most "
                f"{max_findings} findings, ordered by priority and confidence, "
                "and no replacement prose. Empty findings are correct when the "
                "deck does not contain a sufficiently specific defect.\n\n"
                "READ-ONLY DECK:\n"
                f"{json.dumps(transport, ensure_ascii=False)}"
            )
            before_submit = provider_created = None
            if spend_controller is not None:
                before_submit, provider_created = spend_controller.callbacks(
                    stage="qualitative_critic",
                    route=f"{subject}:qualitative-critic",
                    model=critic_provider.model,
                    service_level="interactive",
                    maximum_output_tokens=critic_provider.max_output_tokens,
                )
            response, metadata = critic_provider.complete_json(
                system=system,
                user=user,
                schema=qualitative_critic_output_schema(max_findings),
                schema_name="astrowoof_qualitative_critic",
                attempt_root=critic_root,
                idempotency_material=(
                    f"{sha256_file(baseline_path)}:{subject}:"
                    f"qualitative-critic:{max_findings}:"
                    f"{critic_provider.model}"
                ),
                before_submit=before_submit,
                provider_created=provider_created,
            )
            if spend_controller is not None:
                spend_controller.settle_active(metadata)
            metadata["routing"] = {
                "route": "qualitative_critic",
                "model": critic_provider.model,
                "reasoning_effort": critic_provider.reasoning_effort,
            }
            selection = validate_qualitative_critic_response(
                deck,
                response,
                max_findings=max_findings,
                max_target_fields=max_target_fields,
                max_target_cards=max_target_cards,
            )
            response_path = critic_root / "openai-response.json"
            if not response_path.is_file():
                response_path = critic_root / "critic-provider-response.json"
                write_json_atomic(response_path, response)
            selection = critic_findings_artifact(
                selection,
                run_dir=run_dir,
                deck_path=baseline_path,
                response_path=response_path,
                metadata=metadata,
                run_state=run_state,
            )
            validate_critic_findings_artifact(selection)
            write_json_atomic(critic_root / "critic-findings.json", selection)
            review["critic"] = {
                "provider_metadata": metadata,
                "finding_count": len(response.get("findings", [])),
                "artifact": normalized_path(
                    critic_root / "critic-findings.json"
                ),
            }
            review["selection"] = {
                "eligible_finding_count": len(selection["eligible_findings"]),
                "selected_target_paths": selection["selected_target_paths"],
                "selected_location_count": selection["selected_location_count"],
                "limits": selection["limits"],
            }
        targets = selection["selected_target_paths"]
        if not targets:
            review["state"] = "NO_ELIGIBLE_FINDINGS"
            review["finished_at"] = utc_now()
            return
        if editor_provider is None:
            review["state"] = "DIAGNOSIS_COMPLETE"
            review["finished_at"] = utc_now()
            return

        editor_root = qualitative_root / "candidate"
        all_fields = editable_deck_fields(deck, include_theme_groups=False)
        comparison_paths = sorted({
            path
            for finding in selection["eligible_findings"]
            for path in finding.get("comparison_paths", [])
        })
        read_only_paths = sorted(set(comparison_paths) - set(targets))
        nearby = sparse_polish_context(deck, targets)
        nearby.update({path: all_fields[path] for path in read_only_paths})
        required_context = {
            value
            for finding in selection["eligible_findings"]
            for value in finding.get("required_context", [])
        }
        repair_basis = sparse_polish_basis(deck, targets)
        whole_deck = (
            qualitative_whole_deck_context(deck)
            if "whole_chart" in required_context
            else None
        )
        editor_system = (
            "You are producing a bounded qualitative-polish candidate for "
            "human comparison. Edit only the supplied target paths and only "
            "when the critic diagnosis supports a real improvement. Omit a "
            "target rather than weakening good prose. Preserve factual meaning, "
            "the strongest image, behavioral specificity, useful guidance, "
            "audience purpose, astrology-density role, and compound semantic "
            "contributions. Do not normalize the deck into one writing style."
        )
        editor_user = (
            f"Prepare a sparse candidate for {subject}. The production deck "
            "will not be replaced automatically.\n\nCRITIC FINDINGS:\n"
            f"{json.dumps(selection['eligible_findings'], ensure_ascii=False)}"
            "\n\nEDITABLE TARGETS:\n"
            f"{json.dumps({path: all_fields[path] for path in targets}, ensure_ascii=False)}"
            "\n\nREAD-ONLY COMPARISON AND NEARBY PROSE:\n"
            f"{json.dumps(nearby, ensure_ascii=False)}"
            "\n\nSEMANTIC REPAIR BASIS:\n"
            f"{json.dumps(repair_basis, ensure_ascii=False)}"
            "\n\nOPTIONAL WHOLE-DECK BEHAVIORAL CONTEXT:\n"
            f"{json.dumps(whole_deck, ensure_ascii=False)}"
        )
        before_submit = provider_created = None
        if spend_controller is not None:
            before_submit, provider_created = spend_controller.callbacks(
                stage="qualitative_candidate",
                route=f"{subject}:qualitative-candidate",
                model=editor_provider.model,
                service_level="interactive",
                maximum_output_tokens=editor_provider.max_output_tokens,
            )
        authored, editor_metadata = editor_provider.complete_json(
            system=editor_system,
            user=editor_user,
            schema=sparse_polish_output_schema(targets),
            schema_name="astrowoof_qualitative_candidate",
            attempt_root=editor_root,
            idempotency_material=(
                f"{sha256_file(baseline_path)}:{subject}:qualitative-candidate:"
                f"{sha256_file(critic_root / 'critic-findings.json')}:"
                f"{editor_provider.model}"
            ),
            before_submit=before_submit,
            provider_created=provider_created,
        )
        if spend_controller is not None:
            spend_controller.settle_active(editor_metadata)
        editor_metadata["routing"] = {
            "route": "qualitative_candidate",
            "model": editor_provider.model,
            "reasoning_effort": editor_provider.reasoning_effort,
        }
        if not authored.get("edits"):
            review["candidate"] = {
                "provider_metadata": editor_metadata,
                "artifact": None,
                "edited_field_count": 0,
                "omitted_target_count": len(targets),
                "production_deck_replaced": False,
                "requires_human_review": False,
            }
            review["state"] = "CANDIDATE_NO_CHANGE"
            review["finished_at"] = utc_now()
            return
        candidate = apply_sparse_polish(
            deck,
            authored,
            target_paths=targets,
            include_theme_groups=False,
        )
        candidate_path = editor_root / f"natal.{subject}.cards.candidate.json"
        write_json_atomic(candidate_path, candidate)
        validator_path = Path(validation_module.__file__).resolve()
        linter_path = Path(editorial_lint_module.__file__).resolve()
        validation_path = editor_root / "validation-report.json"
        validation_command = [
            str(python_executable),
            str(validator_path),
            str(baseline_path),
            str(candidate_path),
            "--phase",
            "polish",
            "--report",
            str(validation_path),
        ]
        if any(path.startswith("summary.") for path in targets):
            validation_command.append("--allow-summary-edits")
        validation = run_json_command(
            validation_command,
            validation_path,
            accepted_returncodes={0},
        )
        lint_path = editor_root / "lint-report.json"
        lint = run_json_command(
            [
                str(python_executable),
                str(linter_path),
                str(candidate_path),
                "--output",
                str(lint_path),
            ],
            lint_path,
            accepted_returncodes={0, 2},
        )
        baseline_lint_count = lint_finding_count(
            load_json(Path(record["lint_report"]))
        )
        candidate_lint_count = lint_finding_count(lint["report"])
        structurally_valid = validation["accepted"]
        mechanically_nonworsening = candidate_lint_count <= baseline_lint_count
        review["candidate"] = {
            "provider_metadata": editor_metadata,
            "artifact": normalized_path(candidate_path),
            "validation_report": normalized_path(validation_path),
            "lint_report": normalized_path(lint_path),
            "edited_field_count": len(authored.get("edits", [])),
            "omitted_target_count": len(targets) - len(authored.get("edits", [])),
            "structurally_valid": structurally_valid,
            "baseline_lint_finding_count": baseline_lint_count,
            "candidate_lint_finding_count": candidate_lint_count,
            "mechanically_nonworsening": mechanically_nonworsening,
            "production_deck_replaced": False,
            "requires_human_review": True,
        }
        review["state"] = (
            "CANDIDATE_READY_FOR_REVIEW"
            if structurally_valid and mechanically_nonworsening
            else "CANDIDATE_REJECTED"
        )
        review["finished_at"] = utc_now()
    except Exception as exc:
        if isinstance(exc, AwaitingSpendAuthorization):
            raise
        if isinstance(exc, (BudgetExhausted, AmbiguousProviderSubmission)):
            action_state = (exc.action or {}).get("state")
            if action_state == "SKIPPED_BUDGET_EXHAUSTED":
                review["state"] = "QUALITATIVE_SKIPPED_BUDGET_EXHAUSTED"
                review["finished_at"] = utc_now()
                review["paid_action_id"] = (exc.action or {}).get("action_id")
                return
            raise
        review["state"] = "QUALITATIVE_REVIEW_ERROR"
        review["finished_at"] = utc_now()
        review["error"] = {
            "type": type(exc).__name__,
            "message": str(exc),
            "provider_metadata": getattr(exc, "metadata", None),
        }
        logger.exception(
            "qualitative_review_error subject=%s error_class=%s error=%s",
            record.get("subject"), type(exc).__name__,
            sanitize_error_message(str(exc)),
        )
        if getattr(exc, "fatal", False):
            raise


def finalize_subjects(
    *,
    state: dict[str, Any],
    run_dir: Path,
    python_executable: Path,
    allow_lint_warnings: bool,
    polish: bool = False,
    polish_provider: OpenAIResponsesProvider | None = None,
    max_polish_attempts: int = 2,
    spend_controller: SpendController | None = None,
) -> None:
    """Assemble and validate every subject after authoring completes."""
    if any(
        record["state"] != "PASS_QA_ACCEPTED"
        for record in state["passes"].values()
    ):
        logger.info("finalization_deferred reason=authoring_passes_incomplete")
        return
    logger.info(
        "finalization_start subject_count=%s polish=%s allow_lint_warnings=%s",
        len(subject_records(state)), polish, allow_lint_warnings,
    )
    finals = state.setdefault("subjects", {})
    for subject in sorted(subject_records(state)):
        record = finals.get(subject)
        if record and record.get("state") in FINAL_SUCCESS_STATES:
            continue
        if not record or record.get("state") not in {
            "FINAL_QA_WARN",
            "FINAL_QA_FAILED",
        }:
            record = assemble_subject(
                state=state,
                subject=subject,
                run_dir=run_dir,
                python_executable=python_executable,
            )
            finals[subject] = record
        if record["state"] == "FINAL_QA_PASSED":
            record["state"] = "DELIVERY_COMPLETE"
            package_subject_delivery(record, run_dir=run_dir)
        elif (
            record["state"] in {"FINAL_QA_WARN", "FINAL_QA_FAILED"}
            and polish
            and polish_provider is not None
        ):
            polish_subject(
                record=record,
                provider=polish_provider,
                run_dir=run_dir,
                python_executable=python_executable,
                max_attempts=max_polish_attempts,
                spend_controller=spend_controller,
            )
            if record["state"] == "FINAL_QA_WARN" and allow_lint_warnings:
                record["state"] = "DELIVERY_COMPLETE_WITH_WARNINGS"
                package_subject_delivery(record, run_dir=run_dir)
        elif record["state"] == "FINAL_QA_WARN" and allow_lint_warnings:
            record["state"] = "DELIVERY_COMPLETE_WITH_WARNINGS"
            package_subject_delivery(record, run_dir=run_dir)
        finals[subject] = record
        logger.info(
            "subject_finalization_complete subject=%s final_state=%s",
            subject, record.get("state"),
        )


def create_run(
    *,
    input_package: Path,
    run_dir: Path,
    subject: str | None,
    provider: AuthoringProvider,
    max_attempts: int,
    sbe_script: Path | None,
    python_executable: Path,
    service_level: str = "interactive",
    split_assignment_policy: str = "stratified-v1",
    full_chart_basis_format: str = "legacy",
    exact_natal_policy: str = LEGACY_ATOMIC_POLICY_ID,
    profile: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], Path]:
    if run_dir.exists() and any(run_dir.iterdir()):
        raise FileExistsError(
            f"Run directory is not empty: {run_dir}. Use --resume to continue it."
        )
    run_dir.mkdir(parents=True, exist_ok=True)
    _subjects, input_contract = discover_projected_input(input_package, subject)
    sbe_root = run_dir / "sbe"
    output_dir = sbe_root / "semantic-basis-output"
    bundle_dir = sbe_root / "llm-handoff-bundle"
    sbe_manifest = run_sbe(
        input_package=input_package,
        subject=subject,
        sbe_script=sbe_script,
        python_executable=python_executable,
        output_dir=output_dir,
        bundle_dir=bundle_dir,
        split_assignment_policy=split_assignment_policy,
        full_chart_basis_format=full_chart_basis_format,
        exact_natal_policy=exact_natal_policy,
    )
    specs = discover_passes(sbe_manifest, bundle_dir)
    state = initial_run_state(
        input_package=input_package,
        run_dir=run_dir,
        provider=provider,
        max_attempts=max_attempts,
        sbe_manifest=sbe_manifest,
        specs=specs,
        service_level=service_level,
        input_contract=input_contract,
        profile=profile,
    )
    state["provenance"] = initial_provenance(
        input_root=input_package.resolve(),
        input_contract=input_contract,
        authoring_profile=profile,
    )
    state["prompt_cache"] = prompt_cache_manifest(specs)
    run_json = run_dir / "run.json"
    save_state(run_json, state)
    return state, run_json


def resume_run(
    *,
    run_dir: Path,
    provider: AuthoringProvider,
    max_attempts: int,
    service_level: str = "interactive",
) -> tuple[dict[str, Any], Path]:
    run_json = run_dir / "run.json"
    if not run_json.is_file():
        raise FileNotFoundError(f"Cannot resume without {run_json}")
    state = load_json(run_json)
    previous_schema = state.get("schema_version")
    if previous_schema == SCHEMA_VERSION:
        validate_workspace_snapshot(run_dir, state)
    if (
        previous_schema != SCHEMA_VERSION
        and getattr(provider, "name", None) == "openai"
    ):
        raise ValueError(
            "Legacy OpenAI runs cannot resume paid work without a v0.9 spend "
            "ledger and complete workspace snapshot; reconcile or migrate them "
            "explicitly before execution"
        )
    if previous_schema in {
        "astrowoof.semantic_closure_run.v0.2",
        "astrowoof.semantic_closure_run.v0.3",
        "astrowoof.semantic_closure_run.v0.4",
        "astrowoof.semantic_closure_run.v0.5",
        "astrowoof.semantic_closure_run.v0.6",
        "astrowoof.semantic_closure_run.v0.7",
        "astrowoof.semantic_closure_run.v0.8",
    }:
        state["schema_version"] = SCHEMA_VERSION
        state.setdefault("service_level", "interactive")
        state.setdefault("subjects", {})
        state.setdefault("input_contract", None)
        state.setdefault("authoring_profile", None)
        state.setdefault(
            "provenance",
            migrated_run_provenance(
                previous_schema=previous_schema,
                authoring_profile=state.get("authoring_profile"),
            ),
        )
        configuration = state.setdefault("provider_configuration", {})
        if getattr(provider, "name", None) == "openai":
            configuration.setdefault(
                "prompt_cache_mode", provider.prompt_cache_mode
            )
            configuration.setdefault(
                "prompt_cache_ttl", provider.prompt_cache_ttl
            )
    if state.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported run schema: {state.get('schema_version')!r}"
        )
    if state.get("provider") != provider.name:
        raise ValueError(
            f"Run provider is {state.get('provider')!r}, not {provider.name!r}"
        )
    if state.get("service_level", "interactive") != service_level:
        raise ValueError(
            "Resume must use the original service level "
            f"({state.get('service_level', 'interactive')!r})"
        )
    if state.get("provider_configuration", {}) != provider_configuration(
        provider
    ):
        raise ValueError(
            "Resume must use the original provider configuration "
            f"({state.get('provider_configuration', {})})"
        )
    if state.get("max_attempts") != max_attempts:
        raise ValueError(
            "Resume must use the original --max-attempts value "
            f"({state.get('max_attempts')})"
        )
    normalized_acceptance = False
    for record in state.get("passes", {}).values():
        accepted_attempt = record.get("accepted_attempt")
        accepted_workspace = record.get("accepted_workspace")
        if not accepted_attempt or not accepted_workspace:
            continue
        matching = next(
            (
                attempt
                for attempt in record.get("attempts", [])
                if attempt.get("attempt_number") == accepted_attempt
            ),
            None,
        )
        acceptance_evidence = bool(
            matching
            and (
                matching.get("state") == "PASS_QA_ACCEPTED"
                or matching.get("accepted") is True
                or (matching.get("qa") or {}).get("accepted") is True
            )
        )
        if acceptance_evidence and Path(accepted_workspace).is_dir():
            if record.get("state") != "PASS_QA_ACCEPTED":
                record["state"] = "PASS_QA_ACCEPTED"
                normalized_acceptance = True
            if matching.get("state") != "PASS_QA_ACCEPTED":
                matching["state"] = "PASS_QA_ACCEPTED"
                normalized_acceptance = True
    if normalized_acceptance:
        save_state(run_json, state)
    return state, run_json


def default_sbe_script() -> Path | None:
    """Use a source-tree shim when present, otherwise the installed module."""
    candidate = Path(__file__).resolve().parent.parent / "build_projected_semantic_basis.py"
    return candidate if candidate.is_file() else None


def build_prompt_layout_report(
    *,
    state: dict[str, Any],
    run_dir: Path,
    provider: OpenAIResponsesProvider,
) -> dict[str, Any]:
    """Measure every authoring prompt without submitting a response."""
    layouts: list[dict[str, Any]] = []
    inventories: dict[str, list[dict[str, Any]]] = {}
    with tempfile.TemporaryDirectory(prefix="astrowoof-prompt-layout-") as temp:
        root = Path(temp)
        for spec in specs_from_state(state):
            extracted = root / spec.pass_id
            safe_extract_zip(spec.source_zip, extracted)
            workspace = find_workspace_root(extracted, spec.pass_id)
            inventories[spec.pass_id] = workspace_file_inventory(workspace)
            layouts.append(
                provider.prompt_layout(spec=spec, workspace=workspace)
            )
    segment_hashes: dict[str, dict[str, int]] = {}
    for layout in layouts:
        for name, measurement in layout["segments"].items():
            hashes = segment_hashes.setdefault(name, {})
            digest = measurement["sha256"]
            hashes[digest] = hashes.get(digest, 0) + 1
    content_occurrences: dict[str, dict[str, Any]] = {}
    for pass_id, files in inventories.items():
        for file in files:
            entry = content_occurrences.setdefault(
                file["sha256"],
                {
                    "utf8_bytes": file["utf8_bytes"],
                    "estimated_tokens": file["estimated_tokens"],
                    "locations": [],
                },
            )
            entry["locations"].append(f"{pass_id}/{file['path']}")
    duplicate_tokens = sum(
        entry["estimated_tokens"] * (len(entry["locations"]) - 1)
        for entry in content_occurrences.values()
        if len(entry["locations"]) > 1
    )
    return {
        "schema_version": "astrowoof.prompt_layout_report.v1",
        "created_at": utc_now(),
        "run_dir": normalized_path(run_dir),
        "model": provider.model,
        "token_estimate_method": TOKEN_ESTIMATE_METHOD,
        "pass_count": len(layouts),
        "request_estimated_tokens": sum(
            item["request_estimated_tokens"] for item in layouts
        ),
        "segments": {
            name: {
                "distinct_sha256_count": len(hashes),
                "shared_by_all_passes": len(hashes) == 1,
                "occurrences_by_sha256": hashes,
            }
            for name, hashes in segment_hashes.items()
        },
        "passes": layouts,
        "file_inventory": {
            "passes": inventories,
            "exact_duplicate_estimated_tokens": duplicate_tokens,
            "repeated_content": [
                {"sha256": digest, **entry}
                for digest, entry in sorted(content_occurrences.items())
                if len(entry["locations"]) > 1
            ],
        },
        "note": (
            "This report performs no API request. Estimates support relative "
            "prompt-layout comparisons; response usage remains authoritative."
        ),
    }


def accounting_from_run(path: Path) -> dict[str, Any]:
    state = load_json(path)
    update_run_status(state)
    return state.get("accounting", {})


def compare_cost_runs(baseline_path: Path, candidate_path: Path) -> dict[str, Any]:
    """Compare two persisted runs using their response-level accounting."""
    baseline = accounting_from_run(baseline_path)
    candidate = accounting_from_run(candidate_path)
    baseline_amount = float(
        (baseline.get("estimated_cost") or {}).get("estimated_amount") or 0
    )
    candidate_amount = float(
        (candidate.get("estimated_cost") or {}).get("estimated_amount") or 0
    )
    savings = baseline_amount - candidate_amount
    baseline_usage = baseline.get("usage") or {}
    candidate_usage = candidate.get("usage") or {}
    return {
        "schema_version": "astrowoof.cost_comparison.v1",
        "created_at": utc_now(),
        "baseline": {
            "run_json": normalized_path(baseline_path),
            "accounting": baseline,
        },
        "candidate": {
            "run_json": normalized_path(candidate_path),
            "accounting": candidate,
        },
        "difference": {
            "estimated_cost_usd": round(candidate_amount - baseline_amount, 8),
            "estimated_savings_usd": round(savings, 8),
            "estimated_savings_ratio": round(savings / baseline_amount, 6)
            if baseline_amount
            else None,
            "usage": {
                key: int(candidate_usage.get(key) or 0)
                - int(baseline_usage.get(key) or 0)
                for key in {
                    *baseline_usage.keys(),
                    *candidate_usage.keys(),
                }
            },
        },
    }


def directory_size(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def verified_zip(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Required retained ZIP is missing: {path}")
    with zipfile.ZipFile(path) as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise ValueError(f"Corrupt retained ZIP member in {path}: {bad_member}")


def cleanup_completed_run(run_dir: Path, *, dry_run: bool) -> dict[str, Any]:
    """Remove only reconstructable expanded copies from a completed run."""
    run_dir = run_dir.resolve()
    run_json = run_dir / "run.json"
    if not run_json.is_file():
        raise FileNotFoundError(f"Completed-run cleanup requires {run_json}")
    state = load_json(run_json)
    if state.get("status") not in FINAL_SUCCESS_STATES:
        raise ValueError(
            "Completed-run cleanup refuses nonterminal run state "
            f"{state.get('status')!r}."
        )
    subjects = state.get("subjects") or {}
    if not subjects or any(
        record.get("state") not in FINAL_SUCCESS_STATES
        for record in subjects.values()
    ):
        raise ValueError(
            "Completed-run cleanup requires every subject delivery to be complete."
        )

    retained: list[str] = ["run.json", "public-run.json"]
    for subject, record in subjects.items():
        for key in (
            "deck", "assembly_report", "validation_report", "lint_report",
        ):
            path = Path(record.get(key, ""))
            if not path.is_file():
                raise FileNotFoundError(
                    f"Completed {subject} is missing retained {key}: {path}"
                )
            retained.append(normalized_path(path))
        delivery = Path(record.get("delivery", ""))
        verified_zip(delivery)
        retained.append(normalized_path(delivery))

    for record in state.get("passes", {}).values():
        accepted = Path(record.get("accepted_workspace", ""))
        if not accepted.is_dir():
            raise FileNotFoundError(
                f"Completed pass is missing accepted workspace: {accepted}"
            )
        source_zip = Path(record.get("source_zip", ""))
        verified_zip(source_zip)
        retained.extend((normalized_path(accepted), normalized_path(source_zip)))

    candidates: list[tuple[Path, str]] = []
    bundle = run_dir / "sbe" / "llm-handoff-bundle"
    if bundle.is_dir():
        for expanded in sorted(path for path in bundle.iterdir() if path.is_dir()):
            verified_zip(expanded.with_suffix(".zip"))
            candidates.append((expanded, "expanded_sbe_pass_copy"))
    passes_root = run_dir / "passes"
    if passes_root.is_dir():
        for pass_root in sorted(path for path in passes_root.iterdir() if path.is_dir()):
            source = pass_root / "source"
            if source.is_dir():
                candidates.append((source, "expanded_attempt_source"))
            for response in sorted(pass_root.glob("attempt-*/response")):
                if response.is_dir():
                    candidates.append((response, "reconstructable_response_workspace"))
    final_root = run_dir / "final"
    if final_root.is_dir():
        for duplicate in sorted(final_root.glob("*/accepted-passes")):
            if duplicate.is_dir():
                candidates.append((duplicate, "duplicate_final_accepted_passes"))

    targets: list[dict[str, Any]] = []
    seen: set[Path] = set()
    for path, reason in candidates:
        resolved = path.resolve()
        try:
            relative = resolved.relative_to(run_dir)
        except ValueError as exc:
            raise ValueError(f"Cleanup target escapes run directory: {resolved}") from exc
        if resolved in seen:
            continue
        seen.add(resolved)
        targets.append({
            "path": str(relative).replace("\\", "/"),
            "reason": reason,
            "bytes": directory_size(resolved),
        })

    report = {
        "schema_version": "astrowoof.completed_run_cleanup.v1",
        "status": "dry_run" if dry_run else "complete",
        "run_dir": normalized_path(run_dir),
        "run_status": state["status"],
        "target_count": len(targets),
        "reclaimed_bytes": sum(item["bytes"] for item in targets),
        "targets": targets,
        "retained": sorted(set(retained)),
        "retention_policy": {
            "accepted_pass_workspaces": "retained",
            "source_pass_archives": "retained_and_integrity_checked",
            "request_response_and_batch_evidence": "retained",
            "final_delivery_and_qa": "retained_and_integrity_checked",
            "expanded_reconstructable_copies": "removed",
        },
    }
    if not dry_run:
        for item in targets:
            shutil.rmtree(run_dir / Path(item["path"]))
        write_json_atomic(run_dir / "cleanup-report.json", report)
        write_workspace_snapshot(run_dir)
    return report


def profile_from_args(args: argparse.Namespace) -> dict[str, Any]:
    """Freeze behavior-affecting run options into a versioned profile."""
    return authoring_profile(
        extraction={
            "handoff_profile": "authoring-workspace",
            "workspace_layout": "split",
            "workspace_card_limit": 50,
            "pass_count": PASS_COUNT,
            "split_assignment_policy": args.split_assignment_policy,
            "full_chart_basis_format": args.full_chart_basis_format,
            "exact_natal_policy": args.exact_natal_policy,
        },
        authoring={
            "provider": args.provider,
            "service_level": args.service_level,
            "routing_policy": args.routing_policy,
            "model": args.model,
            "reasoning_effort": args.reasoning_effort,
            "retry_model": args.retry_model,
            "retry_reasoning_effort": args.retry_reasoning_effort,
            "max_attempts": args.max_attempts,
            "max_workers": args.max_workers,
            "max_output_tokens": args.max_output_tokens,
            "prompt_cache_mode": args.prompt_cache_mode,
            "prompt_cache_ttl": args.prompt_cache_ttl,
        },
        qa={
            "allow_lint_warnings": args.allow_lint_warnings,
            "polish": args.polish,
            "max_polish_attempts": args.max_polish_attempts,
            "polish_model": args.polish_model,
            "polish_reasoning_effort": args.polish_reasoning_effort,
            "qualitative_critic": args.qualitative_critic,
            "qualitative_candidate": args.qualitative_candidate,
        },
        spend_policy=(
            validate_policy(getattr(args, "spend_policy_value", None))
            if args.provider == "openai"
            else None
        ),
    )


def apply_spend_authorizations(
    state: dict[str, Any], documents: list[dict[str, Any]]
) -> list[str]:
    ledger = state.get("spend_ledger")
    if not isinstance(ledger, dict):
        raise ValueError("Run has no spend ledger to authorize")
    applied = []
    for document in documents:
        action = authorize_action(ledger, document)
        applied.append(action["action_id"])
    return applied


def apply_spend_reconciliations(
    state: dict[str, Any], documents: list[dict[str, Any]]
) -> list[str]:
    ledger = state.get("spend_ledger")
    if not isinstance(ledger, dict):
        raise ValueError("Run has no spend ledger to reconcile")
    applied = []
    for document in documents:
        if document.get("schema_version") != "astrowoof.provider_spend_reconciliation.v0.1":
            raise ValueError("Unsupported spend reconciliation schema")
        record = append_reconciliation_reference(
            ledger,
            action_id=document["action_id"],
            reference_id=document["reference_id"],
            authority=document["authority"],
            amount_micro_usd=document.get("amount_micro_usd"),
        )
        applied.append(record["reference_id"])
    return applied


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run the AstroWoof semantic-closure extraction and authoring "
            "workflow."
        )
    )
    parser.add_argument("--input-package", type=Path)
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--subject")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--provider-reconciliation-cycle",
        action="store_true",
        help=(
            "Retrieve one bounded due cycle of already-known provider work, "
            "exhaust route-local work, checkpoint, and detach without submission."
        ),
    )
    parser.add_argument(
        "--observed-at",
        help="Frozen UTC decision instant for --provider-reconciliation-cycle.",
    )
    parser.add_argument(
        "--bounded-provider-reconciliation",
        action="store_true",
        help=(
            "Deprecated exact-interactive alias for "
            "--provider-reconciliation-cycle. It does not select bounded Natal."
        ),
    )
    parser.add_argument(
        "--events-jsonl",
        type=Path,
        help=(
            "Append typed non-authoritative execution events to a JSONL file "
            "outside the authoritative run workspace."
        ),
    )
    parser.add_argument(
        "--events-stdout-jsonl",
        action="store_true",
        help=(
            "Emit typed event envelopes and one final typed result envelope as "
            "JSONL on stdout; human diagnostics remain on stderr."
        ),
    )
    parser.add_argument(
        "--spend-policy",
        type=Path,
        help=(
            "Required for new OpenAI runs. JSON policy with explicit run and "
            "per-stage micro-USD ceilings, price book, and optional-stage behavior."
        ),
    )
    parser.add_argument(
        "--spend-authorization",
        action="append",
        type=Path,
        default=[],
        help=(
            "Apply an external authorization envelope for one exact prepared "
            "paid action. May be repeated."
        ),
    )
    parser.add_argument(
        "--initial-wave-authorization",
        type=Path,
        help=(
            "Apply the one exact six-member initial-wave authorization envelope; "
            "requires six ordered --spend-authorization documents."
        ),
    )
    parser.add_argument(
        "--external-authority-request", type=Path,
        help="Exact snapshot-bound request for constrained provider-capable resume.",
    )
    parser.add_argument(
        "--external-authority-grant", type=Path,
        help="All-or-none API grant bound to --external-authority-request.",
    )
    parser.add_argument(
        "--spend-reconciliation",
        action="append",
        type=Path,
        default=[],
        help="Append an API-owned billing/reconciliation reference; may repeat.",
    )
    parser.add_argument(
        "--prompt-layout-report",
        type=Path,
        help="Write a token-free report of the generated authoring prompts.",
    )
    parser.add_argument(
        "--compare-cost-runs",
        nargs=2,
        type=Path,
        metavar=("BASELINE_RUN_JSON", "CANDIDATE_RUN_JSON"),
        help="Compare persisted token usage and estimated cost, then exit.",
    )
    parser.add_argument(
        "--cost-report-output",
        type=Path,
        help="Also persist the --compare-cost-runs report as JSON.",
    )
    parser.add_argument(
        "--cleanup-completed-run",
        type=Path,
        help=(
            "Remove only reconstructable expanded directory copies from a "
            "completed run, then write cleanup-report.json."
        ),
    )
    parser.add_argument(
        "--cleanup-dry-run",
        action="store_true",
        help="Report completed-run cleanup targets without deleting them.",
    )
    parser.add_argument(
        "--provider",
        choices=("fake", "openai"),
        default="fake",
    )
    parser.add_argument(
        "--service-level",
        choices=("interactive", "batch"),
        default="interactive",
        help=(
            "Use direct Responses calls or model-homogeneous asynchronous "
            "Batch API rounds. Batch is OpenAI-only and half-price."
        ),
    )
    parser.add_argument(
        "--batch-detach",
        action="store_true",
        help=(
            "Submit or refresh one Batch round, persist its IDs, and exit "
            "without waiting. Resume the same run later to ingest results."
        ),
    )
    parser.add_argument(
        "--batch-poll-interval-seconds",
        type=float,
        default=30.0,
    )
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument(
        "--split-assignment-policy",
        choices=("contiguous", "stratified-v1"),
        default="stratified-v1",
        help=(
            "Deterministic card-to-pass assignment used by the SBE stage. "
            "Use contiguous for the historical control."
        ),
    )
    parser.add_argument(
        "--full-chart-basis-format",
        choices=("legacy", "compact-v1", "compact-v2"),
        default="legacy",
        help=(
            "Full-chart authoring transport generated by SBE. compact-v1 and "
            "compact-v2 are experimental; legacy remains the production default."
        ),
    )
    parser.add_argument(
        "--exact-natal-policy",
        choices=(LEGACY_ATOMIC_POLICY_ID, AXIS_AWARE_POLICY_ID),
        default=LEGACY_ATOMIC_POLICY_ID,
        help=(
            "Exact-Natal basis policy. axis_aware.v1 is experimental; "
            "legacy_atomic.v1 remains the production default."
        ),
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=6,
        help="Maximum number of independent passes authored concurrently.",
    )
    parser.add_argument(
        "--model",
        help=(
            "Initial authoring model. Defaults to Terra for fixed routing and "
            "Luna for cost-optimized routing."
        ),
    )
    parser.add_argument(
        "--reasoning-effort",
        choices=("none", "low", "medium", "high", "xhigh", "max"),
        default="medium",
    )
    parser.add_argument(
        "--routing-policy",
        choices=("fixed", "cost_optimized"),
        default="fixed",
    )
    parser.add_argument("--retry-model", default="gpt-5.6-terra")
    parser.add_argument(
        "--retry-reasoning-effort",
        choices=("none", "low", "medium", "high", "xhigh", "max"),
        default="medium",
    )
    parser.add_argument("--polish-model", default="gpt-5.6-luna")
    parser.add_argument(
        "--polish-reasoning-effort",
        choices=("none", "low", "medium", "high", "xhigh", "max"),
        default="low",
    )
    parser.add_argument(
        "--api-key-env",
        default="OPENAI_API_KEY",
        help="Environment variable containing the OpenAI API key.",
    )
    parser.add_argument(
        "--openai-base-url",
        default="https://api.openai.com/v1",
    )
    parser.add_argument("--foreground", action="store_true")
    parser.add_argument("--poll-interval-seconds", type=float, default=2.0)
    parser.add_argument("--response-timeout-seconds", type=float, default=1800.0)
    parser.add_argument("--http-timeout-seconds", type=float, default=60.0)
    parser.add_argument("--max-transport-retries", type=int, default=4)
    parser.add_argument(
        "--transport-backoff-seconds",
        type=float,
        default=1.0,
    )
    parser.add_argument("--max-output-tokens", type=int, default=100_000)
    parser.add_argument(
        "--prompt-cache-mode",
        choices=("disabled", "implicit", "explicit"),
        default="explicit",
        help=(
            "Prompt-cache policy for GPT-5.6 authoring calls. Explicit mode "
            "uses stable static and subject breakpoints."
        ),
    )
    parser.add_argument(
        "--prompt-cache-ttl",
        choices=("30m",),
        default="30m",
    )
    parser.add_argument(
        "--polish",
        action="store_true",
        help=(
            "Run up to --max-polish-attempts whole-deck surgical polish "
            "attempts when final lint reports warnings (OpenAI provider only)."
        ),
    )
    parser.add_argument("--max-polish-attempts", type=int, default=2)
    parser.add_argument(
        "--qualitative-critic",
        action="store_true",
        help=(
            "Run an optional read-only whole-deck qualitative critic after "
            "final validation. Findings never replace the production deck."
        ),
    )
    parser.add_argument(
        "--qualitative-candidate",
        action="store_true",
        help=(
            "After qualitative diagnosis, author a capped sparse candidate "
            "for human comparison without replacing the production deck."
        ),
    )
    parser.add_argument("--critic-model", default="gpt-5.6-luna")
    parser.add_argument(
        "--critic-reasoning-effort",
        choices=("none", "low", "medium", "high", "xhigh", "max"),
        default="medium",
    )
    parser.add_argument("--qualitative-editor-model", default="gpt-5.6-luna")
    parser.add_argument(
        "--qualitative-editor-reasoning-effort",
        choices=("none", "low", "medium", "high", "xhigh", "max"),
        default="low",
    )
    parser.add_argument("--max-critic-findings", type=int, default=8)
    parser.add_argument("--max-qualitative-target-fields", type=int, default=12)
    parser.add_argument("--max-qualitative-target-cards", type=int, default=6)
    parser.add_argument(
        "--allow-lint-warnings",
        action="store_true",
        help="Package structurally valid decks even when final lint warns.",
    )
    parser.add_argument("--safety-identifier")
    parser.add_argument(
        "--sbe-script",
        type=Path,
        default=default_sbe_script(),
    )
    parser.add_argument(
        "--python-executable",
        type=Path,
        default=Path(sys.executable),
    )
    parser.add_argument(
        "--fake-reject",
        action="append",
        default=[],
        metavar="PASS_ID:COUNT",
        help="Make a fake pass fail QA COUNT times before succeeding.",
    )
    parser.add_argument(
        "--fake-error",
        action="append",
        default=[],
        metavar="PASS_ID:COUNT",
        help="Make a fake pass raise COUNT provider errors before succeeding.",
    )
    add_logging_arguments(parser)
    args = parser.parse_args()
    configure_logging_from_args(args)
    logger.info("command_start command=semantic_closure")
    if args.events_jsonl is not None and args.events_stdout_jsonl:
        parser.error("choose only one of --events-jsonl and --events-stdout-jsonl")
    if args.events_stdout_jsonl and (args.compare_cost_runs or args.cleanup_completed_run):
        parser.error("--events-stdout-jsonl is supported for authoring commands")

    def output_result(value: dict[str, Any]) -> None:
        if args.events_stdout_jsonl:
            StdoutJsonlSink()(command_result_envelope(value))
        else:
            print(json.dumps(value, ensure_ascii=False, indent=2))
    args.spend_policy_value = (
        load_json(args.spend_policy) if args.spend_policy else None
    )
    args.model = args.model or (
        "gpt-5.6-luna"
        if args.routing_policy == "cost_optimized"
        else "gpt-5.6-terra"
    )
    if args.compare_cost_runs:
        report = compare_cost_runs(*args.compare_cost_runs)
        if args.cost_report_output:
            write_json_atomic(args.cost_report_output, report)
        output_result(report)
        return
    if args.cleanup_completed_run:
        report = cleanup_completed_run(
            args.cleanup_completed_run,
            dry_run=args.cleanup_dry_run,
        )
        output_result(report)
        return
    if args.cleanup_dry_run:
        parser.error("--cleanup-dry-run requires --cleanup-completed-run")
    if args.run_dir is None:
        parser.error("--run-dir is required for authoring and prompt reports")
    if args.events_jsonl is not None:
        event_path = args.events_jsonl.resolve()
        try:
            event_path.relative_to(args.run_dir.resolve())
        except ValueError:
            pass
        else:
            parser.error("--events-jsonl must be outside the authoritative run workspace")
    if args.max_attempts < 1:
        parser.error("--max-attempts must be at least 1")
    if args.max_workers < 1:
        parser.error("--max-workers must be at least 1")
    if args.max_transport_retries < 0:
        parser.error("--max-transport-retries cannot be negative")
    if args.max_output_tokens < 1:
        parser.error("--max-output-tokens must be at least 1")
    if args.max_polish_attempts < 1:
        parser.error("--max-polish-attempts must be at least 1")
    if args.max_critic_findings < 1:
        parser.error("--max-critic-findings must be at least 1")
    if args.max_qualitative_target_fields < 1:
        parser.error("--max-qualitative-target-fields must be at least 1")
    if args.max_qualitative_target_cards < 1:
        parser.error("--max-qualitative-target-cards must be at least 1")
    if args.polish and args.provider != "openai":
        parser.error("--polish requires --provider openai")
    if args.qualitative_candidate and not args.qualitative_critic:
        parser.error("--qualitative-candidate requires --qualitative-critic")
    if args.qualitative_critic and args.provider != "openai":
        parser.error("--qualitative-critic requires --provider openai")
    if args.service_level == "batch" and args.provider != "openai":
        parser.error("--service-level batch requires --provider openai")
    if args.batch_detach and args.service_level != "batch":
        parser.error("--batch-detach requires --service-level batch")
    reconciliation_cycle = bool(
        args.provider_reconciliation_cycle or args.bounded_provider_reconciliation
    )
    if args.provider_reconciliation_cycle and args.bounded_provider_reconciliation:
        parser.error("choose only one provider reconciliation spelling")
    if reconciliation_cycle and not args.resume:
        parser.error("provider reconciliation requires --resume")
    if reconciliation_cycle and args.provider != "openai":
        parser.error("provider reconciliation requires --provider openai")
    if args.bounded_provider_reconciliation and args.service_level != "interactive":
        parser.error(
            "the deprecated alias supports exact interactive service only"
        )
    if reconciliation_cycle and (
        args.spend_authorization or args.spend_reconciliation
        or args.initial_wave_authorization or args.external_authority_request
        or args.external_authority_grant
    ):
        parser.error(
            "provider reconciliation cannot apply spend authorization or reconciliation"
        )
    if args.initial_wave_authorization and len(args.spend_authorization) != PASS_COUNT:
        parser.error(
            "--initial-wave-authorization requires exactly six ordered "
            "--spend-authorization documents"
        )
    if args.initial_wave_authorization:
        parser.error(
            "legacy --initial-wave-authorization cannot authorize provider create; "
            "use the snapshot-bound external authority request and grant"
        )
    if bool(args.external_authority_request) != bool(args.external_authority_grant):
        parser.error(
            "--external-authority-request and --external-authority-grant are required together"
        )
    if args.external_authority_request:
        if args.initial_wave_authorization:
            parser.error("external authority cannot be combined with legacy wave authority")
        if len(args.spend_authorization) != PASS_COUNT:
            parser.error(
                "external initial-wave authority requires exactly six ordered "
                "--spend-authorization documents"
            )
        if not args.resume or args.provider != "openai" or args.service_level != "interactive":
            parser.error(
                "external initial-wave authority requires exact interactive OpenAI resume"
            )
    if args.provider_reconciliation_cycle and not args.observed_at:
        parser.error("--provider-reconciliation-cycle requires --observed-at")
    if args.batch_poll_interval_seconds <= 0:
        parser.error("--batch-poll-interval-seconds must be positive")
    if not args.resume and args.input_package is None:
        parser.error("--input-package is required unless --resume is used")
    if args.provider == "openai" and not args.resume and not args.spend_policy:
        parser.error("new OpenAI runs require --spend-policy")
    if args.resume and args.spend_policy:
        parser.error("--spend-policy is frozen at creation and cannot change on resume")

    try:
        reject_attempts = parse_attempt_map(args.fake_reject)
        error_attempts = parse_attempt_map(args.fake_error)
    except argparse.ArgumentTypeError as exc:
        parser.error(str(exc))
    def make_openai_provider(
        *,
        api_key: str,
        model: str,
        reasoning_effort: str,
    ) -> OpenAIResponsesProvider:
        return OpenAIResponsesProvider(
            api_key=api_key,
            model=model,
            reasoning_effort=reasoning_effort,
            base_url=args.openai_base_url,
            background=not args.foreground,
            poll_interval_seconds=args.poll_interval_seconds,
            response_timeout_seconds=args.response_timeout_seconds,
            http_timeout_seconds=args.http_timeout_seconds,
            max_transport_retries=args.max_transport_retries,
            transport_backoff_seconds=args.transport_backoff_seconds,
            max_output_tokens=args.max_output_tokens,
            safety_identifier=args.safety_identifier,
            prompt_cache_mode=args.prompt_cache_mode,
            prompt_cache_ttl=args.prompt_cache_ttl,
            require_spend_authorization=True,
        )

    polish_provider: OpenAIResponsesProvider | None = None
    critic_provider: OpenAIResponsesProvider | None = None
    qualitative_editor_provider: OpenAIResponsesProvider | None = None
    if args.prompt_layout_report:
        provider = make_openai_provider(
            api_key="prompt-layout-report-does-not-contact-openai",
            model=args.model,
            reasoning_effort=args.reasoning_effort,
        )
    elif args.provider == "fake":
        provider: AuthoringProvider = FakeAuthoringProvider(
            reject_attempts=reject_attempts,
            error_attempts=error_attempts,
        )
    else:
        if args.fake_reject or args.fake_error:
            parser.error(
                "--fake-reject and --fake-error require --provider fake"
            )
        api_key = os.environ.get(args.api_key_env)
        if not api_key:
            parser.error(
                f"--provider openai requires {args.api_key_env} to be set"
            )
        initial_provider = make_openai_provider(
            api_key=api_key,
            model=args.model,
            reasoning_effort=args.reasoning_effort,
        )
        if args.routing_policy == "cost_optimized":
            provider = RoutedOpenAIProvider(
                initial=initial_provider,
                retry=make_openai_provider(
                    api_key=api_key,
                    model=args.retry_model,
                    reasoning_effort=args.retry_reasoning_effort,
                ),
            )
            polish_provider = make_openai_provider(
                api_key=api_key,
                model=args.polish_model,
                reasoning_effort=args.polish_reasoning_effort,
            )
        else:
            provider = initial_provider
            polish_provider = initial_provider
        if args.qualitative_critic:
            critic_provider = make_openai_provider(
                api_key=api_key,
                model=args.critic_model,
                reasoning_effort=args.critic_reasoning_effort,
            )
        if args.qualitative_candidate:
            qualitative_editor_provider = make_openai_provider(
                api_key=api_key,
                model=args.qualitative_editor_model,
                reasoning_effort=args.qualitative_editor_reasoning_effort,
            )
    if reconciliation_cycle:
        from .reconciliation import (
            ProviderReconciliationAdapters,
            reconcile_authoring_provider_cycle,
        )

        preliminary_state = load_json(args.run_dir / "run.json")
        event_emitter = (
            ExecutionEventEmitter(
                release=__version__,
                sink=(
                    StdoutJsonlSink()
                    if args.events_stdout_jsonl
                    else JsonlEventSink(args.events_jsonl)
                ),
                base_correlation={
                    "native_run_id": str(preliminary_state.get("run_id") or "")
                },
            )
            if args.events_jsonl is not None or args.events_stdout_jsonl
            else None
        )
        batch_provider = openai_provider_for_attempt(provider, 1)
        result = reconcile_authoring_provider_cycle(
            args.run_dir,
            observed_at=args.observed_at or utc_now(),
            provider_adapters=ProviderReconciliationAdapters(
                exact_interactive_provider=provider,
                exact_batch_provider=provider,
                exact_batch_transport=UrllibOpenAIBatchTransport(
                    api_key=batch_provider.api_key,
                    base_url=batch_provider.base_url,
                    timeout_seconds=min(batch_provider.http_timeout_seconds, 40.0),
                ),
                max_attempts=args.max_attempts,
                python_executable=args.python_executable,
                polish_provider=polish_provider,
                critic_provider=critic_provider,
                qualitative_editor_provider=qualitative_editor_provider,
            ),
            event_emitter=event_emitter,
        )
        output_result(result)
        if result["outcome"] != "terminal":
            raise SystemExit(3)
        return
    if args.resume:
        preliminary_state = load_json(args.run_dir / "run.json")
        legacy_denial_present = any(
            isinstance(action, dict)
            and action.get("state") == "DENIED_PROVIDERLESS"
            and isinstance(action.get("negative_authorization"), dict)
            and not isinstance(
                action["negative_authorization"].get("run_transition"), dict
            )
            for action in (preliminary_state.get("spend_ledger") or {}).get(
                "actions", []
            )
        )
        if legacy_denial_present or isinstance(
            preliminary_state.get("required_denial_reconciliation"), dict
        ):
            # This runs before the ordinary resume snapshot check so an
            # interrupted, tightly bounded reconciliation can repair its own
            # declared write set. It cannot bless unrelated workspace changes.
            from .lifecycle import reconcile_required_providerless_denial

            reconcile_required_providerless_denial(args.run_dir)
        state, run_json = resume_run(
            run_dir=args.run_dir,
            provider=provider,
            max_attempts=args.max_attempts,
            service_level=args.service_level,
        )
    else:
        state, run_json = create_run(
            input_package=args.input_package,
            run_dir=args.run_dir,
            subject=args.subject,
            provider=provider,
            max_attempts=args.max_attempts,
            sbe_script=args.sbe_script,
            python_executable=args.python_executable,
            service_level=args.service_level,
            split_assignment_policy=args.split_assignment_policy,
            full_chart_basis_format=args.full_chart_basis_format,
            exact_natal_policy=args.exact_natal_policy,
            profile=profile_from_args(args),
        )
    event_emitter = (
        ExecutionEventEmitter(
            release=__version__,
            sink=(
                StdoutJsonlSink()
                if args.events_stdout_jsonl
                else JsonlEventSink(args.events_jsonl)
            ),
            base_correlation={"native_run_id": str(state.get("run_id") or "")},
        )
        if args.events_jsonl is not None or args.events_stdout_jsonl
        else None
    )
    if event_emitter is not None:
        event_emitter.emit(
            "run.resumed" if args.resume else "run.started",
            data={"state_revision": int(state.get("state_revision") or 0)},
        )
    if (state.get("terminal_transition") or {}).get("outcome") == "terminalized":
        from .native_transitions import publish_native_execution_result
        publish_native_execution_result(
            args.run_dir, command_kind="ordinary_authoring",
            sbe_release=__version__, published_at=utc_now(),
            event_emitter=event_emitter,
        )
        output_result(state)
        return
    if (
        args.provider == "openai"
        and args.service_level == "interactive"
        and not isinstance(state.get("initial_authoring_wave"), dict)
    ):
        orphaned_initial_lineage = _orphaned_initial_lineage_categories(
            state, args.run_dir,
        )
        if orphaned_initial_lineage:
            raise _initial_lineage_refusal(
                orphaned_initial_lineage,
                "Historical initial-authoring evidence cannot be joined to one exact wave",
            )
    if args.spend_authorization and not (
        args.initial_wave_authorization or args.external_authority_grant
    ):
        if isinstance(state.get("initial_authoring_wave"), dict):
            raise InitialWaveError(
                "aggregate_grant_required",
                "Initial-wave member authorizations require the exact "
                "snapshot-bound external-authority request and aggregate grant",
            )
        documents = [load_json(path) for path in args.spend_authorization]
        try:
            apply_spend_authorizations(state, documents)
        finally:
            save_state(run_json, state)
    if args.spend_reconciliation:
        documents = [load_json(path) for path in args.spend_reconciliation]
        apply_spend_reconciliations(state, documents)
        save_state(run_json, state)
    spend_controller = (
        SpendController(
            state=state,
            run_json=run_json,
            state_lock=threading.Lock(),
            consumer_id=f"pid:{os.getpid()}",
            event_emitter=event_emitter,
        )
        if args.provider == "openai"
        else None
    )
    if args.prompt_layout_report:
        if not isinstance(provider, OpenAIResponsesProvider):
            raise AssertionError("prompt report requires OpenAI request layout")
        report = build_prompt_layout_report(
            state=state,
            run_dir=args.run_dir,
            provider=provider,
        )
        write_json_atomic(args.prompt_layout_report, report)
        output_result(report)
        return
    exact_initial_wave_mode = bool(
        args.provider == "openai"
        and args.service_level == "interactive"
        and (
            isinstance(state.get("initial_authoring_wave"), dict)
            or all(
                not record.get("attempts")
                for record in state.get("passes", {}).values()
            )
        )
    )
    if exact_initial_wave_mode:
        if args.external_authority_request:
            execute_exact_initial_wave_with_external_authority(
                run_dir=args.run_dir,
                request=load_json(args.external_authority_request),
                grant=load_json(args.external_authority_grant),
                member_authorizations=[
                    load_json(path) for path in args.spend_authorization
                ],
                provider=provider, event_emitter=event_emitter,
            )
            state = load_json(run_json)
            from .native_transitions import publish_native_execution_result
            publish_native_execution_result(
                args.run_dir, command_kind="ordinary_authoring",
                sbe_release=__version__, published_at=utc_now(),
                event_emitter=event_emitter,
            )
            output_result(state)
            return
        stored_initial_wave = state.get("initial_authoring_wave")
        if (
            isinstance(stored_initial_wave, dict)
            and stored_initial_wave.get("state") == "AWAITING_SPEND_AUTHORIZATION"
        ):
            raise InitialWaveError(
                "aggregate_grant_required",
                "A stored initial wave awaiting external authority requires the "
                "exact snapshot-bound request and aggregate grant",
            )
        wave = prepare_exact_interactive_initial_wave(
            state=state, provider=provider, run_dir=args.run_dir,
            run_json=run_json,
        )
        if wave is None:
            raise InitialWaveError(
                "mixed_initial_state",
                "Exact initial wave cannot adopt a partially started legacy run",
            )
        if args.initial_wave_authorization:
            authorize_exact_interactive_initial_wave(
                state=state, run_json=run_json,
                envelope=load_json(args.initial_wave_authorization),
                member_authorizations=[
                    load_json(path) for path in args.spend_authorization
                ],
            )
        if state["initial_authoring_wave"]["state"] == "AUTHORIZED":
            execute_exact_interactive_initial_wave(
                state=state, provider=provider, run_json=run_json,
                event_emitter=event_emitter,
            )
        else:
            save_state(run_json, state)
        from .native_transitions import publish_native_execution_result
        publish_native_execution_result(
            args.run_dir, command_kind="ordinary_authoring",
            sbe_release=__version__, published_at=utc_now(),
            event_emitter=event_emitter,
        )
        output_result(state)
        return
    authoring_complete = True
    with checkpoint_spend_boundary(run_json, state):
        if args.service_level == "batch":
            batch_base_provider = openai_provider_for_attempt(provider, 1)
            authoring_complete = author_pending_passes_batch(
                state=state,
                provider=provider,
                transport=UrllibOpenAIBatchTransport(
                    api_key=batch_base_provider.api_key,
                    base_url=batch_base_provider.base_url,
                    timeout_seconds=batch_base_provider.http_timeout_seconds,
                ),
                run_dir=args.run_dir,
                max_attempts=args.max_attempts,
                python_executable=args.python_executable,
                run_json=run_json,
                poll_interval_seconds=args.batch_poll_interval_seconds,
                detach=args.batch_detach,
                spend_controller=spend_controller,
            )
        else:
            author_pending_passes(
                state=state,
                provider=provider,
                run_dir=args.run_dir,
                max_attempts=args.max_attempts,
                python_executable=args.python_executable,
                run_json=run_json,
                max_workers=args.max_workers,
                spend_controller=spend_controller,
            )
    if not authoring_complete:
        update_run_status(state)
        save_state(run_json, state)
        if event_emitter is not None:
            event_emitter.emit("run.detached", data={
                "state_revision": int(state.get("state_revision") or 0),
                "reason_code": "batch_detach_or_provider_wait",
            })
            event_emitter.emit("checkpoint.committed", data={
                "state_revision": int(state.get("state_revision") or 0),
                "snapshot_sha256": sha256_file(args.run_dir / SNAPSHOT_NAME),
            })
        from .native_transitions import publish_native_execution_result
        publish_native_execution_result(
            args.run_dir, command_kind="ordinary_authoring",
            sbe_release=__version__, published_at=utc_now(),
            event_emitter=event_emitter,
        )
        output_result(state)
        return
    with checkpoint_spend_boundary(run_json, state):
        finalize_subjects(
            state=state,
            run_dir=args.run_dir,
            python_executable=args.python_executable,
            allow_lint_warnings=args.allow_lint_warnings,
            polish=args.polish,
            polish_provider=polish_provider,
            max_polish_attempts=args.max_polish_attempts,
            spend_controller=spend_controller,
        )
        if args.qualitative_critic and critic_provider is not None:
            for record in state.get("subjects", {}).values():
                if record.get("state") in FINAL_SUCCESS_STATES:
                    run_qualitative_review(
                        record=record,
                        critic_provider=critic_provider,
                        editor_provider=qualitative_editor_provider,
                        run_dir=args.run_dir,
                        python_executable=args.python_executable,
                        max_findings=args.max_critic_findings,
                        max_target_fields=args.max_qualitative_target_fields,
                        max_target_cards=args.max_qualitative_target_cards,
                        spend_controller=spend_controller,
                        run_state=state,
                    )
    update_run_status(state)
    save_state(run_json, state)
    if event_emitter is not None:
        event_emitter.emit("checkpoint.committed", data={
            "state_revision": int(state.get("state_revision") or 0),
            "snapshot_sha256": sha256_file(args.run_dir / SNAPSHOT_NAME),
        })
        terminal_reason = {
            "DELIVERY_COMPLETE": "delivery_complete",
            "DELIVERY_COMPLETE_WITH_WARNINGS": "delivery_complete",
            "FINAL_QA_FAILED": "native_qa_failure",
            "FINAL_QA_REQUIRES_REVIEW": "review_required",
            "FAILED_REQUIRES_REVIEW": "review_required",
            "BUDGET_EXHAUSTED": "budget_exhausted",
            "AMBIGUOUS_PROVIDER_SUBMISSION": "ambiguous_provider_submission",
        }.get(state["status"])
        if terminal_reason is not None:
            event_emitter.emit("terminal.transitioned", data={
                "outcome": state["status"], "terminal_reason": terminal_reason,
            })
    from .native_transitions import publish_native_execution_result
    publish_native_execution_result(
        args.run_dir, command_kind="ordinary_authoring",
        sbe_release=__version__, published_at=utc_now(),
        event_emitter=event_emitter,
    )
    output_result(state)
    if state["status"] in {
        "FAILED_REQUIRES_REVIEW",
        "FINAL_QA_FAILED",
        "FINAL_QA_REQUIRES_REVIEW",
    }:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
