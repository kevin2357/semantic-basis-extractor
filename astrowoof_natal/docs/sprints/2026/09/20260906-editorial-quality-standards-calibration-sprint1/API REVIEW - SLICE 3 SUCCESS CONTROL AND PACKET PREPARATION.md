# API review — Slice 3 successful control and packet preparation

## Review outcome

Aligned. The successful-delivery control is a meaningful ordinary control rather
than a no-op: it binds exact accepted polish transitions, passing final
validation/lint, the native `delivery_complete` result, and its receipt to the
authorized generation-10 checkpoint. The access ledger also records exactly the
bounded access authorized by API: one conditional HEAD and one GET, with no
listing, provider work, recovery, reconciliation, or mutation.

The five-run replay remains appropriately provider-free and reproducible. The
eight blinded packets and separate answer key preserve the calibration boundary;
they do **not** silently freeze a public/native routine-capture contract.

## Useful evidence for the companion schema decision

The measured sizes are particularly helpful for Sprint 87 Slice 0-alpha:

- finding-local packets: 6,917–74,254 canonical UTF-8 bytes;
- complete selected-deck packets: 1,016,507–1,081,094 bytes; and
- the successful control proves that an accepted transition can be represented
  honestly with empty residual findings.

Those figures do not require that routine Better Stack capture exclude complete
deck text. They do mean the API experiment should measure both alternatives and
make the complete-deck choice explicit, rather than accidentally treating it as
free. The prospective corpus is exploratory and best-effort, not an
authoritative reporting dataset; its eventual packet model should be chosen for
the editorial queries it makes pleasant and legible.

## Requested input for Sprint 87 Slice 0-alpha

Kevin's pseudocode query is a strong anchor. Please add four to six short,
native-semantics-first example queries that you expect a reviewer to ask of a
routine corpus. Use real conceptual fields/relationships where possible, not
implementation commitments. Useful coverage would include:

1. a rejected polish transition with its exact before/after findings and affected
   field context;
2. a candidate that improves the target finding but remains rejected by a
   whole-deck decision, alongside a successful control;
3. a malformed/non-materialized candidate distinguished from an ordinary
   editorial rejection;
4. a structural validation failure where lint otherwise passes; and
5. a finding pattern across stage/release/prompt provenance, without claiming
   the corpus is population-complete.

API will run these beside Kevin's query against both proposed local packet
shapes before the shared schema is frozen. This is a request for query-design
input only; it authorizes no runtime, public contract, Better Stack publication,
or package change.

## Boundary

Slice 3 may proceed to its owner and independent-model judgments under the
existing private-calibration rules. Any editorial-policy, prompt, production
schema, or release change remains gated at Voof-paws 3.
