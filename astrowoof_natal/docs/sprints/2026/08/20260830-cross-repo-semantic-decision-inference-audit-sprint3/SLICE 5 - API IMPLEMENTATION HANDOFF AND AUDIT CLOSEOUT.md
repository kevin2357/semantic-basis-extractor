# Slice 5 — API implementation handoff and audit closeout

## Outcome

The audit is complete. It found three bounded AstroWoof API mapper defects and
no missing SBE native fact. SBE `0.4.32` requires no code change, schema change,
version bump, or release for this work.

API should implement the corrections in one focused consumer sprint because the
bounded mapper defect can currently activate the generic latest-result fallback.
The sprint must consume the pinned SBE `0.4.32` public contracts; it must not
reconstruct private native state or broaden historical recovery.

## Frozen correction backlog

### API-1 — exact identity at terminal ingress

Normal worker terminal ingress must require exactly one of:

- an invocation-returned, strictly validated terminal command-result envelope;
  or
- an exact result ID supplied by a separately named, validated availability/
  recovery path.

Remove the no-ID `read_latest_sealed` default from the normal ingress method.
If a historical operator workflow still needs discovery, give it a separately
named entry point that validates availability, reads the exact discovered ID,
and passes that ID to common strict ingestion.

Required regressions:

- no envelope + no result ID refuses without reading latest;
- invocation ID outranks conflicting availability/latest;
- named preflight exact ID succeeds;
- wrong native run/result/receipt/invocation refuses atomically;
- exact replay is idempotent.

### API-2 — explicit readiness only

`SbeReadingWorker` must not derive `local_continuation_required` from cycle
disposition when the field is absent. Before workspace readiness mutation, the
worker must have an explicit validated boolean produced by the applicable
versioned mapper.

An absent value is unknown/contract-refused. It must not become local work,
provider wait, terminality, delivery, or a retry fallback.

Required regressions:

- quiescent + absent readiness refuses before workspace mutation;
- review + absent readiness refuses before queue/capacity mutation;
- terminal + absent readiness does not fabricate local continuation;
- every production cycle-result constructor supplies an explicit value; and
- unknown/contradictory contract versions retain evidence for review.

### API-3 — bounded terminal/review/unsupported discrimination

Replace the current `_bounded_cycle_result()` collapse with three distinct
outcomes:

1. true terminal: may enter terminal handling only with exact sealed terminal
   result authority;
2. `retain_for_review`: nonterminal review disposition, no terminal ingress;
3. `unsupported_retain_capacity`: typed unsupported/refusal disposition, no
   terminal ingress.

Neither review nor unsupported may select generic latest evidence, fabricate a
native terminal result, publish delivery, erase action custody, settle billing,
or release reservations. Local capacity handling is a separate API transaction
and must cite its own positive permission.

Required regressions:

- bounded review reaches nonterminal review handling and never terminal ingress;
- bounded unsupported reaches typed unsupported handling and never terminal
  ingress;
- both preserve provider/consumer custody and workspace evidence;
- true bounded terminal requires exact result identity before ingress; and
- outer API status/reason retains the distinction even if current product policy
  maps review to `failed`.

### API-4 — contract-backed coverage additions

Add a runtime spy over the due/not-due pair:

- same checkpoint basis and provider custody;
- before due: no retrieval, exact release-until-due;
- at due: API invokes only the run-level reconciliation command;
- API never computes member freshness or supplies its own subset;
- SBE-selected subset remains bounded and exact; and
- retrieval creates a new checkpoint basis.

Add a v0.2 terminal-review fixture with retained provider/settlement custody and
prove outer `failed` does not release, zero, publish, or discard it.

## Suggested API sprint slices

1. **Slice 0 — reproduce and freeze:** add failing provider-free tests for
   API-1 through API-3 against pinned SBE `0.4.32`; no production mutation.
2. **Slice 1 — exact terminal ingress:** remove generic no-ID fallback and split
   named recovery discovery from normal ingress.
3. **Slice 2 — readiness:** require explicit boolean at worker boundary and
   inventory all production constructors.
4. **Slice 3 — bounded mapper:** implement terminal/review/unsupported
   discrimination and independent resource effects.
5. **Slice 4 — custody and temporal qualification:** add v0.2 retained-custody
   and due/not-due spy cases.
6. **Slice 5 — joint installed qualification:** run focused API suites and the
   released SBE `0.4.32` installed consumer/adversarial surfaces.
7. **Slice 6 — API release/deployment gate:** normal API review, image/runtime
   attestation, and fresh provider-free operational qualification. No paid QA is
   required unless a separately reviewed reason emerges.

## Exact acceptance conditions

- Every terminal ingress has exact result identity provenance.
- Generic latest discovery cannot authorize a live transition.
- Missing readiness is refused, never inferred.
- Bounded review and unsupported cannot enter terminal ingress.
- True terminal, native review, unsupported, provider pending, local work,
  delivery, and external authority remain separately mapped.
- Outer failure never implies provider/financial custody release or publication.
- Due reconciliation consumes SBE's temporal decision and subset.
- Unknown versions and contradictory evidence fail closed.
- Existing v1/v2 initial-wave, ordinary v2 authority, reconciliation, terminal-
  review, and publication behavior remains unchanged.
- Provider calls, spend, and retained-QA access during qualification are zero.

## SBE handoff

No SBE implementation is authorized or recommended. SBE's role in the API
correction is limited to:

- answering contract questions against released 0.4.32 artifacts;
- reviewing API fixtures/mappers for faithful fact consumption;
- running the existing installed adversarial/consumer qualification if useful;
  and
- updating this audit only if implementation reveals a genuinely absent native
  fact.

A later finding that API dislikes a name is not evidence for a new SBE field.
The API must first prove that no existing exact fact or join expresses the needed
permission.

## Process changes

The Native Worker Change Playbook now requires a semantic decision registry for
shared mapper changes and explicitly forbids deriving decisions from descriptive
labels, sealing, presence, emptiness, or exit codes. The Adversarial Lifecycle
Simulation Playbook now includes a proxy-inference mutation method and requires
separate testing of native terminal acceptance, API terminalization, capacity,
custody/settlement, and publication.

## Final audit record

- SBE/API decision sinks inventoried: 46.
- Registry decisions: 28.
- Adversarial mutation families: 15 plus 3 focused mutations.
- Confirmed API mapper defects: 3.
- SBE public-contract gaps: 0.
- Focused tests: 10 passed.
- Broader provider-free tests against the SBE 0.4.32 source surface: 122 passed.
- Provider activity, spend, retained-QA access, deployment, and production
  mutation: zero.

The audit is ready for owner/API final review. Its completion does not itself
authorize the API implementation, deployment, or recovery of any retained run.
