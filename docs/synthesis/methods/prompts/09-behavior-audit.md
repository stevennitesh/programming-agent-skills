# Prompt 09: Behavior Audit

Use this as Step 9 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to audit compact candidate skill wording line by line before
validation, final pruning, or runtime `SKILL.md` edits.

````markdown
We are auditing compact candidate skill wording before validation or final
edits.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Facet or scope: `<facet-number-and-name, or whole skill>`
Compact draft: `<path or paste Prompt 08 output>`
Generous synthesis: `<path or paste Prompt 07 output>`
Existing skill text to preserve: `<path or paste relevant SKILL.md section>`
Relevant owners to check:
- Engineering contract: `<path>`
- Related skills: `<paths>`
- Support docs: `<paths>`

Do not search for sources.
Do not rewrite the full skill.
Do not edit `SKILL.md` yet.
Do not validate against real tasks yet.
Do not final-prune yet.

Your job is to audit every candidate runtime line for behavior change,
ownership, gate strength, and context load.

Use this test for each line:

```text
Does this change agent behavior?
What failure mode does it prevent?
What proof or evidence does it require?
Is it already owned elsewhere?
Is it a leading word, a gate, or a no-op?
Is it duplicated, bloated, or better behind a context pointer?
```

Return:

## 1. Audit Scope

State:

- facet or skill scope being audited;
- compact draft used;
- existing skill behavior that must not regress;
- related owners checked;
- what this audit will not decide.

## 2. Candidate Line Inventory

Break the compact draft into auditable lines.

Use:

| Line ID | Candidate Line | Section | Type |
| --- | --- | --- | --- |

Types:

- invocation
- step
- gate
- completion criterion
- stop/ask rule
- context pointer
- support/reference
- report/handoff
- other

## 3. Line-By-Line Behavior Audit

Use:

| Line ID | Behavior Changed? | Failure Prevented | Evidence Required | Verdict | Reason |
| --- | --- | --- | --- | --- | --- |

Verdicts:

- `keep`
- `revise`
- `move-to-support`
- `owned-elsewhere`
- `cut`

A line should not get `keep` unless it changes behavior or preserves a critical
existing behavior.

## 4. No-Op And Weak Language Check

Use:

| Line ID | Weakness | Why It Is Weak | Stronger Direction |
| --- | --- | --- | --- |

Look for:

- polite mush
- generic advice
- "be careful" wording
- decorative vocabulary
- vague quality claims
- uncheckable completion language
- lines that describe rather than steer

## 5. Gate Strength Check

Use:

| Line ID | Gate | Too Weak If | Too Heavy If | Revision Direction |
| --- | --- | --- | --- | --- |

A good gate should be observable and hard to evade.

## 6. Ownership / Duplication Check

Use:

| Line ID | Possible Duplicate Owner | Conflict Or Duplication | Action |
| --- | --- | --- | --- |

Possible owners:

- engineering contract
- another skill
- repo `AGENTS.md`
- support/reference doc
- domain docs
- ADR
- runtime skill

## 7. Context Pointer Check

Use:

| Line ID | Inline Or Pointer? | Target If Pointer | Why | Risk |
| --- | --- | --- | --- | --- |

Prefer inline only when most invocations need the material. Move
branch-specific or bulky reference behind a pointer.

## 8. Leading Word Check

Use:

| Line ID | Leading Word | Strong / Weak | Why | Action |
| --- | --- | --- | --- | --- |

Keep leading words that recruit useful priors. Cut or replace words that only
decorate.

## 9. Regression Check

Compare the candidate wording against existing skill behavior.

Use:

| Existing Behavior | Preserved? | Candidate Line(s) | Risk |
| --- | --- | --- | --- |

Flag any existing behavior that may be weakened or lost.

## 10. Revised Candidate Line Set

Create the audit-approved line set.

Use:

### Keep

- `<line id>`: `<line>`

### Revise

- `<line id>`: `<revision direction>`

### Move To Support

- `<line id>`: `<target / reason>`

### Owned Elsewhere

- `<line id>`: `<owner / reason>`

### Cut

- `<line id>`: `<reason>`

## 11. Handoff To Validation

End with:

- lines ready for validation;
- lines that must be revised before validation;
- behaviors that need real-task validation;
- gates that need real-task validation;
- regression risks to test;
- likely final-prune targets.

Write the behavior audit to:

`docs/synthesis/compact/skill-facets/<skill-name>/FACET-<n>-<name>-behavior-audit.md`
````

## Quality Bar

This prompt is complete when each candidate runtime line has a verdict, weak
language is exposed, ownership is checked, gate strength is assessed, and the
validation step knows exactly what behavior and regressions to test.
