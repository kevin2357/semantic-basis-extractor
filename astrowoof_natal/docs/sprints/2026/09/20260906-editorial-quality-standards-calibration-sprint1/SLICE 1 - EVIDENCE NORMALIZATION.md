# Slice 1 — evidence normalization

Status: complete. Slice 2 production-oracle replay is next.

## Access and integrity result

The four-run evidence cohort is now locally complete. Doughmeat, Macaron, and
Frisbee were not downloaded again. Madeleine used the one approved conditional
HEAD and GET; its object identity, media type, protection metadata, byte count,
and archive digest matched the coordinate packet.

All four checkpoint archives were then validated offline using the same closed
procedure:

- reject absolute, traversing, duplicate, or symbolic-link members;
- recompute the canonical signed inventory digest;
- require the ZIP member set to equal the declared inventory exactly;
- verify every extracted member's byte count and SHA-256; and
- recompute the workspace snapshot inventory.

| Run | Generation | Members | Archive | Inventory | Snapshot |
| --- | ---: | ---: | --- | --- | --- |
| Madeleine | 9 | 934 | valid | valid | valid |
| Doughmeat | 11 | 949 | valid | valid | valid |
| Macaron | 11 | 945 | valid | valid | valid |
| Frisbee | 11 | 949 | valid | valid | valid |

## Madeleine's formerly missing decision evidence

The retained workspace resolves the main unknown cleanly:

- final structural validation: `fail` with exactly one error;
- exact error: `Card 7 has invalid second-person grammar in no_astro.body.`;
- final editorial lint: `pass`, zero warnings;
- polish-attempt-1 validation: the same one structural error;
- polish-attempt-1 lint: `pass`, zero warnings; and
- native outcome: `review_required / final_qa_requires_review`.

Card 7 is priority `7`, claim `relationship_94a05088e137d997`. Its no-astro
direct-to-dog body contains the grammatically valid clause: “The corner,
blanket, or peculiar ritual that restores you is not evidence that you have
nothing to offer.” The released `BAD_SECOND_PERSON` expression matches the
substring `you is` across the subject-relative-clause boundary. Direct execution
of that production expression against the retained field reproduces the match.
The terminal decision was therefore caused by a deterministic structural false
positive, not by an actual switch away from second person.

This is already materially different from the other cases: Madeleine has no
lint problem at all; she is a structural-validator calibration case concerning
an apparently referential use of `them` in otherwise second-person prose.

## Cross-case evidence now normalized

The retained reports reproduce the known headline states:

- Doughmeat: structurally valid, one residual `repeated_opening` warning (`you
  do not`, six fields) after two accepted polish attempts.
- Macaron: structurally valid, five substantial repetition/template warnings
  after polish 1; polish 2 produced no validation/lint report because its sparse
  edit payload failed before candidate evaluation.
- Frisbee: structurally valid, one residual `repeated_opening` warning after
  polish 2; the exact prior production replay remains the control.

The next work is deterministic production-oracle replay plus byte/text/semantic
comparisons for the four normalized lineage packets. No policy conclusion is
being drawn from the retained reports alone.

## Deterministic private packets

The sprint tool `tools/build_private_lineage_packet.py` produced one consistently
shaped private packet per run under `.tmp-editorial-calibration-r2/private-lineage/`.
Each packet binds all six pass-acceptance records, polish action/Response IDs,
sparse edits, candidate/report byte and semantic hashes, run state, final deck,
and latest sealed native result.

| Run | Attempts | Last attempt | Final-deck relationship |
| --- | ---: | --- | --- |
| Madeleine | 1 | `POLISH_IMPROVED_PARTIAL` | byte- and semantic-equal to its materialized candidate |
| Doughmeat | 2 | `POLISH_ACCEPTED` | byte- and semantic-equal to attempt 2 |
| Macaron | 2 | `POLISH_ERROR` | byte- and semantic-equal to the last materialized candidate (attempt 1) |
| Frisbee | 2 | `POLISH_REJECTED` | correctly differs from rejected attempt 2 and retains attempt 1 |

This closes an important lineage ambiguity: the final decks agree with each
run's recorded adoption decision. The calibration problem concerns the decision
rules applied to those candidates, not evidence that the wrong candidate bytes
were selected.
