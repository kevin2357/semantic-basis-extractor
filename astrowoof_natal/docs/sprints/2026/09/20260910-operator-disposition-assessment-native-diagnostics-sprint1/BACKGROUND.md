# Operator-disposition assessment native diagnostics

## Status

Initial planning on branch `codex/20260910-operator-disposition-assessment-diagnostics`. No implementation or public-contract decision has been made.

## Trigger

The live Baskerville quarantine request `02de1a55-b137-499d-9fb4-c327a7fe3116` was refused by the API operator runner with `disposition_assessment_unavailable`. The durable refusal proves that SBE's public assessment call did not yield an admissible assessment, but the available logs do not identify the failing native phase.

The operator runner invokes `read_operator_disposition_assessment()` in-process from its installed SBE wheel. There is no SBE CLI subprocess for this path and therefore no subprocess stderr stream for API's existing SBE-worker relay to capture.

## Native call path

The public reader currently performs these meaningful phases:

1. resolve the exact run directory;
2. load `run.json`;
3. validate the workspace snapshot;
4. establish the read-only native fence;
5. inspect retry-lineage lifecycle;
6. optionally fall back to lifecycle v0.5 when historical terminal evidence cannot be widened losslessly;
7. normalize lifecycle evidence;
8. resolve terminal evidence;
9. classify native custody and quarantine posture;
10. revalidate the workspace snapshot while fenced; and
11. construct and validate the public assessment.

Today, failure at these boundaries generally reaches API as `TypeError` or `ValueError`; API translates that to its public `SbeOperatorDispositionAssessmentError`. That keeps the admission boundary closed, but collapses native diagnostic precision.

## Primary hypothesis: reuse normal SBE sparkle logging

The first implementation candidate is the existing SBE structured application logger, not a new observation API. SBE already owns the `astrowoof.sbe_worker_log.v1` formatter, closed event catalog, bounded payload validation, safe exception projection, and readable sparkle marker. The assessment reader should use those same facilities if an operator-runner-equivalent host can configure and carry them correctly.

There is one execution-shape difference to prove rather than assume. Normal SBE CLI entrypoints call `configure_logging_from_args()` and install the structured stderr handler. The operator runner imports SBE as a library and calls the reader in-process. SBE deliberately installs only a `NullHandler` on import so library consumers do not receive surprise stderr output. Slice 0 must therefore test whether the actual host process configures a usable handler and, if not, identify the smallest explicit reuse of `configure_logging()` that preserves host ownership and avoids duplicate records.

No callback or new public diagnostic return contract should be introduced unless that direct structured-logging experiment demonstrates a concrete limitation.

## Fallback options, only if ordinary logging is insufficient

### A. Host-configured existing SBE formatter

Have the API operator-runner bootstrap install SBE's existing structured handler for the in-process call. This remains the preferred fallback because it reuses the normal native log schema and event catalog.

### B. Optional observation callback

### A. Optional observation callback

Add an optional keyword-only callback to the public reader. SBE emits bounded native diagnostic records to the callback; API adapts those records into its existing structured execution-event envelope.

Benefits:

- deterministic and directly testable;
- independent of host logging configuration;
- preserves API ownership of its output envelope and correlations; and
- introduces no workspace mutation or provider I/O.

Risks:

- adds a public callable parameter and a small native diagnostic contract;
- callback failures must be strictly non-authoritative and non-propagating; and
- records need a closed vocabulary to avoid accidental leakage.

### C. Typed native exception details only

Introduce a stable SBE assessment exception carrying a bounded phase and reason code. API logs that public diagnostic when assessment fails.

Benefits:

- smallest seam for the immediate failure;
- no host logger dependency; and
- naturally preserves a single fail-closed outcome.

Risks:

- reveals only the terminal failing phase, not fallback selection or successful progress;
- provides little evidence for hangs or partial execution; and
- replacing existing exception shapes may affect consumers unless added compatibly.

## Initial recommendation

First add the needed assessment events to SBE's existing closed sparkle-log vocabulary and prove their capture in an operator-runner-equivalent in-process execution. Prefer a small host bootstrap change, if one is needed, over inventing another diagnostic transport. Reconsider callbacks or typed public diagnostic errors only after recording why the ordinary structured logger cannot satisfy the evidence need.

## Safety fences

- Provider-free and read-only behavior must remain unchanged.
- Diagnostics must not include paths, workspace members, prose contents, credentials, provider payloads, or the full assessment.
- Prefer stable digests, revision numbers, route family, lifecycle schema, custody class, posture, and closed reason codes.
- Callback or logging failure must not change assessment success or failure.
- Do not expose a general tracing hook into arbitrary native state.
- Do not weaken snapshot revalidation, native-fence, exact-identity, or fail-closed semantics.
