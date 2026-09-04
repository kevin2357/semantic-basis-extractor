# Background — Release-smoke zero-paid-action terminal-review correction

## Trigger

API’s GHCR workflow `33834841337` failed before publishing an SBE 0.4.42 worker
image. The failing image layer invokes:

```text
astrowoof-release-smoke --work-dir /tmp/sbe-smoke --require-installed
```

The installed release-smoke fixture reaches `FINAL_QA_FAILED`, then terminal-result
construction raises:

```text
ValueError: Terminal result requires a paid-action inventory
```

The separately invoked public `astrowoof-deployed-qa` command passes on the exact
same installed 0.4.42 wheel, with a provider-free receipt and zero provider
operations/spend. The problem is therefore the release-smoke terminal fixture, not
API’s command selection or deployment wiring.

## Required distinction

Two terminal situations are intentionally different:

1. A real ordinary-v2 run created paid actions. Its terminal review must retain the
   complete exact paid-action disposition inventory; absence is unsafe.
2. A provider-free release-smoke fixture reaches terminal editorial/validation
   failure before any paid action exists. It needs a closed, explicit zero-action
   terminal disposition that can publish and validate without manufacturing action
   lineage.

Do not solve this by weakening the paid-action requirement globally, inventing
synthetic action IDs, deleting the smoke, or treating empty inventory as proof that
an action-free live run is safe.

## API operational posture

- QA deterministic and SBE consumers are suspended.
- No reset window, destructive reset, R2 change, provider operation, or profile
  mutation has run.
- API will keep both `astrowoof-release-smoke` and `astrowoof-deployed-qa` image
  gates. After an immutable SBE patch release, it will conduct normal artifact
  intake, GHCR build, manifest generation, and then the separately approved QA
  reset/deployment.
