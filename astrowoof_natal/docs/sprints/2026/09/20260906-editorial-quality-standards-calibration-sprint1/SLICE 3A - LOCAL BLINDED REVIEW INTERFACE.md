# Slice 3A — local blinded-review interface

## Result

Slice 3A is complete. A deterministic static page presents all eight frozen
candidate-transition samples for private blinded judgment without requiring the
reviewer to inspect raw JSON.

Generated page:

`.tmp-editorial-calibration-r2/private-review-ui/blinded-editorial-review.html`

Receipt:

`.tmp-editorial-calibration-r2/private-review-ui/blinded-editorial-review-receipt.json`

The private page and judgments remain outside the repository.

## Reviewer surface

For each sample the page shows:

- stable blinded packet ID and candidate position;
- every exact edited field path with before/after text;
- prior and candidate finding status, count, identity, and affected text;
- candidate structural-validation status and errors;
- separate closed choices for deck acceptability and candidate adoption; and
- optional reviewer rationale.

Run labels, subject identities, native run IDs, historical adoption decisions,
terminal outcomes, and the answer key are absent.

## Export contract

The export button remains disabled until the reviewer supplies a local role and
both judgments for every sample. The exported JSON contains:

- schema `astrowoof.private_editorial_judgments.v1`;
- frozen rubric version;
- reviewer role;
- packet ID and exact source packet-file SHA-256;
- separate deck-acceptability and candidate-adoption judgment; and
- optional rationale.

The closed vocabulary is:

- `accept`;
- `accept_with_advisory`;
- `request_another_polish`;
- `retain_prior_candidate`;
- `terminal_review`; and
- `insufficient_context`.

No timestamp is added, so identical reviewer inputs serialize identically.

## Verification

- packet count: 8;
- page bytes: 343,188;
- page SHA-256 on both builds:
  `23bacd8c3cd60c117e281da4662c5b4f62e8593d0c665ae69181cb1300061821`;
- receipt SHA-256:
  `f18b4396e8c7b8ee2e819234bf60b5b3288c0c227a7337f3aab8c8651171d563`;
- answer-key identity leaks: 0;
- external HTTP references: 0;
- focused tests: 2 passed.

The tests also cover mixed-rubric refusal, HTML/script-breakout-safe payload
embedding, closed choices, completeness gating, and judgment-to-packet hash
binding.

## Boundary

This is private review tooling only. It changes no production code, editorial
policy, prompt, schema, API transport, Better Stack behavior, or release
surface. Slice 3 still requires actual owner and independent-model judgments.
