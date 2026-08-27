# Evidence — Executable Lifecycle Adversarial Simulation SBE Sprint 1

Status: Slice 2 SBE installed/runtime half complete; joint API proof pending

## Inputs reviewed

- API Sprint 20 state-transition-control plan, log, and evidence.
- API Sprint 21 provider-free multi-run qualification plan.
- SBE scripted-provider, installed-wheel, failure-injection, and lifecycle
  qualification patterns.
- Muffin local-resume wrapper counterexample and corrected ownership diagnosis.

## Safety totals

- provider calls: 0
- external network calls: 0
- spend: USD 0
- retained QA access/mutation: 0
- runtime/schema/source changes: 0

Current gate: planning review.

## Slice 0 evidence

- Reviewed the API agent's joint-boundary recommendations in full.
- Inspected packaged lifecycle/local-work/temporal schemas and public readers.
- Inventoried structured event sites, provider create/retrieve seams, named failure
  injectors, and installed QA commands.
- Reconciled the bounded route-parity release evidence for Batch versus optional
  interactive stages.
- Produced the state, projection, actor, resource, event, construction, route, hook,
  incident, fingerprint, and Muffin-trace catalogs.

Artifact: `SLICE 0 - STATE CATALOG JOINT PROJECTION AND MUFFIN TRACE.md`

Slice 0 safety totals remain unchanged. Current gate: joint review before Slice 1.

## Slice 1 evidence

- Public schema: `astrowoof.lifecycle_adversarial_trace.v1`.
- Public Python builder/reader/validator/canonical serializer exported from the
  package root.
- Three canonical packaged fixtures validate against their deterministic builders.
- Focused source qualification: 13 tests passed with one optional `jsonschema`
  validation skipped in the lean interpreter.
- Adjacent lifecycle plus contract qualification: 37 tests passed with that same
  one optional skip.
- Built a candidate wheel and validated every fixture plus the schema through the
  installed package root from outside the source tree.
- Candidate wheel SHA-256:
  `f522d16eaab2224669136220f491302e266c7e51b0f14e45ede3ddd0e65f2e2c`.
- Schema SHA-256:
  `8b45fb44b68e180e40e420139bd5e2112b72c09a0abbb2c753c05406c3f3ebda`.
- Fixture SHA-256 values:
  - contradictory command/custody:
    `bd13fb2b1167ddf8535cfd21bfc9b5c65d5ac929103a497e642d127e0b7e2644`
  - legitimate provider wait:
    `dfe0abfbc053f6d402350d70b1b3a605ec8d18ae7d466ac258bed8976b62f818`
  - historical review/no-action cycle:
    `50fa354581bf5877e74085e6743b771135a722e8175eb16caf85c7ba15fc0041`
- External network calls: 0.
- Provider creates/retrievals: 0 / 0.
- Spend: USD 0.
- Retained QA access/mutation: 0.
- Private prompt/payload/provider-ID/workspace/credential content: 0.

Artifact: `SLICE 1 - ADVERSARIAL TRACE CONTRACT AND API HANDOFF.md`

Current gate: joint schema/authority review before Slice 2.

## Slice 2 SBE vertical-slice evidence

- Fixed sanitized historical `run.json` materialized directly; production
  public-state, snapshot, writer, and inspection code used thereafter.
- Real writer-fenced v0.7 inspection selected `none / retain_for_review` with zero
  local operations.
- Historical projection: `stutter`, active lease, allocated capacity, separate
  competing-run starvation witness.
- Corrected projection: `productive`, released lease, released capacity.
- Identical native public evidence joined both projections.
- Historical/corrected API fixture projections are joint-test inputs, not production
  API evidence.
- Reproducible API production validation/mapping receipt: pending API Sprint 52.
- Focused SBE adapter/contract/adjacent runtime suite: 22 tests passed with one
  optional-schema skip.
- Installed candidate wheel SHA-256:
  `d167cbb005d72cf6dc19e223beaa702ccd4207fa5a57d1949a0dc0d1c3103e26`.
- Provider creates/retrievals/external calls: 0 / 0 / 0.
- Spend: USD 0.
- Retained QA access/mutation: 0.

Artifact: `SLICE 2 - INSTALLED MUFFIN VERTICAL SLICE JOINT CHECKPOINT.md`

Current gate: API two-run/one-slot scheduler/capacity proof.

## Slice 2A joint acceptance evidence

- API production mapping now uses the distinct nonterminal `REVIEW_REQUIRED`
  disposition for SBE `retain_for_review`.
- Production `SbeReadingWorker` path exercised with real queue/capacity services.
- Native terminal ingress invocation: 0.
- Retained workspace cleanup invocation: 0.
- First API job durably classified `native_review_required`.
- Capacity release and second queued-run claim: proven.
- Stale original-claim replay: refused before duplicate transition.
- Review closeout/job-failed/lease-released events: exactly one each.
- Successor claim disturbance on replay: 0.
- Independently reproduced focused committed API/SBE suite: 76 tests passed.

Initial joint Muffin vertical gate: passed.
