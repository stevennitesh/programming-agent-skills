# Astra skill selection examples

These are canonical **selection boundary** examples for the current managed Astra
pack. They help maintainers and reviewers distinguish a skill's intended request
from its nearest realistic non-match.

They are not complete procedures or an additional router. Each
[skill entry point](../../skills/astra/) remains the execution authority, and the
frontmatter description remains the host-facing discovery contract. For
explicit-only skills, the canonical request includes the skill handle. For
automatically selectable skills, the request is shown in ordinary language.

| Skill | Canonical request | Expected behavior | Nearest non-match |
| --- | --- | --- | --- |
| [$audit-codebase](../../skills/astra/audit-codebase/SKILL.md) | `$audit-codebase Find the most worthwhile improvements in this repo and rank them; do not implement them.` | Investigate promising baseline areas and return a bounded, evidence-backed shortlist without requiring an atlas or user selection of each area. | `Review this PR for regressions.` That is change-review because the subject is a fixed change candidate. |
| [$change-review](../../skills/astra/change-review/SKILL.md) | `Review this branch against main for correctness and maintainability problems introduced by the change.` | Fix the candidate identity, judge changed behavior against accepted obligations, and return evidence-backed findings without unrelated baseline cleanup. | `Audit the whole repo for architecture debt.` That is audit-codebase because there is no selected change candidate. |
| [$codebase-design](../../skills/astra/codebase-design/SKILL.md) | `Decide whether this feature should extend our existing retry helper or replace the duplicated retry paths, and what can be retired.` | Inspect existing capabilities and consumers, choose the simplest suitable ownership, and return the caller transition and retirement obligations with necessary compatibility preserved. | `Implement the already-settled retry change.` Direct implementation needs no additional design phase. `Decide what users should see after a partially saved import.` Unsettled product behavior belongs to shape-work. |
| [$context-hygiene](../../skills/astra/context-hygiene/SKILL.md) | `Reconcile this repo's scattered guidance, conflicting owners, and missing test commands.` | Maintain the affected reading path from verified sources, preserve accepted meaning, and apply authorized cleanup without a separate setup phase. | `Set up agent guidance for this new repository.` That is repo-bootstrap because initial setup is requested. |
| [$cost-aware-coding](../../skills/astra/cost-aware-coding/SKILL.md) | `$cost-aware-coding Implement the accepted retry consolidation plan while minimizing Astra lead-token churn.` | The lead assigns acceptance including caller migration and scoped cleanup; Sol owns implementation and retirement while preserving supported behavior, Luna supplies useful bounded support, and the lead waits for meaningful questions or review returns before accepting the complete candidate. | `Implement this two-line null check.` Direct coding is cheaper than delegation overhead. |
| [$diagnosing-bugs](../../skills/astra/diagnosing-bugs/SKILL.md) | `This failure appears only under concurrent retries. Find the causal mechanism and fix it if the evidence supports a repair.` | Use targeted probes or controlled interventions when existing evidence cannot distinguish causes, adapt the investigation to results, and verify the authorized causal repair. If unresolved, identify the remaining alternatives, next discriminating observation, and limiting condition. | `The stack trace points to a misspelled variable; fix it.` An obvious local fix does not need the diagnosis workflow. |
| [$hillclimb](../../skills/astra/hillclimb/SKILL.md) | `$hillclimb Reduce p95 import latency without changing results; use comparable measurements and keep only proven improvements.` | Preserve the objective and keep rule, repair measurement when needed, adapt the search within scope and budget, and continue past intermediate wins until a stopping condition warrants final confirmation. | `Check once whether batching 100 records is faster than 10.` That is a bounded prototype unless an optimization loop is actually requested. |
| [$parallel-implement](../../skills/astra/parallel-implement/SKILL.md) | `$parallel-implement Implement these three accepted independent tickets concurrently and integrate them; use the existing dataset without copying it into each worktree.` | Establish usable isolated lanes before dispatch, share durable inputs by reference while isolating writes, give workers exclusive custody and implementation freedom, integrate serially, prove the composed result, and clean through each lane's lifecycle owner. | `Implement this one feature.` A single coherent change should stay direct or serial. |
| [$prototype](../../skills/astra/prototype/SKILL.md) | `Run a bounded experiment to determine whether SQLite WAL mode preserves the concurrency behavior this design needs.` | Choose and adapt a faithful experiment, repair ordinary probe failures, and return decisive evidence or a precise gap with any requested artifacts. Multiple runs may support the same bounded decision. | `Keep tuning database settings until p95 is under 50 ms.` That is hillclimb because it requests iterative optimization. |
| [$repo-bootstrap](../../skills/astra/repo-bootstrap/SKILL.md) | `$repo-bootstrap Set up agent guidance for this new repository using its actual commands and local constraints.` | Establish a useful reading path and initial guidance, preserving existing decisions without requiring a standard document tree. | `The repo's guides disagree about test commands; reconcile them.` That is context-hygiene because existing context needs maintenance. |
| [$research](../../skills/astra/research/SKILL.md) | `Compare the documented retry guarantees of SQS and Pub/Sub and recommend which fits these constraints.` | Inspect decisive source material, investigate credible counterevidence without forcing disagreement, and deliver a supported comparison with material uncertainties and coverage limits. Choose methods and depth for the question. | `Benchmark both clients in this repo to observe actual throughput.` That requires a new observation, so use prototype for a bounded experiment. |
| [$resolving-merge-conflicts](../../skills/astra/resolving-merge-conflicts/SKILL.md) | `Resolve the conflicts in this active rebase and continue it, preserving both intended changes.` | Observe the active Git operation, reconcile intended combined behavior, prove the resolved candidate, and reach only the authorized endpoint. | `Merge feature-x into main from a clean worktree.` Starting an ordinary integration is not conflict resolution. |
| [$shape-work](../../skills/astra/shape-work/SKILL.md) | `$shape-work Brainstorm a better failed-import workflow with me, challenge the scope, and write the agreed spec.` | Use an adaptive interview to settle goals, scope, behavior, and acceptance; deliver the spec and reconcile affected current decisions while leaving implementation methods open. | `Choose whether retry state belongs in the service or repository layer.` That is codebase-design because the question is technical ownership. |
| [$to-tickets](../../skills/astra/to-tickets/SKILL.md) | `$to-tickets Turn this migration spec into bounded tickets using this repo's tracker, with enough context for independent agents and dependencies for parallel work.` | Preserve accepted meaning, create coherent assignments with acceptance and accessible source context, and record required predecessor results, unblock conditions, potential parallel work, and known coordination constraints. | `$triage Classify this newly reported issue.` Raw tracker intake belongs to triage. |
| [$triage](../../skills/astra/triage/SKILL.md) | `$triage Clean up this backlog: reconcile stale status, duplicates, and completed work using the repo's tracker conventions.` | Assess the requested set with proportionate evidence, preserve active ownership and truthful dependencies, apply authorized corrections, and report verified changes, unresolved items, and coverage limits. | `Split this accepted feature into implementation tickets.` Decomposition belongs to to-tickets. |
| [$verification-harness](../../skills/astra/verification-harness/SKILL.md) | `$verification-harness Improve our launch and driver tools so agents can exercise the app, CLI, and MCP interface repeatably and capture reliable results.` | Reuse or improve repository tooling, choose methods for the requested surfaces, demonstrate the capability against the intended product, and preserve meaningful assertions, evidence, and resource ownership. | `Run the existing CLI smoke test and report the result.` Routine verification needs no tooling workflow. |
| [$wizard](../../skills/astra/wizard/SKILL.md) | `$wizard Help me enter the private API key through my terminal so you can resume the integration work; keep the key out of this chat and your tool output.` | Reuse or build a checked terminal procedure, keep private input and session output with the human, and use sufficient non-secret evidence to resume already-authorized work. | `Build a reusable driver for the same flow with an isolated test account.` Agent-operated product tooling belongs to verification-harness. |
| [$writing-for-agents](../../skills/astra/writing-for-agents/SKILL.md) | `Rewrite this AGENTS.md section so a fresh coding agent knows when to run the project-specific verifier.` | Preserve intent, receiver context, authority, and completion evidence while leaving valid methods open. | `Ask the worker to fix the typo in this file and report the change.` Routine dispatch uses the owning workflow directly and needs no separate instruction-authoring phase. |
| [$git-cleanup](../../skills/astra/git-cleanup/SKILL.md) | `Review this repo's branches, integrate worthwhile work, then remove safely retired branches and worktrees and sync the default branch.` | Assess exact candidates and integration evidence, preserve unique work and active ownership, integrate within scope, and verify authorized cleanup and synchronization through the relevant lifecycle owners. | `Commit and push these approved changes.` Routine publication needs no branch-cleanup workflow. `Resolve this active rebase conflict.` That belongs to resolving-merge-conflicts. |
| [$portfolio-presentation](../../skills/astra/portfolio-presentation/SKILL.md) | `Make this project's README, results report, and charts tell a coherent story for recruiters using the evidence we already have.` | Reconcile claims and visuals with current evidence, explain contribution and consequential tradeoffs in accessible language, and inspect requested rendered surfaces without inventing impact or new experiments. | `Rewrite this one resume bullet more concisely.` An isolated wording edit stays direct. `Improve the model's held-out performance.` That is analysis or implementation work, not presentation. |

## Context-maintenance branches

`Audit the Codex memories for this project and recommend which temporary states
should be retired; do not change anything.` selects context-hygiene's memory
branch and finishes with findings. A requested memory cleanup uses the runtime's
supported update path and distinguishes submission from active consolidation.
`Summarize this chat so I can resume tomorrow` remains a continuation handoff.

Discovering one stale command during a coding task can justify focused context
assessment within scope; it does not initiate an unrelated repository or memory
audit. A directly requested wording edit to a selected paragraph remains
writing-for-agents.

## Maintenance rule

Keep exactly one row per managed Astra skill. Update a row when a discovery
boundary materially changes; do not churn examples for wording-only edits. A
positive example demonstrates eligible intent, while the near-miss should exercise
the closest realistic boundary rather than an obviously unrelated task.

## Shaping and decision-record branches

- `$shape-work Record our accepted retry-state design as an ADR.` captures the
  settled rationale and applicability without reopening architecture or requiring
  a feature interview.
- `$shape-work Reconcile what "complete" means in this spec, domain record, and ADR.`
  resolves the consequential meaning and reconciles its affected current owners.
- `Turn this agreed spec into an implementation plan.` belongs to the execution
  lead, using cost-aware-coding when selected; it does not require another shaping
  interview.
- `Find and fix stale commands and scattered repository guidance.` belongs to
  context-hygiene. Broader context cleanup does not become shaping merely because
  some documents are ADRs.

## Ticketing input branches

`$to-tickets Draft tickets for the CSV export idea we just agreed, including its
dependencies.` can proceed from a sufficiently clear conversation without a formal
specification. The draft must carry the agreed facts or point to an accessible
shared source. `Help me decide what this export feature should do` belongs to
shape-work while consequential behavior is unresolved; independent settled parts
can still be decomposed when ticketing is requested.

## Triage assessment and cleanup branches

`$triage Show which tickets need attention; do not change them` returns a
read-only overview with useful priorities and coverage limits. A request to clean
up the same queue can apply supported corrections within its authority. Existing
ready tickets remain eligible for assessment; their active claims and assignments
must be preserved unless a coordinated change is authorized. One item needing
deep investigation does not prevent independent cleanup of the rest.

## Wizard delivery and continuation branches

`$wizard Write a script I can run later to enter this key privately` ends with
the checked procedure and exact run command. When the wizard is part of an
already-authorized integration task, a sufficient non-secret result can unblock
that work. Launching a terminal or writing the secret does not by itself prove
the application is ready. If the host cannot provide a genuinely private session,
give the human the run command without opening an agent-attached secret prompt.
