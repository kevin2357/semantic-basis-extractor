# Evidence

## Source export

- File: `C:\Users\kevin\Downloads\sbe logs.txt`
- SHA-256: `7b3729c2801da39fa27eae56e0dc3c2023e998729618df84236dde0147f493f1`
- Times below are America/Denver (UTC-06 on 2026-09-05).

## Triumph — complete native-to-worker timeline

Triumph's native run is
`45eb2039befdf81a3fa09f86a79ef08598dd09085191e98ee5de1bdaa361c468`;
its API run is `9686b45d-f27b-473a-b167-8893bb4b18c2`.

At 00:41:34 the worker invoked the exact v2 external-authority command for the
single prepared polish action `paid_699df696b831d5680681a7c4`. The command
validated the request/fence, consumed the grant, durably entered submission, and
recorded provider identity `resp_0aa0462cf3bb9536006a9bb9a4684887d0a970b807df5d2dd5`.

At 00:42:42 reconciliation retrieved that exact response as `completed`. SBE
joined it to the polish action, adopted and reported it, ran validation and lint
successfully, packaged the delivery, and transitioned the native run to
`DELIVERY_COMPLETE`. All seven actions were `REPORTED`; provider custody and
local dependencies were both zero.

At 00:42:49 SBE sealed and published:

- invocation: `ninv_863529ebeb3a46b097e6a7a7`
- result: `nres_28052253b80b2ddcb36bbbcd`
- result SHA-256: `28052253b80b2ddcb36bbbcd1bc0331609e6520ebe6f0c0ca4e13c68d5924fe9`
- receipt: `nreceipt_00871986cb95123529b5e17e`
- receipt SHA-256: `00871986cb95123529b5e17ee65ab79e67352724cc606a8557419cdce10840c4`
- native outcome/cause/status: `delivery_complete` / `delivery_complete` /
  `DELIVERY_COMPLETE`
- command exit: zero, authoritative transport `stdout_json`

At 00:43:20 the API worker accepted checkpoint generation 9, recorded no local
continuation and zero provider-local dependencies, then emitted
`sbe.closeout.completed` followed by `worker.job.failed` with reason
`native.terminal.delivery_complete`.

## Causal conclusion

SBE completed the provider, adoption, validation, packaging, checkpoint, result,
and receipt path correctly. The failure occurs in API terminal disposition:
`sbe_runtime.py` reduces a lifecycle inspection whose capacity disposition is
`terminal` to `TERMINAL_CLOSED`; `sbe.py` then treats that branch as failure even
when exact native ingress classifies the sealed result as delivery publication.
The explicit sealed-terminal preflight already has a distinct
`DELIVERY_ACCEPTED` path, demonstrating the inconsistent mapper behavior.

This is an API correction. It does not justify an SBE patch or R2 inspection.

## Frisbee

Frisbee remains separate: its native result is an ordinary editorial
review-required outcome after the permitted polish attempts, not evidence of the
Triumph API mapper defect.
