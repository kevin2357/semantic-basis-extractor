# Evidence

The triggering QA cohort is frozen and is evidence only. The accepted release
criterion is provider-free classification/consumer qualification; any later
fresh paid run requires separate approval.

## Pre-saunter code trace

Read-only inspection of the 0.4.22 source confirms the initial boundary
hypothesis:

- `dispatch_external_authority_v2_intent()` durably records
  `active_create_state = CALL_ENTERED` before invoking its `create(action)`
  callback.
- The production CLI callback subsequently resolves the snapshot-bound request
  payload, reads binding/model/output policy, constructs the provider, derives
  the local request key, and only then calls `create_response_only()`.
- The dispatcher's broad exception handler maps every callback exception after
  `CALL_ENTERED` to `AMBIGUOUS_PROVIDER_SUBMISSION`.
- Therefore payload-resolution or local provider-setup failures can currently be
  reported as ambiguity even when no provider transport was reached.

This is a hypothesis about the observed QA outcome, not a claim that the exact
Vafle-hund/Zultan exception is known. Their causal exception detail was not
preserved in the public result, and the cohort remains untouched.

No runtime code, schema, fixture, provider state, or retained workspace was
changed during this planning trace.

## API plan review

API approved the SBE-first sequencing and recorded the intended consumer
dispositions for pre-provider refusal, ambiguity, provider-pending custody,
exact replay, and malformed evidence. The review additionally requires a new
closed command-result version, a tri-state provider-I/O/custody assertion, and a
published provider-free fixture matrix before API implementation begins.

## Scenic Waypoint 0 initial evidence

- Fixture: fresh temporary ordinary-action v2 workspace built through supported
  SBE test/runtime helpers.
- Provider transport: scripted local counter; no network or credentials.
- Before-entry injection: zero callback/provider calls, unchanged replayable
  intent state.
- Missing-payload materialization inside the production-shaped callback: one
  callback entry, zero provider calls, native `ambiguous_submission`, persisted
  ambiguous action/intent, and `provider_io_performed=true`.
- Supported public CLI reproduction: exit code 3, sealed command outcome
  `ambiguous_submission`, first ordered action marked ambiguous, and zero patched
  OpenAI transport POSTs.
- Frozen QA access/mutation: zero.
- Real provider requests/spend: zero.

## Scenic Waypoint 0 focused gate

Command:

```text
python -m unittest \
  astrowoof_natal.tests.test_ambiguous_provider_submission_slice0 \
  astrowoof_natal.tests.test_external_authority_v2_intent_fence \
  astrowoof_natal.tests.test_external_authority_v2_cli \
  astrowoof_natal.tests.test_external_authority_v2_route_qualification
```

Result: 25 tests passed in 19.336 seconds.

The gate covers the new public CLI/local-materialization reproducer plus existing
intent, replay, concurrency, ambiguity, identity durability, route, and event
isolation evidence. Runtime source and public schemas remain unchanged.

## Scenic Waypoint 1 contract evidence

Public contract candidates:

- `astrowoof.external_authority_provider_dispatch_result.v3`
- `astrowoof.external_authority_v2_command_result.v2`

Packaged fixture identity:

- `astrowoof.ambiguous_provider_submission_fixtures.v1`

Focused command used the existing qualified 0.4.22 virtual environment so
optional Draft 2020-12 schema checks were active:

```text
python -m unittest \
  astrowoof_natal.tests.test_ambiguous_provider_submission_contract \
  astrowoof_natal.tests.test_ambiguous_provider_submission_slice0 \
  astrowoof_natal.tests.test_external_authority_v2_intent_fence \
  astrowoof_natal.tests.test_external_authority_v2_cli \
  astrowoof_natal.tests.test_external_authority_v2_route_qualification
```

Result: 30 tests passed in 21.737 seconds; zero skips.

The fixture reader validates all positive cases and proves the contradictory
case fails strict semantic validation. Privacy sentinels, payload fields,
credentials, authorization headers, prompts, and subject parameters are absent.
No provider or retained QA workspace was accessed.

## Scenic Waypoint 2 runtime evidence

The phase-aware runtime and production CLI now prove:

- all four closed local refusal reasons perform zero scripted provider creates;
- a refusal seals the exact old aggregate grant invocation;
- every provably unentered suffix action returns to `PREPARED` with its prior
  authorization/consumption evidence archived;
- a fresh inspection emits a distinct request and accepts a fresh aggregate
  grant/intent;
- a successfully provider-bound prefix remains in `WAITING` custody when the
  next member refuses;
- in a genuine three-member inventory, member one becomes provider-bound,
  member two refuses during preparation, and member three enters neither
  preparation nor transport before being restored to `PREPARED` with the
  archived `not_entered_after_refusal` disposition;
- checkpoint change after preparation returns the typed
  `checkpoint_changed_before_create` refusal, performs zero creates, and makes
  the old invocation replay-only;
- transport-entered failure, missing/malformed returned identity, and process
  interruption after `CALL_ENTERED` remain durable ambiguity; and
- exact replay performs no additional create.

Focused command:

```text
python -m unittest \
  astrowoof_natal.tests.test_ambiguous_provider_submission_runtime \
  astrowoof_natal.tests.test_ambiguous_provider_submission_contract \
  astrowoof_natal.tests.test_ambiguous_provider_submission_slice0 \
  astrowoof_natal.tests.test_external_authority_v2_intent_fence \
  astrowoof_natal.tests.test_external_authority_v2_cli
```

Result: 35 tests passed in 14.264 seconds. `git diff --check` reported only the
repository's expected LF-to-CRLF notices and no whitespace errors. Provider
credentials, network, spend, and retained QA access were all zero.

The API reviewer independently ran the five-module command before the added
three-member case and observed 34 tests with one optional-schema skip in its
lean environment. The candidate environment above includes `jsonschema`, so
the same gate plus the new test completed with no skip.

## Scenic Waypoint 4 release qualification

- Version: 0.4.23.
- Artifact source commit:
  `9f3e3874aee74099b7c1a43b5094fe55c8426fb3`.
- `SOURCE_DATE_EPOCH`: `1787666725`.
- Two independent wheels: byte-identical.
- Wheel bytes: 980,621.
- Wheel SHA-256:
  `adf16ecc785c2eeb98bcc1b4ed77d49bba0f208a1943c58e74320b2eed5135de`.
- Wheel entries/resources: 173 / 105.
- Packaged-resource SHA-256:
  `f8cdbe7c621dc3ac47ffe1d1f2fbbd042e065b28ce4da67e85089a56e36dfd18`.
- `py.typed`: present; bytecode/cache entries: zero.
- Exact SPC 0.11.1 plus `pip check`: pass.
- Installed provider-free fixture export: pass; SHA-256
  `c8034eb067ca60f3984aabade8879635c37d81aedc957eb8cc8426feec378a17`.
- Generic installed release smoke: pass; 50 cards, four summaries,
  `DELIVERY_COMPLETE`.
- Full source suite: 719 passed, 3 expected skips, 758.569 seconds.
- External provider/network calls: zero.
- Provider spend: $0.
- Frozen QA workspace access/mutation: zero.

Tagging and publication remain pending final owner/API authorization.

Stress repetition identified and corrected stale process-cache reuse during
authoritative snapshot publication when Windows recycled a temporary path.
Both snapshot writing and validation now hash current bytes directly at the
integrity boundary.

## Scenic Waypoint 3 consumer evidence

- Public Python validators/readers are exported from the package root.
- `astrowoof-provider-dispatch-result` validates dispatch v3, command result v2,
  or the packaged fixture bundle without provider-capable arguments.
- The packaged contract catalog names both new schema identities.
- The consumer handoff defines API capacity/custody mapping, aggregate-refusal
  suffix semantics, fresh-authority behavior, and the SBE/API ownership split.
- The consumer manifest binds the two schema files and fixture bundle by exact
  SHA-256.
- A deliberately failing event sink cannot alter the checkpoint-drift refusal
  or cause provider I/O.

Focused command:

```text
python -m unittest \
  astrowoof_natal.tests.test_provider_dispatch_result_cli \
  astrowoof_natal.tests.test_ambiguous_provider_submission_runtime \
  astrowoof_natal.tests.test_ambiguous_provider_submission_contract \
  astrowoof_natal.tests.test_external_authority_v2_cli
```

Result: 17 tests passed in 5.643 seconds. Provider credentials, network, spend,
and retained-QA access remained zero.

API review identified that caller-supplied fixture bundles did not initially use
the packaged reader's complete closed-world validation. The shared validator and
CLI regressions now prove empty and extra-key bundles fail before output-file
creation. Focused correction suite: 16 tests passed in 7.030 seconds.
