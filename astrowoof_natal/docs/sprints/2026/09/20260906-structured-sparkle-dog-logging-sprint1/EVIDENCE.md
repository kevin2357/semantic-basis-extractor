# Evidence

## Current gate

Slice 0 is complete. The logging surface and desired-field census are ready for
Slice 1 contract work. No runtime format change has begun.

## Source findings

- One shared application formatter emits the pipe-delimited stderr records.
- Nine public CLI/configuration paths use the shared logging arguments.
- Approximately 169 ordinary logging calls exist in the authoring package.
- Four context variables currently bind host, native run, invocation, and native
  state.
- Typed execution events already use JSON envelopes and isolated sinks.
- Seven bounded observability helpers compute structured values before
  flattening them into messages.
- The run reporter currently reparses pipe messages with a boundary-event set
  and safe-field allowlist.

## Safety characterization

- Ordinary application logs use stderr and do not contaminate command stdout.
- Ordinary application records are distinct from execution-event envelopes.
- No provider, R2, QA, API database, deployment, or retained workspace was
  accessed or mutated.

