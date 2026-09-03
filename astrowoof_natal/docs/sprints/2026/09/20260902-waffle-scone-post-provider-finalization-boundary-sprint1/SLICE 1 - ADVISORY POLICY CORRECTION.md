# Slice 1 — Advisory Policy Correction

Status: complete.

## Change

Final assembly no longer independently enforces the three distribution-only
theme policies:

- `theme_group_coverage`
- `theme_group_balance`
- `cross_section_theme_mirroring`

Those policies remain evaluated and retained by the shared pass/final
validation surface as advisories. Assembly continues to own structural joins:
registry shape and identity, field shape, story/section compatibility,
registered assignment IDs, duplicate assignment artifacts, and required
assignment-field completeness.

## Production-boundary result

The Waffle-shaped fixture now proves the complete supported path:

1. completed provider evidence is adopted;
2. pass 6's imbalanced distribution is accepted with an advisory;
3. the fan-in/adoption operation is durably consumed;
4. assembly and final validation pass;
5. delivery packaging completes; and
6. the public invocation publishes `delivery_complete` and exits zero.

A second fixture combines missing registered-group usage with cross-section
title mirroring and proves both remain advisories through successful assembly.
The unknown-assignment control still fails at pass acceptance.

## Contract impact

There is no lifecycle, authority, custody, provider, result-schema, or API
contract change in Slice 1. It removes contradictory native policy enforcement
and makes assembly agree with the already-published advisory classification.

The separate Slice 2 question remains: how a genuinely deterministic local
assembly contradiction should be sealed and exposed without inviting a retry
loop. Per API review, SBE must not broadly convert every `ValueError`, and API
must never infer disposition from exception text or process exit alone.
