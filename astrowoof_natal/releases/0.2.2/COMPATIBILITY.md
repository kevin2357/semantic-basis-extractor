# AstroWoof Natal Authoring 0.2.2 Compatibility

The wheel remains dependency-free, `py3-none-any`, and requires Python 3.11 or
newer. The qualified upstream tuple remains AGF 0.6.0, SPC 0.10.0, projected
graph 1.3.0, and pyswisseph 2.10.3.2 where live calculation is required.

Existing extraction, scoring, selection, synthesis, identity, provider-
disclosure, spend-policy, public-run, delivery, and provenance schema versions
remain unchanged. Operator run v0.9 and stable-logical-path restoration remain
authoritative.

The new repair command is additive. It supports only the documented 0.2.1
polish mismatch and refuses generic workspace repair.

`critic-findings.json` changes from an unversioned internal artifact to the
normative `astrowoof.qualitative_critic_findings.v0.1` private consumer
contract. Consumers must reject absent or unsupported versions. Old Kevin/Ella
critic files are not v0.1 fixtures and must not be upgraded by inference.
Candidate resume from an unversioned critic artifact fails closed; a completed
legacy run remains readable under its original release evidence.
