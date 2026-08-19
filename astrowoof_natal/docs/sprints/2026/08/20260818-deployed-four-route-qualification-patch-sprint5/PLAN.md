# Deployed Four-Route Qualification Patch Sprint 5 Plan

Date: 2026-08-18  
Status: implementation and API review complete; awaiting explicit 0.4.9 release authorization  
Starting release: SBE 0.4.8  
Proposed release: SBE 0.4.9

## Purpose

Give AstroWoof API a supported installed-wheel QA command it can execute as a
Render one-off job after deployment. The command must prove the four authoring
route topologies without provider credentials, network access, spend authority,
or production run input.

## Frozen boundary

- Public API: `run_deployed_qa_qualification()`.
- Public validator: `validate_deployed_qa_receipt(receipt)`.
- Public schema reader: `read_deployed_qa_schema()`.
- Console command: `astrowoof-deployed-qa`.
- Receipt: `astrowoof.deployed_qa_four_route_qualification.v1`.
- The operation accepts no provider credential, endpoint, run directory,
  authorization, or product input.
- It creates only an automatically deleted temporary qualification workspace.
- It is evidence that installed SBE route mechanisms work; it is never native run
  authority, provider evidence, spend evidence, API reservation authority, or
  permission to publish a reading.

## Qualification assertions

1. Exact and bounded interactive routes each execute six overlapping scripted
   create callbacks through the production initial-wave coordinator, persist each
   outcome serially, detach provider-pending, and reload all six identities from
   durable temporary bytes as a fresh-reader fan-in.
2. Exact and bounded Batch each execute one scripted Batch create carrying six
   unique logical members, persist the round, and reload it as one provider/global
   authority rather than six.
3. Native bounded final-QA outcome classification retains review precedence even
   when all six pass records are accepted.
4. The bounded claim-deck validator rejects duplicate claim IDs before any
   scripted provider callback is available or invoked.
5. The closed receipt declares zero real provider operations, zero spend, no
   network requirement, qualification-only use, and no production authority.

## Test and release gates

- Source API/CLI, closed-digest, schema, tamper, and output-file tests.
- Existing initial-wave/public-contract non-regression tests.
- Strict JSON Schema validation.
- Build a non-publishable 0.4.8-labeled candidate and invoke the installed console
  entry point on Windows and network-isolated Linux.
- Pause for API review before version bump or release work.
- If approved, build and publish only a fresh immutable 0.4.9 after separate Kevin
  authorization.

No paid or live provider qualification is permitted.
