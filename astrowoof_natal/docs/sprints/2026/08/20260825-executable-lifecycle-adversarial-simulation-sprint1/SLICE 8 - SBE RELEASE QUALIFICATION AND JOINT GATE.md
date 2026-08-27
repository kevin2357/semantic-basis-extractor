# Slice 8 — SBE Release Qualification and Joint Gate

Date: 2026-08-27  
Status: SBE-local qualification complete; joined API campaign pending

## Completed SBE evidence

- The focused adversarial corpus passed: 44 tests with one expected optional
  `jsonschema` skip in the lean interpreter.
- The broad source suite passed: 799 tests with 39 expected environment/opt-in
  skips.
- Two independent builds at `SOURCE_DATE_EPOCH=1787844361` produced identical
  1,040,753-byte wheels at SHA-256
  `31f0adf1e43d01b45b79a0341c1deee421b54ff522880babbbaa009eee2220bb`.
- The wheel was installed outside the source tree. Two installed invocations of
  the public qualification surface produced byte-identical receipt files at
  SHA-256
  `ae8b988c13723f8447bd1548748320447ac7f63ca4eb020cefae96413133435a`.
- The installed receipt validated three fixtures, seeds 7/19/41, 22 route cells,
  and 32 checks.

All qualification was provider-free. External network calls, real provider creates,
and spend were zero. No retained QA workspace was opened or mutated.

## Why this is not yet a release recommendation

The candidate still reports published version `0.4.25`; it is intentionally not a
release artifact. SBE's public surface changed, so any eventual publication must use
a fresh immutable version.

The Slice 7 catalog is an inventory and integrity fence, not composed-system proof.
Before a version bump, tag, publication, or API adoption recommendation, the API must
consume the exact catalog through its real validators, worker translation,
persistence, lease/capacity, and scheduler paths and emit the joined campaign
receipt. That receipt must include the required three-run bounded-capacity
progress/fairness witness. Final owner and API review remain mandatory after that
evidence exists.

## Seed budgets and incident promotion

- Ordinary CI uses fixed seeds 7, 19, and 41 plus all named deterministic incident
  fixtures.
- A broader bounded seed/depth/time campaign belongs in nightly or explicit release
  qualification; bounds and truncation must be recorded in its receipt.
- A newly discovered incident is first reduced to its smallest provider-free trace,
  assigned an ownership class, and added as a named deterministic fixture or
  qualification component before increasing random campaign breadth.
- A changed public schema, catalog case/assertion, fixture bytes/hash, semantic
  fingerprint, or ownership mapping requires synchronized SBE/API review and pinned
  adoption. Merely increasing non-normative seed budgets does not.
