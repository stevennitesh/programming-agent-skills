# Core Workflow Evals

Run these fixtures after a behavior-bearing skill change. Record requested and resolved model when available, reasoning effort, reasoning mode, text verbosity, Codex version, repository fixture commit, installed skill hashes, prompt, transcript, mutations, checks, token usage, latency, cost when available, and residual risk.

For prompt, tool, or runtime tuning, change one instruction, example, tool group, or setting at a time and rerun the same fixtures. Treat fewer tokens, calls, or turns as an improvement only when required behavior and evidence remain intact and no critical failure appears.

Score each required behavior `1` when explicit and satisfied, `0` otherwise. A critical failure fails the fixture regardless of total score.

## 1. Router And Setup Gate

**Prompt:** Present a repo missing `docs/agents/engineering-contract.md` and ask which skill should implement one ready issue. Repeat with a compatible repo and clear ready item, an ambiguous repo-backed interview request, and a marker-only conflict with no in-progress Git operation.

**Required:** `$skill-router` returns exactly one route in the `Skill`, `Reason`, and `Precondition` fields; setup wins before implementation; the clear item routes to `$implement`; ambiguity produces one decisive question before one route; marker-only conflict routes to `$resolving-merge-conflicts`; downstream work remains unstarted.

**Critical failures:** starts implementation; returns several equal routes; teaches the downstream workflow itself.

## 2. Wayfinder Chart Bound

**Prompt:** Give a broad product idea with three visible unresolved decisions and no map. Then advance an existing map whose selected final-frontier ticket reaches the destination.

**Required:** destination and scope settle; the map records a distinct Scope Boundary; each child decision becomes a sharp deferred ticket; no child outcome is resolved during Chart; the complete map, child, fog, scope, note-path, and edge mutation packet is approved before publication; a changed packet requires fresh approval; map and edges are read back. Advance resolves exactly the selected final-frontier ticket, reconciles and reads back its consequences, then runs closure as Advance's terminal gate only after no unresolved child or in-scope fog remains and the absence of an in-scope frontier is verified.

**Critical failures:** deep-resolves child questions; records an outcome or runs closure during Chart; treats closure as a third session mode; publishes before approval; publishes an unverifiable map; closes with unresolved child work, fog, or an unverified frontier.

## 3. Spec To Tickets Trace

**Prompt:** Supply a settled source with two actors, one rejected option, one failure mode, and one prototype verdict. Include two write-overlapping tickets in the resulting ready frontier.

**Required:** `$to-spec` accounts for every commitment; `$to-tickets` shows a coverage map that maps each implementation commitment to a ticket, deferral, scope exclusion, or no-ticket reason; source pointers survive; publication is read back; overlapping ready tickets produce one `$implement` recommendation naming the first ticket under tracker ready order.

**Critical failures:** loses or hides a commitment or non-ticket disposition; invents an unapproved decision; publishes tickets before approval; returns an ambiguous overlapping frontier without a selected serial ticket.

## 4. Shared Ready Contract

**Prompt:** Run `$triage` on an incoming enhancement and `$to-tickets` on equivalent settled source.

**Required:** both outputs contain one bounded slice, Source Trace, observable acceptance criteria, dependency state, proof lane, expected write scope, parallel-safety note, and scope fence. Triage adds verification evidence; ticket slicing adds parent/order context.

**Critical failures:** divergent readiness fields; triage reprocesses valid `$to-tickets` output.

## 5. Implement Lock

**Prompt:** Implement one ready item in a repo with unrelated staged work and an ordinary-review finding. Repeat with an explicitly assigned staged worker and an accepting owner.

**Required:** the owner claims tracker-backed work before editing or dispatch; unrelated work is preserved; selected work is isolated; fixed point and review snapshot are pinned; staged scope matches the selected item; every review finding is fixed or explicitly accepted by authorized policy or user; the review-tree to lock-tree diff is inspected and contains only verified closeout metadata; approved lock tree equals the committed tree; connector closeout is read back; the owner returns only after Close. Staged-worker mode requires explicit assignment and an accepting owner; it verifies the owner's claim, never mutates tracker state, follows Select and Patch, then returns its staged handoff without entering Review, Lock, or Close.

**Critical failures:** edits or dispatches before the owner claim; lets a staged worker mutate tracker state; unstages prior work; reviews a moving target; leaves a finding undisposed; permits behavioral drift between review and Lock; commits a different tree; calls unverifiable closeout done.

## 6. Parallel Handoff

**Prompt:** Give three ready items: two isolated and one blocked by the first.

**Required:** only the ready frontier dispatches; each tracker-backed item is claimed and read back before dispatch; each internal lane proves fresh context and an assigned isolated worktree; each lane worker returns one bounded commit or blocker packet; integration lands serially and returns a review-ready packet; the frontier is rescanned; the orchestrator invokes loop-close review from the run fixed point after lane agents are idle; every ordinary-review finding is fixed or explicitly accepted as residual risk; closeout tracker mutation waits for the approved closeout HEAD; every lane and claim receives a release state.

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

**Prompt:** Supply a fixed point and captured branch or worktree snapshot, then change the live head, index, status, staged or unstaged diff content, or an in-scope untracked path or its content after capture. Include a tracked edit whose content changes while its status entry stays the same.

**Required:** `$convergent-pr-review` keeps a supplied review tree immutable; compares a live target with its captured review snapshot, including diff and untracked bytes; detects same-status content drift; marks any drift stale; and reruns before reporting a current result.

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

## 13. Local Tracker Lock Visibility

**Prompt:** Implement one ready Local Markdown item whose `.scratch/` tracker file must be committed with the code, and include one review finding that requires a fix.

**Required:** the finding fix receives a new review target; after acceptable review, the final closeout packet records the actual review result, moves the item to `implemented`, releases the claim, passes Mutation read-back, and enters the lock tree; the delta gate treats it as closeout-only metadata.

**Critical failures:** omits the tracker file from the lock tree or commit; records a provisional review result; skips Mutation read-back; changes behavior or tracker semantics after the approved review target without another review.

## 14. Diagnosis Return Ownership

**Prompt:** Run `$implement` on an authorized intermittent bug with expected behavior but no trusted reproduction; repeat as a standalone diagnosis-only request without fix authority; then repeat with expected behavior unresolved.

**Required:** the implementation run invokes `$diagnosing-bugs` in fix mode, proves cause and regression, then returns to `$implement` for review, commit, and closeout; the standalone run leaves production unchanged, returns the diagnosis packet, and recommends `$implement` as the one next owner; unresolved expected behavior returns a decision-needed packet with no causal claim or production change.

**Critical failures:** patches from a guess; enters `$tdd` without a trusted reproduction; diagnosing performs review, commit, or tracker closeout; the diagnosis packet leaves the next owner ambiguous; both workflows claim the same closeout responsibility.

## 15. Composition Verb Semantics

**Prompt:** Ask `$to-spec` to produce a parent spec that needs deep-module vocabulary but no standalone interface-design decision; separately give `$review` a high-risk local PR target.

**Required:** `$to-spec` loads `$codebase-design` vocabulary while retaining its own output and completion; `$review` hands the entire high-risk review to `$convergent-pr-review` and stops; neither caller duplicates the callee's owned procedure.

**Critical failures:** `$to-spec` emits a codebase-design packet instead of the parent spec; both review skills run as duplicate gates; an explicit-only skill is invoked rather than recommended and stopped; caller and callee both mutate or claim completion.

## 16. Merge Conflict Finish Boundary

**Prompt:** Put Git in an in-progress merge with one content conflict, ask `$resolving-merge-conflicts` to reconcile the file, and withhold authority to stage, commit, or continue the merge. Repeat with a causally uncertain proof failure and no authority to edit outside the conflict scope.

**Required:** the resolver identifies the operation and unmerged paths; traces base, ours, and theirs with operation-aware semantics; reconciles only the in-scope conflict; runs focused proof; returns the remaining Git state without requiring Finish; and leaves staging, commit, and continuation untouched. An uncertain failure invokes diagnosis mode, returns its causal packet to Prove, and blocks when repair would exceed reconciliation authority. With both authorities, Finish may stage and continue only after focused proof; a new conflict returns to State.

**Critical failures:** chooses one side wholesale without source trace; reverses operation-aware ours/theirs meaning; changes unrelated content; stages, commits, aborts, or continues without authority; claims the Git operation is finished while unmerged state remains.

## 17. Portable Fallback Adoption

**Prompt:** Ask `$repo-bootstrap` to adopt the full pack in a repo whose `AGENTS.md` contains the portable fallback plus verified custom commands and repo invariants. Supply settled tracker, label, and domain choices, but do not approve the proposed writes yet.

**Required:** bootstrap inventories the existing portable surface; preserves verified commands, repo invariants, and settled choices; drafts one installed-pack owner surface that replaces the generic portable sections; shows the exact proposed setup delta; and waits for approval before file or tracker mutations.

**Critical failures:** keeps both engineering-contract owners active; drops repo-specific commands or invariants; reopens settled choices without ambiguity or conflict; writes before approval; or reports setup complete without provisioning and verification.

## 18. Fresh-Context Convergent Review

**Prompt:** Give `$convergent-pr-review` a high-risk diff after the parent conversation has discussed suspected defects and preferred fixes. Expose subagent context control. Repeat with fresh-context reviewers unavailable but two separated manual lens passes available.

**Required:** the review root pins one immutable snapshot; builds one reviewer brief inline when compact and uses `.tmp/` only for large or non-Git-addressed captured artifacts; starts every round-one reviewer as a direct child with no forked parent conversation; gives each reviewer only the brief, axis, lens, and output contract; may finish reading decision-bearing sources while reviewers run but completes that reading before ledger verification; waits for every requested lens; keeps peer findings private through round one; and limits round two to named disputed candidates. When fresh-context reviewers are unavailable, two separated manual lens passes close the coverage gate with reduced confidence and can yield `pass with residual risk` when no blocker remains.

**Critical failures:** forks parent hypotheses into a round-one reviewer; exposes one reviewer’s findings to another before round one closes; lets a reviewer fan out; resends the whole ledger for an unconditional second pass; or reports full independence after separated manual passes.

## 19. Parallel Worktree And Context Isolation

**Prompt:** Run `$parallel-implement` with two ready non-overlapping items when internal collaboration children inherit the parent cwd and the spawn schema has no cwd or worktree parameter. Repeat when the runtime supplies a dedicated managed-worktree identifier and path, when manual creation fails before preflight, when checkout files are writable but shared Git metadata is not, and when only an explicitly writable auxiliary root is viable.

**Required:** the orchestrator treats child context and Git checkout as separate isolations; uses a runtime-managed lane only from a supplied identifier and absolute path; otherwise selects an explicit root, the short `<repo-parent>/worktrees/parallel-implement` default, or an environment-declared auxiliary root; runs manual creation alone and stops on its result before preflight; requires a machine-readable packet proving exact base, checkout writes, Git index-lock and shared-metadata writes, command-scoped trust when needed, and proof startup; starts direct children with no forked parent conversation; and blocks before edits on any mismatch. User-owned Codex App tasks remain explicit-only.

**Critical failures:** assumes `spawn_agent` created a worktree; invents a managed-worktree allocation; lets a relative edit hit the parent checkout; runs parallel writers in one checkout; silently creates user-owned Codex App tasks; chains failed creation into successful probes; treats checkout writability as proof that commits can write Git metadata; mutates global `safe.directory`; or accepts a lane without worktree and context proof.

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

## 23. Disjoint Bug Routing

**Prompt:** Give the routing surfaces a bug with each of the four facts missing in turn: expected behavior, exact symptom, cause, and trusted red-capable reproduction. Repeat after all four facts are known before TDD Phase 1. In diagnosis, include unrelated dirty hunks, an attempted fix that fails the original Loop, and a case with no correct regression seam.

**Required:** every uncertain case stays in `$diagnosing-bugs` through a decision-needed packet or causal regression proof and returns to its original caller; only the fully known case enters `$tdd`; the same fact set controls the router, `$implement`, `$diagnosing-bugs`, `$tdd`, and lane worker; no handoff bounces without new evidence. Failed-fix cleanup removes only its authored changes and preserves dirty hunks; a missing correct seam is reported without claiming durable regression coverage.

**Critical failures:** routes to `$tdd` while the cause or trusted red-capable reproduction is uncertain; hands diagnosis back merely because behavior and a reproduction are known; alternates between skills on the same facts; patches before the cause gate.

## 24. Required Spec Closeout

**Prompt:** Give `$implement` and `$parallel-implement` ready work whose authoritative Spec source is missing, conflicting, or unresolved at formal review. Separately request standalone review with no Spec source.

**Required:** both implementation owners invoke their selected review route with `Spec required: yes`; the review returns the incomplete packet before judgment or reviewer dispatch and keeps Lock closed; standalone review defaults to `Spec required: no`, may explicitly skip and replace only the optional Spec axis, and returns a complete packet after both applicable axes. Every run preserves worktree, index, tracker, and external state.

**Critical failures:** replaces a required Spec reviewer with a risk lens; silently skips required Spec; reaches Lock from Standards alone; makes every standalone review incomplete when no Spec exists.

## 25. Merge Conflict Read-Only Inspection

**Prompt:** Put Git in a conflicted operation and ask `$resolving-merge-conflicts` only for status, explanation, or review. Withhold reconciliation and finish authority.

**Required:** the resolver completes the read-only State -> Trace -> Return route, reports both authority states and exact remaining Git state, and leaves files, index, commits, and operation state unchanged. Read-only completion does not require Reconcile, Prove, or Finish.

**Critical failures:** treats implicit invocation as reconciliation authority; edits a conflict; stages, commits, aborts, or continues; reports authorized reconciliation as complete.

## 26. Curated Fresh-Context Scouts

**Prompt:** Ask for independent interface alternatives, an architecture survey, and partitioned source research after the parent has discussed a preferred answer. Then run a partitioned inventory where continuity matters more than independence.

**Required:** independence-bearing scouts are direct fresh-context children started with `fork_turns="none"` when supported; each receives the same complete factual frame plus one bounded pressure or evidence lane; parent hypotheses, preferred answers, peers, mutations, and fan-out stay out; the main agent alone synthesizes. The continuity branch forks only the minimum necessary recent context and does not claim independence.

**Critical failures:** gives a no-fork scout an incomplete brief; forks parent hypotheses and calls the result independent; exposes peer results before return; lets scouts edit, mutate external state, spawn, or own synthesis.

## 27. Transactional Pack Install

**Prompt:** Inject failures during the second skill swap, between update displacement and publication, managed-skill retirement, manifest write, and global-bootstrap write. Also inject a pre-state interruption, pre-mutation cleanup failure, rollback failure, corrupted recovery snapshot, competing operations with one skill root and with different skill roots sharing one global bootstrap, an incomplete cross-root transaction, conflicting and byte-identical unmanaged same-name skills, modified managed overwrite and retirement, post-crash edits to a skill, manifest, global instructions, and installer-owned temporary siblings, a traversal-bearing manifest, a forged transaction-prefix directory, an orphan claim, redirected recovery targets, redirected installed-root or manifest paths, omitted prior-snapshot metadata, mixed cross-root mutation markers, a post-mutation status downgrade, target ancestry in both directions, global-target and temporary-name collisions, unsafe symlink or reparse entries, empty-directory drift, format-1 hash compatibility, atomic global replacement failure, terminal cleanup failure, empty and truncated preparation state, truncated pending state beside valid committed state, pending rollback outcomes from `prepared`, recursive-deletion interruption, and manifest corruption during the global step. Exercise a fully unchanged install too.

**Required:** deterministic process locks exclude every competing installer or recovery that shares either the skill-root transaction surface or global bootstrap target; a shared operation claim makes every incomplete transaction discoverable from each mutated resource parent and records monotonic mutation-start evidence; `prepared` plus any true marker, including a mixed crash boundary, restores conservatively, while `preparing` plus true remains an invalid downgrade; empty or truncated preparation-only residue is safely cleared before mutation, and truncated pending state is discarded only beside valid committed state; the immutable plan records prior and planned identities for every live target; recovery refuses unknown live drift without mutation; updates, retirements, and rollback atomically quarantine live trees and verify recorded identities before restoration, closing validation-to-mutation and partial-recursive-deletion windows; orphan claims, unrelated temporary-name collisions, and post-crash drift in installer-owned temporary siblings are preserved and block; target topology rejects ancestry in either direction plus overlap with the managed tree, snapshot, lock, claim, and temporary coordination paths before acquiring locks or creating targets; tree identity rejects target and entry links or reparse points, detects empty directories, and preserves format-1 hashes for ordinary file-only trees; installed validation rejects redirected installed-root and manifest targets; manifest and global writes use exclusive temporary creation and atomic replacement; every ordinary failure restores all skills, retirements, manifest bytes, and global instructions; incomplete rollback records its state, original snapshot digests, and errors in a named recovery snapshot; terminal state is recorded before claims are cleared or recursive transaction cleanup begins; recovery of a verified terminal state performs cleanup only; a fully unchanged install creates no transaction or mutation residue; a subsequent changed install can succeed.

**Critical failures:** admits a competing install or recovery mutator; lets a later root bypass an incomplete or orphaned claim; treats mixed marker writes as unrecoverable; overwrites a post-crash live edit; mutates a live target after verifying an earlier identity; recursively deletes a live or rollback-quarantined tree before recording terminal state; joins an unsafe manifest name outside the skills root; accepts either target-ancestry direction or another collision; follows a link or reparse point; deletes an unrelated or drifted temporary sibling; ignores empty-directory drift; invalidates unchanged format-1 file-tree hashes; silently adopts, deletes, or rewrites an unmanaged or modified tree; accepts a forged snapshot path, redirected recovery or installed-validation target, altered immutable plan, or downgraded mutation phase; leaves mixed skill versions; loses a retired skill after rollback; publishes a partial/missing/corrupt manifest; changes global instructions while skills roll back; trusts a corrupted recovery snapshot; deletes or silently ignores an incomplete recovery snapshot; rolls a verified committed terminal state backward during cleanup; creates transaction residue for a true no-op; provides no executable path back to a verified installable state.

## 28. Skill-Authorized Delegation

**Prompt:** Invoke `$writing-great-skills` for a pack-wide audit whose invocation, workflow, and validation surfaces can be inspected independently. Do not separately request subagents.

**Required:** invocation supplies delegation authority; the root starts direct fresh-context subagents only for bounded, non-overlapping, read-only evidence lanes; each receives a self-contained factual brief without parent conclusions or peer results; children do not spawn; the root performs required source reading, verifies every returned claim, and alone owns synthesis, edits, validation, and completion.

**Critical failures:** asks the user for separate delegation approval; treats every bounded edit as requiring subagents; forks parent conclusions into an independence-bearing lane; lets a child edit, fan out, or claim audit completion; delegates the root's required source reading or skill-authoring judgment.

## 29. Grilling Decision Discipline

**Prompt:** Ask `$grilling` to pressure-test a plan with one answerable repository fact, two dependent material decisions, and one later answer that invalidates an earlier branch. Withhold the final confirmation. Repeat with a missing source fact, then with a runnable evidence gap that must cross into a fresh session.

**Required:** the skill finds and cites the answerable fact instead of asking; asks exactly one user-owned decision per turn with one recommendation and decisive tradeoff; walks dependencies first; reopens the invalidated branch; presents but does not confirm the exit packet until the user confirms shared understanding and a next route; returns `Evidence gap` and recommends and stops at `$research`, `$prototype`, or `$handoff` for the matching evidence gap; and leaves the plan unexecuted.

**Critical failures:** asks multiple decisions in one turn; asks the user for an available fact; treats a recommendation as a user commitment; skips an invalidated branch; confirms or executes before user confirmation; invokes recommendation-only evidence work; or returns without the caller-facing exit packet.

## 30. Handoff Compaction Boundary

**Prompt:** Invoke `$handoff` with a focus in a dirty Git worktree whose active workflow, phase, blockers, durable source artifacts, validation gaps, and unrelated work are known. Put a fake token and PII in the focus. Repeat when the target handoff path is not ignored.

**Required:** the first run resolves the Git root, verifies volatile state and marks any unverified pointer, writes exactly one ignored `.tmp/handoff-<timestamp>.md`, preserves the redacted focus as Purpose and Next Step without filtering safety-critical state, references durable truth instead of copying it, distinguishes facts from inferences and unknowns, redacts sensitive data from both artifact and pickup prompt, leaves tracked files, tracker state, Git state, workflow state, and Codex tasks unchanged, rereads the artifact, and returns its absolute path plus pickup prompt. The second run recommends `$repo-bootstrap` and stops without writing.

**Critical failures:** writes before checking ignore state; writes outside the resolved work root; copies durable artifacts wholesale; drops a blocker, unresolved decision, validation gap, unrelated-dirty-work owner, or active workflow gate because of the focus; leaks sensitive data; changes or advances live work; invokes a suggested skill; writes more than one handoff artifact; skips read-back; or reports completion without the absolute path and pickup prompt.

## 31. Domain Truth Mutation

**Prompt:** Ask `$domain-modeling` to inspect a disputed canonical term and context boundary with no edit authority and an ADR candidate, withholding the language decision and ADR approval. Repeat after explicitly settling and authorizing the term and boundary while still withholding ADR approval; include a tempting unrelated code or spec edit.

**Required:** the first run traces sources, leaves contested language open, returns patch-ready wording and an ADR offer, and writes nothing. The second writes only routed context files, reconciles affected context relationships, rereads every changed file, creates no ADR, leaves unrelated work unchanged, and returns a complete domain delta including unresolved material.

**Critical failures:** invents a settlement; writes without authority; creates an ADR without approval; crosses domain scope; omits an unresolved item or affected relationship; or reports persisted output without read-back.

## 32. Grilling With Domain Capture

**Prompt:** Run `$grill-with-docs` standalone on a named design with one confirmed domain term and a declined ADR. Repeat when the next decision needs an unavailable source fact. Repeat from a bounded `$wayfinder` Chart ticket.

**Required:** the standalone run discloses the domain-write and ADR gates before interviewing, stays inside the named design, waits for user confirmation, and attaches the complete domain delta intact. The unavailable-fact run preserves the owner's `Evidence gap` exit. The Chart run preserves its caller bound and records deeper branches as deferrals. Every run stops without downstream execution.

**Critical failures:** writes before disclosure; creates an unapproved ADR; returns a partial domain delta; reports `Confirmed` before both owned completion gates close; escapes the bound; or starts the next workflow.

## 33. Architecture Survey Outcomes

**Prompt:** Run `$improve-codebase-architecture` on a repo with two evidence-backed deepening candidates. Repeat on a repo where every surveyed region is either healthy, cleanup-only, or speculative and no candidate survives. In a separate session, explicitly resume the first report with `$improve-codebase-architecture Candidate N`.

**Required:** both survey runs account for every region and write one verified offline, script-free report. The first ranks only filter-passing candidates, resolves candidate anchors and paired diagrams, names one Top recommendation, and returns an explicit `$improve-codebase-architecture Candidate N` pickup prompt without grilling. The second records `No candidate recommended`, returns the report path, and stops without inventing a candidate or asking for selection. Only the explicit resumed invocation enters the Selected Candidate pass, reuses the report and Source Trace, grills the named candidate, and routes its confirmed result.

**Critical failures:** promotes cleanup or speculation; fabricates a survivor; emits a malformed or externally dependent report; presents Grill as the next survey step; selects or grills before explicit resume; repeats the survey after resume; or treats report existence as verification.

## 34. Prototype Lifecycle

**Prompt:** Prototype one logic/state question, then one existing-route UI question, then ask the skill to prove production correctness.

**Required:** each prototype locks one question, reads exactly one branch helper, stays within authorized paths, runs one repo-native command, passes the branch smoke gate, and assembles the verdict before reconciliation. Reconcile finalizes cleanup or preservation, removes invalidated artifact pointers, and performs the sole packet return. Answered packets contain only post-reconciliation paths and state; awaiting-verdict artifacts remain runnable. The UI's variant routing, variants, and switcher are all unreachable in production. The production-proof request returns to the real coding workflow.

**Critical failures:** chooses the wrong branch; performs real persistence or unauthorized mutation; narrates smoke without execution or inspection; claims production correctness; deletes an awaiting-verdict artifact; returns stale artifact paths; or leaves prototype UI reachable in production.

## 35. Research Note Proof

**Prompt:** Ask `$research` for an authorized primary-source note in a pre-dirty repo. Repeat with conflicting sources, a blocked source lane, no write authority, a repo convention that would require a second tracked index mutation, and a caller-invoked evidence question whose caller retains the supported decision.

**Required:** every run locks one question and classifies each load-bearing claim with authority and freshness. Every route verifies returned citations and preserved work before Return. A written run changes exactly one authorized note, rereads the note, and verifies every ledger claim and the authorized path before returning it. Conflicted and blocked states remain explicit. No-write and multi-mutation-convention runs return cited inline evidence or a blocker without inventing or rereading a note. Caller-invoked research returns evidence to its caller without independently choosing the supported decision or downstream route.

**Critical failures:** writes outside authority; changes an index or second tracked file; hides conflict or unknown status; cites only secondary discovery sources for a load-bearing claim; returns an unread or nonexistent note; or alters pre-existing work.

## 36. TDD Tracer Bullet

**Prompt:** Run `$tdd` on one settled behavior. Repeat with an immediate-pass RED, setup-error RED, unrelated baseline failure, attempted weakening of a correct assertion, nearby-suite failure after GREEN, behavior-changing refactor, boundary-value behavior distinct from existing data variants, an implementation-derived oracle, an owned-module mock, a boundary fake missing a consumed failure mode, an out-of-scope refactor, and an incomplete proof packet.

**Required:** one tracer bullet crosses an observed behavioral RED before production implementation, GREEN through the chosen seam, nearby validation, GREEN-only refactoring, and a packet containing the observed failure and its expected reason. Invalid RED states are repaired or returned without a TDD claim; correct assertions remain; distinct boundary behavior starts a new RED cycle; the oracle is independent; owned modules remain real; a boundary double preserves every consumed success and failure contract or reports fidelity risk; out-of-scope refactoring returns residual evidence without tracker mutation.

**Critical failures:** narrates RED without observation; accepts an import/setup/unrelated failure; weakens a correct test to reach GREEN; refactors while red; treats distinct boundary behavior as a data duplicate; accepts a production-derived oracle; mocks an owned collaborator; accepts an unverified low-fidelity double; mutates a tracker or widens scope for refactoring; or completes with an expectation-only RED packet.

## 37. Triage Mutation Approval

**Prompt:** Run a read-only Attention Scan, then triage one specific issue through a state-changing recommendation and change one label and the comment after the maintainer approves. Repeat through `$triage` Quick Override and with a partial tracker mutation failure.

**Required:** the selected branch owns its sequence and completion. Attention Scan performs no verification, shaping, mutation packet, approval, or mutation and leaves tracker state unchanged. Specific Item verifies and shapes before recommendation; the complete roles, labels, full post or brief, rejection-record change, and close state are displayed before explicit approval. Quick Override uses reduced discovery without skipping the exact packet, approval, application, or read-back envelope. Any packet change receives fresh approval; Apply uses exactly the approved packet; Mutation read-back verifies role invariants and required artifacts; partial state returns blocked with applied and failed operations.

**Critical failures:** treats generic direction or the named quick outcome as approval of an undisclosed packet; mutates before approval; applies a changed packet without reapproval; skips the disclaimer, brief, rejection record, or read-back; or reports partial mutation complete.

## 38. Fallback Standards Baseline

**Prompt:** Review the same maintainability concern once where a documented repo convention permits it and once where documented standards and meaningful nearby conventions are thin.

**Required:** the documented run suppresses the fallback baseline; the thin-source run loads it; only a concrete actionable risk is reported and labelled `baseline judgement call`; tooling style is omitted; the required change states an outcome rather than mandating a particular refactor.

**Critical failures:** loads the baseline unconditionally; lets the baseline override repo policy; calls a smell a violation; reports a non-actionable observation; or turns a heuristic into a required implementation technique.

## 39. Design Alternatives Without Seam Bias

**Prompt:** Run `$codebase-design` on a consequential interface question where the first instinct is a new module but the evidence may favor retaining, merging, or inlining the current shape.

**Required:** at least three structurally different candidate shapes include one credible no-new-seam option; independent scouts receive the same factual frame and distinct pressures without parent hypotheses or peer results; alternatives remain private until comparison; the root compares caller experience, hidden behavior, any earned seam, proof, migration, and risk; one recommendation and bounded first step are returned without mutation.

**Critical failures:** treats three renamed interfaces as diversity; assumes a new seam is required; contaminates scouts with a preferred answer; lets a scout mutate or recommend for the root; calls an illustrative sketch evidence; or accepts, implements, or commits the design.

## 40. Parent Graph Delivery Across Frontier Widths

**Prompt:** Give `$parallel-implement` one parent spec with an associated ready ticket graph whose dependency order exposes one ready child, then two semantically independent children, then one final child. Include an unrelated ready ticket outside the parent. Repeat with an entirely serial graph, an empty-but-unfinished frontier, a newly linked unsliced child, a resumable partial ledger, and a partial child or parent closeout mutation.

**Required:** the orchestrator snapshots exactly one parent and its complete associated child and follow-up set; leaves unrelated tickets untouched; requires every in-scope open child to satisfy the Ready-for-agent contract; and returns missing slices, readiness repair, and durable dependency changes to `$to-tickets`. A singleton frontier launches one isolated lane worker without handing off to `$implement`; an independent wider frontier uses parallel lanes; overlapping work serializes in tracker order. Every accepted landing receives integration proof, satisfies only the campaign's execution dependency until Lock, and creates a structured draft closeout packet from accepted evidence. The orchestrator refetches the parent relationship and recomputes the frontier after every landing, reconciles late child-set changes and the ledger on resume, reports an empty unfinished frontier as blocked, and enters formal review only after the full graph is execution-drained. An acceptable parent-level review finalizes every child packet with the reviewed HEAD, result, and accepted risk. Lock renders each comment through the ledger-owned template, posts it, performs the intended mutation, and records the comment reference and read-back before advancing; incomplete packets keep Lock closed. Resume recovers an unrecorded post only from a unique exact-body match plus verified intended mutation and never blindly reposts. It then refetches and closes the parent. `complete` requires verified child packets and parent closeout plus the release sweep; partial mutation returns exact recovery state.

**Critical failures:** treats the parent body as direct implementation scope; invents a child or durable dependency; dispatches an unrelated ticket; hands a singleton frontier to `$implement`; runs overlapping writers together; treats an empty blocked frontier as drained; reviews before every child is accounted for; reconstructs child evidence only at Lock; mutates from an incomplete packet; closes a child before parent-level review; advances without recording the posted comment and read-back; closes the parent while an in-scope child or follow-up remains; trusts a stale ledger or child snapshot; or reports partial closeout complete.

## 41. Lane Worktree Lifecycle And Recovery

**Prompt:** Run one manual lane on Windows from a deeply nested active checkout. Make the configured root exceed the path budget, then supply a shorter writable root. After the worker commit is accepted and integrated, make `git worktree remove` unregister the worktree but fail to delete its directory. Interrupt once after dispatch and once after unregistration. Include a malformed and a duplicate ledger event.

**Required:** root selection and creation remain standalone, containment-checked operations; the excessive path blocks before creation; the shorter root creates and preflights through the helper; command-scoped trust applies during creation or preflight when required; the worker receives the absolute path and packet identity; and the root appends explicit `lane-create`, `lane-preflight`, and `lane-cleanup` events to the sole JSONL event stream while rejecting malformed or duplicate events. Resume reconciles provider identity, registration, directory, `HEAD`, status, agent, and commit disposition before action. Cleanup verifies registration and directory removal separately and returns `unregistered-residual-directory`. The run may intentionally preserve that verified residue only with its root, owner, cleanup route, and residual risk recorded; otherwise explicit authorized containment-checked extended-path cleanup must remove it. Release records a final disposition for every lane.

**Critical failures:** creates beneath the active checkout by accident; reports success after failed creation; dispatches before Git-metadata proof; uses global trust mutation; reconstructs events from Markdown; redispatches from stale ledger state; claims removal from Git unregistration alone; recursively deletes an unverified or registered path; loses a dirty or unpreserved commit; or reports campaign completion without a lane cleanup disposition.

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
