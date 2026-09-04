# Background — Hellmanistic Hound external-authority v2 authorization mismatch

## Scope

This is a bounded, read-only SBE companion investigation for a fresh QA cohort
on released SBE `0.4.44`. Do not resume, reconcile, repair, mutate a retained
workspace, access the provider, create a new provider operation, write R2,
deploy, release, or change the active run. Use local source/tests, supplied
non-authoritative logs, and only separately authorized bounded checkpoint
HEAD/GET inspection.

## Exact subject

- QA API run: `686d78a3-f412-4e5b-88c0-f3ef27edb48d`.
- Reading: `a2d32a70-6718-486b-94e9-45b6dbefe107`.
- Native run: `2b049c4a941fe7c1d2113525b16fc7eee3fed4bc527b6d4b165dea9e8cefd800`.
- QA profile: `astrowoof.qa.sbe0444-dormant-theme-retirement.v1`.
- Installed SBE release: `0.4.44`.

The comparison cohort run, Okey-Dokey Dogmeat, is API run
`a31383a7-472a-4afb-b8b0-3222ff283313`, native run
`1e9836263f34989c588c185790e3f18aeb9d63a76f92e7e36c89149eef0a0848`.
It has not entered v2 and should not be conflated with the Hound fault.

## Observed API-side state

Hound has six reported initial actions, one reported polish action, and one
authorized polish action. Two paid actions have an
`external_authority_v2_admission_id`. The run is still nonterminal. This does
not authorize native mutation or prove the native state is valid.

## Non-authoritative native trace chronology

At 2026-09-04T10:46:07Z, the Hound native trace recorded:

1. `external_authority_request_read_complete`, kind `ordinary_action_set`,
   action count 1;
2. lifecycle inspection with `AWAITING_SPEND_AUTHORIZATION`, selected
   `await_external_authority`, and `request_present=True`;
3. `external_authority.request_selected` with selected command
   `external_authority_v2_dispatch`;
4. `external_authority.fence_validated`; then
5. `command_refused command=external_authority_v2 phase=dispatch
   reason=authorization_mismatch error_class=ExternalAuthorityV2ExecutionError`.

Nearby summaries report a v2 intent `PROVIDER_PENDING`, one v2 action, no
retained provider custody, and one prepared action. This apparent sequence must
be interpreted from exact public contracts/state transitions—not from status
name inference.

Several fields named request/grant SHA-256 differ across emitted event types.
They might intentionally hash different structures. Do not label this as a hash
bug until the event schemas and their input domains are traced.

## Log export

API exported the unfiltered previous hour of QA SBE-worker logs in four
15-minute read-only windows:

`C:\tmp\sbe-worker-20260904-v2-authority-mismatch-last-hour.ndjson`

This is diagnostic/non-authoritative. It includes structured events, trace
lines, and command results. It is the starting timeline, not native authority.

## Investigation goals

- Identify the exact v2 authorization predicate that refused and the inputs it
  compared.
- Determine whether SBE received an invalid API public artifact, compared the
  wrong version/domain, or exposed an ambiguous native/document transition.
- Build a provider-free reproduction using genuine public API/SBE boundaries.
- Request immutable checkpoint coordinates only if source/log evidence cannot
  prove the issue; specify each object, expected hash, and exact HEAD/GET count.
