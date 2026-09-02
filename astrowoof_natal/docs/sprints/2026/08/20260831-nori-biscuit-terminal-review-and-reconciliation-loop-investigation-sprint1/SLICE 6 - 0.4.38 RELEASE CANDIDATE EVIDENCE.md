# Slice 6 — SBE 0.4.38 release-candidate evidence

## Candidate identity

- Version: `0.4.38`
- Wheel: `astrowoof_natal_authoring-0.4.38-py3-none-any.whl`
- Final committed-source bytes: `1,165,977`
- Final committed-source SHA-256: `8d014cf6e51e3cf9616136b0453c87e042eee615a5cd14dfb0f07f787d9e4a5a`
- Reproducibility: two independent builds from committed source identity
  `4fc70cb` were byte-identical.
- Dependency identity: `semantic-projection-core==0.11.1`.

## Scope proof

The accepted wheels were built from fresh `git archive HEAD` source trees with
only the candidate `pyproject.toml` and Nori-modified `closure.py` overlaid.
This avoids dirty-tree package discovery and stale setuptools metadata.

Explicit wheel-member inspection found no:

- `run_report.py`;
- run-reporter qualification module;
- reporter CLI;
- run-evolution schema; or
- run-report qualification schema.

The separately developed reporter files were restored in the working tree and
remain untracked for their own sprint/commit path.

The pre-commit clean-source candidate was SHA-256 `c50fe0fa...e5feb`. Git
normalized `closure.py` line endings while creating the committed blob, so the
post-commit wheel changed bytes without changing Python semantics. Member-level
comparison isolated the difference to `closure.py` and the derived wheel
`RECORD`. The final release artifact is therefore the reproducible wheel built
from the committed source identity above, not the pre-commit candidate.

## Verification

- Focused source regression: 43 tests passed.
- Installed-wheel Nori/Biscuit production-boundary matrix: 5 tests passed.
- Installed `pip check`: no broken requirements.
- Installed identities: SBE `0.4.38`, SPC `0.11.1`.
- Installed package exposes no reporter export.
- `astrowoof-release-smoke --require-installed`: passed.
- Wheel member inspection: reporter members `[]`.
- Diff hygiene: passed; Git emitted only its LF/CRLF advisory.

## Safety and compatibility

- No provider call, retrieval, create, or spend occurred.
- No R2 operation or retained QA workspace execution/mutation occurred.
- No lifecycle, local-work, native-result, receipt, or authority schema changed.
- Exact-interactive optional-stage progress ordering is the only runtime scope.
- Biscuit remains evidence-insufficient and unchanged.
- API still requires its independent full-result custody-disposition fix.

## Gate

Candidate preparation is complete. Commit/tag/publication requires final API
review and explicit owner approval.
