# Prompt 12: Final Prune And Runtime Patch

Use this as Step 12 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to turn a validated plain-language candidate into the smallest safe
runtime change, either as a plan-only final patch shape or as an applied edit
when explicitly requested.

````markdown
We are final-pruning a validated plain-language skill candidate and preparing
the runtime skill change.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Facet or scope: `<facet-number-and-name, or whole skill>`
Candidate runtime draft: `<path or paste Prompt 08 output>`
Detailed skill-context draft: `<path or paste Prompt 09 output>`
Plain-language candidate: `<path or paste Prompt 10 output>`
Validation note: `<path or paste Prompt 11 output>`
Validation decision: `<Prompt 11 validation decision>`
Validated / revise / cut lines: `<Prompt 11 handoff lists>`
Existing skill text: `<path or paste relevant SKILL.md section>`
Mode: `<plan-only | apply-edit>`
Revision feedback: `<optional feedback if rerunning this prompt; otherwise "none">`

Do not search for new sources.
Do not reopen extraction, triage, agent bridge, or full behavior synthesis.
Do not widen the skill beyond the validated scope.
Do not change invocation policy unless validation explicitly requires it.
Do not add support docs unless the validated placement decision requires them.

Your job is to remove anything left after validation that still does not earn a
runtime place. The main plain-language compression already happened in Prompt
10; this pass is residual pruning, support routing, and optional patch
application.

Use the `writing-great-skills` pruning standard:

- keep each meaning in one place;
- keep only behavior-changing lines;
- cut no-ops, sediment, sprawl, decorative wording, and repeated meaning;
- move branch-specific or bulky reference behind context pointers;
- make completion criteria checkable;
- preserve existing behavior that must not regress.

Return:

## 1. Final Prune Scope

State:

- skill and facet or scope;
- detailed skill-context draft and plain-language candidate used;
- validation decision used;
- existing behavior that must be preserved;
- whether this is `plan-only` or `apply-edit`;
- what this pass will not change.

If `Revision feedback` is not `none`, account for it before producing final
runtime text. If the validation decision is not `ready-for-final-prune`, do not
final-prune anyway; return to the owning prompt named by the validation note.

If there is no revision feedback, write:

`No revision feedback to disposition.`

## 2. Validation-Driven Decisions

Use:

| Item / Line ID | Validation Result | Final Decision | Why |
| --- | --- | --- | --- |

Final decisions:

- keep
- revise
- cut
- move-to-support
- owned-elsewhere
- defer

## 3. Final Runtime Text

Produce the smallest final candidate runtime text.

Use:

```markdown
<final candidate SKILL.md text or replacement section>
```

This should be ready to apply if mode is `apply-edit`.

## 4. Invocation / Description Decision

State whether invocation or description changes.

Use:

| Current | Final Candidate | Change? | Why |
| --- | --- | --- | --- |

If unchanged, say:

`No invocation or description change.`

## 5. Context Pointer / Support Doc Decision

Use:

| Pointer Or Support Material | Final Decision | Target | Why |
| --- | --- | --- | --- |

Do not create or edit support docs in `plan-only` mode.

## 6. Prune Log

Record what was cut.

Use:

| Cut Material | Reason | Do Not Revive Unless |
| --- | --- | --- |

Reasons may include:

- no-op
- duplicate
- owned elsewhere
- too vague
- too bulky
- research-only
- unsupported by validation
- branch-specific reference

## 7. Residual Risk

Use:

| Risk | Why It Remains | Mitigation / Follow-Up |
| --- | --- | --- |

Include skipped validation or uncertainty honestly.

## 8. Apply Edit Branch

If mode is `plan-only`, write:

`Mode is plan-only. No runtime files edited.`

If mode is `apply-edit`:

- edit only the validated target files;
- preserve unrelated user changes;
- do not touch unrelated skills;
- run the appropriate checks;
- record files changed and checks run.

Use:

| File | Change |
| --- | --- |

## 9. Completion Summary

End with:

- final-prune decision:
  - `plan-ready`: final patch shape is ready but not applied;
  - `edit-applied`: validated runtime edit was applied;
  - `return-to-validation`: Prompt 11 or an earlier owning prompt must rerun;
  - `blocked`: stop until the named owner, support-doc, or user decision is
    resolved;
- final behavior preserved or introduced;
- files to edit or edited;
- checks to run or run;
- residual risks;
- follow-up work, if any.

Write the final prune note to:

`docs/synthesis/facets/<skill-name>/FACET-<n>-<name>/12-final-prune.md`
````

## Quality Bar

This prompt is complete when the final runtime text is smaller than the draft,
behavior-changing, validation-backed, non-duplicative, and every remaining line
earns its place.
