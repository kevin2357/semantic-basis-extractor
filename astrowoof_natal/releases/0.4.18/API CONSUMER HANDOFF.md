# API Consumer Handoff — SBE 0.4.18

Use `astrowoof-natal-authoring==0.4.18` for retained-workspace lifecycle
inspection and continuation.

This patch makes the lifecycle v0.6 projection accept `independent` resolved
action relationships already defined by lifecycle v0.5. Consumers do not need
to change their command selection, authorization construction, or provider
handling.

The API must continue to treat SBE's public lifecycle inspection and native
result as the authoritative native outcome. Text logs remain diagnostic only.
No new provider authority is implied by this patch.
