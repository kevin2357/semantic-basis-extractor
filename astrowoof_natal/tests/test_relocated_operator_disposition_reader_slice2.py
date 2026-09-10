from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal.tests import (
    test_provider_pending_observation_idempotency as pending_fixtures,
    test_operator_retirement_contract as retirement_fixtures,
)
from astrowoof_natal_authoring.closure import (
    load_json,
    normalized_path,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.operator_disposition import (
    read_operator_disposition_assessment,
)
from astrowoof_natal_authoring.operator_retirement import (
    build_operator_retirement_request,
    execute_operator_retirement,
)
from astrowoof_natal_authoring.relocated_operator_disposition import (
    build_relocation_authority,
    canonical_root_sha256,
    read_relocated_operator_disposition_assessment,
    validate_relocated_assessment_pair,
)


def _bytes(root: Path) -> dict[str, bytes]:
    return {
        item.relative_to(root).as_posix(): item.read_bytes()
        for item in root.rglob("*") if item.is_file()
    }


class RelocatedOperatorDispositionReaderSlice2Tests(unittest.TestCase):
    def _authority(
        self, original: Path, relocated: Path, native_run_id: str,
        terminal_result_id: str | None = None,
    ) -> dict[str, object]:
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
            original_logical_root_sha256=canonical_root_sha256(
                normalized_path(original)
            ),
            restored_root_sha256=canonical_root_sha256(
                normalized_path(relocated)
            ),
            terminal_result_id=terminal_result_id,
            issued_at="2026-09-10T19:00:00Z",
            expires_at="2026-09-10T19:05:00Z",
            provider_io_permitted=False,
            workspace_mutation_permitted=False,
        )

    def _relocated(self, temporary: str) -> tuple[Path, Path, dict[str, object]]:
        original = Path(temporary, "original").resolve()
        original.mkdir(parents=True)
        pending_fixtures.TestProviderPendingObservationIdempotencySlice0().materialize(
            original
        )
        (original / "spend-consumption.lock").write_bytes(b"0")
        write_workspace_snapshot(original)
        relocated = Path(temporary, "operator", "checkpoint").resolve()
        shutil.copytree(original, relocated)
        native_run_id = load_json(relocated / "run.json")["run_id"]
        authority = self._authority(original, relocated, native_run_id)
        return original, relocated, authority

    def test_relocated_reader_preserves_exact_bytes_and_returns_bound_wrapper(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, relocated, authority = self._relocated(temporary)
            before = _bytes(relocated)
            wrapper = read_relocated_operator_disposition_assessment(
                relocated, authority=authority,
                assessed_at="2026-09-10T19:02:00Z",
            )
            validate_relocated_assessment_pair(authority, wrapper)
            self.assertEqual(before, _bytes(relocated))
            self.assertEqual(
                "provider_pending_known_identity",
                wrapper["assessment"]["native_custody_class"],
            )
            self.assertEqual("permitted", wrapper["assessment"]["quarantine_posture"])

    def test_ordinary_reader_still_rejects_relocated_workspace(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, relocated, _ = self._relocated(temporary)
            with self.assertRaisesRegex(ValueError, "original logical absolute path"):
                read_operator_disposition_assessment(relocated)

    def test_wrong_restored_root_and_changed_member_fail_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, relocated, authority = self._relocated(temporary)
            fields = {
                key: value for key, value in authority.items()
                if key != "authority_sha256"
            }
            fields["restored_root_sha256"] = "f" * 64
            wrong = build_relocation_authority(**fields)
            with self.assertRaisesRegex(ValueError, "Restored root"):
                read_relocated_operator_disposition_assessment(
                    relocated, authority=wrong,
                    assessed_at="2026-09-10T19:02:00Z",
                )
            (relocated / "run.json").write_bytes(
                (relocated / "run.json").read_bytes() + b" "
            )
            with self.assertRaisesRegex(ValueError, "incomplete or changed"):
                read_relocated_operator_disposition_assessment(
                    relocated, authority=authority,
                    assessed_at="2026-09-10T19:02:00Z",
                )

    def test_out_of_window_and_same_root_authority_fail_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            original, relocated, authority = self._relocated(temporary)
            with self.assertRaisesRegex(ValueError, "outside authority window"):
                read_relocated_operator_disposition_assessment(
                    relocated, authority=authority,
                    assessed_at="2026-09-10T19:06:00Z",
                )
            fields = {
                key: value for key, value in authority.items()
                if key != "authority_sha256"
            }
            fields["restored_root_sha256"] = canonical_root_sha256(
                normalized_path(original)
            )
            same_root = build_relocation_authority(**fields)
            with self.assertRaisesRegex(ValueError, "Restored root"):
                read_relocated_operator_disposition_assessment(
                    relocated, authority=same_root,
                    assessed_at="2026-09-10T19:02:00Z",
                )

    def test_authority_bound_terminal_result_is_exact_and_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            original = retirement_fixtures.TestOperatorRetirementContract().materialize(
                Path(temporary, "original").resolve()
            )
            request = build_operator_retirement_request(
                original, operator_audit_reference="api:relocated:terminal",
            )
            retired = execute_operator_retirement(
                original, request, committed_at="2026-09-10T18:59:00+00:00",
            )
            result_id = retired["native_result"]["result_id"]
            relocated = Path(temporary, "operator", "checkpoint").resolve()
            shutil.copytree(original, relocated)
            native_run_id = load_json(relocated / "run.json")["run_id"]
            authority = self._authority(
                original, relocated, native_run_id, result_id,
            )
            wrapper = read_relocated_operator_disposition_assessment(
                relocated, authority=authority,
                assessed_at="2026-09-10T19:02:00Z",
            )
            self.assertEqual(
                result_id, wrapper["assessment"]["terminal_evidence"]["result_id"]
            )
            self.assertEqual(
                "invocation_result",
                wrapper["assessment"]["terminal_evidence"]["discovery_mode"],
            )

            for wrong_id in (
                "result_0123456789abcdef01234567",
                "nres_000000000000000000000000",
            ):
                with self.subTest(result_id=wrong_id):
                    wrong = self._authority(
                        original, relocated, native_run_id, wrong_id,
                    )
                    with self.assertRaises((FileNotFoundError, ValueError)):
                        read_relocated_operator_disposition_assessment(
                            relocated, authority=wrong,
                            assessed_at="2026-09-10T19:02:00Z",
                        )


if __name__ == "__main__":
    unittest.main()
