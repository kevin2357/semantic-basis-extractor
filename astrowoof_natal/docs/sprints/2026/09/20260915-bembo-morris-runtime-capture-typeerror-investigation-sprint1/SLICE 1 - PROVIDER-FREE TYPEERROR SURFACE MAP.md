# Slice 1 — provider-free TypeError surface map

## Result

Provider-free evidence does not identify one witness defect. It does prove the
public function has two escaping `TypeError` classes that the live normalized
event cannot distinguish. The ordinary delivery/review fixture suite passes,
so an exact retained-workspace reproduction is the next narrow step.

## Executable boundary matrix

The retained `provider_free_boundary_matrix.py` injected only exception classes
and minimum public identities; it retained no exception prose or workspace
contents.

| Boundary | Injection | Public result | Shared/route-specific |
| --- | --- | --- | --- |
| Pre-assembly evidence collection | collector raises `TypeError` | `TypeError` escapes | shared |
| Within packet assembly | first `_load` raises `TypeError` | typed `unsupported` / `incomplete_native_evidence` | shared at this point; later operations vary |
| Typed-status construction | assembly raises `ValueError`, status helper raises `TypeError` | second `TypeError` escapes and masks the first failure | shared |

Recorded output:

```text
pre_assembly_collect escaped TypeError
within_assembly returned unsupported incomplete_native_evidence
typed_status_construction escaped TypeError
```

The focused public fixture module ran 11 tests successfully. It is already
listed in `astrowoof_natal/tests/test_suite_manifest.json`; no new product test
was added in this investigatory slice.

## Source-backed candidate map

`build_editorial_review_runtime_capture()` invokes
`collect_editorial_review_runtime_evidence()` before entering its assembly
`try`. Therefore TypeErrors from the following operations escape directly:

- exact native result/receipt/snapshot reading and validation;
- mapping access during eligibility and exact-source selection;
- spend-ledger action indexing (`item.get` and duplicate construction);
- pass ordering and attempt iteration;
- logical-path conversion, especially `.replace()` on a non-string persisted
  path;
- binding canonicalization and digesting; and
- candidate-workspace traversal/digest construction.

Those are shared candidates except the review-only action-disposition map and
join, which can independently fail while delivery skips it. The same normalized
class in the two witnesses therefore narrows the language-level failure class,
but does not prove one expression.

Inside the assembly `try`, structural `KeyError`, `TypeError`, `ValueError`,
`OSError`, and JSON decode errors are intentionally translated to typed
`incomplete_native_evidence`. However, `_runtime_capture_status()` is called
inside that exception handler and is not protected by another guard. A
TypeError during status construction or exact-native validation escapes and can
hide the assembly exception that selected the handler.

## Contract ruling

The public function promises a packet branch or one typed no-packet status for
incomplete native evidence. A valid but incomplete evidence condition should
therefore not escape merely because an operation assumes the wrong type. That
does not justify broad normalization yet: malformed native contracts and a
double-fault in status construction have materially different ownership and
fail-closed implications.

## Review Gate A recommendation

Slices 0–1 do not prove a correction. Request one immutable, hash-pinned
coordinate packet for each exact witness and, only after separate owner
authorization, one conditional HEAD and one bounded GET per checkpoint. The
read-only reproduction should invoke exact reader, eligibility, collector, and
public capture independently and retain only first failing frame names/line
numbers and exception class. No R2 read is authorized by this result.

