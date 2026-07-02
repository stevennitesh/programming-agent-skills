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
Compact draft: `<path or paste Prompt 08 output, including line inventory,
placement targets, runtime weights, and minimal runtime core if present>`
Generous synthesis: `<path or paste Prompt 07 output>`
Existing skill text to preserve: `<path or paste relevant SKILL.md section>`
Relevant owners to check:
- Engineering contract: `<path>`
- Related skills: `<paths>`
- Support docs: `<paths>`
Revision feedback: `<optional feedback if rerunning this prompt; otherwise "none">`

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
- Prompt 08 line inventory, placement, runtime weights, and minimal core used;
- existing skill behavior that must not regress;
- related owners checked;
- what this audit will not decide.

## 2. Revision Feedback Closure

If `Revision feedback` is not `none`, verify that the revised compact draft
closed it.

Use:

| Feedback Item | Affected Line IDs | Closed / Still Risky / Not Closed | Evidence In Draft | Next Action |
| --- | --- | --- | --- | --- |

If any feedback is `Not Closed`, the audit decision cannot be
`ready-for-validation-draft`.

If there is no revision feedback, write:

`No revision feedback to close.`

## 3. Candidate Line Inventory

Break the compact draft into auditable lines.

Use:

| Line ID | Candidate Line | Section | Function | Prompt 08 Placement | Prompt 08 Runtime Weight |
| --- | --- | --- | --- | --- | --- |

Preserve Prompt 08 line IDs when they exist. If IDs are missing, assign stable
IDs and flag that as a Prompt 08 weakness.

Functions:

- invocation
- step
- hard gate
- recheck
- completion criterion
- stop/ask rule
- ownership guard
- handoff
- context pointer
- support/reference
- meta decision
- other

Do not treat a meta decision, such as `No runtime pointer proposed yet`, as
runtime wording to validate. Audit it in the relevant placement or pointer
section.

## 4. Line-By-Line Behavior Audit

Use:

| Line ID | Behavior Changed? | Failure Prevented | Evidence Required | Verdict | Reason |
| --- | --- | --- | --- | --- | --- |

Verdicts:

- `keep-for-validation`
- `keep-but-prune-watch`
- `revise-before-draft`
- `move-to-support`
- `owned-elsewhere`
- `cut`
- `not-runtime-line`

A runtime line should not get `keep-for-validation` unless it changes behavior
or preserves a critical existing behavior. Use `keep-but-prune-watch` when the
line should be validated but is likely to shrink, merge, or disappear during
final pruning.

## 5. Placement And Runtime Weight Audit

Check Prompt 08's placement and runtime-weight proposal.

Use:

| Line ID | Prompt 08 Placement / Weight | Audit Verdict | Reason | Revision Direction |
| --- | --- | --- | --- | --- |

Ask:

- should this line be inline runtime, merged with existing text, support-only,
  owned elsewhere, or cut?
- does the minimal runtime core contain every behavior that must be validated?
- does the audit expansion include lines that are useful only for validation or
  final-prune watch?
- does the proposed placement duplicate existing `SKILL.md`, related skills,
  contracts, or support docs?

## 6. No-Op And Weak Language Check

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

## 7. Gate Strength Check

Use:

| Line ID | Gate | Too Weak If | Too Heavy If | Revision Direction |
| --- | --- | --- | --- | --- |

A good gate should be observable and hard to evade.

## 8. Ownership / Duplication Check

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

## 9. Context Pointer Check

Use:

| Line ID Or Decision | Inline / Pointer / No Pointer / Not Runtime | Target If Pointer | Why | Risk |
| --- | --- | --- | --- | --- |

Prefer inline only when most invocations need the material. Move
branch-specific or bulky reference behind a pointer.

## 10. Leading Word Check

Use:

| Line ID | Leading Word | Strong / Weak | Why | Action |
| --- | --- | --- | --- | --- |

Keep leading words that recruit useful priors. Cut or replace words that only
decorate.

## 11. Regression Check

Compare the candidate wording against existing skill behavior.

Use:

| Existing Behavior | Preserved? | Candidate Line(s) | Risk |
| --- | --- | --- | --- |

Flag any existing behavior that may be weakened or lost.

## 12. Revised Candidate Line Set

Create the audit-approved line set.

Use:

### Keep For Validation

- `<line id>`: `<line>`

### Keep But Prune-Watch

- `<line id>`: `<line / prune risk>`

### Revise Before Validation

- `<line id>`: `<revision direction>`

### Move To Support

- `<line id>`: `<target / reason>`

### Owned Elsewhere

- `<line id>`: `<owner / reason>`

### Cut

- `<line id>`: `<reason>`

### Not Runtime Lines

- `<line id or decision>`: `<where it was audited instead>`

## 13. Handoff To Validation Draft

End with:

- audit decision:
  - `ready-for-validation-draft`: Prompt 10 can assemble a validation draft;
  - `revise-before-draft`: feed the revised line set back through Prompt 08
    before Prompt 10;
  - `blocked`: source, ownership, or scope conflict must be resolved before
    compaction continues;
- lines ready for validation-draft assembly;
- lines that must be revised before draft assembly;
- scenario-ready validation tasks tied to line IDs for Prompt 10 to preserve;
- regression risks to test;
- likely final-prune targets.

Use:

| Validation ID | Line IDs | Scenario Or Fixture Needed | Behavior / Gate To Test | Regression Risk |
| --- | --- | --- | --- | --- |

If the decision is `revise-before-draft`, do not assemble or validate the raw
compact draft. Use the audit-approved revision directions as the next Prompt 08
input and produce a revised compact draft first.

Write the behavior audit to:

`docs/synthesis/facets/<skill-name>/FACET-<n>-<name>/09-behavior-audit.md`
````

## Quality Bar

This prompt is complete when each candidate runtime line has a verdict, weak
language is exposed, ownership is checked, gate strength is assessed, and the
next step is unambiguous: either Prompt 10 validation-draft assembly, a Prompt
08 revision loop, or a blocked decision.
