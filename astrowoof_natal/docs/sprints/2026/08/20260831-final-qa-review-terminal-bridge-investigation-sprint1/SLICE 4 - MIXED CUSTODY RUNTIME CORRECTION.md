# Slice 4 — mixed-custody runtime correction

## Outcome

The Glimmer contradiction is corrected at both native boundaries that made it
possible:

1. status reduction no longer lets a provisional final-QA review label conceal
   ambiguity, executable providerless work, or durable provider custody; and
2. the constrained ordinary-v2 executor revalidates the post-intent checkpoint
   under the native writer before it may enter a provider create call.

These changes are deliberately paired. The reducer publishes truthful lifecycle
state after custody exists, while the fence prevents provider I/O if a terminal
contradiction is introduced between authority validation and call-entry.

## Reducer precedence

After true terminal-transition and delivery states, native reduction now uses
this safety order:

1. ambiguous submission evidence;
2. durable provider identity / waiting custody;
3. budget refusal;
4. prepared providerless action;
5. authorized or submitting providerless action;
6. preserved final-QA review only when none of the above remains.

Accordingly:

- provider-pending polish is nonterminal and reconciliation-selected;
- provider custody also outranks a different prepared or budget-blocked action;
- call-entered identity-less polish remains ambiguous;
- authorized providerless polish remains nonterminal;
- a no-custody final-QA warning remains a legitimate review terminal.

## Post-intent fence

`dispatch_external_authority_v2_intent()` reopens and validates the durable
intent under the native lifecycle writer before provider I/O. If the checkpoint
is terminal but contains no provider identity, call-entry cursor, or ambiguity,
the executor refuses the exact invocation before POST.

The refusal is not represented as a transport failure or generic nonzero exit.
It uses:

- dispatch result schema
  `astrowoof.external_authority_provider_dispatch_result.v4`;
- command result schema `astrowoof.external_authority_v2_command_result.v3`;
- outcome `pre_provider_refusal`;
- reason `post_intent_lifecycle_contradiction`;
- provider-I/O assertion `not_attempted`; and
- grant disposition `refused`.

The complete ordered action set is refused as one constrained invocation. Its
history is immutable, the live intent is removed, and the actions return to a
history-bearing `PREPARED` posture. The refused grant cannot be reused. Any
later attempt requires a fresh lifecycle inspection, request, API decision,
authorization documents, and grant.

If provider custody or call-entry ambiguity already exists, that evidence wins:
the fence does not clear, downgrade, or reinterpret it as a pre-provider
refusal.

## Public compatibility

The existing successful dispatch result v3 and command result v2 remain frozen.
Only the new refusal needs the v4/v3 pair, avoiding a dishonest widening of old
closed schemas. Readers and package exports recognize both generations.

No lifecycle schema version changes. Existing lifecycle contracts already
represent the corrected truth: pending custody selects reconciliation and is
not terminal.

## Regression evidence

The focused matrix proves:

- real public ordinary-v2 command with pending polish publishes nonterminal
  reconciliation truth;
- direct executor has the same behavior;
- provider custody plus a different prepared action selects reconciliation;
- provider custody plus a different budget refusal selects reconciliation;
- after custody clears, the remaining prepared or budget fact regains its
  ordinary supported projection;
- ambiguity outranks review;
- authorized providerless work outranks review;
- no-custody review remains terminal;
- direct and public-CLI post-intent contradictions refuse before provider I/O;
- exact refusal replay is inert;
- stale refused authority cannot be reused;
- a fresh request/grant can establish a new intent; and
- rehashed malformed refusal inventories fail validation.

Result: 123 tests passed with five expected optional-schema skips. No external
network, provider, spend, retained-workspace mutation, or real reconciliation
occurred. `git diff --check` is clean.

## Review gate

Paused at Voof-paws 5 for API consumer review before installed-wheel/package
qualification.
