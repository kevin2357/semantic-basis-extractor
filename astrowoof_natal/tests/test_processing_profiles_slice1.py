from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import unittest

from astrowoof_natal_authoring.processing_profiles import (
    PROCESSING_PROFILE_SCHEMA,
    PROMPT_RELEASE_SCHEMA,
    processing_profile_sha256,
    processing_profile_supports_tuple,
    read_processing_profile,
    read_processing_profile_catalog,
    read_prompt_release,
    read_prompt_release_catalog,
    resolve_installed_processing_profile,
    resolve_prompt_release_stage,
    resolve_prompt_release_workspace_assets,
    resolve_sbe_authoring_binding,
    validate_processing_profile,
    validate_prompt_release,
    validate_worker_compatibility,
    worker_compatibility_sha256,
)


PROFILE_ID = "astrowoof.exact_natal.live.compat.v1"
AXIS_AWARE_PROFILE_ID = "astrowoof.exact_natal.live.axisawaresbe.v1"
COMPAT_V2_PROFILE_ID = "astrowoof.exact_natal.live.compat.v2"
AXIS_AWARE_V2_PROFILE_ID = "astrowoof.exact_natal.live.axisawaresbe.v2"
BOUNDED_PROFILE_ID = "astrowoof.bounded_natal.live.stable_facts.v1"
BOUNDED_V2_PROFILE_ID = "astrowoof.bounded_natal.live.stable_facts.v2"
RELEASE_ID = "astrowoof.authoring.compat.v1"
EDITORIAL_RELEASE_ID = "astrowoof.authoring.editorial.v2"
COMPAT_V2_RELEASE_ID = "astrowoof.authoring.compat.v2"
EDITORIAL_V3_RELEASE_ID = "astrowoof.authoring.editorial.v3"
BOUNDED_RELEASE_ID = "astrowoof.authoring.bounded_stable_facts.v1"
BOUNDED_V2_RELEASE_ID = "astrowoof.authoring.bounded_stable_facts.v2"


class ProcessingProfileSlice1Tests(unittest.TestCase):
    def test_installed_catalogs_resolve_compatibility_and_axis_aware_bindings(self) -> None:
        profiles = read_processing_profile_catalog()
        releases = read_prompt_release_catalog()
        self.assertEqual(
            [
                BOUNDED_PROFILE_ID,
                BOUNDED_V2_PROFILE_ID,
                AXIS_AWARE_PROFILE_ID,
                AXIS_AWARE_V2_PROFILE_ID,
                PROFILE_ID,
                COMPAT_V2_PROFILE_ID,
            ],
            [profile["profile_id"] for profile in profiles["profiles"]],
        )
        self.assertEqual(
            [
                BOUNDED_RELEASE_ID,
                BOUNDED_V2_RELEASE_ID,
                RELEASE_ID,
                COMPAT_V2_RELEASE_ID,
                EDITORIAL_RELEASE_ID,
                EDITORIAL_V3_RELEASE_ID,
            ],
            [release["release_id"] for release in releases["releases"]],
        )

        profile = resolve_installed_processing_profile(PROFILE_ID)
        axis_aware = resolve_installed_processing_profile(AXIS_AWARE_PROFILE_ID)
        release = read_prompt_release(RELEASE_ID)
        self.assertEqual(PROCESSING_PROFILE_SCHEMA, profile["schema_version"])
        self.assertEqual(PROMPT_RELEASE_SCHEMA, release["schema_version"])
        self.assertEqual(RELEASE_ID, profile["prompt_release"]["release_id"])
        self.assertEqual(release["release_sha256"], profile["prompt_release"]["release_sha256"])
        self.assertEqual("legacy_atomic.v1", profile["selection_policy"])
        self.assertEqual("axis_aware.v1", axis_aware["selection_policy"])
        self.assertNotEqual(profile["profile_sha256"], axis_aware["profile_sha256"])
        self.assertEqual(profile["route"], axis_aware["route"])
        self.assertEqual(profile["sbe"], axis_aware["sbe"])
        self.assertNotEqual(profile["prompt_release"], axis_aware["prompt_release"])
        self.assertEqual(EDITORIAL_RELEASE_ID, axis_aware["prompt_release"]["release_id"])
        self.assertEqual(
            profile["worker_compatibility"]["deterministic_runtime"],
            axis_aware["worker_compatibility"]["deterministic_runtime"],
        )
        self.assertNotEqual(
            profile["worker_compatibility"]["sbe_authoring"],
            axis_aware["worker_compatibility"]["sbe_authoring"],
        )
        self.assertEqual("live", profile["route"]["execution_mode"])
        self.assertEqual("interactive", profile["sbe"]["provider_service_level"])

        bounded = resolve_installed_processing_profile(BOUNDED_PROFILE_ID)
        self.assertEqual("bounded_natal", bounded["route"]["family"])
        self.assertEqual("bounded", bounded["deterministic_runtime"]["birth_time_mode"])
        self.assertEqual(
            "woofmapped_bounded_astrology.v0@0.1.0",
            bounded["deterministic_runtime"]["projection_contract"],
        )
        self.assertEqual(BOUNDED_RELEASE_ID, bounded["prompt_release"]["release_id"])

        bounded_v2 = resolve_installed_processing_profile(BOUNDED_V2_PROFILE_ID)
        bounded_v2_release = read_prompt_release(BOUNDED_V2_RELEASE_ID)
        self.assertEqual(bounded["route"], bounded_v2["route"])
        self.assertEqual(bounded["selection_policy"], bounded_v2["selection_policy"])
        self.assertEqual(
            "0.4.71",
            bounded_v2["worker_compatibility"]["sbe_authoring"]
            ["required_distributions"][0]["version"],
        )
        self.assertEqual(
            BOUNDED_V2_RELEASE_ID, bounded_v2["prompt_release"]["release_id"],
        )
        self.assertEqual([BOUNDED_V2_PROFILE_ID], bounded_v2_release["profile_ids"])
        self.assertNotEqual(bounded["profile_sha256"], bounded_v2["profile_sha256"])

    def test_v2_profiles_preserve_semantics_but_require_0469(self) -> None:
        compat_v1 = read_processing_profile(PROFILE_ID)
        axis_v1 = read_processing_profile(AXIS_AWARE_PROFILE_ID)
        compat_v2 = read_processing_profile(COMPAT_V2_PROFILE_ID)
        axis_v2 = read_processing_profile(AXIS_AWARE_V2_PROFILE_ID)

        for earlier, later, release_id in (
            (compat_v1, compat_v2, COMPAT_V2_RELEASE_ID),
            (axis_v1, axis_v2, EDITORIAL_V3_RELEASE_ID),
        ):
            self.assertEqual(earlier["route"], later["route"])
            self.assertEqual(earlier["selection_policy"], later["selection_policy"])
            self.assertEqual(earlier["sbe"], later["sbe"])
            self.assertEqual(
                "0.4.69",
                later["worker_compatibility"]["sbe_authoring"]
                ["required_distributions"][0]["version"],
            )
            self.assertEqual(release_id, later["prompt_release"]["release_id"])
            self.assertNotEqual(earlier["profile_sha256"], later["profile_sha256"])

        self.assertEqual("0.4.66", compat_v1["worker_compatibility"]["sbe_authoring"]["required_distributions"][0]["version"])
        self.assertEqual("0.4.68", axis_v1["worker_compatibility"]["sbe_authoring"]["required_distributions"][0]["version"])
        self.assertEqual(
            resolve_prompt_release_stage(PROFILE_ID, stage="initial")[0],
            resolve_prompt_release_stage(COMPAT_V2_PROFILE_ID, stage="initial")[0],
        )
        self.assertEqual(
            resolve_prompt_release_workspace_assets(AXIS_AWARE_PROFILE_ID),
            resolve_prompt_release_workspace_assets(AXIS_AWARE_V2_PROFILE_ID),
        )

    def test_compatibility_profile_owns_only_its_explicit_tuple(self) -> None:
        profile = read_processing_profile(PROFILE_ID)
        self.assertTrue(processing_profile_supports_tuple(
            profile,
            route_family="exact_natal",
            execution_mode="live",
            selection_policy="legacy_atomic.v1",
        ))
        self.assertFalse(processing_profile_supports_tuple(
            profile,
            route_family="bounded_natal",
            execution_mode="live",
            selection_policy="legacy_atomic.v1",
        ))
        self.assertFalse(processing_profile_supports_tuple(
            profile,
            route_family="exact_natal",
            execution_mode="batch",
            selection_policy="legacy_atomic.v1",
        ))
        self.assertFalse(processing_profile_supports_tuple(
            profile,
            route_family="exact_natal",
            execution_mode="live",
            selection_policy="axis_aware.v1",
        ))
        axis_aware = read_processing_profile(AXIS_AWARE_PROFILE_ID)
        self.assertTrue(processing_profile_supports_tuple(
            axis_aware,
            route_family="exact_natal",
            execution_mode="live",
            selection_policy="axis_aware.v1",
        ))
        self.assertFalse(processing_profile_supports_tuple(
            axis_aware,
            route_family="exact_natal",
            execution_mode="live",
            selection_policy="legacy_atomic.v1",
        ))

    def test_bounded_profile_tuple_requires_bounded_projection_contract(self) -> None:
        profile = deepcopy(read_processing_profile(PROFILE_ID))
        profile["profile_id"] = "astrowoof.bounded_natal.live.stable_facts.v1"
        profile["route"] = {
            "family": "bounded_natal",
            "execution_mode": "live",
            "sbe_contract": "astrowoof.bounded_natal.authoring_run.v2",
        }
        profile["selection_policy"] = "stable_facts_only.v1"
        profile["deterministic_runtime"]["birth_time_mode"] = "bounded"
        profile["deterministic_runtime"]["projection_contract"] = (
            "woofmapped_bounded_astrology.v0@0.1.0"
        )
        profile["profile_sha256"] = processing_profile_sha256(profile)
        validated = validate_processing_profile(profile)
        self.assertTrue(processing_profile_supports_tuple(
            validated,
            route_family="bounded_natal",
            execution_mode="live",
            selection_policy="stable_facts_only.v1",
        ))

        invalid = deepcopy(profile)
        invalid["deterministic_runtime"]["projection_contract"] = (
            "woofmapped_astrology.v0@0.1.0"
        )
        invalid["profile_sha256"] = processing_profile_sha256(invalid)
        with self.assertRaisesRegex(ValueError, "projection contract"):
            validate_processing_profile(invalid)

    def test_profile_rejects_injected_secrets_and_changed_identity(self) -> None:
        profile = read_processing_profile(PROFILE_ID)
        injected = deepcopy(profile)
        injected["sbe"]["openai_api_key"] = "not-a-profile-field"
        injected["profile_sha256"] = processing_profile_sha256(injected)
        with self.assertRaisesRegex(ValueError, "SBE fragment"):
            validate_processing_profile(injected)

        changed = deepcopy(profile)
        changed["sbe"]["max_workers"] = 7
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            validate_processing_profile(changed)

    def test_qualified_worker_descriptors_are_closed_and_profile_bound(self) -> None:
        profile = read_processing_profile(PROFILE_ID)
        compatibility = profile["worker_compatibility"]
        self.assertEqual(
            {"deterministic_runtime", "sbe_authoring"}, set(compatibility),
        )
        for role, descriptor in compatibility.items():
            self.assertEqual(role, validate_worker_compatibility(descriptor)["worker_role"])

        changed = deepcopy(profile)
        descriptor = changed["worker_compatibility"]["sbe_authoring"]
        descriptor["required_distributions"][0]["version"] = "0.4.68"
        descriptor["compatibility_sha256"] = worker_compatibility_sha256(descriptor)
        changed["profile_sha256"] = processing_profile_sha256(changed)
        self.assertNotEqual(profile["profile_sha256"], changed["profile_sha256"])
        validate_processing_profile(changed)

        role_mismatch = deepcopy(profile)
        role_mismatch["worker_compatibility"]["sbe_authoring"]["worker_role"] = "deterministic_runtime"
        role_mismatch["worker_compatibility"]["sbe_authoring"]["compatibility_sha256"] = worker_compatibility_sha256(
            role_mismatch["worker_compatibility"]["sbe_authoring"],
        )
        role_mismatch["profile_sha256"] = processing_profile_sha256(role_mismatch)
        with self.assertRaisesRegex(ValueError, "role mismatch"):
            validate_processing_profile(role_mismatch)

    def test_prompt_assets_are_lf_utf8_and_digest_bound(self) -> None:
        release = read_prompt_release(RELEASE_ID)
        component = release["components"][0]
        expected = (
            "You are the author of one bounded AstroWoof authoring pass. "
            "Treat each supplied card or summary as an independent finished "
            "writing assignment while keeping the dog recognizable across the "
            "pass. Read START HERE.md first and follow the workspace's own "
            "guidance as authoritative. Do not borrow wording, templates, or "
            "content from any prior AstroWoof deck. Return only the field "
            "values required by the response schema. Do not include marker "
            "comments in field values.\n"
        ).encode("utf-8")
        self.assertEqual(sha256(expected).hexdigest(), component["sha256"])

        with self.assertRaisesRegex(ValueError, "canonical LF"):
            validate_prompt_release(
                release,
                resource_reader=lambda _resource: expected.replace(b"\n", b"\r\n"),
            )
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            validate_prompt_release(
                release,
                resource_reader=lambda _resource: expected.replace(b"bounded", b"focused"),
            )

    def test_unknown_installed_ids_fail_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "not installed"):
            read_processing_profile("astrowoof.bounded_natal.live.future.v1")
        with self.assertRaisesRegex(ValueError, "not installed"):
            read_prompt_release("astrowoof.authoring.future.v1")

    def test_sbe_binding_requires_exact_installed_profile_and_packages(self) -> None:
        profiles = {
            profile_id: read_processing_profile(profile_id)
            for profile_id in (PROFILE_ID, AXIS_AWARE_PROFILE_ID)
        }
        for profile_id, profile in profiles.items():
            versions = {
                item["distribution"]: item["version"]
                for item in profile["worker_compatibility"]["sbe_authoring"]["required_distributions"]
            }
            binding = resolve_sbe_authoring_binding(
                profile_id=profile_id,
                profile_sha256=profile["profile_sha256"],
                generation_manifest_sha256="a" * 64,
                route_family="exact_natal",
                environment="qa",
                installed_version=versions.__getitem__,
            )
            self.assertEqual(profile_id, binding["processing_profile_id"])
            self.assertEqual(profile["selection_policy"], binding["selection_policy"])
            self.assertEqual("sbe_authoring", binding["worker_compatibility"]["worker_role"])
            expected_release = (
                EDITORIAL_RELEASE_ID
                if profile_id == AXIS_AWARE_PROFILE_ID
                else RELEASE_ID
            )
            self.assertEqual(expected_release, binding["prompt_release"]["release_id"])
            expected_inventory = (
                [
                    {
                        "logical_name": "AUTHORING BRIEF.md",
                        "sha256": "8097cc2639212f82a0ff2b916baacd3d4f7bdaeca3cce22c0ada4d10db659bbc",
                    },
                    {
                        "logical_name": "GUIDING LIGHTS.md",
                        "sha256": "ac1625fed0e6791b7c39c79610e104ba9a99ea720f4ecbe5cba55a8a070e7d08",
                    },
                ]
                if profile_id == AXIS_AWARE_PROFILE_ID else []
            )
            self.assertEqual(
                expected_inventory,
                binding["prompt_release"]["workspace_components"],
            )

        profile = profiles[PROFILE_ID]
        versions = {
            item["distribution"]: item["version"]
            for item in profile["worker_compatibility"]["sbe_authoring"]["required_distributions"]
        }

        with self.assertRaisesRegex(ValueError, "digest"):
            resolve_sbe_authoring_binding(
                profile_id=PROFILE_ID, profile_sha256="b" * 64,
                generation_manifest_sha256="a" * 64, route_family="exact_natal",
                environment="qa", installed_version=versions.__getitem__,
            )
        with self.assertRaisesRegex(ValueError, "version mismatch"):
            resolve_sbe_authoring_binding(
                profile_id=PROFILE_ID, profile_sha256=profile["profile_sha256"],
                generation_manifest_sha256="a" * 64, route_family="exact_natal",
                environment="qa", installed_version=lambda _name: "0.0.0",
            )

    def test_bounded_binding_is_installed_route_and_prompt_specific(self) -> None:
        profile = read_processing_profile(BOUNDED_PROFILE_ID)
        versions = {
            item["distribution"]: item["version"]
            for item in profile["worker_compatibility"]["sbe_authoring"]
            ["required_distributions"]
        }
        binding = resolve_sbe_authoring_binding(
            profile_id=BOUNDED_PROFILE_ID,
            profile_sha256=profile["profile_sha256"],
            generation_manifest_sha256="a" * 64,
            route_family="bounded_natal",
            environment="qa",
            installed_version=versions.__getitem__,
        )
        self.assertEqual("bounded_natal", binding["route"]["family"])
        self.assertEqual(
            "astrowoof.bounded_natal.authoring_run.v2",
            binding["route"]["sbe_contract"],
        )
        self.assertEqual(BOUNDED_RELEASE_ID, binding["prompt_release"]["release_id"])
        self.assertEqual(
            [
                {
                    "logical_name": "AUTHORING BRIEF.md",
                    "sha256": "8cd6ebf406b288bdc0897cac9b55a811523e89f91d3c8508a038b5767273c09e",
                },
                {
                    "logical_name": "GUIDING LIGHTS.md",
                    "sha256": "39f3d75f6e3df58d36c20b74c073c7d4b8d0697f64bda313df6b1258d6e01fc8",
                },
            ],
            binding["prompt_release"]["workspace_components"],
        )

    def test_historical_compatibility_profile_is_preserved_and_refuses_current_worker(self) -> None:
        profile = read_processing_profile(PROFILE_ID)
        self.assertEqual(
            "28a92d24dbbc10597c11c5bca0309ee9ea7aad5168069138f5e76dd90e32bf7a",
            profile["profile_sha256"],
        )
        descriptor = profile["worker_compatibility"]["sbe_authoring"]
        self.assertEqual("0.4.66", descriptor["required_distributions"][0]["version"])
        with self.assertRaisesRegex(ValueError, "version mismatch"):
            resolve_sbe_authoring_binding(
                profile_id=PROFILE_ID,
                profile_sha256=profile["profile_sha256"],
                generation_manifest_sha256="a" * 64,
                route_family="exact_natal",
                environment="qa",
                installed_version=lambda name: {
                    "astrowoof-natal-authoring": "0.4.68",
                    "semantic-projection-core": "0.11.1",
                }[name],
            )

    def test_profile_stage_resolution_preserves_legacy_system_message_bytes(self) -> None:
        prompt, provenance = resolve_prompt_release_stage(PROFILE_ID, stage="initial")
        self.assertEqual(
            "You are the author of one bounded AstroWoof authoring pass. "
            "Treat each supplied card or summary as an independent finished "
            "writing assignment while keeping the dog recognizable across the "
            "pass. Read START HERE.md first and follow the workspace's own "
            "guidance as authoritative. Do not borrow wording, templates, or "
            "content from any prior AstroWoof deck. Return only the field "
            "values required by the response schema. Do not include marker "
            "comments in field values.",
            prompt,
        )
        self.assertEqual("astrowoof.authoring.compat.v1", provenance["release_id"])
        self.assertEqual("initial", provenance["stage"])

    def test_editorial_release_binds_complete_static_workspace_guidance(self) -> None:
        prompt, provenance = resolve_prompt_release_stage(
            AXIS_AWARE_PROFILE_ID, stage="initial",
        )
        self.assertEqual(
            resolve_prompt_release_stage(PROFILE_ID, stage="initial")[0], prompt,
        )
        self.assertEqual(EDITORIAL_RELEASE_ID, provenance["release_id"])
        self.assertIsNone(resolve_prompt_release_workspace_assets(PROFILE_ID))

        assets = dict(resolve_prompt_release_workspace_assets(AXIS_AWARE_PROFILE_ID) or [])
        self.assertEqual({"AUTHORING BRIEF.md", "GUIDING LIGHTS.md"}, set(assets))
        self.assertIn(
            b"This changes audience and tone, never astrology density",
            assets["AUTHORING BRIEF.md"],
        )
        self.assertIn(
            b"Audience changes address and tone, never\n  astrology density",
            assets["GUIDING LIGHTS.md"],
        )

    def test_bounded_release_owns_the_actual_stage_specific_provider_prompts(self) -> None:
        expected = {
            "initial": "Write every editorial field from the bounded packet.",
            "retry": "Rewrite the complete assigned editorial pass after local QA rejection.",
            "polish": "Polish prose only.",
            "critic": "Critique the current deck without rewriting it.",
        }
        for stage, opening in expected.items():
            prompt, provenance = resolve_prompt_release_stage(
                BOUNDED_PROFILE_ID, stage=stage,
            )
            self.assertTrue(prompt.startswith(opening))
            self.assertIn("Do not infer a representative birth time", prompt)
            self.assertEqual(BOUNDED_RELEASE_ID, provenance["release_id"])
            self.assertEqual(stage, provenance["stage"])


if __name__ == "__main__":
    unittest.main()
