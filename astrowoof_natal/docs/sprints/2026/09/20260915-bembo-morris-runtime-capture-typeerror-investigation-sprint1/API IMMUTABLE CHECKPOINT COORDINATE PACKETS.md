# API immutable checkpoint coordinate packets

## Authority

The owner authorizes SBE, for this investigation only, to perform **exactly one
conditional HEAD and one bounded GET per named checkpoint object** below.

The reads are solely for the Slice 2 read-only reproduction.  They do not
authorize listing, alternate-object discovery, writes, provider work, resume,
retry, reconciliation, recovery, queue/lifecycle mutation, Better Stack work,
or mutation of an extracted or retained workspace.

PostgreSQL cannot provide an R2 ETag/version.  The authorized conditional HEAD
must obtain and bind that object version/ETag before its paired bounded GET.
Reject a response whose content length or archive digest does not match this
packet.  Use the exact original logical root only in a disposable,
network-disabled, read-only reproduction.

## Bembo Brioche — delivery witness

| Field | Value |
| --- | --- |
| API run ID | `c77f8bfe-6c8b-4612-8dcd-de76d7d5822b` |
| authoring run ID | `21441f00-5734-4422-9719-ab48c04beb26` |
| native run ID | `a1523be35ee0d47fa5e471fc6dc8b4bd6ee5b3d8959ba591b7b720cf4977d3e0` |
| SBE job ID | `1d8d2534-d594-46a8-93d6-8c1889f62223` |
| checkpoint ID | `e36c440a-f43e-45df-b035-098162a05d0e` |
| generation/state | `8` / `active` |
| storage object ID | `5a80e7ed-b78e-482a-8efb-8bb419b3b319` |
| exact R2 key | `v1/checkpoint/5a80e7edb78e482a8efb8bb419b3b319` |
| archive SHA-256 | `86942cf64c69ed1493d540265962c2622f2bab8a2dd3d3e5db87513f07a2fd8f` |
| inventory SHA-256 | `dc911fd935614e6f7e39128c1e6de4d31c46bd490d26c24f6c9f8285ec36a337` |
| archive byte size | `4,900,517` |
| original logical restore root | `/work/runs/workspace-ff479662-ba95-4ba9-998d-e79c4104334f/sbe` |
| exact result ID / SHA-256 | `nres_a83f5a0c2946e06876d7e79c` / `a83f5a0c2946e06876d7e79c6c71b1589b9d5a694c5201e3af709356b7c78f90` |
| receipt ID / SHA-256 | `nreceipt_a783925cf244a37dde5d8360` / `a783925cf244a37dde5d8360157dca4093ddbeab8f9644027ad4cd332cc5dc65` |
| receipt checkpoint-basis SHA-256 | `ef44ac7c3fbc8c58b213e954ab3f0690b8898477399ea43f441e8a1c017bfece` |

## Morris Madeleine — terminal-review witness

| Field | Value |
| --- | --- |
| API run ID | `f679b5af-8dcb-4db5-a79b-72c67fac4f6f` |
| authoring run ID | `bc9857a6-d2eb-45a2-bd39-f02a0893cbb7` |
| native run ID | `b374742b24ec55c5f04dec878e663cdc4bf8d86d4e476542fdde5ff224651220` |
| SBE job ID | `7353a256-f2f5-44bd-baf8-633f6aecbbdd` |
| checkpoint ID | `4f1cb6ef-1955-442a-84e4-eb45c3d9db12` |
| generation/state | `8` / `active` |
| storage object ID | `2aab8393-42c0-4ccc-8609-ea800e46c0ed` |
| exact R2 key | `v1/checkpoint/2aab839342c04ccc8609ea800e46c0ed` |
| archive SHA-256 | `d0f1d47f38ad91712cd5661435da690dd958acfe78408f53e01b841e747197e5` |
| inventory SHA-256 | `90f6e7205e55b75e4850b92a4b58a44cc8efffe579fcad7558aeac860f2b98ef` |
| archive byte size | `4,796,908` |
| original logical restore root | `/work/runs/workspace-1d2cd92a-feda-46ea-ab8a-349d8a50149d/sbe` |
| exact result ID / SHA-256 | `nres_3f628ce39fa7673b7c141a25` / `3f628ce39fa7673b7c141a25ced381bf77535ec6218035f023ab5a51ac3a9c05` |
| receipt ID / SHA-256 | `nreceipt_b4f0d38e2d9442822a962c8a` / `b4f0d38e2d9442822a962c8a2384b90ef29d30515923dcf16706ede45238b1a4` |
| receipt checkpoint-basis SHA-256 | `5f511b9a8f8da745205dfd16c4e40c5bc5acd80d2670c351c300d6b87b5dc1a4` |

## Derivation

API produced these packets with the checked-in bounded
`sbe-checkpoint-coordinate-packet` PostgreSQL diagnostic, one read-only query
per API run.  The diagnostic selects only the exact `sbe-authoring` job's
highest active checkpoint and joins its latest native receipt.
