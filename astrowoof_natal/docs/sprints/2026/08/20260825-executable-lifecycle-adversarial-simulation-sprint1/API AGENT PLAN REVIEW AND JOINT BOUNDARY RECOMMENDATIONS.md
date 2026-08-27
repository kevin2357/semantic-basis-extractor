# API Agent Plan Review and Joint Boundary Recommendations

Date: 2026-08-26  
Reviewer: AstroWoof API agent  
Status: approved in principle; refinements below should be incorporated before the
joint Slice 0 vocabulary/protocol freeze.

## Overall assessment

This is the right response to Muffin. The plan keeps native truth in SBE and
API-global scheduling/custody truth in the API, then tests their *composition*
instead of promoting either repository's simplified test double into the system
under test. Making bounded systematic exploration primary, with state-aware random
walks and shrinking as complementary depth tools, is the right tradeoff.

The central acceptance case is also correctly chosen: a valid typed native
review/no-action result must never be reconstructed by the API as ordinary local
continuation. The joined campaign must prove that the corrected translation releases
the relevant API capacity and that another continuously eligible run can make
progress.

## Required joint-boundary decisions for Slice 0

1. **Two representations, one explicit projection.** Keep a complete
   `MaterializedScenarioState` for adapters and a smaller `OracleState` for legal
   transitions, progress, cycles, and fairness. Publish/test the projection between
   them. A production fact may be excluded from the semantic oracle only with a
   stated reason that it cannot affect future behavior.

2. **SBE must publish public evidence, not invite reconstruction.** The API harness
   may consume only packaged schemas/readers and sanitized public artifacts. It must
   not read `run.json`, private packets, private workspace logs, or derive native
   commands from raw files. In return, SBE's fixture/trace surface needs the typed
   command/disposition, checkpoint basis, public action/binding identities where
   exposed, temporal boundary, and validated result/snapshot/receipt identities that
   the API needs to translate the native result without guessing.

3. **Closed event/actor/resource inventory.** Model actor identity (scheduler,
   claimed worker, replacement worker, SBE command, provider, lease clock, storage,
   operator, crash injector) and resource ownership (lease, capacity slot, native
   writer, provider custody, API reservation, workspace/checkpoint, publication).
   The explorer derives enabled events from those facts. Intentionally non-enabled
   events are valid negative tests only when reported as typed refusals.

4. **Do not infer a local path from omission.** The joint contract needs an explicit
   rule: an unknown, review, terminal, unsupported, contradictory, or no-action
   native disposition is not local work merely because it is not `release_until_due`.
   The API must fail closed/preserve review authority unless SBE explicitly supplies
   a supported local-work command and non-empty operation inventory.

5. **One canonical simulated clock.** Logical event step and simulated time are
   distinct. API availability/lease deadlines, provider completion, and SBE temporal
   boundaries all consume the same injected canonical time. Accelerating to a next
   boundary must be proved equivalent to repeated base-time advances.

6. **Progress is semantic, not incidental mutation.** The shared classification
   should include `productive`, `legitimate_wait`, `idempotent_replay`, `stutter`,
   `cycle`, `refused`, and `contradictory_evidence`. A legitimate wait additionally
   requires no ready local/API work, correctly released execution capacity/lease,
   correctly retained independent custody, and a declared future boundary.

## SBE-specific suggestions

- Treat the route/stage/mechanism matrix as a closed product. Each
  exact/bounded × Response/Batch × initial/retry/polish/critic/candidate/closeout
  cell is `supported`, `explicitly_refused`, or `deferred`; absent is not a state.
  Batch coverage can be staged, but deferred cells must refuse before provider I/O.

- The SBE simulator adapter should construct ordinary legal states through the same
  packaged runtime APIs and commands that production uses. Direct workspace/row
  setup is reserved for named `historical_shape` or `synthetic_invalid_state`
  fixtures and must never be presented as a normally reachable state.

- Make its provider-free boundary structurally incapable of using credentials or a
  networked transport. The installed-wheel qualification needs to prove this,
  instead of treating a zero observed request count as sufficient.

- Fingerprint native future-affecting facts: run/route/mechanism identity,
  checkpoint basis, ordered action/binding identities, provider custody/status,
  local-work operation keys and consumed keys, external-authority facts, due
  boundary, selected command, and terminal/delivery/publication disposition. Keep
  raw byte/checkpoint digests separately for replay/integrity.

- Package the trace schema, reader/validator, and a deliberately small sanitized
  fixture corpus before requesting API integration. A fixture must declare its SBE
  package/schema identity, supported public reader/command, required API observable
  fields, and expected native refusal/transition. This prevents the API from
  re-implementing native fixture semantics.

## Scope and sequencing recommendation

The full target is worthwhile, but it is large. Preserve the plan's architecture
while requiring an early vertical slice before the broad explorer:

1. Slice 0 jointly freezes the catalog, projection, minimal trace schema, and
   Muffin's four-step counterexample.
2. SBE provides the installed, provider-free artifact/reader needed for that one
   counterexample; API drives it through the real translation and a two-run,
   one-slot persistence scenario.
3. Freeze the shared progress/fairness assertion from the observed vertical slice.
4. Only then expand to the systematic explorer, broader route matrix, random
   generation/shrinking, historical corpus, and installed joint campaign.

This is not a request to reduce ambition; it ensures the first slices prove the
critical composed seam and expose missing hooks before the test framework itself
becomes a large parallel lifecycle implementation.

## Proposed review gates

- **After Slice 0:** jointly approve the materialized-state catalog, oracle
  projection, actor/resource/event table, legal-vs-synthetic construction rule, and
  Muffin trace.
- **After Slice 1:** jointly freeze the versioned trace schema, canonical digest,
  privacy contract, and explicit unknown/contradictory/refusal semantics.
- **After the first installed vertical slice:** API verifies the real production
  translation receives only public SBE evidence and detects the historical loop;
  SBE verifies no private workspace reconstruction is required.
- **After SBE Slice 6:** API reviews the packaged consumer surface and sanitized
  corpus before broad composed testing.
- **Before any release:** require zero provider/network/spend/retained-QA activity,
  reproducible fixed seeds, explicit unexplored frontier/bounds, and an adoption
  handoff that pins package and schema versions.

## No blocker

With those refinements, the companion plan is approved for its planning and Slice 0
work. No new production provider authority, real QA mutation, deployment, or API
release is implied by this review.
