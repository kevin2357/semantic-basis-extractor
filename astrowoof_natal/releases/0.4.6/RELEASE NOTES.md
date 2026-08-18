# AstroWoof Natal Authoring 0.4.6 Release Candidate

Status: published under immutable tag `astrowoof-natal-authoring-v0.4.6`

## Summary

SBE 0.4.6 is the recommended fresh immutable release for bounded-Natal editorial
topology and provider-transport parity. It does not alter the published 0.4.5
artifact or tag.

The release adds:

- the same quality-preserving five card passes plus one summary/theme pass for
  bounded Natal;
- bounded interactive actions bound independently by pass and attempt;
- bounded Batch initial and creative-retry rounds with one paid action/API
  reservation unit per round and member-level audit evidence;
- pass-local retry without regenerating accepted passes;
- strict lifecycle/custody/cost handling for bounded Batch;
- packaged route-parity oracle v2 and bounded consumer traces; and
- strict public readers plus the provider-free
  `astrowoof-route-parity-evidence` CLI.

Initial and retry request semantics are transport invariant. Polish, qualitative
critic, and qualitative candidate remain interactive Responses operations in this
release, even after Batch initial authoring.

## Release gate

The earlier reproducible `0.4.5`-named candidate remains qualification evidence
only. Kevin authorized the fresh 0.4.6 version bump, exact final rebuild, installed
Windows/Linux gates, immutable tag, and publication.

The final wheel is 800,957 bytes with SHA-256
`1770d5c361b81ac5ed90b5b1a825da70aec108a665ac251a13a520d1af66e788`.
Two fixed-epoch builds were byte-identical. Exact installed Windows and Linux gates
passed without provider calls or paid spend.

Publication is complete. Post-publication evidence includes authenticated asset
re-download verification against the same SHA-256.
