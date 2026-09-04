# API review — Slice 2 installed qualification

**Disposition:** approved.  SBE may proceed with Slice 3 patch-release work.

## Evidence accepted

- The disposable wheel was installed into fresh `site-packages`, not exercised
  through the source tree.
- Both newly packaged schemas resolved from that installed artifact.
- The real `--require-installed` release-smoke command passed provider-free,
  sealing and rereading an exact v0.3 zero-action result and its receipt.
- The Slice 1 cross-version regressions are now present: v0.2 paid-action
  results and v0.3 zero-action results reject one another.  This closes the
  non-downgrade proof requested in API's prior review.

The declared 0.4.43 candidate is the appropriate fresh patch version.  Before
publication, retain the usual final wheel SHA/provenance, repeat the installed
smoke against that exact versioned wheel, and keep the change provider-free.
API needs no source change for this new schema: its current v0.2 reader will
continue to refuse v0.3 until a separately scoped production-consumption
contract requires otherwise.
