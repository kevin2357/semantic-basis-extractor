# Slice 2 — authorized acquisition and reproduction checkpoint

## Authority and consumed access

On 2026-09-15 the owner directly authorized exactly one conditional HEAD and
one bounded GET for each coordinate-pinned Bembo and Morris checkpoint. No
listing, alternate discovery, retry, write, delete, provider action, or API
mutation was authorized or performed.

Each HEAD established the current ETag and exact byte size. Its paired GET used
that ETag as `If-Match` and the exact inclusive byte range. Both budgets are now
consumed.

| Witness | HEAD/GET bytes | Archive SHA-256 | ETag SHA-256 |
| --- | ---: | --- | --- |
| Bembo | 4,900,517 | `86942cf64c69ed1493d540265962c2622f2bab8a2dd3d3e5db87513f07a2fd8f` | `0500d24e9b2f2af8af8dce2b83190406a7b7ac912d73c4a94250ae46bb2d586c` |
| Morris | 4,796,908 | `d0f1d47f38ad91712cd5661435da690dd958acfe78408f53e01b841e747197e5` | `b84ca947000f645aa827fe7cd879c6c019eee71bc13bb604ec1a6a2e0557195f` |

## Offline archive verification

Both objects are ZIP checkpoint archives. Safety checks found no duplicate,
absolute, parent-traversal, backslash, or symbolic-link member. The archive
member set, every member byte size, every member SHA-256, and the canonical
inventory digest were verified before extraction.

| Witness | Archive entries | Verified workspace members | Inventory SHA-256 |
| --- | ---: | ---: | --- |
| Bembo | 923 | 922 | `dc911fd935614e6f7e39128c1e6de4d31c46bd490d26c24f6c9f8285ec36a337` |
| Morris | 929 | 928 | `90f6e7205e55b75e4850b92a4b58a44cc8efffe579fcad7558aeac860f2b98ef` |

Verified disposable copies are retained under `C:\tmp`; the R2 objects and
retained workspaces were not modified.

## Exact-root reproduction

After the owner started Docker Desktop, each verified extracted workspace was
mounted read-only at its exact coordinate-pinned original logical root. The
repository/package source was mounted read-only and the disposable containers
used `--network none`, a read-only root filesystem, all capabilities dropped,
`no-new-privileges`, and a bounded temporary filesystem. No workspace or API
state mutation occurred. The local image supplied Python 3.12.14; no image pull
or dependency installation occurred.

Each stage ran in a fresh container because the full snapshot validation takes
longer than the interactive command-capture window. The first combined run was
therefore treated only as a timing control, not evidence of a process failure.
All isolated containers exited zero and were removed after their output was
collected.

| Witness | Exact reader | Eligibility | Evidence collection | Implementation capture | Package export |
| --- | --- | --- | --- | --- | --- |
| Bembo | returned | `delivery` | `delivery` | `delivery` packet | `delivery` packet |
| Morris | returned | `editorial_review` | `unsupported / contradictory_native_evidence` | same typed status | same typed status |

No stage raised an exception. In particular, neither the pre-assembly collector
escape nor the typed-status double-fault from Slice 1 reproduced. Bembo builds
the complete delivery capture. Morris returns a typed contradiction before
packet assembly, exactly as the public contract requires.

## Review Gate B ruling

The retained checkpoints do not support an SBE correction or release:

- the exact 0.4.61 source-equivalent public implementation handles both roots;
- delivery and review take different legitimate retained branches, yet neither
  produces the common live `TypeError`;
- the deployed API revision calls the export with the correct two positional
  arguments; and
- no envelope, HTTP, or provider operation is involved in the reproduction.

The live/retained discrepancy is now API/runtime-owned for further
localization. Likely remaining classes are a transient call-time workspace
member difference not represented by the active generation-8 archive, or a
live interpreter/import/runtime condition that the current safe event cannot
identify. The shared normalized class is still not proof of one expression.

API should retain the exact capture phase plus safe frame/line diagnostics in a
provider-free reproduction or next witness. It should also compare call-time
checkpoint/publication ordering with the archive generation used here. SBE
should not broaden its exception handling or alter packet semantics from these
results.
