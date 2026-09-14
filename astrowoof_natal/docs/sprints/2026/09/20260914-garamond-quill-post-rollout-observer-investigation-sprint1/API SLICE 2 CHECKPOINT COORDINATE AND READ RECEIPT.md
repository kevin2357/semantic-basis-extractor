# API Slice 2 Checkpoint Coordinate and Read Receipt

API completed the owner-authorized bounded R2 inspection. No further R2 call
is authorized or required: use only the two disposable local archives below
for SBE's local reproduction.

| Field | Garamond | Quill |
| --- | --- | --- |
| API run | `abd73e79-f102-4f91-8fda-fd3a56268d58` | `02744933-4b93-4390-8696-4993aee87375` |
| Native run | `3b9d7bedd799e2a7118d2c0cddde483d2fc03a0fa3109e60a36d94f3763f1afe` | `de6a6649510df3fae4bf850be06db93bc1accf66f305e9a587fe939b454b6ae8` |
| SBE job | `47fda7a5-9e43-4f42-b436-125ba9f01bf4` | `a9be5e83-585a-44c7-81c4-95f934030aca` |
| Checkpoint / generation | `763d709d-87ae-4216-9500-8f8cdb62a974` / `8` | `8cad7937-02bc-4fba-a42d-dd4f48eb370b` / `9` |
| R2 key | `v1/checkpoint/e9206da619e54e38983bba0969a3fcc9` | `v1/checkpoint/de618883c3904859bf5f9375710f1e68` |
| HEAD ETag | `"010150e9872fe0b1747866e4a49a8c44"` | `"f39ebff28209e6cdca9e80402c7db5d2"` |
| Version ID | none | none |
| Archive bytes / SHA-256 | `4,923,817` / `76b4b43f9619afe7b7ab789c8eff3c4ba8ba4ea65ef8b29d7b8a6a09165a948a` | `4,949,216` / `f6a5535ed2755e28df48bc5c108d0535acb753e9926f8b214c7c3c70e9158a7b` |
| Inventory SHA-256 | `556429fcbcf2b70368236dcb56582b670df612eec0eb69a23cf2f2571cfc3887` | `779954a0018ddb20ec4b2c46efd3830b638f3f186cab14a53307588420f7b9aa` |
| Logical restore root | `/work/runs/abd73e79-f102-4f91-8fda-fd3a56268d58/sbe` | `/work/runs/02744933-4b93-4390-8696-4993aee87375/sbe` |
| Exact result ID | `nres_8a0f803d144b9430fe945e6c` | `nres_52b2b0fb130ed0fdca2dcbeb` |
| Local archive | `C:\tmp\garamond-post-rollout-observer-checkpoint.zip` | `C:\tmp\quill-post-rollout-observer-checkpoint.zip` |

API performed exactly one HEAD followed by one ETag-conditional GET per
object. Both GETs matched the authoritative size and archive SHA-256. No
listing, write, provider action, retry, or lifecycle mutation occurred.
