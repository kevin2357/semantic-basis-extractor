# Slice 0 — request for retained checkpoint coordinates

## Purpose

The owner has explicitly authorized exact read-only inspection of the relevant
Diffie and Hellman R2 workspaces. Per the approved evidence protocol, SBE still
needs an API-owner-produced coordinate packet naming the two exact objects before
issuing any `HEAD` or `GET`. SBE will not discover them through bucket or prefix
listing.

## Requested closed packet

Please provide one JSON document with an exact entry for each native run:

- label: `Diffie` or `Hellman`;
- API run ID;
- native run ID;
- exact R2 object key;
- object version/generation identifier when the store exposes one;
- expected object byte length;
- expected ETag/checksum and archive SHA-256;
- native checkpoint/snapshot generation and full snapshot SHA-256;
- logical workspace root;
- snapshot inventory/archive member identity when separately known;
- SBE release, worker image digest, compatibility/profile identity, and provider
  mechanism;
- checkpoint sealed/published timestamp; and
- the authoritative API record/export identifiers that establish this object was
  the active checkpoint for the incident invocation.

The packet should contain no credentials, signed URL, prompt, authored content, or
provider payload. Please publish its own SHA-256 alongside it.

## Helpful API join evidence

If available without broadening access, include or separately provide sanitized
immutable exports for:

- the rejected Diffie lifecycle inspection or its exact stored digest and all
  consumer-critical branch/capacity/dependency fields;
- the Hellman lifecycle/request/refusal invocation records for the first refusal
  and one exact replay;
- exact native action/binding joins for the creative-retry provider operations;
- the providerless Hellman action's API admission/authorization and any persisted
  SBE request/grant/document identities;
- command arguments by contract identity/digest, without filesystem secrets; and
- API job/lease/capacity dispositions immediately before and after each relevant
  invocation.

Later API settlement/reporting facts must be timestamped separately and must not
be embedded as if they were members of the earlier native checkpoint.

## Authorized access after delivery

For exactly the two supplied checkpoint keys, SBE may perform:

- one exact metadata `HEAD` per object; and
- one exact object `GET` per object.

No R2 list, prefix discovery, write, copy, restore-in-place, repair, mutation, or
provider operation is authorized. Downloaded bytes will be held in a fresh
temporary directory, validated before interpretation, and removed after sanitized
evidence products and hashes are complete.
