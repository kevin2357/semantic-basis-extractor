# Deployed Four-Route Qualification Patch Sprint 5 Evidence

## Exact 0.4.9 artifact

- Artifact source commit:
  `220aae69badb54ed657f2370167691db0e5be5cf`.
- Wheel: `astrowoof_natal_authoring-0.4.9-py3-none-any.whl`.
- Bytes / SHA-256: 836,513 /
  `3b900cc3216dd07e164af1a18a4a607c17e3fa1190711893808ba6527042f83d`.
- Wheel boundary: 121 entries / 72 resources / zero tests or bytecode /
  `py.typed` present.
- Full source: 454 passed / 20 expected skips / 474 total.
- Exact installed Windows/Linux lifecycle, release, and four-route gates: pass.
- Version-bound receipt SHA-256:
  `104e81d5fc9e6014264c7887e5e1dac626286d29fe732cbb4b07c719497face5`.
- Provider operations / spend: 0 / USD 0.

## Final consumer review

- [API Agent V2 Approval.md](API%20Agent%20V2%20Approval.md)
- Disposition: approved; recommend fresh immutable 0.4.9.
- No remaining API contract or implementation corrections.

## Corrected production Batch evidence

- [API Batch mechanism review](API%20Agent%20Batch%20Mechanism%20Review.md)
- Exact Batch invokes production `author_pending_passes_batch`; native state
  contains one `batch_service.rounds` record, one Batch ID, and six ordered
  `requests` after the scripted provider returns `in_progress`.
- Bounded Batch invokes production `_bounded_batch_authoring_cycle`, including
  native `_prepare_bounded_batch_round`; its native state contains the equivalent
  one-round/one-ID/six-request evidence.
- Both transports record exactly one upload and one create. Neither retrieves or
  downloads because qualification intentionally stops at provider-pending detach.
- Both fresh-reader checks reload `run.json`; no qualification-local substitute
  round is used.
- Focused source suite: 24 passed. Installed Windows/Linux command: pass.

- Command: `astrowoof-deployed-qa`.
- Receipt contract:
  `astrowoof.deployed_qa_four_route_qualification.v1`.
- Exact interactive: six scripted creates, observed concurrent peak six, detached,
  durable-byte reload/fan-in passed.
- Bounded interactive: same topology and assertions passed.
- Exact Batch: one scripted Batch create, one authority, six logical members,
  durable round reload passed.
- Bounded Batch: same one-round/six-member assertions passed.
- Bounded final-QA precedence: `review_required` /
  `final_qa_requires_review` despite six accepted pass records.
- Duplicate bounded claim deck: native validator refused with
  `bounded_claim_identity`; provider create count zero.
- Strict JSON Schema validation: pass.
- Installed Windows and network-isolated Linux command: pass.
- Cross-platform receipt SHA-256:
  `04b8629b59d7742bb4ea87db4956651f0c4c06e3763af10935fcaee486902676`.
- Real provider operations / spend: 0 / USD 0.
