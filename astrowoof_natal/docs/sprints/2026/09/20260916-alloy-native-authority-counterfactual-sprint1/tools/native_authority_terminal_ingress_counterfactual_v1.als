module native_authority_terminal_ingress_counterfactual_v1

// Counterfactual Model A: terminal ingress, API custody, and command selection.
//
// Atoms stand for equality-bearing public identities only. This intentionally does
// not model JSON, hashes, subprocess implementation, provider payloads, logs, or
// private workspace state. It asks whether a small control plane permits the three
// historical unsafe shapes before their corrected precedence rules are imposed.

sig Run {}

abstract sig ResultKind {}
one sig Terminal, Nonterminal extends ResultKind {}

abstract sig Command {}
one sig GenericRetry, OrdinaryResume, Reconcile, Closeout, Refuse extends Command {}

sig NativeResult {
  owner: one Run,
  kind: one ResultKind
}

sig ProviderIdentity {
  owner: one Run
}

sig Invocation {
  owner: one Run,
  available: one NativeResult,
  pending: set ProviderIdentity
}

sig Decision {
  invocation: one Invocation,
  result: one NativeResult,
  command: one Command
}

sig Custody {
  owner: one Run
}

sig Settlement {
  result: one NativeResult,
  custody: one Custody
}

fact PublicIdentityJoins {
  all i: Invocation | i.available.owner = i.owner
  all i: Invocation | all p: i.pending | p.owner = i.owner
  all d: Decision |
    d.result = d.invocation.available and
    d.result.owner = d.invocation.owner
  all s: Settlement | s.result.owner = s.custody.owner
  all i: Invocation | one i.~invocation
}

// Historical permissive shapes. Each must be satisfiable: it demonstrates that a
// missing contract rule admitted the incident pattern, not that the incident bytes
// can or should be reconstructed.

pred LegacyAsterTerminalFallback {
  some d: Decision |
    d.result.kind = Terminal and
    d.command = GenericRetry
}

pred LegacyBrambleDuplicateCloseout {
  some disj first, second: Settlement |
    first.result = second.result and
    first.custody = second.custody and
    first.result.kind = Terminal
}

pred LegacyAsterPendingOrdinaryResume {
  some d: Decision |
    d.result.kind = Nonterminal and
    some d.invocation.pending and
    d.command = OrdinaryResume
}

// Corrected adapter posture. It does not invent a command from unavailable native
// evidence: every decision shown is already joined to one public result.

pred CorrectedAdapter {
  all d: Decision |
    d.result.kind = Terminal implies d.command in Closeout + Refuse

  all d: Decision |
    d.result.kind = Nonterminal and some d.invocation.pending implies
      d.command in Reconcile + Refuse

  all r: NativeResult, c: Custody |
    lone { s: Settlement | s.result = r and s.custody = c }
}

pred ValidTerminalCloseout {
  CorrectedAdapter
  some d: Decision | d.result.kind = Terminal and d.command = Closeout
  some Settlement
}

pred ValidPendingReconciliation {
  CorrectedAdapter
  some d: Decision |
    d.result.kind = Nonterminal and
    some d.invocation.pending and
    d.command = Reconcile
}

assert TerminalDominatesGenericFallback {
  CorrectedAdapter implies
    no d: Decision | d.result.kind = Terminal and d.command = GenericRetry
}

assert TerminalSettlementIsExactOnce {
  CorrectedAdapter implies
    all r: NativeResult, c: Custody |
      lone { s: Settlement | s.result = r and s.custody = c }
}

assert PendingProviderIdentityBlocksOrdinaryResume {
  CorrectedAdapter implies
    no d: Decision |
      d.result.kind = Nonterminal and
      some d.invocation.pending and
      d.command = OrdinaryResume
}

run LegacyAsterTerminalFallback for exactly 1 Run, exactly 1 NativeResult,
  exactly 1 Invocation, exactly 1 Decision, exactly 0 ProviderIdentity,
  exactly 0 Custody, exactly 0 Settlement

run LegacyBrambleDuplicateCloseout for exactly 1 Run, exactly 1 NativeResult,
  exactly 1 Invocation, exactly 1 Decision, exactly 0 ProviderIdentity,
  exactly 1 Custody, exactly 2 Settlement

run LegacyAsterPendingOrdinaryResume for exactly 1 Run, exactly 1 NativeResult,
  exactly 1 Invocation, exactly 1 Decision, exactly 1 ProviderIdentity,
  exactly 0 Custody, exactly 0 Settlement

run ValidTerminalCloseout for exactly 1 Run, exactly 1 NativeResult,
  exactly 1 Invocation, exactly 1 Decision, exactly 0 ProviderIdentity,
  exactly 1 Custody, exactly 1 Settlement

run ValidPendingReconciliation for exactly 1 Run, exactly 1 NativeResult,
  exactly 1 Invocation, exactly 1 Decision, exactly 1 ProviderIdentity,
  exactly 0 Custody, exactly 0 Settlement

check TerminalDominatesGenericFallback for 3
check TerminalSettlementIsExactOnce for 3
check PendingProviderIdentityBlocksOrdinaryResume for 3
