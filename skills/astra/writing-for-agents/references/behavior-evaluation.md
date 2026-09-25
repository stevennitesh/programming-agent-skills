# Behavior evaluation

Use this reference when a meaningful claim depends on whether agent instructions
change behavior: migrating to another model or host, materially revising a skill,
changing discovery, deciding whether guidance still earns its context, or
evaluating a claimed improvement.

Do not require this procedure for ordinary wording corrections whose intended
meaning and behavior are unchanged.

## 1. State the behavioral claim

Describe the behavior the instruction is supposed to change or preserve.

Prefer a claim such as:

> The review guidance should preserve candidate identity and find consequential
> defects without introducing unnecessary review ceremony.

over:

> Make the review prompt better.

Name the receiver, relevant environment, and consequence if the behavior is
missing. Keep explicit user requirements, project contracts, authorization, and
safety boundaries fixed; evaluation does not reopen them merely because a capable
model sometimes follows them without prompting.

## 2. Choose a comparison that answers the question

Use the smallest comparison that can establish the requested claim:

- **New method:** baseline without the method versus candidate.
- **Revision:** frozen current method versus candidate.
- **Keep, simplify, or retire:** baseline without the method, current method, and
  candidate or reduced method.

The baseline still receives the same task, repository guidance, user decisions,
permissions, safety requirements, and project-specific facts that ordinary work
would receive. Do not handicap it by withholding necessary context merely to make
the skill appear useful.

Hold other consequential variables constant: receiver model, reasoning setting,
tools, repository state, task input, and acceptance criteria. If one of these
changes, do not attribute the result solely to the instruction.

Use fresh receiver contexts when earlier answers or candidate wording could
contaminate the comparison.

## 3. Test discovery separately from execution

A method cannot help if the intended task never receives it, and a good method
can still be harmful if it activates too broadly.

For discovery changes, test:

- representative requests that should select the skill;
- realistic near-misses that should not; and
- ambiguous cases where another skill or direct execution is preferable.

Use host evidence of selection or loading when available. If the host does not
expose that state, report the limitation rather than inferring selection solely
from the final answer.

Do not treat a discovery failure as proof that the skill body is poor, or a
successful trigger as proof that its instructions improve execution.

## 4. Judge outcomes, not obedience

Evaluate the result against the task's independent acceptance criteria and the
failure the instruction is meant to prevent.

Useful measures can include:

- correctness and completion;
- consequential omissions;
- invented policy or unsupported assumptions;
- unnecessary questions, approval stops, or premature stops on non-blocking
  status, findings, or reversible choices;
- unnecessary plans, progress files, artifacts, delegation, reviews, or tests;
- scope expansion;
- preservation of authority and required effects;
- maintainability or simplicity of the produced change;
- latency, token use, or tool calls when efficiency is part of the claim.

Do not reward a candidate merely for following more instructions from the
candidate itself. An instruction can achieve perfect procedural compliance while
making the actual result worse.

When the claimed improvement is efficiency—fewer tokens, tool calls, lines of
code, elapsed time, context, or cost—gate the comparison on the same accepted
correctness, completeness, safety, and required-effect criteria first. A candidate
that does less required work or drops a protection does not win an efficiency
comparison. Report efficiency only among outcomes that satisfy those gates, and
report any gate failure separately rather than averaging it into a score.

Use a scenario that can expose the intended distinction. A happy path on which
baseline and candidate naturally behave the same provides little evidence about
the value of the instruction.

## 5. Use enough variation for the strength of the claim

A single run can reveal a clear failure, but one success does not establish broad
reliability.

For an editorial or local migration decision, a small set of representative
cases may be sufficient to expose obvious regressions or no-op guidance. Add
repetitions or held-out cases when variance could change the decision or when the
claim is meant to generalize across task types.

When comparing receiver models, hosts, or reasoning settings, change one
meaningful dimension at a time when practical. Behavior established on one model
or harness is evidence for that environment, not automatic portability to another.

Record important failures as well as successes. Do not tune the candidate only
to the visible examples and then describe performance on those same examples as
general evidence.

## 6. Decide whether the instruction earns its place

Retain guidance when it provides material context or authority the receiver needs,
changes a useful decision, prevents a credible failure, or measurably improves the
accepted result at reasonable cost.

Simplify guidance when a smaller version preserves the useful behavior with less
context, ceremony, or accidental constraint.

Retire a method when representative evidence shows no useful marginal behavior
and it does not carry project-specific facts, authority, fragile operational
contracts, or other information the receiver still requires.

Keep uncertainty explicit when evidence is mixed or incomplete. Do not turn
absence of demonstrated benefit into proof of harm, or structural validity into
proof of efficacy.

Report the comparison conditions, decisive observations, material variability,
and resulting keep, simplify, revise, or retire recommendation. Separate observed
behavior from the inference drawn from it.
