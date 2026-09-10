# API review — Slice 1 relocation authority and wrapper contracts

## Result

The additive contract surface, closed schemas, negative capability assertions,
canonical JSON digesting, and ordinary-reader non-regression are all on the
right path. The reader remains absent, so no relocation authority has yet
expanded any executable/mutating surface.

One small correction is needed before treating the root digest as frozen
cross-package identity:

## Required correction — make root canonicalization real

`canonical_root_sha256()` currently hashes an input string after only basic
nonempty/whitespace checks. Its docstring says “already-canonical normalized,”
but neither the function nor its schema contract establishes what canonical
normalization is or rejects a noncanonical spelling.

That is insufficient for the API/SBE join because equivalent path spellings
could hash differently (separator style, drive/case conventions, redundant
components), while a future implementation might accidentally normalize on one
side only.

Before the reader slice, please do one of these explicitly:

1. invoke the established workspace-contract logical-root canonicalizer and
   reject `value` unless it already equals that canonical representation; or
2. introduce a small shared, platform-independent logical-root canonicalizer,
   use it for both authority construction and reader comparison, and lock it
   down with Windows/POSIX-style fixture cases.

Do not use ambient filesystem resolution for this identity: the original root
need not exist on the assessment host, and the restored root is intentionally
at another physical location.

The authority should continue to carry only the digest, never the raw root.

## Pair validation note

`validate_relocated_assessment()` correctly validates wrapper shape/digest and
the nested v1 assessment, while `build_relocated_assessment()` enforces the
authority window. The future API consumer must validate the wrapper together
with the exact persisted authority before accepting it, so the authority
digest, request/checkpoint binding, and `issued_at <= assessed_at <= expires_at`
relationship are all re-established at the durable boundary. Please make that
paired-validation requirement explicit in the Slice 2 reader/API handoff.

Once root canonicalization is corrected and covered, API approves proceeding to
the read-only relocated reader and its capability-fence qualification.
