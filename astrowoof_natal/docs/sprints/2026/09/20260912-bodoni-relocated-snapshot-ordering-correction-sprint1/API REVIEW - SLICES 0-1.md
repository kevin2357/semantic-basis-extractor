# API review — Slices 0–1

## Verdict

**Approved for Slice 2 package qualification.**

The evidence correctly isolates a host-path ordering defect rather than
archive, snapshot-content, relocation-authority, or API custody drift. The
selected canonical ordering is appropriately narrow and compatible:

- derive workspace-relative POSIX paths first;
- sort by case-sensitive `PurePosixPath(relative).parts`;
- retain strict ordered inventory comparison after canonicalization; and
- preserve historical Linux-authored manifest order rather than silently
  rewriting historical snapshots into a new plain-string order.

That last point matters: a plain POSIX string key would have introduced a new
ordering at the directory-versus-same-prefix-`.zip` boundary. The component
tuple instead re-establishes the existing durable order independently of the
restore host.

## Required package gate

Before release lock, use the private retained Bodoni archive/local restore from
`BACKGROUND.md` to prove the exact public relocated reader:

1. accepts the authority/workspace pair and produces a valid wrapper;
2. keeps all 387 restored files byte-identical before and after the read; and
3. performs zero provider or storage I/O.

API will then repeat public reader/pair intake using the qualified wheel against
the same local copy. No additional R2 read is authorized or needed.

No API contract or schema change is required by this native ordering repair.
