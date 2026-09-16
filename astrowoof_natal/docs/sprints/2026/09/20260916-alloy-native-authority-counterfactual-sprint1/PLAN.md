# Plan — Alloy Counterfactual Native-Authority Seam Failures

## Guardrails

- Provider-free; no R2, database, deployment, API write, provider call, or release.
- New `.als` files, if any, are documentation/investigation artifacts only.
- Do not claim a bounded Alloy check proves production Python behavior or historical
  data accuracy.
- Preserve the distinction between a historical witness, a model abstraction, and
  an executable regression.

## Slice 0 — Freeze the historical counterexample taxonomy

1. Read the six primary historical witnesses named in `EVIDENCE.md`.
2. Produce a one-row-per-witness abstraction table: preconditions, unsafe event,
   missing/violated invariant, expected safe outcome, and model assignment.
3. Keep Aster terminal ingress, Bramble closeout, and pending reconciliation as
   separate Model A rows; do not label them one root cause.
4. Keep retained-wave reanimation, exact v2 handoff, ambiguity, and terminal-review
   precedence as Model B rows.

Gate A: confirm that every proposed relation/state is justified by public contract
meaning rather than log prose or private workspace inference.

Status: complete. `SLICE 0 - HISTORICAL WITNESS ABSTRACTION AND AUTHORITY MAP.md`
separates seven witnesses into Model A (three command/custody cases) and Model B
(four exact-authority cases), and records the formal-versus-empirical boundary.

## Slice 1 — Model A: terminal ingress, custody, and command selection

1. Add a small `.als` model with closed command/disposition vocabularies.
2. Encode permissive historical behavior only where needed to produce each witness.
3. Run counterexample searches for terminal-versus-generic-retry, stale closeout,
   and pending-provider ordinary-resume selection.
4. Add corrected assertions and bounded satisfiable success examples for terminal
   closeout and provider reconciliation.
5. Record exact scopes, commands, expected SAT/UNSAT outcomes, Analyzer version,
   and a plain-language interpretation.

Gate B: review whether Model A found the intended bad traces without excluding valid
reconciliation or normal terminal settlement.

Status: complete and awaiting review. Model A found all three historical permissive
shapes in exact one-atom traces; the corrected checks found no counterexample through
scope 3, while valid terminal closeout and reconciliation remained satisfiable.

## Slice 2 — Model B: exact external authority and create permission

1. Add a separate small `.als` model for inventory/request/grant/dispatch/intent.
2. Search historical permissive traces for fresh creation after prior lineage,
   creation without exact dispatch, and creation after ambiguous intent.
3. Add corrected assertions for the no-invented-continuation invariant.
4. Add satisfiable examples for valid first admission and valid exact retry dispatch.
5. Confirm that terminal-review is non-create-capable even when other historical
   action evidence exists.

Gate C: review the exact scope and whether all counterexamples map to a real
historical contract distinction rather than a made-up abstraction.

Status: complete and awaiting review. Model B found four intended permissive
authority counterexamples, found no corrected-boundary counterexample through scope
4, and retained SAT examples for valid initial admission, exact retry, and ambiguity
retention.

## Slice 3 — Optional adapter refinement and conclusion

Only proceed if Models A/B expose useful findings that are not already obvious from
their individual invariants.

1. Model public-evidence adapter admission/rejection without modeling JSON, stdout,
   or implementation exceptions.
2. Check that unavailable/invalid evidence leads to defined refusal/no-op behavior,
   never synthesized native authority.
3. Produce a concise counterfactual conclusion: likely early catches, limits, and
   recommended future use (retain as design aid, expand, or stop).

## Tooling gate

Before any Analyzer installation/download, record the proposed source, version,
license, integrity method, invocation, and whether it can run offline after setup.
Owner approval is required before that external/tooling change.

## Expected artifacts

- `BACKGROUND.md`, `EVIDENCE.md`, `PLAN.md`, and `LOG.md`;
- one abstraction matrix/receipt per model;
- optional additive `.als` models under `tools/`;
- a concise closeout distinguishing formal conclusions from empirical ones.
