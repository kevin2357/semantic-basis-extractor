# Three-Pup Provider-Lifecycle Envelope Investigation — Background

## Purpose

Investigate the repeatable QA failure in the fresh three-pup cohort launched on
2026-09-12.  This is an evidence-only investigation.  The first SBE invocation
for each run completed the initial wave; the second invocation then failed
closed with the API-recorded classification `worker_contract_failure` and
reason `sbe.contract.provider_lifecycle`.  The SBE trace reports
`SbeProviderContractError`: `SBE reconciliation envelope is unsupported`.

The question is whether the newly installed native/API contract pair has a
provider-lifecycle envelope incompatibility after an otherwise successful
initial-wave command.  Do not infer a provider failure from API state alone.

## Cohort and authoritative outcome

| Pup | API run ID | Native run ID | Initial wave | Terminal state |
| --- | --- | --- | --- | --- |
| Aldine Eclair | `fc0a6140-6b6f-4c08-b323-66864ce74857` | `27d72e6c31ff9a77d398a3090dc18585a39cb655f7e072c179db51a6a26d443c` | completed 2026-09-12T08:05:50Z | failed on SBE attempt 2 at 08:06:46Z |
| Ada Baklava | `a18e8580-9a46-4330-9995-42f70a5a6494` | `4c105c7c2a4a50be9b9ab42d4f64cba6d60ae898deefa7d6ea7fe3f514229748` | completed 2026-09-12T08:07:41Z | failed on SBE attempt 2 at 08:08:38Z |
| Baskerville Biscotti | `563d3f52-3eb5-4588-9383-527391ed26ab` | `849bf454e3506e145367e0f89fdadb7106c537b3f45c1f197c1bf01334c97e13` | completed 2026-09-12T08:09:31Z | failed on SBE attempt 2 at 08:10:28Z |

For all three, the first-cycle SBE trace says:

- `execution_branch=initial_wave`
- `execution_capacity_disposition=continue_local_cycle`
- `outcome=quiescent`
- checkpoint generation 2 accepted
- `local_continuation_required=true`, `provider_local_dependency_count=0`
- job deferred with `reason_code=native.quiescent`

The second SBE attempt then raised the same non-retryable provider-lifecycle
contract error.  Database custody after terminalization shows zero active
lease/allocation and six paid actions per run.  The SBE worker is suspended;
do not resume it.

## Exported SBE worker logs

An unfiltered bounded Render export is available locally at:

`C:\tmp\sbe-worker-20260912-three-pup-provider-lifecycle-failure-logs.jsonl`

Export window: `2026-09-12T07:12:00Z` through `2026-09-12T08:12:30Z`.
Size: 1,518,278 bytes.

Use the per-run IDs above to filter locally.  This log is non-authoritative
trace evidence; PostgreSQL remains authoritative for custody/state.

## Immutable SBE checkpoint coordinate packets

Authorization is limited to exactly one conditional HEAD and one bounded GET
of each named checkpoint object below, after verifying the supplied archive
and inventory SHA-256 values.  The logical restore roots are fixed.  No R2
listing, alternate-object discovery, write, provider access, resume,
reconciliation, recovery, or workspace mutation is authorized.

### Aldine Eclair

- SBE job: `8578dc44-1de9-4269-bd57-86e0425d6ef2`
- checkpoint ID/generation/state: `ef5a92b0-8319-4a43-aafb-8bbc46b37d8e` / `2` / `active`
- object key: `v1/checkpoint/ebcd329c2bb844448fb7654bbdb006c3`
- storage object ID: `ebcd329c-2bb8-4444-8fb7-654bbdb006c3`
- archive SHA-256: `d5c5a62de6cae3495b2569fc9d0b26533d72d9f18a7a5a1f16adfc4627e462cb`
- inventory SHA-256: `5d363dc9d4a776989353bb35e33315a33c75e725230b6b1e5d5b1c07e9d7496a`
- size: `1,751,296` bytes
- restore root: `/work/runs/fc0a6140-6b6f-4c08-b323-66864ce74857/sbe`

### Ada Baklava

- SBE job: `2a41e5ab-801d-4f5d-bee5-654e6ad99ec2`
- checkpoint ID/generation/state: `809faefa-a1de-4f7e-9bee-f52779dea035` / `2` / `active`
- object key: `v1/checkpoint/e56d2d9a729d4478aac7e581eff19078`
- storage object ID: `e56d2d9a-729d-4478-aac7-e581eff19078`
- archive SHA-256: `27d1eaef7e4d546dab5de3a8d25f5af873f657e484ad3a482022f357c28a50ec`
- inventory SHA-256: `54d2d75e12534b92e5d3df3d1ca2b0da25d59d44f5fda5b6c53bb46c67ca6924`
- size: `1,750,304` bytes
- restore root: `/work/runs/a18e8580-9a46-4330-9995-42f70a5a6494/sbe`

### Baskerville Biscotti

- SBE job: `c7c204bf-2be1-485f-a50c-7d6818096244`
- checkpoint ID/generation/state: `96d41835-0d06-4cc4-ac0b-926fd24b246e` / `2` / `active`
- object key: `v1/checkpoint/0c72ac8c7398494898680df42ff0ddc0`
- storage object ID: `0c72ac8c-7398-4948-9868-0df42ff0ddc0`
- archive SHA-256: `6a4cdeb8abb9e561ece09f4f88dcebe1e158794b5064ac637e66eae13faa569c`
- inventory SHA-256: `0f3ae7f1d412a8a84b3a2c055d1d0eaa8cb5ee89d407b819cb38123129679d5f`
- size: `1,751,938` bytes
- restore root: `/work/runs/563d3f52-3eb5-4588-9383-527391ed26ab/sbe`

## Suggested initial slices

1. Build frozen timelines from the exported trace and the three checkpoint
   packets; distinguish native observations from API-owned facts.
2. Perform only the authorized exact-object inspection.  Locate the first
   post-initial-wave inspection/reconciliation payload and compare its envelope
   identity, action disposition, and provider-custody fields against the
   installed SBE public contract.
3. Map the incompatible envelope to source and release history.  Determine
   whether it is a native emission defect, an API consumer expectation defect,
   or a release-pair skew.  Do not propose live repair until the boundary is
   established.

## Boundaries

- No live-provider calls, new spend, retry, resume, reconciliation, repair, or
  run/workspace mutation.
- Do not treat any source as permission to alter QA.
- Preserve the cohort’s known cost ceiling and the frozen evidence state.
