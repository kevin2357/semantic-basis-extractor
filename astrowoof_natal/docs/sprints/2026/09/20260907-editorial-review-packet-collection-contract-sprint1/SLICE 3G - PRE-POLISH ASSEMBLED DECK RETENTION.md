# Slice 3G — pre-optional initial assembled-deck retention

## Decision requested

Freeze how the runtime packet proves the first whole-deck input when an adopted
optional-stage attempt has replaced the subject's final deck path.

## Confirmed native behavior

The assembly boundary writes the first assembled deck to `subject.deck`. During
polish, every materialized candidate is retained in its attempt directory. When
a candidate improves or passes, `polish_subject` copies that candidate over
`subject.deck` and continues from it.

Consequently, after an adopted first polish:

- the adopted candidate is durable both in its attempt directory and at the
  subject deck path;
- later rejected candidates remain durable in their attempt directories;
- the assembly report retains the six selected workspace names and assembly
  facts; but
- no immutable artifact or recorded digest proves the exact original assembled
  deck bytes that were the first polish input.

The retained Frisbee workspace confirms this shape. Its final deck equals the
accepted attempt-1 candidate. Attempt 2 retains its separate rejected candidate.
The assembly report has no output-deck digest.

## Why the builder stops

The v5 packet requires:

- `initial_assembly.assembled_deck`;
- the first optional-stage `input_deck` to equal it; and
- an independently complete artifact carrying those exact deck bytes.

Re-running deterministic assembly from the six accepted pass workspaces would
probably reproduce the missing bytes. It is nevertheless reconstruction, not
a direct persisted native fact. The current packet has no evidence-origin field
that could say so honestly, and the assembly report supplies no original digest
against which to verify replay. The builder therefore must not silently present
reconstructed bytes as retained evidence.

## Recommended correction

For future runs, preserve the initial assembled deck immutably before optional
stages begin and record its normalized path plus canonical content digest in the
subject record (or an equally exact native assembly relation). Polish may keep
updating the ordinary final/deck pointer, but it must never replace this retained
assembly input.

The runtime packet builder may then:

1. resolve the retained path inside the exact restored workspace;
2. recompute and match its persisted digest;
3. use it as both `initial_assembly.assembled_deck` and the first whole-deck
   transition input; and
4. preserve all subsequent candidate/output transitions from their already
   durable attempt artifacts.

This is evidence retention only. It must not affect assembly output, polish
selection, provider behavior, QA, lifecycle, custody, or delivery.

## Historical boundary

Existing optional-stage workspaces without that exact retained artifact are
not eligible for a complete v5 runtime packet and should return the typed
`incomplete_native_evidence` no-packet result. If historical deterministic
reconstruction is desired later, it needs a separately explicit contract that
labels reconstruction provenance and defines its verification boundary.

## Completed work unaffected

The builder's assembly-terminal branch remains valid when no optional stage
ran, because `subject.deck` is still the original assembled deck. Rejected
initial attempts and accepted creative retries are also now translated with
exact predecessor relations and ordered after all six initial attempts.

## Review gate

Pause before adding a new retained native artifact or changing the public
packet shape. API should confirm whether direct immutable retention is the
required forward contract and whether historical reconstruction remains
excluded.
