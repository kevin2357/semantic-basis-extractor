# API final release approval

## Approved for release

The required compatibility correction is incorporated:

- `--allow-theme-group-edits` is no longer treated as an authoring-phase polish
  override;
- it is accepted in both authoring and polish copied-validator invocations;
- it remains invocation provenance only, with no effect on validation,
  warnings, or polish edit locks.

API independently reran the stated focused qualification:

```text
python -B -m unittest astrowoof_natal.tests.test_sbe_v03 \
  astrowoof_natal.tests.test_theme_group_qa_dormant_slice4
Ran 54 tests ... OK
```

The release remains a narrow native/package correction.  No API contract,
lifecycle, provider, custody, or retained-QA migration is required.  SBE may
commit, tag, publish, and release.
