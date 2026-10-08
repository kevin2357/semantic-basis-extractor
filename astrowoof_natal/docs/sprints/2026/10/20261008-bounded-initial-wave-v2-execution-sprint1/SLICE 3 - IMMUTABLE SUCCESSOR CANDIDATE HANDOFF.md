# Slice 3 — Immutable successor candidate handoff

## Disposition

Gate C approved the bounded initial-wave v2 command.  The temporary `0.4.71`
wheel used to prove that command is not a candidate for API admission: it was
built before the Gate C fixes were committed and cannot carry a new immutable
profile identity.

This slice therefore prepares a distinct `0.4.72` candidate.  It does not
rewrite either historical bounded bundle:

| Record | Disposition |
| --- | --- |
| `astrowoof.bounded_natal.live.stable_facts.v1` | retained historical `0.4.70` profile |
| `astrowoof.bounded_natal.live.stable_facts.v2` | retained historical `0.4.71` profile |
| `astrowoof.bounded_natal.live.stable_facts.v3` | new initial-wave-v2 candidate profile |

The prompt assets themselves are unchanged.  A separate prompt-release v3 is
nevertheless required because a prompt release's profile allowlist is part of
its sealed identity; v2 must not be mutated to point at v3.

## Successor static identities

| Surface | Immutable value |
| --- | --- |
| SBE package version | `0.4.72` |
| Bounded profile | `astrowoof.bounded_natal.live.stable_facts.v3` |
| Profile version | `3.0.0` |
| Profile SHA-256 | `5ccdbac1d8b81b9099fa7689f08460c30a2563192b4c766587ea190bfb05caed` |
| Prompt release | `astrowoof.authoring.bounded_stable_facts.v3` |
| Prompt release version | `3.0.0` |
| Prompt release SHA-256 | `737bb2cb64e426b281a12a88578b7831473b228d2b40a7fdb2c8c7ad5fa1b0e6` |
| SBE worker descriptor SHA-256 | `440d4475d4b746833f45bc9a4efc53d220fca636476ca6f8d626f4259b201cf8` |
| Processing-profile catalog SHA-256 | `039fd08ea77f105cb52ae9376e7e3907b3ff130d258f6afccafc375f609d1982` |
| Prompt-release catalog SHA-256 | `d827e2d7cc1aa7fbc4c4f62b3624dda0d30b7afce6bd709bac71523d6006851e` |
| Required SPC distribution | `semantic-projection-core==0.11.1` |

The v3 profile retains the bounded route contract
`astrowoof.bounded_natal.authoring_run.v2`, stable-facts-only policy, four
projection contexts, and the exact v2 stage-prompt/workspace-component
inventory.  Its only semantic successor change is binding that immutable
configuration to the package that contains the approved v2 initial-wave
command.

## Candidate procedure

1. Commit this exact source state.
2. Build the `0.4.72` wheel twice from that committed archive with the release
   epoch; require byte equality.
3. Install only that wheel into an isolated target and rerun the bounded
   public-command success, exact-replay, and pre-provider-refusal fixture.
4. Record the exact wheel path, source commit, whole-wheel SHA/size, package
   descriptors, and raw fixture locations for API's installed-wheel Gate D.

No package publication, tag, deployment, profile activation, workspace
mutation, or provider operation is part of this candidate handoff.
