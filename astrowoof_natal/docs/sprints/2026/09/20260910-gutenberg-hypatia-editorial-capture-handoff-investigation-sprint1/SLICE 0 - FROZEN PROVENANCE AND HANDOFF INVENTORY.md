# Slice 0 — Frozen Provenance and Handoff Inventory

## Status

Complete for local source/log discovery. No retained checkpoint access was
requested or performed. The pinned native result and receipt identities are
corroborated by the unfiltered worker log.

## Coordinate and publication findings

| Run | Native terminal publication | API cycle after native return | Capture prerequisite reaching ingress |
| --- | --- | --- | --- |
| Gutenberg | `review_required`, result `nres_07686011f6203f77fb590e0e`, receipt `nreceipt_4f0d04f075359b55e1fed511`, invocation `ninv_87d2bd33357944ec8161c46e` | `terminal_closed`; job failed non-retryably as `native.terminal.review_required` | absent |
| Hypatia | `delivery_complete`, result `nres_dc1080caa04fd6b4302b0d8e`, receipt `nreceipt_1e3bfaec883c7a6155d76281`, invocation `ninv_8ae755f792b84f79b7097d5d` | first cycle `terminal_closed`, publication rejected and retried; next cycle `delivery_validation` / `delivery_accepted` | absent |

Both archives subsequently accepted at generation 9 match the coordinate
packet framing, but archive contents are not needed to prove that native
publication occurred: the logs contain exact invocation/result/receipt IDs and
the expected result digests.

## Exact three-path map

### Terminal review — Gutenberg

SBE completed an invocation-bound native terminal publication at state revision
64. Its command-exit log nevertheless followed the detached
provider-reconciliation convention: exit code `3`, outcome `review_required`,
and `result_id=unknown` in the command-exit payload.

The API stdout adapter recognizes an exact
`astrowoof.terminal_review_command_result.v0.1`, but `_run_resume` requires exit
code `2` when that envelope is captured. In the no-command-envelope fallback,
the adapter tolerates a nonzero return when mutable progress is terminal and
returns no invocation-bound command object. The cycle then closes from progress
without a `terminal_review_command_result`, so terminal ingress has no exact
result identity for editorial capture.

This is not a failure to seal native evidence. It is a command handoff/exit
semantics gap on detached provider reconciliation.

### Fresh terminal delivery — Hypatia

SBE completed a delivery publication at state revision 58 and exited `0`.
The first API cycle closed terminally, but downstream publication raised
`PublicationEligibilityError: SBE-accepted delivery authority is required`.
The job was retried as `terminal.publication.retry`.

The following cycle entered `delivery_validation`, accepted the delivery, and
completed the job. That cycle did not perform the terminal native invocation;
therefore it could not lawfully reconstruct the prior invocation's result ID,
and latest-result discovery remains correctly forbidden.

The retry is operationally recoverable but is not an expected clean ordering
boundary: accepted-delivery authority should be established from the same
invocation-bound terminal delivery command before publication is attempted.
The retry currently repairs delivery completion but cannot repair observational
capture identity.

### Retry / delivery validation

Delivery validation is a legitimate retry branch, but it is not an identity
source. It may carry an exact sealed result only when that identity was already
preserved from the native invocation. It must not discover a latest result or
mint a synthetic identity.

## Classification

- Native publication: passed for both runs.
- Native result/receipt identity: present and exact for both runs.
- Command serialization / detached return: primary suspect for Gutenberg.
- API cycle-result translation and publication ordering: primary suspect for
  Hypatia.
- Editorial packet/capture builder: not reached with the required identity;
  no evidence of a packet or Better Stack sink failure.
- Retained archive inspection: unnecessary at this stage.

## Slice 1 reproduction fence

Build provider-free regressions that prove:

1. detached provider reconciliation returning terminal review carries the exact
   command result despite its detached command-exit convention;
2. fresh delivery establishes accepted-delivery authority and carries the exact
   `sealed_terminal_result_id` in the same cycle before publication;
3. a later delivery-validation retry never discovers or manufactures a result
   identity, but retains an already-carried exact identity when supplied;
4. ordinary nonterminal detached exit-3 paths remain unchanged;
5. terminal ingress and editorial capture remain fail-closed when the exact
   handoff is genuinely absent or contradictory.

