"""Provider-free Slice 0 probe; run with the repository mounted read-only."""

from __future__ import annotations

from hashlib import sha256
from importlib.resources import files
import inspect
import sys

from astrowoof_natal_authoring import editorial_review_contracts as contracts


def describe(label: str, raw: bytes) -> None:
    print(label, "bytes", len(raw), "sha256", sha256(raw).hexdigest())


print("python", sys.version.split()[0])
root = files("astrowoof_natal_authoring.resources")
print("joinpath_signature", inspect.signature(type(root).joinpath))
name = contracts.SEMANTIC_CONTRACT_RESOURCE

direct = (root / "contracts" / name).read_bytes()
chained = root.joinpath(contracts.CONTRACT_PREFIX).joinpath(name).read_bytes()
describe("direct", direct)
describe("chained", chained)
print("chained_identical", chained == direct)

try:
    original = contracts._resource_bytes(name)
except Exception as exc:
    print("original_outcome", type(exc).__name__)
else:
    describe("original", original)
    print("original_identical", original == direct)

try:
    root.joinpath(contracts.CONTRACT_PREFIX).joinpath("__missing__.json").read_bytes()
except Exception as exc:
    print("missing_outcome", type(exc).__name__)
else:
    print("missing_outcome", "unexpected_success")

try:
    contracts.parse_editorial_review_json_strict(b"{")
except Exception as exc:
    print("malformed_outcome", type(exc).__name__)
else:
    print("malformed_outcome", "unexpected_success")
