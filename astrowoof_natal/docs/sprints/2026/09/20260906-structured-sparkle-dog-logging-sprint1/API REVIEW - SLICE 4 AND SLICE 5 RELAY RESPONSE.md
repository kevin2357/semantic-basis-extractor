# API Review — Slice 4 and Slice 5 Relay Response

## Slice 4 verdict

Approved. The reporter's parsing precedence, malformed/foreign JSON
accounting, producer-time/source-line ordering, and visible duplicate handling
are appropriate for a diagnostic tool. In particular, retaining duplicate
observations rather than silently deduplicating them is the correct stance:
the reporter must not manufacture authority from a relay observation.

The slice preserves the important boundary: validated native v1 fields are
consumed directly and JSON `message` prose neither fills correlations nor
overrides payload/decision fields. Historical pipe inputs remain readable.

## Slice 5 API request

Accepted. This requires a narrow API companion test/qualification mini-sprint,
because the real subprocess construction and relay semantics live in the API
repository. It is not evidence of an API runtime semantic defect and should
not change lifecycle, provider, custody, stdout authority, or deployed
configuration behavior.

The companion will cover the requested route matrix:

1. Reconciliation receives and relays one valid SBE v1 record byte-for-byte on
   stderr, while the reconciliation command-result JSON remains private to the
   API parser.
2. Ordinary resume proves enabled event streaming uses inherited stderr and
   leaves captured command-result stdout separate; disabled streaming proves
   both streams are intentionally suppressed with `DEVNULL`.
3. The same enabled/disabled transport assertions apply to constrained v2
   dispatch, with typed stdout/event parsing still independent of application
   stderr.
4. Fixtures will prove application-log records cannot be parsed as a command
   result or execution-event envelope.
5. The privacy sentinel test will prove SBE-sanitized output reaches neither
   raw relayed stderr, the bounded API stderr tail, nor a parsed diagnostic
   artifact. API is not being represented as a general sanitizer.

The current request accurately describes the present route behavior. The
qualification will name each tested route `verbatim`, `inherited`, or
`intentionally_suppressed`, and will disclose any deployed configuration
variant rather than assuming the test default is universal.

No live provider work, retained-QA mutation, deployment, or authority change
is authorized by this review.

API review: 2026-09-06
