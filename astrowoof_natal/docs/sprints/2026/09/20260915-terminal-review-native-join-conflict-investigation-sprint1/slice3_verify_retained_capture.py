"""Summarize corrected public capture for one already verified workspace."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from astrowoof_natal_authoring.editorial_review_fixtures import (
    validate_editorial_review_packet,
)
from astrowoof_natal_authoring.editorial_review_runtime import (
    build_editorial_review_runtime_capture,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("result_id")
    args = parser.parse_args()
    branch, capture = build_editorial_review_runtime_capture(args.root, args.result_id)
    if branch == "unsupported":
        print(json.dumps({"branch": branch, "reason": capture.get("reason")}, sort_keys=True))
        raise SystemExit(2)
    artifacts = capture["artifacts"]
    packet = capture["packet"]
    print(json.dumps({
        "branch": branch,
        "packet_id": packet["packet_id"],
        "decision_count": len(packet["lineage"]["decisions"]),
        "projection_count": len(capture["projections"]),
        "artifact_count": len(artifacts),
        "artifact_kinds": dict(sorted(Counter(
            row["artifact_kind"] for row in artifacts
        ).items())),
        "manifest_deck_count": len(packet["artifact_manifest"]["decks"]),
        "manifest_provider_response_count": len(
            packet["artifact_manifest"]["provider_responses"]
        ),
        "validation": validate_editorial_review_packet(
            packet, capture["projections"], artifacts,
        ).outcome,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
