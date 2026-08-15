# Slice 0 Baseline Result

Status: complete; pending review and commit

## Reproduced behavior

A provider-free fixture now represents the API-reported state:

- the native run and subject are `DELIVERY_COMPLETE`;
- accepted deck and delivery artifacts exist;
- two creative-retry actions are `AUTHORIZED` but unconsumed;
- neither action has provider identity, reported evidence, or ambiguous submission;
  and
- one lifecycle inspection reports both actions as providerless-denial eligible.

Calling the existing single-action operation for the first action succeeds. Exact
replay of that request is idempotent. Calling it for the second action using the
same original inspection returns `stale_observation`, because the first successful
mutation advanced native revision and snapshot identity.

The second refusal is byte-non-mutating. The first action remains denied, the second
remains authorized, and accepted terminal deck/delivery bytes retain their exact
hashes.

## Interpretation

The API report is confirmed. Existing stale-observation protection is correct and
must not be weakened. Current SBE already permits providerless denial in a terminal
delivery context when the individual action is otherwise eligible. The missing
capability is one all-members preflight and semantic mutation bound to the shared
original observation.

No unrelated lifecycle, provider, snapshot, or delivery defect appeared in this
baseline. Slice 1 can therefore define the batch contract against this fixture.

## Gate evidence

- Focused negative-authorization suite: 12 passed.
- Full repository suite: 275 passed.
- Provider operations: 0.
- Paid spend: $0.
- API key: not used.
