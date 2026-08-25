# Background

Temporal lifecycle v0.6 separated immutable native checkpoint basis from
clock-relative scheduling decisions. Its `external_authority_request.v2`
correctly identifies the exact native state for which external authority is
needed, but a request identity is not itself an executable grant. This sprint
adds the missing constrained continuation seam without weakening that separation.
