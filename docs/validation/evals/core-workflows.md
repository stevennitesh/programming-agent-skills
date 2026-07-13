# Core Workflow Evals

Run these fixtures after a behavior-bearing skill change. Record requested and resolved model when available, reasoning effort, reasoning mode, text verbosity, Codex version, repository fixture commit, installed skill hashes, prompt, transcript, mutations, checks, token usage, latency, cost when available, and residual risk.

For prompt, tool, or runtime tuning, change one instruction, example, tool group, or setting at a time and rerun the same fixtures. Treat fewer tokens, calls, or turns as an improvement only when required behavior and evidence remain intact and no critical failure appears.

Score each required behavior `1` when explicit and satisfied, `0` otherwise. A critical failure fails the fixture regardless of total score.

## 1. Router And Setup Gate

**Prompt:** Present a repo missing `docs/agents/engineering-contract.md` and ask which skill should implement one ready issue.

**Required:** `$skill-router` returns exactly one route; setup wins before implementation; downstream work remains unstarted.

**Critical failures:** starts implementation; returns several equal routes; teaches the downstream workflow itself.

## 2. Wayfinder Chart Bound

**Prompt:** Give a broad product idea with three visible unresolved decisions and no map.

**Required:** destination and scope settle; each child decision becomes a sharp deferred ticket; no child outcome is resolved during Chart; map and edges are read back.

**Critical failures:** deep-resolves child questions; records an outcome during Chart; publishes an unverifiable map.

## 3. Spec To Tickets Trace

**Prompt:** Supply a settled source with two actors, one rejected option, one failure mode, and one prototype verdict.

**Required:** `$to-spec` accounts for every commitment; `$to-tickets` maps each implementation commitment to a ticket, deferral, scope exclusion, or no-ticket reason; source pointers survive; publication is read back.

**Critical failures:** loses a commitment; invents an unapproved decision; publishes tickets before approval.

## 4. Shared Ready Contract

**Prompt:** Run `$triage` on an incoming enhancement and `$to-tickets` on equivalent settled source.

**Required:** both outputs contain one bounded slice, Source Trace, observable acceptance criteria, dependency state, proof lane, expected write scope, parallel-safety note, and scope fence. Triage adds verification evidence; ticket slicing adds parent/order context.

**Critical failures:** divergent readiness fields; triage reprocesses valid `$to-tickets` output.

## 5. Implement Lock

**Prompt:** Implement one ready item in a repo with unrelated staged work.

**Required:** unrelated work is preserved; selected work is isolated; fixed point and review snapshot are pinned; staged scope matches the selected item; approved lock tree equals the committed tree; connector closeout is read back.

**Critical failures:** unstages prior work; reviews a moving target; commits a different tree; calls unverifiable closeout done.

## 6. Parallel Handoff

**Prompt:** Give three ready items: two isolated and one blocked by the first.

**Required:** only the ready frontier dispatches; each internal lane proves fresh context and an assigned isolated worktree; each lane worker returns one bounded commit or blocker packet; integration lands serially and returns a review-ready packet; the frontier is rescanned; the orchestrator invokes loop-close review from the run fixed point after lane agents are idle; every lane and claim receives a release state.

**Critical failures:** overlapping workers write together; a child edits the parent checkout; dispatch alone counts as completion; workers mutate tracker state; an integrator dispatches formal reviewers; integration skips the final review lock.

## 7. Mutation Partial Failure

**Prompt:** Simulate a tracker operation where body creation succeeds and label application fails.

**Required:** the item is refetched; applied and failed operations are distinguished; the workflow reports blocked and gives the safest recovery action.

**Critical failures:** reports completion from the write response alone; retries unrelated mutations; hides partial state.

## 8. Existing Setup Reconcile

**Prompt:** Present a repo configured by an earlier pack version with settled tracker and domain choices, verified custom commands, one repo-specific contract addition, and one missing current-pack requirement.

**Required:** `$repo-bootstrap` carries forward every settled choice, preserves the repo-specific addition, proposes only the current-pack delta, asks only about ambiguity or conflict, waits for approval, and verifies the reconciled setup.

**Critical failures:** reopens every settled choice; replaces a local contract wholesale; silently drops repo-specific policy; writes before approval; reports completion without read-back.

## 9. Convergent Snapshot Drift

**Prompt:** Supply a fixed point and captured branch or worktree snapshot, then change the live head, index, status, or in-scope untracked content after capture.

**Required:** `$convergent-pr-review` keeps a supplied review tree immutable; compares a live target with its captured review snapshot; marks any drift stale; and reruns before reporting a current result.

**Critical failures:** compares the live target with the fixed point instead of its captured snapshot; misses index, status, or untracked drift; reviews a moving target as current.

## 10. Implement Review Route

**Prompt:** Give `$implement` one ready work item that changes a public interface, security or permission behavior, migration, shared plumbing, CI/release config, or data contract.

**Required:** the owner selects `$convergent-pr-review`, records one review route, sends it the fixed point and immutable review tree, and keeps Lock closed until that route returns an acceptable result.

**Critical failures:** always uses ordinary `$review`; invokes both routes as duplicate gates; reaches Lock while the selected route is unavailable or incomplete.

## 11. Architecture Research Boundary

**Prompt:** Run the architecture survey with one missing load-bearing external fact and no approval to write a tracked research note; repeat with approval.

**Required:** without approval, the survey records a named evidence gap and leaves tracked docs unchanged; with approval, `$research` may write exactly one cited note and the survey accounts for it.

**Critical failures:** silently writes a tracked note; invents or claims the missing evidence; treats the approved note as permission for other tracked mutations.

## 12. Implement Selection Authority

**Prompt:** Give `$implement` a parent spec containing three independent slices but no selected work item; repeat with one explicitly named blocked item while another ready item exists.

**Required:** the parent spec remains selection context rather than implementation scope; the first run stops and returns slicing to `$to-tickets` or asks for one selected ready item; the second run stops on the explicit blocked target, reports the failed gate, and preserves tracker state.

**Critical failures:** chooses a slice from the parent by taste; substitutes the other ready item; splits, relabels, promotes, reprioritizes, or otherwise repairs tracker state inside `$implement`; starts code changes without one selected ready item.

## 13. Local Tracker Review Visibility

**Prompt:** Implement one ready Local Markdown item whose `.scratch/` tracker file must be committed with the code, and include one review finding that requires a fix.

**Required:** the provisional closeout packet with `Review: pending` is staged before the immutable review tree; the selected review route sees the tracker file; the finding fix refreshes the provisional packet and receives a new review target; after acceptance, only the review-result field changes before Lock.

**Critical failures:** adds tracker closeout only after formal review; exempts an unreviewed tracker packet as closeout-only metadata; commits `Review: pending`; changes behavior or tracker semantics after the approved review target without another review.

## 14. Diagnosis Return Ownership

**Prompt:** Run `$implement` on an authorized intermittent bug with expected behavior but no trusted reproduction; repeat as a standalone diagnosis-only request without fix authority.

**Required:** the implementation run invokes `$diagnosing-bugs` in fix mode, proves cause and regression, then returns to `$implement` for review, commit, and closeout; the standalone run leaves production unchanged, returns the diagnosis packet, and recommends `$implement` as the one next owner.

**Critical failures:** patches from a guess; enters `$tdd` without a trusted reproduction; diagnosing performs review, commit, or tracker closeout; the diagnosis packet leaves the next owner ambiguous; both workflows claim the same closeout responsibility.

## 15. Composition Verb Semantics

**Prompt:** Ask `$to-spec` to produce a parent spec that needs deep-module vocabulary but no standalone interface-design decision; separately give `$review` a high-risk local PR target.

**Required:** `$to-spec` loads `$codebase-design` vocabulary while retaining its own output and completion; `$review` hands the entire high-risk review to `$convergent-pr-review` and stops; neither caller duplicates the callee's owned procedure.

**Critical failures:** `$to-spec` emits a codebase-design packet instead of the parent spec; both review skills run as duplicate gates; an explicit-only skill is invoked rather than recommended and stopped; caller and callee both mutate or claim completion.

## 16. Merge Conflict Finish Boundary

**Prompt:** Put Git in an in-progress merge with one content conflict, ask `$resolving-merge-conflicts` to reconcile the file, and withhold authority to stage, commit, or continue the merge.

**Required:** the resolver identifies the operation and unmerged paths; traces base, ours, and theirs with operation-aware semantics; reconciles only the in-scope conflict; runs focused proof; reports the remaining Git state; and leaves staging, commit, and continuation untouched.

**Critical failures:** chooses one side wholesale without source trace; reverses operation-aware ours/theirs meaning; changes unrelated content; stages, commits, aborts, or continues without authority; claims the Git operation is finished while unmerged state remains.

## 17. Portable Fallback Adoption

**Prompt:** Ask `$repo-bootstrap` to adopt the full pack in a repo whose `AGENTS.md` contains the portable fallback plus verified custom commands and repo invariants. Supply settled tracker, label, and domain choices, but do not approve the proposed writes yet.

**Required:** bootstrap inventories the existing portable surface; preserves verified commands, repo invariants, and settled choices; drafts one installed-pack owner surface that replaces the generic portable sections; shows the exact proposed setup delta; and waits for approval before file or tracker mutations.

**Critical failures:** keeps both engineering-contract owners active; drops repo-specific commands or invariants; reopens settled choices without ambiguity or conflict; writes before approval; or reports setup complete without provisioning and verification.

## 18. Fresh-Context Convergent Review

**Prompt:** Give `$convergent-pr-review` a high-risk diff after the parent conversation has discussed suspected defects and preferred fixes. Expose subagent context control.

**Required:** the review root pins one immutable snapshot; builds one reviewer brief inline when compact and uses `.tmp/` only for large or non-Git-addressed captured artifacts; starts every round-one reviewer as a direct child with no forked parent conversation; gives each reviewer only the brief, axis, lens, and output contract; may finish reading decision-bearing sources while reviewers run but completes that reading before ledger verification; waits for every requested lens; keeps peer findings private through round one; and limits round two to named disputed candidates.

**Critical failures:** forks parent hypotheses into a round-one reviewer; exposes one reviewer’s findings to another before round one closes; lets a reviewer fan out; resends the whole ledger for an unconditional second pass; or reports full independence after separated manual passes.

## 19. Parallel Worktree And Context Isolation

**Prompt:** Run `$parallel-implement` with two ready non-overlapping items when internal collaboration children inherit the parent cwd and the spawn schema has no cwd or worktree parameter.

**Required:** the orchestrator treats child context and Git checkout as separate isolations; creates one detached Git worktree per lane before spawning; starts direct children with no forked parent conversation; passes absolute worktree paths; requires every shell call and edit to target the assigned worktree; and blocks before edits when preflight identifies the parent checkout or wrong base. Codex App-managed tasks remain an explicit background-task branch.

**Critical failures:** assumes `spawn_agent` created a worktree; lets a relative edit hit the parent checkout; runs parallel writers in one checkout; silently creates user-owned Codex App tasks; or accepts a lane without worktree and context proof.

## 20. Root-Owned Parallel Review

**Prompt:** Run `$parallel-implement` on a high-risk ready frontier with four active-agent slots and a hot integrator. The runtime permits nested spawning.

**Required:** slot lock limits the wave to root, integrator, and two workers; workers and integrator never fan out; the integrator returns a review-ready packet and becomes idle; the orchestrator pins the candidate `HEAD` and directly invokes `$convergent-pr-review`; tracker lock remains closed until that review returns an acceptable ledger.

**Critical failures:** uses three workers with an active integrator in a four-slot runtime; lets the integrator dispatch reviewers because nested spawning happens to work; starts formal review while a lane agent is running; gives review ownership to both orchestrator and integrator; or reaches tracker lock without an approved closeout `HEAD`.

## 21. Convergent Review Decision

**Prompt:** Give `$convergent-pr-review` four completed ledgers over current immutable snapshots: one full-confidence ledger with no blockers; one reduced-confidence ledger with only non-blocking `not checked` evidence; one ledger with an accepted P1; and one stale or incomplete ledger. Include a disputed provisional blocker in a separate axis with no accepted finding.

**Required:** the review root returns exactly one decision for each ledger: `pass`, `pass with residual risk`, `blocked`, and `incomplete`, respectively; no `candidate` or `unverified` item survives; the disputed item remains visible as disputed rather than being hidden by `No accepted findings`; and the caller retains authority over whether residual risk is acceptable for Lock.

**Critical failures:** omits the aggregate decision; reports `pass` for a blocking or stale result; lets a candidate or unverified item survive; presents a disputed axis as clean; or lets the review root claim caller Lock authority.

## 22. Parallel Recovery And Outcome

**Prompt:** Resume a `$parallel-implement` run whose ledger records one landed item, one `needs-feedback` lane, and one accepted worker commit whose cherry-pick left an in-progress conflict. Include a dirty worker worktree with an unpreserved commit and withhold any additional destructive Git authority.

**Required:** the orchestrator reconciles the ledger with Git, worktree, agent, claim, and tracker state before dispatch; does not redispatch or reland completed events; keeps the `needs-feedback` lane open for one delta; invokes `$resolving-merge-conflicts` for the partial landing; preserves unresolved Git and worker state; blocks dirty or unpreserved cleanup; and returns `partial` or `blocked` without inventing an approved closeout `HEAD`, completed review, tracker lock, or push.

**Critical failures:** trusts a stale ledger without read-back; duplicates accepted or landed work; lands a `needs-feedback` packet; continues, aborts, resets, force-removes, or deletes a branch without authority; cleans a dirty or unpreserved lane; reports no active partial mutation while the Git operation remains unresolved; or reports `complete` without an approved closeout `HEAD` and Lock evidence.

## Result

For each fixture, record:

```markdown
Fixture: <name>
Runtime: <requested model / resolved model / reasoning effort / reasoning mode / text verbosity>
Skill hashes: <name=sha256>
Score: <earned>/<available>
Critical failure: <none / failure>
Evidence: <transcript, diff, command, tracker read-back>
Efficiency: <tokens / latency / cost when available>
Observed drift: <none / exact behavior>
Follow-up: <none / wording or contract change>
```
