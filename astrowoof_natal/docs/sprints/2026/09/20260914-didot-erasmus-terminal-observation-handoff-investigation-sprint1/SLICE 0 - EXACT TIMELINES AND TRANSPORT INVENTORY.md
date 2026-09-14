# Slice 0 — Exact Timelines and Transport Inventory

## Result

Both SBE command handoffs crossed structured stdout intact. The ordinary cycle
result is a separate envelope and its absent result/receipt fields do not erase
the command envelope already captured by API.

## Didot

| Boundary | Exact evidence |
| --- | --- |
| Native publication | `ninv_4049ced1f74647c3a56aba1e` / `nres_fd73a016721dcf725d6a5449` / `nreceipt_1d4f473bcd54f879e416ed93` |
| SBE transport | native result v0.1 `delivery_complete`, then exact terminal-delivery command v0.1, then ordinary cycle result v0.2 |
| API attempt 1 | attempt `69c788c8-dc8b-4a16-b415-ed6b169d0069`, lease `266f7f44-a1d7-49ce-9f8f-2a3b1ae51f12`; `provider_reconciliation` / `terminal_closed`; publication failed with `terminal.publication.retry` |
| API attempt 2 | attempt `16eb5d5f-9dcf-4200-af25-c35a22b0b00d`, lease `eca2ddbc-de29-46f8-b8e9-2c68618b4639`; `delivery_validation` / `delivery_accepted`; publication succeeded |
| First loss | the retry result carries no `sealed_terminal_result_id`; `_publish_delivery_and_complete()` therefore has no exact observer authority after the successful publication |

The original exact delivery identity is present at the first attempt and absent
from the retry handoff. This is an API retry-lineage problem, not SBE transport
loss.

## Erasmus

| Boundary | Exact evidence |
| --- | --- |
| Native publication | `ninv_2e71a7e0b2ce495cbfcf46f1` / `nres_68c273587d4363fe3d150cb9` / `nreceipt_a549e4b41eaa0ac8fe3f7329` |
| SBE transport | native result v0.2 `review_required`, then exact terminal-review command v0.1, then ordinary cycle result v0.2 |
| API attempt 11 | attempt `1fcc8448-79eb-4fe2-87c9-49e7e9e7eda1`, lease `72727d47-c616-4d43-87c3-acb299bd5ca3`; claimed `16:10:27.610Z`; command-bearing `provider_reconciliation` close; failed non-retryably at `16:11:21.073Z` |
| API attempt 12 | attempt `6bb86b9d-17c0-4f16-b0c9-33de7809f833`, lease `367fa5e9-abd6-4962-81b2-2d469884a649`; newly claimed `16:12:31.320Z`; `sealed_terminal_preflight`; failed non-retryably at `16:12:39.418Z` |
| First uncertainty | current source preserves the command and selects observation on attempt 11, but the export contains neither observer success nor observer failure; attempt 12 lawfully has only generic sealed-result identity and cannot recreate invocation-bound review authority |

Attempt 12 is not a duplicate event: it has a new attempt number, attempt ID,
lease ID, claim, lease acquisition, cycle start, and close. Something outside the
ordinary non-retryable queue close reactivated the same job between attempts.
The SBE-worker-only export does not identify that writer.

## First-loss classification

- Didot: API loses exact delivery observation identity across publication retry.
- Erasmus A: no loss is reproduced in current API transport/projection/worker
  source; deployed execution or telemetry remains the boundary.
- Erasmus B: generic sealed preflight intentionally lacks the prior invocation-
  bound review command. Treating it as equivalent would weaken the contract.

