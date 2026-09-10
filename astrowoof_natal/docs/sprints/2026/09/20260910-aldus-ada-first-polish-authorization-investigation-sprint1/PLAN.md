# Aldus/Ada First-Polish Authorization Investigation — Plan

## Slice 0 — Frozen source and trace reconstruction

Reconstruct a side-by-side timeline from the supplied API facts and the saved
SBE worker log. Identify every authoritative/native artifact needed to decide:

- whether each first-polish action had exact, structurally valid authority;
- whether the native result expected API to grant, deny, or terminalize; and
- whether the apparent Ada/Aldus difference is semantic or only a different
  publication/command boundary.

Deliver an evidence matrix and request only the smallest immutable checkpoint
coordinate packet that remains necessary. No R2 read, mutation, provider I/O,
or runtime change.

The matrix must preserve two discriminators which are easy to lose in the
shared first-polish story:

- Aldus's action inventory changes from seven reported actions to eight actions
  when polish is prepared, followed by API's exact terminal failure
  `SBE terminal review API action inventory changed`; and
- Ada publishes through native-result v0.1/provider reconciliation while Aldus
  publishes the later ordinary-authoring result through native-result v0.2.

Compare the sealed authority-request fields at those two command/publication
boundaries rather than treating an `authorization.awaiting` trace event as
proof that API received a structurally consumable request.

## Slice 1 — Bounded immutable-evidence inspection

Only after API supplies exact object coordinates and authorizes one conditional
HEAD plus one bounded GET per named object: validate result/receipt/action/
binding joins, final-QA evidence, first-polish intent and any authority request
or refusal. State whether the evidence is sufficient to assign ownership.

Status: complete. Both exact requests are present and API-readable. The defect
is assigned to SBE's native spend-boundary/terminal-review selection; see
`SLICE 1 - IMMUTABLE FIRST-POLISH AUTHORITY FINDINGS.md`.

## Slice 2 — Provider-free reproduction and contract classification

If Slice 1 establishes a native-side gap or ambiguity, build a provider-free
fixture that reproduces the exact initial/creative-retry → final-QA-failed →
first-polish boundary. If the evidence instead shows a valid API authority
request that was not granted/ingested, record an API-owned handoff with the
smallest required consumer contract.

Status: complete. The provider-free reproducer isolates final-QA terminal
dominance over an already elected live polish request. See `SLICE 2 -
PROVIDER-FREE REPRODUCTION AND CONTRACT CLASSIFICATION.md`.

## Slice 3 — Implementation and qualification (gated)

Implement only the owner-approved narrow correction. Demonstrate the fixed
route provider-free, preserve expected terminal editorial outcomes, and avoid
broad changes to batch, bounded, mixed-custody, recovery, or optional-stage
families not proven to share this seam.

Status: implemented and focused-qualified after API and owner approval. The
exact interactive first-polish request now survives `FINAL_QA_FAILED` only
when every ledger, attempt, sidecar, route, revision, and terminal fence agrees.
See `SLICE 3 - FIRST-POLISH AUTHORITY SELECTION CORRECTION.md`.

## Slice 4 — 0.4.58 release qualification

Freeze fresh version `0.4.58`, run the release-identity and complete supported
repository suite through the checked-in coordinator, then qualify two
byte-identical wheels and the exact installed artifact. Because the correction
changes lifecycle and authority selection, the broad/full gate and installed
provider-free adversarial qualification are required. No controlled live run,
tag, publication, or retained-workspace access occurs without its later gate.

Status: in progress after API Slice 3 re-review approval.
