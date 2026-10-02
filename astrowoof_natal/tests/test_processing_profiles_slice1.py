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
    validate_processing_profile,
    validate_prompt_release,
)


PROFILE_ID = "astrowoof.exact_natal.live.compat.v1"
RELEASE_ID = "astrowoof.authoring.compat.v1"


class ProcessingProfileSlice1Tests(unittest.TestCase):
    def test_installed_catalogs_resolve_the_one_compatibility_binding(self) -> None:
        profiles = read_processing_profile_catalog()
        releases = read_prompt_release_catalog()
        self.assertEqual(1, len(profiles["profiles"]))
        self.assertEqual(1, len(releases["releases"]))

        profile = resolve_installed_processing_profile(PROFILE_ID)
        release = read_prompt_release(RELEASE_ID)
        self.assertEqual(PROCESSING_PROFILE_SCHEMA, profile["schema_version"])
        self.assertEqual(PROMPT_RELEASE_SCHEMA, release["schema_version"])
        self.assertEqual(RELEASE_ID, profile["prompt_release"]["release_id"])
        self.assertEqual(release["release_sha256"], profile["prompt_release"]["release_sha256"])
        self.assertEqual("legacy_atomic.v1", profile["selection_policy"])
        self.assertEqual("live", profile["route"]["execution_mode"])
        self.assertEqual("interactive", profile["sbe"]["provider_service_level"])

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


if __name__ == "__main__":
    unittest.main()
