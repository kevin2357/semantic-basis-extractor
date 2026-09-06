# API review — plan and Slice 0 logging census

## Decision

Slice 0 is approved as a strong source/transport census. The proposed shared
formatter boundary, preserved `✨🐶` message, non-authoritative stance, and
dual-format reporter migration are the correct architecture. Proceed to Slice
1's record/privacy contract after incorporating the clarifications below.

## Required Slice 1 contract clarifications

1. **Make the API-relay map invocation-specific.** The current API
   `provider_reconcile` subprocess captures stderr and writes each child line
   verbatim to its own stderr. Ordinary resume and v2 dispatch have different
   behavior: with event streaming enabled they inherit stderr; otherwise their
   stderr can be `DEVNULL`. Do not describe an API stderr relay as universally
   available. Slice 5 must qualify each supported worker invocation explicitly
   and prove that a child JSON line arrives unprefixed, unwrapped, unescaped,
   and unsplit at the Render-facing stream. Any route that deliberately
   suppresses stderr must be named as such rather than silently excluded.
2. **Define a closed record shape, not only an illustrative object.** Freeze
   exact required and nullable keys, `record_type=application_log`,
   `schema_version`, RFC 3339 UTC timestamp precision, JSON primitive types,
   and whether `correlation` keys are always present with `null` or may be
   omitted. Keep `api_run_id` distinct and caller-supplied only; never derive
   it from native state, a subject, path, or message.
3. **Bound payload with an event vocabulary.** Add an explicit event/decision
   name and allow only documented scalar identifiers, enums, counts, timestamps,
   and digests for that event. A generic unconstrained `payload` object would
   recreate the existing privacy/correlation problem inside JSON.
4. **Tighten exception policy.** A raw `exc_info`, raw traceback, or arbitrary
   exception message can contain paths or protected values. Emit only the
   existing sanitized/bounded exception representation by default (type,
   classified code/fingerprint, one-line sanitized message). If a traceback is
   retained, it needs an explicit sanitizer, byte limit, newline escaping, and
   dedicated sentinel tests. Logging failure remains isolated from execution.
5. **Keep existing message sanitization as a hard requirement.** JSON encoding
   protects framing, not confidentiality. The 169 existing message call sites
   still need the current sensitive-content filtering, plus privacy sentinel
   tests over raw stderr, reporter output, fixtures, and API's bounded stderr
   tail.
6. **State scope accurately.** The acceptance criterion should cover ordinary
   SBE application records emitted through SBE's configured handler—not foreign
   host/root handlers or arbitrary embedding applications. Stdout, execution
   event JSONL, command results, and sealed artifacts remain untouched.

## API compatibility position

The raw reconciliation relay is compatible with one-object-per-line SBE JSON;
it performs `sys.stderr.write(line)`, not an API logging wrapper. It remains
diagnostic-only. The API needs no authority interpretation change for this
format, but the Slice 5 route matrix above is a real cross-repository gate,
not a cosmetic test.

With those points frozen, the proposed reporter auto-detection rule is sound:
accept a valid, recognized SBE application-log JSON envelope first; otherwise
fall back to the historical pipe parser. JSON `message` prose must never
override native JSON correlation fields.
