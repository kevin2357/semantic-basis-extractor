# Slice 3 — provider-free production-boundary reproduction

## Result

The current public ordinary-v2 command reproduces Glimmer's contradiction with
one scripted provider call and no network access:

1. a valid `FINAL_QA_WARN` workspace exposes one prepared polish action;
2. temporal lifecycle exports ordinary-v2 external authority;
3. the exact grant is committed;
4. intent persistence changes outer status to
   `FINAL_QA_REQUIRES_REVIEW` while the action is `SUBMITTING`;
5. the public v2 command nevertheless crosses provider call-entry;
6. a scripted response identity becomes durable;
7. the command reports `detached_provider_pending`;
8. public lifecycle simultaneously reports terminal review and provider
   continuation; and
9. no sealed native terminal result exists.

The public temporal document makes the contradiction especially explicit: its
checkpoint basis says `terminal=true` while its temporal decision selects an
eligible `provider_reconciliation_cycle` for the same polish action.

## Added characterization cells

`test_final_qa_mixed_custody_slice3.py` freezes five provider-free cells:

- public CLI: final-QA warning → exact v2 grant → one scripted POST → durable
  pending identity, terminal-looking lifecycle, no sealed result;
- direct executor: the same transition at the intent and identity checkpoints;
- call-entry timeout: action becomes ambiguous but outer review status masks it;
- providerless authorized polish: terminal-looking status appears without an
  explicit denial/retirement disposition; and
- no-custody final-QA warning: the legitimate terminal control remains distinct.

These are characterization tests. They intentionally assert current defective
behavior so Slice 4 can make the mixed-custody cells change while preserving the
legitimate terminal control.

## Focused evidence

The new five-test characterization passes. The combined terminal-review and v2
fence matrix passes 31 tests with two expected optional-`jsonschema` skips.

No real provider endpoint, credentials, spend, R2 access, or retained workspace
was used. The scripted public-command cell counts exactly one local provider
create invocation.

## Minimal correction point

The smallest coherent runtime correction remains:

1. give authorized/submitting/ambiguous/provider-bound ordinary actions proper
   precedence over provisional `FINAL_QA_WARN` in `update_run_status()`;
2. validate the just-persisted intent checkpoint before provider call-entry;
3. refuse a contradictory post-intent checkpoint with zero provider I/O and
   immutable refused-grant evidence; and
4. preserve genuine no-custody review-terminal publication.

This is not an API mapper change and does not justify weakening API's strict
terminal-lifecycle validator.
