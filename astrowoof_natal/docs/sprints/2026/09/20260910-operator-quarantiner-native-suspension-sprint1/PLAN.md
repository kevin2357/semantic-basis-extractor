# Plan

## Status and authority

Only Slice 0 is planned. This plan authorizes no live QA run, provider work,
quarantine execution, runtime correction, suspension-contract implementation,
process termination, or cleanup.

## Evidence limitation

The historical failed assessed-quarantine workspace is gone. The QA reset
dropped and recreated the database and deleted the associated R2 objects. Unless
an independent log archive appears, its exact workspace, checkpoint, subprocess
output, and admission decision cannot be reconstructed.

Slice 0 will therefore reconstruct the **current production boundary**, not
claim to reproduce the historical incident. It will use current code and a
genuine provider-free SBE-generated workspace to determine whether a present
deterministic failure can reproduce the remembered symptom: the operator runner
failed to receive a valid public disposition assessment.

## Slice 0 — Provider-free nice-path reconstruction

### Objective

Exercise this complete boundary without mutating real operational state:

```text
supported SBE lifecycle construction
  -> exact workspace and checkpoint/archive
  -> API restore into an isolated temporary root
  -> installed SBE disposition-assessment subprocess
  -> stdout/stderr/exit/timeout capture
  -> API schema, digest, and identity validation
  -> quarantine dry-run admission or typed refusal
```

The final step is admission logic only. It must not enqueue or execute a
quarantine request, fence a real job, release capacity, or write API/R2 state.

### 0A — Current source map

Jointly trace and record:

- how SBE constructs and validates
  `astrowoof.operator_disposition_assessment.v1`;
- native evidence determining custody class, quarantine posture, reason, and
  supported next actions;
- public CLI arguments, installed resources, working-directory assumptions,
  stdout/stderr behavior, exit codes, and timeout expectations;
- how API restores the archive, selects the installed executable/interpreter,
  sanitizes the environment, and captures streams;
- API parsing, assessment digest, and run/workspace/checkpoint identity joins;
- dry-run admission and the checks that would be repeated before mutation.

Finding a plausible mismatch is not permission to patch it in Slice 0.

### 0B — Genuine native fixture

Construct one assessment-eligible workspace using supported SBE lifecycle APIs
and writers, not hand-authored internal workspace JSON. It must:

- contain only synthetic identities/content;
- make zero provider calls and incur zero spend;
- reach a documented custody class with v1 `quarantine_posture=permitted`;
- contain exact workspace/checkpoint/result/receipt identities;
- validate through ordinary native readers before archival;
- produce deterministic inventory and archive digests;
- live under an owned temporary qualification root.

If no supported provider-free construction path can create a permitted
workspace, stop and record that as the finding rather than fabricating state.

### 0C — Archive/restore equivalence

Pass the generated workspace through the real checkpoint/archive and API restore
shapes. Prove:

- declared and actual member identities and byte counts agree;
- restored bytes equal source bytes;
- logical workspace identity survives physical relocation;
- no source-checkout path is needed after restore;
- no caches, credentials, undeclared files, or local paths enter the archive;
- assessment output before archive and after restore is byte-identical.

An isolated local object-transport stand-in is sufficient. No R2 access is
needed or authorized.

### 0D — Installed subprocess and admission proof

From outside both source checkouts, invoke the exact installed SBE assessment
CLI through API's production subprocess adapter. Retain:

- installed package version and entry-point/module location;
- bounded stdout and separately bounded sanitized stderr;
- exit code, timeout result, and duration;
- parsed contract version and assessment digest;
- exact run/workspace/checkpoint identity comparison;
- custody class, posture, reason, and supported actions;
- API dry-run admission result and reason;
- zero provider/network/spend/workspace/quarantine mutation counters.

Success requires one valid permitted assessment to reach dry-run admission. A
valid semantic refusal proves transport but does not satisfy that positive path.

### 0E — Deterministic failure matrix

Exercise the real subprocess/parser boundary for:

- valid permitted, native-prior-action, and prohibited assessments;
- no assessment output;
- malformed or truncated stdout;
- wrong schema, digest, run, workspace, or checkpoint identity;
- nonzero exit with bounded sanitized stderr;
- timeout and missing/incompatible installed executable/resource;
- workspace/checkpoint identity change between attempts;
- duplicate unchanged reads with byte-identical output.

Faults belong at controlled adapter/fixture seams. They must not turn malformed
examples into valid production contract fixtures. Every cell records whether
the failure belongs to SBE construction/read, SBE CLI serialization, API
invocation, API parsing/identity validation, or API admission.

### 0F — Retry decision

Use the matrix to decide whether bounded read-only assessment retries are
justified. Any proposal must pin and revalidate exact workspace/checkpoint
identity, use fixed small attempt and wall-clock budgets, stop after any valid
semantic assessment, stop on identity change, and retain each attempt's output.

Retry may recover failure to obtain an assessment. It must never poll until SBE
changes a valid semantic answer.

## Required Slice 0 conclusion

The joint result must state:

1. whether the current nice path works end to end for a genuine permitted
   workspace;
2. whether any deterministic current failure reproduces the historical symptom;
3. whether the failing layer is bounded to SBE, API, or deployment configuration;
4. which conclusions are proven versus hypothetical;
5. whether a narrow correction is warranted;
6. whether a bounded live QA experiment could add information unavailable from
   provider-free qualification;
7. the exact authorization, spend ceiling, retained evidence, and stop
   conditions that experiment would require.

Use one final classification:

- **current nice path proven; historical cause unavailable**;
- **current deterministic defect reproduces the historical symptom**; or
- **production boundary remains incomplete or untestable**, naming the missing
  prerequisite.

Do not say the historical incident was reproduced without surviving historical
evidence proving equivalence.

## Exit gate

Pause after Slice 0 for SBE, API, and owner review. That review—not this plan—may
authorize a narrow correction, a bounded live QA experiment, additional
observability work, or planning for the residual not-so-nice suspension and
hard-stop layer.

