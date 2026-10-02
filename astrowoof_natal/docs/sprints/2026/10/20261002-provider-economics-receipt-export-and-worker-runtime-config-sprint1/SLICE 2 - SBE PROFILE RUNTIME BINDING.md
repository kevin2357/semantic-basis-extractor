# Slice 2 — SBE profile runtime binding

**Status:** implemented and provider-free qualified; Slice 3 prompt execution remains next.

## Delivered boundary

The semantic-closure CLI now accepts an exact four-reference API handoff:

- processing profile ID;
- processing profile SHA-256;
- immutable API generation-manifest SHA-256; and
- route family.

It accepts either all four references or none.  In the profile-aware path it
loads SBE's packaged catalog itself, recomputes/validates the installed profile
and referenced prompt release, verifies the SBE worker package descriptor, and
uses only the deployed `ASTROWOOF_ENVIRONMENT` value for the profile's allowed
environment check.  No profile JSON, prompt text, workspace path, secret, or
provider authority crosses the handoff.

The resolved safe binding is durable in `run.json` and creation provenance.
The ordinary authoring profile also includes it, so existing action and
authority bindings inherit its immutable digest rather than silently using a
current default.  A profile-bound resume must repeat the exact same binding;
a missing or changed binding is refused before provider construction.

Profile-owned authoring settings are applied after argument parsing.  Thus a
caller cannot alter the selected profile's provider route, models, retries,
concurrency, basis format, selection policy, optional stages, or transport
settings with ordinary CLI flags.

## Provider-free evidence

`test_processing_profiles_slice1.py` now covers the exact installed
SBE-role package check and negative digest/version cells.  New
`test_processing_profile_runtime_slice2.py` proves all-or-none handoff
handling and replacement of deliberately contradictory CLI settings.  Both
are listed in `tests/test_suite_manifest.json`.

Command run:

```text
PYTHONPATH=astrowoof_natal/src python -m unittest discover -s astrowoof_natal/tests -p 'test_processing_profile*.py'
9 tests passed
```

This is deliberately not the joined API installed-wheel replay.  That is Gate
C after API emits and verifies the matching persisted envelope.
