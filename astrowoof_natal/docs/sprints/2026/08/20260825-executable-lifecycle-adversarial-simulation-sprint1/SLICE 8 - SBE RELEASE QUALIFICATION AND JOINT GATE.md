# Slice 8 — SBE Release Qualification and Joint Gate

Date: 2026-08-27  
Status: joined campaign approved; SBE 0.4.26 published and verified

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

## Final release disposition

The API consumed the exact catalog through its real validators, worker translation,
persistence, lease/capacity, and scheduler paths. Its corrected 15-case receipt binds
the executed historical starvation shape separately from the corrected production
worker path and preserves sealed fixture identities separately from adapter results.
Final API and owner review approved publication. SBE 0.4.26 is now immutable;
consumer deployment/pinning remains separate.

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
