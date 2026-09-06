# OpenAI response editorial-audit feasibility

## Purpose

Determine whether a recent editorially rejected run can be audited with minimal
operational work by joining SBE trace identities to directly retrievable OpenAI
Responses, without first restoring or downloading the retained native workspace.

This is an exploratory audit exercise, not recovery, reconciliation, authority,
or a change to the editorial policy.

## Subject

Frisbee Fandango:

- API run: `e2d7f0ce-8c2a-4209-b79f-eb2187a58b15`
- native run: `cfdd79f1f50bbe940ba40d2c42743bf8b009cc02eef0f44895f0697b0d46be98`
- subject: `dog-f097e03d-58a0-49a4-98cd-946d01391503`
- terminal native posture: `FINAL_QA_REQUIRES_REVIEW`
- terminal inventory: six initial actions and two polish actions, all reported

No creative-retry action appears in the terminal eight-action inventory. The
audit nevertheless treats creative retries as an explicit stage category so a
generic extraction procedure cannot silently omit them on other runs.

## Response identity timing

An OpenAI response ID does not exist before the provider accepts a create call.
Before the call SBE records its native run, action, binding/request, grant, and
call-entry identities. After the create returns, SBE logs and durably records the
provider `resp_...` identity before later reconciliation. Retrieval logs repeat
the exact action-to-response join.

For Frisbee's polish attempts:

| Attempt | Native action | OpenAI response |
| --- | --- | --- |
| 1 | `paid_3fcbc02f87c6d0a289d06268` | `resp_030092921ee38ccb006a9bb789a9d887d0ae3d591e5b05b271` |
| 2 | `paid_998d8d1ab95c49a29e8c83a5` | `resp_040ede014ea2a048006a9bb7f6ae5887d0a62225aa14c3dee0` |

Attempt 2 is explicitly summarized in the trace as `POLISH_REJECTED`, with
validation clean, one lint warning, two edited fields, and five omitted targets.

## Retention premise

Current OpenAI documentation says stored Responses are retained for at least 30
days and may be retrieved by exact response ID. This experiment must treat that
as a time-bounded convenience, not an archival guarantee. A missing response must
remain `unavailable`; it must not be reconstructed or treated as empty.

