# UBL-01 Slicing And Migration Source Packet

Status: source-packet-complete

Supports: UBL01-C1 through UBL01-C5 and the bounded correction decision in
UBL-24

Scope: primary-source semantic research checked 2026-07-22; no repository
history, conversations, behavioral evaluation, language-reference edits,
synthesis edits, runtime edits, or local-adoption claims

## Question And Boundary

Which distinctions among tracer bullets, vertical slices, task size,
dependency readiness, and expand-contract migration are stable enough to
support the five claims admitted by UBL-00?

This packet can classify and bound source meaning. It cannot establish that a
term changes agent behavior, that a formulation transfers between harnesses,
or that this repository should adopt any resulting wording.

## Admission Header

| Field | Locked Value |
| --- | --- |
| Menu ID and claim IDs | UBL-01; UBL01-C1, UBL01-C2, UBL01-C3, UBL01-C4, UBL01-C5 |
| Decision | Decide whether the admitted reference rows should be confirmed, narrowed, split, demoted, rewritten, rejected, or left unresolved before UBL-24 |
| Boundary | Include term meaning, operational conditions, counterexamples, and migration exceptions; exclude intellectual-history reconstruction, pack intent, behavioral efficacy, transfer, and local adoption |
| Source plan | Original or canonical accounts for each facet, bounded official-practice counterpressure, and corroboration only where one source cannot decide the disposition |
| Budget | Three independent facets; at most 16 source records / 22 directly inspected pages; three read-only source scouts; zero repository-history lanes, contacts, practitioner sessions, or behavioral runs |
| Stop | Stop when every active claim has a bounded disposition, evidence repeats an existing distinction, the cap is reached, or a named gap prevents a decision |
| Output | This packet plus one evidence pointer and disposition reconciliation in `UBL-00-claim-ledger.md` |

## Facet Map

| Facet | Claims | Decision Pressure |
| --- | --- | --- |
| Learning path versus delivery shape | UBL01-C1, UBL01-C2, UBL01-C3 | Separate tracer-bullet feedback from vertical-slice value organization and determine what kind of completeness or proof each requires |
| Size, readiness, and independence | UBL01-C1, UBL01-C3, UBL01-C4 | Separate smallness from readiness, testability, precedence, and safe concurrency |
| Compatibility migration | UBL01-C5 | Separate expand-migrate-contract sequencing from product slicing and progressive-exposure blast-radius control |

## Verified Source Registry

All links below were opened directly. “Original” means an account by the
named originator or primary author; “official” means current project or vendor
documentation. Check dates are 2026-07-22 unless a publication date is shown.

| Evidence ID | Source And Locator | Authority And Access | Supports / Limits |
| --- | --- | --- | --- |
| S01 | Andrew Hunt and David Thomas, [The Art in Computer Programming](https://media.pragprog.com/articles/other-published-articles/ArtInProgramming.pdf), 2001, pp. 2-3 | Complete author-hosted article; original tracer-bullet account | A skeletally thin, observable end-to-end system creates feedback and a proven base; the example crosses several real components. It does not require customer value, final architecture, or every possible layer. |
| S02 | Pragmatic Bookshelf, [Pragmatic Programmer tips](https://pragprog.com/tips/), Tips 20 and 68 | Official concise author/publisher statements | Tracer bullets find the target; small end-to-end increments enable learning. Concise tips do not define vertical slices or proof independence. |
| S03 | Hunt and Thomas, [The Pragmatic Programmer, 20th Anniversary Edition, Topic 12 preview](https://www.oreilly.com/library/view/the-pragmatic-programmer/9780135956977/f_0030.xhtml), 2019 | Licensed publisher preview; partial access | Confirms the current topic and metaphor. The preview ends before the full operational discussion, so S01-S02 carry the detailed accessible meaning. |
| S04 | Jimmy Bogard, [Vertical Slice Architecture](https://www.jimmybogard.com/vertical-slice-architecture/), 2018 | Original architecture account; complete page | Organizes all concerns front-to-back around a request/use case and allows each slice to choose its implementation. It is an architecture/coupling account, not a universal requirement to touch every architectural layer. |
| S05 | Bill Wake, [INVEST in Good Stories, and SMART Tasks](https://xp123.com/invest-in-good-stories-and-smart-tasks/), 2003 | Original INVEST account; complete page | Separates Independent, Valuable, Small, and Testable story properties and separately time-boxes tasks. Independence is negotiable and imperfect, not a synonym for smallness or concurrency. |
| S06 | Bill Wake, [Testable Stories in the INVEST Model](https://xp123.com/testable-stories-in-the-invest-model/), 2011 | Original clarification; complete page | Testability requires agreed expected behavior or outputs; it does not require all tests upfront, automation, or a complete specification. |
| S07 | Scrum Guides, [The Scrum Guide](https://scrumguides.org/scrum-guide.html), 2020, Increment and Definition of Done | Official normative guide; complete page | An increment must be usable and verified against the Definition of Done. This is completion evidence, not a definition of tracer bullet or scheduling independence. |
| S08 | Python 3.14, [`TopologicalSorter.get_ready`](https://docs.python.org/3/library/graphlib.html#graphlib.TopologicalSorter.get_ready) | Official current library documentation | “Ready” means predecessors have been processed in this graph API. It establishes eligibility under one dependency model, not actual concurrent execution. |
| S09 | GitHub, [Issue dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies) and [workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency) | Official live documentation | Blocking/blocked-by records predecessor constraints; separate concurrency controls can serialize otherwise eligible jobs. Product-specific semantics limit transfer. |
| S10 | Apache Airflow 3.3, [Tasks](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html), [Scheduler](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/scheduler.html), and [Pools](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/pools.html) | Official current documentation | Upstream state, scheduler state, and resource pools are separate: dependency satisfaction does not itself guarantee execution or concurrency. Workflow-engine semantics are illustrative, not universal planning definitions. |
| S11 | PMI, [Difficult work assignments and task managing](https://www.pmi.org/learning/library/difficult-work-assignments-task-managing-7690) and [Resource-based project scheduling](https://www.pmi.org/learning/library/resource-based-project-scheduling-concurrent-activities-1978) | Professional operational counterpressure; complete articles | Hard dependencies constrain sequence; soft dependencies and resources can change scheduling; parallel activities may still be serialized by limited resources. These articles do not establish “frontier” as a standard term. |
| S12 | Danilo Sato, [Parallel Change](https://martinfowler.com/bliki/ParallelChange.html), 2014 | Primary practitioner account on Martin Fowler's site; complete page | Defines expand, migrate, and contract phases with old and new forms coexisting and each phase releasable. The example can be local, so “broad migration” is too restrictive. |
| S13 | GitLab, [Multi-version compatibility](https://docs.gitlab.com/development/multi_version_compatibility/), [Avoiding required stops](https://docs.gitlab.com/development/avoiding_required_stops/), and [Avoiding downtime in migrations](https://docs.gitlab.com/development/database/avoiding_downtime_in_migrations/) | Official mature operational guidance; live pages | Mixed versions and large data changes create real ordering constraints and multi-release migration stages; dependencies can require stops. Safe staging does not make each stage an independent product slice. |
| S14 | OpenStack Keystone, [Database Migrations](https://docs.openstack.org/keystone/latest/contributor/database-migrations.html), last-updated marker 2023-06-27 | Official project documentation; complete page | Separates expand and contract repositories and preserves compatibility while versions coexist. It is a project-specific implementation of the broader pattern. |
| S15 | Martin Fowler, [Branch by Abstraction](https://martinfowler.com/bliki/BranchByAbstraction.html) | Canonical practitioner counterexample; complete page | Large changes may proceed through coexistence and staged substitution while the system keeps running, even when the work is not a sequence of independent product slices. |
| S16 | Microsoft Azure Well-Architected Framework, [Safe deployment practices](https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/safe-deployments) | Official current operational guidance | Blast radius is controlled through progressive exposure, health checks, and deployment scope. It is related risk control, not part of the expand-contract definition. |

## Claim Classification And Disposition

`Supported`, `conflicted`, and `unknown` classify the source record. The final
column is the bounded roadmap disposition that UBL-24 may use; it is not an
edit authorization.

| Claim ID | Source Classification | Evidence And Counterpressure | Disposition | Behavioral Status |
| --- | --- | --- | --- | --- |
| UBL01-C1 | supported in part; combined wording conflates four axes | S01-S04 distinguish a learning/feedback path from request-oriented delivery organization. S05 separates story value, size, independence, and testability; no source makes “shortest working diff” a synonym for any of them. | `split`: tracer bullet, vertical slice, bite-sized task, and shortest working diff should remain separate decisions with stated overlap, not aliases | untested |
| UBL01-C2 | conflicted | S01 demonstrates a thin real path through several components; S04 groups the concerns needed for a request. Neither supports the universal “every necessary real layer” formulation, and S01 permits a skeletal, non-final base. | `narrow`: require the real components or concerns needed for the selected feedback or value, not every architectural layer and not necessarily customer-complete value | untested |
| UBL01-C3 | supported as local completion policy, not as a term definition | S05-S07 support testable, observable, usable completion evidence. They do not define “independently verifiable” as tracer-bullet or vertical-slice semantics, and independence in S05 concerns negotiability/order rather than reviewer isolation or concurrency. S12-S15 show declared migration dependencies without waiving releasability or compatibility. | `narrow`: retain explicit proof through the claimed boundary as a local gate; do not present independent verification as definitional or treat migration dependency as an exception to intermediate operability | untested |
| UBL01-C4 | underlying distinction supported; terminology not supported as general professional vocabulary | S08-S11 distinguish predecessor satisfaction, eligibility, scheduler state, resources, and concurrency. “Blocking edge” is understandable graph language, but no inspected source establishes “frontier” as a stable cross-domain planning term. | `demote`: define a local dependency-ready frontier if retained; qualify readiness dimensions and state explicitly that unblocked or independent work is not thereby concurrency-safe | untested |
| UBL01-C5 | conflicted and compound | S12-S15 support expand-migrate-contract compatibility sequencing, releasable intermediate states, coexistence, and real dependencies. S12 shows the pattern need not be broad. S16 treats blast radius as progressive-exposure risk, and no source equates migration phases with vertical product slices. | `split`: separate compatibility migration, progressive-exposure blast-radius control, and product-slice shape; use releasable/backward-compatible intermediate state rather than “green”; do not make broadness or failed vertical slicing an entry condition | untested |

## Important Concepts

- A tracer bullet is primarily a learning and steering strategy: establish a
  thin real path, observe it, and adjust from a proven base.
- A vertical slice is primarily a delivery or architecture shape organized
  around a request or valuable behavior. “Vertical” means crossing relevant
  concerns, not mechanically touching every named layer.
- Smallness, value, testability, dependency readiness, and concurrency are
  independent questions even when a good slice answers several together.
- Expand-migrate-contract preserves compatibility while old and new forms
  coexist. Its phases may be staged technical work without being independent
  product slices.
- Releasability, compatibility, and operability are more precise source-backed
  intermediate-state properties than the metaphorical word “green.”
- Blast radius concerns exposure and consequence containment. It can complement
  a migration, but it is not a phase or defining property of parallel change.

## Usable Techniques

1. Name the purpose first: learning path, customer/value slice, dispatch-size
   limit, dependency eligibility, compatibility migration, or exposure control.
2. For an end-to-end increment, name the selected feedback or behavior and the
   real components it must cross; avoid universal layer-count claims.
3. Record proof separately from size and independence: expected output,
   observable boundary, usability or releasability, and the applicable done
   condition.
4. Model readiness with named prerequisites, then check resource, ownership,
   state, and conflict constraints before claiming concurrency.
5. For incompatible interfaces or schemas, record expand, migrate, and contract
   phases plus coexistence, compatibility, release, and cleanup gates.

## Disagreements And Context Conditions

- S01's tracer bullet can be deliberately skeletal; S04's vertical slice is
  organized around fulfilling a request. Their overlap is real, but neither
  term subsumes the other.
- INVEST independence is desirable but negotiable. It does not establish that
  multiple implementation owners can safely edit or run shared resources.
- Staged horizontal or technical work is not automatically a slicing failure.
  S12-S15 show it can be the safer shape for compatibility-sensitive change.
- Dependency readiness is domain-relative. Graph APIs, issue trackers,
  workflow engines, and project schedules use different completion and resource
  rules; “frontier” therefore needs a local definition if used.

## Inferred Correction Directions

These are source-bounded inferences for UBL-24, not changes to the language
reference:

- Split the current tracer-bullet/vertical-slice compound label, then describe
  their possible overlap rather than treating them as one method.
- Replace universal layer language with the real path or relevant concerns
  required for the selected feedback/value claim.
- Keep a strong verification gate as repository policy while labeling it as
  policy, not inherited term meaning.
- Demote “frontier” from professional anchor to locally defined dependency-ready
  shorthand, and keep readiness separate from parallel safety.
- Rewrite the expand-contract row around coexistence and compatibility; split
  blast-radius control and product-slice classification into separate checks.

## Prune And Rejection Log

| Candidate Evidence | Decision | Reason |
| --- | --- | --- |
| Search snippets, Wikipedia, glossary mirrors, and unsourced agile summaries | rejected | Discovery aids are not adequate provenance for load-bearing meaning |
| Unlicensed copies of *The Pragmatic Programmer* | rejected | The complete 2001 author article, official tips, and licensed current preview provide lawful bounded access |
| Term-frequency evidence for “frontier,” “bite-sized,” or “green” | rejected | Frequency cannot establish a stable operational definition or completion gate |
| PMBOK or ISO material not available for direct inspection | rejected | Prestige without inspectable passages cannot carry the claim |
| Whole-repository history for GitLab, Airflow, or source packs | deferred | UBL-01 did not require intent or lineage to decide these semantic dispositions |
| Behavioral comparisons of candidate wording | deferred | No immutable candidate, control, task, harness, or evaluator is admitted; behavior remains `untested` |

## Evidence Gaps And Limitations

- Full text of the 2019 tracer-bullet chapter was not accessible beyond a
  licensed preview. S01-S02 are strong primary evidence, but exact edition
  drift beyond the accessible passage remains unverified.
- No inspected canonical source establishes “frontier” as a general planning
  term. The underlying ready-set concept is supported only within explicitly
  named dependency models.
- No source directly compares expand-contract phases with vertical product
  slices. Their separation is an inference from the distinct goals and gates
  in S04 and S12-S16.
- Live official documentation may change after the check date. This packet
  records the inspected semantics, not future stability.
- Source plausibility does not establish agent behavior, transfer, or local
  suitability. All five behavioral statuses remain `untested`.

None of these gaps prevents the bounded source dispositions above. No
conditional UBL-09-through-UBL-15 lane is decision-critical.

## Resource Use And Stop

- Inspected 16 source records / 22 directly linked pages across the three
  locked facets.
- Used three fresh-context, read-only source scouts inside UBL-01; root retained
  admission, classification, synthesis, writing, and verification ownership.
- Opened no repository-history, conversation, practitioner, or behavioral lane.
- Stopped after all five active claims received bounded dispositions and
  additional sources repeated the same learning/delivery, readiness/concurrency,
  and compatibility/product-slice distinctions.

## Completion-Gate Verification

- Every claim admitted by UBL-00 has one source classification, one bounded
  disposition, an EV-09 ledger pointer, and behavioral status `untested`.
- Canonical or original evidence and bounded counterpressure cover all three
  independent facets; rejected and deferred evidence lanes remain explicit.
- Provenance, access limits, disagreements, inferred applications, and
  unresolved gaps are preserved without promoting source plausibility to
  behavior, transfer, or local suitability.
- The evidence gaps do not block UBL-24, and no conditional UBL-09-through-
  UBL-15 lane is needed for the same correction decision.
- Only this packet and its campaign-ledger pointer were changed; no language
  reference, synthesis document, runtime skill, `CONTEXT.md`, or engineering
  contract was edited.
- The packet terminates with exactly one authorized decision token below.

## Final Decision

`source-packet-complete`
