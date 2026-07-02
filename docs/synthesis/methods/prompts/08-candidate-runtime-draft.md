# Prompt 08: Candidate Runtime Draft

Use this as Step 8 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to turn full behavior synthesis into detailed-draft-ready
candidate runtime lines without editing `SKILL.md` or treating the draft as
final plain language.

````markdown
We are drafting candidate runtime skill wording from full behavior synthesis.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Facet or scope: `<facet-number-and-name, or whole skill>`
Full behavior synthesis artifact(s): `<path or paste one Prompt 07 output, or multiple completed facet outputs for whole-skill integration>`
Synthesis decision: `<Prompt 07 synthesis decision>`
Behavior flow artifact(s): `<path or paste matching Prompt 06 output(s)>`
Existing skill text to preserve: `<path or paste relevant SKILL.md section>`
Relevant owners to preserve:
- Engineering contract: `<path>`
- Tracker docs: `<paths>`
- Related skills: `<paths>`
- Support docs: `<paths>`
Revision feedback: `<optional feedback if rerunning this prompt; otherwise "none">`

Do not search for sources.
Do not reopen extraction or triage.
Do not revise the full behavior synthesis or agent bridge here.
Do not edit `SKILL.md` yet.
Do not claim this wording is final.
Do not assemble the detailed skill-context draft yet.
Do not run the plain-language pass yet.
Do not validate against real tasks yet.

Your job is to produce candidate skill lines that Prompt 09 can assemble into
a detailed skill-context draft. Keep the meaning explicit enough for behavior,
ownership, and placement review. Prompt 10 owns the plain-language pass after
the detailed draft is assembled.

Return:

## 1. Candidate Draft Scope

State:

- facet or skill scope being drafted;
- full behavior synthesis input used;
- Prompt 07 synthesis decision used;
- existing skill text that must be preserved;
- behavior this draft must make predictable;
- what this draft must not decide.

If the synthesis decision is not `ready-for-candidate-runtime-draft`, do not continue.
Return to Prompt 07 or the earlier owning prompt named by the synthesis
decision.

## 2. Prompt 07 Handoff Check

Account for the full behavior synthesis handoff before drafting runtime prose.

Use:

| Handoff Item | Prompt 07 Direction | Step 08 Disposition | Risk For Prompt 09 |
| --- | --- | --- | --- |

Include:

- synthesis decision;
- candidate draft contract items that must be preserved;
- material Prompt 07 allowed Step 08 to compress into candidate lines;
- material Prompt 07 said to demote to support or research-only;
- candidate runtime budget;
- typed gates and branch exits that must survive candidate drafting;
- design questions that were resolved, deferred, or blocked.

If the Prompt 07 handoff is missing or too vague to draft safely, choose
`revise-full-behavior-synthesis` in the detailed-draft handoff.

## 3. Revision Feedback Disposition

If `Revision feedback` is not `none`, account for it before drafting.

Use:

| Feedback Item | Affected Line IDs Or Sections | Step 08 Action | Remaining Draft Risk |
| --- | --- | --- | --- |

Stable line IDs from an earlier candidate runtime draft should stay stable unless a line
is cut or replaced. If an ID changes, record the old ID, new ID, and reason.

If there is no revision feedback, write:

`No revision feedback to disposition.`

## 4. Owner Boundary Scan

Identify owner conflicts before drafting candidate runtime lines.

Use:

| Owner | Owned Behavior | Step 08 May Draft | Step 08 Must Not Draft | Candidate Impact |
| --- | --- | --- | --- | --- |

Include relevant owners such as the existing skill section, engineering
contract, tracker docs, related skills, support docs, later steps in the same
skill, and user decisions.

This is a lightweight scan. Prompt 09 owns the full placement and owner-boundary
assembly check, but Prompt 08 should not knowingly draft lines owned elsewhere.
If drafting exposes an unresolved owner conflict, choose `blocked`,
`revise-full-behavior-synthesis`, or `revise-agent-bridge` in the handoff.

## 5. Candidate Drafting Principles

List the principles used to draft candidate runtime lines.

Include:

- what strong leading words must survive;
- what explanatory prose should be cut;
- what belongs behind context pointers;
- what gates and consequences must remain checkable;
- what should stay research-only.

Do not convert the wording to plain language here. Prompt 10 owns that pass.

## 6. Candidate Invocation / Description Wording

Only include this section if the facet affects skill invocation.

Draft candidate description text.

Use:

```markdown
description: <candidate description>
```

Then explain:

- trigger branch it serves;
- words that improve invocation;
- wording cut from the current description, if any;
- risk to preserve in the detailed draft.

If invocation is not affected, write:

`No invocation wording change proposed.`

## 7. Candidate Runtime Steps

Draft candidate `SKILL.md` wording for the facet.

Use skill-shaped candidate prose, not research notes or final runtime prose.

Assign stable line IDs to each candidate runtime line or gate. Use short IDs
that survive feedback loops, such as `B1`, `P3`, or `F2`.

For each candidate step:

```markdown
### <candidate heading>

[<Line ID>] <compact instruction text>

[<Line ID>] Done when <checkable completion criterion>.
```

Each step should:

- use active verbs;
- contain one main instruction per sentence where possible;
- include explicit conditions;
- preserve strong leading words;
- end with or include a checkable gate when relevant.

## 8. Candidate Line Inventory And Placement

Inventory every candidate runtime line, including invocation lines, gates,
completion criteria, and context pointers.

Use:

| Line ID | Candidate Line | Function | Placement / Merge Target | Prompt 07 Source | Runtime Weight | Draft Risk |
| --- | --- | --- | --- | --- | --- | --- |

Use these function labels when they fit:

- `description`;
- `step`;
- `hard gate`;
- `recheck`;
- `completion criterion`;
- `stop/ask rule`;
- `ownership guard`;
- `handoff`;
- `context pointer`.

Use these placement labels when they fit:

- `insert`;
- `replace`;
- `merge with <existing heading or line>`;
- `keep existing`;
- `owned elsewhere`;
- `defer to support`;
- `cut`.

Use these runtime weights:

- `must-runtime`;
- `candidate-runtime`;
- `support-only`;
- `research-only`;
- `likely-prune`.

The runtime weight label must be one of the values above. Do not invent
near-synonyms.

This is a placement draft, not a final patch. Do not edit `SKILL.md`.

## 9. Candidate Gate Consequences

List the gate and branch consequences that must remain checkable.

Use:

| Line ID | Candidate Line | Purpose | Failure Prevented |
| --- | --- | --- | --- |

Examples of consequence shapes:

- `Stop when <condition>.`
- `Ask only when <commitment boundary>.`
- `Done means <observable evidence>.`
- `<condition> waits unless <exception>.`

These are candidate consequences, not plain-language lines. Prompt 10 may
later make them blunter after Prompt 09 assembles the detailed draft.

## 10. Context Pointer Candidates

Identify material that should move behind a pointer rather than stay inline.

Use:

| Line ID | Pointer Text | Target Support Doc | Why It Should Be Disclosed | When Agent Should Open It |
| --- | --- | --- | --- | --- |

Do not create support docs yet unless the user explicitly asked.

## 11. Minimal Runtime Core

Name the smallest likely runtime patch separately from the fuller validation
draft detail.

Use:

| Line ID | Runtime Core / Validation Detail / Support / Cut | Why |
| --- | --- | --- |

Use these core classes exactly:

- `Runtime Core`;
- `Validation Detail`;
- `Support`;
- `Cut`.

The runtime core should contain only lines likely to survive final pruning.
The validation detail may contain lines that Prompt 09 should place and Prompt
10 may later merge or compress before validation.

## 12. Cut / Preserve Log

Record compression decisions.

Use:

| Material | Cut / Preserve / Move | Why |
| --- | --- | --- |

This is not final prune and not the plain-language pass. It is a draft
candidate log.

## 13. Candidate Runtime Draft

Assemble the best candidate wording in one block.

Use:

```markdown
<candidate skill text>
```

This block should be ready for Prompt 09 to assemble into a detailed draft,
not ready to ship.

## 14. Detailed Draft Handoff

End with:

- candidate-draft decision:
  - `ready-for-detailed-skill-context-draft`: continue to Prompt 09;
  - `revise-full-behavior-synthesis`: return to Prompt 07 because drafting would
    lose taste, gates, or placement decisions;
  - `revise-agent-bridge`: return to Prompt 06 because candidate lines expose
    sequence, branch, or ownership problems;
  - `blocked`: stop until the named owner, support-doc, or user decision is
    resolved;
- lines most likely to be no-ops;
- lines most likely to duplicate another skill or contract;
- line IDs whose placement or runtime weight is most uncertain;
- owner conflicts or owner-boundary risks;
- gates most likely to be too weak;
- gates most likely to be too heavy;
- context-pointer decisions to preserve or defer;
- existing skill behavior that must not regress;
- validation scenario seeds to remember.

The candidate-draft decision label must be explicit. Do not omit it.

Write the candidate runtime draft to:

`docs/synthesis/facets/<skill-name>/FACET-<n>-<name>/08-candidate-runtime-draft.md`
````

## Quality Bar

This prompt is complete when Prompt 09 has concrete candidate runtime lines to
assemble into a detailed skill-context draft with behavior, no-op, duplication,
gate, ownership, and context-pointer risks visible, or when it names the
synthesis/bridge loop needed before detailed-draft assembly.

Completion requires:

- the Prompt 07 synthesis decision is `ready-for-candidate-runtime-draft`;
- every Prompt 07 candidate draft contract item is preserved, compressed, demoted,
  deferred, or blocked;
- every candidate runtime line has a stable line ID;
- every candidate line uses an allowed runtime weight;
- every Minimal Runtime Core row uses an allowed core class;
- owner-boundary risks are recorded before Prompt 09;
- no detailed draft assembly, plain-language compression, reality
  validation, final prune, or `SKILL.md` edit has happened.
