from __future__ import annotations

import inspect
import shutil
import tempfile
import unittest
from pathlib import Path

import astrowoof_natal_authoring as public
from astrowoof_natal.tests import (
    test_operator_retirement_contract as retirement_fixtures,
)
from astrowoof_natal_authoring.closure import (
    resume_run,
    write_workspace_snapshot,
)
from astrowoof_natal_authoring.native_transitions import (
    publish_native_execution_result,
)
from astrowoof_natal_authoring.operator_retirement import (
    build_operator_retirement_request,
)
from astrowoof_natal_authoring.post_fan_in_contracts import (
    commit_local_work_progress,
    inspect_post_fan_in_lifecycle,
)
from astrowoof_natal_authoring.reconciliation import (
    ProviderReconciliationAdapters,
    reconcile_authoring_provider_cycle,
)
from astrowoof_natal_authoring.relocated_operator_disposition import (
    read_relocated_operator_disposition_assessment,
)


OBSERVED_AT = "2026-09-10T19:02:00+00:00"


def _bytes(root: Path) -> dict[str, bytes]:
    return {
        item.relative_to(root).as_posix(): item.read_bytes()
        for item in root.rglob("*") if item.is_file()
    }


class _ForbiddenProvider:
    name = "openai"
    api_key = "fixture-secret"
    base_url = "https://provider.invalid/v1"
    http_timeout_seconds = 1.0
    max_transport_retries = 0

    @property
    def responses(self):
        return self

    def author(self, *args, **kwargs):
        raise AssertionError("provider must not be reached")

    def _request_with_retry(self, *args, **kwargs):
        raise AssertionError("provider must not be reached")


class RelocatedOperatorDispositionCapabilityFenceSlice3Tests(unittest.TestCase):
    def _roots(self, temporary: str) -> tuple[Path, Path]:
        original = Path(temporary, "original").resolve()
        retirement_fixtures.TestOperatorRetirementContract().materialize(original)
        lock = original / "spend-consumption.lock"
        if not lock.exists():
            lock.write_bytes(b"0")
        write_workspace_snapshot(original)
        relocated = Path(temporary, "operator", "checkpoint").resolve()
        shutil.copytree(original, relocated)
        return original, relocated

    def _assert_refused_without_mutation(self, root: Path, operation) -> None:
        before = _bytes(root)
        with self.assertRaisesRegex(ValueError, "original logical absolute path"):
            operation()
        self.assertEqual(before, _bytes(root))

    def test_relocation_authority_is_exclusive_to_the_read_only_reader(self):
        self.assertIn(
            "authority",
            inspect.signature(read_relocated_operator_disposition_assessment).parameters,
        )
        for operation in (
            resume_run,
            reconcile_authoring_provider_cycle,
            commit_local_work_progress,
            publish_native_execution_result,
            build_operator_retirement_request,
            write_workspace_snapshot,
        ):
            with self.subTest(operation=operation.__name__):
                parameters = inspect.signature(operation).parameters
                self.assertNotIn("authority", parameters)
                self.assertNotIn("relocation_authority", parameters)
        self.assertFalse(hasattr(public, "write_workspace_snapshot"))
        self.assertFalse(hasattr(public, "publish_checkpoint"))
        self.assertFalse(hasattr(public, "native_suspension"))

    def test_resume_reconciliation_and_local_work_reject_relocated_copy(self):
        with tempfile.TemporaryDirectory() as temporary:
            original, relocated = self._roots(temporary)
            prior = inspect_post_fan_in_lifecycle(
                original, observed_at=OBSERVED_AT,
                native_exclusive_access="established",
            )
            self._assert_refused_without_mutation(
                relocated,
                lambda: resume_run(
                    run_dir=relocated, provider=_ForbiddenProvider(), max_attempts=1,
                ),
            )
            self._assert_refused_without_mutation(
                relocated,
                lambda: reconcile_authoring_provider_cycle(
                    relocated, observed_at=OBSERVED_AT,
                    provider_adapters=ProviderReconciliationAdapters(
                        exact_interactive_provider=_ForbiddenProvider(),
                    ),
                ),
            )
            self._assert_refused_without_mutation(
                relocated,
                lambda: commit_local_work_progress(
                    relocated, prior=prior, observed_at=OBSERVED_AT,
                ),
            )

    def test_publication_and_retirement_reject_before_any_relocated_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            _, relocated = self._roots(temporary)
            self._assert_refused_without_mutation(
                relocated,
                lambda: publish_native_execution_result(
                    relocated, command_kind="ordinary_authoring",
                    sbe_release="0.4.60", published_at=OBSERVED_AT,
                ),
            )
            before = _bytes(relocated)
            with self.assertRaisesRegex(ValueError, "not retirement-eligible"):
                build_operator_retirement_request(
                    relocated, operator_audit_reference="api:fence:fixture",
                )
            self.assertEqual(before, _bytes(relocated))


if __name__ == "__main__":
    unittest.main()
