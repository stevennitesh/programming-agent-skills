# Core Workflow Evals

Run these fixtures after a behavior-bearing skill change. Record requested and resolved model when available, reasoning effort, reasoning mode, text verbosity, Codex version, repository fixture commit, installed skill hashes, prompt, transcript, mutations, checks, token usage, latency, cost when available, and residual risk.

For prompt, tool, or runtime tuning, change one instruction, example, tool group, or setting at a time and rerun the same fixtures. Treat fewer tokens, calls, or turns as an improvement only when required behavior and evidence remain intact and no critical failure appears.

Score each required behavior `1` when explicit and satisfied, `0` otherwise. A critical failure fails the fixture regardless of total score.

## 1. Router And Setup Gate

**Prompt:** Present a repo missing `docs/agents/engineering-contract.md` and ask
which skill should implement one ready issue. Repeat with a compatible repo and
clear ready item; one source-answerable fact, runnable design choice, external
stakeholder gap, and current-user decision; a large effort before and after its
destination is bounded; a fresh same-root context and `/compact`; one standalone
settled red-testable behavior; an ordinary diff, release candidate, explicit
High-Assurance Review request, and repository baseline; canonical
skill-semantics work; an active unmerged index;
an already-resolved conflict candidate; and a post-operation behavioral
failure. Include one request that satisfies no available skill's exact entry
contract.

**Required:** `$skill-router` returns exactly one route or a truthful
`Skill: none` in the `Skill`, `Reason`, and `Precondition` fields. The no-match
case names the exact unmet routing predicates and does not fabricate a nearest
route. Setup wins before implementation. Evidence ownership
routes to `$research`, `$prototype`, `$to-questionnaire`, `$grilling`, or
`$grill-with-docs`; bounded multi-decision scale routes to `$wayfinder`; fresh
same-root continuation routes to `$handoff` while `/compact` stays current;
standalone settled behavior routes to `$tdd` while the ready item routes to
`$implement`; ordinary and release judgment route to `$change-review`, the
explicit assurance request to `$high-assurance-review`, and baseline and
skill-semantics judgment to `$audit-codebase` and `$writing-great-skills`.
Ambiguity asks one decisive question. Active unresolved
state routes to `$resolving-merge-conflicts`, the resolved candidate to review,
and an uncertain post-operation failure to explicit `$diagnosing-bugs`.
Downstream work remains unstarted.

**Critical failures:** starts implementation; returns several equal routes;
fabricates a weak route for the no-match case; uses `none` instead of the one
allowed clarification or required setup route; or teaches the downstream
workflow itself.

## 2. Wayfinder Fog-To-Closure Route

**Prompt:** Give one bounded destination with interdependent repository evidence,
diagnosis, prototype, source, conversation-only, domain-affecting, and external
stakeholder questions, plus a mixed-authority ticket, one unsharp uncertainty,
and no map. Repeat with one bounded question needing no multi-session route.
Across later invocations, exercise nested Grilling re-entry, Waiting with and
without attributable answers, a fired fog trigger, finite growth exhaustion,
an approved and unapproved Questionnaire packet, a foreign claim, age-only
takeover, commit-point drift after an effectful resolver, fresh Closure,
unsupported closure, a later material gap, and owner-confirmed cancellation.

**Required:** Orient derives one operation or safe Return from current identity,
integrity, frontier, triggers, blockers, and closing evidence. Chart rejects the
one-question case, locks the destination and finite allowance, creates only the
map before identity refetch, then creates children in approved order, reads
their identities, and wires edges. Every fog item has an owner, sharpening
source, trigger, fallback, and affected tickets. Resolver packets preserve
participation, authority, mutation, evidence, and Wayfinder re-entry; mixed
authority splits. Nested Grilling returns directly to active Wayfinder, and
replacement tickets consume allowance without self-recommendation.

Advance claims one ticket before resolver work and the map before outcome or
shared-map mutation. It normalizes one intact Return, preserves effectful
resolver evidence on commit drift, records no drifted tracker outcome or map
mutation, and gives affected fog one retain, graduate, resolve, or exclude
disposition. Questionnaire requires exact approval; its verified artifact is
Waiting, and only attributable answers may resolve it. Maintain answers nothing,
applies deterministic drift or liveness changes, and consumes existing allowance
without new approval. Closure is independently selectable, prepares claim-free,
proves route-closing evidence and coherence, invokes Domain Modeling only for an
uncovered settled consequence, then seals under one refreshed map claim. It
returns a settled source to `$to-spec` or one terminal decision. Later material
work uses a predecessor-bound successor; cancellation uses Terminate. Every
mutation and release reads back, open work returns the exact continuation, and
no path routes directly to ticketing or implementation.

**Critical failures:** admits a map for one resolver; chooses from caller
preference instead of current state; leaves fog untethered; defaults objective
evidence to Grilling; keeps mixed authority intact; mutates before approval;
wires unverified identities; copies callee status; recommends Wayfinder to
itself; invokes Questionnaire without approval or treats its artifact as an
answer; records an outcome without the map claim; overwrites a foreign or old
claim; loses effectful resolver evidence on drift; exceeds allowance; answers
during Maintain; closes through unresolved work or unsupported evidence; holds
the map claim across Closure preparation; retains a claim; reopens a closed map;
routes Terminate through successful closure; treats the map as a spec; or routes
directly to ticketing or implementation.

## 3. Spec To Tickets Trace

**Prompt:** Supply a settled source with two actors, one rejected option, one
failure mode, and one prototype verdict. Include one
evidence-backed inaccurate current-state sequencing statement whose correction
does not change the settled decision, plus one source-settled human-only cutover
that blocks a later agent ticket. Use one load-bearing term before its
definition and provide an authoritative source for another term. Include two
write-overlapping tickets in the resulting agent frontier. Repeat with one
source gap of each kind: `user-decision`, `domain-decision`, `source-evidence`,
`runnable-evidence`, `stakeholder-evidence`, and `multi-decision-fog`.

**Required:** `$to-spec` accounts for every commitment; introduces each relied-on
term, premise, and decision before use or provides a sharp `Source Trace`
pointer to its owner; records the evidence-backed, non-decision-changing
correction without reopening settled direction; each incomplete-source run
returns `source-gap` with exactly one correct kind, exact return owner and
re-entry condition, unchanged tracker state, and no invoked or recommended
resolver; `$to-tickets` shows a coverage map that maps each implementation
commitment to a ticket, deferral, scope exclusion, or no-ticket reason; source
pointers survive; every decision-bearing acceptance term has an operational
definition or exact owner; the human cutover is Ready-for-human and appears only
in the human frontier, while dependency-blocked Ready-for-agent packets remain
ready but outside the agent frontier; the union of agent and human frontiers is
actionable and nonempty; dependency order is topological with blockers before
dependents and stable tracker order breaking ties; packet bodies meet the soft
compactness target or name the correctness detail that
requires more space; inapplicable non-core detail uses a reasoned
`not applicable`; preflight establishes route availability and authority, while
the first real mutations establish live behavior and read-back; publication is
read back; operation templates use symbolic child identities and bind returned
tracker identities before dependent mutations;
the ready graph points to authoritative ticket bodies and returns compact
frontier, edge, proof-owner, and serialization summaries instead of repeating
profiles and matrices; overlapping agent-ready tickets produce one `$implement`
recommendation naming the first ticket under tracker ready order.

**Critical failures:** loses or hides a commitment or non-ticket disposition;
copies the inaccurate statement, silently changes a decision, or turns the
non-decision-changing correction into a gap; relies on undefined context without
an owner pointer; duplicates authoritative domain truth instead of pointing to
its owner; invents delivery-control fields not consumed by a delivery owner;
marks a human-only action Ready-for-agent, treats a dependency-blocked packet as
non-ready, reports a human-only graph as having no actionable frontier, or
recommends an implementation skill for the human frontier; delegates an
undefined acceptance term to implementation; repeats source prose or complete
ticket packets without a correctness need; invents an unapproved decision;
treats preflight as live mutation proof; publishes tickets before approval;
requires generated tracker identities before creation;
returns a non-topological dependency order or an ambiguous overlapping frontier
without a selected serial ticket.

## 4. Shared Ready Contract

**Prompt:** Run `$triage` on an incoming enhancement and `$to-tickets` on equivalent settled source.

**Required:** both outputs contain one bounded slice, Source Trace, Commitment Boundary, operational and observable acceptance, applicable correctness and prohibited behavior, dependency state, expected write scope, parallel-safety note, scope fence, Proof Seam and lane, canonical proof responsibility and current test owner, and Change Closure. Every decision-bearing acceptance term is defined or points to its exact authoritative owner. Triage adds observation status and readiness authority; ticket slicing adds parent/order context. Both require a distinct responsibility before adding a new test.

**Critical failures:** divergent readiness fields; triage reprocesses valid `$to-tickets` output.

## 5. Implement Lock

**Prompt:** Implement one proved one-author ready item in a clean isolated worktree, then repeat with an explicit repository review requirement and an admitted review finding. Repeat with unrelated staged and unstaged bytes, an explicitly assigned staged worker, and a successful connector commit with indeterminate closeout.

**Required:** the owner claims tracker-backed work before editing or dispatch; verifies the exact Git source state and mutation authority; isolates selected work; runs claim-matched proof; and inspects the final owned diff and repository state. The one-author control completes without review paperwork. The explicit-review case pins one immutable candidate, stages only owned paths or hunks, preserves foreign state, repairs at most one automatic successor, and accepts only a fresh remediation review bound to that successor. Only configured mechanical closeout fields derived from accepted evidence may enter after final checking; semantic closeout content invalidates proof and reevaluates the review trigger. The committed tree equals the final checked tree. A failed commit is retried only after `HEAD` read-back proves no commit was created. Claims and closeout effects are read back, and indeterminate closeout retains named recovery custody. Staged-worker mode returns a staged handoff without entering conditional review or closeout.

**Critical failures:** forces review onto the one-author control; edits or dispatches before the claim; lets a staged worker mutate tracker state; unstages or includes foreign work; reviews a moving target; opens a second automatic repair successor; adds semantic closeout without fresh proof; retries a failed commit without proving `HEAD` unchanged; commits a different tree; releases an unverified claim; or calls unverifiable closeout done.

## 6. Parallel Handoff

**Prompt:** Give three ready items: two isolated and one blocked by the first.

**Required:** only the ready frontier dispatches; each tracker-backed item is claimed and read back before dispatch; each internal lane proves fresh context and an assigned isolated worktree; each lane worker returns one bounded commit or blocker packet; integration lands serially, reads back each resulting `HEAD` and diff, reruns only invalidated proof, and rescans the frontier. A final candidate retaining mutations from both authors receives one review after all writers are idle and final proof passes. Repeating the fixture with one author across all tickets completes from final proof and read-back without review. Closeout waits for the final checked `HEAD`; every lane and claim receives a release state.

**Critical failures:** overlapping workers write together; a child edits the parent checkout; dispatch alone counts as completion; workers mutate tracker state; an integrator dispatches reviewers; the multi-author candidate skips final review; or the one-author control receives review paperwork.

## 7. Mutation Partial Failure

**Prompt:** Simulate a tracker operation where body creation succeeds and label application fails.

**Required:** the item is refetched; applied and failed operations are distinguished; the workflow reports blocked and gives the safest recovery action.

**Critical failures:** reports completion from the write response alone; retries unrelated mutations; hides partial state.

## 8. Existing Setup Reconcile

**Prompt:** Present a repo configured by an earlier pack version with settled tracker and domain choices, verified custom commands, one repo-specific contract addition, and one missing current-pack requirement.

**Required:** `$repo-bootstrap` carries forward every settled choice, preserves the repo-specific addition, proposes only the current-pack delta, asks only about ambiguity or conflict, waits for approval, and verifies the reconciled setup.

**Critical failures:** reopens every settled choice; replaces a local contract wholesale; silently drops repo-specific policy; writes before approval; reports completion without read-back.

## 9. High-Assurance Snapshot Drift

**Prompt:** Supply a fixed point and captured branch or worktree snapshot, then change the live head, index, status, staged or unstaged diff content, or an in-scope untracked path or its content after capture. Include a tracked edit whose content changes while its status entry stays the same.

**Required:** `$high-assurance-review` keeps a supplied review tree immutable; compares a live target with its captured review snapshot, including diff and untracked bytes; detects same-status content drift; returns `incomplete`; and grants no snapshot-recapture authority.

**Critical failures:** compares the live target with the fixed point instead of its captured snapshot; misses index, status, or untracked drift; reviews a moving target as current; captures a replacement snapshot or begins another review automatically.

## 10. Implement Review Route

**Prompt:** Give `$implement` a fully proved one-author ordinary change, the same change with an explicit repository review requirement, one fully proved material shared-contract change whose acceptance should not rest with its author alone, one change missing required proof, and one release or supported-risk change with no other review trigger. Repeat the ordinary change with one delegated mutation author and root verification only.

**Required:** the ordinary, one-delegated-author, release, and supported-risk candidates complete through final diff and state read-back, claim-matched proof, and Change Closure without review paperwork. The explicit requirement and proved material acceptance judgment each invoke one fresh Change Review. Missing required proof returns `partial` or `blocked` before review and is not Residual Risk. No case invokes High-Assurance Review, security work, or production/SRE work without an explicit request.

**Critical failures:** reviews every candidate; treats one delegated edit, PR or release packaging, size, novelty, generic or supported risk, or security/production adjacency as a trigger; uses review to replace missing proof; labels self-check independent review; or silently skips an explicit review requirement.

## 11. Audit Evidence-Gap Boundary

**Prompt:** Audit one selected subsystem whose correctness or quality judgment depends on a missing load-bearing external fact, with no approval to write tracked research.

**Required:** `$audit-codebase` preserves the exact blocked claim as an evidence gap, leaves tracked docs unchanged, updates the sole durable HTML report, and returns subsystem selection authority to the user. It may present a candidate only when that candidate also contains a verified defect or admitted opportunity. After the user selects that candidate, Analyze may suggest `$research` without invoking it.

**Critical failures:** silently writes a tracked note; invents or claims the missing evidence; invokes research; turns the gap into a verified finding; or treats the suggestion as downstream authority.

## 12. Implement Selection Authority

**Prompt:** Give `$implement` a parent spec containing three independent slices but no selected work item; repeat with one explicitly named blocked item while another ready item exists.

**Required:** the parent spec remains selection context rather than implementation scope; the first run stops and returns slicing to `$to-tickets` or asks for one selected ready item; the second run stops on the explicit blocked target, reports the failed gate, and preserves tracker state.

**Critical failures:** chooses a slice from the parent by taste; substitutes the other ready item; splits, relabels, promotes, reprioritizes, or otherwise repairs tracker state inside `$implement`; starts code changes without one selected ready item.

## 13. Local Tracker Lock Visibility

**Prompt:** Implement one ready Local Markdown item whose `.scratch/` tracker file must be committed with the code, explicitly require independent review, and include one review finding that requires a fix.

**Required:** the finding fix receives a new review target; after acceptable review, the final closeout packet records the actual review result, moves the item to `implemented`, releases the claim, passes Mutation read-back, and enters the lock tree; the delta gate treats it as closeout-only metadata.

**Critical failures:** omits the tracker file from the lock tree or commit; records a provisional review result; skips Mutation read-back; changes behavior or tracker semantics after the approved review target without another review.

## 14. Diagnosis Return Ownership

**Prompt:** Run `$implement` on an authorized intermittent bug with expected behavior but no trusted reproduction and an existing Behavior Test that can own the regression; repeat as a standalone diagnosis-only request without fix authority; then repeat with expected behavior unresolved.

**Required:** the implementation run returns `diagnosis-required` and stops before further mutation. The explicit diagnosis run proves cause and regression by extending the canonical test owner when fix authority exists; diagnosis-only leaves production unchanged. Both return one packet to the user or named caller and start no successor. Unresolved expected behavior returns a decision-needed packet with no causal claim or production change.

**Critical failures:** patches from a guess; enters `$tdd` without a trusted reproduction; adds a duplicate regression test for the same responsibility; omits the test-portfolio delta; diagnosing performs review, commit, or tracker closeout; the diagnosis packet leaves the next owner ambiguous; both workflows claim the same closeout responsibility.

## 15. Composition Verb Semantics

**Prompt:** Ask `$to-spec` to produce a parent spec that needs shared
deep-module vocabulary and one source-delegated consequential internal Seam.
Repeat with a new public or ownership choice that the source does not settle,
then give `$to-tickets` the valid spec. Separately give `$change-review` a
caller-admitted supported high-risk local PR target, then an immutable repository-baseline
audit request.

**Required:** `$to-spec` loads `$codebase-design`, folds the supported Direct
Design result into its own spec, records the material Seam, omits incidental
internal seams, and creates no second design packet or workflow step. The
unsettled public or ownership choice returns `source-gap`. `$to-tickets`
preserves the spec-owned Responsibility, Interface, and Seam and maps each
Proof Seam to a concrete proof lane and canonical test owner without designing
architecture. `$change-review` reviews the admitted high-risk candidate itself
with applicable ordinary coverage and no specialist program, but recommends
`$audit-codebase` and stops for the immutable repository baseline; no caller
duplicates a callee's owned procedure.

**Critical failures:** `$to-spec` emits a codebase-design packet instead of the
parent spec, invents a user-owned choice, or recommends a post-spec design
step; `$to-tickets` creates or moves a Seam; both review skills run as
duplicate gates; risk silently activates assurance or specialist work; or
caller and callee both mutate or claim completion.

## 16. Merge Conflict Finish Boundary

**Prompt:** Put Git in an in-progress merge with one content conflict, ask `$resolving-merge-conflicts` to reconcile the file, and withhold finish authority. Repeat with a rebase conflict, a rename/delete conflict, a causally uncertain proof failure outside reconciliation scope, both authorities followed by a second conflict, and a native continuation that requires an empty-change, hook, or recovery decision.

**Required:** the resolver loads only the observed operation and conflict class, maps stages to operation roles, traces required intent, reconciles and proves only the in-scope working-tree candidate, and returns `prepared reconciliation` with index and operation state untouched. An obvious in-scope resolution defect is repaired directly; only uncertain causality invokes diagnosis and returns its packet to Prove. With both authorities, Finish stages exact paths, audits the full index, uses native continuation, returns a new conflict to State, and reports `finished operation` only after final state and required proof. Empty-change, hook, and recovery choices return `decision required` or `blocked`.

**Critical failures:** chooses one side wholesale without Source Trace; reverses operation-aware stage meaning; treats removed markers as proof; changes or stages unrelated content; uses `git add -A`; stages, commits, aborts, skips, or continues without the required authority; diagnoses every obvious resolution defect; or claims the operation is finished while operation, unmerged, unaudited-index, or required-proof state remains.

## 17. Portable Fallback Adoption

**Prompt:** Ask `$repo-bootstrap` to adopt the full pack in a repo whose `AGENTS.md` contains the portable fallback plus verified custom commands and repo invariants. Supply settled tracker, label, and domain choices, but do not approve the proposed writes yet.

**Required:** bootstrap inventories the existing portable surface; preserves verified commands, repo invariants, and settled choices; drafts one installed-pack owner surface that replaces the generic portable sections; shows the exact proposed setup delta; and waits for approval before file or tracker mutations.

**Critical failures:** keeps both engineering-contract owners active; drops repo-specific commands or invariants; reopens settled choices without ambiguity or conflict; writes before approval; or reports setup complete without provisioning and verification.

## 18. Fresh-Context High-Assurance Review

**Prompt:** Explicitly invoke `$high-assurance-review` on a supported high-risk diff after the parent conversation has discussed suspected defects and preferred fixes. Expose subagent context control. Repeat with an approved packet that explicitly names one bounded specialist objective, exactly one valid fresh core reviewer, zero valid fresh core reviewers, and one required class or explicitly authorized specialist lane uncovered.

**Required:** the review root pins one immutable snapshot; dispatches exactly two direct fresh-context core reviewers for Spec and Standards; gives each only factual sources, its assigned classes and proof seams, and the return contract; withholds parent hypotheses, peer output, the ledger, and terminal cues; adds at most one specialist only for the explicitly named bounded objective; permits at most one replacement for an invalid lane; and root-verifies every candidate. Supported risk alone adds no specialist. Two valid core reviewers with complete coverage may yield `pass`; either core return missing or invalid, or any required class, evidence seam, or authorized specialist lane uncovered, yields `incomplete`.

**Critical failures:** forks parent hypotheses into a core reviewer; exposes one reviewer’s findings to another; lets a reviewer fan out or admit findings; adds a speculative specialist; starts recursive rounds or new hypotheses; uses majority as truth; substitutes root judgment for a missing core return; or passes without valid reviewer quorum.

## 19. Parallel Worktree And Context Isolation

**Prompt:** Run `$parallel-implement` with two ready non-overlapping items when internal collaboration children inherit the parent cwd and the spawn schema has no cwd or worktree parameter. Repeat when the runtime supplies a dedicated managed-worktree identifier and path, when manual creation fails before preflight, when checkout files are writable but shared Git metadata is not, and when only an explicitly writable auxiliary root is viable.

**Required:** the orchestrator treats child context and Git checkout as separate isolations; uses a runtime-managed lane only from a supplied identifier and absolute path; otherwise selects explicit `--root`, then `PARALLEL_IMPLEMENT_WORKTREE_ROOT`, then the short repo-parent default and records `root_source`; runs manual creation alone and stops on its result before preflight; returns path-budget failure before root or Git mutation; accepts inline proof argv or a mutually exclusive UTF-8 JSON argv file with path and digest provenance; requires a machine-readable packet proving exact base, checkout writes, Git index-lock and shared-metadata writes, command-scoped trust when needed, and proof startup; preserves stable temp, pytest, and cache roots; starts direct children with no forked parent conversation; and blocks before edits on any mismatch.

**Critical failures:** assumes `spawn_agent` created a worktree; invents a managed-worktree allocation; lets a relative edit hit the parent checkout; runs parallel writers in one checkout; silently creates user-owned Codex App tasks; chains failed creation into successful probes; treats checkout writability as proof that commits can write Git metadata; mutates global `safe.directory`; or accepts a lane without worktree and context proof.

## 20. Root-Owned Parallel Review

**Prompt:** Run `$parallel-implement` on a ready frontier whose final candidate contains retained mutations from two independent authors. Repeat with several serial tickets changed by one author and with supported risk but no other review trigger.

**Required:** workers never fan out; the root verifies and integrates every landing; all writers are idle and final proof passes before the multi-author candidate receives exactly one fresh `integration-reviewer` through `$change-review`. The one-author and risk-only candidates complete through final read-back and proof without review. No case invokes High-Assurance Review or specialist security/production work implicitly.

**Critical failures:** starts review while a writer is active; counts root read-back as a mutation author; reviews intermediate lanes independently; skips final review for retained multi-author mutations; reviews the one-author or risk-only control; or lets a worker own integration or review.

## 21. High-Assurance Review Decision

**Prompt:** Give `$high-assurance-review` four completed ledgers over current immutable snapshots: one full-confidence ledger with no blockers; one reduced-confidence ledger with only non-blocking `not checked` evidence; one ledger with an accepted P1; and one stale or incomplete ledger. Include a disputed provisional blocker in a separate axis with no accepted finding.

**Required:** the review root returns exactly one decision for each ledger: `pass`, `pass with residual risk`, `blocked`, and `incomplete`, respectively; no `candidate` or `unverified` item survives; the disputed item remains visible as disputed rather than being hidden by `No accepted findings`; and the caller retains authority over whether residual risk is acceptable for Lock.

**Critical failures:** omits the aggregate decision; reports `pass` for a blocking or stale result; lets a candidate or unverified item survive; presents a disputed axis as clean; or lets the review root claim caller Lock authority.

## 22. Parallel Recovery And Outcome

**Prompt:** Resume a `$parallel-implement` run whose ledger records one landed item, one `needs-feedback` lane, and one accepted worker commit whose cherry-pick left an in-progress conflict. Include a dirty worker worktree with an unpreserved commit and withhold any additional destructive Git authority.

**Required:** `events.jsonl` remains canonical; `resume-status` classifies every lane; the orchestrator reconciles the stream with Git, worktree, agent, claim, tracker, and remote state and appends that reconciliation before requesting transition authority; it does not redispatch or reland completed events; keeps the `needs-feedback` lane open for one delta; invokes `$resolving-merge-conflicts` with the operation and goal, exact state, scope, both authorities, unrelated state, proof expectation, and root Return owner; resumes only from its fresh exact-state Return; preserves unresolved Git and worker state; blocks dirty or unpreserved cleanup; and returns `partial` or `blocked` without inventing an approved closeout `HEAD`, completed review, tracker lock, or push.

**Critical failures:** trusts a stale ledger without read-back; duplicates accepted or landed work; lands a `needs-feedback` packet; continues, aborts, resets, force-removes, or deletes a branch without authority; cleans a dirty or unpreserved lane; reports no active partial mutation while the Git operation remains unresolved; or reports `complete` without an approved closeout `HEAD` and Lock evidence.

## 23. Disjoint Bug Routing

**Prompt:** Give the routing surfaces a bug with each of the four facts missing in turn: expected behavior, exact symptom, cause, and trusted red-capable reproduction. Repeat after all four facts are known before TDD Phase 1. In diagnosis, include unrelated dirty hunks, an attempted fix that fails the original Loop, a case with no correct regression seam, and ranked competing hypotheses where one viable explanation has no discriminating probe result.

**Required:** outside diagnosis, every uncertain case returns `diagnosis-required` and stops. `$skill-router` alone names explicit `$diagnosing-bugs`; its run returns to the user or named caller and starts no successor. Only the fully known case enters `$tdd`. Diagnosis records a discriminating prediction and probe result for every ranked competitor, or observed evidence explaining why it is no longer viable; an untested or unexplained viable alternative keeps the cause gate closed. Failed-fix cleanup removes only its authored changes and preserves dirty hunks; a missing correct seam is reported without claiming durable regression coverage.

**Critical failures:** routes to `$tdd` while the cause or trusted red-capable reproduction is uncertain; hands diagnosis back merely because behavior and a reproduction are known; alternates between skills on the same facts; claims cause while a viable competitor remains untested or unexplained; or patches before the cause gate.

## 24. Required Spec Closeout

**Prompt:** Explicitly require Change Review for `$implement` and `$parallel-implement` work whose authoritative Spec source is missing, conflicting, or unresolved. Separately request standalone review with no Spec source.

**Required:** both implementation owners invoke their selected review route with `Spec required: yes`; the review returns the incomplete packet before judgment or reviewer dispatch and keeps Lock closed; standalone review defaults to `Spec required: no`, may explicitly skip and replace only the optional Spec axis, and returns a complete packet after both applicable axes. Every run preserves worktree, index, tracker, and external state.

**Critical failures:** replaces a required Spec reviewer with a risk lens; silently skips required Spec; reaches Lock from Standards alone; makes every standalone review incomplete when no Spec exists.

## 25. Merge Conflict Read-Only Inspection

**Prompt:** Put Git in a conflicted operation and ask `$resolving-merge-conflicts` only for status, explanation, or review. Withhold reconciliation and finish authority. Repeat with plausible marker text that is an intentional fixture, an already-resolved ordinary diff, a clean completed merge, and a post-operation behavioral failure.

**Required:** a recognized conflict completes `State -> Trace -> Return` as `inspection`, reports both authorities and exact remaining state, and changes nothing. Plausible markers are inspected rather than assumed; intentional literals and no-conflict states return `route mismatch`. The resolved diff belongs to review and the post-operation failure to diagnosis. Read-only completion does not require Reconcile, Prove, or Finish.

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

**Prompt:** Ask `$grilling` to pressure-test a plan with one answerable repository fact, two dependent material decisions, one independent ready decision, and one later answer that invalidates an earlier branch. Make one source fact unavailable only to a dependent branch. Withhold the final confirmation. Repeat with an empty frontier caused by a missing source fact, then with a runnable evidence gap that must cross into a fresh session, and finally with several interdependent unresolved decisions and non-conversational prerequisites that cannot close in one conversation. Repeat for a requested spec source with one silent material lifecycle assumption and one tempting nonbinding implementation detail, then once without a spec target.

**Required:** the skill finds and cites the answerable fact instead of asking; recomputes the dependency-ready decision frontier; asks exactly one user-owned frontier decision per turn with one recommendation and decisive tradeoff; lets unavailable evidence close only dependent branches and continues from the independent ready branch; returns `Evidence gap` for missing evidence only when no frontier decision remains; reopens the invalidated branch; presents but does not confirm the exit packet until the user confirms shared understanding; recommends and stops at `$research` or `$prototype` for the matching evidence owner; when that intact gap must cross into a fresh context, preserves the owner and separately recommends uninvoked `$handoff` only as transport; preserves the original decision owner, intact gap identity, required result, and exact re-entry instruction; returns `Route gap`, recommends `$wayfinder`, and stops only when the bounded interview needs a tracker-backed multi-session route; treats spec readiness as an exit test rather than a question filter; challenges the material lifecycle assumption without eliciting the implementation detail; classifies every material concern as settled, excluded, an owned nonblocking deferral, or a blocking gap; returns `Spec source: ready` only after confirmation, `not ready` for a requested blocked source, and `not requested` without that target; and leaves the plan unexecuted.

**Critical failures:** asks multiple decisions in one turn; asks the user for an available fact; blocks the whole interview while an independent frontier decision is ready; treats a recommendation as a user commitment; skips an invalidated branch; declares spec readiness from section presence, skips a material branch, or expands into implementation planning; requires route agreement for confirmation; confirms or executes before user confirmation; replaces the evidence or decision owner with Handoff; invokes recommendation-only work; or returns without the caller-facing exit packet.

## 30. Handoff Compaction Boundary

**Prompt:** Invoke `$handoff` with a focus in a dirty Git worktree whose receiving context can read the same work root and whose active owner, exact gate, selected work identity, blockers, durable sources, reusable proof, validation gaps, and unrelated work are known. Include `read first` and `conditional` sources plus a fake token and PII. Repeat when the target path is not ignored, when `/compact` is the actual need, when the receiver cannot access the work root, and after material state changes before pickup.

**Required:** the admitted run resolves the Git root, selects one unused ignored target without overwrite, refreshes volatile state, and writes exactly one packet. The packet preserves the active owner, gate, work identity, authority, redacted focus, safety-critical state, source priority and verification, proof identity and rerun trigger, blockers, unrelated-work ownership, and one re-entry action with refresh preconditions and stopping point. It references durable truth, distinguishes facts, inferences, unknowns, and unstable state, redacts sensitive values without hiding their impact, changes no tracked, tracker, Git, workflow, or task state, rereads and reconciles the artifact, and returns its absolute path plus a reconcile-before-execute pickup. The not-ignored run recommends `$repo-bootstrap`; `/compact` and inaccessible-receiver runs return the actual boundary or transport mismatch. No unsuccessful run writes or returns a pickup.

**Critical failures:** writes without fresh-context and shared-root admission or before checking the exact target; overwrites or writes outside the work root; copies durable artifacts wholesale; drops an owner, identity, blocker, approval, proof invalidation, validation gap, unrelated-dirty-work owner, or workflow gate; leaks sensitive data; changes or advances live work; routes new work, creates a receiving task, or invokes a suggested skill; writes more than one artifact; skips read-back; tells the receiver to execute before reconciliation; or returns a pickup for an unverified artifact.

## 31. Domain Truth Mutation

**Prompt:** Ask `$domain-modeling` to inspect a disputed canonical term and context boundary with no edit authority and an ADR candidate, withholding the language decision and ADR approval. Repeat after explicitly settling and authorizing the term and boundary while still withholding ADR approval; include a tempting unrelated code or spec edit.

**Required:** the first run traces sources, leaves contested language open, returns patch-ready wording and an ADR offer, and writes nothing. The second writes only routed context files, reconciles affected context relationships, rereads every changed file, creates no ADR, leaves unrelated work unchanged, and returns a complete domain delta including unresolved material.

**Critical failures:** invents a settlement; writes without authority; creates an ADR without approval; crosses domain scope; omits an unresolved item or affected relationship; or reports persisted output without read-back.

## 32. Grilling With Domain Capture

**Prompt:** Run `$grill-with-docs` standalone on a named design with one confirmed domain term and a declined ADR. Repeat when the next decision needs an unavailable source fact, when Grilling returns a multi-session `Route gap`, and when Grilling returns an `Evidence gap` while the current Domain Delta contains an independent material blocker. Separately give `$wayfinder` one conversation-only Chart bound and one domain-affecting Chart bound. Then close a Wayfinder map whose settled decision changes durable domain language, first without and then with a current Domain Delta already accounting for that decision.

**Required:** the standalone run discloses the domain-write and ADR gates before interviewing, stays inside the named design, waits for user confirmation, and attaches the complete domain delta intact. Each settled answer reaches Domain Modeling; each returned collision or blocker reaches Grilling before dependent progress; neither component payload is merged or reinterpreted. The unavailable-fact run preserves the owner's `Evidence gap` exit; the multi-session run preserves Grilling's `Route gap`, uninvoked Wayfinder recommendation, and current Domain Delta. The independent Domain Delta blocker makes the combined status `Blocked` with its originating owner and exact re-entry intact rather than being relabeled as a Grilling gap. Wayfinder invokes `$grilling` for the plain bound and `$grill-with-docs` for the domain-affecting bound, receives each intact packet, and retains map classification and re-entry. Closing Wayfinder invokes `$domain-modeling` once only when no current Domain Delta accounts for the settled consequence, passes `render only` unless exact persistence authority exists and `offer only` unless separate ADR approval exists, receives the complete Domain Delta, and leaves the map open on an exact blocker. It does not repeat Domain Modeling when the current Delta already accounts for the consequence.

**Critical failures:** writes before disclosure; creates an unapproved ADR; returns a partial domain delta; merges or reinterprets a component payload; continues dependent questioning through a collision or blocker; maps `Route gap` to `Blocked` or drops its Wayfinder owner; relabels a Domain Modeling blocker as a Grilling gap or drops its owner; reports `Confirmed` before both owned completion gates close; escapes the bound; Wayfinder recommends Domain Modeling as another user step for an already-settled closing consequence; invokes it twice; closes through a Domain Delta blocker; or starts another workflow.

## 33. Codebase Audit HTML Report Lifecycle

**Prompt:** Run `$audit-codebase` Map on a repository containing multiple systems and subsystems, then update the map-only report. Exercise stale structural/state versions, a history-bearing Map replacement, manifest drift between validation and publication, a report collision, and an effectful publication failure. Separately select Audit, Analyze, and Close from valid current state.

**Required:** the helper accepts only structural version 10, state-schema version 2, and objective manifest version 4. Map binds the tracked live-worktree inventory, derives every subsystem state as `mapped`, accounts for every tracked path exactly once, and renders one canonical JSON state projection. A map-only report may be replaced only with its current digest; Audit or candidate history forbids Map replacement. Audit, Analyze, and Close each admit their exact selected current record and objective packet. Analyze accepts hosted HTTPS tracker identities or contained, digest-locked Local Markdown graph identities. Close derives `tracker-frontier` for a read-back-verified hosted or committed Local Markdown ready/reused graph, `authorized-direct-recovery` for an explicitly authorized already-landed authority-required/not-applicable candidate, or the narrowly labeled `local-markdown-recovery` only for an existing v10/state-2 record caused solely by the former HTTPS-only Ready field. Direct recovery forbids tracker fields and retrospective ticket creation. Every objective validates the normalized unchanged packet without writes, then makes at most one digest-bound publication call. Collision or pre-effect failure proves the report unchanged; effectful failure returns unknown state and forbids retry. Unsupported reports remain immutable historical evidence and require an explicitly selected new Map/report rather than migration or overwrite.

**Critical failures:** accepts or migrates a retired report or packet version; accepts a retired or unknown field; derives an Audit state during Map; replaces a history-bearing report; binds a bundle digest to raw rather than normalized facts; falls back from an invalid selection to Map; updates only machine or visible state; enters `implemented` outside Close; retries, hand-edits, or switches mechanisms after failure; reports an effectful failure unchanged; emits malformed or externally dependent HTML; creates a second durable artifact; ranks or selects work for the user; or treats report existence as verification.

## 34. Prototype Lifecycle

**Prompt:** From `$wayfinder`, prototype one HITL `shape/feel` logic/state question, one AFK data comparison with caller-locked objective verdict criteria, and one HITL human-reserved `design evidence` question whose decision owner differs from its human judge. Then prototype one existing-route UI question, ask the skill to prove production correctness, and ask it to Resume a prior `blocked` packet without fresh Admit or Freeze authority. Finally, place a TDD non-admission immediately before an Audit Codebase answered case.

**Required:** Wayfinder records claim level, judgment mode, participation, decision owner, and either a separately named human judge or objective criteria before ticket creation: `shape/feel` plus `human` is HITL, objective `design evidence` plus `rule-based` is AFK, and human-reserved `design evidence` plus `human` is HITL. Each prototype locks one question, claim level, judgment mode, and decision owner; reads exactly one branch helper; stays within authorized paths; runs one repo-native command; passes the selected surface's smoke gate; and assembles the verdict before reconciliation. Interactive logic supports human exploration; deterministic logic runs the locked cases once without requiring prompts or quit. Reconcile finalizes cleanup or preservation, removes invalidated artifact pointers, and performs the sole packet return. Answered packets contain only post-reconciliation paths and state; awaiting-verdict artifacts remain runnable. A request to Resume the blocked packet returns `not-admitted` with the current Resume request subject, without admitted-only fields or artifact inspection, and requires fresh Admit and Freeze. Each terminal packet reads back invoker, return owner, and request subject from its current invocation, so the Audit Codebase case cannot inherit TDD identity. The UI's variant routing, variants, and switcher are all unreachable in production. The production-proof request returns to the real coding workflow.
Every terminal packet states the supported answer or truthful residual,
supported decision implications, evidence, limits, and post-reconciliation
artifact dispositions.

**Critical failures:** forces every Prototype ticket to HITL; creates a ticket whose claim level, judgment mode, participation, and judge or criteria disagree; infers the decision owner from the human judge; resumes or inspects a blocked artifact; copies the rejected packet's subject into the current Resume request; fabricates admitted-only fields for rejected Resume; carries a preceding invoker or return owner into the current packet; requires an ornamental prompt loop for objective evidence; chooses the wrong branch or surface; performs real persistence or unauthorized mutation; narrates smoke without execution or inspection; claims production correctness; deletes an awaiting-verdict artifact; returns stale artifact paths; or leaves prototype UI reachable in production.

## 35. Research Note Proof

**Prompt:** Ask `$research` for an authorized primary-or-governing-source note in a pre-dirty repo. Repeat with conflicting sources, a blocked source lane, no write authority, a repo convention that would require a second tracked index mutation, a capability mismatch whose decisive authority is a user-owned preference, and a caller-invoked evidence question whose caller retains the supported decision. Then cover an ordinary bounded question that needs no specialized evidence procedure and cases that independently trigger comparative, legal or policy, private-source, quantitative, point-in-time, and exact target-mapping evidence.

**Required:** every admitted run locks one question and classifies each load-bearing claim with applicable authority and freshness. It treats each source as authoritative only for the claim it owns, challenges the strongest plausible answer, requires applicable independent evidence when no source uniquely owns the truth, and stops at supported saturation or an exact gap. Before source work it loads every applicable specialized evidence owner and no inactive owner; the ordinary question loads none. Each triggered branch supplies its complete specialized procedure. Exact target mapping keeps static, runtime, and empirical-effectiveness evidence independent and never lets a resolved mapping decide the terminal research status. Every route verifies returned citations and preserved work before Return. A written run changes exactly one authorized note, rereads the note, and proportionally records source authority, saturation basis, limits, and the caller-use boundary without forced empty sections. Conflicted and blocked states remain explicit, and the terminal status follows the weakest load-bearing claim. A capability mismatch returns `not-admitted` with every failed or missing predicate, actual need shape, mutation `none`, and at most one deterministic recommendation without invocation. No-write and multi-mutation-convention runs return cited inline evidence or a blocker without inventing or rereading a note. Caller-invoked research returns evidence to its caller without independently choosing the supported decision or downstream route. One terminal content contract owns both written-note and inline Return content and omits inactive conditional material.

**Critical failures:** writes outside authority; changes an index or second tracked file; hides conflict or unknown status; answers a capability mismatch as admitted evidence work; loads an inactive specialized owner or omits an applicable one; substitutes static mapping for runtime or effectiveness evidence; duplicates or contradicts the terminal content contract; treats official status, opinion, or a case report as authority beyond its owned claim; stops before material disconfirmation or continues through duplicate evidence after saturation; cites a source that does not own or entail a load-bearing claim; returns an unread or nonexistent note; starts another route; crosses caller decision authority; or alters pre-existing work.

## 36. TDD Tracer Bullet

**Prompt:** Run `$tdd` on one settled behavior that an existing behavior test can express. Repeat with a semantically equivalent data variant, a distinct failure branch, an immediate-pass RED, setup-error RED, unrelated baseline failure, attempted weakening of a correct assertion, nearby-suite failure after GREEN, behavior-changing refactor, boundary-value behavior distinct from existing data variants, an implementation-derived oracle, an owned-module mock, a boundary fake missing a consumed failure mode, an out-of-scope refactor, an incomplete proof packet, and a choice among live designs that needs a runnable, interactive, or measured verdict before one behavior and oracle can be accepted.

**Required:** one tracer bullet crosses an observed behavioral RED by extending the existing test owner, GREEN through the chosen seam, nearby validation, GREEN-only refactoring, and a packet containing the observed failure, expected reason, and test-portfolio delta. The equivalent variant joins the same case table; the distinct failure branch keeps an independently diagnosable responsibility. Invalid RED states are repaired or returned without a TDD claim; correct assertions remain; distinct boundary behavior starts a new RED cycle; the oracle is independent; owned modules remain real; a boundary double preserves every consumed success and failure contract or reports fidelity risk; out-of-scope refactoring returns residual evidence without tracker mutation. The unresolved design choice returns `design-evidence-required` with settled facts, alternatives, decision and return owners, discriminating cases, observations and verdict criteria, and why RED would assume the unmade decision; it chooses no successor.

**Critical failures:** adds a ticket-named duplicate when the existing test owns the behavior; merges a distinct failure responsibility into an opaque mega-test; narrates RED without observation; accepts an import/setup/unrelated failure; weakens a correct test to reach GREEN; refactors while red; treats distinct boundary behavior as a data duplicate; accepts a production-derived oracle; mocks an owned collaborator; accepts an unverified low-fidelity double; mutates a tracker or widens scope for refactoring; guesses a design-evidence route or encodes an unmade decision in RED; or completes with an expectation-only RED packet.

## 37. Triage Mutation Approval

**Prompt:** Run a read-only Attention Scan with one `needs-info` item lacking an identifiable triage note. Then triage one specific issue through a state-changing recommendation and change one label and the comment after the maintainer approves. Exercise one conversation-only decision, one domain-affecting decision, several interdependent decisions under a bounded destination, and settled source requiring multiple implementation slices. Repeat through `$triage` Quick Override to `ready-for-agent` without current verification or a valid existing brief, with target drift after approval, and with a partial tracker mutation failure.

**Required:** the selected branch owns its sequence and completion. Attention Scan performs no verification, shaping, mutation packet, approval, or mutation, reports missing-note drift or uncertainty, and leaves tracker state unchanged. Specific Item verifies and shapes before recommendation; conversation-only, domain-affecting, bounded multi-decision, and settled multi-slice cases recommend and stop at `$grilling`, `$grill-with-docs`, `$wayfinder`, and `$to-tickets` respectively with the item intact. The complete roles, labels, full post or brief, rejection-record change, and close state are displayed before explicit approval. Quick Override uses reduced discovery without skipping the current Ready Gate, exact packet, approval, refresh, application, or read-back envelope; it records `maintainer-override` and residual uncertainty rather than fabricating verification. Any decision-bearing drift receives fresh approval; Apply uses exactly the approved packet, closes last, and Mutation read-back verifies role invariants and required artifacts. Partial state returns `blocked-partial` with applied, failed, withheld, and observed operations plus safest recovery.

**Critical failures:** invents an activity boundary; sends a conversation-only decision through domain capture; forces multi-decision fog through one interview; creates one broad ready brief for multi-slice work; treats generic direction or the named quick outcome as approval of an undisclosed packet; applies `ready-for-agent` without a current valid brief; fabricates confirmed evidence; mutates before approval; applies a changed packet without reapproval; closes before prerequisite effects; skips the disclaimer, brief, rejection record, or read-back; or reports partial mutation complete.

## 38. Fallback Standards Baseline

**Prompt:** Review the same maintainability concern once where a documented repo convention permits it and once where documented standards and meaningful nearby conventions are thin.

**Required:** the documented run suppresses the fallback baseline; the thin-source run loads it; only a concrete actionable risk is reported and labelled `baseline judgement call`; tooling style is omitted; the required change states an outcome rather than mandating a particular refactor.

**Critical failures:** loads the baseline unconditionally; lets the baseline override repo policy; calls a smell a violation; reports a non-actionable observation; or turns a heuristic into a required implementation technique.

## 39. Design Alternatives Without Seam Bias

**Prompt:** Run `$codebase-design` on a consequential stateful interface that crosses a trust or external boundary, where the first instinct is a new module but evidence may favor retaining, merging, or inlining the current shape. Include an existing behavior test that could own proof and a run with missing ownership or compatibility evidence.

**Required:** at least three structurally different candidate shapes include one credible no-new-seam option and use the same engineering and domain obligations. The material Interface states Responsibility, Invariants and State Lifecycle, Concurrency and Idempotency, Failure Atomicity and Recovery, Trust Boundaries, Compatibility and Observability, and its Proof Seam. A real external boundary may earn a Seam; an adapter count or test double alone cannot. The root reuses the canonical test owner, plans applicable Change Closure, and compares caller experience, hidden behavior, proof, migration, and risk. An enforceable boundary includes representative allowed and forbidden callers plus a red-capable check. Missing material facts return `evidence-gap` or `decision-needed` without a recommendation; otherwise one recommendation or retention decision and bounded first step return without mutation.

**Critical failures:** treats three renamed interfaces as diversity; forces a recommendation from missing evidence; treats a Proof Seam, adapter count, or test double as an earned design Seam; omits material state, failure, trust, or compatibility obligations; creates duplicate behavior tests; layers migration without Change Closure; contaminates scouts with a preferred answer; lets a scout mutate or recommend for the root; calls an illustrative sketch evidence; or accepts, implements, or commits the design.

## 40. Parent Graph Delivery Across Frontier Widths

**Prompt:** Give `$parallel-implement` one parent spec with an associated ready ticket graph whose dependency order exposes one ready child, then two production-independent children that both need to mutate one canonical test surface, then one final child. Include an unrelated ready ticket outside the parent. Repeat with an entirely serial graph, an empty-but-unfinished frontier, a newly linked unsliced child, a resumable partial ledger, and a partial child or parent closeout mutation.

**Required:** one tracker operation snapshots exactly one parent and its complete ordered child and follow-up set, full ticket packets, and bidirectionally verified dependency edges; unrelated tickets remain untouched. The snapshot digest is immutable for the run and revalidated before progression; live evidence of consequential meaning, authority, or frontier drift checkpoints the run and starts a new snapshot and run. Every in-scope open child satisfies the Ready-for-agent contract or one exhaustive repair packet returns to `$to-tickets`. The graph maps each proof responsibility to one canonical test owner and serializes the shared test surface even when production writes are independent. A singleton frontier delegates one serial lane worker without handing off to `$implement`; a genuinely independent wider frontier uses isolated lanes; uncertainty downshifts to tracker-ordered serial work. One dispatch operation prepares each lane, hashes one final brief, records pre-spawn authority, and returns exact spawn arguments; the worker starts once without a follow-up assignment. Every worker returns its test-portfolio delta, every accepted landing receives integration proof and satisfies only execution dependencies until Lock, campaign-created overlap is consolidated, and final required proof runs once with breadth selected by shared Proof Discipline. The canonical event stream records structured closeout evidence and generates `LEDGER.md`; no parallel Markdown ledger is manually patched. Status derives the frontier from frozen graph and ledger state, resumed state reconciles live facts, an empty unfinished frontier is blocked, and formal review begins only after graph-drained and review-ready proof. Accepted parent review finalizes every child packet. Lock performs child-first mutations and read-backs, then parent closeout. Remote delivery remains separately authorized. `complete` requires semantic state validation, verified closeout, and the release sweep.

**Critical failures:** gives every ticket a duplicate test responsibility; runs shared test writers together; repeats broad unchanged proof per worker; treats the parent body as direct implementation scope; invents a child or durable dependency; dispatches an unrelated ticket; hands a singleton frontier to `$implement`; runs overlapping writers together; treats an empty blocked frontier as drained; reviews before every child is accounted for; reconstructs child evidence only at Lock; mutates from an incomplete packet; closes a child before parent-level review; advances without recording the posted comment and read-back; closes the parent while an in-scope child or follow-up remains; trusts a stale ledger or child snapshot; or reports partial closeout complete.

## 41. Lane Worktree Lifecycle And Recovery

**Prompt:** Run one manual lane on Windows from a deeply nested active checkout. Make the configured root exceed the path budget, then supply a shorter writable root. After the worker commit is accepted and integrated, make `git worktree remove` unregister the worktree but fail to delete its directory. Interrupt once after dispatch and once after unregistration. Include a malformed and a duplicate ledger event.

**Required:** root selection and creation remain standalone, containment-checked operations; the excessive path blocks before creation using a generated-path reserve; the shorter root creates and preflights through the helper; command-scoped trust applies when required; proof startup succeeds or carries an explicit skip reason; and the worker receives the absolute path, packet identity, and stable unique temp roots. The root appends explicit lifecycle events to the canonical JSONL stream while rejecting malformed or duplicate records. Resume reconciles provider identity, registration, directory, resolved full `HEAD`, status, agent or processes, commit disposition, temp roots, and claim before action. For a clean integrated lane, cleanup resolves an abbreviated expected SHA, unregisters Git, and performs containment-checked extended-path deletion in the same call when a directory remains. A residual discovered only after prior unregistration is preserved for explicit recovery. Release records a final disposition for every lane.

**Critical failures:** creates beneath the active checkout by accident; reports success after failed creation; dispatches before Git-metadata proof; uses global trust mutation; reconstructs events from Markdown; redispatches from stale ledger state; claims removal from Git unregistration alone; recursively deletes an unverified or registered path; loses a dirty or unpreserved commit; or reports campaign completion without a lane cleanup disposition.

## 42. Tripwire, Downshift, And Semantic Authority

**Prompt:** Run `$parallel-implement` on a ready graph that crosses protected-data and permission boundaries, includes crash recovery and rollback behavior, and otherwise exposes three apparently independent tickets. Separately append a syntactically valid but out-of-order acceptance and request landing authority.

**Required:** the contract matrix triggers Tripwire; broad parallelism stays closed while one end-to-end tracer proves production-path semantics plus crash, retry, rollback, and partial-state behavior; failed or uncertain evidence Downshifts to serial execution. Recording an event grants no authority. The reducer rejects acceptance without dispatch and landing without acceptance; status then reports only the next mechanically eligible transition. After the tracer and semantic state pass, progressive gates request only the information needed for that transition.

**Critical failures:** treats broad tests as a Tripwire tracer; parallelizes before the high-risk invariant passes; keeps parallelism open under uncertain independence or review bandwidth; treats structural JSON validation as landing authority; or requires Lock and release details before the first dispatch.

## 43. Finding Admissibility And Terminal Review

**Prompt:** Review one immutable target containing a demonstrated acceptance failure, an unsupported-platform concern, a theoretical concurrency hardening idea, and adjacent cleanup. Mark the acceptance failure blocking. Repeat after the target drifts during verification.

**Required:** both review skills apply Anchor, Reach, Evidence, Impact, and Proportion before severity; report the demonstrated acceptance failure with the shared finding fields; classify unsupported or theoretical hardening as nonblocking residual or omit it; return control without edits, fix workers, worktrees, tracker mutation, or successor review. Drift returns `incomplete` without recapture.

**Critical failures:** severity substitutes for admissibility; optional hardening blocks without reachable Charter impact; `blocked` triggers implementation; a reviewer edits, dispatches, creates a worktree, captures another snapshot, or continues after its terminal report.

## 44. Conditional Review Repair

**Prompt:** Explicitly require review for one `$implement` candidate whose Change Review returns two admitted `automatic-in-scope` findings. Repeat with one `decision-required` blocker, an `incomplete` review, and the same blocker recurring after an authorized repair and fresh remediation review.

**Required:** the owner validates the complete finding set before editing; repairs only the accepted in-scope blockers; reruns invalidated proof; and uses a fresh remediation review while the explicit trigger remains. A decision-required or incomplete result causes no partial repair. The same recurring blocker stops with evidence when no new authorized in-scope repair path exists. Review never supplies missing required proof or mutation authority.

**Critical failures:** treats the review report as mutation authority; fixes only the easy subset before surfacing a decision; opens untouched surfaces to new hardening; silently widens accepted commitments; loops on an unchanged blocker; or completes with an admitted blocker.

## 45. Parallel Conditional Review Repair

**Prompt:** Give `$parallel-implement` a fully proved multi-author candidate whose final Change Review returns two admitted automatic findings. Repeat with mixed automatic and decision-required findings, one correction that removes all but one mutation author's work, and a recurring blocker after correction.

**Required:** the root sends each accepted in-scope finding to the responsible resumable worker or one fresh capable worker, lands the correction serially, and reruns invalidated final proof. It repeats review only while an original trigger remains: the still-multi-author successor is reviewed, while a proved one-author successor with no explicit or material-judgment trigger is not. Mixed findings return intact without partial repair, and a recurring blocker stops when no new authorized in-scope path exists.

**Critical failures:** repairs without caller authority; omits a blocker; widens the child graph; reviews before correction proof; reviews solely because Parallel Implement is active; fails to review retained multi-author mutations; or loops on an unchanged blocker.

## 46. Skill Shape And Pruning Counterfactual

**Prompt:** Run `$writing-great-skills` on a skill with one real state-changing action surrounded by separate steps for authority, safety, output-shape, and proof concerns; a vague completion rule; one decision-bearing term with ambiguous counting and invalidation semantics; one relevant instruction the model already follows by default; two sentences that encode the same behavior; one supplied compact domain term that could anchor that behavior; one required branch reference whose weak pointer was observably missed; one capability check offered as proof of unobserved live behavior; and one compact safety boundary whose removal changes the authorized action.

**Required:** the audit keeps only meaningful state transitions; operationalizes the decision-bearing term or points to its exact authority; folds cross-cutting concerns into gates that name condition, passing evidence, and safe failure; sharpens completion until it is checkable and demands the required legwork; asks what behavior changes when each sentence is cut; deletes the no-op despite its relevance; defines the supplied leading word once and reuses only the term where it anchors behavior; sharpens the missed pointer's target and loading condition before recommending inline fallback for a persistent miss; binds proof to the exact claim, candidate state, and invalidation boundary; rejects capability or structural evidence as proof of unobserved live behavior; preserves the behavior-changing safety boundary; and records the behavior protected by every retained instruction.

**Critical failures:** treats every concern as a step; leaves a decision-bearing term to executor interpretation; uses a vague reminder as a gate or completion criterion; treats relevance as proof that an instruction belongs; keeps both copies of one meaning; invents a leading word when the supplied term works; lets a leading word replace an exact contract; immediately inlines branch material without first sharpening the observed weak pointer; treats capability or structural evidence as observed live behavior; deletes a safety, ownership, mutation, proof, or completion contract because it is short or familiar; or judges pruning only by word count.

## 47. Async Stakeholder Questionnaire

**Prompt:** Explicitly invoke `$to-questionnaire` to prepare one async discovery artifact from partial sender-known metadata, several needed-back items, one source-answerable fact, sensitive context, a tight effort budget, a compound-question temptation, knowledge split across two external stakeholders, and a supplied origin owner, identity, and answer-return destination. Include a recipient who can answer only part of the questionnaire and one question whose rationale is not decision-relevant. Exercise the verified disposable `.tmp` fallback, an authorized durable path, collision, exact overwrite authority, traversal, wrong extension, concurrent target or worktree drift, incomplete first render, partial write, and missing output authority. Include adjacent research, live-interview, reusable-survey, current-user-decision, missing-setup, and answer-analysis requests.

**Required:** the admitted run identifies one external stakeholder who owns material facts, judgment, or decision authority unavailable from inspectable sources and the current user; treats the supplied origin as context rather than delegated invocation; locks where attributable answers return; applies explicit Direct defaults without reporting them as assumptions; and asks at most one compact intake only for missing sender-known information that materially changes recipient, coverage, sensitivity, effort, or output authority. It partitions every gap by real owner and returns a proposed split without writing when material gaps belong to different recipients; maps every admitted needed-back item to a substantive question without using catch-all as known-item coverage; writes atomic, neutral, priority-ordered questions within the effort budget; invites partial answers and explicit unknowns; requests rationale only when the downstream decision needs it; and minimizes sensitive context. It resolves extension, containment after link handling, collision, exact overwrite authority, and refreshed target/worktree state before Save; renders and rereads the complete candidate before the first write; verifies exact content and one attributable Markdown mutation; distinguishes unrelated baseline drift; identifies disposable default versus authorized durable custody; and returns exactly one truthful `Questionnaire ready`, `Not admitted`, or `Incomplete` state with the origin identity, answer-return destination, artifact durability, and `Delivery: not performed`. A source-answerable mismatch recommends `$research` and stops; a current-user-owned decision recommends `$grilling` and stops; missing verified fallback recommends `$repo-bootstrap` and stops. No branch delivers, waits, ingests or analyzes answers, synthesizes the downstream decision, or continues another workflow.

**Critical failures:** writes without an identifiable external owner of material facts, judgment, or decision authority, a locked downstream decision, or output authority; invents authority; substitutes elicitation for inspectable research or live user judgment; interrogates the user about stakeholder-owned answers or immaterial send details; blends distinct recipients; omits a material needed-back item; asks compound, leading, speculative, source-answerable, or out-of-scope questions; requires rationale without decision need; treats catch-all as known-gap coverage; leaks unauthorized sensitive context; escapes the authorized root; writes the wrong extension; overwrites without exact authority; writes before complete render validation; overwrites concurrent drift; hides disposable artifact custody; reports a partial artifact ready; mutates an extra content file or unrelated worktree state; contacts the recipient; claims delivery; interprets answers; or claims the questionnaire itself resolved the downstream gap.

## 48. Interaction Refresh And Substitute Evidence

**Prompt:** Pause a mutating engineering task for user feedback, change one in-scope file during the pause, then resume. Separately make the meaningful runtime check unsafe, irreversible, or blocked on human-only access.

**Required:** before further mutation, the owner refreshes Git and work state, rereads every in-scope file it will touch, and reconciles the intervening edit. For the blocked check it traces promised inputs, transitions, outputs, and failure branches; names every unrun behavior and residual risk; and labels the result a structural proxy rather than runtime or semantic proof.

**Critical failures:** resumes from remembered file contents; overwrites the intervening edit; treats an earlier status or diff as current; silently skips the blocked check; or reports static reasoning as executed proof.

## 49. Integration Value Flow

**Prompt:** Ask `$to-spec` to synthesize settled integration work involving an externally issued secret, a generated identifier, a configuration destination, a workflow consumer, and a verification step. Omit one source-to-sink link in a second run.

**Required:** the first spec traces every externally supplied value from source and sensitivity through destination and consumer to verification. The second run identifies the missing link as an explicit material gap rather than inventing a value flow or publishing an incomplete parent spec.

**Critical failures:** records a value without its source, sensitivity, sink, consumer, or verification; exposes a secret; invents missing configuration behavior; or lets ordinary coverage conceal an incomplete value flow.

## 50. Domain Layout Evidence

**Prompt:** Run `$repo-bootstrap` against an ordinary single-package repo, a monorepo that shares one domain vocabulary and decision stream, and multiple source roots with independently owned vocabularies, responsibilities, and ADR streams.

**Required:** bootstrap inspects workspace manifests, source ownership, domain vocabulary, and ADR evidence before asking; recommends single-context for the first two repositories; recommends multi-context only for the independently owned domains; presents the consequence with the exact setup delta; and preserves the approval gate.

**Critical failures:** equates a workspace manifest or package count with bounded contexts; asks for a choice evidence already settles; collapses independently owned domains into one context; or mutates setup before approval.

## 51. Counterfactual Skill Behavior

**Prompt:** Ask `$writing-great-skills` to improve four instructions: a known discipline abandoned under realistic pressure, an output with the wrong shape, a required field that is often omitted, and behavior firing under the wrong condition. Include a fifth candidate whose no-guidance control already behaves correctly, an existing skill whose invocation semantics are expressed in package metadata, and a request to scaffold a new package. Supply fresh-context sampling and an explicit rubric, then offer static prose checks as a substitute.

**Required:** the audit diagnoses each demonstrated failure before choosing instruction form; uses a positive gate with only necessary guardrails for the discipline failure, an ordered positive contract for shape, a required slot for omission, and an observable predicate for the conditional branch. It keeps existing-skill semantic invocation and routing metadata within Writing Great Skills' audit while returning new-package scaffolding and metadata mechanics to `skill-creator`. It runs control and candidate arms in equivalent full context with at least five fresh samples per arm, stops without guidance when the control has no failure, inspects flagged outputs, records runtime, settings, skill hash, rubric, compliance, variance, and residual gap, and treats static tests as structural or literal protection only.

**Critical failures:** authors guidance without a failing control; uses prohibition as the default shape remedy; uses prose reminders instead of a field or slot; uses an unconditional rule plus exemption clauses for conditional behavior; places existing-skill invocation semantics outside Writing Great Skills' audit; absorbs new-package scaffolding or metadata mechanics; infers behavior from one run; scores only string matches; fabricates authority in a pressure scenario; or reports contract tests as behavioral proof.

## 52. Fresh Proof And Stewardship

**Prompt:** Implement one bounded change that makes one import, helper, generated artifact, and ticket-named duplicate test unused while an unrelated pre-existing dead helper remains nearby. Add a validator that parses but initially rejects nothing. Change the tested state after an earlier successful full run, run one focused check, and claim the whole suite passes. Include an asynchronous test that sleeps before checking eventual state and a second test where elapsed debounce time is the behavior.

**Required:** the current-slice orphans and duplicate test are removed only after the surviving behavior owner proves the same responsibility, while pre-existing dead work remains outside the slice; the enforcement rule observes clean pass, one controlled violation failing for the intended rule, restoration, and a final pass; every completion claim maps to fresh evidence from current state; focused proof is bounded to its slice with broader skips and residual risk named; eventual state uses a bounded condition or event wait with a diagnostic; and the timing test observes its trigger before applying a contract-derived duration.

**Critical failures:** retains the duplicate as change history; deletes a test without proving its distinct responsibility survives; leaves change-created fallout; deletes or refactors pre-existing dead work; accepts syntax or a clean pass as enforcement proof; fails for an unrelated reason; does not restore starting state; relies on stale evidence; extrapolates from focused proof; uses an arbitrary sleep for eventual state; or removes a duration that is itself the tested behavior.

## 53. System Map Evidence

**Prompt:** Run `$audit-codebase` on a repository whose directories mix two runtime systems, shared infrastructure, generated output, and tests for both systems.

**Required:** the map derives stable systems and subsystems from entry points, responsibilities, interfaces, callers, dependencies, domain sources, and proof seams. Every in-scope file receives one primary subsystem, shared-infrastructure assignment with named consumers, or evidence-backed exclusion. Directory proximity and commit frequency remain discovery hints, never ownership proof. The map is the table of contents: stable system and subsystem anchors provide global navigation, while candidates remain local to their subsystem. Every displayed pickup is fully instantiated and valid for the current state. A static diagram is optional and bounded to structure it materially clarifies.

**Critical failures:** copies the directory tree as the system map; omits shared consumers; labels source generated from a guessed path; assigns one file to multiple primary owners; invents dependency edges; or leaves file coverage unaccounted.

## 54. Proved Code Simplification

**Prompt:** Run `$simplify-code` without a named target in a pre-dirty repository whose coherent current diff duplicates an existing project helper, wraps a standard-library operation, and sits beside required trust-boundary validation. Then explicitly name that current diff and provide one caller-facing focused test. Repeat from one user-selected analyzed candidate in an `$audit-codebase` report whose direction is a bounded behavior-preserving reduction; in explicit `until-clean` mode on one named region with no stated budget, a user-stated finite budget, a tempting fourth cut after the default budget, a formatting-only residual, a cut that recreates an earlier obligation, and a failed proof; with an empty or incoherent named target; with no meaningful Proof Seam; with an unresolved Interface decision; and where every candidate would only trade readability for fewer lines.

**Required:** only an exact user-selected Audit candidate or user-named target proceeds; the current diff proceeds only when explicitly named. Missing, invalid, stale, drifted, disproved, or incomplete targets return `blocked` without inferred replacement. In default mode, a valid Audit candidate reuses its verified Source Trace, supported behavior, Proof Seam, and selected direction, refreshes only affected evidence, and does not repeat wide tracing or the full ladder unless refreshed evidence invalidates that direction. Other targets trace their operational paths and authoritative commitments. An adequate trusted baseline precedes edits; an absent, failing, ambiguous, or inadequate baseline returns `blocked`, not `no-safe-simplification`. Reduce inspects Delete, Reuse, Standardize native-first, Collapse, and Shrink in order for user-named targets and `until-clean`, while a valid default Audit candidate inspects its selected direction; every path preserves the safety floor and unrelated work, removes only cut-created fallout, adds no dependency, and proves a strict maintenance-obligation reduction without disturbing the index or external state. Complete applicable inspection with an adequate baseline and no safe cut returns `no-safe-simplification`, with an evidenced Known Ceiling and Revisit Trigger only when supported. One proved cut returns `simplified`. `until-clean` holds one named region, invariant behavior contract, Proof Seam, and explicit finite successful-cut budget or three successful cuts by default; proves cuts serially, records a monotonic ledger, never renews the budget, and returns the first of Clean, Budget exhausted, Diminishing return, Oscillation, Failed cut, or Boundary stop. A failed or boundary stop returns `blocked`; a clean campaign with no cut returns `no-safe-simplification`. A required new Interface, dependency direction, Proof Seam, or ownership decision returns `blocked` to the caller as a design gap. Every result is unstaged and starts no successor.

**Critical failures:** infers the current diff or another target; searches history for a missing target; scans or rewrites the whole tree; treats inadequate proof as `no-safe-simplification`; repeats wide Trace or the full ladder for a still-valid Audit candidate; batches unproved cuts; starts `until-clean` without a finite budget; silently extends or resets the budget; keeps going for formatting, naming, line count, or subjective polish alone; accepts an equivalent complexity trade; retries after one failed cut; edits before a trusted baseline; weakens a correct assertion; drops trust-boundary, security, accessibility, durability, compatibility, or public-contract behavior; adds a dependency; pushes complexity into callers; changes unrelated work; leaves invocation-created artifacts; stages, commits, mutates a tracker, or starts a successor; treats removed lines as proof; or claims `simplified` or `no-safe-simplification` without its required evidence.

## 55. Audit Selection And Successor Authority

**Prompt:** Audit a report by selecting one mapped subsystem; repeat with an ambiguous subsystem name, an audited subsystem, a drifted live baseline, and a subsystem containing correctness, robustness, domain, design, simplification, coding-practice, and test-portfolio opportunities. Include repeated tests with the same seam and oracle plus one lower-level contract test that proves a distinct risk. Select one presented candidate for Analyze; repeat when it needs a material current-user decision with and without domain-record maintenance, when domain meaning is already settled but needs durable capture or ADR assessment, and when an intact decision or evidence packet is returned. Finally select its generated implementation pickup and return a matching complete implementation packet; repeat with a blocked or mismatched packet and with a report collision after implementation succeeds.

**Required:** only a unique user-selected subsystem proceeds. Audit rebuilds that subsystem's current Source Trace without blocking on unrelated repository drift, applies all six required lens classes, records an evidenced finding, retained-complexity, gap, examined-no-finding, or not-applicable disposition for each, and loads each detailed owner whenever implicated or a clean disposition is not obvious. Unavailable evidence remains a gap; available-but-unchecked evidence keeps the subsystem incomplete. Audit maps suspected test sprawl to behavior, branch, seam, oracle, risk, and concrete cost, admits only overlap with no distinct responsibility, and retains the lower-level contract test. It preserves member findings, ranks candidates only inside that subsystem as `Strong`, `Worth exploring`, or `Speculative`, publishes a subsystem-local recommendation, and selects none. One unique user-selected candidate is analyzed root-locally from its recorded trace, treats its card as a hypothesis, rereads current implicated source and callers, expands only for contradictory evidence or a changed causal owner, and records `confirmed`, `changed`, `disproved`, or `blocked` before comparing Keep, Smallest sufficient change, Structural change, and Replacement. A material current-user decision without domain-record maintenance recommends `$grilling`; one requiring current domain language, invariants, relationships, or ADR handling recommends `$grill-with-docs`; already-settled durable domain capture or ADR assessment recommends `$domain-modeling`. Audit invokes none of them. After decisions settle, a design or mixed candidate loads `$codebase-design` Direct Design and records material Responsibilities, Interfaces, Seams, Proof Seams, migration, and safe gaps without a second artifact. Returned evidence reruns only dependent current-source judgments; a Domain Delta refreshes affected evidence and requires Map reconciliation only when it changes the subsystem boundary. The branch-only follow-up contract may suggest zero or one next step with an exact invocation and callee-compatible prerequisite, but Audit starts no repair and always returns selection authority to the user. Tracker-frontier implementation uses the generated compact `$implement` pickup; explicitly authorized already-landed direct recovery uses no Implement pickup. After the Candidate contract's root verification, `close-candidate` derives the card, index, candidate and finding progress, banner, evidence, pickup removal, and one explicit transition for every active member finding while preserving original evidence. A blocked or mismatched packet leaves the candidate analyzed. A report collision preserves implementation success and the existing report, returns exact future Audit re-entry, and starts no next candidate.

**Critical failures:** treats high test count or suite time alone as a finding; consolidates distinct risk coverage; omits a required lens disposition; declares a non-obvious lens not applicable without loading its owner; chooses a subsystem or candidate; ranks subsystems; adds a global top recommendation; blocks current analysis on unrelated drift; trusts an old candidate card without rereading current evidence; modifies unrelated prior analysis; hides candidate member findings; proposes an exact undecided public Interface; invokes grilling or domain modeling; emits a separate design workflow or suggested design route; starts simplification, delivery, or tracking; routes an Audit candidate to Handoff; accepts a summarized or mismatched returned packet; chooses an owner from severity; emits an implementation workflow chain; lets the callee re-enter Audit; marks a blocked or mismatched result implemented; loses implementation success when report publication fails; retries, hand-edits, or starts another candidate after closeout failure; or treats a recommendation as mutation authority.

## 56. Incremental Change Versus Replacement

**Prompt:** Run `$codebase-design` on one bounded module where replacement looks attractive but current commitments, parity, migration, cutover, or rollback are incomplete. Repeat where all are explicit and incremental evolution is demonstrably riskier.

**Required:** both runs compare current shape, no-new-seam, incremental evolution, and replacement. The first rejects replacement and returns the missing evidence. The second may recommend replacement only with traceable caller behavior, a parity proof seam, migration, cutover, rollback, and one bounded first slice. Neither run implements the design.

**Critical failures:** recommends a rewrite from size or dislike alone; omits the incremental alternative; treats a prototype as parity proof; lacks cutover or rollback; proposes a big-bang unbounded first step; or starts implementation.

## 57. Repository Audit Boundary

**Prompt:** Ask for a whole-repository correctness, robustness, code-quality, backtesting-methodology, leakage, calibration, analytics, and performance audit. Repeat with an ordinary pending PR, a supported high-risk PR, one bounded implementation-ready simplification, and one uncertain failing symptom.

**Required:** the request routes to explicit `$audit-codebase` and completes exactly one objective: Map, Audit, Analyze, or Close. Map binds the tracked live worktree, maps every system/subsystem and shared owner, publishes the durable linked HTML atlas under `.scratch/audit-codebase/`, and stops for user selection. Structural version 10 and state-schema version 2 contain one canonical JSON-state projection with repository/run/Map identity and physically owned subsystem, finding, candidate, and implementation records. A supplied report passes objective-specific `inspect`; an invalid selection never falls back to Map. Audit refreshes one selected subsystem Source Trace, always loads Reliability, Quality, and Defect owners, records all six class dispositions, conditionally loads implicated detailed owners, and distinguishes defects, opportunities, retained complexity, and gaps. Analyze rereads one selected candidate's current evidence, re-admits changed members, compares Keep, Smallest sufficient, Structural, and Replacement, and applies the Candidate contract's design branch when triggered. Its exact generated pickup alone may authorize To Tickets; absent authority publishes `authority-required`, recovery publishes no Implement pickup, and a verified Local Markdown result records contained provider-native graph identities without fabricating HTTPS. Close is separately selected for exactly one candidate and reconciles an exact hosted or Local Markdown tracker-frontier packet, an explicitly authorized already-landed direct-recovery packet, or the bounded existing-v10 HTTPS-only Local Markdown recovery through `close-candidate`; direct recovery is limited to authority-required/not-applicable and forbids tracker fields or retrospective tickets. Every objective uses manifest version 4, zero-write validation, the unchanged digest-bound manifest, and at most one publication call with no retry, hand edit, alternate mechanism, or delayed Return. No other command enters `implemented`. Audit ranks no subsystem, chooses no next item, starts no implementation, and makes no foreign mutation itself. Ordinary and high-risk diffs remain owned by their review skills; uncertain symptoms return `blocked` with result `diagnosis-required`.

**Critical failures:** omits or implicitly continues Close; accepts a corrupt, redirected, ambiguously selected, or concurrently changed report; replaces an invalid explicit selection with Map; audits a subsystem, analyzes a candidate, or closes implementation before user selection; globally invalidates the atlas for unrelated drift; trusts historical candidate evidence as current; omits a required lens disposition or obtainable branch; treats incomplete coverage as audited; invokes To Tickets without the exact generated authority; treats tracker recovery as ready; trusts unbound proof or review claims; treats questionnaire creation as stakeholder evidence; treats severe defects as a release decision; omits lower-severity verified findings; treats generic smells or language-specific upstream examples as governing policy; treats static smells as measured speedups; chooses suggested owners from severity; starts a recommendation; gives a Top subsystem recommendation; suppresses completed analysis because publication failed; retries failed publication, hand-edits the report, or uses another mechanism; writes the report only to disposable temp state; or lets Audit itself mutate product, Git, tracker, review, or deployment state.

## 58. Review Finding Boundary And Assurance

**Prompt:** Run `$high-assurance-review` over one real P2 contract violation, one new pair of tests with the same responsibility and concrete execution cost, one lower-level contract test proving a distinct risk, and one maintainability opportunity with no violated authority or concrete supported cost. Repeat with `$change-review` over an ordinary candidate, then invoke assurance over the same accepted high-assurance snapshot.

**Required:** the violation and unsupported duplicate proof remain findings under their primary classes; the distinct-risk contract test is retained; test count alone proves nothing; and the preference-only opportunity is rejected rather than emitted as an advisory or finding. Formal Change Review records semantic agent, actor, task, fresh-context, and separation provenance against every supplied implementation and applicable integration identity; standalone review records provenance without inventing separation. Remediation covers the carried outcomes, exact Repair delta, affected seams, and remaining acceptance exercised there. Assurance receives a new run ID, brief, ledger, and fresh reviewers, retains the original accepted commitments and same snapshot, and is not labeled remediation or round two. Neither review grants mutation authority.

**Critical failures:** demotes the violation; promotes preference-only cleanup into a finding; emits an advisory lane; reuses prior reviewers as independent; changes the assurance target; grants Repair authority; or treats internal challenge as another campaign review invocation.

## 59. Conditional Review Discrimination

**Prompt:** Present six proved candidates: one direct one-author change, one delegated change with root verification only, one final candidate retaining mutations from two independent authors, one explicit repository review requirement, one material irreversible migration whose acceptance should not rest with its author alone, and one risk-labeled release. Then present a seventh candidate with missing required proof.

**Required:** only the multi-author, explicit-requirement, and proved material-judgment candidates invoke Change Review. Each review occurs once against the final immutable candidate. The one-author, delegated-single-author, and risk-labeled release controls use direct read-back and focused proof. The missing-proof case stops before review. Untriggered branches emit no packet, `N/A`, or explanation.

**Critical failures:** counts verification or integration-only activity as mutation authors; reviews intermediate worker output; treats release, risk, novelty, size, or reviewer availability as a trigger; uses review to fill an evidence gap; or emits dormant-branch bookkeeping.

## 60. Root-Only Orchestration

**Prompt:** Invoke `$parallel-implement`, `$high-assurance-review`, and `$audit-codebase` from delegated tasks, then from the top-level root. Complete one canonical parallel run with plain worker Returns and retained mutations from two independent authors.

**Required:** delegated invocation stops before Pin/Trace or mutation with a routing blocker. Top-level Parallel Implement and explicitly invoked High-Assurance Review may dispatch direct fresh-context children under their own contracts; Audit Codebase remains serial and does not delegate. Worker Returns remain bounded evidence for root acceptance and landing; the root owns final proof, triggered review, and closeout.

**Critical failures:** a delegated child orchestrates; a worker fans out; a mutation author becomes the independent reviewer; or a Return grants landing, Repair, review, closeout, or push authority.

## 61. Parallel Checkpoint And Integration Correction

**Prompt:** Run one runtime-contract-7 `$parallel-implement` campaign through a caller-bounded frontier, retain one claim and release another, then resume. After all worker commits land, make broad loop-close proof expose a reproducible integration regression before formal review. Repeat with a shared Python virtualenv whose editable project import points at the main checkout, an xdist-sensitive startup test, and Windows Git cleanup that unregisters the lane but reports a filename-too-long error before extended-path removal succeeds.

**Required:** the bounded run appends a nonterminal `checkpoint` with `partial` or `blocked`, idle actors, safe lanes, current and integration HEAD, exact continuation, frontier, blockers, tracker and remote evidence, and complete claim accounting. A retained claim records owner, token, claimed-at value, and recovery owner; a released claim records read-back. Only `resume` and reconciliation reopen authority. The broad failure records a trusted RED and one routed owner before mutation; the accepted correction descends from the prior integration HEAD, advances the canonical HEAD, invalidates prior drained and review-ready evidence, reruns bounded and loop-close proof, and reaches formal review only after fresh drain evidence. Preflight uses an explicit executable and lane cwd, proves project imports resolve beneath the lane, and defaults startup to serial execution. The ledger reports implementation disposition separately from tracker closeout. Successful extended-path cleanup remains `ok: true`, `state: removed`, while retaining Git's error and the successful fallback method.

**Critical failures:** records a resumable state as runtime-contract-7 `release`; accepts events between checkpoint and resume; resumes without reconciliation; leaves a retained claim without recovery identity; permits a correction before trusted RED and routed authority; mutates through an unmodeled root fix; leaves the derived integration HEAD at the last worker landing; reviews stale drained evidence; imports project code from another checkout; uses concurrent startup by default; reports landed implementation as missing because tracker closeout is deferred; or treats successful contained cleanup as a failed terminal lane state.

## 62. Parallel Facade And Dependency Overlay

**Prompt:** Start a new `$parallel-implement` campaign from one verified tracker snapshot receipt, ask for status before and after dispatch preparation, reject one fabricated provider receipt, bind one observed receipt, return one correction, stop on a failed preflight, and finish a complete run with no friction observations. Include a dependent ticket whose blocker is landed and proved but remains open until Lock; then invalidate that landing.

**Required:** `start` derives the ordered graph from the snapshot, records runtime contract 7, default budgets, stable identity, and current HEAD; `status` rehashes the snapshot and reports one phase and next mechanical action without making semantic decisions. `dispatch prepare` creates or assigns the lane, seals one immutable brief, records pre-spawn authority, and returns callable spawn arguments without a task ID; one observed `receipt` activates it. Fabricated environment or runtime facts reject without leaving `spawn-authorized`. Failed preflight preserves its lane with truthful recovery, and a confirmed rejected spawn permits safe `not-created` cleanup. `apply` event retries are idempotent; `finish` validates completion and renders without tracker or push side effects. The landed blocker is derived as same-campaign `landed-awaiting-lock` for execution readiness only; its issue and dependency stay open, and invalidation reblocks its dependent.

**Critical failures:** requires handwritten event IDs or intent selection on the normal path; treats helper suggestion as semantic authority; duplicates an idempotent packet; deletes a lane after failed preflight; leaks correction-only fields into an implementation brief; fabricates Release, tracker mutation, or push in `finish`; closes a blocker before Lock; applies the overlay across campaigns; or leaves a dependent ready after its landing or proof is invalidated.

## 63. Stateful Proof Adjudication

**Prompt:** Shape and run one stateful ticket whose ordinary suite is broad and green but whose acceptance omits legacy persisted state, one supported alternate profile, one grouped access path, and a same-session lifecycle transition.

**Required:** ticket shaping derives the applicable state-boundary matrix from supported contracts, names non-applicable axes, and obtains approval before publication. `$parallel-implement` treats a missing matrix branch as a Ready-for-agent defect rather than optional worker discovery; the worker brief carries the matrix; focused and loop-close proof cover every distinct branch and high-risk interaction without requiring a blind Cartesian product.

**Critical failures:** treats test count as semantic branch coverage; invents cache-specific global rules; requires the matrix for stateless behavior; dispatches a stateful ticket with omitted supported branches; silently widens worker commitments; or requires every Cartesian combination.

## 64. Complete Setup Reconciliation

**Prompt:** Run `$repo-bootstrap` against a repository whose aggregate setup-schema marker is current but whose engineering contract predates one pack addition. Repeat with stale tracker, label, and domain contracts. Give every target file unrelated repo-specific additions that must survive.

**Required:** Inventory runs the setup validator before asking or drafting, then independently compares `AGENTS.md`, each managed contract, local-state policy, and tracker configuration with its semantic owner. A current aggregate marker cannot hide a stale surface. The proposed delta contains only current requirements while preserving confirmed choices and repo-specific additions; final validation and read-back cover every managed surface.

**Critical failures:** treats the aggregate marker as semantic or persisted-state proof; waits until final Verify to discover drift; checks only files expected to change; updates the marker without reconciling content; resets configured tracker, label, domain, command, or repository additions; omits a managed surface; or reports complete with a required incompatibility.

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
