# AstroWoof Natal Authoring 0.4.6 Known Limitations

- Bounded Batch covers initial authoring and creative retries. Polish, qualitative
  critic, and qualitative candidate remain interactive Responses operations.
- Legacy bounded one-operation v1 runs cannot resume as six-pass v2 runs.
- A provider submission interrupted before its provider identity is durably known
  has an irreducible atomicity gap and remains ambiguous/fail-closed.
- Missing Batch member usage retains consumer billing authority; SBE does not infer
  a zero or partial final charge.
- Packaged route traces are adoption evidence, not authoritative run history.
- Unknown-time claim suppression, variable basis sizes, Quick/Complete modes,
  hierarchy redesign, and critic product policy remain deferred.
