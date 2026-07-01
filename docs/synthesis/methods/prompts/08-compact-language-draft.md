# Prompt 08: Compact Language Draft

Use this as Step 8 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to compact generous synthesis into audit-ready candidate runtime
skill language without editing `SKILL.md` or treating the draft as final.

````markdown
We are compacting generous synthesis into candidate runtime skill wording.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Facet or scope: `<facet-number-and-name, or whole skill>`
Generous synthesis: `<path or paste Prompt 07 output>`
Behavior flow: `<path or paste Prompt 06 output>`
Existing skill text to preserve: `<path or paste relevant SKILL.md section>`

Do not search for sources.
Do not reopen extraction or triage.
Do not edit `SKILL.md` yet.
Do not claim this wording is final.
Do not run the behavior audit yet.

Your job is to produce compact, audit-ready candidate skill language.

Use `docs/synthesis/TEMPLATE.md` and
`docs/synthesis/methods/controlled-language-pass.md`.

Compress hard, but do not flatten the taste. Keep strong professional terms
when they recruit useful priors. Make gates blunt.

Return:

## 1. Compact Draft Scope

State:

- facet or skill scope being compacted;
- synthesis input used;
- existing skill text that must be preserved;
- behavior this draft must make predictable;
- what this draft must not decide.

## 2. Compression Principles

List the principles used to compress.

Include:

- what strong leading words must survive;
- what explanatory prose should be cut;
- what belongs behind context pointers;
- what gates need blunt wording;
- what should stay research-only.

## 3. Candidate Invocation / Description Wording

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
- risk to audit.

If invocation is not affected, write:

`No invocation wording change proposed.`

## 4. Candidate Runtime Steps

Draft candidate `SKILL.md` wording for the facet.

Use compact skill-shaped prose, not explanatory paragraphs.

For each candidate step:

```markdown
### <candidate heading>

<compact instruction text>

Done when <checkable completion criterion>.
```

Each step should:

- use active verbs;
- contain one main instruction per sentence where possible;
- include explicit conditions;
- preserve strong leading words;
- end with or include a checkable gate when relevant.

## 5. Candidate Rules / Gates

List the blunt lines that should be considered for runtime.

Use:

| Candidate Line | Purpose | Failure Prevented |
| --- | --- | --- |

Examples of gate shapes:

- `No proof, no done.`
- `Stop when <condition>.`
- `Ask only when <commitment boundary>.`
- `Done means <observable evidence>.`

## 6. Context Pointer Candidates

Identify material that should move behind a pointer rather than stay inline.

Use:

| Pointer Text | Target Support Doc | Why It Should Be Disclosed | When Agent Should Open It |
| --- | --- | --- | --- |

Do not create support docs yet unless the user explicitly asked.

## 7. Cut / Preserve Log

Record compression decisions.

Use:

| Material | Cut / Preserve / Move | Why |
| --- | --- | --- |

This is not final prune. It is a draft compression log.

## 8. Candidate Compact Draft

Assemble the best candidate wording in one block.

Use:

```markdown
<candidate skill text>
```

This block should be ready for Prompt 09 to audit line by line.

## 9. Audit Handoff

End with:

- lines most likely to be no-ops;
- lines most likely to duplicate another skill or contract;
- gates most likely to be too weak;
- gates most likely to be too heavy;
- context-pointer decisions to audit;
- existing skill behavior that must not regress;
- validation tasks to remember.

Write the compact draft to:

`docs/synthesis/compact/skill-facets/<skill-name>/FACET-<n>-<name>-compact-draft.md`
````

## Quality Bar

This prompt is complete when Prompt 09 has concrete candidate runtime lines to
audit for behavior change, no-ops, duplication, gates, ownership, and
context-pointer placement.
