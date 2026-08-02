# Targeted Polish Execution Contract

The handbook defines how to read, appreciate, judge, and edit. This document
defines the mechanics and evidence rules for this run.

## One decision per field

Return exactly one decision for every allowlisted path, with no omissions,
duplicates, or additional paths.

## Keep

Choose `keep` when the current value already fulfills its role or when a
proposed change would mainly make it shorter, safer, more generic, or more
uniform. Copy the current value verbatim into `replacement`.

Useful keep codes include:

- `keep_existing_peak`
- `keep_semantic_precision`
- `keep_voice_or_rhythm`
- `keep_richness`
- `keep_no_material_defect`

## Replace

Choose `replace` only when the new value materially addresses an applicable
diagnosis while preserving factual meaning and existing strengths.

Useful replacement codes include:

- `repair_lens_overlap`
- `restore_specificity`
- `improve_behavioral_grounding`
- `remove_repeated_mechanism`
- `differentiate_voice`
- `preserve_compound_semantics`
- `remove_true_overexplanation`

Copy every applicable diagnostic reason code and add appropriate editorial
decision codes.

## Coordinated diagnoses

Some diagnoses apply to a set rather than proving every member individually
defective. Individual members may be kept, but the completed decisions must
materially resolve the shared diagnosis.

- For repeated openings, retain strong exceptions only if the resulting set no
  longer feels architecturally repeated.
- For humor clusters, a strong individual joke may survive if enough other
  members change to restore meaningful comic variety.
- For summaries, compare individual fields and then evaluate all four complete
  summaries as a coordinated set with distinct theses, examples, implications,
  and language.
- For related compound renderings, preserve the supported interaction across
  the affected audience and density variants.

## Length

Use `CURRENT DECK LENGTH PROFILE.md` descriptively, not as a quota. Remain near
the current field’s scale unless its diagnosis identifies true
over-explanation or more space is required to restore supported meaning. Do
not shorten summaries merely because briefer paraphrases are possible.

## Evidence

- Summary fields may use the full chart.
- Ordinary cards may use only their corresponding rich claim evidence and
  projected-term context.
- Semantic neighbors establish distinction but do not donate facts.
- Read-only prose supplies continuity and comparison but is not additional
  evidence.
- Supported semantic contributions may be recovered or clarified; new
  interpretations may not be invented.

## Locked material and output

All unlisted prose and all identity, structural, categorical, evidentiary, and
selection data are locked.

Return strict JSON matching the supplied response schema. For `keep`, the
replacement must exactly equal the current value. For `replace`, it must be a
nonempty materially revised value.
