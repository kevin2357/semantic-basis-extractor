# API final review — SBE 0.4.59 release lock

## Decision

API technical review approves owner publication of the qualified SBE `0.4.59`
artifact, subject to the stated immutable tag and wheel fence.

## Exact artifact reviewed

- Release-lock/tag target:
  `e5127caea466b12340472eee48b2563abfd68650`.
- Required component tag:
  `astrowoof-natal-authoring-v0.4.59`.
- Exact qualified artifact SHA-256:
  `9211b7a7fd2e1a10a42cfe6bf47cafd749fa2076767b2dd7500621a93d9cbe92`.
- Exact qualified artifact byte size: `1,376,264`.

The initial API-side local rebuild differed by one byte because it used a
different packaging toolchain. SBE retained the actual qualified candidate and
supplied its stable local handoff path. API independently recomputed the
candidate's SHA-256 and byte size; both match the release-lock qualification.

## API/SBE installed-wheel consumer gate

API ran its provider-free executable release-pair qualification against the
exact retained candidate, using a qualification-only manifest bound to API
revision `e21934f38e9636645420d60b99e28eed7ebae718` and declaring SBE `0.4.59`.

Result:

```text
status=pass
result=api_sbe_executable_contract_qualified
provider_free=true
provider_operations=0
provider_spend_usd=0
sbe_wheel_version=0.4.59
sbe_wheel_sha256=9211b7a7fd2e1a10a42cfe6bf47cafd749fa2076767b2dd7500621a93d9cbe92
```

The gate exercised installed public qualification commands from the wheel and
validated the API/SBE lifecycle contract pair. It did not access QA, R2,
providers, or retained workspaces.

## Integration assessment

The producer change supplies the exact missing same-invocation terminal command
evidence for both detached `review_required` and fresh `delivery_complete`
publication. It aligns with API's already-implemented fresh delivery authority
ingress and the pending detached review exit-3 consumer correction. It does not
broaden source-of-truth discovery, provider authority, or observer transport
semantics.

## Publication fence

Tag only `e5127caea466b12340472eee48b2563abfd68650` and upload only the exact
reviewed bytes. The GitHub asset must use the valid canonical wheel filename:

```text
astrowoof_natal_authoring-0.4.59-py3-none-any.whl
```

The retained local filename contains an additional provenance segment and is
not accepted by `pip` as a wheel filename; renaming the same verified bytes for
publication is required and does not create a substitute artifact.
