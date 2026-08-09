# AstroWoof Natal Authoring 0.2.1 Compatibility

`astrowoof-natal-authoring 0.2.1` is a dependency-free `py3-none-any` wheel
requiring Python 3.11 or newer. The exact candidate passed installed smoke on
CPython 3.12.13/Windows and CPython 3.11.15/Linux amd64.

The supported commands and versioned JSON contracts are unchanged from 0.2.0.
The qualified upstream tuple remains AGF 0.6.0, SPC 0.10.0, projected graph
1.3.0, and pyswisseph 2.10.3.2 where live AGF calculation is required. Opaque
UUID source identity and the historical accepted `natal:<subject>` spelling
retain their 0.2.0 behavior.

Production orchestration, spend authorization, public run state, provider
disclosure, workspace snapshots, evidence provenance, and delivery schemas are
byte-for-byte the packaged 0.2.0 contracts. No API integration or database
migration is required when replacing 0.2.0 with 0.2.1.

The fake provider remains a non-production selectable route. Its authored
placeholder wording is not a compatibility surface, but its determinism and
ability to satisfy production normalization are now portable across supported
path behavior. Failed release-smoke JSON has been extended with original QA
status and an explicit skipped-cleanup result; consumers should continue to
gate promotion on top-level `status: pass` and `DELIVERY_COMPLETE`.
