# Python Typing Consumer Note

Status: unreleased follow-up after 0.3.0

`astrowoof_natal_authoring` ships inline annotations and exposes lifecycle inspection,
provider-less denial, closeout, and structured-event interfaces as supported Python
consumer APIs. The next release packages a `py.typed` marker so PEP 561-aware
type checkers inspect those inline annotations instead of classifying the installed
distribution as an untyped third-party package.

This marker is not present in the immutable published 0.3.0 wheel. Consumers pinned
to 0.3.0 may retain narrow `# type: ignore[import-untyped]` annotations until they pin
a later release containing the marker.

The marker communicates that inline annotations are available; it does not promise
that every returned JSON document is statically narrowed beyond the published
versioned dictionary/JSON Schema contracts. Future typing improvements may add
public `TypedDict` or protocol definitions without changing native lifecycle
authority.
