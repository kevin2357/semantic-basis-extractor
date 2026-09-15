# API review — 0.4.63 pre-tag installed-wheel consumer gate

## Decision

**Technical approval granted for owner authorization to create the immutable
`astrowoof-natal-authoring-v0.4.63` tag and publish the exact qualified wheel.**

This is a provider-free API/SBE compatibility gate only.  It made no live API,
queue, R2, provider, retained-workspace, or deployment mutation.

## Exact candidate bound

| Field | Verified value |
| --- | --- |
| Immutable tag target | `ceb0dc5a28b81cff91a4a985edb4cf6ff3217e24` |
| Candidate wheel | `astrowoof_natal_authoring-0.4.63-py3-none-any.whl` |
| Retained source artifact | `C:\\dev\\github\\semantic-basis-extractor\\.release-work\\0.4.63\\lock-final-a\\dist\\astrowoof_natal_authoring-0.4.63-py3-none-any.whl` |
| Byte size | `1,385,639` |
| SHA-256 | `fe0fba0c0be87ec25257a9b9c8c5f6e0166f9544df99fc8f940b20109ea1e355` |

API independently checked the retained artifact’s byte size and SHA-256 before
installing it with `--no-deps` into an isolated temporary target.  The API’s
normal installed SBE package remained untouched.  The consumer process used
that isolated target plus the current API source tree.

## Provider-free API consumer results

All nine public installed-wheel consumer qualifications passed against the
exact artifact above:

1. external-authority v1;
2. external-authority v2;
3. provider-dispatch result;
4. final-QA mixed custody;
5. temporal lifecycle;
6. post-fan-in lifecycle v2;
7. ordinary-v2 happy path;
8. providerless-denial settlement; and
9. polish-authority handoff.

Every receipt that carries `sbe_version` reported `0.4.63`; all cells carrying
the wheel identity reported the exact SHA-256 above.  The temporal and
post-fan-in legacy receipts do not emit a version field, but did bind the same
exact wheel SHA.

## Scope note

This gate validates API’s public consumer compatibility with the candidate. It
does not replace SBE’s documented source, cross-runtime, reproducibility, and
installed-wheel qualification.  Those release-lock gates remain the owner’s
basis for final tag/publish authorization.
