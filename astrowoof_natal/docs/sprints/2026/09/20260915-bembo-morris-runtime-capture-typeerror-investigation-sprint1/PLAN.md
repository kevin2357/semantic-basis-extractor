# Plan — Bembo/Morris runtime-capture TypeError investigation

## Status

Closed at Review Gate B. Exact retained-workspace reproduction did not produce
the live `TypeError`; no SBE semantic correction or release is justified. A
separate SBE diagnostics sprint will instrument the public capture boundary so
a future witness can identify its first safe phase and frame without exposing
native contents.

## Objective

Identify the exact expression and native evidence condition that caused the
installed SBE 0.4.61 runtime-capture callable to raise `TypeError` for one
delivery witness and one terminal-review witness, before API envelope or HTTP
work. Assign and implement nothing until that first failing boundary is proven.

## Frozen fences

- No providers, retries, resumes, reconciliation, queue or lifecycle mutation.
- No Better Stack POST, replay, configuration change, or credential inspection.
- No latest-result discovery or substitution for either exact result ID.
- No retained-workspace access until API supplies hash-pinned coordinates and
  the owner separately authorizes the exact bounded reads.
- Any reproduction is read-only, network-disabled, and uses disposable output
  outside the retained root.
- Diagnostics may retain safe phase/reason tokens, normalized exception class,
  counts, IDs already public in the handoff, and digests. They must exclude
  paths, exception prose, deck text, prompts, provider responses, and secrets.

## Slice 0 — Freeze trace provenance and the TypeError boundary

1. Verify each export's byte count, concatenated-record count, first/last record
   timestamp, and SHA-256; retain empty requested windows explicitly.
2. Reconstruct Bembo and Morris from exact API run, native run, and result IDs.
3. Prove for each witness: exact authority selected, wrapper and capture entered,
   capture failed as `type_error`, call-time workspace-reference digest matched
   SBE's independently logged logical-root digest, wrapper returned unavailable,
   completed outcome retained the same failure class, and no envelope/preflight/
   HTTP/artifact phase occurred.
4. Freeze installed SBE/API release and source provenance. Do not infer an inner
   expression merely from the normalized exception class.

Acceptance: both complete timelines and the common pre-envelope boundary are
hash-pinned; a wrong call-time root string, transport, and missing-event
explanations are excluded by direct evidence.

## Slice 1 — Provider-free TypeError surface map

1. Split the public call into these independently executable boundaries:
   exact result reader, eligibility classification, exact capture source,
   evidence collection, and packet assembly.
2. Enumerate operations before packet assembly's internal `try` that can raise
   `TypeError`, including native result/receipt/snapshot validators, iteration and
   ordering of pass/attempt collections, logical-path input conversion, and
   canonical binding serialization. Also inspect typed-status construction in
   the assembly exception handler: a second exception there can escape while
   masking the assembly error that selected the handler.
3. Exercise existing public fixtures and controlled one-field structural
   mutations through the public callable and narrower helpers. Record only the
   first safe phase and exception class. Do not alter a fixture merely to make it
   resemble a witness without native-schema justification.
4. Compare delivery and review control flow. Treat the same `type_error` token as
   evidence of one class, not proof of one expression: review-only disposition
   handling may fail independently of delivery collection.
5. Determine whether the public contract currently promises typed `unsupported`
   for the candidate condition or legitimately permits an exception. Do not
   normalize exceptions broadly without that ruling.

Acceptance: a source-backed and executable candidate matrix identifies which
boundaries can reproduce an escaping `TypeError`, while preserving exact-reader
and fail-closed semantics.

## Review Gate A

Joint API/SBE review decides whether provider-free evidence proves one defect.
If it does not, API may supply one immutable coordinate packet per witness.
Coordinates alone do not authorize R2 access.

## Slice 2 — Exact retained-workspace reproduction (separately gated)

1. Verify each coordinate packet joins API run, SBE job, native run, exact result
   and receipt, checkpoint generation, object key, archive size/digest,
   inventory digest, and original logical root.
2. After separate explicit owner authorization, permit at most one conditional
   HEAD and one bounded GET per named checkpoint. No listing or retry.
3. Verify archive and every manifest member before use. Mount the extracted
   workspace read-only at its exact original logical root in a network-disabled
   disposable container.
4. Invoke, in order, the exact reader, eligibility helper, evidence collector,
   implementation callable, and package-root export. Retain safe traceback frame
   names/line numbers and exception class, never exception prose.
5. If needed, run only the smallest structural join needed to identify the exact
   offending field/type. Do not publish native contents or modify the copy.

Acceptance: each witness has one exact first failing operation and a safe
classification, or returns a typed result that proves a live/retained runtime
difference requiring API-side follow-up.

## Review Gate B — Ownership

- SBE owns a correction only if valid native evidence reaches a public capture
  operation that applies an invalid type assumption, or an expected unsupported
  condition escapes contrary to the public contract.
- API owns a correction if the exact retained callable succeeds, receives a
  different call-time value than its digest implies, or otherwise changes the
  native call boundary.
- No implementation, version bump, package qualification, release, deployment,
  additional R2 access, or live-run action begins before joint review.

## Slice 3 — Conditional narrow correction

Implement only the reviewed owner-side correction. Add both structural witness
regressions plus negative malformed/incomplete evidence cases, add every new test
to the test manifest, and run focused and broad provider-free qualification.
Record Alloy impact explicitly: a capture data-shape/error-normalization change
is expected to require a no-model-change ruling; any altered native lifecycle or
selection semantics requires a model update and separate review.

Not entered. Review Gate B assigned no SBE correction from the retained
evidence.
