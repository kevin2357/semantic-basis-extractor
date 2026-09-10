from __future__ import annotations

import unittest

from astrowoof_natal_authoring.operator_disposition_fixtures import (
    read_operator_disposition_fixtures,
)
from astrowoof_natal_authoring.relocated_operator_disposition import (
    build_relocated_assessment,
    build_relocation_authority,
    canonical_logical_root,
    canonical_root_sha256,
    read_relocated_assessment_schema,
    read_relocation_authority_schema,
    validate_relocated_assessment,
    validate_relocated_assessment_pair,
    validate_relocation_authority,
)


class RelocatedOperatorDispositionContractSlice1Tests(unittest.TestCase):
    def _authority(self, native_run_id: str) -> dict[str, object]:
        return build_relocation_authority(
            request_id="11111111-1111-4111-8111-111111111111",
            api_run_id="22222222-2222-4222-8222-222222222222",
            job_id="33333333-3333-4333-8333-333333333333",
            native_run_id=native_run_id,
            checkpoint_id="44444444-4444-4444-8444-444444444444",
            checkpoint_generation=7,
            checkpoint_contract="astrowoof.sbe-workspace-checkpoint.v1",
            compatibility_identity="astrowoof.qa.fixture.v1",
            archive_sha256="a" * 64,
            inventory_sha256="b" * 64,
            original_logical_root_sha256=canonical_root_sha256("/work/runs/original/sbe"),
            restored_root_sha256=canonical_root_sha256("/work/operator/request/sbe"),
            terminal_result_id=None,
            issued_at="2026-09-10T19:00:00Z",
            expires_at="2026-09-10T19:05:00Z",
            provider_io_permitted=False,
            workspace_mutation_permitted=False,
        )

    def test_authority_and_wrapper_are_canonical_and_replay_stable(self):
        assessment = read_operator_disposition_fixtures()["fixtures"][0]
        authority = self._authority(assessment["native_run_id"])
        wrapper = build_relocated_assessment(
            authority=authority,
            assessed_at="2026-09-10T19:02:00Z",
            assessment=assessment,
        )
        self.assertEqual(authority, validate_relocation_authority(authority))
        self.assertEqual(wrapper, validate_relocated_assessment(wrapper))
        self.assertEqual((authority, wrapper), validate_relocated_assessment_pair(authority, wrapper))
        self.assertEqual(
            wrapper,
            build_relocated_assessment(
                authority=authority,
                assessed_at="2026-09-10T19:02:00Z",
                assessment=assessment,
            ),
        )

    def test_changed_authority_and_out_of_window_assessment_fail_closed(self):
        assessment = read_operator_disposition_fixtures()["fixtures"][0]
        authority = self._authority(assessment["native_run_id"])
        changed = dict(authority)
        changed["checkpoint_generation"] = 8
        with self.assertRaisesRegex(ValueError, "authority digest"):
            validate_relocation_authority(changed)
        with self.assertRaisesRegex(ValueError, "outside authority window"):
            build_relocated_assessment(
                authority=authority,
                assessed_at="2026-09-10T19:06:00Z",
                assessment=assessment,
            )

    def test_capabilities_times_and_nested_identity_fail_closed(self):
        assessment = read_operator_disposition_fixtures()["fixtures"][0]
        fields = self._authority(assessment["native_run_id"])
        fields = {key: value for key, value in fields.items() if key != "authority_sha256"}
        fields["provider_io_permitted"] = True
        with self.assertRaisesRegex(ValueError, "capabilities"):
            build_relocation_authority(**fields)
        fields["provider_io_permitted"] = False
        fields["issued_at"] = "2026-09-10T13:00:00-06:00"
        with self.assertRaisesRegex(ValueError, "canonical UTC"):
            build_relocation_authority(**fields)
        wrong = self._authority("different_native_run")
        with self.assertRaisesRegex(ValueError, "native identity changed"):
            build_relocated_assessment(
                authority=wrong,
                assessed_at="2026-09-10T19:02:00Z",
                assessment=assessment,
            )

    def test_packaged_schemas_are_closed(self):
        authority = read_relocation_authority_schema()
        wrapper = read_relocated_assessment_schema()
        self.assertFalse(authority["additionalProperties"])
        self.assertFalse(wrapper["additionalProperties"])
        self.assertEqual(
            "astrowoof.operator_disposition_relocation_authority.v1",
            authority["properties"]["schema_version"]["const"],
        )

    def test_root_identity_is_platform_independent_and_lexically_canonical(self):
        self.assertEqual(
            "posix:/work/runs/sbe",
            canonical_logical_root("/work//runs/./x/../sbe/"),
        )
        self.assertEqual(
            canonical_root_sha256("C:\\Work\\Runs\\SBE"),
            canonical_root_sha256("c:/work/runs/./sbe/"),
        )
        self.assertNotEqual(
            canonical_root_sha256("/Work/Runs/SBE"),
            canonical_root_sha256("/work/runs/sbe"),
        )
        with self.assertRaisesRegex(ValueError, "absolute"):
            canonical_root_sha256("relative/workspace")
        with self.assertRaisesRegex(ValueError, "absolute"):
            canonical_root_sha256("C:")
        with self.assertRaisesRegex(ValueError, "escapes"):
            canonical_root_sha256("/../workspace")
        for value in ("/work/with\ttab", "/work/with\x1bescape", "/work/with\x7fdelete"):
            with self.subTest(value=repr(value)):
                with self.assertRaisesRegex(ValueError, "invalid"):
                    canonical_root_sha256(value)

    def test_pair_validation_rejects_rebound_wrapper(self):
        assessment = read_operator_disposition_fixtures()["fixtures"][0]
        authority = self._authority(assessment["native_run_id"])
        wrapper = build_relocated_assessment(
            authority=authority,
            assessed_at="2026-09-10T19:02:00Z",
            assessment=assessment,
        )
        other = self._authority(assessment["native_run_id"])
        other_body = {key: value for key, value in other.items() if key != "authority_sha256"}
        other_body["checkpoint_generation"] = 8
        other = build_relocation_authority(**other_body)
        with self.assertRaisesRegex(ValueError, "does not match"):
            validate_relocated_assessment_pair(other, wrapper)


if __name__ == "__main__":
    unittest.main()
