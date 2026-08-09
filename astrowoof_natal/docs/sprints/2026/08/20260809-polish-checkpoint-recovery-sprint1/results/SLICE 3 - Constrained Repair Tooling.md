# Slice 3 - Constrained Repair Tooling

Status: complete; gate approval pending.

## Result

The package now exposes `astrowoof-repair-polish-checkpoint`, a dry-run-first
inspection and repair command limited to the proven SBE 0.2.1 polish-boundary
shape. It has no force, arbitrary allowlist, relocation, or generic rehash
mode.

Eligibility requires the affected v0.9 run and v0.1 authoring profile, stable
logical absolute path, awaiting-authorization state, missing subject mapping,
and exactly three changed final members. The current final deck, validation
report, and lint report must each be byte-identical to retained polish
attempt-1 output. All other snapshot members must match.

The command also proves:

- attempt 1 is reported with one matching ledger, marker, and response ID;
- reported usage and estimated spend exist;
- attempt 2 is exactly `PREPARED`, with no authorization, consumption,
  provider identity, or reported usage;
- the retained attempt-2 request hashes to the prepared binding; and
- the external authorization schema, action ID, and complete binding match.

Apply additionally requires a separate byte-identical complete backup and an
API-owned exclusive-lease reference, then acquires SBE's spend-consumption
lock. SBE records the lease reference for audit; the API remains responsible
for preventing other worker mutation under its authoritative lease.

The repair reconstructs the missing state-owned subject and attempt-1 record as
`POLISH_IMPROVED_PARTIAL`, preserving that it was not accepted and that attempt
2 remains necessary. It preserves the existing passes and spend ledger,
persists operator/public/authorization state, publishes a complete snapshot,
and validates the result before returning success. The external authorization
is evidence only: it is neither installed nor consumed.

The machine-readable report records before/after snapshot hashes, run revision,
accepted-pass and ledger digests, the three proven member hashes, response and
action identities, backup path, and exclusive-owner reference. Reports are
required to live outside the repaired workspace.

## Refusal qualification

Synthetic tests prove refusal for:

- missing or additional authoritative members;
- a retained attempt artifact altered independently of its final copy;
- inconsistent provider response identity;
- mismatched external authorization binding;
- an authorized or otherwise non-prepared next action;
- a missing or non-identical complete backup; and
- any mismatch set other than the exact three supported final members.

## Verification

- Repair inspection/apply/refusal tests: 8 passed.
- Repair, spend, and semantic-closure focused suites: 97 passed.
- Complete deterministic repository suite: 165 passed in 81.479 seconds.
- `git diff --check`: pass.
- OpenAI requests, incremental spend, and authorization consumption: zero.
- Retained acceptance run mutation: none.

Next action: approve the command and documentation before any inspection or
repair is run against a copy of the retained acceptance workspace.
