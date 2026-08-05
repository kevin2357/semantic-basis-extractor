# Slice 6 — Controlled Live Release Candidate

## Result

Slice 6 passed after discovering and correcting one genuine retry-orchestration
defect. A clean wheel installed outside the checkout completed a real Ella run
through OpenAI Batch authoring, local acceptance, assembly, sparse polish,
final QA, provenance capture, and delivery packaging.

## Candidate boundary

- Distribution: `astrowoof-natal-authoring 0.1.0`
- Replacement candidate wheel SHA-256:
  `8f1f2a700c1cee99b2f5cbd44fa2c89673168b210ec32c2444836b19bb497a97`
- Installed package location:
  `C:\tmp\astrowoof-release-slice6-fixed-venv\Lib\site-packages\astrowoof_natal_authoring`
- Packaged resource count: 19
- Packaged resource aggregate SHA-256:
  `67be96ba08fbd89ab379d1ebf247ef011d595bd4446c4534edd5072a503dcdf2`
- Input contract: `astrowoof.projected_natal_input.v0.1`
- Run contract: `astrowoof.semantic_closure_run.v0.7`
- Authoring profile: `astrowoof-natal-default-v0.1`

The live process imported the runtime from the clean installed environment, not
from the source tree.

## Discovery run

The first installed candidate behaved correctly at the safety boundary but did
not deliver a deck:

1. passes 1–5 cleared attempt 1;
2. pass 6 attempt 1 failed `theme_group_balance`;
3. pass 6 attempt 2 fixed balance but failed `theme_group_registry`;
4. pass 6 attempt 3 regressed to `theme_group_balance`; and
5. the runner stopped at `FAILED_REQUIRES_REVIEW` after the configured maximum
   rather than bypassing QA.

Estimated discovery-run spend was `$0.65478326`. The evidence showed that each
retry saw only the immediately preceding rejection. This allowed a repair to
forget a constraint established by an earlier attempt.

The correction makes editorial retry feedback cumulative within each pass. It
deduplicates and retains all earlier public issue codes and affected claim IDs,
includes a per-attempt rejection history, uses the latest broad guidance, and
continues to conceal checker thresholds and implementation details. A focused
regression test plus the full 117-test suite passed.

## Successful replacement run

- Final status: `DELIVERY_COMPLETE`
- Wall-clock run-state interval: 9m 37.6s
- Batch rounds: 1
- Initial authoring attempts: 6
- Creative retries: 0
- Accepted passes: 6 of 6 on attempt 1
- Cards: 50
- Summaries: 4
- Sparse polish attempts: 1
- Sparse polish targets: 9
- Sparse polish edits: 2
- Final validation: pass
- Final lint warnings: 0
- Delivery members: 5
- Delivery ZIP integrity: pass

The pre-polish deck had two advisory lint warnings: a repeated
`Neptune in Pisces` handler opening and a repeated fine-print humor mechanism.
Sparse polish removed both by changing only two fields and left seven eligible
targets untouched.

## Cost and usage

| Stage | Attempts | Input tokens | Output tokens | Estimated cost |
|---|---:|---:|---:|---:|
| Initial Batch authoring | 6 | 254,848 | 88,086 | `$0.42353573` |
| Creative retry | 0 | 0 | 0 | `$0.00000000` |
| Sparse polish | 1 | 11,588 | 436 | `$0.01420400` |
| **Total** | **7** | **266,436** | **88,522** | **`$0.43773973`** |

The prior Phase-6 Ella live run cost `$0.48054136`. The release candidate is
`$0.04280163` lower, an 8.9% reduction. Authoring alone fell from
`$0.47662236` to `$0.42353573`; this run needed a somewhat larger but still
small targeted polish because it began with two lint warnings.

## Artifact identity

- Deck SHA-256:
  `2e45e9d18d05526f348b1969be0e374f958f2aafc3bb20ab2a7ead1759836729`
- Delivery ZIP SHA-256:
  `5217324951edd9d70ed1f144e80a81f4b879161559791d594b921b60f497d12a`
- Params SHA-256:
  `a6e9256c54fe683f0557abc68ad9b801f8bc4a375ed3829a5b4e30efe8b88688`
- SPC engine declared by all four inputs: `0.10.0`
- AGF graph version declared by all four inputs: `1.3.0`

The delivery manifest independently records every projected-context artifact,
its embedded context identity, source graph identity, runtime/resource set, and
the hashes of all four packaged delivery artifacts.

## Editorial spot check

The result is suitable as a release reference, not merely a structural test.
Its no-astro handler summaries remain concrete and differentiated—for example,
`Ella Lives in Chapters`, `Give Ella a Base, a Boundary, and a Brief`, and
`Train the Return, Not the Disappearance`. Summary bodies average 76.4 words
across all densities and audiences versus 85.3 in the prior Phase-6 reference,
placing this deck modestly closer to the UI-friendly middle without collapsing
the four lenses.

Both dynamic sections contain four independent chapters. Each registry entry
has a distinct long title, short navigation title, emoji, stable ID, order, and
one-sentence subtitle. Interdogpendence uses relationship/process organization
such as `When Spark Meets Structure`; Takeaways uses conclusion/support framing
such as `Skills That Keep Her Spark`. No title is shared across the sections.

## Preserved evidence

The exact successful deck, selected authoring packet, delivery manifest,
assembly report, validation report, and lint report are preserved under:

`astrowoof_natal/qa/reference_decks/ella/20260805-release-candidate-live/`

Raw provider request/response payloads and reconstructable multi-gigabyte run
workspaces are deliberately not committed.
