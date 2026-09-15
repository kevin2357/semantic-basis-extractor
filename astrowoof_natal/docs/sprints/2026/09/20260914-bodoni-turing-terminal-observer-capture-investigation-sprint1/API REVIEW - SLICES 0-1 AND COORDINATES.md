# API review — Slices 0–1 and exact coordinates

## Review

Approved. Slice 0 now establishes the complete, uncapped witness chronology.
Slice 1 correctly separates two issues:

1. the still-unclassified local capture refusal inside the installed public SBE
   callable; and
2. the independently proven API observability defect: CamelCase Python exception
   names violate the lowercase reason-token field and cause the best-effort phase
   emitter to silently discard the `capture failed` event.

The latter does not identify the original capture cause. Exact retained-workspace
reproduction is the narrowest appropriate next step.

## API-authoritative coordinate packets

### Bodoni Brioche

| Field | Value |
| --- | --- |
| API run | `e64ab155-432a-433a-b3f8-ebfa737db0d7` |
| Native run | `af93c196e0ef923ff617086004d2de0cec503eafb651cd9774068db8510a5ba7` |
| SBE job | `fe3bcb4c-4654-4ac1-b117-fba597ef018f` |
| Exact terminal result | `nres_2b91727d5ba5b97bf07110ff` |
| Result SHA-256 | `2b91727d5ba5b97bf07110ff02df50a8f366b608baf98e4d69e5eefe17e83e04` |
| Receipt ID / SHA-256 | `nreceipt_d6c412aecb13c29ae826852e` / `d6c412aecb13c29ae826852e70f92ece51f3873711c927a70a72298e318065d0` |
| Checkpoint ID / generation | `e3068feb-ad5b-4bdd-a11e-8d76c8c23864` / `9` |
| R2 key | `v1/checkpoint/f2ab0539f8e84919af3ca3b24aa9be30` |
| Storage object ID | `f2ab0539-f8e8-4919-af3c-a3b24aa9be30` |
| Archive SHA-256 / bytes | `e4274217c5821d553f4f1fe321b87f2b4b7ac3a2e07ce2aa8d17f0a9fbaefae5` / `5,252,898` |
| Inventory SHA-256 | `0dcd2d09fcdd036acc88e1403905ad6cef77d28a2bebe1f5a202b1901c76ebf2` |
| Logical restore root | `/work/runs/workspace-59cceb2b-340b-4d0f-8e19-8f2832ea9000/sbe` |

### Turing Tart

| Field | Value |
| --- | --- |
| API run | `9cb4d9d8-be9d-4ffb-948c-e47839831f00` |
| Native run | `ddf49bcaf474f3ff5493d8c990541031c8fffce563da24d6faa35fa16ca2e95d` |
| SBE job | `b50e4b72-8f30-429b-a104-23be2ac4cded` |
| Exact terminal result | `nres_433d168be822521a18043c6a` |
| Result SHA-256 | `433d168be822521a18043c6aadd1eef73cdda55a9fc53a543390a97413269b32` |
| Receipt ID / SHA-256 | `nreceipt_5f98d3d232ea2c0c8f77eae7` / `5f98d3d232ea2c0c8f77eae788653a99ce03a106b71e87193b7995c1ef38c518` |
| Checkpoint ID / generation | `bc44cf59-0e8b-442f-910f-836e3953c8f9` / `10` |
| R2 key | `v1/checkpoint/0a37d964e06741c394a11a3ec26d877d` |
| Storage object ID | `0a37d964-e067-41c3-94a1-1a3ec26d877d` |
| Archive SHA-256 / bytes | `0eb6a327433ba5fcd56973aa8d152086a4ea839358bac7c55a95feab7f6835ea` / `5,141,410` |
| Inventory SHA-256 | `7f906d7be89da017c24e85b9a128fc19044f0f8581fb0834406a90baf45a8bc3` |
| Logical restore root | `/work/runs/workspace-8f5c86db-27a9-4543-90e2-1592c6d7ef88/sbe` |

PostgreSQL does not retain R2 ETags/version IDs; a conditional object HEAD is
needed to obtain those immutable storage metadata values.

## Read authority

This review authorizes the coordinate handoff only. It does **not** authorize an
R2 HEAD or GET. Before object access, SBE must request the plan's exact bounded
authorization (one conditional HEAD and one bounded GET per named object).
