# Alloy rule mapping

The canonical model is
`tools/native_cooperative_suspension_v1.als`. This map keeps every bounded
assertion tied to Gate B prose and to a future provider-free executable test.

| Alloy check | Gate B rule | Future fixture |
| --- | --- | --- |
| `FenceNeverRestoresOrdinaryAuthority` | force fence is immutable; rejected control never restores ordinary work | fence followed by attempted ordinary-v2 dispatch |
| `StaleOrMismatchedRequestCannotSuspend` | freshness, supported route, identity, and C1/C2 lineage fail closed | stale generation, unsupported route, forked/non-successor checkpoint |
| `ResolutionHistoryIsContiguousAndUnforked` | evidence successors form one append-only, same-fence chain | competing resolution successor publication |
| `ExitReleasesOnlyWorkerExecution` | exact child exit permits worker-execution reclamation only | exit with retained run/provider/spend/workspace/native custody |
| `PartialEvidenceCannotSettleCustody` | fence/result/exit members are individually insufficient | each incomplete evidence subset |
| `PriorOrdinaryResultDominates` | ordinary result committed before native safe-point observation wins | ordinary result after fence but before request observation |
| `ReplayIsInertOrRefused` | exact replay returns the same identity; conflict refuses | same key/same digest and same key/different digest |
| `CrossRunIsolation` | evidence cannot affect a different run | wrong-run result, exit, and resolution joins |
| `OneCanonicalResultPerRequest` | one request cannot acquire a second semantic outcome | duplicate publication with changed outcome and recomputed digests |

The five `*Witness` predicates deliberately omit their corresponding rule and
must remain satisfiable. They are negative-design evidence, not valid protocol
fixtures.

## Scope boundary

Alloy models identifier equality, cardinality, relation ownership, finite
ordering, replay classification, and resource separation. It does not prove
canonical JSON, hash correctness, filesystem atomicity, path/reparse safety,
Python serialization, child-process behavior, provider timing, packaging, or
deployment. Slice 2 and later provider-free fixtures remain mandatory.
