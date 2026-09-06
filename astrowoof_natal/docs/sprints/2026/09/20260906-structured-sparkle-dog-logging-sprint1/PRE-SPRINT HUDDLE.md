# Pre-Sprint Huddle

## Initial assessment

This is worthwhile and should be implemented at the logger boundary, not as a
Better Stack-specific adapter. Render, Better Stack, local captures, and the run
reporter should all receive the same one-line JSON record.

The main architectural caution is that SBE already emits typed execution-event
JSON. Application logs should become structured without masquerading as those
events. A trace may explain what code observed; it cannot authorize a queue,
lifecycle, provider, custody, or terminal transition.

## Recommended first-release posture

- Preserve the `✨🐶` marker inside `message` rather than as a non-JSON prefix.
- Prefer a closed versioned record envelope.
- Carry semantically distinct correlation fields; never use a generic `run_id`
  when API and native identities might differ.
- Add fields explicitly at decision points instead of parsing `key=value` prose.
- Keep JSON on stderr and authoritative result transport unchanged.
- Upgrade the reporter in the same release so historical and new logs can be
  investigated together.
- Coordinate the raw stderr relay with API, but keep API changes outside SBE's
  implementation unless its relay transforms or rejects JSON.

## Principal risk

The dangerous failure would be a superficially structured record whose useful
fields still live only in `message`, or whose generic identifiers conflate API,
native, action, and provider identities. That would change appearance without
fixing correlation. Slice 0's field census and the Slice 1 gate exist to prevent
that outcome.

