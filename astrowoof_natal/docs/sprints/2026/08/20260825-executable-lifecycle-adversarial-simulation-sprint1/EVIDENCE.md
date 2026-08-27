# Evidence — Executable Lifecycle Adversarial Simulation SBE Sprint 1

## SBE 0.4.26 publication

- Artifact source: `8f6addb19a4225040aa5e2762c5f5b264edb5a7a`.
- Release-record commit: `95eec9ee90248a0ca94f10d92549752b7e40f077`.
- Tag target: `bab2a7ac6aafc839808e3c277f6fecb0a1b818a2`.
- Tag: `astrowoof-natal-authoring-v0.4.26`.
- Release ID: `377980739`.
- Published at: `2026-08-27T16:46:50Z`.
- Wheel: 1,040,752 bytes; SHA-256
  `b120221381e20c491b0face592a2dfe32f9d057d99ca1213936b977d635d1047`.
- GitHub wheel asset ID: `532593157`; checksum asset ID: `532593156`.
- Two deterministic source builds, GitHub's asset digest, and an independently
  downloaded release asset all match.
- Installed release smoke: pass. Installed aggregate adversarial qualification:
  pass; receipt SHA-256
  `3a42cda2d5691e7fe99f758a32590a3e3ed5180b3017131761cc7f405cb0f67e`.
- Exact dependency: `semantic-projection-core==0.11.1`.
- External provider/network calls: 0; spend: USD 0; retained-QA access/mutation: 0.

Status: SBE release complete and immutable; API pin/deployment remains separate.

## Final joint review

- Review: `API FINAL JOINT CAMPAIGN REVIEW.md`.
- Decision: approved for the SBE release/adoption gate.
- Independent API reproduction: 7 passed in 45.51 seconds.
- Regenerated receipt validation: passed; case count 15.
- External network/provider calls: 0; spend: USD 0; retained-QA access: 0.
- Remaining SBE gate: explicit owner release authorization.
- API deployment and pin/adoption remain separately gated.

## Joint API campaign evidence

- API commit: `2109b6e` (`Complete joint adversarial lifecycle campaign`).
- Public catalog SHA-256:
  `eea70ce9fed3c1ee986454dbac8e71e5e39b266f895628cd8adb2e53e9eab01e`.
- Joined receipt internal identity:
  `14a58ba927e60df32c4010f2284c44b6eb09da76018dcb82e849973e157313ce`.
- Joined receipt file SHA-256:
  `b5c8951d72134e4174146b7dd25cc734071c9f8dd3d5eaac837adeb4d1d285c1`.
- Exact 15-case inventory: validated and discharged in catalog order.
- Real API three-run/one-slot progress: third continuously eligible run claims at
  step three after two review/no-action runs release capacity.
- Exact expired-lease replacement/stale-writer fence: passed as a separate real
  queue/capacity cell.
- Focused joined suite: 6 passed in 42.56 seconds.
- Receipt-producing real-worker cell: 1 passed in 44.09 seconds.
- External provider/network calls: 0; spend: USD 0; retained-QA access/mutation: 0.

Status: composed campaign complete; final API/owner release review pending.

### Release-review correction

- API correction commit: `1636927` (`Tighten joint campaign release evidence`).
- Historical starvation is now a separately executed `historical_shape`, not
  constructor-supplied expected values.
- Corrected and historical trace digests are independently bound in the receipt.
- Every packaged-fixture discharge binds both the exact catalog fixture digest and
  a distinct adapter-result digest; non-fixture evidence rejects fixture hashes.
- Corrected focused suite: 7 passed in 42.54 seconds.
- Corrected receipt internal identity:
  `1d200013835e75bde8ab476ae5a02480ac07660a235b77fc8ce88148eb20055d`.
- Corrected receipt file SHA-256:
  `ed7e580d2a8ec1514d517916a67ddfb0b69077a2a8651e1d23f60319ecf10e98`.
- External provider/network/spend and retained-QA totals remain zero.

## Slice 8 SBE-local qualification

- Focused adversarial suite: 44 passed, 1 expected optional-schema skip.
- Broad suite: 799 passed, 39 expected environment/opt-in skips; duration
  779.599 seconds.
- Fixed build epoch: `1787844361`.
- Two independent 1,040,753-byte candidate wheels: byte-identical SHA-256
  `31f0adf1e43d01b45b79a0341c1deee421b54ff522880babbbaa009eee2220bb`.
- Candidate package version remained `0.4.25`; this is qualification evidence, not
  an attempt to overwrite the published release.
- Two isolated installed qualification receipts: byte-identical file SHA-256
  `ae8b988c13723f8447bd1548748320447ac7f63ca4eb020cefae96413133435a`.
- Receipt status: pass; 3 fixtures; seeds 7/19/41; 22 route cells; 32 checks.
- External provider/network calls: 0; real provider creates: 0; spend: USD 0.
- Retained-QA access/mutation: 0.
- Remaining release gate: joined API catalog campaign receipt proving the required
  composed traces, including three-run bounded-capacity progress/fairness, followed
  by final owner/API review.

## Slice 7 API review

- Result: approved with no SBE correction requested.
- API independently built and installed the candidate wheel, invoked the public
  catalog reader, and validated 15 cases, nine packaged fixtures, and every literal
  fixture SHA-256.
- Independently observed catalog SHA-256:
  `eea70ce9fed3c1ee986454dbac8e71e5e39b266f895628cd8adb2e53e9eab01e`.
- External provider/network calls: 0; spend: USD 0; retained QA access: 0.
- Remaining joint gate: API production adapters must consume the catalog and emit
  the composed campaign receipt before tag/adoption.

## Slice 7 consumer catalog

- Contract: `astrowoof.adversarial_consumer_catalog.v1`.
- Catalog SHA-256:
  `eea70ce9fed3c1ee986454dbac8e71e5e39b266f895628cd8adb2e53e9eab01e`.
- Cases: 15; ownership classes: SBE, joint, API.
- Packaged fixtures are literal-byte hash validated by the public reader.
- Provider/network calls: 0; spend: USD 0; retained QA access: 0.

## Slice 6 installed qualification

- Console: `astrowoof-adversarial-qa`.
- Contract: `astrowoof.lifecycle_adversarial_qualification.v1`.
- Candidate wheel SHA-256:
  `b40edcde3026e1bcf3910e9f89d194bd7af0be11f40518c1f905eff628e22fc5`.
- Deterministic installed receipt SHA-256:
  `ae8b988c13723f8447bd1548748320447ac7f63ca4eb020cefae96413133435a`.
- Repeated installed-console receipt equality: true.
- Aggregate: 3 fixtures, seeds 7/19/41, 22 route cells, 32 invariant/cell
  checks, exact and bounded route coverage.
- External provider/network calls: 0; real creates: 0; spend: USD 0.

## Slice 5 seeded campaign

- Public walk/replay: `run_seeded_walk()` and `replay_seeded_walk()`.
- Public campaign qualification: `run_seeded_campaign_qualification()`.
- Fixed seeds: 7, 19, 41; exact and bounded route coverage.
- Shrunk stutter witness length: one event.
- External provider/network calls: 0; real creates: 0; spend: USD 0.

## Slice 4 review corrections

- Unit branch: 300 actual `advance_base_unit` events.
- Accelerated branch: one actual `advance_to_boundary` event.
- Successor states and SHA-256 identities match exactly.
- Rehashed receipts with depths 0, 1, and 9 fail semantic validation.

## Slice 4 systematic explorer

- Public projection builder/validator: `build_action_binding_projection()` and
  `validate_action_binding_projection()`.
- Provider-free qualification: `run_systematic_explorer_qualification()`.
- Six-member initial state: four durable identities, two unentered members.
- Shortest distinct-create and duplicate-refusal witnesses: one event each.
- Alternative member ordering reaches one deduplicated semantic successor.
- Real v0.7 Muffin inspection yields a one-step stutter witness.
- Focused result: 31 passed, one optional-schema skip.
- External provider/network calls: 0; real creates: 0; spend: USD 0.

## Slice 3 review correction

- Added a regression proving trace v1 does not falsely classify a mixed partial
  wave as duplicate creation merely because another member has provider evidence.
- Create-at-most-once remains required, but its proof moves to Slice 4's exact
  redacted action/binding projection.

## Slice 3 native oracle

- Public derivation: `classify_adversarial_transition()`.
- Ordered history evaluation: `evaluate_adversarial_history()`.
- Safety evaluation: `adversarial_safety_violations()` and
  `assert_adversarial_safety()`.
- Public contradiction derivation: `native_contradictions()`.
- No-op snapshot/revision/checkpoint republish regression proves no false progress.
- Focused result: 27 passed, one optional-schema skip.
- Provider/network calls: 0; spend: USD 0.

## Slice 2 broader route matrix

- Public builder: `build_adversarial_route_matrix_qualification()`.
- Strict validator: `validate_adversarial_route_matrix_qualification()`.
- Cells: 22, spanning exact/bounded initial Response/Batch, post-fan-in local work,
  four ordinary Response stages, and their explicitly refused Batch counterparts.
- Source evidence: three validated production-path qualification receipts.
- Focused result: 20 passed, one optional-schema skip.
- External provider/network calls: 0; real provider creates: 0; spend: USD 0.

Status: Slice 2 complete; initial joint API causal/replay proof accepted

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
