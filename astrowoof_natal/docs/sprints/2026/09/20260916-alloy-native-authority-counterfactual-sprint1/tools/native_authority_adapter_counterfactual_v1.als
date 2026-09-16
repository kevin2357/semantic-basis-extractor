module native_authority_adapter_counterfactual_v1

// Optional Counterfactual Model C: public-evidence adapter behavior.
// The model represents the API/SBE translation boundary, not JSONL, subprocesses,
// schemas, database transactions, or implementation exceptions. An AdapterDecision
// may persist a terminal result, invoke exact authority dispatch, use generic retry,
// or refuse. The question is whether it can choose the wrong category of action.

sig Run {}

abstract sig ResultKind {}
one sig ValidTerminal, ValidNonterminal, Invalid extends ResultKind {}

abstract sig AdapterAction {}
one sig PersistTerminal, ExactDispatch, GenericRetry, Refuse extends AdapterAction {}

sig PublicResult {
  owner: one Run,
  kind: one ResultKind
}

sig PublicAuthorityRequest {
  owner: one Run
}

sig ExactGrant {
  owner: one Run,
  request: one PublicAuthorityRequest
}

// Generic API authorization is deliberately weaker than an ExactGrant. It records
// policy admission but does not carry the SBE request identity required for dispatch.
sig GenericAuthorization {
  owner: one Run
}

sig AdapterAttempt {
  owner: one Run,
  result: lone PublicResult,
  request: lone PublicAuthorityRequest,
  grant: lone ExactGrant,
  genericAuthorization: lone GenericAuthorization
}

sig AdapterDecision {
  attempt: one AdapterAttempt,
  action: one AdapterAction,
  selectedResult: lone PublicResult,
  selectedRequest: lone PublicAuthorityRequest,
  selectedGrant: lone ExactGrant
}

fact PublicEvidenceOwnership {
  all q: ExactGrant | q.request.owner = q.owner
  all a: AdapterAttempt |
    (some a.result implies a.result.owner = a.owner) and
    (some a.request implies a.request.owner = a.owner) and
    (some a.grant implies a.grant.owner = a.owner) and
    (some a.genericAuthorization implies a.genericAuthorization.owner = a.owner)
  all a: AdapterAttempt | one a.~attempt
  all d: AdapterDecision |
    (some d.selectedResult implies d.selectedResult.owner = d.attempt.owner) and
    (some d.selectedRequest implies d.selectedRequest.owner = d.attempt.owner) and
    (some d.selectedGrant implies d.selectedGrant.owner = d.attempt.owner)
}

// These are the historical/architectural bad choices the unconstrained adapter
// admits. They are intentionally not all claims about one named historical run.

pred LegacyTerminalFallsToGenericRetry {
  some d: AdapterDecision |
    some d.attempt.result and
    d.attempt.result.kind = ValidTerminal and
    d.action = GenericRetry
}

pred LegacyGenericAuthorizationSynthesizesDispatch {
  some d: AdapterDecision |
    some d.attempt.genericAuthorization and
    no d.attempt.request and
    d.action = ExactDispatch
}

pred LegacyExactRequestFallsToGenericRetry {
  some d: AdapterDecision |
    some d.attempt.request and
    some d.attempt.grant and
    d.action = GenericRetry
}

pred LegacyTerminalReopensAsDispatch {
  some d: AdapterDecision |
    some d.attempt.result and
    d.attempt.result.kind = ValidTerminal and
    d.action = ExactDispatch
}

pred CorrectedAdapter {
  all d: AdapterDecision |
    d.action = PersistTerminal implies
      some d.attempt.result and
      d.attempt.result.kind = ValidTerminal and
      d.selectedResult = d.attempt.result

  all d: AdapterDecision |
    d.action = ExactDispatch implies
      some d.attempt.request and
      some d.attempt.grant and
      d.attempt.grant.request = d.attempt.request and
      d.selectedRequest = d.attempt.request and
      d.selectedGrant = d.attempt.grant and
      (no d.attempt.result or d.attempt.result.kind != ValidTerminal)

  all d: AdapterDecision |
    some d.attempt.result and d.attempt.result.kind = ValidTerminal implies
      d.action in PersistTerminal + Refuse

  all d: AdapterDecision |
    some d.attempt.genericAuthorization and
    no d.attempt.request implies d.action != ExactDispatch

  all d: AdapterDecision |
    some d.attempt.request and some d.attempt.grant and
    d.attempt.grant.request = d.attempt.request and
    (no d.attempt.result or d.attempt.result.kind != ValidTerminal)
    implies d.action in ExactDispatch + Refuse
}

pred ValidTerminalIntake {
  CorrectedAdapter
  some d: AdapterDecision |
    d.action = PersistTerminal and
    d.attempt.result.kind = ValidTerminal
}

pred ValidExactAuthorityDispatch {
  CorrectedAdapter
  some d: AdapterDecision |
    d.action = ExactDispatch and
    d.attempt.request = d.attempt.grant.request
}

pred ValidGenericAuthorizationRefusal {
  CorrectedAdapter
  some d: AdapterDecision |
    some d.attempt.genericAuthorization and
    no d.attempt.request and
    d.action = Refuse
}

assert TerminalDoesNotUseFallbackOrDispatch {
  CorrectedAdapter implies
    no d: AdapterDecision |
      some d.attempt.result and d.attempt.result.kind = ValidTerminal and
      d.action in GenericRetry + ExactDispatch
}

assert ExactDispatchUsesExactPublishedPair {
  CorrectedAdapter implies
    all d: AdapterDecision |
      d.action = ExactDispatch implies
        d.selectedRequest = d.attempt.request and
        d.selectedGrant = d.attempt.grant and
        d.attempt.grant.request = d.attempt.request
}

assert GenericAuthorizationCannotStandInForRequest {
  CorrectedAdapter implies
    all d: AdapterDecision |
      some d.attempt.genericAuthorization and no d.attempt.request implies
        d.action != ExactDispatch
}

assert ExactPairDoesNotUseGenericRetry {
  CorrectedAdapter implies
    no d: AdapterDecision |
      some d.attempt.request and some d.attempt.grant and
      d.attempt.grant.request = d.attempt.request and
      (no d.attempt.result or d.attempt.result.kind != ValidTerminal) and
      d.action = GenericRetry
}

run LegacyTerminalFallsToGenericRetry for exactly 1 Run, exactly 1 PublicResult,
  exactly 0 PublicAuthorityRequest, exactly 0 ExactGrant,
  exactly 0 GenericAuthorization, exactly 1 AdapterAttempt, exactly 1 AdapterDecision

run LegacyGenericAuthorizationSynthesizesDispatch for exactly 1 Run,
  exactly 0 PublicResult, exactly 0 PublicAuthorityRequest, exactly 0 ExactGrant,
  exactly 1 GenericAuthorization, exactly 1 AdapterAttempt, exactly 1 AdapterDecision

run LegacyExactRequestFallsToGenericRetry for exactly 1 Run,
  exactly 0 PublicResult, exactly 1 PublicAuthorityRequest, exactly 1 ExactGrant,
  exactly 0 GenericAuthorization, exactly 1 AdapterAttempt, exactly 1 AdapterDecision

run LegacyTerminalReopensAsDispatch for exactly 1 Run, exactly 1 PublicResult,
  exactly 1 PublicAuthorityRequest, exactly 1 ExactGrant,
  exactly 0 GenericAuthorization, exactly 1 AdapterAttempt, exactly 1 AdapterDecision

run ValidTerminalIntake for exactly 1 Run, exactly 1 PublicResult,
  exactly 0 PublicAuthorityRequest, exactly 0 ExactGrant,
  exactly 0 GenericAuthorization, exactly 1 AdapterAttempt, exactly 1 AdapterDecision

run ValidExactAuthorityDispatch for exactly 1 Run, exactly 0 PublicResult,
  exactly 1 PublicAuthorityRequest, exactly 1 ExactGrant,
  exactly 0 GenericAuthorization, exactly 1 AdapterAttempt, exactly 1 AdapterDecision

run ValidGenericAuthorizationRefusal for exactly 1 Run, exactly 0 PublicResult,
  exactly 0 PublicAuthorityRequest, exactly 0 ExactGrant,
  exactly 1 GenericAuthorization, exactly 1 AdapterAttempt, exactly 1 AdapterDecision

check TerminalDoesNotUseFallbackOrDispatch for 3
check ExactDispatchUsesExactPublishedPair for 3
check GenericAuthorizationCannotStandInForRequest for 3
check ExactPairDoesNotUseGenericRetry for 3
