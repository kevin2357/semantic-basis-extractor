# Slice 2 — Broader Route Adapter Matrix

Status: implemented and focused-qualified

## Outcome

The provider-free adapter now composes three existing production-path qualification
receipts into one strict route matrix rather than recreating their behavior:

- deployed four-route qualification for exact/bounded initial Response and Batch;
- external-authority v2 qualification for exact/bounded ordinary Response stages
  and deliberate ordinary-Batch refusal; and
- post-fan-in v2 qualification for exact/bounded fresh-reader local progress.

The resulting 22 cells cover both routes, initial Response/Batch, post-fan-in local
work, creative retry, polish, qualitative critic, and qualitative candidate. Every
ordinary Batch counterpart is explicitly refused. Each cell binds the exact source
receipt schema and digest plus the source assertion; it is not a free-standing claim.

Denial, terminal closeout, and publication safety remain native-oracle evidence for
Slice 3. They are not falsely represented as provider-transport cells.

## Safety boundary

The composite is qualification-only and declares zero external network calls, real
provider creates, and provider spend. Its defaults invoke the public packaged
qualification functions. Runner injection exists only to make the closed join itself
cheap to mutation-test.

## Focused evidence

- 20 adversarial adapter/trace/matrix tests passed.
- One optional `jsonschema` check skipped in the lean interpreter.
- `git diff --check` passed; the existing Windows line-ending notice is non-failing.
