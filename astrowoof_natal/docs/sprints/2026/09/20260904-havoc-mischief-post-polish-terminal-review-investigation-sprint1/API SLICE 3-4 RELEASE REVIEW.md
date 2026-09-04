# API Slice 3–4 release review

## Disposition: one small correction, then approved for release

The implementation is correctly narrow and is the appropriate native/package
release scope.  It removes only dormant theme-group evaluation from the copied
final-validator source, keeps legacy representations structurally tolerated,
and proves the handoff-bundle subprocess—not merely an imported module—has the
same behavior.  The retained non-theme context-filter failure is the right
negative control.  No API, lifecycle, provider, custody, or retained-QA change
is indicated.

## Required small correction

`--allow-theme-group-edits` is described as a parser-compatible no-op, but it
is still included in the authoring-phase `any([...])` guard that raises
`parser.error` for polish overrides.  Therefore an otherwise-valid authoring
invocation that merely carries the historical flag changes from success to
failure; that is not a literal no-op.

Please remove `args.allow_theme_group_edits` from that phase guard and add a
small regression proving the flag is accepted in both `authoring` and `polish`
without changing validation results.  It may remain present in the emitted
diagnostic report as supplied-invocation provenance, provided it remains
non-authoritative and does not alter errors, warnings, or edit-lock behavior.

After that correction, API approves tagging and releasing this package-only
change.  No API ingestion work is required beyond the ordinary dependency
version rollout when the release is available.
