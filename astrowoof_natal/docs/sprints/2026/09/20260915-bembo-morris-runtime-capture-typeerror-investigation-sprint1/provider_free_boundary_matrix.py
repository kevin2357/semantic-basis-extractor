"""Provider-free exception-boundary probe for Bembo/Morris Slice 1."""

from unittest.mock import patch

import astrowoof_natal_authoring.editorial_review_runtime as runtime


RESULT_ID = "nres_" + "a" * 24
RESULT = {"result_id": RESULT_ID, "run_id": "run-matrix"}
RECEIPT = {"result_id": RESULT_ID, "run_id": "run-matrix"}
EVIDENCE = {
    "result": RESULT,
    "receipt": RECEIPT,
    "subject_id": "subject-matrix",
}


def classify(label, operation):
    try:
        branch, value = operation()
        print(label, "returned", branch, value.get("reason"))
    except Exception as exc:  # Deliberately records class only.
        print(label, "escaped", type(exc).__name__)


with patch.object(
    runtime,
    "collect_editorial_review_runtime_evidence",
    side_effect=TypeError("redacted"),
):
    classify(
        "pre_assembly_collect",
        lambda: runtime.build_editorial_review_runtime_capture(".", RESULT_ID),
    )

with (
    patch.object(
        runtime,
        "collect_editorial_review_runtime_evidence",
        return_value=("delivery", EVIDENCE),
    ),
    patch.object(runtime, "_load", side_effect=TypeError("redacted")),
):
    classify(
        "within_assembly",
        lambda: runtime.build_editorial_review_runtime_capture(".", RESULT_ID),
    )

with (
    patch.object(
        runtime,
        "collect_editorial_review_runtime_evidence",
        return_value=("delivery", EVIDENCE),
    ),
    patch.object(runtime, "_load", side_effect=ValueError("redacted")),
    patch.object(runtime, "_runtime_capture_status", side_effect=TypeError("redacted")),
):
    classify(
        "typed_status_construction",
        lambda: runtime.build_editorial_review_runtime_capture(".", RESULT_ID),
    )
