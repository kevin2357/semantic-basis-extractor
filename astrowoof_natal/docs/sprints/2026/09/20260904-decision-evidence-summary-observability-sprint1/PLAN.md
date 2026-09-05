# Plan — decision-evidence trace summaries

## Status

- Slices 0-6 complete; release published and independently verified.
- Candidate version: `0.4.50` (frozen before release-bound testing).
- Artifact-source commit: `d11bfece886055cb34570ea29cc124214561a529`.
- Artifact-source builds and installed-wheel qualifications: complete.
- Release: `astrowoof-natal-authoring-v0.4.50`, published 2026-09-04 MDT.
- Published wheel SHA-256: `e59df304562f967c8a1ae79f59fa20632088ba697cde338df92960e8bd3525c9`.

## Slice 0 — Production decision-boundary inventory

1. Map the exact writer/consumer call sites for:
   - optional-stage adoption (`creative_retry`, `polish`, `critic`, candidate);
   - deterministic validation/lint/finalization;
   - lifecycle and reconciliation selection;
   - external-authority/dispatch refusal; and
   - terminal result publication.
2. Inventory what validated evidence exists at each boundary and which fields
   have repeatedly required workspace restoration.
3. Classify each candidate field as safe scalar, closed reason code, bounded
   identifier inventory, count/digest only, protected, or unavailable.
4. Identify duplication with current `native_state_summary`,
   `native_decision_summary`, mutation/publication, and command-exit traces.
5. Freeze which boundaries merit a new event and which should reuse/enrich an
   existing event.

Pause for review before freezing the event contract.

## Slice 1 — Closed projection and privacy contract

1. Define exact event names, required fields, null/unknown semantics, canonical
   ordering, inventory caps, overflow counts, and summary digests.
2. Define a stable stage-attempt projection including:
   - stage/attempt/action/provider correlation;
   - `accepted`, `no_change`, `error`, `refused`, or other exact typed outcome;
   - findings before/after where known;
   - bounded reason/error classifications; and
   - report identities/digests where available.
3. Define validation evidence with status and counts by closed code, preserving
   unknown separately from zero.
4. Define publication evidence joining explicit outcome/cause, subject evidence,
   action and custody counts, lifecycle posture, and result/receipt/checkpoint
   identities without inferring terminality from sealing.
5. Prohibit raw prose/payload fields and specify deterministic sanitization for
   exceptional messages that are operationally necessary.

Voof-paws 2: cross-repository review of privacy, semantics, and event volume.

## Slice 2 — Projection helpers and unit qualification

1. Implement pure projection helpers in the existing observability layer.
2. Reuse one sanitizer and bounded-inventory implementation.
3. Add strict unit tests for:
   - accepted, no-change, and error optional-stage outcomes;
   - validation pass/warn/reject/error;
   - absent versus zero evidence;
   - stable ordering/digests and overflow behavior;
   - unknown codes/versions failing closed or remaining explicitly unknown;
   - protected prompt/payload/path/credential sentinels; and
   - logger/event-sink failure isolation.
4. Extend the run reporter parser for the new structured events without making
   them authoritative.

## Slice 3 — Runtime wiring at durable boundaries

1. Emit stage evidence only after the real stage consumer has classified native
   truth.
2. Emit validation evidence after the exact report consumed by the decision is
   durable/validated.
3. Emit publication evidence from the writer/publication boundary and bind it
   to the returned result/receipt identities.
4. Enrich refusal/decision summaries only where needed for exact joins.
5. Cover direct authoring, exact interactive reconciliation, bounded
   reconciliation, and applicable Batch paths; explicitly document unsupported
   or structurally different cells.
6. Prove events neither precede the durable fact they describe nor alter command
   behavior when logging fails.

Voof-paws 3: runtime-placement and semantic-parity review.

## Slice 4 — Investigation replay matrix

Use provider-free fixtures representing recent failure/outcome classes:

1. Doughmeat: two accepted polish attempts, findings reduced but not cleared.
2. Macaron: accepted attempt followed by invalid duplicate sparse field.
3. Completed evidence awaiting fan-in/adoption.
4. Provider pending due and not due.
5. Ambiguous submission after call entry.
6. Pre-provider refusal with `not_attempted` assertion.
7. Terminal review with retained provider custody.
8. Deterministic finalization failure before terminal publication.

For each case, show whether logs alone yield the correct bounded operational
classification. Record which questions still legitimately require public
artifact or checkpoint inspection.

## Slice 5 — Packaged observability qualification and playbook

1. Extend the provider-free observability qualification and packaged schema.
2. Exercise installed-wheel public commands in fresh processes.
3. Validate stable event parsing, protected-sentinel absence, bounded volume,
   sink isolation, and zero provider/network activity.
4. Update the operator trace playbook and run-reporter usage documentation.
5. Publish a before/after investigation table demonstrating the 90% log-first
   target against the fixture matrix.

Voof-paws 4: source/package-contract and operator-handoff review. The owner
waived a separate external review for this observability-only sprint and
authorized autonomous progression unless a substantive issue arose.

## Slice 6 — Regression and release preparation

1. Select focused, broad, or full regression scope according to the release
   playbook after the final runtime diff is known.
2. Bump to a fresh unreleased patch version before release-bound tests/builds.
3. Run diff hygiene, deterministic double-build, installed-wheel qualification,
   dependency verification, and required regression suite.
4. Record exact source/tag identity, wheel SHA-256, test totals, and explicit
   zero-provider/R2/retained-QA activity.
5. Pause for explicit owner approval before immutable tag/publication.

## Release boundary

The sprint may produce an SBE patch because production trace wiring and packaged
qualification resources change. It must not alter lifecycle, authority,
custody, editorial policy, provider behavior, or API disposition contracts.
