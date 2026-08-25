# API Agent Slice 0 Review

Date: 2026-08-25

## Verdict

Approved to proceed to Slice 1.

The reproduction isolates the exact observed seam without touching the frozen QA
cohort, and the public-path evidence supports the proposed precedence correction:
retained provider custody and required provider-result fan-in must be exhausted
before SBE exposes a later external-authority request.

## Confirmed contract interpretation

- Due provider custody continues to select only SBE's bounded subset (four here).
- Not-due custody must produce the existing reconciliation command with native
  `not_before`, not `await_external_authority`.
- Completed evidence requiring local fan-in must select `ordinary_resume` and
  suppress external authority until the fan-in records a new checkpoint basis.
- Under an unchanged workspace basis, trusted time can alter reconciliation
  eligibility/subset only; it must not add or remove authority inventory.
- Existing v0.5/v0.6 fields are sufficient for these branches. No API schema or
  command-rerouting change is needed if those public meanings remain intact.

## Slice 1 gates

Please make the failing combinations explicit in the public semantic validators,
including both a direct lifecycle contradiction and the temporal basis-digest
stability assertion. Keep diagnostic detail redacted to counts, reason categories,
and digests. No provider I/O, new provider creation, authority consumption, or
frozen-QA access is authorized by this review.
