"""Closed, package-installed processing-profile and prompt-release catalogs.

This module intentionally has no workspace, CLI, environment, or provider
dependencies.  It establishes immutable catalog identity before a later slice
allows a semantic-closure command to consume a selected profile.
"""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version as distribution_version
from importlib.resources import files
import json
import math
import re
from typing import Any, Callable, Mapping


PROCESSING_PROFILE_SCHEMA = "astrowoof.processing_profile.v1"
PROCESSING_PROFILE_CATALOG_SCHEMA = "astrowoof.processing_profile_catalog.v1"
PROMPT_RELEASE_SCHEMA = "astrowoof.prompt_release.v1"
PROMPT_RELEASE_WORKSPACE_SCHEMA = "astrowoof.prompt_release.v2"
PROMPT_RELEASE_CATALOG_SCHEMA = "astrowoof.prompt_release_catalog.v1"
WORKER_COMPATIBILITY_SCHEMA = "astrowoof.worker_compatibility.v1"
PROCESSING_PROFILE_BINDING_SCHEMA = "astrowoof.processing_profile_binding.v1"
PROFILE_CATALOG_RESOURCE = "processing-profile-catalog.v1.json"
PROMPT_RELEASE_CATALOG_RESOURCE = "prompt-release-catalog.v1.json"

_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_IDENTIFIER = re.compile(r"^[a-z][a-z0-9._-]*$")
# Package descriptors use the closed subset needed for release candidates:
# a final PEP 440 three-part release or its explicit alpha sequence.
_SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:a[0-9]+)?$")
_PROFILE_KEYS = {
    "schema_version", "profile_id", "profile_version", "profile_sha256",
    "allowed_environments", "route", "selection_policy", "prompt_release",
    "deterministic_runtime", "sbe", "worker_compatibility",
}
_PROMPT_RELEASE_KEYS = {
    "schema_version", "release_id", "release_version", "release_sha256",
    "status", "allowed_environments", "route_families", "profile_ids",
    "stage_components", "components",
}
_PROMPT_RELEASE_WORKSPACE_KEYS = _PROMPT_RELEASE_KEYS | {"workspace_components"}
_CATALOG_KEYS = {"schema_version", "catalog_sha256", "profiles"}
_PROMPT_CATALOG_KEYS = {"schema_version", "catalog_sha256", "releases"}
_PROFILE_ROUTE_KEYS = {"family", "execution_mode", "sbe_contract"}
_PROMPT_REFERENCE_KEYS = {"release_id", "release_sha256"}
_COMPONENT_KEYS = {"component_id", "resource", "sha256"}
_WORKSPACE_COMPONENT_KEYS = {"component_id", "resource", "destination", "sha256"}
_WORKER_COMPATIBILITY_KEYS = {
    "schema_version", "worker_role", "required_distributions",
    "compatibility_sha256",
}
_DISTRIBUTION_KEYS = {"distribution", "version"}
_DETERMINISTIC_RUNTIME_KEYS = {
    "birth_time_mode", "ephemeris_mode", "projection_contexts",
    "projection_contract",
}
_SBE_COMPATIBILITY_KEYS = {
    "provider", "provider_service_level", "routing_policy", "model",
    "reasoning_effort", "retry_model", "retry_reasoning_effort",
    "split_assignment_policy", "full_chart_basis_format", "max_workers",
    "max_attempts", "max_output_tokens", "background",
    "poll_interval_seconds", "response_timeout_seconds", "http_timeout_seconds",
    "max_transport_retries", "transport_backoff_seconds", "prompt_cache_mode",
    "prompt_cache_ttl", "polish", "max_polish_attempts", "polish_model",
    "polish_reasoning_effort", "qualitative_critic", "critic_model",
    "critic_reasoning_effort", "qualitative_candidate",
    "qualitative_editor_model", "qualitative_editor_reasoning_effort",
}


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("processing-profile JSON contains duplicate keys")
        value[key] = item
    return value


def _reject_nonfinite(value: str) -> None:
    raise ValueError(f"processing-profile JSON contains non-finite number: {value}")


def _assert_finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("processing-profile JSON contains non-finite number")
    if isinstance(value, list):
        for item in value:
            _assert_finite(item)
    elif isinstance(value, dict):
        for item in value.values():
            _assert_finite(item)


def _parse_json(raw: bytes) -> Any:
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError("processing-profile resource must be UTF-8") from exc
    decoder = json.JSONDecoder(
        object_pairs_hook=_reject_duplicate_pairs,
        parse_constant=_reject_nonfinite,
    )
    try:
        value, end = decoder.raw_decode(text)
    except json.JSONDecodeError as exc:
        raise ValueError("processing-profile resource is invalid JSON") from exc
    if text[end:].strip():
        raise ValueError("processing-profile resource has trailing content")
    _assert_finite(value)
    return value


def canonical_processing_profile_json(value: Any) -> bytes:
    """Return the one digest representation for closed profile/release values."""
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    body = dict(value)
    body.pop(field, None)
    return sha256(canonical_processing_profile_json(body)).hexdigest()


def processing_profile_sha256(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "profile_sha256")


def prompt_release_sha256(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "release_sha256")


def worker_compatibility_sha256(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "compatibility_sha256")


def _catalog_sha256(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "catalog_sha256")


def _require_identifier(value: Any, *, label: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        raise ValueError(f"{label} is invalid")
    return value


def _require_digest(value: Any, *, label: str) -> str:
    if not isinstance(value, str) or not _HEX64.fullmatch(value):
        raise ValueError(f"{label} must be a lowercase SHA-256")
    return value


def _require_semver(value: Any, *, label: str) -> str:
    if not isinstance(value, str) or not _SEMVER.fullmatch(value):
        raise ValueError(f"{label} is invalid")
    return value


def _require_identifier_list(value: Any, *, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a nonempty array")
    items = [_require_identifier(item, label=label) for item in value]
    if items != sorted(items) or len(items) != len(set(items)):
        raise ValueError(f"{label} must be sorted and unique")
    return items


def validate_worker_compatibility(value: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a role's stable package requirements, not deployment state."""
    descriptor = deepcopy(dict(value))
    if set(descriptor) != _WORKER_COMPATIBILITY_KEYS:
        raise ValueError("worker compatibility fields are not exact")
    if descriptor.get("schema_version") != WORKER_COMPATIBILITY_SCHEMA:
        raise ValueError("worker compatibility schema is unsupported")
    if descriptor.get("worker_role") not in {"deterministic_runtime", "sbe_authoring"}:
        raise ValueError("worker compatibility role is invalid")
    distributions = descriptor.get("required_distributions")
    if not isinstance(distributions, list) or not distributions:
        raise ValueError("worker compatibility distributions are invalid")
    names: list[str] = []
    for item in distributions:
        if not isinstance(item, dict) or set(item) != _DISTRIBUTION_KEYS:
            raise ValueError("worker compatibility distribution is invalid")
        names.append(_require_identifier(item.get("distribution"), label="worker distribution"))
        _require_semver(item.get("version"), label="worker distribution version")
    if names != sorted(names) or len(names) != len(set(names)):
        raise ValueError("worker compatibility distributions are not canonical")
    _require_digest(descriptor.get("compatibility_sha256"), label="worker compatibility digest")
    if descriptor["compatibility_sha256"] != worker_compatibility_sha256(descriptor):
        raise ValueError("worker compatibility digest mismatch")
    return descriptor


def validate_processing_profile(value: Mapping[str, Any]) -> dict[str, Any]:
    """Validate one closed processing profile and its canonical identity."""
    profile = deepcopy(dict(value))
    if set(profile) != _PROFILE_KEYS:
        raise ValueError("processing profile fields are not exact")
    if profile.get("schema_version") != PROCESSING_PROFILE_SCHEMA:
        raise ValueError("processing profile schema is unsupported")
    _require_identifier(profile.get("profile_id"), label="processing profile ID")
    _require_semver(profile.get("profile_version"), label="processing profile version")
    _require_identifier_list(
        profile.get("allowed_environments"), label="processing profile environments",
    )
    route = profile.get("route")
    if not isinstance(route, dict) or set(route) != _PROFILE_ROUTE_KEYS:
        raise ValueError("processing profile route is invalid")
    if route.get("family") not in {"exact_natal", "bounded_natal"}:
        raise ValueError("processing profile route family is invalid")
    if route.get("execution_mode") not in {"live", "batch"}:
        raise ValueError("processing profile execution mode is invalid")
    if not isinstance(route.get("sbe_contract"), str) or not route["sbe_contract"]:
        raise ValueError("processing profile SBE route contract is invalid")
    _require_identifier(profile.get("selection_policy"), label="selection policy")
    prompt_release = profile.get("prompt_release")
    if not isinstance(prompt_release, dict) or set(prompt_release) != _PROMPT_REFERENCE_KEYS:
        raise ValueError("processing profile prompt-release reference is invalid")
    _require_identifier(prompt_release.get("release_id"), label="prompt release ID")
    _require_digest(prompt_release.get("release_sha256"), label="prompt release digest")
    deterministic = profile.get("deterministic_runtime")
    if not isinstance(deterministic, dict) or set(deterministic) != _DETERMINISTIC_RUNTIME_KEYS:
        raise ValueError("processing profile deterministic fragment is invalid")
    birth_time_mode = deterministic.get("birth_time_mode")
    if birth_time_mode not in {"exact", "bounded"}:
        raise ValueError("processing profile birth-time mode is invalid")
    if deterministic.get("ephemeris_mode") != "moshier":
        raise ValueError("processing profile ephemeris mode is invalid")
    if deterministic.get("projection_contexts") != [
        "direct_to_dog", "general", "handler", "hybrid",
    ]:
        raise ValueError("processing profile projection contexts are invalid")
    expected_projection_contract = (
        "woofmapped_bounded_astrology.v0@0.1.0"
        if birth_time_mode == "bounded"
        else "woofmapped_astrology.v0@0.1.0"
    )
    if deterministic.get("projection_contract") != expected_projection_contract:
        raise ValueError("processing profile projection contract is invalid")
    compatibility = profile.get("worker_compatibility")
    if not isinstance(compatibility, dict) or set(compatibility) != {
        "deterministic_runtime", "sbe_authoring",
    }:
        raise ValueError("processing profile worker compatibility is invalid")
    for role, descriptor in compatibility.items():
        validated_descriptor = validate_worker_compatibility(descriptor)
        if validated_descriptor["worker_role"] != role:
            raise ValueError("processing profile worker compatibility role mismatch")
    sbe = profile.get("sbe")
    if not isinstance(sbe, dict) or set(sbe) != _SBE_COMPATIBILITY_KEYS:
        raise ValueError("processing profile SBE fragment is invalid")
    if sbe.get("provider") != "openai" or sbe.get("provider_service_level") not in {"interactive", "batch"}:
        raise ValueError("processing profile SBE provider settings are invalid")
    if sbe.get("routing_policy") not in {"fixed", "cost_optimized"}:
        raise ValueError("processing profile SBE routing policy is invalid")
    if sbe.get("split_assignment_policy") not in {"contiguous", "stratified-v1"}:
        raise ValueError("processing profile SBE split policy is invalid")
    if sbe.get("full_chart_basis_format") not in {"legacy", "compact-v1", "compact-v2"}:
        raise ValueError("processing profile SBE basis format is invalid")
    if sbe.get("prompt_cache_mode") not in {"disabled", "implicit", "explicit"} or sbe.get("prompt_cache_ttl") != "30m":
        raise ValueError("processing profile SBE prompt-cache settings are invalid")
    if any(not isinstance(sbe.get(key), bool) for key in (
        "background", "polish", "qualitative_critic", "qualitative_candidate",
    )):
        raise ValueError("processing profile SBE boolean settings are invalid")
    if any(isinstance(sbe.get(key), bool) or not isinstance(sbe.get(key), int) or sbe[key] < 0 for key in (
        "max_workers", "max_attempts", "max_output_tokens", "max_transport_retries",
        "max_polish_attempts",
    )):
        raise ValueError("processing profile SBE integer settings are invalid")
    if any(isinstance(sbe.get(key), bool) or not isinstance(sbe.get(key), (int, float)) or sbe[key] <= 0 for key in (
        "poll_interval_seconds", "response_timeout_seconds", "http_timeout_seconds",
        "transport_backoff_seconds",
    )):
        raise ValueError("processing profile SBE timeout settings are invalid")
    for key in (
        "model", "reasoning_effort", "retry_model", "retry_reasoning_effort",
        "polish_model", "polish_reasoning_effort", "critic_model",
        "critic_reasoning_effort", "qualitative_editor_model",
        "qualitative_editor_reasoning_effort",
    ):
        _require_identifier(sbe.get(key), label=f"processing profile SBE {key}")
    _require_digest(profile.get("profile_sha256"), label="processing profile digest")
    if profile["profile_sha256"] != processing_profile_sha256(profile):
        raise ValueError("processing profile digest mismatch")
    return profile


def _resource_bytes(resource: str) -> bytes:
    return files("astrowoof_natal_authoring.resources.contracts").joinpath(resource).read_bytes()


def _prompt_resource_bytes(resource: str) -> bytes:
    return files("astrowoof_natal_authoring.resources").joinpath(resource).read_bytes()


def _validate_prompt_component(
    component: Any, *, resource_reader: Callable[[str], bytes], workspace: bool,
) -> tuple[str, str, str | None, bytes]:
    expected = _WORKSPACE_COMPONENT_KEYS if workspace else _COMPONENT_KEYS
    if not isinstance(component, dict) or set(component) != expected:
        raise ValueError("prompt release component is invalid")
    component_id = _require_identifier(component.get("component_id"), label="prompt component ID")
    resource = component.get("resource")
    if (
        not isinstance(resource, str) or not resource.startswith("authoring/")
        or ".." in resource.split("/") or not resource.endswith(".md")
    ):
        raise ValueError("prompt component resource is invalid")
    destination: str | None = None
    if workspace:
        destination = component.get("destination")
        if (
            not isinstance(destination, str) or not destination.endswith(".md")
            or destination in {".", ".."} or "/" in destination or "\\" in destination
        ):
            raise ValueError("prompt workspace destination is invalid")
    raw = _canonical_prompt_asset(resource_reader(resource))
    if component.get("sha256") != sha256(raw).hexdigest():
        raise ValueError("prompt component digest mismatch")
    return component_id, resource, destination, raw


def read_processing_profile_catalog() -> dict[str, Any]:
    value = _parse_json(_resource_bytes(PROFILE_CATALOG_RESOURCE))
    if not isinstance(value, dict) or set(value) != _CATALOG_KEYS:
        raise ValueError("processing-profile catalog fields are not exact")
    if value.get("schema_version") != PROCESSING_PROFILE_CATALOG_SCHEMA:
        raise ValueError("processing-profile catalog schema is unsupported")
    _require_digest(value.get("catalog_sha256"), label="processing-profile catalog digest")
    if value["catalog_sha256"] != _catalog_sha256(value):
        raise ValueError("processing-profile catalog digest mismatch")
    profiles = value.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        raise ValueError("processing-profile catalog profiles are invalid")
    validated = [validate_processing_profile(item) for item in profiles]
    profile_ids = [item["profile_id"] for item in validated]
    if profile_ids != sorted(profile_ids) or len(profile_ids) != len(set(profile_ids)):
        raise ValueError("processing-profile catalog profile IDs are not canonical")
    return {**value, "profiles": validated}


def read_processing_profile(profile_id: str) -> dict[str, Any]:
    _require_identifier(profile_id, label="processing profile ID")
    catalog = read_processing_profile_catalog()
    for profile in catalog["profiles"]:
        if profile["profile_id"] == profile_id:
            return deepcopy(profile)
    raise ValueError("processing profile is not installed")


def _canonical_prompt_asset(raw: bytes) -> bytes:
    try:
        raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError("prompt asset must be UTF-8") from exc
    if b"\r" in raw or not raw.endswith(b"\n"):
        raise ValueError("prompt asset must use canonical LF-terminated bytes")
    return raw


def validate_prompt_release(
    value: Mapping[str, Any], *,
    resource_reader: Callable[[str], bytes] = _prompt_resource_bytes,
) -> dict[str, Any]:
    """Validate one release and every installed text asset it names."""
    release = deepcopy(dict(value))
    schema = release.get("schema_version")
    workspace_schema = schema == PROMPT_RELEASE_WORKSPACE_SCHEMA
    expected_keys = _PROMPT_RELEASE_WORKSPACE_KEYS if workspace_schema else _PROMPT_RELEASE_KEYS
    if set(release) != expected_keys:
        raise ValueError("prompt release fields are not exact")
    if schema not in {PROMPT_RELEASE_SCHEMA, PROMPT_RELEASE_WORKSPACE_SCHEMA}:
        raise ValueError("prompt release schema is unsupported")
    _require_identifier(release.get("release_id"), label="prompt release ID")
    _require_semver(release.get("release_version"), label="prompt release version")
    if release.get("status") not in {"active", "deprecated"}:
        raise ValueError("prompt release status is invalid")
    _require_identifier_list(release.get("allowed_environments"), label="prompt release environments")
    if release.get("route_families") not in [["exact_natal"], ["bounded_natal"], ["bounded_natal", "exact_natal"]]:
        raise ValueError("prompt release route families are invalid")
    _require_identifier_list(release.get("profile_ids"), label="prompt release profile IDs")
    components = release.get("components")
    if not isinstance(components, list) or not components:
        raise ValueError("prompt release components are invalid")
    component_ids: list[str] = []
    seen_resources: set[str] = set()
    for component in components:
        component_id, resource, _destination, _raw = _validate_prompt_component(
            component, resource_reader=resource_reader, workspace=False,
        )
        if resource in seen_resources:
            raise ValueError("prompt component resource is duplicated")
        seen_resources.add(resource)
        component_ids.append(component_id)
    if component_ids != sorted(component_ids) or len(component_ids) != len(set(component_ids)):
        raise ValueError("prompt release component IDs are not canonical")
    stage_components = release.get("stage_components")
    if not isinstance(stage_components, dict) or set(stage_components) != {"initial", "retry", "polish", "critic"}:
        raise ValueError("prompt release stage map is invalid")
    for stage, selected in stage_components.items():
        if not isinstance(stage, str) or not isinstance(selected, list) or not selected:
            raise ValueError("prompt release stage selection is invalid")
        if selected != sorted(selected) or len(selected) != len(set(selected)):
            raise ValueError("prompt release stage selection is not canonical")
        if any(item not in component_ids for item in selected):
            raise ValueError("prompt release stage names unknown component")
    if workspace_schema:
        workspace_components = release.get("workspace_components")
        if not isinstance(workspace_components, list) or not workspace_components:
            raise ValueError("prompt release workspace components are invalid")
        workspace_ids: list[str] = []
        workspace_resources: set[str] = set()
        workspace_destinations: set[str] = set()
        for component in workspace_components:
            component_id, resource, destination, _raw = _validate_prompt_component(
                component, resource_reader=resource_reader, workspace=True,
            )
            assert destination is not None
            if resource in workspace_resources or destination in workspace_destinations:
                raise ValueError("prompt release workspace components are duplicated")
            workspace_resources.add(resource)
            workspace_destinations.add(destination)
            workspace_ids.append(component_id)
        if workspace_ids != sorted(workspace_ids) or len(workspace_ids) != len(set(workspace_ids)):
            raise ValueError("prompt release workspace component IDs are not canonical")
    _require_digest(release.get("release_sha256"), label="prompt release digest")
    if release["release_sha256"] != prompt_release_sha256(release):
        raise ValueError("prompt release digest mismatch")
    return release


def read_prompt_release_catalog() -> dict[str, Any]:
    value = _parse_json(_resource_bytes(PROMPT_RELEASE_CATALOG_RESOURCE))
    if not isinstance(value, dict) or set(value) != _PROMPT_CATALOG_KEYS:
        raise ValueError("prompt-release catalog fields are not exact")
    if value.get("schema_version") != PROMPT_RELEASE_CATALOG_SCHEMA:
        raise ValueError("prompt-release catalog schema is unsupported")
    _require_digest(value.get("catalog_sha256"), label="prompt-release catalog digest")
    if value["catalog_sha256"] != _catalog_sha256(value):
        raise ValueError("prompt-release catalog digest mismatch")
    releases = value.get("releases")
    if not isinstance(releases, list) or not releases:
        raise ValueError("prompt-release catalog releases are invalid")
    validated = [validate_prompt_release(item) for item in releases]
    release_ids = [item["release_id"] for item in validated]
    if release_ids != sorted(release_ids) or len(release_ids) != len(set(release_ids)):
        raise ValueError("prompt-release catalog release IDs are not canonical")
    return {**value, "releases": validated}


def read_prompt_release(release_id: str) -> dict[str, Any]:
    _require_identifier(release_id, label="prompt release ID")
    for release in read_prompt_release_catalog()["releases"]:
        if release["release_id"] == release_id:
            return deepcopy(release)
    raise ValueError("prompt release is not installed")


def resolve_installed_processing_profile(profile_id: str) -> dict[str, Any]:
    """Resolve the closed profile and verify its referenced prompt release.

    Command-line and workspace integration deliberately follow in Slice 2.
    """
    profile = read_processing_profile(profile_id)
    reference = profile["prompt_release"]
    release = read_prompt_release(reference["release_id"])
    if release["release_sha256"] != reference["release_sha256"]:
        raise ValueError("processing profile prompt-release digest mismatch")
    if profile["profile_id"] not in release["profile_ids"]:
        raise ValueError("prompt release does not allow processing profile")
    if profile["route"]["family"] not in release["route_families"]:
        raise ValueError("prompt release does not allow processing route")
    return profile


def resolve_sbe_authoring_binding(
    *,
    profile_id: str,
    profile_sha256: str,
    generation_manifest_sha256: str,
    route_family: str,
    environment: str,
    installed_version: Callable[[str], str] = distribution_version,
) -> dict[str, Any]:
    """Resolve the closed SBE half of an API-approved profile handoff.

    The caller provides references only.  This function loads the installed
    bundle itself, checks its canonical identity and package requirements, and
    returns a safe durable binding rather than a profile payload.
    """
    _require_identifier(profile_id, label="processing profile ID")
    _require_digest(profile_sha256, label="processing profile digest")
    _require_digest(
        generation_manifest_sha256, label="generation manifest digest",
    )
    _require_identifier(route_family, label="processing profile route family")
    _require_identifier(environment, label="processing profile environment")
    profile = resolve_installed_processing_profile(profile_id)
    if profile["profile_sha256"] != profile_sha256:
        raise ValueError("processing profile digest does not match installed profile")
    route = profile["route"]
    if route["family"] != route_family:
        raise ValueError("processing profile route family mismatch")
    if route["execution_mode"] != "live":
        raise ValueError("processing profile execution mode is unsupported")
    if environment not in profile["allowed_environments"]:
        raise ValueError("processing profile is not allowed in this environment")
    release = read_prompt_release(profile["prompt_release"]["release_id"])
    if environment not in release["allowed_environments"]:
        raise ValueError("prompt release is not allowed in this environment")
    descriptor = profile["worker_compatibility"]["sbe_authoring"]
    for requirement in descriptor["required_distributions"]:
        try:
            actual = installed_version(requirement["distribution"])
        except PackageNotFoundError as exc:
            raise ValueError("required SBE distribution is not installed") from exc
        if actual != requirement["version"]:
            raise ValueError("required SBE distribution version mismatch")
    return {
        "schema_version": PROCESSING_PROFILE_BINDING_SCHEMA,
        "processing_profile_id": profile["profile_id"],
        "processing_profile_sha256": profile["profile_sha256"],
        "generation_manifest_sha256": generation_manifest_sha256,
        "route": {
            "family": route["family"],
            "execution_mode": route["execution_mode"],
            "sbe_contract": route["sbe_contract"],
        },
        "selection_policy": profile["selection_policy"],
        "prompt_release": {
            "release_id": release["release_id"],
            "release_version": release["release_version"],
            "release_sha256": release["release_sha256"],
            "workspace_components": [
                {
                    "logical_name": component["destination"],
                    "sha256": component["sha256"],
                }
                for component in sorted(
                    release.get("workspace_components", []),
                    key=lambda component: component["destination"],
                )
            ],
        },
        "worker_compatibility": {
            "worker_role": descriptor["worker_role"],
            "compatibility_sha256": descriptor["compatibility_sha256"],
            "required_distributions": deepcopy(descriptor["required_distributions"]),
        },
    }


def resolve_prompt_release_stage(
    profile_id: str, *, stage: str,
) -> tuple[str, dict[str, Any]]:
    """Load the installed, profile-bound prompt text for one known stage."""
    if stage not in {"initial", "retry", "polish", "critic"}:
        raise ValueError("prompt release stage is unsupported")
    profile = resolve_installed_processing_profile(profile_id)
    release = read_prompt_release(profile["prompt_release"]["release_id"])
    component_by_id = {item["component_id"]: item for item in release["components"]}
    selected = release["stage_components"][stage]
    raw_components = [_canonical_prompt_asset(
        _prompt_resource_bytes(component_by_id[item]["resource"])
    ) for item in selected]
    # The release asset is LF-terminated for reproducible package identity;
    # the historical system message was not.  Preserve existing request bytes.
    rendered = "\n\n".join(raw.decode("utf-8").rstrip("\n") for raw in raw_components)
    return rendered, {
        "release_id": release["release_id"],
        "release_version": release["release_version"],
        "release_sha256": release["release_sha256"],
        "stage": stage,
        "components": [
            {
                "component_id": component_by_id[item]["component_id"],
                "sha256": component_by_id[item]["sha256"],
            }
            for item in selected
        ],
        "rendered_sha256": sha256(rendered.encode("utf-8")).hexdigest(),
    }


def resolve_prompt_release_workspace_assets(
    profile_id: str,
) -> list[tuple[str, bytes]] | None:
    """Return release-owned static workspace assets for one installed profile.

    A v1 release predates workspace-asset binding and deliberately returns
    ``None`` so its legacy workspace route remains byte-compatible. A v2
    release must carry the complete declared static asset set.
    """
    profile = resolve_installed_processing_profile(profile_id)
    release = read_prompt_release(profile["prompt_release"]["release_id"])
    if release["schema_version"] == PROMPT_RELEASE_SCHEMA:
        return None
    return [
        (component["destination"], _canonical_prompt_asset(
            _prompt_resource_bytes(component["resource"]),
        ))
        for component in release["workspace_components"]
    ]


def processing_profile_supports_tuple(
    profile: Mapping[str, Any], *, route_family: str, execution_mode: str,
    selection_policy: str,
) -> bool:
    """Return whether one *installed profile* explicitly owns this tuple."""
    validated = validate_processing_profile(profile)
    route = validated["route"]
    return (
        route["family"] == route_family
        and route["execution_mode"] == execution_mode
        and validated["selection_policy"] == selection_policy
    )


__all__ = [
    "PROCESSING_PROFILE_SCHEMA", "PROCESSING_PROFILE_CATALOG_SCHEMA",
    "PROMPT_RELEASE_SCHEMA", "PROMPT_RELEASE_WORKSPACE_SCHEMA", "PROMPT_RELEASE_CATALOG_SCHEMA",
    "WORKER_COMPATIBILITY_SCHEMA", "PROCESSING_PROFILE_BINDING_SCHEMA",
    "canonical_processing_profile_json", "processing_profile_sha256",
    "prompt_release_sha256", "worker_compatibility_sha256",
    "validate_worker_compatibility", "validate_processing_profile",
    "validate_prompt_release", "read_processing_profile_catalog",
    "read_processing_profile", "read_prompt_release_catalog", "read_prompt_release",
    "resolve_installed_processing_profile", "resolve_sbe_authoring_binding",
    "resolve_prompt_release_stage", "resolve_prompt_release_workspace_assets",
    "processing_profile_supports_tuple",
]
