# Plan — Bounded Initial-Wave v2 Execution

## Objective

Close the bounded initial-wave v2 authority/execution gap exposed by the first
paid QA bounded run, without changing provider behavior during this sprint and
without weakening v1 or ordinary-v2 custody boundaries.

## Slice 0 — Contract and state-machine inventory

Trace the exact v2 request, grant, dispatch-intent, command, and resume path
that refused the QA witness. Compare it to the existing bounded v1
initial-wave path. Record:

1. every immutable identity that a v2 initial-wave request/grant must bind;
2. the canonical six-member semantic order and initial-wave digest inputs;
3. durable mutation and replay points before any provider call;
4. the narrowest reusable bounded-lifecycle helpers; and
5. an explicit compatibility disposition for 0.4.71 v1-authorized workspaces.

**Gate A:** API reviews the frozen proposed v2 initial-wave shape and confirms
that no API-side code will infer or transform v1 authority into v2.

## Slice 1 — v2 initial-wave authority contract

Extend the v2 request/grant/inspection contracts only as needed to represent
`initial_wave_admission` independently of `ordinary_action_set`.

- Require exactly six members in prepared semantic order.
- Bind the native route, checkpoint, run/profile/spend-policy identity, and
  initial-wave context/digest.
- Preserve ordinary-v2 lexical ordering as a separate branch.
- Reject mixed schemas, wrong route/profile/checkpoint, wrong ordering, stale
  grants, duplicates, malformed authorization documents, and source/binding
  descriptor path-or-digest tamper before native mutation or provider I/O.

**Gate B:** provider-free unit/fixture review proves the new contract is exact
and no v1 document is accepted as a v2 document.

## Slice 2 — Durable bounded v2 intent and execution adapter

Add a bounded-initial v2 dispatch path that validates the new documents, writes
an exact durable intent once, and delegates through the established bounded
initial-wave execution machinery.

- Do not recreate prepared actions or spend reservations.
- Preserve the six-action all-or-nothing authority boundary.
- Give a replay the same completed/intent result rather than another provider
  submission.
- Retain current ordinary-v2 dispatch unchanged.

**Gate C:** failure-injection and fake-provider tests cover pre-intent refusal,
post-intent replay, partial execution recovery, duplicate authorization, and
zero-I/O malformed paths, including source/binding descriptor path-or-digest
tamper.

## Slice 3 — Immutable successor catalog and candidate handoff

Create the successor bounded runtime profile/prompt release records, if required
by the immutable catalog model, and build a retained candidate wheel. Provide
API with the complete wheel/profile/prompt/catalog/package identity table and
raw success/refusal fixtures.

**Gate D:** API installs the exact candidate and runs a joint provider-free
initial-wave admission/resume/replay cell, alongside unchanged ordinary-v2
coverage. Only then can owner-approved release qualification begin.

## Non-goals

No operation against the terminal 0.4.71 QA workspace, no provider-backed test,
and no deployment or activation are authorized by this plan.
