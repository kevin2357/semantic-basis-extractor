# Slice 0 — Production Characterization

Status: complete; Voof-paws 1 review pending.

## Finding

SBE 0.4.39 contains one confirmed Waffle defect: theme-group distribution
policy is advisory at pass acceptance but remains a hard exception in final
assembly. The exception escapes the public command without a sealed typed
result, so the API sees a generic retryable subprocess failure and can re-enter
the same deterministic failure indefinitely.

The initially suspected premature local-work consumption is not supported.
The consumed semantic operation was provider-result fan-in and retry evaluation;
adopting the completed provider evidence durably changed the action/pass truth.
Final assembly was the next phase reached in the same invocation.

## Source map

- `validation.py` classifies distribution-only theme findings as advisories at
  pass acceptance and final validation.
- `assembly.py` still independently raises when an interdogpendence theme group
  violates its legacy minimum/balance boundary.
- `closure.main()` first inspects and executes completed-provider fan-in,
  commits that semantic operation after the action becomes `REPORTED`, and then
  enters `finalize_subjects()`.
- The assembly `ValueError` is outside a typed native-result publication path.

## Provider-free production-boundary witness

`test_waffle_scone_finalization_slice0.py` constructs real accepted pass
workspaces, rewrites pass 6 to a structurally valid but imbalanced 14/2/2/2
distribution, and proves:

1. real pass acceptance returns success with only
   `theme_group_balance` advisory evidence;
2. lifecycle v0.7 selects
   `provider_result_fan_in_and_retry_evaluation` for completed provider evidence;
3. the public `closure.main()` resume adopts that evidence and durably consumes
   exactly that operation;
4. real `finalize_subjects()` / `assemble_subject()` raises the same legacy
   balance exception; and
5. no command-result JSON is published and no subject is assembled.

A separate control replaces one assignment with an unknown registry value and
proves the structural `theme_group_assignment` error remains a hard pass-
acceptance failure.

Focused command:

```text
python -m unittest astrowoof_natal.tests.test_waffle_scone_finalization_slice0 -v
```

Result: 2 passed.

## Causal boundary

This is not evidence of provider duplication, false custody release, or false
consumption. The provider-backed operation completed and was adopted exactly
once. The loop begins because a later deterministic local policy contradiction
is exposed only as an untyped process failure.

Scone remains an independent comparator: its trace carries live polish custody
and a sealed v0.2 review result. No shared implementation cause is claimed.

## Proposed correction boundary

- Remove the obsolete distribution hard gate from assembly while preserving
  structural registry/assignment failures.
- Ensure deterministic pre-publication assembly contradictions have a closed,
  non-spinning public disposition; do not make stderr or exit code authoritative.
- Do not alter the established fan-in consumption ordering based on this
  incident.
