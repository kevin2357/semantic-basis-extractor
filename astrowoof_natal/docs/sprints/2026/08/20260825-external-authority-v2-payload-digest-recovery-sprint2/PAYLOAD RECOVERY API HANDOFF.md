# External-Authority v2 Payload Recovery — API Handoff

Status: implementation and installed-wheel qualification complete; release review pending

## Supported correction

New ordinary provider requests persist their exact private request object before
external authorization. The native ledger action owns the sole content reference:

- artifact schema identity;
- stable logical path beneath the restored run workspace;
- exact file SHA-256;
- canonical complete-request SHA-256; and
- canonical JSON representation identity.

The resolver validates the complete workspace snapshot, joins the requested action
to exactly one ledger member and binding, follows only that reference, and requires
the complete request digest to equal `binding.request_sha256`. It never recursively
searches for payload candidates. The full payload remains private native evidence;
it is not projected into lifecycle inspection, events, logs, fixtures, or results.

## Narrow 0.4.23 compatibility adapter

Historical rebuild is supported only for an exact-Natal interactive
`creative_retry` created by SBE 0.4.23 under run schema v0.9. It additionally
requires:

- an immutable prior `pre_provider_refusal /
  request_payload_digest_mismatch` record for the exact action;
- the fresh action to be history-bearing providerless `PREPARED` work;
- exact retained route, attempt, action, profile, provider configuration, source
  archive, source-workspace, prior-feedback, runtime, and resource-set identities;
- the retained source archive to resolve beneath the restored logical workspace;
- exactly one expected placeholder at the exact redacted-request location;
- the rebuilt flattened prompt to equal the retained UTF-8 prompt; and
- both the rebuilt redacted object and complete-request digest to match retained
  native evidence.

Missing, external, malformed, incompatible, or contradictory inputs fail closed
before provider create. Literal redacted-JSON-plus-prompt reattachment is not a
supported reconstruction method. Historical bounded reconstruction is not
supported; bounded work already retained complete direct request evidence.

## Recovery sequence for the retained runs

1. Install and attest the fresh released wheel at the stable logical workspace.
2. Restore and validate the complete exact snapshot.
3. Read a fresh temporal lifecycle inspection and v2 external-authority request.
4. API makes a fresh authority decision and supplies a new exact v2 grant and
   ordinary authorization document. Never reuse the refused grant.
5. Invoke the supported `astrowoof-external-authority-v2` command.
6. A successful create records its provider identity durably and detaches into the
   ordinary reconciliation-only lifecycle. Replaying the same invocation cannot
   create again.
7. API retains the old refusal and new grant/result as separate audit facts.

No SBE result asserts API-global reservation, capacity, lease, admission, or billing
facts.

## Installed-wheel qualification

Run:

```text
astrowoof-payload-recovery-qa --output payload-recovery-receipt.json
```

The command is self-contained and accepts no provider credentials, production
inputs, run directory, grant, or payload. It constructs a sanitized historical
workspace and proves:

- the real lossy artifact refuses with `request_payload_digest_mismatch` and
  `not_attempted`;
- old refusal replay performs no create;
- fresh inspection/request/grant is distinct;
- deterministic rebuild reaches exactly one scripted create;
- fresh replay performs no second create; and
- refusal history remains immutable.

The receipt schema is
`astrowoof.external_authority_v2_payload_recovery_qualification.v1`. The receipt is
qualification evidence only and is never execution, lifecycle, spend, or delivery
authority.
