# API review — Slice 1ε executable contract

## Decision

**Approved.** Slices 1ε.0–1ε.2 correctly turn the jointly adopted editorial
packet contract into a package-owned, provider-free validation foundation.

The proposed API transport policy is also approved as recorded: canonical
JSON/UTF-8, deterministic gzip (`level=9`, `mtime=0`, no filename/comment/
extra), no more than 99 atomic editorial events, and a **9 MiB compressed safe
threshold** beneath the verified 10 MiB receiver ceiling. It remains an
API-owned preflight rule: SBE may carry and fixture it, but cannot make a live
transport, lifecycle, custody, or terminalization decision from it.

## Evidence accepted

- The semantic manifest binds all eleven closed schemas by digest, separates
  native, joint-fixture, and API-transport ownership, and makes unknown roots,
  versions, rules, and incomplete semantic stages fail closed.
- The two synthetic positive lineages are deliberately distinct and useful:
  accepted delivery proves real post-initial adoption and delivery continuity;
  editorial closeout proves retained terminal selection without inventing a
  delivery. Both preserve terminal-owned validation as a separate owner form.
- The 24 rehashed mutation cases exercise the hard relationships rather than
  relying on shallow malformed input: chronology, continuity, response/action
  joins, finding/validation ownership, terminal selection, projection set,
  artifact scope, summaries, and envelope-native digest binding all receive
  typed failures with safe detail codes.
- The no-side-effect boundary is appropriately aggressive for this layer:
  package fixtures/resources and in-memory validation only, with socket and
  subprocess construction fenced. This is exactly the right boundary before a
  future runtime builder is introduced.
- I independently ran the three editorial-contract test modules in the
  supported source layout: **23 passed, 1 expected optional `jsonschema`
  skip**. The implementation-surface diff hygiene check is clean.

## Fences retained

- This approval does **not** authorize a runtime packet builder, retained-run
  inspection, R2/API/Better Stack/provider/network work, installed-wheel
  qualification, release, or a live capture write.
- API will validate and construct its own observation envelope, add its own
  correlations, and apply the 9 MiB / 99-event preflight before any best-effort
  POST. Those API fields remain outside SBE native identity and digest domains.
- A capture failure remains non-authoritative: no retry, recovery, resource,
  spend, custody, or final-run outcome may depend on it.

## Next boundary

Slice 2 may now implement the narrow runtime builder only at the frozen,
ordinary live-exact terminal boundary, consuming the invocation-returned result
and restored durable workspace evidence without latest-result discovery or any
side effect. Keep the typed no-partial-set outcome for every excluded,
incomplete, contradictory, unknown-version, record-overflow, and byte-overflow
case.
