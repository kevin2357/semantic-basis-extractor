from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from astrowoof_natal_authoring.basis_policies import (  # noqa: E402
    ExactNatalPolicy,
    LEGACY_ATOMIC_POLICY_ID,
    resolve_exact_natal_policy,
)
from astrowoof_natal_authoring.extractor import (  # noqa: E402
    build_candidates,
    compile_packet,
    discover_subject_packages,
    load_and_validate_contexts,
    main as extract_main,
    optimize,
    qa_report,
)


class TestBasisPolicies(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        packages = discover_subject_packages(ROOT / "examples", "bre")
        cls.contexts, cls.registry, cls.input_audit = load_and_validate_contexts(
            "bre", packages["bre"]
        )

    def replay(self, policy=None):
        candidates, analysis = build_candidates(self.contexts, policy)
        selected, rejected, audit = optimize(candidates, policy=policy)
        packet = compile_packet(
            "bre",
            self.contexts,
            selected,
            rejected,
            analysis,
            self.registry,
            self.input_audit,
            policy=policy,
        )
        qa = qa_report(candidates, selected, rejected, packet, policy)
        return candidates, selected, rejected, audit, packet, qa

    def test_default_resolves_to_released_legacy_policy(self) -> None:
        policy = resolve_exact_natal_policy()
        self.assertIsInstance(policy, ExactNatalPolicy)
        self.assertEqual(LEGACY_ATOMIC_POLICY_ID, policy.policy_id)
        self.assertEqual("exact_natal", policy.route)
        self.assertEqual(50, policy.selection_budget)
        self.assertEqual(16, policy.mandatory_count)

    def test_explicit_legacy_policy_is_exactly_default_equivalent(self) -> None:
        default = self.replay()
        explicit = self.replay(LEGACY_ATOMIC_POLICY_ID)
        self.assertEqual(
            json.dumps(default, default=lambda value: value.as_dict(), sort_keys=True),
            json.dumps(explicit, default=lambda value: value.as_dict(), sort_keys=True),
        )

    def test_unknown_or_wrong_route_policy_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported exact-Natal policy"):
            resolve_exact_natal_policy("legacy_atomic.v9")
        with self.assertRaisesRegex(ValueError, "not exact_natal"):
            resolve_exact_natal_policy(
                SimpleNamespace(policy_id="bounded.v1", route="bounded_natal")
            )

    def test_cli_rejects_unknown_policy_before_processing(self) -> None:
        with patch.object(
            sys,
            "argv",
            [
                "extract",
                "--input-package",
                str(ROOT / "examples" / "projected_bre_files"),
                "--exact-natal-policy",
                "legacy_atomic.v9",
            ],
        ), redirect_stderr(StringIO()), self.assertRaises(SystemExit) as raised:
            extract_main()
        self.assertEqual(2, raised.exception.code)

    def test_cli_audits_resolved_policy_without_changing_packet(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "output"
            bundle = root / "bundle"
            with patch.object(
                sys,
                "argv",
                [
                    "extract",
                    "--input-package",
                    str(ROOT / "examples" / "projected_bre_files"),
                    "--output-dir",
                    str(output),
                    "--bundle-dir",
                    str(bundle),
                    "--exact-natal-policy",
                    LEGACY_ATOMIC_POLICY_ID,
                ],
            ), redirect_stdout(StringIO()):
                extract_main()

            expected = {
                "route": "exact_natal",
                "policy_id": LEGACY_ATOMIC_POLICY_ID,
            }
            candidate_pool = json.loads(
                (output / "bre" / "bre.candidate-pool.json").read_text("utf-8")
            )
            selection = json.loads(
                (output / "bre" / "bre.selection-audit.json").read_text("utf-8")
            )
            run = json.loads((output / "run-manifest.json").read_text("utf-8"))
            self.assertEqual(expected, candidate_pool["policy"])
            self.assertEqual(expected, selection["policy"])
            self.assertEqual(expected, run["policy"])
            self.assertEqual(expected, run["subjects"][0]["policy"])


if __name__ == "__main__":
    unittest.main()
