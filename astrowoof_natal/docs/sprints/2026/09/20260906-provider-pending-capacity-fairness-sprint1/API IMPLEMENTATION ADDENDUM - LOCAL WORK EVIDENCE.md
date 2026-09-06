# API implementation addendum — exact local-work evidence

The Voof-paws 3 direction remains approved. This is an implementation precision
note, not a request for SBE code or schema work.

`local_work_ready` in the joint prose names the intended posture. The persisted
v0.7 API local-work reader represents the exact first-release predicate as:

- `execution_branch_command == ordinary_resume`;
- `execution_capacity_disposition == continue_local_cycle`;
- `local_work_ready_now == true`; and
- `execution_capacity_reason_code == ordinary_local_continuation_ready`.

This matters because `ordinary_resume` by itself is not enough. Further, where
the v0.7 decision retains provider custody, the existing runtime already
requires a matching v0.8 retry-lineage successor before it treats the local
operation as safe. API Slice 4 will preserve that join rather than rotating
from a v0.7 observation alone.

No naming or contract change is requested from SBE. The API implementation and
its negative cases will make the exact persisted-reader predicates explicit.
