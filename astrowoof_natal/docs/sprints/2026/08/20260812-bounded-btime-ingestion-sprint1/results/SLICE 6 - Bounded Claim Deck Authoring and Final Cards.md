# Slice 6 - Bounded Claim Deck, Authoring, and Final Cards

## Result

SBE now compiles the exactly-fifty bounded selection into four separate v1
artifacts:

- private `astrowoof.bounded_natal.claim_deck.v1`;
- provider-minimized `astrowoof.bounded_natal.authoring_packet.v1`;
- private `astrowoof.bounded_natal.disposition_report.v1`; and
- reader-facing `astrowoof.bounded_natal.cards.v1`.

Each has a packaged JSON Schema and appears in the packaged contract catalog. The
bounded route does not reuse or masquerade as the exact-Natal authoring-packet or
final-card contract.

## Locked semantic authority

Every private claim locks its selected ID/order, candidate kind, invariant
classification, proof scope, selected dependencies, source and correspondence
references, root-owner lineage, selected projected-term references, and private
evidence digest. The claim deck separately preserves the selection audit and the
full safe context records.

Compilation rejects non-invariant authority, a non-fifty selection, duplicate
claim identity, missing dependency closure, or missing projected terms. Only the
41 terms required by selected claims and their selected dependencies enter the
bounded selected-term registry. Final QA rejects registry drift, claim-ID drift,
locked authority changes, evidence-scope changes, malformed editorial fields,
remaining placeholders, and normalized duplicate passages.

Selected-card provenance is keyed by claim ID under
`claim_local_selected_evidence`. Summary provenance is independently keyed under
`summary_whole_dog_selected_basis`; the four summary groups collectively reference
the selected basis without being presented as card-local evidence.

## Provider-minimized view

The packaged `Bounded Natal Provider Disclosure Inventory.md` gives a field-level
inventory for initial authoring, retries, polish, and critic requests. The compiler
uses an allow-list rather than subtracting fields from private artifacts.

Providers may receive editorial subject identity, selected invariant categorical
semantics in each of the four contexts, selected dependencies, proof-scope labels,
private evidence digests, and the shared selected-term subset. Invariant sign and
coordinate-transform labels are included because they are necessary to explain
the selected projected semantics; they are not exact positions.

Providers do not receive birth dates/times, interval endpoints, coordinates,
locations or location evidence, full graphs, source identity/artifact objects, raw
evidence/ranges/witnesses/counterexamples, orbs, structural strength, relationship
allocation scores, private source/correspondence/root-owner IDs, unselected
material, the disposition report, or selection component details.

The boundary enforces forbidden keys and supports seeded protected-value scanning.
Tests inject datetime, latitude, longitude, location, and interval sentinel values
and prove their absence. Term definitions are held once in a shared selected-term
registry rather than repeated per claim.

## Provider-free authoring proof

`fake_author_bounded()` deterministically fills the distinct bounded final-card
contract. It generates unique content for all fifty cards across three densities
and three voices, plus four whole-dog summaries. It is test infrastructure and
performs no paid operation.

On the supplied full-scale archive, official admission through final bounded QA
passed with 50 cards, four summaries, 41 selected terms, separate evidence scopes,
and no protected seed disclosure. Compact artifact hashes and sizes are recorded
in `slice6-bounded-authoring-summary.json`.

## Qualification

- Eight focused tests cover separate contract compilation, exact fifty/closure,
  provider allow-list and protected seeds, selected registry closure, separate
  evidence scopes, deterministic fake authoring, final QA, locked-field and
  registry/summary/identity mutations, missing terms, field injection, packaged
  schemas, catalog entries, and authoring documentation.
- 29 combined bounded tests passed.
- Complete repository suite: 254 passed in 171.428 seconds.
- The official full-scale artifact passed admission, selection, compilation,
  protected-value scanning, deterministic fake authoring, and final QA in the
  qualified Linux SPC 0.11.0 image.
- A fresh non-editable wheel packaged and loaded all four schemas, the contract
  catalog additions, provider inventory, authoring brief, and Python compiler;
  SHA-256
  `379a50f44a6cddb93c5096fae1c0f0ff3646d34a3110386d033a5773ce375849`.
- `git diff --check`: passed with only expected Windows line-ending notices.
- Provider operations: zero.

## Gate status

Gate 6 is ready for review. The shared resumable lifecycle, spend boundaries,
events, snapshot/restore behavior, retry/polish/critic routing, and delivery
packaging remain Slice 7 work.
