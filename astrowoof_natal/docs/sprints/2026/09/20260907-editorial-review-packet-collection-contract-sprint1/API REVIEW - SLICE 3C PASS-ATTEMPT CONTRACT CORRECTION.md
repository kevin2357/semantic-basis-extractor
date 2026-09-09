# API review — Slice 3C pass-attempt contract correction

## Decision

**Approved.** The v3 contract now represents the actual pre-assembly topology
without manufactured deck evidence. SBE may resume the narrow, read-only Slice
3 ordinary-live-exact runtime-builder implementation.

## Evidence accepted

- Both first attempts and creative retries are materializations of one released
  pass. A rejected initial attempt remains explicitly represented with its
  candidate workspace and QA digest, but cannot claim an accepted workspace.
- A retry must identify the immediate same-pass rejected predecessor, match its
  attempt identity and QA digest, and advance the attempt number exactly one.
  The action carries an identity/digest for the request, never a forbidden raw
  provider request body.
- The assembly bridge now lists six ordered pass winners rather than relying on
  the first six chronological decisions. Validation requires one and only one
  accepted winner for every released pass and binds its accepted workspace and
  claim-set identity to the first assembled deck.
- Whole-deck transitions are correctly limited to post-assembly `polish`,
  `critic`, and `candidate` stages in this ordinary live-exact model.
- The seven new rehashed cases cover the relevant lies: false acceptance,
  wrong retry relation/predecessor/QA/pass, superseded winner, and duplicate
  winner. Combined campaign coverage is now 36 cases.
- The Alloy result is stated honestly: the v3 world is inhabited and the
  response-uniqueness assertion has no bounded counterexample; the two stopped
  broader checks are not represented as proof. Their executable invariants are
  still covered by the deterministic test campaign.
- I independently ran the focused contract suite in the supported source
  layout: **23 passed, 1 expected optional `jsonschema` skip**. Scoped diff
  hygiene is clean.

## Builder fences retained

The builder may only consume the explicit invocation-returned result through
the validated exact-result reader and the restored workspace evidence it names.
It may not discover a latest result, mutate a workspace, call provider/R2/API/
database/network authority, alter lifecycle/custody/spend/retry state, or make
Better Stack delivery consequential. Any unsupported, incomplete,
contradictory, unknown-version, oversized, or over-count case returns a typed
no-partial-set result.

## Next boundary

After provider-free runtime construction, deterministic byte/idempotency, and
no-side-effect qualification are complete, pause for the existing package and
installed-wheel review. This approval does not authorize transport, release,
deployment, or live retained-workspace inspection.
