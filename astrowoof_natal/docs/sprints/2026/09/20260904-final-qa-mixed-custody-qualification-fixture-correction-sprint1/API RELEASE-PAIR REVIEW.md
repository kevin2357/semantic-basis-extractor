# API release-pair review — Voof-paws 1

## Decision

**Approved to prepare a replacement SBE wheel, conditional on the stated
release gate.** No API reader, release-pair code, lifecycle contract, or
runtime-worker change is required for this correction.

The correction fixes the invalid fixture chronology rather than weakening the
terminal-dominance boundary that correctly rejected it in 0.4.46:

1. coherent ordinary polish authority is created from a nonterminal checkpoint;
2. the pending fixture dispatches and durably records exact provider identity;
3. later final-QA review evidence is introduced; and
4. retained provider custody selects reconciliation before terminal closeout.

The refusal fixture separately injects its terminal outer-status contradiction
only after native dispatch intent durability, preserving the intended
pre-provider, zero-I/O `post_intent_lifecycle_contradiction` fence. The added
negative control also correctly proves conclusion-first construction cannot mint
fresh authority.

## API consumer compatibility

API's `_read_final_qa_mixed_custody_receipt()` requires the exact closed v1
field set and the same semantic values:

- `astrowoof.final_qa_mixed_custody_qualification.v1`;
- pass / qualification-only / provider-free declarations;
- zero external-network, real-provider-create, and provider-spend counters;
- the v2 pending `detached_provider_pending` reconciliation selection;
- the v3/v4 pre-provider contradiction refusal; and
- the valid terminal-review receipt assertions.

The proposed implementation retains that receipt schema and those expected
values. The dynamic `sbe_version` remains intentionally accepted as a non-empty
published package version, so moving from 0.4.46 to 0.4.47 requires no API
consumer change. API will continue to hash the closed receipt and bind it to the
exact wheel SHA-256 in the release-pair receipt.

I independently ran the updated source tests with the SBE source path ahead of
the installed package:

```text
python -m unittest \
  astrowoof_natal.tests.test_final_qa_mixed_custody_qa \
  astrowoof_natal.tests.test_final_qa_mixed_custody_slice3

Ran 13 tests: OK
```

## Replacement-wheel gate

The narrow source scope supports a fixture-only patch release *only if* the
final diff remains limited to qualification construction/tests/docs. Do not
relax, skip, or special-case API's release-pair consumer.

Because the failure happened specifically when a previous release omitted its
full suite, 0.4.47 should additionally run the full SBE suite before tag/publish
even though the production runtime diff is empty. The focused affected matrix is
necessary but not sufficient evidence for restoring confidence in the release
ritual.

Before publishing, please also complete the plan's two byte-identical candidate
builds, clean-environment installation / `pip check`, packaged
`astrowoof-final-qa-mixed-custody-qa` execution, and adjacent terminal/
ordinary-v2 qualifications. Supply API the candidate wheel plus its immutable
SHA-256; API will rerun the exact Sprint 76 release-pair command before any paid
QA admission or fleet pin update.
