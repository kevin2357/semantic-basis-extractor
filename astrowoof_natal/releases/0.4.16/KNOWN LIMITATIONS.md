# Known Limitations — SBE 0.4.16

- Lifecycle v0.6 requires caller-supplied trusted canonical UTC time; SBE does not
  claim authority over the API's durable temporal sequencing.
- The temporal decision is scheduling evidence, not API-global slot, reservation,
  quota, billing, or product authority.
- Provider retrieval remains bounded to four due Response actions per cycle.
- A provider identity/output conflict remains a review condition; it is not an
  automatic retry signal.
- Legacy lifecycle versions fail closed at the v0.6 boundary and are not silently
  reinterpreted.
- The installed qualification is provider-free and qualification-only. It does not
  confer production authority or exercise live OpenAI traffic.

