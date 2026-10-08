# Processing-profile catalog

This is a human-readable index of the package-installed catalogs. The JSON
catalogs remain authoritative; the values below describe the profiles planned
for SBE `0.4.71`.

| Profile | Route and selection policy | Prompt release | Required SBE | Purpose |
| --- | --- | --- | --- | --- |
| `astrowoof.exact_natal.live.compat.v1` | exact natal / live; `legacy_atomic.v1` | `astrowoof.authoring.compat.v1` | `0.4.66` | Historical compatibility bundle. Retain its compatible worker context for recovery. |
| `astrowoof.exact_natal.live.compat.v2` | exact natal / live; `legacy_atomic.v1` | `astrowoof.authoring.compat.v2` | `0.4.69` | Current-code compatibility profile. |
| `astrowoof.exact_natal.live.axisawaresbe.v1` | exact natal / live; `axis_aware.v1` | `astrowoof.authoring.editorial.v2` | `0.4.68` | Historical axis-aware editorial bundle. |
| `astrowoof.exact_natal.live.axisawaresbe.v2` | exact natal / live; `axis_aware.v1` | `astrowoof.authoring.editorial.v3` | `0.4.69` | Current axis-aware editorial bundle. |
| `astrowoof.bounded_natal.live.stable_facts.v1` | bounded natal / live; `stable_facts_only.v1` | `astrowoof.authoring.bounded_stable_facts.v1` | `0.4.70` | Stable-facts-only bounded bundle; not active until its separate API/QA gate passes. |
| `astrowoof.bounded_natal.live.stable_facts.v2` | bounded natal / live; `stable_facts_only.v1` | `astrowoof.authoring.bounded_stable_facts.v2` | `0.4.71` | Successor bounded bundle with the explicit API-owned spend-policy handoff; requires its own installed-wheel/API gate. |

All listed profiles currently permit `qa` and `production`. Permission to be
selected is separate from being installed: API controls admission and the active
profile/context selector per environment.

## Prompt releases

| Prompt release | Contents | Bound profile(s) |
| --- | --- | --- |
| `astrowoof.authoring.compat.v1` | Compat system authoring prompt | compat v1 |
| `astrowoof.authoring.compat.v2` | Same compat prompt bytes, independently versioned with its 0.4.69 profile bundle | compat v2 |
| `astrowoof.authoring.editorial.v2` | Editorial system prompt plus versioned authoring brief and guiding lights | axis-aware v1 |
| `astrowoof.authoring.editorial.v3` | Same declared editorial component bytes, independently versioned with its 0.4.69 profile bundle | axis-aware v2 |
| `astrowoof.authoring.bounded_stable_facts.v1` | Versioned bounded authoring, retry, critic, and polish instructions with anti-precision guidance | bounded stable-facts v1 |
| `astrowoof.authoring.bounded_stable_facts.v2` | Same bounded instruction/component inventory, independently versioned for the `0.4.71` paid-initialization bundle | bounded stable-facts v2 |

The apparent byte equivalence of two releases is not an invitation to collapse
their identities. Each profile binds the exact release ID and digest it was
qualified with. See [README.md](README.md) for the immutable-recovery rule.
