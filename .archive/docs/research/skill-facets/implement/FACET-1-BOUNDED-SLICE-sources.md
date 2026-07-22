# Facet 1: Bounded Slice Source Search

Historical source-to-skill Prompt 03 artifact for `implement` Facet 1.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/custom/implement/SKILL.md`

Facet: `1. Bounded Slice`

Facet research question: How do strong teams keep one implementation run small,
valuable, independently provable, and reviewable?

Facet boundaries:

- Owns what makes one selected issue a bounded implementation slice.
- Owns how to keep adjacent behavior, cleanup, docs, config, and refactor work
  from joining the diff accidentally.
- Owns how to distinguish tracer-bullet slices from support slices.
- Owns what to do when proof failure reveals work outside the slice.
- Does not own writing ready-for-agent issues; `to-issues` and
  `triage/AGENT-BRIEF.md` own that.
- Does not own the full TDD procedure; `$tdd` owns red-green-refactor mechanics.
- Does not own the final review process; `$review` owns fixed-point review.
- Does not own baseline capture, commit, or implementation-note details beyond
  the slice boundary itself.

Prior artifacts:

- Intent and keywords:
  [`01-intent-and-keywords.md`](01-intent-and-keywords.md)
- Facet map:
  [`02-facet-map-and-research-plan.md`](02-facet-map-and-research-plan.md)

Do not rewrite the skill yet. Do not extract detailed lessons yet. Do not
summarize sources for their own sake.

## 1. Facet Search Objective

This source search is trying to find sources that make `bounded slice`
operational for an implementation agent: one selected issue becomes one useful,
proof-carrying, reviewable change, and adjacent work becomes either explicit
follow-up or a reason to stop/split.

The behavior to improve is scope control during `$implement`: the agent should
choose one observable behavior or support proof, keep validation and review
inside that boundary, and avoid turning proof failure, nearby cleanup, or broad
repo context into a larger mission.

Upper-bound source quality for this facet means sources that provide one or
more of:

- a durable leading word for a real narrow path, such as `tracer bullet`, `thin
  slice`, `small batch`, or `one self-contained change`;
- operational gates for slice size, proof, reviewability, and follow-up;
- empirical or industrial evidence that mixed concepts and wide diffs increase
  review/comprehension burden;
- direct translation to coding-agent behavior: clear task boundaries,
  validation commands, acceptance criteria, and stop conditions.

Noise for this facet includes generic Agile taxonomy, hard line-count or file
count folklore, scaled-process material that does not change one implementation
run, tool-branded agent jargon, and secondhand blog summaries when a primary
book, paper, official doc, or practitioner source is available.

## 2. Search Queries

### Books

- `"tracer bullets" "The Pragmatic Programmer"` - find the primary source for a
  narrow production-shaped path that produces feedback.
- `"walking skeleton" "Growing Object-Oriented Software"` - verify
  outside-in/walking-skeleton source pressure for the first end-to-end proof
  path.
- `"User Story Mapping" Jeff Patton "thin slices"` - ground slices in user or
  operator activity rather than code layers.
- `"Specification by Example" Gojko Adzic "acceptance criteria"` - find proof
  language for concrete examples and pass/fail commitments.
- `"Principles of Product Development Flow" "batch size"` - verify delivery
  economics around smallest useful batch, WIP, queueing, and feedback.

### Papers

- `"What makes a code change easier to review" empirical investigation
  reviewability` - find empirical factors behind reviewable changes.
- `"Characteristics of Useful Code Reviews" Microsoft "file count"` - verify
  file spread and useful-review signals.
- `"The effects of change decomposition on code review" controlled experiment`
  - test whether separating concepts improves review behavior.
- `"Do Small Code Changes Merge Faster" pull request size time-to-merge` - add
  a counterweight against overclaiming smallness as speed.
- `"Information Needs in Contemporary Code Review" splittable small patches` -
  connect slice boundaries to reviewer information needs.
- `"SWE-agent" "Agent-Computer Interfaces" automated software engineering` -
  bridge bounded tasks to tool/test feedback loops.
- `"Agentless" "LLM-based software engineering agents" localization repair
  validation` - test simple staged agent workflows against freeform autonomy.

### Manuals / Official Docs

- `"Small CLs" Google Engineering Practices "one self-contained change"` -
  verify the strongest operational gate for reviewable diffs.
- `"Software Engineering at Google" "Code Review" small changes` - connect
  small changes to large-scale industrial review.
- `DORA "working in small batches" software delivery` - verify modern
  delivery-economics language for feedback and recovery.
- `OpenAI Codex prompting smaller focused tasks validation` - find direct
  Codex task-boundary and verification guidance.
- `GitHub Copilot coding agent well scoped issues acceptance criteria tests` -
  verify coding-agent issue shape guidance.
- `Claude Code best practices runnable checks verification` - find first-party
  agent verification-loop guidance.

### Agentic Coding / LLM Tooling

- `site:developers.openai.com/codex Codex best practices bounded work tests
  planning` - direct bridge to Codex execution.
- `site:developers.openai.com/codex "non-goals" validation stopping condition`
  - find stop-condition vocabulary for bounded work.
- `"SWE-bench Verified" solvable issues tests` - verify benchmark framing around
  clear issues and correctness tests.
- `"AutoCodeRover" GitHub issues code search tests` - find localization,
  repair, and validation patterns.
- `"coding agent" "acceptance criteria" "well-scoped task"` - find official
  task-shaping docs without importing broad agent-framework jargon.

### Field Practice

- `"Humanizing Work" "Guide to Splitting User Stories"` - find practical
  vertical-slice and story-splitting gates.
- `"story splitting" "acceptance criteria" "Agile Alliance"` - verify a
  concise professional definition.
- `"Elephant Carpaccio" thin vertical slices Cockburn Kniberg` - find an
  exercise-backed source for tiny but still vertical slices.
- `"Continuous Delivery" "small batches" "working software"` - verify delivery
  feedback language from the Humble/Farley lane.
- `"SPIDR" "split user stories" Mountain Goat Software` - find practical split
  patterns as support, not a mandatory method.

## 3. Verified Source List

| Rank | Source | Type | Link / Locator | Verification Basis | Why It Matters | Expected Contribution | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Hunt and Thomas, *The Pragmatic Programmer*, Topic 12 "Tracer Bullets" | Classic SWE book | [Publisher](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/), [O'Reilly topic](https://www.oreilly.com/library/view/the-pragmatic-programmer/9780135956977/f_0030.xhtml), [Artima interview](https://www.artima.com/articles/tracer-bullets-and-prototypes) | Publisher/O'Reilly metadata verifies the book/topic; Artima verifies author discussion of tracer bullets and prototypes. | Best leading metaphor for a narrow real path through the system that produces feedback and can become production code. | `tracer bullet`; real path; feedback under actual conditions; avoid throwaway prototype drift. | High |
| 2 | Google Engineering Practices, "Small CLs" | Official engineering manual | [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) | Official Google engineering-practices page. | Strongest operational gate: one self-contained change, related tests, reviewer context, and judgment over hard limits. | "One self-contained change"; proof travels with the diff; file spread as a smell; no hard LOC threshold. | High |
| 3 | Humanizing Work, "The Humanizing Work Guide to Splitting User Stories" | Practitioner field guide | [Guide](https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/) | Author/practice site with concrete story-splitting guidance. | Best practical source for keeping a slice valuable and vertical instead of horizontal/layered. | Slice smells; value-preserving split gates; support-slice caveats; follow-up decisions. | High |
| 4 | Ram et al., "What Makes a Code Change Easier to Review?" | Empirical software engineering paper | [Mozilla page](https://www.mozillafoundation.org/en/research/library/what-makes-a-code-change-easier-to-review-an-empirical-investigation-on-code-change-reviewability/), [PDF](https://marco-c.github.io/publications/reviewability-fse2018.pdf) | Mozilla research-library page and author PDF verify an empirical investigation of reviewability. | Best empirical definition pressure for reviewable change beyond "small". | Explained, properly sized, coherent, self-contained changes; avoid size-only framing. | High |
| 5 | Freeman and Pryce, *Growing Object-Oriented Software, Guided by Tests* | Classic testing/design book | [Book site](https://growing-object-oriented-software.com/), [TOC](https://growing-object-oriented-software.com/toc.html), [O'Reilly Chapter 10](https://www.oreilly.com/library/view/growing-object-oriented-software/9780321574442/ch10.html) | Book site/TOC verify acceptance-test and walking-skeleton chapters; O'Reilly verifies Chapter 10. | Strong outside-in proof source when a new or uncertain shape needs one thin end-to-end path first. | Acceptance test first; walking skeleton as conditional tool; feedback before breadth. | High |
| 6 | Jeff Patton, story mapping / thin slices | Product and requirements source | [Official story mapping page](https://jpattonassociates.com/story-mapping/), [The New Backlog](https://jpattonassociates.com/the-new-backlog/), [O'Reilly](https://www.oreilly.com/library/view/user-story-mapping/9781491904893/) | Author site and O'Reilly metadata verify the source lane. | Grounds implementation slices in user/caller/operator activity, not folder or component layers. | Activity/path vocabulary; thin release slice; whole-map context without boiling the ocean. | High |
| 7 | DORA, "Working in Small Batches" | Official delivery capability | [DORA capability](https://dora.dev/capabilities/working-in-small-batches/) | Official DORA/Google Cloud capability page. | Best modern delivery-economics source for feedback, remediation, and risk reduction from smaller work units. | Small batch rationale; recovery and learning loops; avoid building too much before feedback. | High |
| 8 | *Software Engineering at Google*, Chapter 9 "Code Review" | Official SWE book chapter | [Chapter](https://abseil.io/resources/swe-book/html/ch09.html) | Public Abseil-hosted chapter from the official book. | Reinforces small changes as reviewability and maintainability practice at industrial scale. | Lightweight review norms; reviewer comprehension; small change as optimization, not dogma. | High |
| 9 | OpenAI Codex Prompting / Best Practices | Official agentic-coding docs | [Prompting](https://developers.openai.com/codex/prompting), [Best practices](https://developers.openai.com/codex/learn/best-practices) | Official OpenAI Developers documentation. | Direct bridge from SWE slice language to Codex behavior: smaller focused tasks, tests, validation, review. | Agent goal boundaries; success criteria; verification-loop wording. | High |
| 10 | GitHub Copilot coding agent best practices | Official agentic-coding docs | [GitHub Docs](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results) | Official GitHub documentation. | Confirms coding agents need well-scoped tasks, acceptance criteria, and concrete repo/file context. | Issue/task anatomy; acceptance criteria; file hints; no broad agent mission. | High |
| 11 | di Biase et al., "The Effects of Change Decomposition on Code Review" | Empirical code-review paper | [arXiv](https://arxiv.org/abs/1805.10978) | arXiv record and related DOI metadata verify a controlled experiment. | Best empirical support for separating different concepts while avoiding magic claims about defect discovery. | Concept separation; lower reviewer noise; stop mixing adjacent work. | High |
| 12 | Kudrjavets et al., "Do Small Code Changes Merge Faster?" | Empirical code-review paper / contrast | [arXiv](https://arxiv.org/abs/2203.05045) | arXiv record verifies the large PR/review data study. | Essential counterweight: do not claim small changes automatically merge faster. | Anti-overclaim guardrail; small means comprehensible/provable/recoverable, not guaranteed faster. | High |
| 13 | Bosu, Greiler, Bird, "Characteristics of Useful Code Reviews" | Empirical code-review paper | [Microsoft Research](https://www.microsoft.com/en-us/research/publication/characteristics-of-useful-code-reviews-an-empirical-study-at-microsoft/) | Microsoft Research publication page verifies the MSR 2015 study. | Adds empirical support that file spread and review context affect useful feedback. | File-count/file-spread smell; useful feedback density; review usefulness over approval speed. | High |
| 14 | Pascarella et al., "Information Needs in Contemporary Code Review" | Empirical code-review paper | [TU Delft metadata](https://research.tudelft.nl/en/publications/information-needs-in-contemporary-code-review/), [PDF](https://pure.tudelft.nl/ws/files/53074402/cscw_author_version.pdf) | University metadata and PDF verify peer-reviewed CSCW source. | Connects bounded slices to reviewer information needs: rationale, context, splittability, and revertability. | Rationale/context gate; reviewer burden; small self-contained patches. | Medium |
| 15 | Anthropic, "Building Effective Agents" | Official agent engineering article | [Article](https://www.anthropic.com/research/building-effective-agents) | Official Anthropic research/engineering article. | Useful bridge for clear task, success criteria, feedback loops, and human oversight. | Stop/ask rules; clear criteria; avoid unconstrained autonomy. | Medium |
| 16 | Agentless: "Demystifying LLM-Based Software Engineering Agents" | Agentic coding paper | [arXiv](https://arxiv.org/abs/2407.01489), [ACM DOI](https://dl.acm.org/doi/10.1145/3715754) | arXiv and ACM records verify the paper. | Good contrast against over-agentic freeform autonomy; supports staged localize-repair-validate behavior. | Localization-repair-validation; simple staged workflow; avoid framework jargon. | Medium |
| 17 | SWE-agent: "Agent-Computer Interfaces Enable Automated Software Engineering" | Agentic coding paper | [arXiv](https://arxiv.org/abs/2405.15793) | arXiv record verifies the paper. | Supports executable tool feedback and repo navigation/edit/test loops for coding agents. | Tool/test feedback loop; bounded edit/validate cycle; keep ACI jargon out of runtime skill text. | Medium |
| 18 | Continuous Delivery, Humble/Farley lane | Delivery source | [continuousdelivery.com](https://continuousdelivery.com/), [Fowler book page](https://martinfowler.com/books/continuousDelivery.html) | Official site and Fowler book page verify the source lane. | Supports small batches as feedback from working software rather than all-at-once delivery. | Working state; fast feedback; avoid broken middle. | Medium |
| 19 | Gojko Adzic, *Specification by Example* | Requirements/testing book | [Manning](https://www.manning.com/books/specification-by-example) | Publisher page verifies the book and topic. | Useful support for turning a slice into concrete examples and pass/fail commitments. | Acceptance examples; proof commitments; avoid abstract "done" claims. | Medium |
| 20 | Scrum Guide, Definition of Done / Increment | Official framework guide | [Scrum Guide](https://scrumguides.org/scrum-guide.html) | Official Scrum Guide page. | Lightweight done-gate support, but too process-oriented to be central. | "No proof, no done" pressure; quality gate language without ceremony. | Medium |

## 4. Expected But Unverified Sources

| Source | Why It Might Matter | How To Verify | Keep Searching? |
| --- | --- | --- | --- |
| Alistair Cockburn primary "Walking Skeleton" source | Could strengthen walking-skeleton origin and architecture-risk framing. | Find a primary Cockburn page, book excerpt, or conference/source PDF rather than a bio mention. | Maybe, only if Prompt 04 needs stronger historical grounding. |
| Don Reinertsen, *Principles of Product Development Flow* | Could sharpen smallest useful batch, queueing, WIP, and economic tradeoff language. | Verify through publisher, author page, or library metadata beyond retailer listings. | Yes, before using as a core extraction source. |
| Mike Cohn / SPIDR story splitting | Could provide practical split-pattern vocabulary. | Verify against Mountain Goat official articles and compare against Humanizing Work overlap. | Maybe; likely supporting only. |
| Cucumber user-story / Given-When-Then docs | Could support acceptance-criteria examples. | Verify official Cucumber docs and confirm relevance to bounded slice rather than semantic proof facet. | Maybe; stronger for Semantic Proof than Bounded Slice. |
| Elephant Carpaccio primary material | Could provide extreme thin-slice practice language. | Verify Cockburn/Kniberg primary material and avoid treating the exercise as runtime procedure. | Maybe; supporting only. |
| AutoCodeRover | Could support localize-search-repair-validate agent behavior. | Verify paper metadata and decide whether it adds anything beyond Agentless/SWE-agent. | No unless agentic bridge feels thin. |

## 5. Source Quality Notes

- `core`: *The Pragmatic Programmer* tracer bullets. Best leading word for a
  narrow real path that produces feedback without becoming throwaway prototype
  work.
- `core`: Google Engineering Practices "Small CLs". Strongest operational
  source for one self-contained reviewable change with related tests/context.
- `core`: Humanizing Work story splitting. Most directly useful for deciding
  whether work is a vertical, valuable slice or a horizontal/support fragment.
- `core`: Ram et al. reviewability paper. Best empirical guard against shallow
  "small means few lines" wording.
- `core`: GOOS walking skeleton / acceptance-test flow. Essential if extraction
  needs outside-in proof language, with the caveat that walking skeleton is
  conditional for new/uncertain structure, not every issue.
- `core`: Patton story mapping / thin slices. Best product-path source for
  keeping slices tied to user/caller/operator activity.
- `supporting`: DORA working in small batches. Useful delivery-economics source
  for feedback and recovery.
- `supporting`: *Software Engineering at Google* code review. Good large-scale
  reinforcement for reviewability and maintainability.
- `bridge`: OpenAI Codex Prompting / Best Practices. Directly translates slice
  discipline into Codex task boundaries and verification.
- `bridge`: GitHub Copilot coding-agent docs. Useful first-party source for
  well-scoped coding-agent tasks and acceptance criteria.
- `supporting`: di Biase et al. change decomposition. Empirical support for
  separating different concepts, with limits.
- `contrast`: Kudrjavets et al. small-change/time-to-merge paper. Prevents
  overclaiming that small automatically means faster.
- `supporting`: Bosu et al. useful code reviews. Good empirical backing for file
  spread/review usefulness, less directly slice-specific.
- `supporting`: Pascarella et al. information needs. Good for reviewer context
  and splittability; likely stronger in Review And Lock later.
- `bridge`: Anthropic effective agents. Useful general agent-loop support, but
  less specific to implementation slices than OpenAI/GitHub docs.
- `contrast`: Agentless. Useful against over-autonomous workflows; extract only
  staged localize/repair/validate pressure, not benchmark jargon.
- `bridge`: SWE-agent. Useful for executable feedback loop; avoid ACI/harness
  vocabulary in runtime text.
- `supporting`: Continuous Delivery. Good small-batch rationale, but the DORA
  page is a more concise extraction target for this facet.
- `supporting`: Specification by Example. Valuable proof language, but stronger
  for Semantic Proof unless extraction needs examples to define the active
  slice.
- `reject`: generic vertical-slice architecture articles. Often discuss code
  organization/CQRS rather than one implementation run.
- `reject`: Medium/dev.to tracer-bullet explainers. Mostly secondhand summaries
  when primary book/interview sources exist.
- `reject`: hard PR-size / LOC threshold posts. They fight the actual evidence:
  useful smallness is self-contained, comprehensible, provable, and recoverable.
- `reject`: scaled Agile/portfolio WIP sources. Too broad for a single
  `$implement` run.
- `reject`: agent-framework jargon sources that do not change slice boundaries,
  validation gates, or stop/split behavior.

## 6. Expected Extraction Targets

| Source | Extract For | Watch For | Avoid Extracting |
| --- | --- | --- | --- |
| *The Pragmatic Programmer* tracer bullets | Leading word; real path through production-shaped system; feedback under real conditions. | Keep prototype/tracer distinction clear. | Long metaphor, historical examples, or advice to skip proof. |
| Google "Small CLs" | Behavior gates: one self-contained change, related tests, reviewer context, no hard size rule. | "Small" includes conceptual spread and file spread, not just line count. | Numeric thresholds or generic "make it smaller" no-op language. |
| Humanizing Work story splitting | Vertical-vs-horizontal gate; value-preserving split; in-scope branch vs follow-up. | This facet should not teach all splitting methods. | Agile ceremony, full story-writing procedure, backlog management. |
| Ram et al. reviewability | Empirical reviewability factors: size, description, coherent history, self-contained change. | Use as pressure for reviewable implementation, not review procedure. | Detailed metrics or tool-specific reviewability scoring. |
| GOOS walking skeleton | Outside proof, acceptance test first, feedback source before broad implementation. | Walking skeleton is for uncertain/new system shape. | Making walking skeleton mandatory for every issue. |
| Patton story mapping / thin slices | Activity/path vocabulary; thin slice tied to user/caller/operator outcome. | `implement` consumes ready issues; it does not story-map the backlog. | Product-discovery workshop procedure. |
| DORA working in small batches | Feedback, recovery, and risk language for small useful batches. | Avoid turning `$implement` into delivery-process doctrine. | DORA capability taxonomy beyond bounded work. |
| *Software Engineering at Google* code review | Reviewability and maintainability reasons for smaller changes. | Keep `$review` as owner of full review mechanics. | Full Google code-review process or approval rules. |
| OpenAI Codex docs | Agentic bridge: smaller focused tasks, success criteria, validation commands. | Codex docs are tool-specific; translate into skill-neutral behavior. | Prompting tutorial detail unrelated to implementation scope. |
| GitHub Copilot coding-agent docs | Well-scoped task anatomy, acceptance criteria, file/repo hints. | Issue creation belongs upstream to `to-issues` and `triage`. | GitHub-specific coding-agent workflow. |
| di Biase et al. change decomposition | Failure mode: mixed concepts; stop/split when a change contains separate concepts. | Decomposition improved review behavior, not guaranteed defect finding. | Claiming decomposition is always faster or finds more bugs. |
| Kudrjavets et al. small-change study | Contrast guardrail against merge-speed claims. | Use as anti-overclaim only. | Treating negative speed result as anti-small-batch argument. |
| Bosu et al. useful reviews | File-spread smell and useful-feedback framing. | Less direct than Google/Ram; keep supporting. | Raw comment-count optimization. |
| Agentless / SWE-agent | Agentic staged loop: localize, edit, validate; executable feedback. | Keep runtime text free of benchmark/framework vocabulary. | ACI, ReAct, leaderboard, pass-rate, or autonomous-agent jargon. |

## 7. Coverage Check

- Do we have at least one strong professional SWE source? Yes:
  *The Pragmatic Programmer*, GOOS, Google Engineering Practices, and
  *Software Engineering at Google*.
- Do we have at least one source that connects to agentic coding or LLM
  behavior? Yes: OpenAI Codex docs, GitHub Copilot coding-agent docs,
  Agentless, and SWE-agent.
- Do we have at least one source that gives operational gates rather than taste
  words? Yes: Google "Small CLs", Humanizing Work story splitting, OpenAI Codex
  docs, and GitHub Copilot docs.
- Are we over-weighting one author, school, era, or tool? Mostly no. The set
  balances classic SWE, product slicing, modern delivery, empirical review, and
  official coding-agent docs. Google appears several times, but in distinct
  lanes: review practice, DORA delivery, and SWE book/practices.
- What source lane is missing? Strong empirical evidence for product/story
  slicing itself is weaker than the code-review lane. That is acceptable if the
  extraction treats story slicing as practitioner taste and uses empirical
  sources for reviewability/comprehension claims.
- Which recommended sources still need stronger verification? Reinertsen,
  Cockburn primary walking-skeleton material, SPIDR, and Elephant Carpaccio are
  not in the recommended extraction set until better primary verification is
  found.

## 8. Recommended Source Set

| Priority | Source | Why Extract Next |
| --- | --- | --- |
| 1 | Hunt and Thomas, *The Pragmatic Programmer*, "Tracer Bullets" | Best leading word for one narrow real path that produces feedback and avoids prototype drift. |
| 2 | Google Engineering Practices, "Small CLs" | Best operational gate for one self-contained, tested, reviewable change. |
| 3 | Humanizing Work, "Guide to Splitting User Stories" | Best practical source for vertical/value-preserving slice boundaries and follow-up decisions. |
| 4 | Ram et al., "What Makes a Code Change Easier to Review?" | Best empirical source for reviewability factors beyond line count. |
| 5 | GOOS, walking skeleton / acceptance-test flow | Best outside-in proof source when a thin end-to-end path is needed. |
| 6 | Jeff Patton story mapping / thin slices | Best product-path source for user/caller/operator activity slices. |
| 7 | OpenAI Codex Prompting / Best Practices | Direct bridge from bounded SWE slice to Codex execution and verification behavior. |
| 8 | DORA, "Working in Small Batches" | Best concise delivery-economics support for feedback and recovery. |
| 9 | di Biase et al. plus Kudrjavets et al. | Paired empirical guardrails: separate concepts, but do not overclaim speed or defect guarantees. |

## 9. Output Artifact

Final source search packet:
`docs/research/skill-facets/implement/FACET-1-BOUNDED-SLICE-sources.md`

- Best source to start extraction from: Hunt and Thomas, *The Pragmatic
  Programmer*, "Tracer Bullets".
- Strongest source lane: professional SWE practice plus code-review
  reviewability.
- Weakest source lane: empirical evidence for product/story slicing itself.
- Biggest risk in the source set: overcompressing `bounded slice` into "small"
  and losing the stronger criteria: useful, self-contained, provable,
  reviewable, and recoverable.
- Ready for source extraction: yes.
