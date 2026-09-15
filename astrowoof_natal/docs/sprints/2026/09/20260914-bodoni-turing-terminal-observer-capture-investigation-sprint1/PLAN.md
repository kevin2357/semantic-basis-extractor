# Plan — Bodoni/Turing terminal-observer capture investigation

## Objective

Explain why exact terminal-review authority reached the API observer but local
SBE capture returned `unavailable` before envelope construction, and assign any
correction to the package that owns the defective boundary. Preserve terminal
state, provider custody, retained evidence, and Better Stack state throughout
the investigation.

## Frozen fences

- No provider calls, retries, resumes, reconciliations, or terminal-state changes.
- No Better Stack POST is needed to reproduce local capture behavior.
- No latest-result discovery or substitution for either exact result ID.
- No retained-workspace access until exact coordinates, hashes, and separate
  owner authorization are recorded.
- Reproductions must be read-only, network-disabled, and use disposable output
  outside the restored root.
- Safe diagnostics may retain phase/reason tokens, exception class, counts, and
  digests; they must not retain paths, exception prose, deck text, prompts,
  provider responses, credentials, or request bodies.

## Slice 0 — Freeze complete trace evidence

1. Record hashes, byte counts, line counts, and actual first/last timestamps for
   the eight supplied exports.
2. Treat file 07 as capped: it has exactly 1,000 lines and ends at
   `2026-09-15T00:53:24Z`, before its requested `00:56:35Z` boundary.
3. Obtain smaller unfiltered subdivisions covering the omitted tail, or an
   equivalently complete export whose cap status can be proven. Filters may aid
   navigation but must not replace the unfiltered evidence.
4. Reconstruct both witness timelines by exact API run ID, native run ID, and
   result ID. Distinguish observed absence from export truncation.

Acceptance: Bodoni and Turing each have a hash-pinned, non-capped chronology from
terminal publication through observer return, or the evidence register states
precisely which witness remains incomplete.

## Slice 1 — Map the public SBE capture and exception boundary

1. Verify the source and installed release export:
   `astrowoof_natal_authoring.build_editorial_review_runtime_capture`, its
   signature, implementation identity, and package version.
2. Map exceptions from exact-result reading and
   `collect_editorial_review_runtime_evidence()` separately from packet assembly.
   The collector currently runs before the builder's typed-unsupported catch;
   identify every evidence shape that can therefore escape as `ValueError`,
   `OSError`, `KeyError`, or `TypeError`.
3. Reproduce the API boundary provider-free with controlled exported-function
   outcomes: ordinary capture, typed unsupported, expected exception, and an
   unexpected exception. Prove which cases become `unavailable`, which phase is
   retained, and whether the phase reporter can mask or lose diagnostics.
4. Explain the live signature: `capture entered` followed by wrapper
   `returned/unavailable` proves an observer-caught local exception. The lack
   of `capture failed` must be classified separately as an event-emission or
   evidence-export gap, not as proof that the failure branch did not run.

Acceptance: the public callable and API catch boundary have a source-backed
exception map and a provider-free executable reproduction. No witness contents
are required for this slice.

## Review gate A

Joint SBE/API review decides whether Slice 0–1 already identifies a deterministic
contract defect. If not, review must approve exact coordinate collection before
retained evidence is requested.

## Slice 2 — Exact retained-workspace reproduction (separately gated)

1. Record one immutable coordinate packet per witness: object key, expected
   object metadata/digest, workspace-root identity, exact result ID, and archive
   extraction bounds.
2. After explicit owner authorization, permit at most one conditional HEAD and
   one bounded GET per named object.
3. Extract each archive read-only into an isolated, network-disabled environment.
   Invoke both the package-root exported callable and its implementation callable
   against the same exact root/result pair.
4. Capture only branch, typed status reason, exception class, safe phase token,
   bounded counts, and output digests. Run narrower exact reader/collector joins
   only as needed to identify the first failing boundary.
5. Compare the exact deployed release wheel with current source only after the
   witness result is known; do not silently substitute one for the other.

Acceptance: each witness either returns an exact typed capture/status or has one
first failing native boundary with a safe, reproducible classification.

Status: complete. Both exact-root retained workspaces return the typed
`unsupported / contradictory_native_evidence` status. The live exception does
not reproduce; see `SLICE 2 - EXACT RETAINED WORKSPACE REPRODUCTION.md`.

## Review gate B — Ownership and correction

- SBE owns a fix if the public capture callable leaks an expected native evidence
  condition that its contract should represent as typed `unsupported`, or if its
  installed export differs from the qualified implementation.
- API owns a fix if it loses an otherwise valid SBE result, misclassifies the
  public exception contract, or its phase-event schema/sink discards the only
  bounded failure diagnostic.
- Evidence/export tooling owns a fix if the apparent discrepancy is solely
  truncation or rejected diagnostics.
- No implementation begins until the first failing boundary and owner are
  jointly reviewed.

## Slice 3 — Narrow correction and qualification (conditional)

Implement only the reviewed owner-side correction. Add focused regressions for
both terminal-review witnesses' structural shapes plus negative identity and
incomplete-evidence cases. Add every new test to the repository test manifest,
run provider-free focused and broad qualification, and assess whether the change
alters the Alloy lifecycle model. A capture/error-normalization or observability
change alone is expected to require a documented no-model-change ruling rather
than a model revision.
