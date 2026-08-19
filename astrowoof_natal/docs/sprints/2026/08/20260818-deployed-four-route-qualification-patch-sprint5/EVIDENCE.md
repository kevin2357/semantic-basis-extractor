# Deployed Four-Route Qualification Patch Sprint 5 Evidence

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
