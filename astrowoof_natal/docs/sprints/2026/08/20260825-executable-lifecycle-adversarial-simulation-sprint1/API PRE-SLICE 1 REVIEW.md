# API Pre–Slice 1 Review

Date: 2026-08-27  
Reviewer: AstroWoof API agent  
Status: approved to begin Slice 1, subject to the contract refinements below.

## Assessment

Slice 0 is complete and materially stronger than the initial planning draft. It
correctly makes the missing composition layer explicit, preserves the SBE/API
authority split, closes the route/stage/mechanism matrix, and gives Muffin a concise
four-step counterexample. The early installed vertical slice is the right sequencing:
prove the actual cross-repository reader/translator/scheduler seam before investing
in the full systematic explorer.

The API Slice 0 inventory independently agrees with the key conclusion. Sprint 20's
oracle was valid for its intentionally small authority tuple, but it did not contain
the current lifecycle facts necessary to distinguish typed review/no-action from
ordinary local work or to prove multi-run fairness.

## Slice 1 contract decisions

1. **Public consumer boundary.** The SBE trace contract may carry only sanitized,
   validated public artifacts and references needed by the packaged reader. It must
   not require API access to `run.json`, private packets, native workspace roots,
   private logs, prompts, raw provider payloads, or raw provider IDs. Where provider
   identity must be correlated, publish an opaque fixture correlation or a validated
   digest—not a value the API could use to reconstruct native command meaning.

2. **Materialized versus semantic identity.** Freeze both an exact raw evidence
   digest and a distinct semantic fingerprint. The latter includes every fact that
   changes future legal command, authority, custody, scheduling, or publication;
   logs, harmless observation timestamps, retry-look counters, and nonsemantic
   rewrites remain excluded. The API will separately project its materialized state
   into a corresponding semantic oracle state.

3. **Closed vocabulary.** Trace validation must reject unknown schema versions,
   commands, capacity dispositions, progress classes, construction classes, fault
   kinds, and event fields. `unknown`/contradictory evidence is a typed refusal or
   review outcome; it must never default to `ordinary_resume`.

4. **Muffin vertical-slice contract.** The fixture must expose a valid typed
   `none` command with non-local review/no-action disposition and empty immediate
   local-work inventory. The API test will demonstrate both the historical lossy
   reduction's stutter/starvation witness and the current production translation's
   correct non-local terminal/review handling. The composed successor must release
   the **API execution lease and capacity** when that terminal/review handling
   completes; independent review/provider/spend authority is retained only where its
   own validated disposition requires it.

5. **Provider-free structural proof.** The Slice 1 schema/fixture test surface must
   make credential or network transport unavailable, not merely assert that an
   observed request count is zero. Fixture creation and replay must operate through
   supported installed-wheel readers/builders without source-tree imports.

6. **Clock and replay.** `logical_step` always advances per event. Simulated time
   changes only through a declared clock event. The canonical encoding/digest must
   retain enough identity to reproduce a failure byte-for-byte while the semantic
   projection detects stutter/cycles despite incidental byte changes.

7. **Trace scope.** The first schema need not encode every future route/fault in
   executable detail, but each current matrix cell must already have a closed
   `supported`, `explicitly_refused`, or `deferred` classification. A deferred cell
   cannot silently become a generic event at generation time.

## Requested Slice 1 outputs

- Versioned strict Python builder/reader/validator and canonical serializer/digest.
- Sanitized Muffin trace fixture plus at least one positive legal wait and one
  intentionally contradictory/unknown negative fixture.
- A schema field table identifying SBE-owned facts, API-owned facts, fixture-only
  facts, and the permitted consumer visibility of each.
- Privacy and installed-wheel tests proving no source-tree import, credential,
  network, prompt, raw payload, or private-workspace dependency.
- An API-consumer note defining the exact public reader/entry point and compatibility
  promise for the vertical slice.

## Approval

No blocker. Please proceed with Slice 1 and pause for joint schema/authority review
before beginning the installed adapter work in Slice 2. The API team will preserve an
analogous review response in API Sprint 52 after receiving SBE's contract packet.
