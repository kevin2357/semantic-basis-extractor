# API release-pair candidate result — SBE 0.4.47

## Exact gate result

**PASS** — API reran the same provider-free Sprint 76 release-pair consumer
which correctly rejected the published 0.4.46 wheel.

Verified candidate inputs:

- release-lock commit: `0d0285297f6c74295939eb24c2a16d29af91a012`;
- artifact-source commit: `31a09e472bae871a0105d7a5e5719592b9a92407`;
- candidate wheel:
  `C:\dev\github\semantic-basis-extractor\.release-0.4.47-final-a\astrowoof_natal_authoring-0.4.47-py3-none-any.whl`;
- expected and independently calculated SHA-256:
  `4be9dbf1420376ca4213009a978224b1740094c371b351bcb3a75a7a8912e875`;
- exact API runtime revision:
  `a52bb5bf2dfe410cfadfe3e218a70f02fb17b308`; and
- SPC: `0.11.1`.

The API receipt reported:

```text
status=pass
result=api_sbe_executable_contract_qualified
sbe_wheel_version=0.4.47
sbe_wheel_sha256=4be9dbf1420376ca4213009a978224b1740094c371b351bcb3a75a7a8912e875
provider_operations=0
provider_spend_usd=0
```

It includes valid closed-receipt hashes for the executable lifecycle,
external-authority v2, provider-dispatch, final-QA mixed-custody, temporal,
post-fan-in, and ordinary-v2 happy-path qualifications. This is the same API
consumer which failed for 0.4.46 at the packaged mixed-custody command; no
reader exception, version special case, or gate bypass was added.

## Candidate-manifest scope

For this pre-publication consumer test, API used a temporary non-deployable
manifest copy whose only semantic change was the SBE distribution declaration
from `0.4.46` to `0.4.47`. Its structural image-digest field was retained only
because the release-pair parser requires a digest-shaped SBE role identity; it
does **not** assert that the currently deployed 0.4.46 image contains 0.4.47.

Consequently, a real QA runtime manifest cannot be truthfully pinned until the
tagged/published 0.4.47 asset has been consumed by the API image build and that
build returns immutable SBE-worker and operator-runner GHCR image digests. The
later deployment manifest must then:

1. declare `astrowoof-natal-authoring: 0.4.47` for SBE-worker and operator;
2. pin their actual new image digests, not the current 0.4.46 digests;
3. mint a fresh QA release/profile and matching compatibility identities across
   all four fleet roles; and
4. be runtime-attested and profile-activated before any paid cohort.

## Remaining publication condition

The API gate is green, and API has no code or consumer-contract work remaining.
However, the just-formalized SBE release playbook requires the two
byte-identical builds and installed qualification to be produced from the
**release-lock commit**. The recorded pair is from the parent
artifact-source commit `31a09e4`, while the intended annotated release tag
points at `0d02852`.

Because `0d02852` is a release-lock documentation commit and should not affect
wheel package data, the expected outcome is the same candidate SHA. Please
nevertheless rebuild twice from `0d02852` with the recorded epoch and confirm
that both wheels are byte-identical to
`4be9dbf1420376ca4213009a978224b1740094c371b351bcb3a75a7a8912e875`; repeat
the recorded installed public qualification from that exact candidate. This is
a narrow final provenance check, not a request to weaken or repeat the full
suite.

After that confirmation, API grants technical approval for owner authorization
to annotate/tag `astrowoof-natal-authoring-v0.4.47` at `0d02852` and publish
the already-qualified exact wheel plus `SHA256SUMS.txt`.

## SBE final provenance confirmation

Completed after API review:

- rebuilt twice from exact release-lock commit
  `0d0285297f6c74295939eb24c2a16d29af91a012`;
- used recorded `SOURCE_DATE_EPOCH=1788547986`;
- both wheels were 1,199,948 bytes and matched SHA-256
  `4be9dbf1420376ca4213009a978224b1740094c371b351bcb3a75a7a8912e875`;
- repeated isolated installed mixed-custody, terminal-review,
  finalization-boundary, and generic release-smoke qualifications; all passed;
- created annotated tag `astrowoof-natal-authoring-v0.4.47` at the exact
  release-lock commit;
- published only the qualified wheel and `SHA256SUMS.txt`; and
- downloaded both assets fresh and reproduced the exact qualified digest.
