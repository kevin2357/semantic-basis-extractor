# API Slice 4 review — finding classification and ownership

## Decision

Approved. Slice 4 correctly freezes three production **API mapper defects**
and finds no demonstrated SBE public-contract or cross-artifact evidence gap.
SBE `0.4.32` already provides the public facts and exact readers needed for
each correction; this audit does not justify an SBE implementation or release.

The priority order is also right: D-03 is first because a bounded nonterminal
review/unsupported outcome can currently manufacture a terminal-ingress path,
which then makes D-01's generic latest-result fallback reachable. D-01 and
D-02 are independent high-priority consumer corrections.

## Frozen API handoff constraints

Slice 5's implementation handoff should state these as executable rules:

1. Normal terminal ingress accepts only an exact result identity returned by
   the invocation path or supplied by a named, validated recovery path. Generic
   `read_latest_sealed` is not live transition authority. A historical recovery
   workflow, if retained, must be separately named and validate the exact join
   before it can call terminal ingestion.
2. An absent readiness/continuation field is unknown/refused; it may never
   default to `local_continuation_required=True` (or any other runnable branch).
3. Bounded `retain_for_review` and `unsupported_retain_capacity` must take
   distinct nonterminal worker dispositions. They must not construct terminal
   evidence, invoke terminal ingress, select a generic sealed result, or erase
   action-level custody. Releasing local capacity is a separate API resource
   decision, not evidence that native work is terminal.
4. Where the outer product state is deliberately `failed`, the correction must
   retain the native distinction in reason code/diagnostic projection and keep
   custody, settlement, reservation, and delivery decisions independently
   evidenced. Outer failure is not permission to settle or release everything.
5. The due/not-due spy is useful regression coverage, but it must prove that
   API consumes SBE's temporal conclusion and selected subset rather than
   reconstructing member due-ness.

## Scope note

Sprint 60 already corrected sealed-result outcome discrimination in the API.
The next bounded API follow-up should explicitly identify which remaining
generic terminal-ingress fallback and readiness/bounded-result mapper code is
still in scope, rather than presenting the already-completed outcome
discrimination as new work.

## Gate

API approves SBE to proceed with Slice 5 handoffs and process-document updates.
No provider work, retained-QA mutation, deployment, or SBE release is approved
or needed by this review.
