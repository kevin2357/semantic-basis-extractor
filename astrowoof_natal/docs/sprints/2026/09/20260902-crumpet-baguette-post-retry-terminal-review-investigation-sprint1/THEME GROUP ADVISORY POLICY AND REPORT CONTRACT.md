# Theme-group advisory policy and pass-gate report contract

Status: implemented and published in SBE 0.4.39
qualification.

## Decision

Theme-group data remains authored, validated, persisted, and observable. The
currently provisional distribution/editorial rules no longer decide whether an
otherwise valid pass is accepted:

- `theme_group_coverage` is advisory;
- `theme_group_balance` is advisory; and
- `cross_section_theme_mirroring` is advisory.

Structural integrity remains hard acceptance authority:

- malformed or incomplete registries remain `theme_group_registry` rejection;
- assignments to an ID absent from the applicable registry are the distinct
  `theme_group_assignment` rejection; and
- unrelated existing deterministic-QA failures are unchanged.

Unknown finding codes are not advisory merely because they concern theme
groups. Only the closed advisory set above is downgraded.

## Public/native evidence

Newly evaluated opaque pass reports use
`astrowoof.authoring_pass_gate.v0.2`. The report retains the v0.1 rejection
projection and adds an independent advisory projection:

```json
{
  "schema_version": "astrowoof.authoring_pass_gate.v0.2",
  "workspace": "...",
  "status": "accept",
  "editorial_issue_codes": [],
  "affected_claim_ids": [],
  "advisory_issue_codes": ["theme_group_coverage"],
  "advisory_affected_claim_ids": ["..."],
  "guidance": "..."
}
```

`editorial_issue_codes` and `affected_claim_ids` remain rejection-only.
Advisories never masquerade as rejection evidence. A report with one or more
hard findings remains `reject` even when it also contains advisories.

Historical v0.1 reports remain immutable evidence of the policy in force when
they were produced. They are not reinterpreted or rewritten.

## Runtime behavior

- Advisory-only pass 6 is accepted and persists its v0.2 QA report.
- Advisory-only findings do not prepare or authorize a creative retry.
- The parent worker emits one sanitized `pass_acceptance_advisory` trace with
  codes and affected-claim count; it emits no prompt or content.
- The pass-6 prompt and provider request are unchanged.
- API lifecycle, custody, authority, and terminal contracts are unchanged.

The persisted QA report is durable native evidence. Text logs are diagnostic
and may be retained for a shorter period; they are not acceptance authority.
