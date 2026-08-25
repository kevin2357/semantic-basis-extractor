# API Agent Plan Review

Date: 2026-08-25  
Verdict: approved to begin Slice 0

The revised plan correctly narrows the suspected issue: due retrieval already
precedes a prepared action, while scheduled/not-due custody and completed evidence
needing local fan-in may not. Treating this as a full precedence audit rather than
flipping one condition is the right scope.

## Responses to Slice 0 questions

1. **Local work versus external authority.** Retained provider custody must always
   precede external authority: due reconciliation, coherent not-due scheduling,
   and required completed-provider fan-in. Other local work should precede a new
   authority only if it can determine, alter, or refuse the exact next paid-action
   inventory. This avoids both unsafe authority publication and accidental
   starvation by unrelated optional work.
2. **Versioning.** Prefer strict in-place v0.5/v0.6 semantic hardening if current
   fields can express the corrected disposition. Add a new public version only if
   a consumer cannot distinguish a corrected result using existing closed fields.
3. **Nonblocking critic custody.** It may not suppress already-publishable
   delivery, but it remains retained provider custody and should suppress an
   unrelated later optional provider authority unless that authority is proved
   independent and the contract explicitly supports coexistence. The default is
   custody-first, delivery-independent—not authority-independent.
4. **Reasons and diagnostics.** Preserve current public reason vocabularies where
   they remain semantically sufficient. Add redacted structured diagnostics
   (custody counts, due/not-due counts, prepared deferment, selected subset digest,
   and branch) rather than inventing a public state for observability alone.
5. **Frozen cohort.** Keep recovery entirely separate. The patch qualification must
   access neither frozen QA workspace nor provider state.

## Additional gates

- The Slice 0 reproducer must assert that a not-due mixed state returns a
  nonmutating scheduling/deferment result—not a generic external-authority wait.
- The completed-evidence fan-in row should assert no new authority request before
  fan-in emits its new checkpoint basis.
- The exact next-action inventory/request digest must be unchanged by time-only
  not-due observation; a new basis may change it only through recorded fan-in.
- API needs no code change merely to consume a corrected selector, provided the
  existing inspection/temporal schemas carry the corrected command and
  `not_before` semantics.

Slice 0 may proceed provider-free. Pause at its planned API gate before changing
semantic validation or lifecycle selection.

