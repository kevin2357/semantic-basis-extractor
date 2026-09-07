# R2 access ledger

## Campaign summary

Slice 0 performed no R2 operations. After Voof-paws 1, the approved Slice 1
campaign revalidated three previously downloaded archives locally and performed
the sole remaining bounded read for Madeleine.

| Run | Local evidence | Verification performed in this sprint | New HEAD | New GET |
| --- | --- | --- | ---: | ---: |
| Doughmeat Dunsinane | `.tmp-doughmeat-macaron-r2/doughmeat-generation-11.zip` | bytes `4,971,544`; SHA-256 `942ccb5c010984ece428edbbe9078ba0e4a467770219eb14dfb1734674074154` | 0 | 0 |
| Lady Macaron MacLean | `.tmp-doughmeat-macaron-r2/macaron-generation-11.zip` | bytes `4,766,586`; SHA-256 `7e92e963e331fbf61e81f3cbcbce866741a27e5c5597a19c12af4f28a4eef4e1` | 0 | 0 |
| Frisbee Fandango | `C:\tmp\astrowoof-frisbee-openai-audit-20260906\checkpoint-generation-11.zip` | bytes `5,002,462`; SHA-256 `b9a916e15daf33c6dbc54958a3e6f6d9c4eea37d043ecebcff42ca490cff6de3` | 0 | 0 |
| Marauding Madeleine | `.tmp-editorial-calibration-r2/madeleine-generation-9.zip` | ETag, bytes, media type, protection metadata, archive SHA-256, signed inventory, every member digest, and workspace snapshot | 1 | 1 |

All four archive digests match their immutable coordinates. Slice 1 independently
revalidated all four signed inventories and every extracted member before using
semantic artifacts. Member counts were Madeleine `934`, Doughmeat `949`, Macaron
`945`, and Frisbee `949`; all four workspace snapshots also reproduced exactly.

## Prospective operation budget

The approved campaign budget is exhausted. Madeleine used exactly one conditional
HEAD and one conditional GET totaling `4,686,611` bytes. The campaign performed
zero listings, writes, deletes, provider operations, workspace executions, or
retained-workspace mutations. See `MADELEINE R2 ACCESS RECEIPT.json`.

## Slice 3 successful-delivery control

The separately approved ordinary successful-delivery control consumed exactly
one HEAD and one conditional GET totaling `5,041,051` bytes. It performed zero
listings, writes, deletes, provider operations, workspace executions, recovery,
reconciliation, or retained-workspace mutations. Its separate allowance is now
exhausted. See `SUCCESS CONTROL R2 ACCESS MANIFEST.json` and
`SUCCESS CONTROL R2 ACCESS RECEIPT.json`.
