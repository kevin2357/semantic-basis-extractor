# Sprint evidence

## Frozen incident evidence available at Slice 0 start

- API run: `f84b3524-659a-4b86-83b4-7deb5b7c59a6`.
- Native run:
  `42407f1f4386eb0fcd387de9feb305a932d6626949dea247750f785bd1851920`.
- Native action: `paid_fb28a0c3a7e2a44743d65b8d`.
- First observed provider identity:
  `resp_0a83dca212896636006a93ae4a599087d0ae269439ce29c1d8`.
- Second observed provider identity:
  `resp_00ecec3e2a02b87b006a93aed2cb2887d0912ecce39fcef0a4`.
- SBE release: `0.4.29`.
- Background SHA-256:
  `59fea9f798c2376d40d0d3e4cfecd7c0d2b998385451474be88663b40b950ee2`.
- Investigation source baseline: `fd1652f5217a63eedefe3c82014be9f60663366c`.

## Slice 0 exact retained evidence

- API coordinate packet SHA-256:
  `a00f9a3bde6bc0ca903db23fd0fa893d791ac5244250f541607d4958fe0edfe6`.
- Checkpoint generation: 11; archive SHA-256:
  `eb8353732aba6b67169e9fe08603949412b1fa4c1d662326fa2ad5df4b88433e`;
  inventory SHA-256:
  `2f53194805d643ebed032417d627b0d6260bf88bbbcf9634f4d6be78af89ffe5`.
- Archive size: 3,832,236 bytes. Validated inventory: 760 members totaling
  16,672,267 bytes; every declared member path and SHA-256 matched.
- `run.json` SHA-256:
  `ce76c2e712061f96af99fcb09ba956ef7f00b12599781f7201bad20a42ea3fc4`.
- Journal SHA-256:
  `00dded683db07bd44763410e70a532b346e1e0da5d78f3a093d1147b7ddc3962`.
- Latest result: `nres_baa071ce080d1201658cb3ec`, published
  `2026-08-30T04:13:39Z`, outcome `provider_pending`; it contains the
  predecessor and predates the affected action.
- Affected action journal evidence in generation 11 consists of one
  `action.prepared` record at sequence 82 / `04:14:06.617729Z`.
- Provider-free characterization:
  `test_completed_retry_duplicate_submission_investigation_slice0.py` — one
  focused test passed, two exact restores produced two scripted creates, and both
  reached the real `semantic_work_not_consumed` refusal.

The repository-local configured database was queried read-only and contained no
matching run. It is not the authoritative QA database and is not negative incident
evidence.

## Side-effect counters after Slice 0

- R2 HEAD: 2 (one validator-stopped HEAD and one successful repeated HEAD).
- R2 GET: 1.
- R2 LIST: 0.
- R2 writes/deletes: 0.
- Provider calls/retrievals: 0.
- Retained workspace mutation/recovery: 0.
- Worker resume: 0.
- Protected temporary archive/workspace retained: no; removed after validation.

## Slice 0 conclusion

The retained checkpoint plus provider-free characterization support a combined
handoff-seam defect: generic create-capable ordinary resume had no API-retainable
pre-I/O native fence; after post-provider local-progress refusal prevented normal
result publication, API restored the older PREPARED checkpoint and invoked the
same create-capable action again. The evidence does not authorize choosing either
provider response or recovering the historical run.

## Voof-paws 1 review

- API approved Slice 0's causal assessment and independently ran the focused
  characterization: 1 passed in the SBE 0.4.29 environment.
- Review clarification incorporated: the test exercises genuine `closure.main()`
  restore/re-entry and real local-progress refusal, while authorization application
  and ordinary authoring/provider completion are scripted. Slice 2 must cover the
  unpatched v2 call-entry fence.

## Slice 2 native correction

- New public contract:
  `astrowoof.generic_provider_dispatch_refusal.v1`.
- New terminal-review cause: `local_work_progress_contradiction`.
- Generic refusal proves exit 0, exact run/basis/snapshot/action binding, zero
  mutation, zero native-result publication, and zero provider create.
- Local-progress contradiction proves exit 2 with a receipt-validated v0.2 result,
  exact action inventory, and `new_provider_create_permitted=false`.
- Existing real v2 dispatch regression proves durable `CALL_ENTERED`, interruption
  ambiguity, immediate identity durability, and no-create exact replay.
- Focused command: six test modules, 36 tests passed, two optional-schema skips.
- External provider calls: 0.
- Retained QA access after Slice 0 cleanup: 0.

## Slice 3 API-shaped fixture evidence

- Bundle schema: `astrowoof.duplicate_submission_fence_fixtures.v1`.
- Bundle SHA-256:
  `5382bd768a38cc3eeb2aafa092c3407c276932d479012c8deddc5a32f8cd9955`.
- Generic refusal cell is digest-bound to one exact run/basis/snapshot/action
  inventory and proves `not_attempted`, no publication, and fresh-inspection
  routing.
- Contradiction cell joins result
  `nres_c9c1a108c5b9f8accb912c02`, receipt
  `nreceipt_bc7877d0cb909bad54dba94b`, and the exact invocation envelope.
- Its provider-bearing action is explicitly retained under
  `provider_reconciliation_only`; new provider creation is false.
- Focused Slice 0–3 command: 8 tests passed, one expected optional-schema skip.
- External provider/R2/retained-QA activity during Slices 2–3: 0.

## Slice 4 installed-wheel qualification

- Candidate wheel SHA-256:
  `88355c4ef28d30ff59e8a90abfd6d8939e967a8a0994300a8a2bca6a61d2cbb5`.
- Wheel inventory contains all three required packaged JSON resources and the
  `astrowoof-duplicate-submission-fence-qa` console entry point.
- Installed qualification receipt SHA-256:
  `a4fb626def6300e445f4c69180dfa6e84c0dfb7eb93226812434a94018776049`.
- Fixture-bundle schema SHA-256:
  `8c1c9341594b295f99e3f360964f74f91fe9eafee3bb09bca7382be786c5dbd3`.
- Qualification schema SHA-256:
  `b65cd29e3e3b341768b85fcb664b0af263055f888bbc62234d528a2f195e0ceb`.
- Installed command was invoked outside the source checkout and re-read the
  packaged fixture bundle SHA-256
  `5382bd768a38cc3eeb2aafa092c3407c276932d479012c8deddc5a32f8cd9955`.
- Source fixture/qualification tests: 7 passed, two expected optional-schema
  skips. Broader Slice 0–3 focused suite: 40 passed, three expected optional
  schema skips.
- External provider calls/retrievals/spend and retained-QA access: 0.

## Slice 5 final release evidence

- Release identity: `0.4.30` (fresh and unpublished at qualification time).
- Full suite: 890 passed; 46 expected environment/optional skips.
- Deterministic wheel A/B SHA-256:
  `19a8728b35281e2415ec0b407ef882a505576e41c81d34488961ce08b5a83e9a`.
- Installed generic release smoke: pass; runtime resolved from virtualenv
  `site-packages` under `--require-installed`.
- Installed duplicate-submission-fence receipt SHA-256:
  `56ef9c75a84c079c140b21cc66074c0a036b0e10d1d9723fbaca3a6d4e645547`.
- Installed terminal-review receipt SHA-256:
  `71ace38b91584b179fd57432812ea473554da3dbdfff965f1c6598ce81335524`.
- Fixture-bundle/schema identities remain exactly those reviewed in Slice 4.
- Provider calls, retrievals, spend, R2 access, retained-QA mutation/recovery,
  and worker resume: 0.
