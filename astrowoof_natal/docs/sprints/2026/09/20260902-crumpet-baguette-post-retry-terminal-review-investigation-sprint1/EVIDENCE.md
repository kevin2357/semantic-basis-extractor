# Evidence index

- Exact protected checkpoint coordinates: [BACKGROUND.md](BACKGROUND.md).
- Per-run QA SBE trace windows: [BACKGROUND.md](BACKGROUND.md).
- Combined Render log diagnostic preflight:
  [results/SLICE 0 - TRACE PREFLIGHT.md](results/SLICE%200%20-%20TRACE%20PREFLIGHT.md).
- Frozen protected-access manifests and read receipts:
  [results](results/README.md).
- Paired authoritative checkpoint findings:
  [results/SLICE 0 - PAIRED CHECKPOINT FINDINGS.md](results/SLICE%200%20-%20PAIRED%20CHECKPOINT%20FINDINGS.md).
- Sanitized deterministic comparison receipt:
  [results/SLICE 0 - OFFLINE COMPARISON RECEIPT.json](results/SLICE%200%20-%20OFFLINE%20COMPARISON%20RECEIPT.json).
- Cross-repository causal review and Slice 1 approval:
  [API VOOF-PAWS 1 REVIEW.md](API%20VOOF-PAWS%201%20REVIEW.md).

## Current conclusion

Crumpet and Baguette are positive orchestration qualifications through API
closeout and resource release. Their only rejection was the configured native
theme-group coverage/balance policy after the bounded pass-6 attempt budget.
No API/SBE seam correction is indicated by Slice 0.

## Selected release direction

- Theme-group distribution and mirroring findings remain deterministic,
  persisted, and logged, but cease to be pass-rejection authority.
- Malformed theme-group structure and unknown assignments remain hard failures.
- The pass-6 prompt and provider/retry topology remain unchanged.
- Frozen policy/report contract:
  [THEME GROUP ADVISORY POLICY AND REPORT CONTRACT.md](THEME%20GROUP%20ADVISORY%20POLICY%20AND%20REPORT%20CONTRACT.md).
- The separately source-qualified
  [run evolution reporter](../../../08/20260831-run-evolution-matrix-reporter-mini-sprint1/PLAN.md)
  will be packaged and installed-qualified in the same feature release, while
  remaining operationally and semantically independent from pass acceptance.
- Candidate consumer/operator handoff:
  [THEME POLICY AND RUN REPORTER CONSUMER HANDOFF.md](THEME%20POLICY%20AND%20RUN%20REPORTER%20CONSUMER%20HANDOFF.md).

## Source implementation evidence

- `test_semantic_closure`: 95 passed, including real bundled-checker authoring
  and finalization paths.
- `test_sbe_v03` plus `test_run_report`: 60 passed before the second-corpus
  grammar addition; the reporter subsequently passes 12 focused tests.
- Theme-policy and reporter qualification tests: 15 focused tests after the
  second-corpus grammar addition.
- Release smoke runtime: 4 passed, 1 expected environment-dependent skip.
- Source qualification receipts validate with zero provider, network, or native
  workspace access.
- The current 2,149-line Render export parses 1,829/1,829 marked records with no
  malformed or unknown event and renders all four formats deterministically.

## Installed 0.4.39 candidate evidence

- Two fixed-epoch candidate builds are byte-identical: wheel SHA-256
  `06217b35a5cc024123bc3855c087b0f5c13864b06051d9847f90214c2da43fe4`.
- A clean isolated install reports package version `0.4.39`; `pip check` and
  `astrowoof-release-smoke --require-installed` pass.
- Installed theme-policy qualification passes all six closed assertions;
  canonical receipt SHA-256:
  `8572848ce703aeb2ec208bb26fedae868d7e85970bd9a3f5cead440e5cbe1d88`.
- Installed run-reporter qualification passes all five closed assertions;
  canonical receipt SHA-256:
  `8005e4bb9891052419223bdbda2b8cdfdd9158fcee13b150ae1556f280ae3634`.
- The installed reporter validates and parses the real 2,149-line export with
  complete marked-line coverage, zero malformed records, zero unknown events,
  and two native runs. Generated report file SHA-256:
  `5ec69134c8462bc37198735402fed49dcb2dbc7fafa995c82198c2add4dcb1e6`.
- Packaged schemas validate the generated report and both qualification
  receipts. No provider, network, R2, retained-run, or native-workspace access
  occurred.
- The full repository suite was not run. Qualification instead used the full
  95-test semantic-closure module, the affected validation and reporter suites,
  both installed feature qualifications, and installed release smoke.
