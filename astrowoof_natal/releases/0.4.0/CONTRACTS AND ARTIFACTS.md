# Bounded Contracts and Artifact Inventory

The packaged `astrowoof.contract_catalog.v0.1` is authoritative for names. Packaged
JSON Schemas are authoritative where listed.

| Artifact | Contract | Visibility |
| --- | --- | --- |
| Admission summary | `astrowoof.bounded_natal.input_admission.v1` | private/operator |
| Candidate policy | `astrowoof.bounded_natal.candidate_policy.v1` | private |
| Editorial utility | `astrowoof.bounded_natal.editorial_utility.v1` | private; not confidence |
| Claim deck | `astrowoof.bounded_natal.claim_deck.v1` | private; packaged schema |
| Disposition report | `astrowoof.bounded_natal.disposition_report.v1` | private; packaged schema |
| Authoring packet | `astrowoof.bounded_natal.authoring_packet.v1` | provider-visible; packaged schema |
| Final cards | `astrowoof.bounded_natal.cards.v1` | reader-facing; packaged schema |
| Critic result | `astrowoof.bounded_natal.critic.v1` | private; packaged schema |
| Delivery | `astrowoof.bounded_natal.delivery.v1` | consumer handoff; packaged schema |
| Delivery provenance | `astrowoof.bounded_natal.delivery_provenance.v1` | private/consumer |
| Route specialization | `astrowoof.bounded_natal.authoring_run.v1` | inside common run v0.9 |

Delivery references the exact bytes of cards, private claim deck, provider packet,
and disposition report. The complete workspace snapshot—not delivery alone—is the
resume unit. Selected-card evidence and summary/whole-dog evidence retain distinct
provenance scopes.

See `sanitized-bounded-delivery-example.json` for the shape produced by the
provider-free installed acceptance run. Its hashes identify ephemeral sanitized
artifacts that are deliberately not checked into the repository.
