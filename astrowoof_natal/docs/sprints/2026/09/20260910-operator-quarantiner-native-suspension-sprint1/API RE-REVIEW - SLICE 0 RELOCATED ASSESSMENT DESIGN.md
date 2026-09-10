# API re-review — Slice 0 relocated assessment design

## Result

**Approved.** The revised Slice 0 has incorporated the API freeze points
correctly and is sufficiently closed to begin the additive implementation.

In particular, the revised design now explicitly fixes:

- canonical normalized root-string digesting rather than raw host path spelling;
- UTC RFC 3339 time syntax, before-and-after freshness checks, and frozen
  `assessed_at` semantics for deterministic qualification;
- canonical digest coverage for both the relocation authority and wrapper;
- API-owned immutable request/replay handling;
- exact-only terminal result selection with no discovery fallback;
- the distinction between a valid nested v1 prohibited/unsupported posture and
  a malformed/contradictory/expired evidence refusal; and
- the real API restore → installed SBE reader → API wrapper-validation gate.

The `actual root != authoritative logical root` condition remains important:
the dedicated relocated reader must refuse an ordinary-path input rather than
becoming a permissive alternate reader. Equally, relocation authority must
remain unrecognized by every executable or mutating command.

No new API production contract issue is identified. API implementation can
begin once SBE supplies the frozen public schemas and installed reader surface;
the eventual cross-package gate should exercise the exact API-owned archive
and replay boundary, not a synthetic replacement.
