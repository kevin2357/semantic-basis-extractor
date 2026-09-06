# Four-run checkpoint coordinate request

## Requested decision

Please review the complete four-run campaign in `FOUR-RUN AUDIT MANIFEST.json`
and provide one consolidated coordinate packet and authorization decision.

Three members are already complete and require no further R2 operation:

| Run | Coordinate | Local archive | Fresh R2 operations |
| --- | --- | --- | ---: |
| Doughmeat Dunsinane | generation 11, fully pinned | archive SHA reverified locally | 0 |
| Lady Macaron MacLean | generation 11, fully pinned | archive SHA reverified locally | 0 |
| Frisbee Fandango | generation 11, fully pinned | archive SHA reverified locally | 0 |

The only incomplete member is Marauding Madeleine:

- API run `98d2819f-4807-4f13-9b73-9bc8e8d2e1f5`;
- native run `064c17a411af2df9670372d1e6d1cf71880d2f1c0d5d92b0682e3da751696965`;
- latest native result known to API: `review_required / final_qa_requires_review`;
- six initial Responses and one polish Response are already preserved locally;
- missing evidence: the exact final checkpoint coordinate and its retained
  assembled-deck, validation, lint, accepted-pass, polish, result, and receipt
  members.

Please supply Madeleine's exact immutable checkpoint identity, including:

- checkpoint ID and generation;
- storage object UUID and exact object key;
- provider version / ETag;
- archive byte size and SHA-256;
- inventory SHA-256;
- compatibility identity and logical restore root; and
- exact sealed result/receipt identities and digests where API retained them.

## Requested access envelope

After coordinate review, authorize exactly:

- one conditional `HEAD` of Madeleine's named object; and
- one conditional, size-bounded `GET` of that same object if the HEAD matches.

No object listing, alternate-object discovery, writes, deletion, provider calls,
reconciliation, recovery, run mutation, or API/database mutation is requested.
The other three archives must not be fetched again. The operations need not be
performed simultaneously; this request freezes the full campaign up front so
later investigation does not require one authorization round per subject.

## Review gate

Voof-paws 1 remains closed until the consolidated packet confirms all four run
identities and the owner/API approve the single missing `HEAD`/`GET` pair.
