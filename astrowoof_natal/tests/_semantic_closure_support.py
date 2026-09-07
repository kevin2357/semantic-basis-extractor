"""Shared test-only support for semantic-closure lifecycle fixtures.

This module is intentionally not discoverable as a test module.  It owns no
cross-process cache: each importing test process constructs and retains its own
immutable compiled packet.
"""

from __future__ import annotations

import json
import sys
import threading
import unittest
import zipfile
from copy import deepcopy
from pathlib import Path

from astrowoof_natal_authoring.closure import (
    FakeAuthoringProvider,
    OpenAIResponsesProvider,
    SpendController,
    author_pending_passes_batch,
    discover_passes,
    initial_run_state,
    load_json,
    save_state,
    writable_fields,
)
from astrowoof_natal_authoring.extractor import (
    build_candidates,
    build_story_workspace,
    compile_packet,
    discover_subject_packages,
    load_and_validate_contexts,
    optimize,
)
from astrowoof_natal_authoring.spend import (
    AUTHORIZATION_SCHEMA,
    PRICE_BOOK_VERSION,
    AwaitingSpendAuthorization,
    authorize_action,
)


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


def authored_field_payload(workspace: Path) -> dict:
    result = {}
    ordinal = 0
    for relative_path, fields in writable_fields(workspace).items():
        result[relative_path] = {}
        for field in fields:
            ordinal += 1
            if field == "context_filter_groups.high_level":
                value = "Personality"
            elif field == "context_filter_groups.detail_level":
                value = "Core Personality"
            else:
                value = f"Fresh authored value {ordinal} for {field}."
            result[relative_path][field] = value
    return {"files": result}


def completed_response(
    authored: dict,
    *,
    response_id: str = "resp_test",
) -> dict:
    return {
        "id": response_id,
        "status": "completed",
        "model": "gpt-5.6-terra",
        "output": [{
            "type": "message",
            "content": [{
                "type": "output_text",
                "text": json.dumps(authored),
            }],
        }],
        "usage": {
            "input_tokens": 1000,
            "input_tokens_details": {"cached_tokens": 200},
            "output_tokens": 500,
            "output_tokens_details": {"reasoning_tokens": 100},
            "total_tokens": 1500,
        },
    }


class ScriptedTransport:
    def __init__(self, results: list[dict | Exception]) -> None:
        self.results = list(results)
        self.calls: list[dict] = []

    def request_json(self, **kwargs):
        self.calls.append(kwargs)
        if not self.results:
            raise AssertionError("Unexpected transport call")
        result = self.results.pop(0)
        if isinstance(result, Exception):
            raise result
        return result


def _test_spend_policy() -> dict:
    return {
        "currency": "USD",
        "price_book_version": PRICE_BOOK_VERSION,
        "run_ceiling_micro_usd": 100_000_000,
        "stage_ceilings_micro_usd": {
            "authoring_initial": 100_000_000,
            "creative_retry": 100_000_000,
            "polish": 100_000_000,
            "qualitative_critic": 100_000_000,
            "qualitative_candidate": 100_000_000,
        },
        "optional_stage_budget_behavior": {
            "polish": "skip",
            "qualitative_critic": "skip",
            "qualitative_candidate": "skip",
        },
    }


class SemanticClosureFixture(unittest.TestCase):
    """Process-local semantic-closure fixture shared by test modules."""

    @classmethod
    def setUpClass(cls) -> None:
        packages = discover_subject_packages(EXAMPLES, "bre")
        contexts, registry, input_audit = load_and_validate_contexts(
            "bre", packages["bre"]
        )
        candidates, analysis = build_candidates(contexts)
        selected, rejected, _ = optimize(candidates)
        cls._packet_template = compile_packet(
            "bre",
            contexts,
            selected,
            rejected,
            analysis,
            registry,
            input_audit,
        )

    def setUp(self) -> None:
        # Each test owns mutable fixture state. The process-local compiled
        # template is never handed to a test directly.
        self.packet = deepcopy(type(self)._packet_template)

    def make_passes(
        self,
        root: Path,
        *,
        count: int = 6,
        cards_per_pass: int = 2,
    ) -> tuple[dict, list, Path]:
        bundle = root / "bundle"
        bundle.mkdir()
        for number in range(1, count + 1):
            workspace = root / f"bre_{number}"
            if number <= 5:
                build_story_workspace(
                    workspace,
                    self.packet,
                    ROOT,
                    cards_per_pass,
                    card_start=(number - 1) * cards_per_pass + 1,
                    pass_number=number,
                    pass_count=6,
                )
            else:
                build_story_workspace(
                    workspace,
                    self.packet,
                    ROOT,
                    0,
                    card_start=cards_per_pass * 5 + 1,
                    include_summaries=True,
                    include_theme_plan=True,
                    pass_number=6,
                    pass_count=6,
                )
            archive = bundle / f"bre_{number}.zip"
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as handle:
                for path in sorted(workspace.rglob("*")):
                    if path.is_file():
                        handle.write(
                            path,
                            Path(workspace.name) / path.relative_to(workspace),
                        )
        manifest = {
            "status": "pass",
            "subject_count": 1,
            "subjects": [{"subject": "bre", "status": "pass"}],
        }
        specs = discover_passes(manifest, bundle) if count == 6 else []
        return manifest, specs, bundle

    def make_state(
        self,
        root: Path,
        provider: FakeAuthoringProvider,
        *,
        max_attempts: int = 3,
        cards_per_pass: int = 2,
    ) -> tuple[dict, Path]:
        manifest, specs, _ = self.make_passes(root, cards_per_pass=cards_per_pass)
        run_dir = root / "run"
        run_dir.mkdir()
        packet_dir = run_dir / "sbe" / "semantic-basis-output" / "bre"
        packet_dir.mkdir(parents=True)
        (packet_dir / "bre.selected-authoring-packet.json").write_text(
            json.dumps(self.packet, indent=2) + "\n", encoding="utf-8"
        )
        state = initial_run_state(
            input_package=EXAMPLES,
            run_dir=run_dir,
            provider=provider,
            max_attempts=max_attempts,
            sbe_manifest=manifest,
            specs=specs,
            profile=(
                {"spend_policy": _test_spend_policy()}
                if getattr(provider, "name", None) == "openai"
                else None
            ),
        )
        run_json = run_dir / "run.json"
        save_state(run_json, state)
        return state, run_json

    def make_authorized_detached_batch(
        self, root: Path, transport,
    ) -> tuple[OpenAIResponsesProvider, dict, Path, dict]:
        provider = OpenAIResponsesProvider(
            api_key="test-key",
            model="gpt-5.6-luna",
            max_output_tokens=30_000,
            prompt_cache_mode="disabled",
            require_spend_authorization=True,
        )
        state, run_json = self.make_state(root, provider, cards_per_pass=10)
        state["service_level"] = "batch"
        save_state(run_json, state)
        controller = SpendController(
            state=state,
            run_json=run_json,
            state_lock=threading.Lock(),
            consumer_id="batch-worker",
        )
        with self.assertRaises(AwaitingSpendAuthorization):
            author_pending_passes_batch(
                state=state,
                provider=provider,
                transport=transport,
                run_dir=root / "run",
                max_attempts=3,
                python_executable=Path(sys.executable),
                run_json=run_json,
                detach=True,
                sleep=lambda _: None,
                spend_controller=controller,
            )
        action = state["spend_ledger"]["actions"][0]
        authorize_action(state["spend_ledger"], {
            "schema_version": AUTHORIZATION_SCHEMA,
            "action_id": action["action_id"],
            "binding": action["binding"],
            "authorization_reference": "test-reservation",
        })
        save_state(run_json, state)
        self.assertFalse(author_pending_passes_batch(
            state=state,
            provider=provider,
            transport=transport,
            run_dir=root / "run",
            max_attempts=3,
            python_executable=Path(sys.executable),
            run_json=run_json,
            detach=True,
            sleep=lambda _: None,
            spend_controller=controller,
        ))
        return provider, load_json(run_json), run_json, action
