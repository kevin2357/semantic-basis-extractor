# API Consumer Handoff — SBE 0.4.22

The detailed contract is:

- `docs/sprints/2026/08/20260825-provider-reconciliation-precedes-external-authority-sprint1/PROVIDER CUSTODY PRECEDENCE API HANDOFF.md`

Consumer summary:

1. Validate lifecycle v0.5 or temporal lifecycle v0.6.
2. Invoke only `execution_branch.command` / `temporal_decision.selected_command`.
3. Never select or reconstruct reconciliation members.
4. A not-due reconciliation branch releases native/local capacity until SBE's
   `not_before`; it does not release API consumer authority or reservations.
5. Completed provider evidence runs deterministic fan-in before later authority.
6. Accept `await_external_authority` only from the successor checkpoint basis after
   retained provider custody/fan-in is exhausted.
7. Pin SBE 0.4.22 with exact SPC 0.11.1 and prove the newly deployed worker/profile
   pair before creating a paid QA cohort.
