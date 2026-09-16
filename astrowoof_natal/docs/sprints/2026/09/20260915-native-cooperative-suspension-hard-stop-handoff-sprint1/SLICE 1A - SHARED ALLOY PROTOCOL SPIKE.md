# Slice 1A — Shared Alloy protocol spike

## Result

The bounded model is useful and ready for renewed Voof-paws B2. Five complete protocol
worlds are satisfiable, all twelve full-contract assertions have no
counterexample in scope, and nine deliberately weakened rules each produce a
bad-world witness. No schema, reader, coordinator, process-control, provider,
R2, API, or release work occurred.

## Exact evidence

- Analyzer: Alloy Analyzer CLI `6.2.0`
- Official `org.alloytools.alloy.dist.jar` SHA-256:
  `6b8c1cb5bc93bedfc7c61435c4e1ab6e688a242dc702a394628d9a9801edb78d`
- Solver: CLI-default `sat4j`
- Model: `tools/native_cooperative_suspension_v1.als`
- Model SHA-256:
  `f8c0a9afc7c258541d7d30b8596f6f73415c05c08074ba7ce003119f069d4064`
- Stable result summary: `alloy-protocol-spike-receipt.v1.json`
- Rule/fixture traceability: `ALLOY RULE MAPPING.md`
- Private raw analyzer receipt:
  `.tmp-alloy-native-cooperative-suspension-slice1a/receipt.json`

Commands were enumerated with `alloy.exe commands` and executed together with:

```text
alloy.exe exec -f -c * -t json -o <private-output> <model>
```

## Inhabited scenarios

All five returned `SAT`:

1. two isolated runs with suspension, ordinary-result, resolution-successor,
   exit, and worker-execution-release evidence;
2. a valid first request followed by a distinct same-invocation request with a
   different key, producing a typed conflict refusal without changing the first
   result;
3. force-fence checkpoint C1 followed by exact contiguous safe-point C2; and
4. an ordinary result committed before suspension observation dominating the
   resolution; and
5. the narrower required chronology where that ordinary result commits after
   the fence but before native request observation and still suppresses every
   suspension artifact.

The satisfiable scenarios prevent the twelve `UNSAT` checks from being mistaken
for proofs over an impossible full-contract world.

## Full-contract checks

All twelve checks returned `UNSAT`, meaning no counterexample was found in the
finite scope: irreversible fence, stale/mismatched refusal, contiguous
non-branching resolution, worker-only release after exit, no partial-evidence
settlement, ordinary-result precedence, replay behavior, cross-run isolation,
one canonical result per request, and exact one-to-one same-invocation
receipt/command-result transport binding, plus strict capability-before-launch-
before-fence-before-request chronology and refusal of substituted capability
joins.

Every command used an overall scope of eight with exactly eight ordered moments.
The inhabited scenarios additionally pin one or two runs/invocations and exact
small populations of requests, results, checkpoints, exits, and resolutions.

## Counterexamples and contract corrections

The spike earned three concrete contract tightenings:

1. **One request, one semantic result.** The first inhabited world allowed the
   same request to acquire both `refused` and `suspended` results. Gate B now
   says a request has at most one canonical semantic result and exact replay
   returns that same result/receipt identity.
2. **Observation-time precedence.** Ordinary-result precedence must compare
   against SBE's recorded native safe-point `observed_at`, not API's earlier
   force-fence admission. This preserves an ordinary result committed in the
   legitimate fence-to-observation interval.
3. **A chain cannot fork.** Merely immutable predecessor links permit two
   competing direct successors. Gate B now explicitly requires an acyclic,
   non-branching, same-fence resolution history.

The model also made the already intended same-run checkpoint-lineage join
explicit. Seven weakened predicates demonstrate concrete bad worlds for forked
resolution, exit-as-total-settlement, stale-request suspension, lost ordinary
precedence, conflicting outcomes for one request, duplicate receipts, and
cross-invocation command-result binding.

## Gate B2 review corrections

API's first B2 review found two remaining relational gaps. Both are now closed:

- conflict is invocation-wide, so any distinct later request refuses even when
  its idempotency key changes; the valid conflict world keeps the first
  suspended result intact and refuses only the later request; and
- an ordinary result committed before the recorded safe-point observation now
  suppresses suspension-result publication itself. The valid precedence world
  contains an observation and ordinary resolution but exactly zero suspension
  results, receipts, or suspension command-result envelopes.

Compact `SuspensionReceipt` and `SuspensionCommandResult` relations now require
exactly one same-invocation receipt and transport binding per result. The full
campaign was rerun after these changes.

## Limits and decision

## Slice 4A launch-order correction

API's real adapter work exposed the abstraction hole that the original spike
explicitly left outside its process model: it had no launch event, so it could
not distinguish a harmless pre-launch supervision capability from a later
operator-admitted force fence. The canonical model now includes distinct
`SupervisionCapability`, `Invocation.launchedAt`, `ForceFence`, request, and
observation relations.

The corrected campaign proves within scope:

- capability creation strictly precedes the exact invocation launch;
- the exact capability-bound force fence strictly follows launch;
- request publication strictly follows the force fence and joins both;
- substituted or unrelated capability/fence joins can produce only refusal;
- an ordinary result committed after fence admission but before native
  observation suppresses all suspension artifacts; and
- the deliberately weakened pre-launch-fence and capability-substitution
  predicates each produce a concrete SAT bad world.

The first corrected campaign also found a genuine abstract counterexample:
although a mismatched request was forced to `Refused`, a resolution could still
select that refusal across an unrelated fence. The full contract now requires
every selected suspension result to have the exact capability/fence binding.
`CrossRunIsolation` then returned `UNSAT`, while the intended mismatch witness
remained `SAT` only under the weakened rule.

These are bounded relational results, not proof of the eventual Python or API
implementation. The prose remains authoritative and was corrected before any
runtime work. The model should be retained as an optional shared design check;
Slice 2 executable schemas/readers and mutation tests remain the real contract
boundary.

This is Voof-paws B2. No implementation begins until API/SBE/owner review the
exact model, digest, receipt, and prose corrections.
