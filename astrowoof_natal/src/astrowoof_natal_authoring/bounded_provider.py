"""OpenAI Responses adapter for the bounded-Natal lifecycle protocol."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from .bounded_authoring import (
    DENSITY_KEYS,
    FINAL_CARDS_CONTRACT,
    VOICE_KEYS,
    assert_provider_minimized,
)
from .closure import OpenAIResponsesProvider
from .resource_access import read_resource_text


class OpenAIBoundedLifecycleProvider:
    """Use the released resumable Responses implementation for bounded JSON work."""

    name = "openai"
    paid = True

    def __init__(
        self, *, run_dir: Path, api_key: str, model: str = "gpt-5.6-terra",
        reasoning_effort: str = "medium", service_level: str = "interactive",
        maximum_output_tokens: int = 100_000, **responses_options: Any,
    ) -> None:
        if service_level not in {"interactive", "batch"}:
            raise ValueError("Bounded OpenAI service_level must be interactive or batch")
        self.run_dir = run_dir.resolve()
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.service_level = service_level
        self.maximum_output_tokens = maximum_output_tokens
        if service_level == "batch":
            raise ValueError(
                "Bounded Batch submission is not implemented; do not claim Batch pricing"
            )
        self.responses = OpenAIResponsesProvider(
            api_key=api_key, model=model, reasoning_effort=reasoning_effort,
            max_output_tokens=maximum_output_tokens,
            require_spend_authorization=True, **responses_options,
        )

    @staticmethod
    def _voices_schema() -> dict[str, Any]:
        return {
            "type": "object", "additionalProperties": False,
            "required": list(VOICE_KEYS),
            "properties": {
                voice: {"type": "string", "minLength": 1} for voice in VOICE_KEYS
            },
        }

    @classmethod
    def _cards_schema(cls) -> dict[str, Any]:
        densities = {
            "type": "object", "additionalProperties": False,
            "required": list(DENSITY_KEYS),
            "properties": {
                density: {
                    "type": "object", "additionalProperties": False,
                    "required": ["headline", "body"],
                    "properties": {
                        "headline": cls._voices_schema(), "body": cls._voices_schema(),
                    },
                }
                for density in DENSITY_KEYS
            },
        }
        strings = {
            "type": "array", "items": {"type": "string", "minLength": 1},
            "minItems": 1,
        }
        card_properties = {
            "claim_id": {"type": "string", "minLength": 1},
            "dos": strings | {"minItems": 3, "maxItems": 3},
            "donts": strings | {"minItems": 3, "maxItems": 3},
            "funny_dog_quotes": strings,
            "imperative_dog_quotes": strings,
            "applicable_canine_jokes": strings,
            "densities": densities,
        }
        summary_properties = {
            "summary_id": {"type": "string", "minLength": 1},
            "headline": cls._voices_schema(), "body": cls._voices_schema(),
        }
        return {
            "type": "object", "additionalProperties": False,
            "required": ["cards", "summaries"],
            "properties": {
                "cards": {
                    "type": "array", "minItems": 1,
                    "items": {
                        "type": "object", "additionalProperties": False,
                        "required": list(card_properties), "properties": card_properties,
                    },
                },
                "summaries": {
                    "type": "array", "minItems": 1,
                    "items": {
                        "type": "object", "additionalProperties": False,
                        "required": list(summary_properties),
                        "properties": summary_properties,
                    },
                },
            },
        }

    @classmethod
    def _schema(cls, stage: str, payload: dict[str, Any]) -> dict[str, Any]:
        del payload
        if stage == "qualitative_critic":
            return json.loads(
                read_resource_text("schemas/bounded-natal-critic-v1.schema.json")
            )
        return cls._cards_schema()

    @staticmethod
    def _hydrate_cards(
        editorial: dict[str, Any], packet: dict[str, Any]
    ) -> dict[str, Any]:
        expected_claims = {claim["claim_id"]: claim for claim in packet["claims"]}
        supplied_cards = editorial.get("cards") or []
        by_claim = {card.get("claim_id"): card for card in supplied_cards}
        if len(by_claim) != len(supplied_cards) or set(by_claim) != set(expected_claims):
            raise ValueError("Bounded provider response has missing, duplicate, or unknown claims")
        editorial_fields = (
            "dos", "donts", "funny_dog_quotes", "imperative_dog_quotes",
            "applicable_canine_jokes", "densities",
        )
        cards = []
        for claim in packet["claims"]:
            authored = by_claim[claim["claim_id"]]
            cards.append({
                "claim_id": claim["claim_id"],
                "priority_id": claim["priority_id"],
                "claim_kind": claim["claim_kind"],
                "editorial_tier": claim["editorial_tier"],
                "invariant_authority": claim["invariant_authority"],
                "evidence_provenance": {
                    "scope": "claim_local_selected_evidence",
                    "evidence_sha256": claim["invariant_authority"]["evidence_sha256"],
                },
            } | {field: authored[field] for field in editorial_fields})
        expected_summaries = packet["summaries"]
        supplied_summaries = editorial.get("summaries") or []
        by_summary = {summary.get("summary_id"): summary for summary in supplied_summaries}
        if len(by_summary) != len(supplied_summaries) or set(by_summary) != set(expected_summaries):
            raise ValueError("Bounded provider response has missing, duplicate, or unknown summaries")
        summaries = {}
        for summary_id, source in expected_summaries.items():
            authored = by_summary[summary_id]
            summaries[summary_id] = {
                "evidence_provenance": {
                    "scope": "summary_whole_dog_selected_basis",
                    "selected_claim_ids": list(source["selected_claim_ids"]),
                },
                "headline": authored["headline"], "body": authored["body"],
            }
        return {
            "schema_version": FINAL_CARDS_CONTRACT,
            "editorial_status": "complete",
            "subject": packet.get("subject") or {},
            "authority_notice": packet["authority_notice"],
            "cards": cards, "summaries": summaries,
            "projected_term_registry": packet["projected_term_registry"],
        }

    @staticmethod
    def _instructions(stage: str) -> str:
        common = (
            "Use only the supplied bounded invariant packet and current cards. "
            "Do not infer a representative birth time, exact placement, orb, strength, "
            "confidence, house, or angle. Return only the requested editorial JSON."
        )
        stages = {
            "authoring_initial": "Write every editorial field from the bounded packet.",
            "creative_retry": "Rewrite the complete editorial deck after local QA rejection.",
            "polish": "Polish prose only.",
            "qualitative_critic": "Critique the current deck without rewriting it.",
            "qualitative_candidate": "Produce one complete improved editorial candidate.",
        }
        if stage not in stages:
            raise ValueError(f"Unsupported bounded OpenAI stage: {stage}")
        return f"{stages[stage]} {common}"

    def _complete(
        self, *, stage: str, route: str, payload: dict[str, Any],
        before_submit: Callable[[dict[str, Any]], None] | None,
        provider_created: Callable[[str | None, str], None] | None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        assert_provider_minimized(payload)
        attempt_root = self.run_dir / "bounded" / "provider" / route.replace(":", "_")
        result, metadata = self.responses.complete_json(
            system=self._instructions(stage),
            user=json.dumps(payload, ensure_ascii=False, sort_keys=True),
            schema=self._schema(stage, payload),
            schema_name=f"astrowoof_bounded_{stage}", attempt_root=attempt_root,
            idempotency_material=f"{route}:{self.model}",
            before_submit=before_submit, provider_created=provider_created,
        )
        if stage != "qualitative_critic":
            result = self._hydrate_cards(result, payload["authoring_packet"])
        return result, metadata

    def execute(
        self, *, stage: str, route: str, payload: dict[str, Any],
        before_submit: Callable[[dict[str, Any]], None] | None,
        provider_created: Callable[[str | None, str], None] | None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        return self._complete(
            stage=stage, route=route, payload=payload,
            before_submit=before_submit, provider_created=provider_created,
        )

    def resume(
        self, *, stage: str, route: str, provider_operation_id: str,
        payload: dict[str, Any],
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        marker = (
            self.run_dir / "bounded" / "provider" / route.replace(":", "_")
            / "openai-background-response.json"
        )
        recorded = json.loads(marker.read_text(encoding="utf-8"))
        if recorded.get("id") != provider_operation_id:
            raise ValueError("Bounded provider marker conflicts with lifecycle identity")
        return self._complete(
            stage=stage, route=route, payload=payload,
            before_submit=None, provider_created=None,
        )
