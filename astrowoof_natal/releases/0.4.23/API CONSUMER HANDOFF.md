# API Consumer Handoff — SBE 0.4.23

The normative detailed handoff is:

- `docs/sprints/2026/08/20260825-ambiguous-provider-submission-contract-sprint1/AMBIGUOUS PROVIDER SUBMISSION API CONSUMER HANDOFF.md`

Validate the packaged provider dispatch v3 and command result v2 pair before
mapping capacity or custody. Pre-provider refusal permits release only of the
exact proven-unspent API reservation(s) joined from API authority. Ambiguity
retains review custody and prohibits create. Durable identities are
reconciliation-only. Exact replay causes no new transition.

The installed wheel exposes:

```text
astrowoof-provider-dispatch-result --packaged-fixtures --output fixtures.json
astrowoof-provider-dispatch-result --input result.json --output validated.json
```

This command is provider-free and qualification/validation-only.
