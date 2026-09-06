# Audit manifest

## Scope and private storage

- API run: `e2d7f0ce-8c2a-4209-b79f-eb2187a58b15`
- native run: `cfdd79f1f50bbe940ba40d2c42743bf8b009cc02eef0f44895f0697b0d46be98`
- subject: `dog-f097e03d-58a0-49a4-98cd-946d01391503`
- raw directory: `C:\tmp\astrowoof-frisbee-openai-audit-20260906\raw`

The raw JSON is intentionally uncommitted because it contains full provider
output. All timestamps below use America/Denver (`UTC-06` on this date).

## Initial wave

| Action | Response | Created | Completed | Bytes | SHA-256 |
| --- | --- | --- | --- | ---: | --- |
| `paid_ae911e9ecc46ae933e55c5f0` | `resp_01868e153adc6360006a9bb64f718887d0a2561b673fa90ddf` | 00:27:27 | 00:29:43 | 185412 | `f8a77b09454798f0ca89009188907529e6152973787d62a5506b6c4b87e0c6a4` |
| `paid_81821e3d234e44ba15e15eda` | `resp_05673a08aef382d4006a9bb64f47fc87d0b316b166a7d10b30` | 00:27:27 | 00:30:45 | 191331 | `c8fd3831d07180c861f4585c039ef20a75eaa13223928d197a9b34b1f4bcc698` |
| `paid_216f33878628ea17dafd5a2d` | `resp_0211795486a21f9a006a9bb64f839087d08fbc4d53baea9282` | 00:27:27 | 00:30:34 | 188951 | `5e138f3d3f1a51e0022e0fd25789dd0f5ba85fca812f8fe1dcdd3f51245190f6` |
| `paid_d8087b478258bf1aed4fe577` | `resp_042af2e9d7f0a909006a9bb64f744c87d0ad77023a8b40a7c4` | 00:27:27 | 00:30:47 | 190485 | `35e71e5f92b8f825ef73afc50b7b9cd01b89b7202b2979a2b152e95bef53898e` |
| `paid_1706dfd2c0211eb4fe7806e9` | `resp_012de5b13c79d96a006a9bb64f571887d0ac19d93b9886e013` | 00:27:27 | 00:30:23 | 185548 | `f89b0bf9eb5b3fec6b1be554e824671f8926725114fd8e88b5e9a6bc0c7b7103` |
| `paid_bc4deb748eeb2a8665f14dff` | `resp_0a6a5f81fb7bb5c6006a9bb64f2b3087d082b7b1982c7b43d9` | 00:27:27 | 00:29:17 | 96407 | `e4a51488332bae0e986faca15e8ad8fe9d660ad064a5966a5252094156c38130` |

## Optional-stage lineage

| Stage | Attempt | Action | Response | Created | Completed | Bytes | SHA-256 | Native disposition |
| --- | ---: | --- | --- | --- | --- | ---: | --- | --- |
| polish | 1 | `paid_3fcbc02f87c6d0a289d06268` | `resp_030092921ee38ccb006a9bb789a9d887d0ae3d591e5b05b271` | 00:32:41 | 00:32:59 | 16500 | `4afd556812b26b44f9f2403b2ae4bfa9f58c86713557ff85bf12cafb7b04d096` | accepted before attempt 2 was requested |
| polish | 2 | `paid_998d8d1ab95c49a29e8c83a5` | `resp_040ede014ea2a048006a9bb7f6ae5887d0a62225aa14c3dee0` | 00:34:30 | 00:34:37 | 4637 | `2eb784e6d2380c8189221b20bc896875148be94e6a735b2fb149ce65b1b6a764` | `POLISH_REJECTED`; validation clean, one lint warning, two edits, five omitted targets |
| creative retry | — | — | — | — | — | — | — | `none_observed` |
| critic | — | — | — | — | — | — | — | `none_observed` |
| candidate | — | — | — | — | — | — | — | `none_observed` |

## Provider metadata summary

All eight objects are stored, completed background Responses from
`gpt-5.6-luna`. The initial outputs contain approximately 49k–84k characters of
message text each; polish attempt 1 contains approximately 10.7k characters and
attempt 2 approximately 943 characters. This is consistent with full initial
authoring artifacts followed by progressively narrower editorial patch payloads.

