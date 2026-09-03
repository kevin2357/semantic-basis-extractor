# Evidence Index

- Unfiltered Render export: `C:\tmp\sbe-worker-last-2h-20260902.txt`.
- Waffle checkpoint `4e2ed817-60a9-457f-913b-889bb40817f3` and coordinate
  packet in [BACKGROUND.md](BACKGROUND.md).
- Scone is a comparison run, not yet a shared-cause conclusion.
- Initial trace/source finding and review posture:
  [PRE-SPRINT HUDDLE.md](PRE-SPRINT%20HUDDLE.md).
- Slice 0 source map, production-boundary reproduction, controls, and corrected
  causal conclusion: [SLICE 0 - PRODUCTION CHARACTERIZATION.md](SLICE%200%20-%20PRODUCTION%20CHARACTERIZATION.md).
- Provider-free focused characterization: 2 tests passed.
- API Voof-paws 1 approval and Slice 1 guardrails:
  [API VOOF-PAWS 1 REVIEW.md](API%20VOOF-PAWS%201%20REVIEW.md).
- Slice 1 production correction:
  - removed assembly's duplicate hard authority for the three distribution-only
    advisory policies;
  - Waffle-shaped balance advisory reaches `DELIVERY_COMPLETE` through the real
    public resume boundary;
  - combined coverage/mirroring advisories reach successful assembly; and
  - unknown assignments remain hard failures.
- Focused Slice 1 evidence: 3 sprint tests and 3 existing policy tests passed.
- Slice 2 contract analysis and proposed narrow public disposition:
  [SLICE 2 - DETERMINISTIC FINALIZATION FAILURE CONTRACT.md](SLICE%202%20-%20DETERMINISTIC%20FINALIZATION%20FAILURE%20CONTRACT.md).
- API Voof-paws 2 approval:
  [API VOOF-PAWS 2 REVIEW.md](API%20VOOF-PAWS%202%20REVIEW.md).
- Slices 2–3 runtime evidence:
  - deterministic assembly contradictions alone map to sealed native-result
    v0.2 cause `finalization_contract_invalid` with final custody;
  - the invocation-bound command envelope is emitted before exit 2;
  - exact replay returns the identical result identity;
  - immutable API action/binding projection validation passes;
  - a rehashed non-final-custody mutation fails semantic validation;
  - publication interruption repairs the same result;
  - operational `OSError` produces no fabricated terminal review; and
  - `WAITING` and `SUBMITTING` action custody outrank finalization review.
- Focused runtime module: 7 tests passed in 116 seconds. Existing terminal-
  review contract suite: 9 passed, 2 optional-schema skips.
- Slice 4 packaged qualification:
  - added `astrowoof-finalization-boundary-qa` and its closed v1 receipt schema;
  - a real exact-Natal fixture proves a 14/2/2/2 `theme_group_balance`
    advisory reaches `DELIVERY_COMPLETE`;
  - deterministic finalization contradiction proves exact invocation/result,
    receipt, full action/binding, final-custody, and exact-replay joins;
  - operational `OSError` proves no native result is fabricated;
  - receipt asserts zero external network, real provider create, and spend;
  - source qualification passed with receipt SHA-256
    `8cc191895d08842deb9fce5f42149a2388e9b1b5b0e84511cfc35b985225d087`;
  - isolated `0.4.39` pre-release-shape wheel SHA-256
    `9878991df788283846ed6ab46cbff109c8f4c2511185a9864aed9ebfd279ad19`
    contained the command/schema and produced the same receipt; and
  - this is packaging evidence only, not the final immutable release artifact.
- Slice 4 handoff:
  [FINALIZATION BOUNDARY API HANDOFF.md](FINALIZATION%20BOUNDARY%20API%20HANDOFF.md).
- API Voof-paws 3 approved runtime, qualification, and handoff with no API
  source/schema change required before release. API's post-release gate is one
  installed-artifact ingress regression through its heartbeat worker.
- Release candidate version was bumped to `0.4.40` before release-bound tests.
- Release-bound focused evidence:
  - Waffle/Scone production-boundary matrix: 7 passed in 108.610 seconds;
  - terminal-review and theme-policy suites: 12 passed, 2 expected optional-
    schema skips;
  - source qualification passed (source metadata continued to identify the
    already-installed `0.4.39`, so it is not used as artifact identity);
  - two independently built `0.4.40` wheels were byte-identical at SHA-256
    `0a5904150eb2a579724f01d050c035a1c66d5f1882e7b19a78fb22775b54d8ad`;
  - wheel contents include the packaged command, reader, and schema;
  - installed console qualification passed with receipt SHA-256
    `dcbe5100ebd85a6a6fbbc2a5943a3cdacf7a79ad04030ac44309be7efc948587`;
  - isolated installed generic release smoke passed;
  - installed dependency check passed with SPC `0.11.1`; and
  - `git diff --check` is clean.
- The full repository suite was not run. Scope is limited to assembly policy,
  exact-interactive finalization error classification, the existing v0.2 cause
  vocabulary, and a qualification-only command. The focused/runtime/installed
  gates above are the recorded risk-proportionate release evidence.
- Candidate wheel evidence above precedes the final source commit. After owner
  approval, rebuild from the committed source and require the same deterministic
  wheel/qualification identities before tagging or publication.
- Owner approved release. Source commit
  `bfc80dbe1ea05fb3b9c1cda4a427ec5137c0f85c` reproduced the exact candidate
  wheel twice, then tag `astrowoof-natal-authoring-v0.4.40` and the GitHub
  release were published.
- Independent published-asset verification:
  - downloaded wheel SHA-256 matched `0a5904…54d8ad` and `SHA256SUMS.txt`;
  - remote annotated tag peeled to `bfc80db…0f85c`;
  - published wheel installed with SPC `0.11.1` and passed `pip check`; and
  - installed qualification reproduced `dcbe51…948587` with status `pass`.
