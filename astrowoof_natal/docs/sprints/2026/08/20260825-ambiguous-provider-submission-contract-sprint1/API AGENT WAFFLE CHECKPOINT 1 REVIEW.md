# API Agent Waffle Checkpoint 1 Review

Status: approved to proceed to Scenic Waypoint 2, with the runtime conditions
below retained as acceptance gates.

## What is approved

The proposed public pair is the right correction:

- `astrowoof.external_authority_provider_dispatch_result.v3`; and
- `astrowoof.external_authority_v2_command_result.v2`.

In particular, the split between `provider_io_disposition` and
`grant_invocation_disposition` is necessary. It lets API distinguish all three
operationally different facts that v2 collapsed:

1. a provider request was positively not attempted;
2. the create boundary was crossed but provider acceptance is unknown; and
3. a provider identity is durable and only retrieval/reconciliation remains.

The closed refusal and ambiguity vocabularies, ordered prefix rules, and
sanitized fixture set are sufficient for API consumer implementation. A
`pre_provider_refusal` must remain nonterminal for the native run while sealing
the exact grant invocation; API must never translate it into an implicit retry
or replay.

Historical v2 `ambiguous_submission` remains review-only. Nothing in this
contract authorizes retrospective reclassification from absent provider IDs,
stdout, or a reconstructed request.

## Required Waypoint 2 runtime gates

1. The prepared-create digest must have one canonical, documented basis for
   both success and pre-provider refusal. For refusal, it must bind stable
   failed-preparation facts—not exception text—and must not include payload,
   prompt, subject, credential, header, or API-global reservation material.
2. A fresh pre-provider refusal must durably seal the exact invocation before
   its v3 result is published. A later continuation must require a new SBE
   inspection and new API authority; it must not be reachable by generic resume
   or by replaying the old grant.
3. The runtime test matrix must verify action state, invocation state, snapshot
   revision, create-call count, and the public v3 result together for every
   refusal/ambiguity boundary. A test that observes only the public result is
   not sufficient.
4. The command-result reader must preserve the existing distinction between a
   newly committed intent and a prior durable intent being continued. When an
   embedded intent result is present it must join exactly, as implemented; when
   it is absent, the dispatch's request/grant/action/snapshot identities must
   still be enough for API to join its already durable admission record.
5. `provider_identity_durable` is correctly named as the durable custody
   conclusion, not a claim that the replay invocation itself performed new
   provider I/O. Keep that clarification in the public consumer handoff and
   CLI examples.

No API change should begin until the runtime emits this result pair and the
Waypoint 3 fixtures are packaged through the supported installed surface.

## API implementation consequence

On adoption, API will accept only a pinned compatible SBE result v3/command v2
pair, validate it through the public reader, and map it as follows:

| SBE conclusion | API action |
|---|---|
| `pre_provider_refusal` / `not_attempted` | release only the exact unspent action reservation; retain grant/audit; require new inspection and authority for any future work |
| `ambiguous_submission` / `create_entered_unknown` | release execution capacity; retain ambiguity/review custody; prohibit create |
| `detached_provider_pending` / `provider_identity_durable` | release execution capacity; retain reconciliation-only custody |
| `exact_replay` | make no new authority or capacity decision |

That mapping is conditional on the exact runtime proof above; it is not granted
to a v3-shaped fixture alone.
