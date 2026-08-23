# Slice 1 — Observation Contract Proposal

Status: proposal complete; awaiting joint SBE/API schema and ownership review

The proposed public unit is one cumulative append-only revision of one paid native
transaction. It deliberately resembles an immutable transaction tape, not a deck,
stage, or cohort report.

Key decisions:

- native run/action identity is stable authority;
- interactive actions are individual transactions;
- a Batch round is one transaction and one authority with ordered member evidence;
- revisions bridge provider settlement and later editorial/run outcomes;
- revisions are self-contained cumulative documents with exact predecessors;
- missing or partial usage is not zero;
- SBE estimates remain distinct from provider money and API billing;
- multiple timing bases remain named and polling delay is not provider latency;
- PostgreSQL may retain revisions and merge them into an API-owned current row;
- analytics aggregates are derived downstream; and
- prompts, protected subject data, full bindings, and authorization documents are
  excluded.

Full proposal:
[Provider Economics Transaction Revision Contract Proposal](../PROVIDER%20ECONOMICS%20OBSERVATION%20CONTRACT%20PROPOSAL.md)

The two JSON examples in this directory are discussion aids, not frozen/package
fixtures. Runtime schemas and validators begin only after joint approval.

