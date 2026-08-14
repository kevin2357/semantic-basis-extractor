"""Console entry point for strict bounded-Natal family admission."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..bounded_admission import (
    ADMISSION_EVENT_CONTRACT,
    BoundedAdmissionError,
    admit_bounded_family,
    load_bounded_family,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-package", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--event-output", type=Path)
    args = parser.parse_args()
    try:
        admission = admit_bounded_family(load_bounded_family(args.input_package))
        result = admission.summary
        event = admission.event
        exit_code = 0
    except BoundedAdmissionError as exc:
        result = {
            "schema_version": "astrowoof.bounded_natal.input_admission.v1",
            **exc.as_dict(),
            "provider_operation_count": 0,
        }
        event = {
            "schema_version": ADMISSION_EVENT_CONTRACT,
            "event_name": "bounded_input.rejected",
            "status": exc.status,
            "data": {"code": exc.code},
        }
        exit_code = 2
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    if args.event_output:
        args.event_output.parent.mkdir(parents=True, exist_ok=True)
        args.event_output.write_text(
            json.dumps(event, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(rendered, end="")
    if exit_code:
        raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
