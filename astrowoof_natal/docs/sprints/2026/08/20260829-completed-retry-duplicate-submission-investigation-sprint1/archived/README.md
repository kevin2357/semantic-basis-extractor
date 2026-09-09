# Archived Slice 0 duplicate-submission characterization

`completed_retry_duplicate_submission_investigation_slice0.py.txt` preserves
the exact source of the provider-free historical reproduction originally run as
`astrowoof_natal/tests/test_completed_retry_duplicate_submission_investigation_slice0.py`.

The active regression suite no longer executes it because its passing condition
is the obsolete failure itself: restoring one frozen mixed checkpoint twice and
observing two scripted successor creates. It remains useful forensic evidence,
but is not a present-tense product invariant.

Git history:

- introduced/refined by `0b37c70` (`fix duplicate provider submission reentry fence`);
- semantic-closure support extraction updated it in `7f35474`; and
- archived during the 2026-09-06 duration-led provisional promotion campaign.

The modern safety boundary remains active in that incident sprint's Slice 2
regressions: generic create-capable resume refuses before provider I/O, while a
completed-local-progress contradiction seals a typed review result with
`new_provider_create_permitted=false`.
