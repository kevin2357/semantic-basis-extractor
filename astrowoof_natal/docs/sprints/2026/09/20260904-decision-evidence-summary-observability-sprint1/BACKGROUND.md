# Background — decision-evidence trace summaries

## Motivation

SBE `0.4.36` introduced sanitized workspace fingerprints, native-state
summaries, public decision summaries, publication summaries, and command-exit
events. Those traces now answer most lifecycle, custody, authority, and
publication questions without restoring a retained workspace.

Recent investigations still required exact R2 archives to answer a more basic
operational question: **what validated evidence caused this otherwise coherent
decision?**

The Doughmeat/Macaron investigation is the clearest example. Logs proved that
both runs reconciled eight provider actions, consumed two polish attempts, and
sealed `review_required / final_qa_requires_review`. They did not disclose:

- the final validation and lint classifications;
- the remaining rejection/warning codes;
- whether each polish attempt was accepted, unchanged, or invalid; or
- the bounded reason why Macaron's second polish produced no candidate reports.

The exact archives showed ordinary editorial exhaustion, including an invalid
sparse edit on Macaron's second attempt. That was valuable confirmation, but it
should not require an R2 restore in a routine investigation.

## Objective

Make routine diagnosis log-first by emitting compact, sanitized summaries of
the evidence SBE has already validated at stable decision boundaries. Preserve
public artifacts and native state as the only authority. Retain exact artifact
inspection for integrity proofs, unfamiliar failures, historical/missing logs,
or suspected persistence contradictions.

## Scope

This is intentionally broader than terminal decisions but narrower than
general-purpose debug logging. Candidate boundaries are:

1. **Optional-stage adoption** — what exact completed evidence was accepted,
   rejected, unchanged, or failed before a candidate report existed.
2. **Deterministic validation/finalization** — validation/lint status, bounded
   reason-code counts, and whether the result is eligible for continuation,
   review, or delivery.
3. **Lifecycle selection** — enrich the existing public decision summary only
   where the validated contract already carries relevant evidence.
4. **External-authority/dispatch refusal** — the typed predicate and
   provider-I/O/custody assertion, without exposing grants or payloads.
5. **Native publication** — the complete sanitized publication-evidence
   summary after sealing, joined to exact public identities. Terminality remains
   an explicit result-contract fact, never an inference from publication.

Do not emit a large summary at every mutation. Intermediate implementation
details are not durable decisions and would increase noise without improving
forensics.

## Non-goals

- Logs do not become transition, recovery, settlement, or release authority.
- No prompts, deck prose, provider request/response bodies, credentials,
  authorization documents, or private workspace paths are logged.
- No API state, lease, reservation, capacity, or settlement fact is asserted.
- No lifecycle, custody, authority, editorial-policy, or provider behavior is
  changed.
- No unbounded action, finding, field-path, or identifier inventory is emitted.

## Success criterion

Replaying representative recent investigations from logs alone should classify
the routine outcome and its bounded reason in at least 90% of cases. Exact
workspace/result inspection remains necessary when the question is whether the
logged projection agrees byte-for-byte with authoritative evidence.
