# Slice 4 — recent investigation replay matrix

## Outcome

The new evidence summaries were replayed against the recurring operational
classes that drove recent checkpoint downloads. Seven of eight classes are now
classifiable from trace evidence alone. The eighth is intentionally bounded:
logs can identify a deterministic finalization failure before publication, but
an exact public-artifact or checkpoint read remains necessary if the question
is whether a valid publication nevertheless survived an interruption.

This is the intended log-first boundary. Logs accelerate diagnosis; they do not
replace sealed public artifacts as authority.

## Exact retrospective: Doughmeat and Macaron

The already-retained, read-only generation-11 archives were projected through
the new helpers. No R2, provider, API, or QA operation occurred.

### Doughmeat

The projected trace facts distinguish ordinary editorial exhaustion:

- polish attempt 1: `POLISH_ACCEPTED`, accepted and improved, 2 warnings;
- polish attempt 2: `POLISH_ACCEPTED`, accepted and improved, 1 warning;
- final validation: `pass`, 0 errors, 1 warning;
- final lint: `warn`, 3 ordinary warnings;
- closed warning distribution: `repeated_opening:3`;
- acceptance projection: `accept:1`; and
- no rejection code or stage exception.

This answers the prior causal question without authored prose or a workspace
path: two real polish attempts ran successfully and reduced, but did not clear,
the remaining deterministic concern.

### Macaron

The projected trace facts distinguish a different failure shape:

- polish attempt 1: `POLISH_ACCEPTED`, accepted and improved, 7 warnings;
- polish attempt 2: `POLISH_ERROR`, not accepted, `ValueError`;
- attempt 2 has no validation or lint report;
- final validation: `pass`, 0 errors and warnings;
- final lint: `warn`, 6 ordinary warnings;
- closed rejection distribution:
  `cross_card_exact_duplicate:1,multi_field_opening_template:1`; and
- acceptance projection: `reject:1`.

The trace therefore separates a structural stage exception from an ordinary
accepted-but-imperfect polish attempt and from the later deterministic
acceptance rejection.

## Replay matrix

| Case | Trace-only operational classification | Exact authority still required? |
|---|---|---|
| Two accepted polish attempts with residual findings | Yes: attempt states, accepted/improved flags, before/after counts, final validation/lint codes | Sealed result only for authoritative terminal disposition |
| Accepted polish then duplicate-field exception | Yes: second attempt is a typed error with no reports; final rejection codes remain distinct | Sealed result only for authoritative terminal disposition |
| Completed evidence awaiting adoption | Yes: custody/decision summary shows completed evidence; stage summary appears only after durable classification | Checkpoint only for disputed field-level binding or repair |
| Provider pending, due versus not due | Yes: lifecycle decision retains the exact due/not-due reason and selected command | Public inspection remains transition authority |
| Ambiguous submission after call entry | Yes: typed outcome/reason plus provider-I/O custody assertion | Dispatch result remains retry/create authority |
| Pre-provider refusal | Yes: typed refusal plus `not_attempted` assertion | Refusal result/grant history remains authority |
| Review publication with retained provider custody | Yes: state/decision custody counts plus publication outcome/cause and exact result/receipt joins | Result and receipt govern API disposition |
| Deterministic finalization failure before publication | Partly: exact exception class/fingerprint and absence of publication are visible | Yes, if determining whether publication survived or inspecting contradictory native bytes |

## Parser correction discovered by replay

The replay caught one observability-only defect: code-distribution values are
rendered as bounded semicolon/comma-delimited tokens, but the reporter's safe
token parser previously hashed those values. The parser now permits those two
delimiters, so operators see the closed code counts rather than an opaque hash.
This does not widen the set of accepted field names or expose finding prose.

## Remaining legitimate checkpoint uses

Checkpoint inspection remains appropriate for:

- exact field-level binding disputes;
- snapshot/journal integrity contradictions;
- determining whether an interrupted publication left a valid sealed artifact;
- historical runs produced before these events existed; and
- forensic reconstruction beyond the bounded public trace projection.

It should no longer be the first move for routine optional-stage exhaustion,
typed stage failure, due/not-due custody, refusal, ambiguity, or published
review-with-custody questions.

## Qualification

- Deterministic replay regression: 8 operational classes.
- Exact archive retrospective: Doughmeat and Macaron generation 11.
- Provider calls: 0.
- Network/R2 operations: 0.
- Retained QA mutations: 0.
- Protected prose/payloads emitted: 0.
