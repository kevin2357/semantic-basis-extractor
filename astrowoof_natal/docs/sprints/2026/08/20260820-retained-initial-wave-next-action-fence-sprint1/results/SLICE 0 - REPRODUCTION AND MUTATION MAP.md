# Slice 0 — Reproduction and Mutation Map

Date: 2026-08-20  
Status: complete; paused for API review before Slice 1 schema freeze

## Provider-free reproduction

`test_characterizes_retained_initial_lineage_reentry_before_fence` constructs a
generated exact-Natal workspace through the production preparation functions. It
then preserves six historical `authoring_initial` ledger actions and provider
Response identities while removing the currently joinable wave and pass attempts.
No retained Aster bytes are read.

Under the SBE 0.4.13 behavior, the next ordinary route evaluation sees all pass
attempts empty. `prepare_exact_interactive_initial_wave()` does not examine the
historical ledger/provider lineage before preparing another wave. The reproducer
therefore proves:

- six old and six new action IDs are disjoint;
- the ledger contains twelve initial-authoring actions;
- the newly inferred wave accepts a complete authorization envelope; and
- the real concurrent create coordinator makes six calls to a scripted transport.

This is the incident class. The test deliberately characterizes the unsafe
pre-fence behavior; Slice 4 will invert it into a zero-create refusal regression.

`test_characterizes_public_resume_reentry_before_constrained_grant` proves the same
route through the actual public `closure.main()` resume/dispatch command. The first
ordinary resume infers and publishes a distinct prepared wave. The second ordinary
resume supplies the existing v1 wave envelope and six member authorization files,
but no proposed constrained external-authority grant, and reaches six scripted
creates. This confirms both the routing assumption and the lower-level mechanism.

## Current mutation and provider-I/O sequence

1. `main()` loads and snapshot-validates the workspace.
2. Exact interactive routing selects initial-wave mode when either a stored wave
   exists or every pass has no attempts.
3. `prepare_exact_interactive_initial_wave()`:
   - derives six request payloads;
   - calls `prepare_action()` six times;
   - writes request/private prompt artifacts and pass attempts;
   - sets the new `initial_authoring_wave`;
   - writes the binding bundle;
   - persists `run.json`, public state, spend requests and journal projection;
   - publishes a complete workspace snapshot.
4. `authorize_exact_interactive_initial_wave()` preflights the wave envelope and
   six member documents against a copied ledger, swaps the authorized ledger into
   state, marks the wave authorized, and persists a checkpoint.
5. `execute_exact_interactive_initial_wave()` launches six local create workers.
6. Under a process-local mutation lock, each worker changes its action from
   `AUTHORIZED` to `SUBMITTING` and persists state.
7. A six-member barrier publishes one complete pre-POST workspace snapshot only
   after all six intent records are durable.
8. The lock is not held during the six scripted/provider creates.
9. Returned provider identities are serialized into durable ledger/pass state;
   each identity checkpoint is persisted and snapshotted.
10. A wave result and ordinary native transition result are published after the
    coordinator unwinds.

## Last safe preflight point

The last safe point for the new constrained continuation is before step 3 performs
any preparation mutation. Under the shared cross-process
`spend-consumption.lock`, SBE must revalidate the inspected snapshot/request/grant
and classify historical lineage before it can prepare, authorize, or consume an
action.

For an admitted exact wave, the same writer ownership must continue through grant
application and the durable all-member pre-submit intent checkpoint. It must then
be released for slow provider I/O and reacquired for provider-identity persistence.
This preserves concurrency without pretending the local checkpoint and remote
provider create are atomic.

## Required failure interpretation

- Before durable intent: refusal or interruption permits no provider create.
- Durable intent plus durable provider ID: reconciliation/replay of that identity.
- Durable intent without durable provider ID: ambiguity/review; never create again.
- Historical initial-wave lineage without one exact joinable wave:
  `initial_wave_lineage_unjoinable`, `external_authority_request=null`, closed
  `external_authority_refusal`, and zero provider creates.

## Controls already exercised

- Fresh six-member preparation/authorization/detach remains covered by
  `test_exact_interactive_initial_wave_prepares_authorizes_and_detaches`.
- Existing authorization tests prove the six-member wave application is
  all-or-none once a valid wave exists.
- Existing spend tests cover ordinary independently prepared actions.

## Focused test evidence

Command:

```text
python -m unittest \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_characterizes_public_resume_reentry_before_constrained_grant \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_characterizes_retained_initial_lineage_reentry_before_fence \
  astrowoof_natal.tests.test_semantic_closure.TestSemanticClosure.test_exact_interactive_initial_wave_prepares_authorizes_and_detaches
```

Result: 3 passed; provider network calls: 0; retained-workspace access: none.
