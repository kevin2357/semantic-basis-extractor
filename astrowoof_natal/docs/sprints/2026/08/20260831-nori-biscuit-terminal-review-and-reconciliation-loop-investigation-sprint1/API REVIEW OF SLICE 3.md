# API review of Slice 3

## Decision

Slice 3 is accepted. Proceed to Slice 4 contract/runtime design for the
confirmed Nori ordering defect only.

The Biscuit reproduction correctly fails to reproduce a general
creative-retry defect. Do not broaden the Nori patch to creative retry or
invent the missing Biscuit predicate. Its API no-progress/capacity containment
gap remains a separate concern.

## Confirmed scope

- Nori is now proven through the public `closure.main()` boundary: a completed
  polish operation is advertised, author-pass work has no matching consumer,
  and the first progress seal happens before the later polish consumer. The
  result is the truthful custody-preserving v0.2 review result observed in QA.
- The provider-not-due control preserves the essential negative case: genuine
  provider custody must not become synthetic local work.
- Biscuit's retained checkpoint outcome is real, but the generic
  creative-retry fixture advances successfully. Runtime design must leave that
  cause evidence-insufficient rather than adding a run-shaped special case.

## Required implementation-test refinement

The current Nori positive control demonstrates the intended ordering by
injecting consumption through a patched `author_pending_passes`. That is useful
as an ordering proof but is not yet a regression for the real polish consumer.

Before calling the correction qualified, add a provider-free production-shaped
test where the actual stage-specific polish path (`finalize_subjects` and its
real adoption boundary) consumes the completed response artifact without a
provider request. It should prove all of the following together:

1. the polish operation is no longer advertised after consumption;
2. the consumed-operation history records its stable key;
3. no contradictory review result is sealed; and
4. the next public decision is truthful for the resulting state.

Use minimal, explicitly provider-free fixtures; do not replace the test with a
mock that directly writes action state.

## API follow-on frozen by this evidence

Whatever SBE emits after the narrow ordering correction, API must later consume
the full native result custody disposition. `review_required` remains an
editorial/native outcome label, not permission to terminalize or clean up when
the result says reconciliation custody remains.

No retained-QA recovery, deployment, provider action, or release is approved
by this review.
