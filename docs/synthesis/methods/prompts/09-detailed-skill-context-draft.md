# Prompt 09: Detailed Skill-Context Draft

Use this as Step 9 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to assemble Prompt 08 candidate wording into a detailed
skill-context draft before the plain-language pass, without editing runtime
`SKILL.md`.

````markdown
We are assembling a detailed skill-context draft from candidate skill wording.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Facet or scope: `<facet-number-and-name, or whole skill>`
Candidate runtime draft: `<path or paste Prompt 08 output>`
Candidate-draft decision: `<Prompt 08 candidate-draft decision>`
Existing skill text: `<path or paste relevant SKILL.md section>`
Relevant owners to preserve:
- Engineering contract: `<path>`
- Tracker docs: `<paths>`
- Related skills: `<paths>`
- Support docs: `<paths>`
Revision feedback: `<optional feedback if rerunning this prompt; otherwise "none">`

Do not search for sources.
Do not reopen extraction, triage, agent bridge, or full behavior synthesis.
Do not run the plain-language pass yet.
Do not validate against real tasks yet.
Do not final-prune yet.
Do not edit `SKILL.md`.
Do not add unapproved runtime behavior.

Your job is to merge Prompt 08 candidate lines into an integrated detailed
draft that carries all useful detail into skill context before plain-language
compression. This draft may be more explicit than final runtime text because
Prompt 10 will collapse it into the candidate that reality validation will
test.
Preserve definitions, examples, consequences, and placement notes that Prompt
10 and Prompt 11 need, even when they are too wordy for final runtime.

Return:

## 1. Draft Scope

State:

- facet or skill scope being assembled;
- candidate runtime draft used;
- existing `SKILL.md` text used as the base;
- Prompt 08 candidate-draft decision used;
- what this draft must preserve;
- what this draft will not decide.

If the candidate-draft decision is not `ready-for-detailed-skill-context-draft`, do not
continue. Return to Prompt 08 or the earlier owning prompt named by the
candidate runtime draft.

## 2. Revision Feedback Disposition

If `Revision feedback` is not `none`, account for it before assembling.

Use:

| Feedback Item | Affected Line IDs Or Sections | Step 9 Action | Remaining Risk |
| --- | --- | --- | --- |

If there is no revision feedback, write:

`No revision feedback to disposition.`

## 3. Owner Boundary Check

Map the owners that must remain outside this draft before assembling runtime
prose.

Use:

| Owner | Owned Behavior | Prompt 09 May Use | Prompt 09 Must Not Inline | Draft Action |
| --- | --- | --- | --- | --- |

Include relevant owners such as the existing skill section, engineering
contract, tracker docs, related skills, support docs, later steps in the same
skill, and user decisions.

If preserving an owner boundary requires a pointer or placeholder, record it
here and again in Section 9. If the boundary cannot be preserved, choose
`blocked` or `revise-candidate-runtime-draft` in the draft decision.

## 4. Candidate Input

List the Prompt 08 line sets being assembled. Use Prompt 08's Candidate Line
Inventory, Minimal Runtime Core table, Candidate Runtime Draft, and Handoff
risk notes as inputs.

Use:

| Line ID | Prompt 08 Runtime Weight | Prompt 08 Core Class | Prompt 08 Placement | Candidate Line Or Decision | Step 9 Treatment |
| --- | --- | --- | --- | --- | --- |

Use Prompt 08 runtime weights exactly:

- `must-runtime`;
- `candidate-runtime`;
- `support-only`;
- `research-only`;
- `likely-prune`.

Use Prompt 08 core classes exactly when they are present:

- `Runtime Core`;
- `Validation Detail`;
- `Support`;
- `Cut`.

Assemble `must-runtime`, `candidate-runtime`, `Runtime Core`, and
`Validation Detail` lines when they can be placed without duplication or owner
drift. Record `support-only`, `research-only`, `likely-prune`, `Support`,
`Cut`, owned-elsewhere, and not-runtime lines so they do not silently re-enter
the draft.

Prompt 09 may create or refine validation scenario IDs for existing behavior
preservation, placement risk, or regression risk. It must not create new
runtime obligations that were not present in Prompt 08 or existing skill
behavior.

## 5. Placement And Merge Map

Map each assembled line to the existing skill text.

Use:

| Line ID | Existing Location | Draft Action | Why This Placement Preserves Behavior |
| --- | --- | --- | --- |

Draft actions:

- `insert`;
- `replace`;
- `merge`;
- `keep existing`;
- `support placeholder`;
- `not assembled`.

If a line cannot be placed without duplication or weakening existing behavior,
choose `revise-candidate-runtime-draft` or `blocked` in the draft decision.

## 6. Preserved Existing Behavior

Show how the draft protects behavior that already exists.

Use:

| Existing Behavior | Preserved By Draft Location / Line ID | Regression Risk |
| --- | --- | --- |

This section should catch accidental loss of invocation, context intake,
proof, review, cleanup, commit, or support-doc behavior.

## 7. Detailed Skill-Context Draft

Produce the integrated detailed draft as a patch-shaped or section-shaped
artifact.

Use:

```markdown
<detailed skill-context draft text or replacement section>
```

The draft should read like skill text, not research notes, but it does not need
to be the smallest or plainest runtime wording yet. Keep candidate line IDs out
of the runtime prose unless the project explicitly wants them there. Use
surrounding tables in this artifact for traceability.

This section should carry all detail needed for detailed-draft quality:
definitions, concrete consequences, branch outcomes, owner boundaries,
regression protections, and any examples needed to prevent misreading. Do not
collapse those details into plain language yet; Prompt 10 owns that pass. Do
not repeat the same meaning in runtime prose; put repeated IDs and source
traceability in tables.

## 8. Traceability Map

Map draft locations back to candidate lines and validation scenarios.

Use:

| Draft Location / Heading | Line IDs | Validation IDs | What Prompt 10 Must Preserve For Prompt 11 |
| --- | --- | --- | --- |

Create stable validation IDs here if Prompt 08 did not provide them.

Only create new validation IDs for existing behavior preservation, placement
risk, or regression risk. Mark any such IDs as Prompt 09-created and explain
which existing behavior they protect.

## 9. Support Pointer Placeholders

Record any support/context-pointer decisions that the draft depends on.

Use:

| Pointer Or Placeholder | Draft Location | Target If Validated | Why It Is Not Created Yet |
| --- | --- | --- | --- |

Do not create support docs yet unless the user explicitly asked.

## 10. Draft Decision

Choose one:

- `ready-for-plain-language-candidate`: Prompt 10 can produce the plain-language
  candidate that Prompt 11 will validate;
- `revise-candidate-runtime-draft`: return to Prompt 08 because candidate wording cannot
  be assembled cleanly;
- `blocked`: stop until the named owner, support-doc, or user decision is
  resolved.

End with:

- draft decision;
- draft artifact path;
- line IDs assembled;
- line IDs not assembled and why;
- owner boundaries preserved or blocked;
- validation scenarios Prompt 10 must preserve for Prompt 11;
- placement conflicts or residual risks.

The draft decision label must be explicit. Do not omit it.

Write the detailed draft to:

`docs/synthesis/facets/<skill-name>/FACET-<n>-<name>/09-detailed-skill-context-draft.md`
````

## Quality Bar

This prompt is complete when the Prompt 08 candidate lines have been integrated
into a detailed skill-context draft with traceable placement, repeated runtime
meaning removed, existing behavior preserved, and Prompt 10 can convert the
gates to plain language without rediscovering where the candidate wording
belongs.

Completion requires:

- the Prompt 08 candidate-draft decision is `ready-for-detailed-skill-context-draft`;
- every Prompt 08 line is assembled, not assembled, support-placeholdered,
  owned-elsewhere, or cut;
- Prompt 08 runtime weights and core classes are preserved or explicitly
  translated;
- every owner boundary at risk has a draft action;
- every existing behavior at risk has a preservation note;
- every validation scenario maps to draft text;
- no repeated meaning remains in the draft runtime prose;
- no plain-language compression, reality validation, final prune, or
  `SKILL.md` edit has happened.
