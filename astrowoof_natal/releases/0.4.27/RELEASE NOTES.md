# AstroWoof Natal Authoring 0.4.27

Status: published and download-verified

SBE 0.4.27 corrects post-fan-in lifecycle routing and publishes two scoped,
provider-free ordinary-v2 happy-path witnesses. Completed provider evidence now
selects local fan-in only when the run is nonterminal and no retained provider
action is already due. Due provider custody continues to outrank local fan-in;
not-due custody permits the exact completed local operation to advance.

When multiple successor actions become co-ready after custody clears, SBE exposes
one lexical `ordinary_action_set` envelope while preserving distinct paid-action
bindings, authorization documents, reservations, and grant members.

The public happy-path artifacts are explicitly scoped to
`post_fan_in_selector_authority_and_replay`. They are production-shaped
selector/authority witnesses, not end-to-end authoring simulations; their exact
fixture-installed precursors are machine-readable.

## Candidate qualification

- Artifact source commit: `adbbc70`.
- Fixed build epoch: `1787874000`.
- Full source suite: 839 passed; 41 expected environment/opt-in skips.
- Two byte-identical candidate wheels; SHA-256
  `210ed3c98bcc84c2cfe9e9669edebaa56a1780bc1bb8057e61c0fffbd0c4c276`.
- Generic installed release smoke: passed with `DELIVERY_COMPLETE`.
- Installed adversarial, post-fan-in, and scoped happy-path qualifications: passed.
- API installed campaign: 10 passed; source `adbbc70` and exact wheel digest
  accepted in API commit `abcc024`.
- Exact installed dependency: `semantic-projection-core==0.11.1`.
- External provider/network calls and spend: 0.
- Retained QA access/mutation: 0.

Owner and API reviews authorized immutable publication. The release is published
at `astrowoof-natal-authoring-v0.4.27`; the downloaded wheel and GitHub asset
metadata both verify SHA-256
`210ed3c98bcc84c2cfe9e9669edebaa56a1780bc1bb8057e61c0fffbd0c4c276`.
