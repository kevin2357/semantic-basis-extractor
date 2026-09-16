# Log — Alloy Counterfactual Native-Authority Seam Failures

## 2026-09-16 — Sprint seeded

- Created a documentation-first counterfactual investigation on branch
  `codex/alloy-native-authority-counterfactual-sprint1` from `main`.
- Frozen two related but distinct historical clusters: the Danish-adjacent Aster /
  Bramble terminal-and-command-selection witnesses, and the tighter exact
  native-authority “no invented continuation” witnesses.
- Identified three possible model layers: terminal/custody/command selection,
  external-authority create permission, and an optional public-evidence adapter
  refinement.
- No Alloy CLI/JAR is currently installed. Tool acquisition is explicitly deferred
  to the plan’s approval gate. No external, provider, deployment, R2, or database
  operation occurred.

## 2026-09-16 — Slice 0 historical authority map

- Read the named Aster, Bramble, retained-wave, retry-handoff, and mixed-custody
  records plus the later provider-free counterexample corpus.
- Classified seven witnesses into two small models without treating log chronology
  as state authority. Model A is terminal ingress/custody/command choice; Model B is
  exact continuation authority.
- Gate A passes: proposed relations are grounded in public result/inspection/request
  contracts and API-owned custody/authorization facts. Tool acquisition remains the
  next separate approval boundary.

## 2026-09-16 — Tooling proposal prepared

- Confirmed through AlloyTools’ official release information that Alloy 6.2.0 has a
  Windows AMD64 archive and CLI-capable distribution. Local inspection found neither
  an Analyzer nor Java.
- Recorded a tightly bounded proposal: one official archive download to `C:\tmp`,
  SHA-256 recording, disposable extraction, and offline bounded model execution only.
- No archive was downloaded and no tool was installed; owner authorization remains
  required before proceeding to Model A.

## 2026-09-16 — Temporary Analyzer verified

- Owner approved temporary `C:\tmp` use. The proposed archive was already present,
  so it was not overwritten; SHA-256 and contents were verified before extraction.
- Extracted only to `C:\tmp\alloy-6.2.0`. Its bundled `alloy.exe` reports version
  6.2.0 and exposes offline `exec`; it includes its own runtime, so no system Java
  installation is needed.
- Began Model A as a deliberately small, content-free control-plane model.

## 2026-09-16 — Slice 1 Model A result

- Ran the offline Alloy 6.2.0 CLI against the terminal-ingress/custody/command model.
- All three deliberately permissive historical shapes were SAT: terminal plus
  generic retry, duplicate settlement, and pending provider identity plus ordinary
  resume.
- Under the three corrected adapter rules, all three bounded `check` commands found
  no counterexample through scope 3. Valid terminal closeout and pending
  reconciliation remained SAT, avoiding a vacuous “nothing can happen” model.
- Recorded model/receipt hashes and the full interpretation in the Slice 1 artifact.
  Pause at Gate B before the independent Model B authority model.

## 2026-09-16 — Slice 2 Model B result

- Added and ran the content-free exact-continuation model offline with Alloy 6.2.0.
- Its first execution exposed a scoped quantifier syntax error; corrected only the
  parentheses that bound the expressions. No model concept changed.
- All four historical permissive authority shapes were SAT. Under the corrected
  boundary, five `check` commands found no counterexample through scope 4; valid
  initial admission, exactly authorized retry, and ambiguity retention remained SAT.
- Pause at Gate C. Model C is optional because Models A/B already cover the core
  counterfactual question.
