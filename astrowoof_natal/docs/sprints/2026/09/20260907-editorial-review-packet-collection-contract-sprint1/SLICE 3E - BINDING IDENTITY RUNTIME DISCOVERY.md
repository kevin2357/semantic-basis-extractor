# Slice 3E — binding identity runtime discovery

## Decision requested

Replace the proposed editorial-only `binding_id` with the canonical native
`binding_sha256` as the binding identity before the Slice 3 runtime builder is
completed.

## What runtime mapping found

Production native evidence does not mint or persist a separate binding ID.
Across the retained Frisbee workspace and the released native implementations:

- paid-action records retain the complete immutable `binding` document;
- initial-wave and external-authority members retain `binding_sha256`;
- terminal-review action dispositions retain `binding_sha256`; and
- native validators recompute that digest from the complete binding document.

No non-editorial production source or retained JSON evidence uses
`binding_id`. The only occurrences are in the new editorial-review v3 proposal,
its synthetic fixtures, and its ID derivation. Those fixtures currently invent
values such as `bind_<digest-prefix>`. That value is deterministic, but it is
not durable native provenance.

## Why this is a contract issue

The packet must report what the native system proves. Minting a decorative
binding identifier inside the review layer would create a second identity
namespace and make a consumer believe it joined a persisted field that never
existed. The native digest already supplies the required exact identity and can
be recomputed from the retained binding document.

## Proposed coordinated v4 correction

Advance the coordinated decision, packet, projection, transport, and semantic
contract resources together and:

1. remove `binding_id` from the action relation;
2. keep `binding_sha256` required and use it as the canonical binding identity;
3. derive `decision_id` from `binding_sha256`, not a synthesized label;
4. require the runtime builder to recompute the digest from the exact paid-action
   binding and join it to the exact native result/action disposition where that
   disposition is present;
5. retain `paid_action_id`, `request_sha256`, and `provider_response_id` as
   distinct identities rather than treating any as an alias for the binding;
6. update projections and artifacts to carry the digest only; and
7. add rehashed mutations for changed binding bytes/digest, duplicate binding
   digest, wrong result-disposition join, and unchanged decision identity after
   a binding change.

The optional Alloy relation remains conceptually useful, but its `Binding` atom
must be documented as the abstract identity represented concretely by
`binding_sha256`; Alloy does not justify inventing another runtime field.

## Boundary

Runtime collection remains read-only and provider-free. No Better Stack, R2,
API, database, installed-wheel, or release operation is implicated. Work is
paused before changing the coordinated public resources because this is a
consumer-visible schema/identity correction.
