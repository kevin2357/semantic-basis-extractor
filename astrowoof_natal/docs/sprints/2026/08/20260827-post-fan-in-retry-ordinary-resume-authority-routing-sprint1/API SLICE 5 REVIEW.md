# API Slice 5 Review — Candidate 0.4.27 Installed Qualification

Date: 2026-08-27  
Disposition: **approved as the exact candidate for the API joined campaign; hold
publication until that campaign passes**

## Candidate verification

The candidate lineage and packaging evidence are coherent:

- source candidate: `e1a22ab`;
- version: `0.4.27`;
- deterministic A/B wheel SHA-256:
  `ae8da7a7ce64cd83e1a4444fb8a77587eafb1c1f5a7ff1cc3ac615dfb51e611a`;
- exact dependency: `semantic-projection-core==0.11.1`; and
- packaged surface: `py.typed`, the post-fan-in fixture, receipt schema, and
  `astrowoof-post-fan-in-retry-qa` entry point.

I independently executed the public runner from the isolated installed
`site-packages` tree, outside the checkout. It imported from the installed
candidate, produced the expected `detached_provider_pending` endpoint, and two
invocations returned equal receipts, phase evidence, and endpoint evidence.

The recorded receipt-file digest
`0db488713ad4711f52431d0a65187d6103f7784e41cd9a2c1d192c5af7eee074` is
consistent with the two installed output files. (It is the SHA-256 of the rendered
receipt bytes, distinct from the receipt's internal `receipt_sha256` field.)

## Release gate

This qualifies 0.4.27 as the **only** candidate API should consume for the joined
Sprint 54 campaign. It does not yet approve tag/publication or QA deployment.

Before Slice 6/release:

1. API must validate the candidate fixture/receipt through its real translation,
   persistence, scheduler, lease, and one-slot capacity paths.
2. The joined test must preserve provider/spend custody while capacity is released,
   show the eligible peer progresses, and reject stale replay without duplicate
   dispatch/publication.
3. API-owned terminal/delivery assertions belong in that joined campaign; the SBE
   fixture correctly stops at provider-pending custody.

No provider work, retained-QA recovery, deployment, or new spend is authorized by
this review.
