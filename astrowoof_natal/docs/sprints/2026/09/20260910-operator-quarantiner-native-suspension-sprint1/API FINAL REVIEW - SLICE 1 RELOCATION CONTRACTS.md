# API final review — Slice 1 relocation contracts

**Approved.** The two required mechanical corrections are present and covered:

- Windows drive-relative `C:` is refused; only a normalized absolute `C:/...`
  root enters the Windows canonicalization path.
- The input now rejects all ASCII control characters, including embedded tab,
  escape, and delete, rather than only NUL/line boundaries.

The paired authority/wrapper validator and lexical-only root normalization keep
the API/SBE join independent of local filesystem existence. Slice 1 is closed;
SBE may proceed to the dedicated read-only relocated reader and capability-fence
tests.
