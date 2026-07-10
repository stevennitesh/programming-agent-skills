# Core Workflow Evals

Run these fixtures after a behavior-bearing skill change. Record model, Codex version, repository fixture commit, installed skill hashes, prompt, transcript, mutations, checks, and residual risk.

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

**Required:** only the ready frontier dispatches; each lane worker returns one bounded commit or blocker packet; integration lands serially; frontier is rescanned; loop-close review uses the run fixed point; every lane and claim receives a release state.

**Critical failures:** overlapping workers write together; dispatch alone counts as completion; workers mutate tracker state; integration skips the final review lock.

## 7. Mutation Partial Failure

**Prompt:** Simulate a tracker operation where body creation succeeds and label application fails.

**Required:** the item is refetched; applied and failed operations are distinguished; the workflow reports blocked and gives the safest recovery action.

**Critical failures:** reports completion from the write response alone; retries unrelated mutations; hides partial state.

## Result

For each fixture, record:

```markdown
Fixture: <name>
Skill hashes: <name=sha256>
Score: <earned>/<available>
Critical failure: <none / failure>
Evidence: <transcript, diff, command, tracker read-back>
Observed drift: <none / exact behavior>
Follow-up: <none / wording or contract change>
```
