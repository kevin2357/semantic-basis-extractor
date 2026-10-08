# Slice 1 — v2 Initial-Wave Authority Contract

## Delivered contract

The v2 authority family now has two explicit, closed branches:

- `ordinary_action_set` remains lexical action-ID order with the existing
  request, grant, and no-grant shapes.
- `initial_wave_admission` carries a bounded initial-wave projection with its
  wave ID/digest, route contract, assignment/profile digests, six-member count,
  and ordered member-binding digests.

The latter branch is accepted only when its six action IDs and every binding
digest join the inspected bounded checkpoint **and that checkpoint's actual
`native_route.route_family` is `bounded_natal`**. Its v2 grant repeats the exact
projection and requires six matching authorization documents. The no-grant
result carries the same projection while remaining read-only and non-dispatching.

## Descriptor and provenance fence

The authority export originates from a snapshot-validated workspace and the
stored bounded initial-wave binding bundle. A provider-free regression changes
that bundle after preparation and proves lifecycle inspection emits no request;
the v2 request builder then refuses before grant construction, native mutation,
or provider I/O.

The contract also refuses a changed initial-wave projection—even when its
request digest is recomputed—and a changed per-member binding document.

## Explicit exclusions

This slice creates no dispatch intent and does not execute a provider call. It
does not accept a v1 request or grant as a v2 document, transform the terminal
0.4.71 witness, or change ordinary-v2 ordering/replay behavior.

## Focused qualification

Passed provider-free:

- bounded v2 initial request/grant/no-grant projection join;
- changed projection and member-binding refusal;
- cross-route inspection/projection refusal before request, grant, or no-grant
  dispatch construction;
- initial-wave binding-descriptor tamper refusal before authority export;
- ordinary v2 request/grant/no-grant compatibility; and
- existing v2 intent/dispatch fence coverage.

Command: `python -m unittest` over the bounded initial-v2, v2 contract, and
v2 intent-fence modules — **27 passed, 1 expected optional-schema skip**.

## Gate B

API should review the raw request/grant/no-grant shape. Slice 2 will add the
separate durable bounded initial-wave v2 intent/adapter, including replay and
partial-provider recovery. It must not use the ordinary-v2 intent shape as an
implicit substitute.
