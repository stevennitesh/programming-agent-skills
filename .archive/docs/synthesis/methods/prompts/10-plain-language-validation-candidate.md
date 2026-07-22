# Prompt 10: Plain-Language Validation Candidate

Use this as Step 10 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to turn the detailed skill-context draft into the plain-language,
leading-word-heavy candidate that reality validation will actually test,
without editing runtime `SKILL.md`.

````markdown
We are converting a detailed skill-context draft into the plain-language
runtime candidate that will be validated against reality.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Facet or scope: `<facet-number-and-name, or whole skill>`
Detailed skill-context draft: `<path or paste Prompt 09 output>`
Draft decision: `<Prompt 09 draft decision>`
Traceability map and validation scenarios: `<Prompt 09 traceability map / scenarios>`
Existing skill text: `<path or paste relevant SKILL.md section>`
Revision feedback: `<optional feedback if rerunning this prompt; otherwise "none">`

Do not search for sources.
Do not reopen extraction, triage, agent bridge, full behavior synthesis, or
candidate runtime draft unless the detailed draft cannot be converted to plain
language safely.
Do not validate against real tasks yet.
Do not final-prune yet.
Do not edit `SKILL.md`.
Do not add unvalidated behavior.

Your job is to convert the gates to plain language, not flatten the taste. Collapse
explanatory prose into strong leading words, short commands, and observable
stop/done gates while preserving every behavior Prompt 09 says must be
validated.

Use `docs/synthesis/methods/plain-language-pass.md`.

Return:

## 1. Plain-Language Candidate Scope

State:

- skill and facet or scope;
- detailed skill-context draft used;
- Prompt 09 draft decision used;
- existing behavior that must not regress;
- what this pass will not decide.

If the draft decision is not `ready-for-plain-language-candidate`, do not continue.
Return to Prompt 09 or the earlier owning prompt named by the draft decision.

## 2. Revision Feedback Disposition

If `Revision feedback` is not `none`, account for it before compressing.

Use:

| Feedback Item | Affected Draft Area / Line IDs | Step 10 Action | Remaining Risk |
| --- | --- | --- | --- |

If there is no revision feedback, write:

`No revision feedback to disposition.`

## 3. Leading Word And Gate Plan

List the words and gates that will carry attention in the plain-language
candidate.

Use:

| Draft Meaning | Leading Word / Gate | Keep / Merge / Cut | Why |
| --- | --- | --- | --- |

Prefer strong professional words that recruit useful priors. Convert prose
definitions into gates only when the behavior remains checkable.

## 4. Plain-Language Candidate Text

Produce the exact candidate text that Prompt 11 should validate.

Use:

```markdown
<plain-language candidate SKILL.md text or replacement section>
```

This should be shorter than the Prompt 09 draft, but not final-pruned. It may
keep validation-visible lines that are likely to merge or disappear later if
they are needed for Prompt 11 evidence. Remove repeated runtime meaning here;
one leading word, one gate, and one consequence should carry each behavior.

## 5. Preservation Check

Map plain-language text back to Prompt 09 behavior.

Use:

| Prompt 09 Behavior / Line IDs | Preserved In Plain-Language Text | Risk |
| --- | --- | --- |

If any required behavior cannot survive plain language, choose
`return-to-detailed-skill-context-draft`.

## 6. Reality Validation Handoff

Map the plain-language candidate to validation scenarios.

Use:

| Plain-Language Candidate Area | Prompt 09/10 Validation IDs | What Prompt 11 Should Test First | Pass / Fail Signal |
| --- | --- | --- | --- |

Carry forward Prompt 09 validation IDs. Add a new stable ID only when Prompt 09
missed an existing behavior that must be preserved; mark it as Step 10-created.

## 7. Plain-Language Candidate Decision

Choose one:

- `ready-for-reality-validation`: Prompt 11 can validate the plain-language
  candidate;
- `return-to-detailed-skill-context-draft`: Prompt 09 must reassemble the draft because
  plain language cannot preserve placement, behavior, or traceability;
- `return-to-candidate-runtime-draft`: Prompt 08 must revise candidate wording, line
  IDs, or validation IDs;
- `blocked`: stop until the named owner, support-doc, or user decision is
  resolved.

End with:

- plain-language candidate decision;
- artifact path;
- text areas ready for validation;
- behavior or line IDs preserved;
- behavior or line IDs cut or merged and why;
- validation scenarios Prompt 11 should run first;
- likely final-prune targets after validation.

The plain-language candidate decision label must be explicit. Do not omit it.

Write the plain-language candidate to:

`docs/synthesis/facets/<skill-name>/FACET-<n>-<name>/10-plain-language-validation-candidate.md`
````

## Quality Bar

This prompt is complete when the version to validate is the strong
plain-language runtime candidate, not the explanatory detailed draft; every
compressed gate remains traceable; repeated runtime meaning has been removed;
and Prompt 11 can test the actual wording that might ship.
