# Evidence — Hound external-authority v2 authorization mismatch

| Field | Value |
| --- | --- |
| API run | `686d78a3-f412-4e5b-88c0-f3ef27edb48d` |
| Native run | `2b049c4a941fe7c1d2113525b16fc7eee3fed4bc527b6d4b165dea9e8cefd800` |
| SBE release | `0.4.44` |
| Reported refusal | `ExternalAuthorityV2ExecutionError: authorization_mismatch` |
| Diagnostic log export | `C:\tmp\sbe-worker-20260904-v2-authority-mismatch-last-hour.ndjson` |

SBE logs aid chronology but do not replace API/PostgreSQL authority.

## Slice 0–1 evidence

- At `10:46:07Z`, the execution trace emitted both
  `external_authority.request_selected` and
  `external_authority.fence_validated` for Hound's fresh successor authority
  pair. The fresh grant therefore passed the SBE public fence; it is not
  evidenced as malformed or stale.
- The same invocation then emitted
  `intent_revalidation_deferred reason=action_state_or_custody_mismatch`.
  Native summary at revision 59 showed the predecessor action as `REPORTED`,
  zero provider custody, and a still-live `PROVIDER_PENDING` v2 intent holding
  the predecessor request/grant identities.
- Released `0.4.44` source confirms the exact ordering: the ordinary response
  reconciliation cycle publishes state and a snapshot with `persist_state()` /
  `write_workspace_snapshot()`; it does not request v2 intent retirement. The
  public v2 CLI catches that stale-intent refusal but then calls dispatch with
  the fresh request/grant. Dispatch correctly compares those identities to the
  old live intent and raises `authorization_mismatch` before payload resolution
  or provider creation.
- The initial provider-free characterization demonstrated the erroneous
  dispatch. The repair regression now proves the replacement behavior:
  `test_public_cli_refuses_unretired_completed_intent_without_dispatch` returns
  a v4 command result whose v5 dispatch result says
  `completed_intent_retirement_required`, with zero dispatch calls, payload
  resolutions, or provider creates.
- The reconciliation coordinator now calls the existing strict retirement
  helper only after local response adoption/fan-in. The retained-intent suite
  proves completed/reported inventory retires and replays exactly, while a
  partial terminal inventory remains live.
- The CLI classification is deliberately narrower than its triggering error
  family. It emits v4/v5 only when a copied native-state retirement proof
  establishes one different retained intent whose entire ordered inventory is
  `REPORTED`, has complete response evidence, and has neither custody nor
  ambiguity. A provider-pending/non-`PREPARED` action-state mismatch regression
  preserves the original exception and produces no v4/v5 result.

Focused repair suite: 17 passing provider-free tests on 2026-09-04. This does
not authorize mutation of Hound or establish that API must create a replacement
grant; subsequent authority remains a fresh API decision from a fresh native
inspection.

## Slice 3 installed-wheel qualification

- Candidate version: `0.4.45` (frozen before build/qualification).
- Two builds with `SOURCE_DATE_EPOCH=1778064000` were byte-identical:
  `bcee274df15e877ca54efecbada15bed8565a604493689fdc9790e6178aeb42b`.
- An isolated environment installed the candidate wheel and local
  `semantic-projection-core==0.11.1`; the installed retirement qualification
  passed provider-free with zero external network/provider calls and zero spend.
- The v5 dispatch-result and v4 command-result packaged schema readers returned
  their exact public IDs. The installed three-case CLI regression passed outside
  the source checkout.
- After installing the declared `jsonschema` dependency, isolated `pip check`
  reported no broken requirements.
