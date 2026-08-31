# Slice 2 — causal matrix and contract freeze

## Status

Proposed contract freeze for Voof-paws 3. No runtime or packaged contract bytes
have changed.

## Causal conclusion

Glimmer crossed a native seam between a provisional editorial finding and
provider custody:

1. final assembly set the subject to `FINAL_QA_WARN`;
2. SBE correctly prepared a polish action and exported ordinary-v2 authority;
3. constrained dispatch authorized and consumed that action;
4. intent persistence called the general run-status reducer;
5. the reducer promoted the provisional warning to outer
   `FINAL_QA_REQUIRES_REVIEW` despite the `SUBMITTING` polish action;
6. the executor did not reject the terminal-shaped post-intent checkpoint;
7. one provider operation was created and its identity became durable; and
8. public lifecycle correctly refused to reinterpret the terminal outer status
   as provider-continuable.

The API refusal was correct. The producer checkpoint was contradictory.

## Precedence contract

The following ordering is normative for exact-interactive ordinary paid work:

1. invalid snapshot, writer ambiguity, provider call-entry ambiguity, and
   contradictory native evidence fail closed;
2. existing durable provider custody selects retrieval/reconciliation only;
3. completed provider evidence requiring adoption selects local fan-in;
4. an authorized/submitting ordinary action remains a nonterminal constrained
   dispatch state and cannot be terminalized from provisional editorial facts;
5. a providerless prepared action selects external authority;
6. other required native local work selects ordinary local continuation; and
7. only after those inventories are empty may final-QA failure/review seal a
   terminal result.

The run-status projection must therefore use `WAITING_FOR_RESPONSE` while a
durable, unresolved ordinary provider identity exists, including polish,
qualitative critic, or qualitative candidate work. A subject-level
`FINAL_QA_WARN` remains preserved as editorial evidence; it does not itself
authorize terminal closeout.

`SUBMITTING`/call-entered evidence remains ambiguity or constrained-dispatch
custody, never `FINAL_QA_REQUIRES_REVIEW`. A merely authorized providerless
action is also nonterminal, but this sprint does not authorize its denial or
retirement.

## Causal matrix

| Native facts | Outer/public disposition | Provider permission | Terminal result |
|---|---|---|---|
| `FINAL_QA_WARN`; no polish action/custody/local publication work | legitimate review terminal | none | required and exact-inventory-bound |
| `FINAL_QA_WARN`; polish `PREPARED` | await external authority | none until a fresh grant | forbidden |
| `FINAL_QA_WARN`; polish authorized/intent committed; call not entered | nonterminal constrained dispatch | only exact fenced invocation | forbidden |
| `FINAL_QA_WARN`; call entered without durable identity | ambiguity review | create forbidden | forbidden |
| `FINAL_QA_WARN`; durable polish identity pending/not due | release until due; reconciliation command named but ineligible | GET only when due | forbidden |
| `FINAL_QA_WARN`; durable polish identity due | provider reconciliation selected | bounded SBE-selected GET only | forbidden |
| completed polish response not yet adopted | ordinary local fan-in | no create | forbidden |
| polish adopted and QA now passes | next supported stage/delivery | per resulting inventory | forbidden until closeout inventory is empty |
| polish adopted and review remains after supported attempts exhausted | legitimate review terminal | none | required and exact-inventory-bound |
| providerless authorized polish at an operator stop | explicit denial/retirement contract required | none | forbidden until that transition is proven |

## Terminal-result authority

A terminal status label is never sufficient terminal authority. Publication of
a terminal result must revalidate under the native writer that its exact action
inventory contains none of:

- unresolved provider identities;
- call-entry ambiguity;
- authorized or consumed create-capable work;
- completed provider evidence awaiting adoption;
- providerless actions awaiting an explicit supported disposition; or
- required local terminal-publication work.

The result, receipt, snapshot, and terminal action-inventory/closure digest must
seal one checkpoint. Absence of a sealed result remains an explicit negative
fact in consumer fixtures.

## Post-intent provider-call fence

After the aggregate grant, selected inventory, authorizations, and intent are
durably checkpointed—but before provider call-entry—the executor must re-read
and validate that exact checkpoint under the writer. It must prove:

- the outer lifecycle is nonterminal;
- the exact intent and ordered action inventory are current;
- every selected action is still `SUBMITTING`, providerless, and joined to the
  same request/grant; and
- no newer snapshot or conflicting custody exists.

Only then may it publish `provider_create_permitted` and release the writer for
slow I/O.

If this post-intent check fails before call-entry, provider I/O disposition is
`not_attempted`; the failed grant invocation is immutable and refused; no
provider identity exists; and any later attempt requires fresh inspection and
fresh API authority. The result must be typed and replay-safe.

The existing phase-aware dispatch-result v3 has a closed refusal vocabulary
that does not truthfully name this condition. Slice 4 should therefore publish
a fresh result/command schema version with the narrow refusal reason
`post_intent_lifecycle_contradiction`, while retaining the existing
`pre_provider_refusal` / `not_attempted` / refused-grant semantics. It must not
mislabel the condition as `checkpoint_changed_before_create` when no external
checkpoint change occurred.

## Public lifecycle compatibility

No lifecycle schema expansion is proposed. Existing v0.5/v0.7/v0.8 fields can
represent the corrected truth:

- provider custody and timing remain native facts;
- due-member selection remains SBE-owned;
- API invokes only the supported run-level reconciliation command;
- terminal remains terminal; and
- API must continue refusing contradictory terminal-plus-custody bytes.

The semantic correction is to the producer's status/custody composition, not a
request that API reinterpret old terminal documents.

## Retained Glimmer compatibility

Glimmer's durable response ID remains retrieval-only evidence. This sprint does
not authorize accessing it, resuming the run, replacing it, denying it, or
rewriting generation 18. A future supported recovery decision must use released
code and separate owner/API authority after the patch is qualified.

## Slice 3 proof obligations

The provider-free reproduction must exercise the public production path and
prove both sides of the distinction:

1. final-QA warning with no active custody seals a real review terminal; and
2. the same warning with active polish custody stays nonterminal through
   dispatch, reconciliation, and adoption.

It must additionally inject a deliberately contradictory post-intent checkpoint
and prove typed pre-provider refusal, zero POSTs, immutable refusal history,
fresh-authority-only re-entry, and no terminal result publication.
