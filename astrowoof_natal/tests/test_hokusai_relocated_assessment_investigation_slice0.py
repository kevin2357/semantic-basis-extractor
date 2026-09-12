from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from astrowoof_natal.tests import (
    test_provider_pending_observation_idempotency as pending_fixtures,
)
from astrowoof_natal_authoring.closure import (
    load_json,
    normalized_path,
    write_json_atomic,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.relocated_operator_disposition import (
    build_relocation_authority,
    canonical_root_sha256,
    read_relocated_operator_disposition_assessment,
)


HOKUSAI_LOGICAL_ROOT = "/work/runs/workspace-hokusai/sbe"
DETERMINISTIC_DOMAIN_ROOT = "/work/deterministic-domain"


class HokusaiRelocatedAssessmentInvestigationSlice0Tests(unittest.TestCase):
    def _relocated_provider_pending_workspace(
        self, temporary: str,
    ) -> tuple[Path, str]:
        original = Path(temporary, "native", "sbe").resolve()
        original.mkdir(parents=True)
        pending_fixtures.TestProviderPendingObservationIdempotencySlice0().materialize(
            original
        )
        (original / "spend-consumption.lock").write_bytes(b"0")
        state = load_json(original / "run.json")
        state["workspace_contract"] = {
            "mode": "stable_logical_absolute_path",
            "logical_root": HOKUSAI_LOGICAL_ROOT,
        }
        write_json_atomic(original / "run.json", state)
        write_workspace_snapshot(original)
        manifest = load_json(original / "workspace-snapshot.json")
        manifest["logical_root"] = HOKUSAI_LOGICAL_ROOT
        write_json_atomic(original / "workspace-snapshot.json", manifest)

        relocated = Path(temporary, "operator", "request", "sbe").resolve()
        shutil.copytree(original, relocated)
        return relocated, state["run_id"]

    def _authority(
        self, *, relocated: Path, native_run_id: str, original_root: str,
    ) -> dict[str, object]:
        return build_relocation_authority(
            request_id="e80e824c-fe88-4753-9f55-d2ff42aeb1c0",
            api_run_id="00667fb9-c068-415e-a045-8d4059ac549e",
            job_id="3c1dc0cd-3169-4542-8f9b-40305d8dcf3b",
            native_run_id=native_run_id,
            checkpoint_id="b7ceea14-cb07-4366-b944-31bceb2c5159",
            checkpoint_generation=4,
            checkpoint_contract="astrowoof.sbe-workspace-checkpoint.v1",
            compatibility_identity="astrowoof.qa.sbe0460.v1",
            archive_sha256=(
                "79b771d0ce02a7c1e20fb6d177e4ac0ae62f1f5608bfb877c0480762792cde86"
            ),
            inventory_sha256=(
                "6351e48ca7e6ad27a45d4d38dc4d0bf7861a900f1e822add1df0360ddd982d3b"
            ),
            original_logical_root_sha256=canonical_root_sha256(original_root),
            restored_root_sha256=canonical_root_sha256(normalized_path(relocated)),
            terminal_result_id=None,
            issued_at="2026-09-12T10:47:54Z",
            expires_at="2026-09-12T10:49:54Z",
            provider_io_permitted=False,
            workspace_mutation_permitted=False,
        )

    def test_matching_sbe_logical_root_returns_provider_pending_assessment(self):
        with tempfile.TemporaryDirectory() as temporary:
            relocated, native_run_id = self._relocated_provider_pending_workspace(
                temporary
            )
            authority = self._authority(
                relocated=relocated,
                native_run_id=native_run_id,
                original_root=HOKUSAI_LOGICAL_ROOT,
            )

            wrapper = read_relocated_operator_disposition_assessment(
                relocated,
                authority=authority,
                assessed_at="2026-09-12T10:47:55Z",
            )

            self.assertEqual(
                "provider_pending_known_identity",
                wrapper["assessment"]["native_custody_class"],
            )
            self.assertEqual("permitted", wrapper["assessment"]["quarantine_posture"])

    def test_deterministic_domain_authority_refuses_at_original_root_binding(self):
        with tempfile.TemporaryDirectory() as temporary:
            relocated, native_run_id = self._relocated_provider_pending_workspace(
                temporary
            )
            authority = self._authority(
                relocated=relocated,
                native_run_id=native_run_id,
                original_root=DETERMINISTIC_DOMAIN_ROOT,
            )

            with self.assertRaisesRegex(
                ValueError,
                "Original logical root does not match relocation authority",
            ):
                read_relocated_operator_disposition_assessment(
                    relocated,
                    authority=authority,
                    assessed_at="2026-09-12T10:47:55Z",
                )


if __name__ == "__main__":
    unittest.main()
