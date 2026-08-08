# AstroWoof Natal Authoring v0.2 Compatibility

`astrowoof-natal-authoring 0.2.0` is a dependency-free `py3-none-any` wheel
requiring Python 3.11 or newer. It was built and fully verified with CPython
3.12.13 on Windows. A Linux image must run the installed release smoke before
promotion because this sprint did not execute a Linux container smoke.

The supported public interfaces are the `astrowoof-semantic-closure`,
`astrowoof-build-natal-basis`, and `astrowoof-release-smoke` commands plus the
versioned JSON contracts in `contract-catalog.json`. Package-internal Python
modules are not a consumer API.

## Upstream and identity boundary

The qualified tuple is AGF 0.6, SPC 0.10, projected graph 1.3.0, and SBE 0.2.0.
The installed smoke uses the exact AGF/SPC wheel hashes recorded in the release
manifest and proves an opaque UUID source identity through claims, syntheses,
authoring state, delivery provenance, and installed-wheel output. The historical
`natal:<subject>` spelling remains accepted but is no longer required.

Preferred input is `astrowoof.projected_natal_input.v0.1`; the legacy projected
directory and unversioned params shapes are normalized. Unknown-time claim
suppression, variable basis sizes, Quick/Complete, hierarchy redesign, and
critic product policy are deferred and are not compatibility promises here.

## Durable boundary

Operator state is `astrowoof.semantic_closure_run.v0.9`; historical v0.2-v0.9
states are recognized, but legacy paid-provider runs without the evolved frozen
spend/profile state fail closed. The workspace must be restored at its recorded
stable logical absolute path with the complete validated snapshot boundary.
Incomplete or relocated snapshots cannot be resumed.

The API must distinguish public waiting, warning, review, budget exhaustion,
ambiguous submission, and delivery outcomes. Only `DELIVERY_COMPLETE` or an
explicitly supported delivery-with-warnings policy is promotable.
