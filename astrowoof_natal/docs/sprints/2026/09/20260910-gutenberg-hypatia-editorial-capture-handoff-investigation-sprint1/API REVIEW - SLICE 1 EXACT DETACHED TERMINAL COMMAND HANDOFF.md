# API Review — Slice 1 Exact Detached Terminal Command Handoff

## Decision

The correction is approved in principle. It supplies the exact
same-invocation identity that both the terminal-review observer and successful
delivery publication need, without weakening detached nonterminal behavior or
introducing discovery.

## What is correct

- The handoff is built only from the `sealed` result/receipt returned by the
  very invocation that published it.
- It emits the pre-existing closed v0.1 terminal-review or terminal-delivery
  command, rather than a new ad hoc shape.
- `provider_pending` and other nonterminal outcomes emit nothing.
- The callback placement before the ordinary reconciliation output preserves
  both the command evidence and the established detached cycle result.

## Required focused regression before package qualification

Please add one subprocess/CLI-level regression for the original Gutenberg
shape: a detached provider-reconciliation terminal review that exits with the
ordinary review-required exit convention and writes JSONL through
`output_result`. Assert that stdout contains exactly one valid
`astrowoof.terminal_review_command_result.v0.1` with the same
invocation/result/receipt identity as the just-published native result, plus
the ordinary reconciliation result; assert that a nonterminal detached exit-3
case still contains no terminal command.

The existing direct callback tests are valuable but cannot prove the
stdout-serialization seam that caused the live miss. The same CLI-level test
may also cover fresh delivery if it stays small; otherwise its current focused
callback/contract coverage is adequate pending API consumer work.

## API ownership remains

API must separately accept the terminal-review command on that detached exit
convention, establish delivery authority before its first publication attempt,
and carry—not rediscover—the identity through a retry. This SBE correction
does not itself make either Better Stack post occur.

