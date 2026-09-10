# API re-review — Slice 1 canonical root and pair validation

The requested correction is substantively incorporated: root identity is now
platform-independent and lexical, and
`validate_relocated_assessment_pair()` restores the authority/wrapper/freshness
join at API intake. That is the right shape.

Two tiny implementation/documentation mismatches should be corrected before
the reader slice starts:

1. `canonical_logical_root()` currently accepts `C:` as a Windows root because
   the drive regex makes the slash optional. On Windows that spelling is
   drive-relative, not an absolute root, and Slice 1 expressly says relative
   paths are refused. Require `C:/...` after separator normalization; retain
   `C:/` as the actual drive-root spelling.
2. The documentation says control characters are refused, but the current
   check rejects only NUL (and CR/LF incidentally). Reject every ASCII control
   character in both the full value and every segment, including embedded tab
   or escape characters.

Please add focused cases for both. With those two mechanical corrections, API
approves Slice 1 and the relocated-reader implementation can proceed.
