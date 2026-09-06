# API Review — Voof-paws 1 structured logging contract

## Decision

Approved. Slices 0–1 establish a sufficiently closed, diagnostic-only v1
application-log contract for formatter implementation.

The important API/SBE boundary distinctions are correctly preserved:

- `astrowoof.sbe_worker_log.v1` is an ordinary stderr application record, not
  a command result or typed execution-event envelope;
- native JSON correlation fields are observational only and cannot authorize a
  transition, provider call, replay, or settlement;
- `api_run_id` is caller-supplied only and stays distinct from native run and
  subject identity;
- one physical JSON object per stderr line is compatible with the existing
  provider-reconciliation relay, which forwards child stderr lines verbatim;
- historical pipe logs remain a parser input, while a valid recognized v1 JSON
  envelope takes precedence without reparsing its message prose; and
- bounded payload/event catalogs plus the sanitizer/exception rules prevent
  JSON from becoming an unrestricted protected-data channel.

## Slice 2–5 implementation guardrails

1. Keep the three API subprocess behaviors distinct in tests and docs. The
   reconciliation reader relays stderr verbatim today. Ordinary resume and v2
   dispatch only inherit stderr in their event-stream configuration; otherwise
   they may deliberately use `DEVNULL`. A successful reconciliation test does
   not prove universal visibility.
2. In the positive reconciliation relay test, assert the exact child line is
   one unprefixed, unwrapped, unescaped JSON object at the API-facing stderr
   stream. In the intentional-suppression tests, assert no accidental stdout or
   execution-event contamination rather than treating invisibility as a
   formatter failure.
3. Preserve the readable `✨🐶` message but never use it as a fallback join key
   when a structured field is null. Null is the honest value for an unavailable
   correlation identity.
4. Keep formatter failure containment non-recursive: a serialization fallback
   must not call the same formatter/handler again, and it must not alter command
   exit status or native work.
5. Add privacy sentinels at the raw stderr and parsed reporter boundaries as
   planned. The API relay does no general redaction of a line it forwards, so
   SBE's handler-level sanitizer is the primary protection at this boundary.

## Scope

This approves formatter/context/parser work only. It does not approve a release,
deployment, provider work, retained-QA mutation, or an API authority-contract
change. API has no required runtime mutation before the Slice 5 relay
qualification results are available.
