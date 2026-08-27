# API Slice 4A Re-Review

Status: approved for the joined API campaign with the replacement candidate.

## Correction verified

The previous receipt-join weakness is corrected. Public bundle validation now
reconstructs the canonical provider-free qualification receipt through the shared
artifact constructor with bundle validation disabled, validates that receipt, and
requires exact equality with `qualification_receipt_sha256`. This avoids the
former recursion while making a rehashed arbitrary receipt reference fail.

The requested mutation test is present and precise: it changes only the receipt
reference, recomputes the outer bundle digest, and receives the typed receipt
identity refusal. Independent focused execution passed locally: 10 passed, with
one expected optional `jsonschema` skip.

## Handoff disposition

The installed replacement candidate is suitable for API's joined, provider-free
campaign:

- source commit: `9205235`;
- unpublished version: `0.4.27`;
- wheel SHA-256:
  `db5ff09afce53b063dea1b29d8fcb94af581bcf383f7cab5da1d65cc0d4e48ed`;
- installed receipt SHA-256:
  `982f8e3044c7e20a9324d44c61867af5e1787d2d996289ad7fe57aff19e6f2b9`;
- installed bundle SHA-256:
  `75247d8652698e122c46fc79480bbf5b73fd0671b8cb38cb6aa5671eaab2a8a4`.

API must pin that exact wheel hash (not the superseded pre-4A `0.4.27` build)
and consume the projection through a narrow public-bundle adapter. The bundle is
not a complete generic lifecycle v0.7 inspection document; API must not invent
its intentionally omitted private checkpoint fields. The adapter may persist
and schedule the exposed public semantics only. It must never treat the bundle
as spend authority or as permission to invoke a native command.

No SBE publication/deployment, provider work, spend, or retained-QA recovery is
approved by this review. The next gate is the API/Linux joined campaign against
this exact candidate.

