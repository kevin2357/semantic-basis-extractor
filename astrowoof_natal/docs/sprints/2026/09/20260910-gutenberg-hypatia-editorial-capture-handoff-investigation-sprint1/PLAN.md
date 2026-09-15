# Plan

Status: complete. The exact detached terminal-review handoff correction was
qualified, approved, released as immutable `0.4.59`, and verified by a fresh
download of the published wheel and checksum.

## Slice 0 — Frozen provenance and handoff inventory

Status: complete. The loss boundary was classified at native command
serialization/adapter handoff rather than packet or observer behavior.

- Validate the supplied checkpoint/result/receipt coordinate packets.
- Map the three exact native-to-API handoff shapes without treating them as one
  generic terminal path:

  | Path | Native command output | API adapter evidence required |
  | --- | --- | --- |
  | terminal review | exact `terminal_review_command_result` | preserve the same command-result object and its result/receipt identity |
  | fresh ordinary delivery | exact `terminal_delivery_command_result` | carry its exact `result_id` as `sealed_terminal_result_id` |
  | retry / delivery validation | exact sealed publication from that invocation | carry the same immutable result identity without latest-result discovery |

- For each path, distinguish four possible seams: native publication, command
  serialization, subprocess parsing, and `SbeCycleResult` translation.
- Classify the initial Hypatia publication retry without runtime changes. Treat
  it as expected only if the authoritative delivery inputs changed between the
  failed and successful attempts; identical authoritative inputs indicate a
  race or contract violation.
- Prefer provider-free source/log proof. Request bounded checkpoint access only
  if the exact invocation output cannot otherwise be established.

## Slice 1 — Provider-free reproduction or contract correction

Status: complete and approved. The detached exit-3 terminal-review path emits
the exact same-invocation v0.2 command-result handoff; nonterminal exit-3
behavior remains unchanged.

- Build the narrowest provider-free fixture for any missing identity/handoff.
- Cover terminal review, fresh delivery, and delivery-validation retry as
  separate adapter cases, even if they share one implementation correction.
- Keep captures observational and post-publication.
- Do not introduce latest-result discovery or a synthetic result identity.

## Slice 2 — Package qualification, if SBE changes

Status: complete through immutable `0.4.59` publication and authenticated
fresh-download verification.

- Test the exact consumer handoff from an installed wheel before release.
