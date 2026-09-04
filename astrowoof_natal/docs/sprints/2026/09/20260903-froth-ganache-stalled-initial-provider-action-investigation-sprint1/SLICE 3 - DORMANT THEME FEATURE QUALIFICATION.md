# Slice 3 — dormant theme-feature qualification

**Status:** clean-wheel and installed-artifact qualification complete; final
release review pending.

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
5b18f4e25b12d92ca05ccd09e998a5f8051c69e1114a27a00ce5cbea35077de4
```

It was force-installed without dependencies into an existing isolated release
environment. `pip check` reported no broken requirements. A clean working
directory then confirmed that imported `assembly` and `extractor` modules came
from that environment's `site-packages`, not the source tree, before executing
the direct Ganache-shaped complete-assembly witness successfully.

## Release gate

Before tag/publication: obtain final review, commit the exact candidate source,
then rebuild from that commit and repeat the installed witness against the final
wheel. The existing public theme-policy qualification command is historical
policy evidence and is not used to claim this dormant-feature behavior.
