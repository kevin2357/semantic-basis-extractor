"""Run safe read-only capture stages and report only frame/function/class metadata."""

from __future__ import annotations

import argparse
import json
import traceback
from pathlib import Path

import astrowoof_natal_authoring as package
from astrowoof_natal_authoring.editorial_review_runtime import (
    build_editorial_review_runtime_capture,
    collect_editorial_review_runtime_evidence,
    read_eligible_editorial_result,
)
from astrowoof_natal_authoring.native_transitions import read_native_transition_result


def safe_result(label, operation):
    try:
        value = operation()
        if isinstance(value, tuple):
            branch, body = value
            result = {
                "stage": label,
                "outcome": "returned",
                "branch": branch,
                "reason": body.get("reason") if isinstance(body, dict) else None,
            }
        else:
            result = {"stage": label, "outcome": "returned"}
    except Exception as exc:
        frames = traceback.extract_tb(exc.__traceback__)
        result = {
            "stage": label,
            "outcome": "raised",
            "exception_class": type(exc).__name__,
            "frames": [
                {"file": Path(frame.filename).name, "function": frame.name, "line": frame.lineno}
                for frame in frames
            ],
        }
    print(json.dumps(result, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--result-id", required=True)
    parser.add_argument(
        "--stage",
        choices=("exact_reader", "eligibility", "evidence_collection", "implementation_capture", "package_export_capture"),
    )
    args = parser.parse_args()
    root = args.root
    result_id = args.result_id
    operations = {
        "exact_reader": lambda: read_native_transition_result(root, result_id),
        "eligibility": lambda: read_eligible_editorial_result(root, result_id),
        "evidence_collection": lambda: collect_editorial_review_runtime_evidence(root, result_id),
        "implementation_capture": lambda: build_editorial_review_runtime_capture(root, result_id),
        "package_export_capture": lambda: package.build_editorial_review_runtime_capture(root, result_id),
    }
    for label, operation in operations.items():
        if args.stage is None or args.stage == label:
            safe_result(label, operation)


if __name__ == "__main__":
    main()
