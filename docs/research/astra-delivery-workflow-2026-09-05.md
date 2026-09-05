# Astra delivery workflow reconciliation

Date: 2026-09-05. Scope: compatibility between repo-bootstrap, to-tickets, and
parallel-implement, followed by a disposable local-tracker workflow exercise.

## Contract changes

- Bootstrap owns tracker representation and conditional parallel prerequisites:
  permitted lane placement, actual worker/runtime access, Python/Git/helper
  availability, and one canonical local-tracker checkout. No automatic lane
  creation, permissions expansion, or obsolete host configuration schema.
- To-tickets returns complete-parent versus subset scope, actual published
  identities, dependencies and unresolved gates. Agent-readiness and human-only
  handoffs are distinct; neither implies concurrency independence.
- Parallel-implement claims whole-parent coordination explicitly, distinguishes
  run/actor identity from shared accounts, and requires exclusive coordination
  rather than pretending read-back is an atomic claim.
- Completed children and parents receive mapped implemented state, lose readiness
  and this run's active claim, and close only under configured policy. Subsets
  preserve parent ownership; pauses preserve unfinished state and recovery.
- Version-controlled tracker writes belong exclusively to the integration root.
  Graph and claim commits precede dispatch; sibling claims share one clean base.
  Completion metadata cannot be written concurrently with an integration writer.
- Proof at code commit C may carry to final metadata commit H only after inspecting
  C..H and confirming the delta cannot affect behavior or proof inputs. Records
  cite C; cleanup verification receives H. This avoids a self-referential record.

The custom workflow supplied the missing parent and readiness transitions. Its
conditional bootstrap parallel-support branch was retained in host-neutral form.
Upstream review in the preceding compatibility assessment supported cohesive
ticket outcomes, real frontier dependencies, bounded live work and candidate-bound
evidence; no additional scheduler, mandatory reviewers, or publication defaults
were needed.

## Challenger review

Two fresh read-only challengers reviewed a frozen candidate. One owned tracker
transitions and claim semantics; the other owned local Git/proof integration and
environment prerequisites. Accepted their corrections:

1. Explicitly mark parent implemented while respecting providers that leave it open.
2. Agent dispatch must not consume ready-for-human work.
3. Both main finish and helper reference explicitly identify final H for cleanup.

Both reviewers rechecked the final corrections and reported no remaining findings
in their seams. Root retained final integration and verification.

## Workflow exercise

Disposable fixture and controller: `.tmp/astra-workflow-exercise/`. The nested
repository is `repo/`; helper lanes are outside that repository under `lanes/`.
The fixture uses real Git, the actual Astra lane helper, current bootstrap seeds,
local Markdown tickets, and two fresh implementing subagents. Root orchestrates
the transitions; this is a concrete integration exercise, not a blind measurement
of whether an unprompted agent selects and follows the three skills.

The accepted graph contains a serial record producer, independent JSON and CSV
consumers, and a final combined-export consumer gated on an explicit fixture
decision. Worker scopes exclude the canonical tracker and exercise controller.
The final check feeds actual produced output through both consumers and parses
their results against independent expectations, preserving leading-zero identity,
Unicode/comma/quote/newline name content, and signed integer amount.

The exercise passed using the final reconciled instructions:

- Published the graph and bootstrap guides; committed parent/prerequisite claims.
- Implemented and proved the serial producer; completed it and claimed both
  consumers together. Both lanes started at
  `551080ae46cfbe6362668669aff28778ff353729`.
- Two fresh workers returned scoped commits: JSON
  `2f2bf0aaf1d2136a625e36a882120bf522b09efe` and CSV
  `60d30857ee40b3da171730b18c68bf7e6b424a3b`. Root inspected their actual changes,
  helper eligibility, and integrated tests. Worker tests covered two JSON tests
  and a CSV test with eight name cases; root also ran the combined output check.
- Landed JSON, committed canonical completion metadata, then merged CSV while
  retaining those tracker updates and both worker commits as ancestors.
- Verified the last descendant remained unclaimed and the parent incomplete.
  It then held ready-for-human without agent dispatch. The fixture controller
  supplied the planned decision before changing it to agent-ready and implementing.
- Actual producer-to-renderer-to-parser proof passed at code commit
  `4cf337f6a8a420a58aa14e30890feb8ccd08b4f4` (C).
- Root completed all tickets and parent, cleared claims/readiness, and committed
  metadata to `05e0af086ec82fe996abb44814366dc5eae76031` (H). C..H changed only
  intended tracker records and no Python code; completion records cite C.
- Helper verification using C failed with `head_matches: false`; using H passed
  with `finish_clean: true` for the entire retained two-lane set. Final fixture
  Git status was clean and all items were implemented with no active claims.

Controller, state.json, composed proof, and fixture history remain under the
scratch location as local evidence, not installed skill resources. Test commits
exist only in that disposable nested repository, not the main source repository.

## Validation limits

The exercise does not test remote GitHub/GitLab APIs, real multi-coordinator claim
races, or host configurations beyond the available Windows workspace. It does
not prove comparative skill effectiveness. No full workflow engine or instruction-
wording tests were introduced. The 10 focused repository checks, skill validator,
25 local links, and both whitespace checks passed for the reconciled documents.
All three changed skill packages also passed their package validator. Parent
close=no on a remote tracker, competing coordinator races, subset delivery, and
new-child drift were reviewed as contract cases but not executed in this exercise.
