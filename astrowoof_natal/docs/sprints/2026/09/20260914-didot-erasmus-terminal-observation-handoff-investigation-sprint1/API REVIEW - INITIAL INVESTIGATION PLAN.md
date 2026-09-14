# API Review — Initial Investigation Plan

**Status: approved through Slice 2.** The plan correctly treats Didot and
Erasmus as distinct authority losses and does not propose unsafe latest-result
discovery or a generic terminal-evidence shortcut.

## Confirmed framing

- Didot's native terminal-delivery command, result
  `nres_fd73a016721dcf725d6a5449`, receipt, and invocation are exact evidence.
  The relevant investigation question is where API loses that already-proven
  identity after the first eligibility failure and before the retry's
  `delivery_validation` result. This is not a reason to ask SBE to invent new
  delivery evidence.
- Erasmus's exact terminal-review command, result
  `nres_68c273587d4363fe3d150cb9`, receipt, and invocation are likewise exact
  evidence. A later generic sealed preflight must not be promoted into the
  earlier invocation-bound command authority merely to make observation run.
- The unexpected second Erasmus claim is independently important. It can
  explain the later skip, but it cannot retroactively excuse a missing observer
  call on the first command-bearing close.

## Required Slice 1 assertions

For each of the three reproductions, record both the `SbeCycleResult` field
values *and* whether `_observe_editorial_terminal()` was entered. Do not use
the ordinary logger line alone as proof of invocation: the production logger
may itself be a separate telemetry failure. A spy/recording observer plus the
normal production worker constructor is appropriate.

The Didot reproduction should additionally prove that the retry reuses the
same native run/result/receipt identity and cannot cross-bind a different job
or newer result.

The Erasmus-A reproduction should establish whether the command-bearing close
calls the observer under current source. If it does, Slice 2 must distinguish
runtime/deployment/logging loss from a control-flow omission before any code
change is proposed.

## Ownership and boundaries

No current evidence supports an SBE schema bump. SBE has supplied exact typed
handoffs; API must first prove where it receives, persists, or drops them.
Keep all proposed observation work post-authoritative and best-effort: no
observer outcome may affect queue state, retryability, custody, capacity,
spend, cleanup, or terminal outcome.

Slice 3's possible durable carry-forward needs an explicit API ownership and
idempotency decision; it must not be added incidentally while diagnosing the
retry. The stated Alloy-impact fence is appropriate.
