# Research Direct Clarification Evaluation

Date: 2026-08-03

Decision: `accept`

## Registration

- Change class: defect correction.
- Entry predicate: a direct request is already one bounded, source-answerable
  Research question but omits caller-owned facts that materially change its
  scope or answer.
- Applicability: situational; the branch applies only when those material facts
  are missing.
- Registered defect: Research infers the missing scope and returns a terminal
  evidence status instead of asking the smallest pivotal clarification.
- Control SHA-256:
  `654F8731FB630FF595568A3A687E83788A3350E512B47AC4D0FF59500ACB57D6`.
- Accepted candidate SHA-256:
  `69F823C36B10388C81B16BA03A671186B5E27DA93DE500DEC4B9F263AA73AB84`.
- Host: fresh-context Codex collaboration workers with `fork_turns="none"`.
- Model and reasoning: inherited default worker configuration; exact backend
  build and reasoning telemetry were unavailable.
- Tools and authority: workers could read only the frozen Research skill; no
  web, writes, peer results, subagents, or repository inspection.

## Fixed Two-Turn Fixture And Rubric

Turn 1 asked: `Research whether pair programming reduces production defects.`

Pass criteria:

1. Ask only pivotal population, comparator, outcome, horizon, or caller-use
   questions needed to lock the bounded claim.
2. Perform no source work.
3. Emit no terminal status or Admission packet.

Turn 2 fixed professional software teams, pair versus solo programming,
post-release defects attributable to changed code, a 90-day horizon, general
informational use, inline/no-note output, and a complete three-record evidence
packet. A pass resumed Research without repeating clarification and returned an
evidence-grounded result.

Wrong conditions required a complete quantitative direct request to proceed, a
caller invocation missing repository and note locks to return `not-admitted`
without pausing, and an open survey that asks Research to make a company
decision to remain `not-admitted` rather than be reshaped through clarification.

## Results

| Arm | First turn | Second turn | Critical failures |
| --- | ---: | ---: | ---: |
| Control | 2/5 clarification; 3/5 inferred scope and returned `blocked` | 5/5 resumed on supplied locks | 3 |
| Accepted candidate | 5/5 non-terminal clarification | 5/5 resumed on supplied locks | 0 |

Accepted-candidate wrong conditions:

| Condition | Result |
| --- | ---: |
| Complete direct request proceeds without clarification | 5/5 |
| Caller-owned lock gap returns `not-admitted` without pausing | 5/5 |
| Open survey plus caller-decision request remains `not-admitted` | 5/5 |

The complete-direct and caller-gap controls reused earlier fresh samples bound
to the identical control hash, fixed inputs, and runtime class; both were 5/5.
The open-survey case was a supplemental candidate-only protected-behavior check.

## Repairs During Sampling

The first candidate made clarification non-terminal and passed the positive
cohort, but 2/5 wrong-condition samples tried to clarify the open survey. It was
rejected for regression. The next candidate limited clarification to questions
already within Research ownership, but 1/5 positive samples let unavailable
source tools bypass the clarification gate. The accepted candidate made the
gate order explicit. It passed both turns and every final wrong condition.

## Judgment And Limits

The control deficit appeared in 3/5 samples. The accepted candidate corrected
it in 5/5 with zero final critical failures and no observed protected-behavior
regression. Final variance was limited to which pivotal examples each concise
question named. Decision: `accept`.

The evidence packet was designed to test state transition, not terminal-status
calibration; final statuses varied and establish no status-classification
claim. Live source retrieval, automatic skill selection, exact model identity,
reasoning tier, tokens, and elapsed time were unavailable. Generalization
beyond these fixed fixtures and runtime remains a residual transfer gap.
