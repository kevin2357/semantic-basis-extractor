# Packaged Runtime Smoke Test

The installed distribution exposes a deterministic, token-free release smoke
test:

```powershell
astrowoof-release-smoke --require-installed
```

Use `--work-dir PATH` to preserve its working files and `--output REPORT.json`
to persist the report. Without `--work-dir`, the command uses and removes a
temporary directory.

## What it proves

The smoke command materializes four projected Bre contexts from package
resources, invokes installed extraction, and writes an initial resumable run.
It then launches a separate installed closure process that:

1. resumes the pre-authoring run;
2. deterministically rejects the first pass once;
3. retries and accepts that pass;
4. authors and accepts all six passes;
5. assembles and validates the 50-card/four-summary deck;
6. creates and integrity-tests the five-file delivery ZIP;
7. recalculates every delivery-manifest hash;
8. verifies input, resource, QA, and delivery provenance;
9. plans cleanup without mutation;
10. performs cleanup; and
11. verifies that operator/public state and final delivery remain.

`--require-installed` rejects a runtime module that did not load from a
`site-packages` directory. For the strongest release proof, run the installed
command from a working directory outside the checkout.

## Boundaries

The smoke provider is deterministic and sends no network requests or tokens.
It proves packaging, contracts, orchestration, retry/resume, deterministic QA,
assembly, integrity, provenance, and cleanup. It does not assess literary
quality or replace the controlled live Ella release-candidate run.
