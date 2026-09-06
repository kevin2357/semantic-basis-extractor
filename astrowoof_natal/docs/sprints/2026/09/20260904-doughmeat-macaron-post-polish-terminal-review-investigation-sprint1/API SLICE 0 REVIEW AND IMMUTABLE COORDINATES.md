# API review — Slice 0 and immutable terminal-evidence coordinates

## Review decision

Approved. Slice 0 correctly distinguishes two-attempt polish exhaustion from a
lifecycle, custody, adoption, or publication failure. The `local_dependencies`
value is a non-executable final-review posture, as the closed inspection itself
shows (`command=none`, `eligible_now=false`). No runtime correction is justified
by the preserved traces alone.

The final substantive question is therefore narrow: whether the surviving
editorial findings are genuine under the current policy. API can supply the
following exact coordinate packet. It authorizes **no** R2 operation yet; it is
only a closed future-HEAD/GET target if the owner separately approves that
inspection.

## Shared archive-member convention

Each named SBE checkpoint below is a hash-pinned archive plus hash-pinned
workspace inventory. The requested evidence is expected at these relative
members, all under the exact logical workspace root stated for that run:

```text
final/<subject>/natal.<subject>.cards.json
final/<subject>/natal.<subject>.validation-report.json
final/<subject>/natal.<subject>.lint-report.json
final/<subject>/polish/attempt-001/validation-report.json
final/<subject>/polish/attempt-001/lint-report.json
final/<subject>/polish/attempt-002/validation-report.json
final/<subject>/polish/attempt-002/lint-report.json
```

These paths are source-defined expected members, not a claim that API has
independently listed or read the archive. The archive SHA-256 and inventory
SHA-256 below are the authoritative immutable binding; a later bounded reader
must verify both before relying on any member.

## Doughmeat Dunsinane

```json
{
  "coordinate_contract": "astrowoof.sbe-terminal-evidence-coordinate.v1",
  "api_run_id": "cfa8f529-4a70-4e4b-a245-15bc03615671",
  "native_run_id": "c24a10322bfdd58d70a50e285dcf6d1b0e7013aa42f21e875d3f493235794294",
  "subject": "dog-78bd4096-9f8a-4ae5-a89d-53f96e113f34",
  "checkpoint": {
    "id": "b026f362-7b34-4fb3-8013-0441f758b3ad",
    "job_id": "fe60fe0a-7f18-44bd-84a0-cc173bb536b5",
    "attempt_id": "8ec0566b-8589-4320-93cb-6203a0642dbe",
    "generation": 11,
    "state": "active",
    "checkpoint_contract": "astrowoof.sbe-workspace-checkpoint.v1",
    "compatibility_identity": "astrowoof.qa.sbe0449-polish-authority-handoff.v1",
    "storage_environment": "qa",
    "storage_namespace": "checkpoint",
    "protection_class": "protected-operator",
    "storage_object_id": "c6c7fb8f-df6f-49b4-8e8c-f46af300e9b7",
    "archive_byte_size": 4971544,
    "archive_sha256": "942ccb5c010984ece428edbbe9078ba0e4a467770219eb14dfb1734674074154",
    "inventory_sha256": "8327c9710a139dd034605bb73a4daffc5eb6970394d0bf272d7470059c4e1a98",
    "provider_version": "5a5d631627a711d0e4c4276a4e595404",
    "logical_restore_path": "/work/runs/cfa8f529-4a70-4e4b-a245-15bc03615671/sbe",
    "native_lifecycle_status": "bounded-review_required"
  },
  "sealed_terminal_result": {
    "result_id": "nres_f58c15ff3f7b047945aae1dc",
    "result_sha256": "f58c15ff3f7b047945aae1dc93b02571a98b803c3629cf9abdae813dafd94757",
    "receipt_id": "nreceipt_4d461fb6f121f3ac3228720c",
    "receipt_sha256": "4d461fb6f121f3ac3228720c1cd037f00c4d58d70337dd7b1e5d6c2185189d60",
    "invocation_id": "ninv_2a7274e44c57421e9cea887d",
    "command_kind": "provider_reconciliation",
    "outcome": "review_required",
    "cause_code": "final_qa_requires_review",
    "post_state_revision": 69,
    "checkpoint_basis_sha256": "4c4b091b848ba8fd0c346deb0118aa9f8356a6a9b883ce8b3667b4a5fd01317e",
    "snapshot_sha256": "d9689a1f865d1cbf4ee7744ec020d5002c83d1643f3cd1bcd6e0e6edca516984",
    "journal_range_sha256": "dfe4a1ed30277bf0747e9104576818237704a71ef1161959de75d1eb16c5dc83",
    "result_logical_workspace_root": "/work/runs/workspace-0aaa113c-1940-48aa-ae0d-30512c573d8e/sbe"
  }
}
```

## Lady Macaron MacLean

```json
{
  "coordinate_contract": "astrowoof.sbe-terminal-evidence-coordinate.v1",
  "api_run_id": "218faa53-d773-4e57-9b29-aa8738196078",
  "native_run_id": "13326ec073ec9b7bf4c214c1db0964f5e59a2b7ba57351fa77645a87b24d4aef",
  "subject": "dog-bd811155-4d62-4ea6-a95e-a91189f784f1",
  "checkpoint": {
    "id": "dd2d45e2-32d9-4638-8249-60cf96ee538b",
    "job_id": "e4b1ae3a-9a13-47da-b916-e02f39fd22f9",
    "attempt_id": "d60a527a-5f17-4aac-bb95-1657accba391",
    "generation": 11,
    "state": "active",
    "checkpoint_contract": "astrowoof.sbe-workspace-checkpoint.v1",
    "compatibility_identity": "astrowoof.qa.sbe0449-polish-authority-handoff.v1",
    "storage_environment": "qa",
    "storage_namespace": "checkpoint",
    "protection_class": "protected-operator",
    "storage_object_id": "e56740ca-aedf-44ca-a83f-2e3003a2f77d",
    "archive_byte_size": 4766586,
    "archive_sha256": "7e92e963e331fbf61e81f3cbcbce866741a27e5c5597a19c12af4f28a4eef4e1",
    "inventory_sha256": "97174b9f51bbe44037d9536090674f7391b5e3d2fbd66cbb6d8ec9e178b5bc40",
    "provider_version": "790890abffe9859255b8528d7ff8dcac",
    "logical_restore_path": "/work/runs/218faa53-d773-4e57-9b29-aa8738196078/sbe",
    "native_lifecycle_status": "bounded-review_required"
  },
  "sealed_terminal_result": {
    "result_id": "nres_3772c1c3d356fb594f91d414",
    "result_sha256": "3772c1c3d356fb594f91d41402de7b95c707b0c1fa67e049b09d9df160044496",
    "receipt_id": "nreceipt_e81a18e0fd408d521b364458",
    "receipt_sha256": "e81a18e0fd408d521b3644584a137df2b5f447b8b399357568928c9bf8fa8aba",
    "invocation_id": "ninv_ce4caf34d2cd425c94ac4c89",
    "command_kind": "provider_reconciliation",
    "outcome": "review_required",
    "cause_code": "final_qa_requires_review",
    "post_state_revision": 69,
    "checkpoint_basis_sha256": "0e96e5a64c3ad38882b762ecc3dc93aa0669ae571c38583d6855501f18439e14",
    "snapshot_sha256": "2bc58f279ee7a5c9bdad778c4f30141b93f8e1ef48b2f1e35d8dad24c9f70388",
    "journal_range_sha256": "bb82177dded47b0e9aefabdb8c4bbed11562b5ba9733d235b8d6026e713d9756",
    "result_logical_workspace_root": "/work/runs/workspace-50e4cc65-7814-4cc3-b717-6788bdf9d4cf/sbe"
  }
}
```

## Explicit boundary

API has not listed or read either archive, and does not currently project
per-file final/polish lint or validation digests. The closed checkpoint archive
and inventory identities above are therefore the strongest truthful binding
available before a separately authorized immutable-object inspection.
