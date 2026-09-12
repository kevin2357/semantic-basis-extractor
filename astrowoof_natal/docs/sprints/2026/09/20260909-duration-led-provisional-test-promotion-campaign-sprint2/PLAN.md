# Plan — duration-led provisional test promotion campaign Sprint 2

## Status

Slices 0 and 1's Batch 12 state-surface audit are complete. The concurrent
editorial-review packet family is frozen and selected as the coherent Batch 12
cohort. Paused at the campaign paws-point before bounded collision
qualification; no manifest promotion has occurred.

## Objective

Continue safely reducing the provisional tail, calibrate execution profiles,
prove whole-suite equivalence, and close the adopted test workflow without
mixing campaign commits into concurrent package-release work.

## Slice 0 — checkpoint and moving-family intake

**Complete.** See `SLICE 0 - CURRENT TREE AND MOVING FAMILY INTAKE.md`.

- Verify Sprint 1's final 78/18/36 manifest and Batch 11 receipt identities.
- Re-discover every active test module and require exactly-once classification.
- Wait for the editorial-review packet sprint to freeze its four-module family;
  then inventory and measure that family without presuming promotion.
- Refresh durations only where source/test identity changed since the frozen
  campaign inventory, recording provenance rather than silently replacing old
  weights.
- Confirm no other concurrent test module entered without conservative
  `provisional` classification.

## Slice 1 — adaptive promotion batches beginning with Batch 12

**Batch 12 manifest promotion is applied after approval, but actual-manifest
stress is blocked by a reproducible current-main frozen BRE packet-digest
mismatch.** See
`SLICE 1 - PROMOTION BATCH 12 STATE-SURFACE AUDIT.md` and
`SLICE 1 - PROMOTION BATCH 12 COLLISION QUALIFICATION.md`, plus
`SLICE 1 - BATCH 12 ACTUAL-MANIFEST STRESS BLOCKER.md`. Paused for review
before changing the unrelated baseline or rerunning the paired stress gate.

- Select remaining candidates by descending useful duration and state-surface
  similarity, not a fixed three-module quota.
- Use smaller cohorts for expensive/stateful modules and larger cohorts for
  simple subsecond modules, capped to host-appropriate collision concurrency.
- For each batch: audit state surfaces, pause for review, run bounded collision
  qualification, pause for promotion approval, update only approved manifest
  rows, run guards, and repeat concurrent actual-manifest stress.
- Retain modules as provisional or classify them serially when isolation
  evidence is insufficient; eliminating the provisional class is not required.
- Preserve the semantic-closure behavioral family as serial unless a separately
  approved equivalence/refactor exercise proves otherwise.

## Slice 2 — worker-count and scheduling calibration

- Compare one, two, three, and four workers on the materially expanded safe set.
- Measure wall time, variance, CPU and memory pressure where available, file-lock
  residue, and serial-tail contention.
- Keep one worker as the conservative local default unless repeated evidence
  supports a higher default; preserve higher-worker profiles for stronger CI
  hardware even when this laptop shows no speedup.
- Define a controlled weight-refresh procedure with recorded source and timing
  provenance.

## Slice 3 — authoritative whole-suite equivalence

- Freeze candidate manifest and source identities.
- Run repeated one-worker and selected multi-worker broad suites.
- Require identical exact test and outcome inventories, including skips,
  expected failures, failures, errors, and unexpected successes.
- Inject deterministic worker failures and retain exact reproduction commands.
- Prove disjoint work roots, no orphan subprocesses or Windows lock residue, no
  external activity, and unchanged serial release authority.

**Campaign paws-point:** approve or reject the final promoted set and execution
profiles.

## Slice 4 — distributed-growth manifest architecture

- Design a backward-compatible closed manifest schema for future natal,
  synastry, transit, and production-path simulation suites.
- Evaluate fields for pipeline ownership, tier, resource class, duration
  provenance, isolation needs, protected logging, serial-authority reason, and
  eligible local/distributed profiles.
- Produce deterministic local/laptop and distributed-CI shard projections from
  the same repository authority.
- Preserve exact local reproduction of remote failures and explicitly serial
  deterministic build/release authority.
- Avoid binding the contract to one CI vendor.

## Slice 5 — workflow adoption and closeout

- Update runner guidance, release playbook, classification intake, promotion
  evidence, calibration, and failure-reproduction procedures.
- Update the relevant Control Room issue with timings and remaining exclusions.
- Run focused runner guards, diff hygiene, and one final supported broad
  invocation.
- Close without a package release unless installed package behavior/resources
  changed; otherwise use the normal release playbook under a fresh version.

## Success criteria

- Every active test remains classified exactly once.
- Promotions preserve semantics, identity, outcomes, and failure sensitivity.
- Execution profiles scale to stronger hardware without weakening isolation.
- Whole-suite equivalence and deterministic failure reproduction are retained.
- External systems remain untouched and release authority remains serial.
