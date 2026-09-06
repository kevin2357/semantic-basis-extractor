# Plan — run timeline progressive identity join correction

## Status

Complete. SBE `0.4.53` was published under immutable component tag
`astrowoof-natal-authoring-v0.4.53` and independently downloaded and verified.
No cross-repository review pause was required because this restores
the already-approved interval grammar without changing its public authority
model.

## Objective

Make the cohort timeline consume the deployed asymmetric wrapper-event shape:
pair exact API boundaries first, enrich them with an expressly witnessed
API/native run mapping, and retain fail-closed behavior for missing or
contradictory evidence.

## Invariants

1. Wrapper starts and ends pair only on the exact identities their producer
   supplies at both boundaries.
2. A missing start-side `native_run_id` is never invented from time adjacency.
3. Native identity may be enriched only from another accepted wrapper event
   that explicitly joins the same API run to one native run.
4. One API run mapping to multiple native runs, or the reverse, fails closed.
5. An event whose API run has no witnessed native mapping remains unprojectable;
   it cannot silently acquire another lane.
6. The timeline remains diagnostic-only and its closed public schema is not
   widened.

## Slice 0 — production characterization

- Preserve counts for wrapper candidates, accepted/refused events, and native
  structured evidence from the real three-run export.
- Freeze the deployed start-without-native/end-with-native shape.
- Record the implementation drift from the original approved interval grammar.

## Slice 1 — progressive identity join

- Admit otherwise valid wrapper events when `native_run_id` is absent.
- Build a bijective API-run/native-run mapping from accepted events carrying
  both identities.
- Enrich missing native identities only after that mapping validates.
- Pair cycles and leases without redundant native identity in their keys.
- Preserve contradiction and unresolved-mapping refusals.

## Slice 2 — regression and real-cohort acceptance

- Add production-shaped cycle and lease pairing tests.
- Add conflicting mapping and unresolved mapping negative tests.
- Run the focused timeline/reporter suites and diff hygiene.
- Run the installed `0.4.52`-derived CLI from the corrected source against the
  retained three-run export and regenerate JSON/HTML under `C:\tmp`.
- Compare unpaired counts and native evidence coverage with the broken output.

## Completion

Close when the real export produces paired cycle/allocation intervals, the
negative identity cases fail closed, and no unrelated runtime behavior changes.

All implementation completion conditions passed. Release qualification follows
the focused patch gate in the maintainer playbook.
