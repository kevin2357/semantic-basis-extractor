# Slice 0 — Exact Terminal and Observer Timelines

## Decision

Slice 0 is complete. Both runs prove the same handoff shape: SBE published one
exact accepted-delivery result and receipt; API's first terminal publication
attempt entered its bounded retry; the retry retained that exact result ID;
and the observer was invoked for it. The observer then returned a local
`capture_or_preflight` failure before any HTTP outcome existed.

## Garamond

| Boundary | Exact evidence |
| --- | --- |
| API run | `abd73e79-f102-4f91-8fda-fd3a56268d58` |
| API job | `47fda7a5-9e43-4f42-b436-125ba9f01bf4` |
| Native run | `3b9d7bedd799e2a7118d2c0cddde483d2fc03a0fa3109e60a36d94f3763f1afe` |
| Delivery invocation | `ninv_282f6a5d9b754eeaba685f1a` |
| Delivery result | `nres_8a0f803d144b9430fe945e6c` |
| Delivery receipt | `nreceipt_bc0a2a6938486fa73bc126f4` |
| Terminal command emitted | `2026-09-14T19:05:08.623Z` |
| Initial API attempt | `ffa98c3e-7501-44d7-82ed-7f05b7824fa3` (publication retry selected) |
| Retry API attempt | `2f6742e3-94ce-4a28-b5a3-7bfc7a59eb37` (`delivery_validation=accepted`) |
| Observer completion | `2026-09-14T19:06:09.708Z` |
| Observer result ID | `nres_8a0f803d144b9430fe945e6c` |
| Observer outcome | `unavailable / capture_or_preflight / delivered=false / artifacts=0` |

## Quill

| Boundary | Exact evidence |
| --- | --- |
| API run | `02744933-4b93-4390-8696-4993aee87375` |
| API job | `a9be5e83-585a-44c7-81c4-95f934030aca` |
| Native run | `de6a6649510df3fae4bf850be06db93bc1accf66f305e9a587fe939b454b6ae8` |
| Delivery invocation | `ninv_79ff79fcaf4a4994b2b178aa` |
| Delivery result | `nres_52b2b0fb130ed0fdca2dcbeb` |
| Delivery receipt | `nreceipt_fd7df83ce6c7bfbc9425685e` |
| Terminal command emitted | `2026-09-14T19:09:13.924Z` |
| Initial API attempt | `5e5d95b3-58c7-4c43-ab98-20a2c421c19a` (publication retry selected) |
| Retry API attempt | `8a952ba0-1704-4b53-bea9-c3b5cbb9cb15` (`delivery_validation=accepted`) |
| Observer completion | `2026-09-14T19:10:15.699Z` |
| Observer result ID | `nres_52b2b0fb130ed0fdca2dcbeb` |
| Observer outcome | `unavailable / capture_or_preflight / delivered=false / artifacts=0` |

## Classification

For each pup, the observer result ID is exactly equal to SBE's delivery result
ID. The paired evidence excludes missing observer invocation, disabled
configuration, identity loss across terminal retry, HTTP non-2xx, timeout,
connection failure, and Better Stack query behavior as the first failure.
Successful reading publication, terminal custody, cleanup, and spend remain
authoritative and unchanged.
