# API review — Slice 1 and qualification block

## Decision

Slice 1 is approved as implemented.  The live
`editorial_review_contracts._resource_bytes()` correction is narrow,
byte-preserving, and correctly covered on the declared Python minimum and the
existing 3.12 qualification runtime.

The current release must **not** advance to a candidate wheel or Gate B while
the broader editorial-contract suite still has eight Python 3.11 errors at the
known `editorial_review_fixtures.py:628` call site.

## Evidence assessment

- The live helper alone changed, as approved.
- Its direct tests pass on CPython 3.11.15 and 3.12.14.
- It preserves the expected resource bytes/digest and `FileNotFoundError` for
  a missing resource.
- The broader 3.12 suite remains green.
- The broader 3.11 suite independently confirms the next inventoried
  incompatibility instead of concealing it.

That last result validates the scope fence and is a release-quality signal, not
a reason to weaken the minimum-runtime gate.

## Next step and relationship to Control Room work

Proceed via the separate Control Room child [#23 — Python 3.11 packaged-resource
traversal compatibility sweep](https://github.com/kevin2357/astrowoof-api/issues/23).
Create a companion, separately reviewed SBE sweep record that:

1. begins with `editorial_review_fixtures.py` because it blocks the current
   qualification;
2. separately assesses `resource_access.py` and then every remaining inventoried
   call, including the starred form, with real callers/resources;
3. proves each change selects identical bytes and preserves missing/malformed
   failures on Python 3.11 and 3.12; and
4. completes the required Python 3.11 qualification before this live-defect
   sprint resumes at Slice 2.

The sweep is now release-blocking in practice, but it remains a distinct scope:
do not silently fold broad changes into Slice 1 or claim a partial candidate is
qualified.  No API, packet, schema, lifecycle, transport, Better Stack, or
Alloy change is implied.
