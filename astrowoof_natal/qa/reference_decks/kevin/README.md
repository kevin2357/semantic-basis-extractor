# Kevin Reference Decks

Kevin is represented as a male Golden Retriever using `params.json`. His
versions cover multi-subject authoring, compact authoring, independently
authored pass assembly, and the first optimized automated semantic-closure run.

`20260730-six-pass-final` is the manual-process comparison reference.
`20260801-automated-live-polish-1` is the strongest preserved candidate from
the pre-20260802 automated run, although that run ended in final QA failure due
to metadata/polish-control defects later fixed in the pipeline.

`selected-authoring-packet.json` is the packet from that automated live run and
is the preferred validator basis for current Kevin comparisons.

`20260804-k7-mechanical` is the current controlled Phase-5 mechanical-polish
reference. It derives from an immutable fresh K6 baseline, passes structural
validation, and has zero whole-deck lint warnings. Use it as the source for K8
qualitative diagnosis and candidate comparison, not as evidence that advisory
validator warnings were repaired.

`20260804-k8-qualitative-candidate` is a non-production research candidate
derived from K7. It preserves the critic's upstream/local diagnosis and seven
bounded edits. Use it for comparative review; do not treat it as promoted gold
or a replacement for K7.
