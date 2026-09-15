"""Provider-free real-accessor inventory probe for Python 3.11 and 3.12."""

from __future__ import annotations

from hashlib import sha256
from importlib.resources import files
import json
import sys

from astrowoof_natal_authoring.adversarial_consumer import (
    read_adversarial_consumer_catalog,
)
from astrowoof_natal_authoring.adversarial_trace import (
    read_adversarial_trace_fixture,
    read_adversarial_trace_schema,
)
from astrowoof_natal_authoring.editorial_review_fixtures import (
    read_packaged_editorial_review_fixture,
)
from astrowoof_natal_authoring.external_authority_v2 import (
    read_external_authority_v2_fixture,
)
from astrowoof_natal_authoring.provider_economics import (
    read_provider_economics_fixture,
    read_provider_economics_mutation_corpus,
)
from astrowoof_natal_authoring.resource_access import read_resource_bytes


ROOT = files("astrowoof_natal_authoring")


def expected(relative: str) -> tuple[int, str]:
    raw = ROOT.joinpath("resources").joinpath(relative).read_bytes()
    return len(raw), sha256(raw).hexdigest()


CASES = (
    (
        "generic_accessor",
        "contracts/contract-catalog.json",
        lambda: read_resource_bytes("contracts/contract-catalog.json"),
    ),
    (
        "editorial_fixture_accepted",
        "fixtures/editorial_review/editorial-review-accepted_delivery.v5.json",
        lambda: read_packaged_editorial_review_fixture("accepted_delivery"),
    ),
    (
        "editorial_fixture_closeout",
        "fixtures/editorial_review/editorial-review-editorial_closeout.v5.json",
        lambda: read_packaged_editorial_review_fixture("editorial_closeout"),
    ),
    (
        "adversarial_consumer_catalog",
        "fixtures/adversarial-consumer/catalog.v1.json",
        read_adversarial_consumer_catalog,
    ),
    (
        "adversarial_trace_schema",
        "contracts/lifecycle-adversarial-trace.v1.schema.json",
        read_adversarial_trace_schema,
    ),
    (
        "adversarial_trace_fixture",
        "fixtures/adversarial-traces/review-no-action-cycle.v1.json",
        lambda: read_adversarial_trace_fixture("review-no-action-cycle.v1.json"),
    ),
    (
        "external_authority_fixture",
        "fixtures/external-authority-v2/ordinary-action-set.v1.json",
        read_external_authority_v2_fixture,
    ),
    (
        "provider_economics_fixture",
        "fixtures/provider-economics/providerless-no-work.v1.json",
        lambda: read_provider_economics_fixture("providerless-no-work.v1.json"),
    ),
    (
        "provider_economics_corpus",
        "fixtures/provider-economics/mutation-corpus.v1.json",
        read_provider_economics_mutation_corpus,
    ),
)


print("python", sys.version.split()[0])
for label, relative, reader in CASES:
    size, digest = expected(relative)
    try:
        value = reader()
    except Exception as exc:
        outcome = type(exc).__name__
    else:
        outcome = "success_bytes" if isinstance(value, bytes) else "success_parsed"
    print(json.dumps({
        "case": label,
        "resource": relative,
        "bytes": size,
        "sha256": digest,
        "outcome": outcome,
    }, sort_keys=True))
