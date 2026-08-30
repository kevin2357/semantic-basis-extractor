# Slice 5 — Exact-interactive fan-in adoption implementation

## Implemented correction

Exact-interactive ordinary authoring now recognizes the narrow retained state in
which:

- the last unfinished pass attempt says `AMBIGUOUS_PROVIDER_SUBMISSION`;
- its exact paid action has a durable Response identity;
- reconciliation has durably recorded `completed`; and
- the snapshot-bound response artifact joins that same identity.

Before successor selection, `prepare_completed_exact_attempt_for_adoption()`
validates the run, action, stage, route, attempt, service level, provider kind,
provider identity, reconciliation outcome, artifact presence, response identity,
and completed status. It then persists only the pass-attempt marker needed to
re-enter the existing `OpenAIResponsesProvider.author()` completion path.

That existing path performs the substantive adoption:

1. load the already-retrieved response rather than GET or POST;
2. parse output text and JSON;
3. materialize the authored workspace;
4. require complete output;
5. repair deterministic metadata;
6. run deterministic pass QA;
7. settle/report the paid action; and
8. persist accepted/rejected pass truth before retry selection.

If the narrow join is unavailable or invalid, ordinary authoring returns without
preparing a successor. The existing local-work progress fence then preserves the
unconsumed predecessor and produces typed review evidence. It never guesses.

## Public behavior

- Accepted validated response: predecessor is reported, pass is accepted, no
  successor action exists.
- QA-rejected validated response: predecessor rejection is durable, exactly one
  providerless successor is prepared, the prior local operation is consumed, and
  the successor inspection selects its exact `await_external_authority` request.
- Invalid/conflicting/missing response: no successor, no consumption, no provider
  I/O, typed review through the existing progress fence.
- Replay after post-adoption interruption: cached evidence is revalidated; no
  provider I/O occurs; at most one deterministic successor is prepared.

No lifecycle, external-authority, terminal-review, or command-result schema
changed. API behavior remains unchanged.

## Interruption boundaries

### Before coherent adoption checkpoint

The test interrupts while persisting the restored pass marker. The prior
snapshot fails closed, no successor exists, and no local-work operation is marked
consumed. A partial marker cannot become provider-create authority.

### After adoption/QA rejection, before successor preparation

The test interrupts immediately after the coherent rejected-attempt checkpoint.
The ledger action is already `REPORTED`, the response artifact remains durable,
and no successor yet exists. A fresh-worker replay performs zero provider I/O,
prepares exactly one successor, and exposes exactly that action through the
successor external-authority inspection.

## Route applicability

- Exact interactive Response creative retry: corrected.
- Bounded interactive: unchanged; its route contract is not admitted by the new
  exact-run helper.
- Exact Batch and bounded Batch: unchanged; they use their separate Batch result
  ingestion path.
- Initial wave and optional editorial stages: unchanged.

## Qualification

New Moxie matrix:

```text
Ran 8 tests — OK
```

Focused adjacent matrix:

```text
test_moxie_terminal_review_inventory_slice3
test_post_fan_in_retry_runtime_slice2
test_completed_retry_duplicate_submission_slice2
test_post_fan_in_retry_authority_routing_slice0

Ran 19 tests — OK
```

The matrix covers retained bad ordering, accepted adoption, rejected adoption,
invalid identity, interruption before adoption, interruption after adoption,
replay, strict API subset refusal, exact authority publication, and zero provider
I/O. `git diff --check` is clean.

## Release gate

Slice 5 changes runtime source. Pause for API review before activating installed-
wheel qualification/version/release work. Moxie remains suspended and untouched.
