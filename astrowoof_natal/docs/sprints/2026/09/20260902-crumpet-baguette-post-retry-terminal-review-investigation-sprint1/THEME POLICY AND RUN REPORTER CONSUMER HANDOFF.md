# Theme policy and run reporter consumer handoff

Status: source- and installed-wheel-qualified 0.4.39 candidate; final source
commit and release approval pending.

## Theme-group acceptance policy

New pass evaluations retain theme-group coverage, balance, and cross-section
mirroring findings as deterministic advisories. Advisory-only pass 6 is
accepted. The advisory does not consume a creative retry and does not create
provider authority.

The complete advisory projection is persisted in the native
`astrowoof.authoring_pass_gate.v0.2` report:

- `advisory_issue_codes`;
- `advisory_affected_claim_ids`; and
- advisory-aware bounded `guidance`.

Hard `editorial_issue_codes` remain rejection-only. Invalid registry structure
and assignments to unregistered IDs remain hard failures. Unknown finding codes
fail closed as hard findings.

The worker also emits a sanitized `pass_acceptance_advisory` trace containing
only advisory codes and affected-claim count. Neither the report nor the log
contains prompt/card content in these summary fields.

No API routing or lifecycle change is required. Historical v0.1 QA reports,
including Crumpet and Baguette, retain their original meaning and bytes.

## Run reporter

The release adds an opt-in diagnostic surface:

```text
astrowoof-run-report build --input worker.log --output-dir report
astrowoof-run-report parse --input worker.log --output report.json
astrowoof-run-report render --report report.json --format md --output report.md
astrowoof-run-report-qa --output qualification.json
```

`build` emits validated JSON plus deterministic Markdown, self-contained HTML,
and Mermaid views. It accepts exported local log files only. It accepts no run
workspace, provider credential, network endpoint, authority document, or
transition command.

The report is diagnostic—not lifecycle, custody, terminal, billing, acceptance,
or recovery authority. Missing log evidence never proves that an event did not
occur. No-progress candidates identify repeated semantic posture without a
direct progress witness; they are review prompts, not defect verdicts.

## Real-export qualification

The source candidate parsed the supplied 2026-09-02 Render export with:

- source SHA-256:
  `9ede6c03d27794eca19538f5c20f432a177b308cd0dfddf72c0a02bbed3e2854`;
- lines: 2,149;
- marked `✨🐶` records: 1,829;
- parsed marked records: 1,829;
- malformed marked records: 0;
- recognized JSON execution/command envelopes: 317;
- unknown registered events: 0; and
- native runs: 2.

The installed candidate's generated report file SHA-256 is
`5ec69134c8462bc37198735402fed49dcb2dbc7fafa995c82198c2add4dcb1e6`;
its self-declared canonical report SHA-256 is
`275adde8f770fa1ec714c3dca3fec3bad1de296efe1c5ba0b8dbfa89a3791732`.
Its nine no-progress candidates remain diagnostic and have not been classified
as nine pipeline defects.

## Release boundary

Both CLIs and both qualification commands were exercised from the clean
installed candidate wheel. Package schemas and root-level Python readers
resolve from that wheel. The qualification was provider-free, network-free,
R2-free, and native-workspace-free.

The deterministic candidate wheel SHA-256 is
`06217b35a5cc024123bc3855c087b0f5c13864b06051d9847f90214c2da43fe4`.
Its canonical theme-policy qualification receipt SHA-256 is
`8572848ce703aeb2ec208bb26fedae868d7e85970bd9a3f5cead440e5cbe1d88`;
the run-reporter qualification receipt SHA-256 is
`8005e4bb9891052419223bdbda2b8cdfdd9158fcee13b150ae1556f280ae3634`.
