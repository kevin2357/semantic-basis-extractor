# API review — Slices 4–6

## Decision

Slices 4's equivalence and isolation qualification is approved. The evidence
supports retaining the deterministic runner and checked-in classification
manifest as a safe, useful test framework. It does **not** support claiming a
whole-suite performance improvement or changing CI/default/release-playbook
execution today.

The final authority pair is particularly persuasive:

- one worker and two workers collected the same 1,115 tests with 58 skips;
- their exact inventory and outcome digests match;
- neither had failures, errors, or unexpected successes; and
- injected failures remained attributable to their exact shard and retained a
  usable reproduction command.

The credential sanitation, owned-root proof, protected unquiet observability
group, and serial treatment of build/release/installed-wheel authority are the
right safety boundaries. No API/SBE lifecycle, package, provider, or release
contract concern appears in this work.

## Required adoption posture

1. Do not make two-worker execution the broad-suite default or claim it speeds
   up this laptop: it was 126.279 seconds slower than the one-worker run.
2. Keep the serial installed-wheel, rebuild, package-inventory, qualification,
   and release-receipt gates as the only release authority.
3. Treat the coordinator and classification manifest as an opt-in diagnostic
   and growth framework until a separate duration-led campaign promotes enough
   provisional modules with repeated isolation/equivalence evidence.
4. If CI adoption is later proposed, require it to invoke this same checked-in
   manifest/coordinator rather than reproduce a different sharding rule in
   YAML. The aggregate must require every approved shard and serial tail.
5. Preserve the focused serial command as the universal fallback and exact
   shard reproduction commands as failure evidence.

## Slice 5–6 recommendation

Do not proceed with CI/default/release-playbook adoption under this sprint's
current performance result. Close this sprint as a successful framework and
qualification effort after the usual focused runner checks, broad serial gate,
diff/status review, and a concise maintainer note that parallel mode is
available for controlled experimentation but is not yet the faster standard.

Update Control Room issue #16 with the measured result and follow-on
duration-led provisional-promotion campaign. No SBE package release is needed
for test-only tooling unless future work changes packaged behavior or resources.
