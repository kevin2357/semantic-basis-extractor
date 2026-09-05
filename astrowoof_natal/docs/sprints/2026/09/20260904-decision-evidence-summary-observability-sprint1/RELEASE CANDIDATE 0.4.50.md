# Release candidate — SBE 0.4.50

## Identity

- Version: `0.4.50`
- Artifact-source commit: `d11bfece886055cb34570ea29cc124214561a529`
- Build epoch: `1788586591`
- Wheel: `astrowoof_natal_authoring-0.4.50-py3-none-any.whl`
- Wheel bytes: `1217628`
- Wheel SHA-256:
  `e59df304562f967c8a1ae79f59fa20632088ba697cde338df92960e8bd3525c9`
- Wheel members: 266
- Forbidden cache/bytecode/test members: 0
- SPC compatibility: `0.11.1`

## Regression evidence

- Candidate version and version-derived fixture were frozen before testing.
- Focused observability/reporter/adoption/publication/version matrix: pass.
- Full repository suite: **1,061 passed, 3 expected skips** in 901.827 seconds.
- No correction was made after the successful full suite.

## Reproducibility

Independent builds in `.release-0.4.50-a` and `.release-0.4.50-b` used the same
source commit and `SOURCE_DATE_EPOCH`; filenames, sizes, member inventories, and
SHA-256 values match.

## Installed qualification

The exact candidate wheel was installed from outside the source package into a
Windows Python 3.11 environment with SPC 0.11.1.

- `pip check`: no broken requirements.
- Import path: installed `site-packages`, not checkout source.
- Generic `astrowoof-release-smoke --require-installed`: pass.
- `astrowoof-trace-observability-qa`: pass, receipt
  `d18e8f5168b0fd324894380f883bea83187992bfa485f64df116bf7c82597ddc`.
- `astrowoof-run-report-qa`: pass, receipt
  `ff3a78561aa6567e29018ba5038652ca313fc123bb5633f5181964f40d5c1c44`.
- `astrowoof-decision-evidence-observability-qa`: pass, receipt
  `d2653ba2aa807baa12b2ba7ee309ff9a656501d5f9ef99efccb8cdd1386abc87`.

## Safety and scope

- Provider create calls: 0.
- Provider retrieval calls: 0.
- External network calls: 0.
- R2 operations: 0.
- Retained QA reads/mutations: 0.
- Lifecycle/provider/editorial behavior changes: none.
- Public transition-authority changes: none.

## Remaining release-lock gate

Commit this record as the release lock, rebuild twice from that exact commit and
its commit epoch, require the same wheel SHA-256, repeat installed public
qualifications, and then pause for explicit owner authorization before creating
the immutable component tag and GitHub release.
