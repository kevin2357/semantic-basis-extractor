# Slice 1 — Bounded checkpoint findings

Status: complete; native causal/reproduction gate before implementation.

## Access accounting

API authorized exactly three protected checkpoint reads. Each HEAD matched the
frozen ETag/version and byte size before its conditional GET. Each downloaded
archive matched the frozen SHA-256. All archive entries were locally checked for
absolute paths, traversal, and non-file/non-directory members before extraction;
every member then matched its manifest byte size and SHA-256.

| Checkpoint | Archive SHA-256 | Members | Remote operations |
|---|---|---:|---|
| Pastiche generation 17 | `a1627407ad6b9e07c42a409db382a40c75305191b6d9fa860abfda0caa2daba5` | 842 | HEAD 1, GET 1 |
| Puff generation 21 | `e2422a2c6a001e3844f68e86bdc1e98939514f3356bbec1d24db111e8cb9ab03` | 1045 | HEAD 1, GET 1 |
| Puff generation 22 | `10bf1acf9163e2ace26f2d6bf42eb4a42bc2c3708f292c7db1cf44bd3e7a9468` | 1049 | HEAD 1, GET 1 |

Aggregate remote operations: 3 HEAD, 3 GET, 0 list, 0 write, 0 delete.
Workspace executions, mutations, provider calls, and reconciliation calls: 0.

## Pastiche: legitimate hard editorial rejection

The retained acceptance reports resolve the advisory/rejection ambiguity.

| Pass-6 attempt | Status | Hard issue codes | Advisory codes | Hard-affected claims | Advisory-affected claims |
|---|---|---|---|---:|---:|
| 2 | `reject` | `theme_group_assignment` | `theme_group_balance` | 2 | 14 |
| 3 | `reject` | `theme_group_assignment`, `theme_group_assignment` | `theme_group_coverage` | 7 | 19 |

Attempt-2 report SHA-256:
`9feb6c5ca6d6426ad8afe647acedc64c5e644ffdd2b8d5b563f778ffc38f49a5`.

Attempt-3 report SHA-256:
`7ffa83c17c13292cd2018328fee86d9594d698ac8cc03d93e083b331c43ca14d`.

Conclusion: Pastiche did not fail because an advisory was accidentally retained
as a hard gate. Both retries contained invalid theme assignments, which remain
hard failures under the current policy. The advisory logger was truthful but
incomplete: it did not mention the accompanying hard issue codes. Pastiche is a
positive qualification of the softened advisory policy plus the retained hard
assignment-integrity gate, not a runtime seam defect.

An observability improvement may be useful—log the bounded hard-code summary
next to advisory codes—but no policy/runtime correction is supported by this
run.

## Puff: completed polish evidence was not joined into its consumer attempt

Generations 21 and 22 contain the same decisive contradiction:

- Run status `WAITING_FOR_RESPONSE`.
- Polish action `paid_047fd998009e0e133e0a64a1` remains ledger state
  `WAITING`.
- Its exact provider identity is durable:
  `resp_09fee2f3adfd1124006a997b439bd487d08fd9a9a95bc44799`.
- Its provider-reconciliation record says `last_outcome: completed`, with one
  retrieval attempt at `2026-09-03T13:52:00Z`.
- The response artifact is present and byte-identical across both generations
  (SHA-256
  `f5bb474ca19f2c2525dee46e5cf838e60581b735a9613f1ff14a28985f1ba882`).
- The live v2 intent remains `PROVIDER_PENDING` and binds the same action,
  request, grant, provider ID, and inventory.
- The subject's polish attempt 1 remains `SUBMITTED`, `finished_at: null`,
  `provider_metadata: null`, `accepted: false`, with no recorded error.
- The action has no `reported` evidence and no consumption successor.
- Cumulative `consumed_operation_keys` are identical across generations 21 and
  22; the advertised polish operation was not added.

Generation 21 `run.json` SHA-256:
`4cf5bc09c4d775c798657f7702cd8a7916d8c71f96df3d32472c8e3221de0509`.

Generation 22 `run.json` SHA-256:
`9fd08e99efdcf55e91f2b3f4b6122d62c0ad4ce7f98f61619321afd071f3787b`.

The terminal v0.2 result and receipt are present in generation 22 and validate
the trace identity:

- result `nres_dac25445bfa8c6613d0d0ca0`, SHA-256
  `ea287a08b13fd2e7be83960d6e03c0c3e29b7b4b2ebff73292027ac7cfbc28a1`;
- receipt `nreceipt_d38140389b21ae33e151f1fe`, SHA-256
  `3e40184f6f1e5e98687d9a534e61ea66fa1bff01665bc8e3582e3ecdf184e45f`.

## Native source seam

The response reconciliation reducer durably writes completed response evidence.
It then invokes `finalize_subjects()` with a reconciliation-only spend
controller. `polish_subject()` recognizes a resumable attempt only through its
stored `SUBMITTED` record, but it has no equivalent of the initial/creative-pass
completed-evidence adoption join. It calls the provider path again with the
reconciliation-only controller; that controller correctly refuses the
already-provider-bound action as ambiguous. Consequently:

1. provider evidence is safely retained;
2. no duplicate create is authorized;
3. the polish attempt never receives the completed response metadata/output;
4. the v2 intent cannot retire;
5. the local-work operation cannot be consumed; and
6. the semantic-progress fence correctly seals `local_work_progress_contradiction`.

This is a native optional-stage completed-evidence adoption defect. The safety
fences and terminal-review publication behave correctly; they expose and contain
the defect rather than causing it.

The correction should be designed for every ordinary-v2 optional-stage consumer
that can detach and reconcile, not special-cased to Puff or polish. Exact route
coverage is mandatory; bounded/Batch applicability must be characterized before
scope expands.

## Next gate

Proceed with a provider-free production-boundary reproduction of:

`SUBMITTED optional-stage attempt → durable provider identity → completed
reconciliation artifact → adoption into exact attempt → deterministic QA/result
processing → reported action + retired intent + consumed local operation`.

The existing bad path must first be reproduced without patching the adoption
function. Then freeze whether critic/candidate routes share the same missing join
before runtime implementation.
