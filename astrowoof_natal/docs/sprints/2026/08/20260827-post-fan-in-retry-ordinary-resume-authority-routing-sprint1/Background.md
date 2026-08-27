# Post-fan-in retry: `ordinary_resume` authority-routing investigation

## Status

Planning-only incident record. No implementation, provider work, retained-run
mutation, deployment, or release is authorized by this document.

## Incident

On 2026-08-27, a fresh two-run QA qualification cohort reached the post-fan-in
creative-retry path. The initial six-member waves completed and were durably
reported for both runs. Two later OpenAI Responses retry calls also appeared
complete in the provider dashboard, but neither result was ingested by the
AstroWoof API/SBE boundary.

The QA SBE worker was paused after diagnosis to prevent further futile attempts.

### Cohort and identities

| Pup | API run ID | Native run ID |
| --- | --- | --- |
| Strudel McSniff | `e664f04c-14bd-481e-8800-e1b3b768d012` | `e396df661d3c34e24c77a3dc0a02c068f204c69be8129b08505d3231272b9f1a` |
| Princess Pumpernickel | `fb1c03e7-a7df-4e4e-8422-6f77846ce358` | `c6960f033b5f4f7f175968e605cd3540e0402dd696d2dd150ff3fd675bacca55` |

The active QA SBE worker was `srv-da12sktbedkc73btpu00`.

## Authoritative evidence

All timestamps below are UTC.

1. Strudel's retry provider operation was created at `19:50:26.011758Z`:
   `resp_05032fd8aff1a69d006a90950139f087d0823ec7cb1abac425`.
2. Princess's retry provider operation was created at `19:51:44.029698Z`:
   `resp_0ffb749787e56f3f006a90954f64e087d085dddb8de925860a`.
3. For both operations, API persistence contains only the initial
   `identity_recorded` / `pending` observation. The corresponding
   `sbe_paid_actions` remain `provider_created`; neither has a provider-result
   observation, `reported` action state, or reported cost.
4. Both initial waves are already fully `reported` (six actions each). Their
   reported costs were USD `0.824529` (Strudel) and USD `0.832820` (Princess).
5. Strudel has a further creative-retry action in `authorized` state, created
   at `19:54:16.037054Z`, with no provider operation. This was not a new
   provider request.
6. At the point of pause, Strudel was `running` with a leased SBE job and an
   active capacity allocation on slot 1. Princess was `running` with its job
   in `retry_wait` and its allocation released. The cohort had one QA SBE slot,
   so Strudel's retained allocation prevented Princess from receiving a turn.

## Non-authoritative SBE trace evidence

The Render trace logs are diagnostic evidence only; they do not authorize a
repair. They establish the execution-side selector behavior that the database
alone cannot show.

### Expected early behavior

For both runs, SBE initially selected `provider_reconciliation`, reported one
provider-local dependency, and used `release_until_due`. This was compatible
with a genuinely pending Response.

### Actual broken Strudel behavior

After the retry was provider-created, the trace transitioned to a repeating
local loop:

- `execution_branch=local_resume`
- `execution_capacity_disposition=continue_local_cycle`
- `outcome=quiescent`
- `local_continuation_required=true`
- `provider_local_dependency_count=0`
- job deferred with `reason_code=native.quiescent`

The worker repeatedly reclaimed Strudel's job (at least attempts 10 through
19) roughly once per minute. It released each lease, but retained Strudel's
sole capacity allocation, thereby starving Princess.

The decisive live trace at `2026-08-27T20:03:12.333569Z` (SBE release `0.4.26`)
records:

```text
event_name=lifecycle.local_work_selected
selected_command=ordinary_resume
operation_count=1
```

The selected command then fails in `astrowoof-semantic-closure` with:

```text
InitialWaveError: Initial-wave member authorizations require the exact
snapshot-bound external-authority request and aggregate grant
```

This means the failure is not a slow OpenAI response, a capacity shortage at
the provider, or a missing API spend decision. A one-operation post-fan-in
continuation is being routed through an initial-wave external-authority guard.
That is incompatible with the intended distinction between ordinary retained
continuations and the six-member initial-wave admission.

## Scope and desired outcome

This is primarily an SBE selector/command-classification and authority-routing
defect. The eventual sprint should determine the smallest general correction
that ensures:

1. a post-fan-in creative retry with retained provider lineage is selected as
   the correct reconciliation/ordinary continuation path;
2. the initial-wave aggregate-grant guard is applied only when an actual fresh
   initial-wave admission is being attempted;
3. an `ordinary_resume` cannot report `quiescent` while its chosen path cannot
   execute because of an incompatible initial-wave authorization precondition;
4. local continuation/capacity retention cannot starve another run when no
   executable local work remains; and
5. result ingestion remains idempotent and does not reconstruct or infer
   private API authority.

The existing external-authority-v2 and reconciliation contracts should be
reviewed rather than bypassed. The API must remain the authority owner, and
SBE must not manufacture a grant to make the error disappear.

## Suggested investigation sequence

1. Reproduce this exact lifecycle state provider-free using the executable
   lifecycle simulator and/or a sealed workspace fixture.
2. Trace the selector inputs that produce `lifecycle.local_work_selected` and
   `ordinary_resume` for Strudel's one-operation inventory.
3. Identify why the selected command invokes the initial-wave member
   authorization guard; confirm whether the problem is selector classification,
   command plumbing, or guard scope.
4. Add a focused regression covering both the correct post-fan-in retry
   successor and the two-run/one-slot starvation consequence.
5. Only after the contract and regression tests are clear, define the API
   companion work (if any). Do not treat the retained QA cohort as the primary
   test fixture or as the reason to broaden normal production behavior.

## Operational disposition

- The QA SBE worker was suspended through Render's service-suspend API and
  verified as `suspended` on 2026-08-27.
- No provider reconciliation, retry, terminalization, capacity mutation, or
  retained-run repair was performed during this incident capture.
- Both completed provider responses remain preserved for later evidence-based
  assessment; their provider-dashboard completion does not itself authorize
  ingestion or recovery.
