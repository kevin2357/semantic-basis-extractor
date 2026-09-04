# Slice 3 — dormant theme-feature qualification

**Status:** final committed-source wheel qualification complete; tag and
publication await owner approval.

## Scope

This is not a lifecycle, provider, custody, terminal-result, or API-contract
change. It makes the dormant theme-group filtering feature non-participatory:

- legacy `ASSIGN THEME GROUPS.md` is ignored during assembly;
- no registry or assignment field is emitted in a delivered deck;
- pass-six production generation no longer creates or requests the artifact;
- explicit legacy fixture construction remains supported only to prove old
  workspaces do not fail.

## Provider-free source evidence

Command:

```text
PYTHONPATH=astrowoof_natal/src \
  .tmp-puff-041-final-venv/Scripts/python.exe -m unittest -b \
  astrowoof_natal.tests.test_sbe_v03 \
  astrowoof_natal.tests.test_theme_group_qa_dormant_slice4
```

Result: **51 passed**.

The direct assembly witness starts with new pass-six generation (which lacks
the artifact and its instruction), then injects a retained Ganache-shaped
artifact whose registry is valid but whose `theme_group.interdogpendence.*`
assignment refers to `grounded_companionship`, an unknown chapter. The real
multi-pass assembler returns the complete deck with no theme-group fields and
no placeholder leakage.

The dormant-policy checks separately prove the live acceptance path does not
invoke the theme evaluator, while an unrelated editorial rejection remains a
hard rejection.

`git diff --check` passed. No network, provider, R2, retained workspace, or
run action occurred.

## Clean-wheel / installed-artifact evidence

Candidate version: `0.4.42`.

The wheel was built from a `git archive HEAD` source copy overlaid only with the
candidate `pyproject.toml`, `assembly.py`, `extractor.py`, and the focused test
file. This intentionally excluded unrelated dirty working-tree changes,
including reconciliation work.

Wheel SHA-256:

```text
58ccfaa319a244afea177e40e7c83e40b0e220c9bd86fe0034512ee19a28dc8d
```

The final package was rebuilt twice from source commit `72d5d6c`, using a
minimal archive of only `pyproject.toml` and package source so unrelated dirty
files and long-path historical reference artifacts could not enter it.
`SOURCE_DATE_EPOCH` was pinned to that commit's timestamp; both wheels matched
the digest above. The final wheel was force-installed without dependencies into
an isolated release environment. `pip check` reported no broken requirements.
A clean working directory then confirmed that imported `assembly` and
`extractor` modules came from that environment's `site-packages`, not the
source tree, before executing the direct Ganache-shaped complete-assembly
witness successfully.

## Release gate

The release source commit and final wheel are ready for tag/publication. The
existing public theme-policy qualification command is historical policy evidence
and is not used to claim this dormant-feature behavior.
