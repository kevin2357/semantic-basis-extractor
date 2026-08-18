# AstroWoof Natal Authoring 0.4.5

Status: qualified for publication under proposed immutable annotated tag
`astrowoof-natal-authoring-v0.4.5`.

This patch adds a durable native transition journal and sealed command-result
publication protocol so consumers can ingest terminal SBE truth before interpreting
subprocess exit behavior.

## Added

- append-only, hash-linked native transition journal records for ordinary
  authoring and provider reconciliation;
- immutable command results bound to a bounded journal range and checkpoints;
- content-addressed publication receipts binding result, journal range, complete
  workspace snapshot, checkpoint basis, run/invocation identity, and logical root;
- strict public Python reader `read_native_transition_result(run_dir, result_id)`;
- provider-free `astrowoof-native-transition` CLI with explicit result-ID authority;
- packaged route-neutral consumer matrix spanning delivery, review, provider
  failure, pending custody, ambiguity, replay, conflict, and malformed refusal;
- deterministic orphan projection/publication repair after interrupted persistence;
  and
- non-authoritative redacted `native.result_published` observation events.

CLI `--output` must resolve outside the native run directory. Publication is an
atomic validation protocol, not literal multi-file filesystem atomicity. Partial
publication fails closed unless the exact provenance-bound orphan can be repaired.

Provider operations and provider spend during implementation and qualification:
zero / `$0`.

## Qualification

- complete repository suite: 383 passed, 4 expected skips;
- exact 0.4.5 wheel installed `pip check`, lifecycle smoke, and release smoke passed
  on Windows and Linux CPython 3.11;
- two fixed-epoch release builds were byte-identical;
- wheel SHA-256:
  `9b5f1ce0336c791ec4fde906ccd2e8deeac3abc6bc9eac49e94f2c7ea62e71b4`;
- wheel bytes/entries/resources/cache entries: 770978 / 98 / 55 / 0;
- packaged consumer matrix passed the real API validator, including malformed
  identity refusal;
- exact AGF 0.8.1 and SPC 0.11.0 compatibility remains pinned; and
- artifact source commit:
  `2df6b8f63179fdada9fb5fffc144abb89813655c`.

Tagging and publication are pending completion of the immutable release lock.
