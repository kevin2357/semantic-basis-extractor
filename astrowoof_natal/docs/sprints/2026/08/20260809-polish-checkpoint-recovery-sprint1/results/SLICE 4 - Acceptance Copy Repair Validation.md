# Slice 4 - Acceptance Copy Repair Validation

Status: complete; gate approval pending.

## Scope and isolation

The canonical retained acceptance run remained untouched. Two complete copies
were made outside Git:

- working copy: `C:\tmp\sbe-polish-repair-slice4-working`;
- backup copy: `C:\tmp\sbe-polish-repair-slice4-backup`.

Both began with 878 files and the same `run.json` SHA-256 as the canonical run.
The working copy was mounted at its required Linux logical path
`/work/run/sbe-run-2`; the backup was mounted separately and read-only. All
inspection, repair, and resume checks used the existing acceptance image with
networking disabled.

## Dry-run result

The installed-source repair command accepted the copy and reproduced the
frozen Slice 0 model exactly:

- run ID and revision 60 matched;
- the only mismatches were the same final deck, lint report, and validation
  report;
- each current hash equaled its retained attempt-1 hash;
- attempt 1 matched the durable Response ID and 16,644 micro-USD report;
- action 2 was `PREPARED`, unused, and providerless; and
- the external authorization matched its exact binding.

## Pre-apply correction

The planned offline resume check identified that a persisted `SUBMITTED`
polish attempt needed to be reused explicitly. Otherwise a later authorized
resume could skip the prepared attempt because the attempt list had already
reached its maximum length. No repair had been applied when this was found.

Production polish resume now reuses the final `SUBMITTED` attempt at its
existing attempt number. Repair reconstructs both attempt 1 as
`POLISH_IMPROVED_PARTIAL` and attempt 2 as `SUBMITTED`. Focused regression tests
prove that resume executes the same attempt object without appending attempt 3.

## Apply and interruption result

The user explicitly authorized applying repair to the working copy only. The
offline command exceeded the local 180-second harness timeout after publishing
revision 61 and the new snapshot but before writing its external report. SBE
did not retry the operation. Read-only post-interruption validation established
that the checkpoint itself had completed successfully:

- native workspace snapshot validation: pass;
- snapshot SHA-256:
  `16d115e2b7573212df54cc2bcbcd825b20afd6521da0169f92dea7652d22048a`;
- status: `AWAITING_SPEND_AUTHORIZATION`;
- attempt states: `POLISH_IMPROVED_PARTIAL`, `SUBMITTED`;
- accepted-pass digest unchanged: true;
- complete spend-ledger digest unchanged: true;
- action 2: `PREPARED`, with no authorization, consumption, or provider ID.

The absent external report is classified as a harness-timeout artifact, not a
checkpoint-integrity failure. This result record and the compact Slice 4 JSON
preserve the independently validated before/after evidence. The backup and
canonical workspace remain unchanged.

## Offline resume boundary

The repaired copy was resumed through the real polish and spend-controller
path with an OpenAI transport that raises if called. The result was:

- exact awaiting action: `paid_0d941d208206a4d8b0349f91`;
- attempt count before/after: 2 / 2;
- provider transport calls: 0;
- persisted action state: `PREPARED`;
- snapshot still valid: true.

No authorization was supplied to the runner, consumed, or persisted. No
provider operation or incremental spend occurred.

The complete deterministic repository suite passed: 165 tests in 87.805
seconds.

## Canonical-run consequence

The repaired-copy evidence qualifies the constrained procedure for this exact
run shape. It does not authorize mutation of the canonical retained run or a
provider-connected resume. Either action remains separately gated by the API
owner.

Next action: approve the acceptance-copy evidence before the Slice 4 commit and
Slice 5 patch-artifact and consumer-handoff work.
