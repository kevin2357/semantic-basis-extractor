# API review — Slice 0 root identity classification

## Decision

**Approved as the exact live causal classification.** The missing job-bound
join is now supplied. No R2 inspection is needed.

API ran one bounded read-only join pinned to Hokusai SBE job
`3c1dc0cd-3169-4542-8f9b-40305d8dcf3b`, not the earlier run-wide latest-active
checkpoint query. It returned:

| Fact | Value |
| --- | --- |
| API run / native run | `00667fb9-c068-415e-a045-8d4059ac549e` / `06931bef20441d0ce8b76adb01404279d821327b0c2f9ccf04d7d078f2cce05c` |
| exact SBE checkpoint | `c1726aeb-f091-45d4-956a-4f628bb96439`, generation `3`, active |
| exact checkpoint root | `/work/runs/00667fb9-c068-415e-a045-8d4059ac549e/sbe` |
| `SbeAuthoringRun.logical_workspace_path` | `/work/runs/00667fb9-c068-415e-a045-8d4059ac549e/sbe` |
| archive / inventory SHA-256 | `6d6a9ebdb6dfcf6172d41c06107c89fbeadd86efeb068fdd208d78af6b189626` / `2ee271fcbec0b326568975aec2c002cb9a0029d49b2135bb0b1fb999cfd2e204` |

The frozen SBE trace records the copied workspace's durable native root as:

```text
/work/runs/workspace-5d5294a3-6d1d-4fe4-9a36-c0e2b067414a/sbe
```

API's deployed `OperatorRunner._build_relocation_authority()` passes the
database `SbeAuthoringRun.logical_workspace_path` as `original_logical_root`.
That value is the exact API-run root above. It is not canonically equal to the
native root. The public SBE reader is therefore correct to refuse at original
logical-root binding. This is not a release-pair mismatch or SBE reader defect.

The earlier `b7ce…` generation-4 `/work/deterministic-domain` coordinate was
the deterministic-domain job's active checkpoint. It is not relevant to the
operator restore, but exposed a catalog limitation: `checkpoint-coordinate-
packet` currently selects by run rather than by exact job.

## Ownership and next gate

API owns the defective identity source: it writes and later consumes an API-run
logical root that does not equal the native durable workspace-contract root.
SBE should not relax the reader or add an ignore-path escape hatch.

The next work is an API correction proposal that makes the native root an
exact durable API-owned join/fact before any relocated authority is built,
with provider-free regression coverage for the Hokusai shape. Keep all live
execution and any new QA attempt separately gated.
