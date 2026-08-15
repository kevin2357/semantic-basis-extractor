"""Versioned public contracts for AstroWoof natal authoring."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


INPUT_BUNDLE_SCHEMA = "astrowoof.projected_natal_input.v0.1"
SUBJECT_PARAMS_SCHEMA = "astrowoof.subject_params.v0.1"
PUBLIC_RUN_SCHEMA = "astrowoof.semantic_closure_public_run.v0.1"
DELIVERY_MANIFEST_SCHEMA = "astrowoof.natal_delivery_manifest.v0.1"
AUTHORING_PROFILE_SCHEMA = "astrowoof.authoring_profile.v0.1"
INPUT_MANIFEST_NAME = "astrowoof-input-manifest.json"
CONTEXT_NAMES = ("general", "direct_to_dog", "handler", "hybrid")
CONTEXT_SUFFIXES = {
    "general": "general",
    "d2d": "direct_to_dog",
    "direct_to_dog": "direct_to_dog",
    "handler": "handler",
    "hybrid": "hybrid",
}


def _contained_file(root: Path, relative: str, *, label: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError(f"{label} must be a non-empty relative path")
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} escapes input package: {relative!r}") from exc
    if not candidate.is_file():
        raise FileNotFoundError(f"{label} does not exist: {candidate}")
    return candidate


def discover_projected_input(
    input_package: Path,
    subject_filter: str | None = None,
) -> tuple[dict[str, dict[str, Path]], dict[str, Any]]:
    """Normalize explicit v0.1 manifests and legacy directory layouts."""
    root = input_package.resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Input package is not a directory: {root}")
    manifest_path = root / INPUT_MANIFEST_NAME
    if manifest_path.is_file():
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict) or raw.get("schema_version") != INPUT_BUNDLE_SCHEMA:
            raise ValueError(
                f"{manifest_path}: schema_version must be {INPUT_BUNDLE_SCHEMA!r}"
            )
        records = raw.get("subjects")
        if not isinstance(records, list) or not records:
            raise ValueError(f"{manifest_path}: subjects must be a non-empty array")
        discovered: dict[str, dict[str, Path]] = {}
        normalized_subjects: list[dict[str, Any]] = []
        for record in records:
            if not isinstance(record, dict):
                raise ValueError(f"{manifest_path}: every subject must be an object")
            subject = record.get("subject_id")
            if not isinstance(subject, str) or not subject.strip():
                raise ValueError(f"{manifest_path}: subject_id must be a non-empty string")
            subject = subject.lower()
            if subject_filter and subject != subject_filter.lower():
                continue
            if subject in discovered:
                raise ValueError(f"{manifest_path}: duplicate subject_id {subject!r}")
            contexts = record.get("contexts")
            if not isinstance(contexts, dict):
                raise ValueError(f"{manifest_path}: {subject}.contexts must be an object")
            unknown = sorted(set(contexts) - set(CONTEXT_NAMES))
            missing = sorted(set(CONTEXT_NAMES) - set(contexts))
            if unknown or missing:
                raise ValueError(
                    f"{manifest_path}: {subject}.contexts missing={missing}, unknown={unknown}"
                )
            paths = {
                context: _contained_file(
                    root,
                    contexts[context],
                    label=f"{subject}.contexts.{context}",
                )
                for context in CONTEXT_NAMES
            }
            if len({path.parent for path in paths.values()}) != 1:
                raise ValueError(
                    f"{manifest_path}: {subject} context files must share one directory"
                )
            discovered[subject] = paths
            normalized_subjects.append(
                {
                    "subject_id": subject,
                    "contexts": {
                        name: str(path.relative_to(root)).replace("\\", "/")
                        for name, path in paths.items()
                    },
                    "params": (
                        str((next(iter(paths.values())).parent / "params.json").relative_to(root)).replace("\\", "/")
                        if (next(iter(paths.values())).parent / "params.json").is_file()
                        else None
                    ),
                }
            )
        if not discovered:
            raise FileNotFoundError(
                f"No projected natal subjects matched {subject_filter!r}"
            )
        return discovered, {
            "schema_version": INPUT_BUNDLE_SCHEMA,
            "source_format": "manifest-v0.1",
            "manifest": str(manifest_path),
            "subjects": normalized_subjects,
        }

    candidate_dirs = [root]
    if not any(root.glob("natal.*.woof.*.json")):
        candidate_dirs = sorted(path for path in root.iterdir() if path.is_dir())
    discovered: dict[str, dict[str, Path]] = {}
    for directory in candidate_dirs:
        for path in sorted(directory.glob("natal.*.woof.*.json")):
            parts = path.name.split(".")
            if len(parts) < 5 or parts[0].lower() != "natal" or parts[-1].lower() != "json":
                continue
            suffix = parts[-2].lower()
            if suffix not in CONTEXT_SUFFIXES:
                continue
            subject = ".".join(parts[1:-3]).lower()
            if not subject or (subject_filter and subject != subject_filter.lower()):
                continue
            context = CONTEXT_SUFFIXES[suffix]
            subject_paths = discovered.setdefault(subject, {})
            if context in subject_paths:
                raise ValueError(f"Duplicate {context} files for subject {subject}")
            subject_paths[context] = path.resolve()
    if not discovered:
        raise FileNotFoundError("No projected natal context files found")
    normalized_subjects = []
    for subject, paths in sorted(discovered.items()):
        normalized_subjects.append(
            {
                "subject_id": subject,
                "contexts": {
                    name: str(path.relative_to(root)).replace("\\", "/")
                    for name, path in sorted(paths.items())
                },
                "params": (
                    str((next(iter(paths.values())).parent / "params.json").relative_to(root)).replace("\\", "/")
                    if (next(iter(paths.values())).parent / "params.json").is_file()
                    else None
                ),
            }
        )
    return dict(sorted(discovered.items())), {
        "schema_version": INPUT_BUNDLE_SCHEMA,
        "source_format": "legacy-directory-v0",
        "manifest": None,
        "subjects": normalized_subjects,
    }


def normalize_subject_params(
    value: dict[str, Any],
    *,
    subject_id: str,
    source: str,
) -> dict[str, Any]:
    """Validate params.json and return its versioned normalized form."""
    if not isinstance(value, dict):
        raise ValueError(f"{source}: params.json must contain one object")
    allowed = {
        "schema_version", "subject_id", "display_name", "subject_type", "gender",
        "pronouns", "breed", "birth_date", "birth_datetime", "birth_latitude",
        "birth_longitude", "birth_location", "birth_date_precision",
    }
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ValueError(f"{source}: unsupported fields: {unknown}")
    version = value.get("schema_version", SUBJECT_PARAMS_SCHEMA)
    if version != SUBJECT_PARAMS_SCHEMA:
        raise ValueError(f"{source}: unsupported schema_version {version!r}")
    if value.get("subject_id") not in (None, "", subject_id):
        raise ValueError(f"{source}: subject_id must match {subject_id!r}")
    result = dict(value)
    result["schema_version"] = SUBJECT_PARAMS_SCHEMA
    result["subject_id"] = subject_id
    string_fields = allowed - {"schema_version", "pronouns", "birth_latitude", "birth_longitude"}
    for field in string_fields:
        if field in result and not isinstance(result[field], str):
            raise ValueError(f"{source}: {field} must be a string")
    for field, low, high in (("birth_latitude", -90, 90), ("birth_longitude", -180, 180)):
        if field in result:
            if isinstance(result[field], bool) or not isinstance(result[field], (int, float)):
                raise ValueError(f"{source}: {field} must be numeric")
            if not low <= result[field] <= high:
                raise ValueError(f"{source}: {field} must be between {low} and {high}")
    pronouns = result.get("pronouns")
    pronoun_fields = {"subject", "object", "possessive_adjective", "possessive_pronoun", "reflexive"}
    if pronouns is not None:
        if not isinstance(pronouns, dict):
            raise ValueError(f"{source}: pronouns must be an object")
        unknown_pronouns = sorted(set(pronouns) - pronoun_fields)
        if unknown_pronouns:
            raise ValueError(f"{source}: unsupported pronoun fields: {unknown_pronouns}")
        if any(not isinstance(item, str) for item in pronouns.values()):
            raise ValueError(f"{source}: pronoun values must be strings")
    return result


def public_run_state(state: dict[str, Any]) -> dict[str, Any]:
    passes = list(state.get("passes", {}).values())
    accepted = sum(item.get("state") == "PASS_QA_ACCEPTED" for item in passes)
    ledger = state.get("spend_ledger") or {}
    actions = ledger.get("actions") or []
    terminal = state.get("terminal_transition") or {}
    return {
        "schema_version": PUBLIC_RUN_SCHEMA,
        "status": state.get("status"),
        "created_at": state.get("created_at"),
        "updated_at": state.get("updated_at"),
        "service_level": state.get("service_level"),
        "progress": {"passes_total": len(passes), "passes_accepted": accepted},
        "spend_control": {
            "currency": (ledger.get("policy") or {}).get("currency"),
            "pending_action_ids": [
                item.get("action_id") for item in actions
                if item.get("state") == "PREPARED"
            ],
            "budget_exhausted_action_ids": [
                item.get("action_id") for item in actions
                if item.get("state") == "BUDGET_EXHAUSTED"
            ],
            "ambiguous_action_ids": [
                item.get("action_id") for item in actions
                if item.get("state") == "AMBIGUOUS_PROVIDER_SUBMISSION"
            ],
        },
        "terminal": ({
            "outcome": terminal.get("terminal_outcome"),
            "reason": terminal.get("terminal_reason"),
            "state_revision": state.get("state_revision"),
        } if terminal.get("outcome") == "terminalized" else None),
        "subjects": {
            subject: {
                "status": record.get("state"),
                "delivery_ready": bool(record.get("delivery")),
            }
            for subject, record in sorted(state.get("subjects", {}).items())
        },
    }


def authoring_profile(**values: Any) -> dict[str, Any]:
    return {
        "schema_version": AUTHORING_PROFILE_SCHEMA,
        "profile_id": "astrowoof-natal-default-v0.1",
        **values,
    }
