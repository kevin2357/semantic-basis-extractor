# AstroWoof Natal Authoring 0.4.17

Status: qualified for immutable publication

SBE 0.4.17 is a narrow provider-reconciliation integrity patch over 0.4.16.

Before selecting or retrieving any due provider operation, SBE validates the
complete retained provider-backed action inventory against the native run identity
and closed public binding contract. Any contradiction refuses the whole cycle with
`review_required`, performs zero GETs, publishes no native transition, and leaves
the authoritative workspace unchanged.

The exact diagnostic reason is emitted as the redacted, failure-isolated
`execution.failed` event reason `provider_binding_integrity_mismatch`. The closed
reconciliation result continues to expose `review_required` as its authoritative
machine-readable outcome; diagnostic events and text logs are not authority.

No authoring, scoring, prompt, delivery, spend-authority, provider-submission, or
public lifecycle-state behavior changed.

## Qualification

- Artifact source commit: `6da874eb52934ad259048c1ca8abb90238df828d`.
- Fixed build epoch: `1787589134`.
- Two byte-identical wheel builds.
- Complete source suite: 593 passed, 30 existing environment/opt-in skips.
- Installed bridge qualification: 10 passed.
- Installed release smoke: pass.
- External provider/network calls: 0.
- Provider POST/create/submit/retry calls: 0.
- Spend: USD 0.
- Retained Aster workspace access: 0.

