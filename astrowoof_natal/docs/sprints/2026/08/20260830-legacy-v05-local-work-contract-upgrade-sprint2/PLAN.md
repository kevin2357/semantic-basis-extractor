# SBE companion plan — legacy v0.5 local-work contract upgrade

## Goal

Provide and qualify the minimum public SBE evidence required for API's narrow,
fail-closed handling of a legacy v0.5 local-work representation gap. Reuse the
released 0.4.31 surface wherever it is already sufficient; do not presume a new
SBE implementation or release.

## Status

Slices 1–4 and immutable `0.4.32` publication are complete. The same-checkpoint witness
proved the released readers and validators, and refined mixed-custody precedence:
not-due pending custody does not block exact deterministic fan-in of separately
completed evidence. No SBE runtime correction is indicated. API requested one
additive packaged qualification bundle/receipt for Slice 3 so its consumer does
not import SBE tests or manufacture a native workspace; that surface is now
implemented and source-qualified. Version bump and installed-wheel release gate
and lean installed-wheel gate are complete.

This is provisionally classified as a **lean package-only patch**. If the diff
remains confined to qualification code, closed schemas/fixtures, package exports,
console entry point, tests, version metadata, and sprint/release documentation,
the release gate intentionally does not require the full runtime suite. Any
runtime lifecycle, provider, custody, authority, snapshot, or mutation-path
change invalidates that classification and returns the sprint to owner/API review
before broader testing.

## Slices

1. **Contract inventory and predicate freeze** — identify the precise v0.5
   semantic-validation failure that is eligible for upgrade handling while every
   other v0.5 invariant remains valid. Inventory the released v0.7 local-work and
   v0.8 retry-lineage readers, schemas, fixtures, identity joins, and refusal
   cases. Freeze when v0.7 alone is sufficient and when v0.8 is additionally
   required. Pause for API review before code.
2. **Provider-free evidence witness** — reuse or minimally extend a public
   fixture representing completed fan-in plus retained provider custody. Prove
   the legacy v0.5 shape and the minimum newer observation needed for the same
   run/checkpoint. Verify no provider I/O and do not imply that every case must
   traverse both v0.7 and v0.8.
3. **Additive three-version qualification package** — add one closed public
   fixture bundle, strict Python validator/schema reader, qualification runner,
   and provider-free CLI which prove the same-checkpoint v0.5/v0.7/v0.8 seam
   without exposing a workspace archive or private native state. Include three
   explicit scenario cells:

   - consistent lineage, completed fan-in, and unrelated custody not due:
     v0.8 selects the exact local operation, retains custody, and performs no
     provider I/O;
   - custody due: v0.8 selects SBE's bounded reconciliation command/subset, while
     the qualification itself performs no provider I/O; and
   - lineage conflict: retained custody permits reconciliation but forbids
     forward dispatch; after custody clears, typed review is selected.

   The packaged fixture bundle carries only closed public lifecycle documents
   and declared identity joins. The concise reproducible receipt binds fixture
   and schema hashes, package/version identity, per-scenario selected outcomes,
   stable join assertions, zero-I/O counts, and privacy assertions. It must not
   contain prompts, provider payloads, raw `run.json`, workspace archives,
   credentials, retained-QA data, or machine-specific workspace paths.

   The validator must use SBE's public v0.5/v0.7/v0.8 validators as the canonical
   action/binding/provider composition authority. Its additional work is limited
   to closed bundle shape, hashes, stable shared-identity equality, expected
   scenario outcomes, and privacy/I/O declarations. Add mutation tests for each
   identity join, selected outcome, fixture/schema/receipt digest, extra field,
   and privacy/I/O assertion. Pause for API fixture review.

4. **Lean patch qualification and release gate** — after API accepts Slice 3:

   - choose and set a fresh immutable patch version everywhere before building or
     running the release-shaped test gate;
   - run the new focused validator/fixture/CLI tests plus the existing legacy,
     v0.7, v0.8, and package-resource tests;
   - build the candidate wheel and verify its resource inventory;
   - clean-install that exact wheel, run `pip check`, generic release smoke, and
     the new qualification command twice in separate work directories;
   - require byte-identical normalized receipts from the two installed runs;
   - perform deterministic double wheel build and compare SHA-256;
   - run `git diff --check` and audit that no runtime lifecycle/provider/custody/
     authority/mutation source changed; and
   - pause for owner and API release approval before commit/tag/publication.

   The full runtime suite is **not required** for this lean package-only patch if
   the scope audit remains clean. The release record must state that explicitly
   rather than implying a full-suite pass. If scope expands or focused tests
   expose runtime coupling, stop and re-plan the release gate.

## Non-goals

- Claiming a definitive Diffie diagnosis.
- Relaxing v0.5 or automatically selecting operations for API.
- Treating arbitrary validation errors as upgradeable.
- Requiring a blind v0.5 to v0.7 to v0.8 fallback sequence.
- Changing lifecycle selection, provider reconciliation, local-work execution,
  retry-lineage semantics, native mutation, or production authority behavior.
- Retained-QA access, provider I/O, deployment, or release without approval.

## Lean-patch acceptance criteria

- Production runtime behavior and existing public contract bytes remain
  unchanged.
- The new surfaces are explicitly qualification-only and non-authoritative.
- The CLI accepts no run directory, provider credentials, authorization/grant,
  provider ID, production input, or retained-workspace coordinate.
- Fixture and receipt validation is closed-world and strict without optional
  `jsonschema`.
- Installed qualification is network-free, spend-free, reproducible, and binds
  the exact candidate wheel/version and every packaged fixture/schema digest.
- API can ingest the bundle through public readers and independently compare
  stable shared identities without reconstructing SBE's native composition
  rules.
