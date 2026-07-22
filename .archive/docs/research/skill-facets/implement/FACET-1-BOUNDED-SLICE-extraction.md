# Facet 1: Bounded Slice Source Extraction

Historical source-to-skill Prompt 04 artifact for `implement` Facet 1.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/custom/implement/SKILL.md`

Facet: `1. Bounded Slice`

Facet research question: How do strong teams keep one implementation run small,
valuable, independently provable, and reviewable?

Source search packet:
[`FACET-1-BOUNDED-SLICE-sources.md`](FACET-1-BOUNDED-SLICE-sources.md)

Do not rewrite the skill yet. Do not decide final runtime wording yet. Do not
summarize sources for their own sake. Do not discard extracted material just
because it feels redundant; Prompt 05 owns triage.

## 1. Extraction Scope

This extraction is for `implement` Facet 1: `Bounded Slice`.

In-scope verified sources:

- Hunt and Thomas, *The Pragmatic Programmer*, "Tracer Bullets":
  [publisher](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/),
  [O'Reilly topic](https://www.oreilly.com/library/view/the-pragmatic-programmer/9780135956977/f_0030.xhtml),
  [Artima interview](https://www.artima.com/articles/tracer-bullets-and-prototypes)
- Google Engineering Practices, [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
- Humanizing Work, [Guide to Splitting User Stories](https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/)
- Ram et al., [What Makes a Code Change Easier to Review?](https://www.mozillafoundation.org/en/research/library/what-makes-a-code-change-easier-to-review-an-empirical-investigation-on-code-change-reviewability/)
- Freeman and Pryce, *Growing Object-Oriented Software*:
  [book site](https://growing-object-oriented-software.com/),
  [TOC](https://growing-object-oriented-software.com/toc.html),
  [Chapter 10](https://www.oreilly.com/library/view/growing-object-oriented-software/9780321574442/ch10.html)
- Jeff Patton, [The New User Story Backlog is a Map](https://jpattonassociates.com/the-new-backlog/)
  and [story mapping](https://jpattonassociates.com/story-mapping/)
- DORA, [Working in Small Batches](https://dora.dev/capabilities/working-in-small-batches/)
- *Software Engineering at Google*, [Chapter 9: Code Review](https://abseil.io/resources/swe-book/html/ch09.html)
- OpenAI Codex [Prompting](https://developers.openai.com/codex/prompting)
  and [Best Practices](https://developers.openai.com/codex/learn/best-practices)
- GitHub Copilot coding-agent [best practices](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results)
- di Biase et al., [The Effects of Change Decomposition on Code Review](https://arxiv.org/abs/1805.10978)
- Kudrjavets et al., [Do Small Code Changes Merge Faster?](https://arxiv.org/abs/2203.05045)
- Bosu, Greiler, Bird, [Characteristics of Useful Code Reviews](https://www.microsoft.com/en-us/research/publication/characteristics-of-useful-code-reviews-an-empirical-study-at-microsoft/)
- Pascarella et al., [Information Needs in Contemporary Code Review](https://research.tudelft.nl/en/publications/information-needs-in-contemporary-code-review/)
- Anthropic, [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- Agentless, [Demystifying LLM-Based Software Engineering Agents](https://arxiv.org/abs/2407.01489)
- SWE-agent, [Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793)

Source lanes represented:

- classic and professional software engineering;
- product/requirements slicing;
- delivery and small-batch feedback;
- empirical code-review research;
- official coding-agent guidance and agentic coding papers.

Intentionally out of scope:

- full story-writing, story-mapping, backlog, or product-discovery procedure;
- full TDD mechanics, which `$tdd` owns;
- full fixed-point review mechanics, which `$review` owns;
- runtime `SKILL.md` wording, which later synthesis prompts own;
- hard PR-size or LOC policy.

## 2. Source Coverage

| Source | Sections / Chapters / Pages / Docs Used | Why This Part Was Used | Extraction Confidence |
| --- | --- | --- | --- |
| *The Pragmatic Programmer* / Artima tracer-bullet interview | Topic 12 metadata; Artima sections on tracer bullets, skeleton applications, and prototypes | Extract leading word for one real path, feedback under real conditions, and prototype/tracer distinction. | High |
| Google Engineering Practices, "Small CLs" | "What is Small?", splitting CLs, separate refactorings, related test code, can't make it small enough | Extract operational gates for one self-contained change, proof in the diff, reviewer context, file spread, and stop/split behavior. | High |
| Humanizing Work story splitting | INVEST/value, workflow slices, operations, variations, spike split, split evaluation | Extract vertical/value-preserving slice rules and failure modes like component masquerade, variation creep, and spike drift. | High |
| Ram et al. reviewability | Mozilla overview plus paper framing surfaced in source search | Extract empirical reviewability factors: description, size, coherent history, self-containment, and composite-change pressure. | High |
| GOOS walking skeleton / acceptance-test flow | Book TOC and Chapter 10 page | Extract conditional walking-skeleton and outside-proof behavior for new or uncertain system shape. | High |
| Jeff Patton story mapping | Activity/task/backbone and smallest end-to-end system sections | Extract user/caller/operator activity vocabulary and "little walking skeleton" framing without importing workshop procedure. | High |
| DORA working in small batches | Benefits, INVEST-like batch attributes, AI pitfalls, small-batch reduction | Extract feedback/recovery rationale, independent/testable batch gates, and AI large-change caution. | High |
| *Software Engineering at Google*, Code Review | Review flow, correctness/comprehension, maintainability, ownership concerns | Extract reviewability as comprehension and correctness pressure; avoid full review process. | High |
| OpenAI Codex Prompting / Best Practices | Smaller focused steps, validation, task context, done-when guidance | Extract direct Codex bridge for focused task, checkability, validation, and reviewability. | High |
| GitHub Copilot coding-agent docs | Well-scoped issues, unsuitable task classes, planning before PR | Extract coding-agent stop conditions around vague, broad, sensitive, and domain-heavy tasks. | High |
| di Biase et al. change decomposition | arXiv abstract/results/conclusions | Extract concept separation and its empirical limits. | High |
| Kudrjavets et al. small changes/time-to-merge | arXiv abstract/results | Extract anti-overclaim guardrail: do not justify bounded slices by guaranteed merge speed. | High |
| Bosu et al. useful reviews | Microsoft Research abstract/summary | Extract file spread as review-size smell and useful-comment quality over quantity. | High |
| Pascarella et al. information needs | TU Delft abstract and source packet notes | Extract reviewer information needs: rationale, code context, necessity, splittability, and expertise. | Medium |
| Anthropic effective agents | Clear criteria, simple patterns, evaluator loop | Extract agent autonomy guardrails and success-criteria language. | Medium |
| Agentless | Localization, repair, validation staging | Extract localize-repair-validate behavior and anti-over-agentic contrast. | Medium |
| SWE-agent | Tool/test feedback and repository interaction framing | Extract tool feedback as evidence loop, while avoiding ACI/framework jargon. | Medium |

## 3. Leading Words

| Term | Source | Meaning In Source | Possible Skill Use | Behavior It Should Trigger | Risk / Caveat |
| --- | --- | --- | --- | --- | --- |
| `tracer bullet` | *The Pragmatic Programmer* / Artima | A narrow production-shaped path that produces early feedback under real conditions. | Name the selected implementation slice as one real path, not a broad feature bucket. | Lock one user/caller/operator path or support unblocker, prove it, then stop or adjust within bounds. | Can become excuse for incomplete or throwaway code if prototype distinction is lost. |
| `one self-contained change` | Google Small CLs | A change that addresses one thing, includes related tests, gives reviewer context, and leaves the system working. | Core bounded-slice gate. | Keep code, proof, and rationale together for one concept. | Can be split so small that the implication is hard to understand. |
| `vertical slice` | Humanizing Work | A value-preserving slice through layers, not a layer/component task pretending to be a story. | Distinguish behavior slices from horizontal implementation chunks. | Prefer one observable behavior path through needed layers; classify layer-only work as support. | Can become slogan or UI-to-database dogma. |
| `thin slice` | Patton / Humanizing Work | A small user/caller activity path or variation that still teaches or delivers value. | Keep the issue grounded in caller/operator activity. | Name the activity or caller outcome before coding. | Can pull `implement` into upstream story-mapping work. |
| `walking skeleton` | GOOS / Patton | Minimal end-to-end structure for a new or uncertain system/feature shape. | Conditional tool for uncertain system shape. | Establish the smallest executable feedback path before breadth. | Too heavy for routine fixes; must not become mandatory for every issue. |
| `small batch` | DORA / Continuous Delivery | A small independently testable unit that speeds feedback and remediation. | Explain why the slice should be independently validated and recoverable. | Keep one run to one validated unit; do not regroup adjacent batches before proof. | Do not claim small automatically means faster merge or higher value. |
| `one concept` | di Biase / Ram | Different concepts should be separated to reduce review noise and improve comprehension. | Split behavior/support/refactor/docs/config when they become independently meaningful concepts. | Stop when the diff can no longer be summarized as one concept. | Some coupled edits are legitimately one behavior and should not be mechanically split. |
| `reviewable change` | Ram / Google / SWE@Google | A change with clear description, manageable size/spread, coherent history, and enough context for comprehension. | Make reviewability a completion pressure before `$review`. | Self-review whether purpose, changed areas, proof, and risk are understandable cold. | Reviewability must not replace semantic correctness. |
| `file spread` | Google / Bosu | The number and spread of touched files affects review burden, independent of line count. | Treat broad touched-area spread as scope warning. | Re-bound or justify every touched area when the diff spreads. | Cross-cutting fixes may be necessary; do not avoid them blindly. |
| `success criteria` | OpenAI / GitHub / Anthropic | Clear pass/fail conditions that let an agent validate work. | Lock proof target before editing. | Name the focused test/check/inspection that proves the slice. | Subjective criteria can create validation theater. |
| `localize-repair-validate` | Agentless / SWE-agent | Stage work by finding relevant context, making a narrow repair, and validating the patch. | Bridge SWE bounded-slice language into coding-agent actions. | Read/search to locate the relevant seam, edit narrowly, validate with tools. | Bug-repair phrasing can be too rigid for feature/support slices. |
| `tool feedback` | SWE-agent / OpenAI Codex | Command/test output and environment responses steer the next step. | Keep fixes grounded in evidence. | Let failures steer only in-scope fixes; classify out-of-scope failures. | Tool output can send the agent into unrelated work if relevance is not checked. |

## 4. Behavior Rules

| Rule | Source | Agent Behavior | When It Applies | Evidence Gate | Failure Prevented |
| --- | --- | --- | --- | --- | --- |
| Lock the slice before editing. | Tracer bullets; OpenAI/GitHub task guidance; Ram reviewability | Name one behavior/support proof, likely touched areas, validation target, and non-goals. | Before production edits for the selected issue. | The work can be stated as one path/concept and one proof. | Issue-title implementation, scope drift, hidden assumptions. |
| Prefer one real path over broad feature breadth. | *The Pragmatic Programmer*; GOOS; Patton | Implement the narrowest production-shaped path that can give feedback. | New behavior or uncertain implementation shape. | A focused check proves the selected path or highest useful seam. | Building broad feature surface before learning whether the path works. |
| Treat support work as support, not fake user value. | Humanizing Work; Google Small CLs | If the issue is config/docs/refactor/test harness, state the support purpose and proof. | A ready issue is not user-visible behavior. | Validation proves the unblocker or behavior-preserving support change. | Forcing support work into bogus vertical-slice language. |
| Reduce variation to one complete required case. | Humanizing Work | Pick one scenario, rule, data variation, interface variation, or workflow path that satisfies the issue; record non-required variations as follow-up. | The issue includes multiple variations or examples. | Test/fixture/example names the chosen variation and passes. | Variation creep and accidental whole-feature implementation. |
| Do not implement a broken middle. | Humanizing Work; GOOS; Patton | Prefer a minimal complete path over only one internal workflow step when the issue promises behavior. | Workflow or multi-layer behavior issues. | Evidence exercises the minimal complete path. | A diff that compiles but cannot be used or validated as behavior. |
| Keep related proof with the diff. | Google Small CLs; OpenAI Codex docs | Add or update tests/fixtures/checks that prove this exact slice in the same change. | Logic, behavior, or support changes with a meaningful proof path. | Proof would fail if the promised behavior/support outcome were wrong. | Code-only completion and validation theater. |
| Separate broad refactors from behavior changes. | Google Small CLs; di Biase | Include only refactor/cleanup required for the slice or tiny local cleanup protected by proof. | Cleanup or refactor temptation appears during implementation. | Every cleanup change is required by the slice or named as follow-up. | Mixed behavior/refactor diffs and review confusion. |
| Treat file spread as scope evidence. | Google Small CLs; Bosu | When many files/areas are touched, re-check whether this is still one concept. | The diff spreads beyond the expected area. | Each touched area has an in-scope reason tied to one proof. | Broad opportunistic rewrites hidden behind modest line count. |
| Stop broadening after failed proof. | Tracer feedback; OpenAI/GitHub/Anthropic stop guidance | Classify failures as in-slice, adjacent follow-up, or changed commitment. | Validation fails or reveals more work. | The next action is either an in-slice fix, a recorded follow-up, or a user question. | Chasing every failing test or adjacent defect. |
| Justify bounded slices by proof, review, feedback, and recovery, not speed. | Kudrjavets; DORA; Google | Avoid claims that small PRs automatically merge faster. | Synthesis or runtime language explains why one slice matters. | Language ties boundedness to comprehension, validation, rollback/recovery, or feedback. | Unsupported speed/productivity folklore. |
| Localize before editing. | Agentless; SWE-agent; OpenAI Codex | Read/search enough to identify the relevant seam before touching files. | Before implementing the slice. | Changed files match the localized cause/proof path. | Broad autonomous wandering. |
| Make the diff understandable cold. | Google Small CLs; Ram; Pascarella; SWE@Google | Final note/diff context should carry rationale, proof, skipped checks, and residual risk without hidden scratch reasoning. | Before lock and before `$review`/handoff. | A reviewer can understand the purpose, changed areas, and proof. | Review depends on the agent's private exploration trail. |
| Use bounded offloads only. | OpenAI/GitHub/agentic bridge sources | Subagents or parallel work answer narrow questions; they do not expand the mission. | When using helper agents during implementation. | Offload result returns a bounded answer with evidence. | Multi-agent sprawl and parallel scope expansion. |

## 5. Failure Modes

| Failure Mode | Source | What Goes Wrong | Agent Warning Sign | Countermeasure | Evidence Gate |
| --- | --- | --- | --- | --- | --- |
| Prototype drift | *The Pragmatic Programmer* / Artima | Disposable learning code is mistaken for a production tracer path. | Scratch/spike code remains in the final diff without production proof. | Delete scratch or productionize and prove it. | Final diff contains only tested production code or documented non-production artifact requested by the user. |
| Heavy up-front certainty | Tracer-bullet contrast | Agent waits for exhaustive understanding instead of using a narrow real path to learn. | Long exploration produces no checkable slice. | Lock enough context for one path and proceed. | Slice has path, proof, non-goals, and stop conditions. |
| Walking-skeleton overuse | GOOS / Patton | Routine fixes get inflated into infrastructure or architecture work. | Agent creates skeleton/harness work unrelated to issue uncertainty. | Use walking skeleton only when shape or feedback path is uncertain. | Skeleton proves minimal path and is required for the selected issue. |
| Horizontal slice | Humanizing Work / Google splitting | Agent implements only one layer or component for a behavior issue. | "UI done, backend later" or "schema only" for user-visible behavior. | Reframe to a minimal complete path, or state it as a support slice. | Behavior path passes, or support proof validates the unblocker. |
| Component masquerade | Humanizing Work | Technical tasks are treated as value slices without a real behavior or support proof. | The issue has no beneficiary/outcome and no unblocker statement. | Classify as support slice and define support validation. | Validation proves the support change's intended effect. |
| Variation creep | Humanizing Work | The agent implements every rule/data/user/interface variation. | Diff grows across examples not required by acceptance criteria. | Choose one required variation; record adjacent variations. | Test/example names the chosen variation and acceptance coverage. |
| Broken middle | Humanizing Work / GOOS | Internal steps exist but no caller path works. | Code compiles but no check exercises the promised outcome. | Add the smallest complete path or stop if impossible in slice. | Focused behavior check passes through the selected path. |
| Tangled/composite change | Ram / di Biase | Multiple concepts appear in one diff, increasing review burden and wrong reports. | Summary becomes a list of unrelated fixes. | Split, ask, or move adjacent work to follow-up. | Final summary has one concept and one proof story. |
| File-spread blind spot | Google / Bosu | Small line count hides a wide review surface. | Many files/directories are touched for unclear reasons. | Re-bound and justify every touched area. | Each file supports the selected concept/proof. |
| Reviewability without correctness | Google / SWE@Google / Ram | The diff is easy to review but does not prove behavior. | Final evidence only says "looks clean" or "builds." | Require semantic proof for the selected slice. | Proof would catch the promised behavior being wrong. |
| Smallness speed myth | Kudrjavets | Bounded slice is justified by unsupported time-to-merge claims. | Language says small will be faster to merge. | Tie smallness to comprehension, proof, review usefulness, recovery, and feedback. | No runtime/synthesis claim depends on merge-speed guarantee. |
| Broad autonomous wandering | OpenAI / GitHub / Agentless | Agent searches/edits widely without a locked slice. | Many files opened or changed without relation to one proof. | Return to localize-repair-validate. | Each touched file has an in-scope reason. |
| Tool-feedback overtrust | SWE-agent / OpenAI | Noisy command output sends the agent into unrelated repairs. | Agent fixes failures not tied to the selected issue. | Classify failure as in-slice, adjacent, or environment. | Out-of-scope failures are recorded, not absorbed. |
| Validation theater | OpenAI / GitHub / SBE | A check runs but cannot prove the requested behavior. | Evidence is syntax-only for a semantic change. | Choose focused semantic proof or concrete fixture/example. | Evidence would fail on the bug/behavior being wrong. |
| Multi-agent sprawl | Agentic bridge sources | Delegated helpers expand the mission. | Subagents return new work outside the slice. | Assign narrow questions and integrate only bounded evidence. | Helper output answers the assigned question without new scope. |

## 6. Evidence Gates

| Gate | Source | What It Proves | How An Agent Can Check It | Too Weak If | Too Heavy If |
| --- | --- | --- | --- | --- | --- |
| Slice lock | Tracer bullets; OpenAI/GitHub docs | The run has one target before editing. | State selected behavior/support proof, non-goals, validation target, and likely touched areas. | It names only an issue title. | It becomes a full PRD/story-map exercise. |
| One self-contained change | Google Small CLs; Ram | The diff is one concept with enough context and proof. | Explain every changed file through one purpose. | It ignores related tests or context. | It splits inseparable dependent edits into nonsense. |
| Related proof travels with diff | Google Small CLs | Code and proof are reviewed together. | Tests/fixtures/checks/docs validation for the slice are changed or recorded with code. | It only says tests exist somewhere. | It pulls in unrelated test cleanup. |
| Highest useful path proof | Tracer bullets; GOOS; Humanizing Work | The selected behavior/support outcome works through the meaningful boundary. | Run focused test, fixture, command, or inspection that exercises the outcome. | It checks only syntax or output existence. | It requires slow end-to-end infrastructure when a narrower seam proves the issue. |
| Acceptance/success criteria named | GOOS; OpenAI; GitHub; Anthropic | The agent knows what done means. | Identify pass/fail acceptance, example, invariant, command, or explicit substitute. | It says "works" or "improve." | It demands all future variants. |
| File-spread review | Google; Bosu | Touched area breadth is still justified. | Inspect diff and list why each area belongs. | It counts only LOC. | It blocks necessary cross-file behavior changes. |
| Concept separation check | di Biase; Ram | The diff does not mix independent concepts. | Try to summarize the change as one sentence; move second concepts to follow-up. | The summary is a bag of fixes. | It refuses coupled edits required for proof. |
| Reviewer information check | Pascarella; Ram; Google | A future reviewer has enough rationale/context. | Final note includes issue link/intent, proof, skipped checks, residual risk, and follow-ups. | It depends on hidden scratch work. | It repeats all exploration details. |
| Feedback classification | DORA; OpenAI; SWE-agent | Failed proof is handled without scope drift. | Classify failure as in-slice, adjacent follow-up, changed commitment, or environment. | All failures are fixed blindly. | Agent stops on every minor in-scope failure. |
| Recovery/revertability check | DORA; Pascarella; Google | The slice can be understood and recovered as one unit. | Describe rollback/recovery blast radius or why not relevant. | The change spans unrelated behavior. | It imports production-release ceremony into local work. |

## 7. Stop / Ask Conditions

| Condition | Source | Why It Matters | Agent Should | Resume When |
| --- | --- | --- | --- | --- |
| The selected issue cannot be stated as one behavior/support proof. | OpenAI/GitHub task guidance; Humanizing Work | Implementation would be guesswork or a project bucket. | Ask for missing commitment or propose a narrower slice. | The issue has problem, acceptance/proof target, non-goals, and likely seam. |
| Implementation requires a second independent concept. | Google Small CLs; di Biase; Ram | Mixed concepts make review and proof worse. | Split, ask, or record follow-up instead of absorbing it. | The active diff returns to one concept, or user approves broader scope. |
| Proof failure points outside the locked slice. | Tracer feedback; OpenAI; SWE-agent | Tool feedback should not expand mission silently. | Stop, split, ask, or record follow-up. | New slice is approved or failure is shown to be in-scope. |
| File spread grows beyond the expected review surface. | Google Small CLs; Bosu | Broad spread is hidden size. | Re-bound and justify touched areas before continuing. | Each touched area supports the selected proof. |
| A broad refactor is needed to make progress. | Google Small CLs | Refactor mixed with behavior can obscure correctness. | Split refactor, ask, or keep only tiny protected local simplification. | Refactor is separate, approved, or proven necessary inside the slice. |
| Walking skeleton implies architecture, dependency, tooling, public contract, data, security, or privacy change. | GOOS; SWE@Google; GitHub unsuitable-task guidance | These are commitment boundaries, not ordinary technique. | Ask before implementing. | User approves the changed commitment or a smaller local path is chosen. |
| Acceptance criteria or success criteria are ambiguous. | OpenAI; GitHub; Anthropic; SBE | Agent cannot know what proof should prove. | Ask or produce a narrow plan for approval. | Pass/fail proof is concrete enough to run or inspect. |
| Task is broad, cross-repo, incident-like, security-critical, or deep-domain-heavy. | GitHub Copilot docs | Coding agents are poor fits for vague/high-risk broad tasks without human narrowing. | Stop or ask whether to split/escalate. | User confirms scope and risk boundary. |
| Validation cannot run in the environment. | OpenAI Codex docs; engineering-contract proof pressure | Done cannot honestly claim semantic proof. | Record blocker and use strongest available substitute. | Required tools are available or user accepts substitute evidence. |
| Helper agents produce adjacent opportunities. | Agentic bridge sources | Parallelism can widen the slice. | Integrate only assigned evidence; record adjacent work. | Adjacent work becomes a new approved slice. |

## 8. Agentic Bridge Language

| Source Concept | SWE Meaning | Agentic Meaning | Skill Behavior It Could Steer | Bridge Confidence |
| --- | --- | --- | --- | --- |
| Tracer bullet | Real narrow path creates feedback. | Use repo tools/tests to prove one path, then adjust within boundary. | Lock one path; prove it before breadth. | High |
| One self-contained change | Reviewable unit with code, proof, and context. | Keep one issue/concept plus related evidence in the diff. | One issue, one concept, related proof. | High |
| Vertical/thin slice | Observable value through needed layers. | Prefer one caller/operator path over layer-only work unless support slice is explicit. | Name behavior path or support proof before editing. | High |
| Small batch | Independent, testable unit for fast feedback/recovery. | Keep one run independently validated; do not regroup adjacent work. | Validate the unit and record follow-ups. | High |
| Reviewable change | Human can understand purpose and risk. | Self-review as if the reviewer lacks the agent's exploration context. | Make purpose, changed areas, proof, and risk understandable cold. | High |
| File spread | Review burden is not just line count. | Treat touched-area breadth as scope signal. | Re-bound when many files/areas change. | High |
| Success criteria | Clear pass/fail target. | Name what will prove the slice before editing. | Make task checkable before code. | High |
| Localize-repair-validate | Find context, patch narrowly, validate. | Search/read first, edit the smallest meaningful area, run focused proof. | Find relevant seam, change narrowly, validate. | Medium |
| Tool feedback | Command output guides work. | Use failures to steer only in-scope fixes. | Classify failed checks before fixing. | Medium |
| Simple agent loop | Avoid over-agentic ceremony. | Use plain search/edit/test/review/stop actions. | Keep framework vocabulary out of runtime wording. | Medium |
| Coherent unit/thread | One conversation/run should not become a project bucket. | Do not let `$implement` absorb adjacent issues discovered while working. | Finish or stop after one slice. | High |
| Specification by example | Concrete examples make expectations testable. | Use example/fixture/invariant when criteria are fuzzy. | Convert vague proof to concrete pass/fail or ask. | Medium |

## 9. Weak Or No-Op Language

| Weak Phrase | Source / Context | Why It Is Weak | Stronger Replacement Direction |
| --- | --- | --- | --- |
| "Keep it small" | Common summary of Google/DORA/review research | Size-only; can become line-count policy. | One self-contained behavior/support change with related proof. |
| "Do a vertical slice" | Product slicing sources | Slogan unless tied to observable behavior and proof. | One user/caller/operator path through the highest useful seam. |
| "Make progress" | Tracer/small-batch misread | Does not define feedback or done. | Produce feedback from the locked path. |
| "Add tests" | Google/OpenAI proof guidance | Test presence is not semantic proof. | Related proof travels with the diff and would fail if behavior were wrong. |
| "Avoid scope creep" | General bounded-slice idea | True but inert. | When a second concept appears, record follow-up, split, or ask. |
| "Be reviewable" | Reviewability sources | Good goal, weak action. | Reviewer can understand purpose, changed areas, and proof from the diff/note. |
| "Use walking skeleton" | GOOS/Patton | Overbroad for routine fixes. | Use walking skeleton only when system shape or feedback path is uncertain. |
| "Refactor as needed" | Google separate-refactor guidance | Invites cleanup drift. | Simplify only when protected and inside the selected slice. |
| "Run validation" | OpenAI/Codex guidance | Does not state what validation proves. | Run the focused check that would fail if the promised behavior/support outcome is wrong. |
| "Well-scoped task" | GitHub coding-agent docs | Useful source term, weak alone. | Problem, acceptance criteria, likely files/seam, non-goals. |
| "Use agentic workflows" | Agentic paper/docs lane | Jargon with no behavior. | Search, edit, test, review, and stop when scope changes. |
| "Autonomously solve it" | Agent autonomy lane | Encourages overreach. | Proceed autonomously inside the locked slice; ask when commitments change. |
| "Run tests if possible" | Validation escape hatch | Too easy to skip proof. | Run focused checks and explain skipped repo-standard validation. |
| "Small PRs merge faster" | Kudrjavets contrast | Unsupported by the cited empirical study. | Small enough to explain, prove, review, and recover as one unit. |
| "Just add a follow-up" | Story slicing misuse | Can dodge required acceptance criteria. | Follow-up only for non-required adjacent variation or separate concept. |
| "Spike it" | Humanizing Work spike caution | Invites open-ended research. | Answer bounded questions, then stop or implement the approved slice. |
| "MVP" | Product/delivery lane | Too product-process heavy for `implement`. | Smallest end-to-end proof for this issue. |

## 10. Extraction Notes By Source

### *The Pragmatic Programmer* / Tracer Bullets

Most useful extraction:

- A tracer bullet is a real narrow path that produces early feedback under
  actual conditions.

Strongest behavior pressure:

- Lock one path, prove it, and treat feedback as aim correction rather than
  permission to broaden.

Likely research-only material:

- The full artillery metaphor and management/prototype discussion.

Open question:

- How much of the tracer-bullet term should survive runtime without making the
  skill sound like it owns upstream slicing?

### Google Engineering Practices, Small CLs

Most useful extraction:

- One self-contained change includes related test code and enough reviewer
  context; smallness is conceptual, not just line count.

Strongest behavior pressure:

- Proof travels with the diff; broad refactor, config, docs, and behavior
  changes should split unless they are required for one selected slice.

Likely research-only material:

- Google-specific CL stacking and review process.

Open question:

- Whether `one self-contained change` is stronger than `bounded slice` as the
  runtime leading word.

### Humanizing Work Story Splitting

Most useful extraction:

- Component tasks can masquerade as stories; useful slices preserve value or
  have explicit support proof.

Strongest behavior pressure:

- Choose one required variation/path and record adjacent variations as
  follow-ups.

Likely research-only material:

- Full story-splitting flowchart and backlog/product-owner procedure.

Open question:

- How to keep `support slice` honest without forcing fake user-value language.

### Ram et al. Reviewability

Most useful extraction:

- Reviewability depends on description, size/self-containment, coherent history,
  and style, not raw smallness.

Strongest behavior pressure:

- If the implementation note can only summarize the diff as multiple fixes, the
  diff is probably not one bounded slice.

Likely research-only material:

- Tool-specific reviewability scoring and detailed study instrumentation.

Open question:

- Which reviewability factors belong in Facet 1 versus later Review And Lock.

### GOOS Walking Skeleton / Acceptance-Test Flow

Most useful extraction:

- For new or uncertain system shape, establish a minimal executable feedback
  path before breadth.

Strongest behavior pressure:

- Name the outside proof before implementation, but choose the highest useful
  proof rather than always demanding end-to-end tests.

Likely research-only material:

- Full outside-in TDD procedure, which `$tdd` owns.

Open question:

- How to phrase walking skeleton as conditional without weakening it into a
  no-op.

### Jeff Patton Story Mapping

Most useful extraction:

- Ground slices in user activities/tasks and smallest end-to-end functionality.

Strongest behavior pressure:

- A behavior slice should be explainable as a caller/operator activity, not as a
  folder or layer.

Likely research-only material:

- Story-map workshop mechanics and release planning.

Open question:

- Whether `caller/operator path` is more fitting than user-story language for a
  programming-agent skill.

### DORA Working In Small Batches

Most useful extraction:

- Small batches shorten feedback and remediation loops, and are especially
  important when AI can generate large changes quickly.

Strongest behavior pressure:

- Stop or split when AI speed produces a large mixed-concept diff.

Likely research-only material:

- Deployment/trunk-based delivery doctrine.

Open question:

- How much recovery/release language belongs in Facet 1 versus Review And Lock.

### *Software Engineering at Google*, Code Review

Most useful extraction:

- Review checks correctness, comprehension, maintainability, and ownership
  fit, not just style.

Strongest behavior pressure:

- Self-review the diff as a cold reviewer before handing it to `$review`.

Likely research-only material:

- Google-specific approval bits and ownership process.

Open question:

- Whether "cold reviewer" should become a runtime gate or stay synthesis-only.

### OpenAI Codex Prompting / Best Practices

Most useful extraction:

- Codex handles complex work better when broken into smaller focused steps with
  validation and done-when criteria.

Strongest behavior pressure:

- Make the slice checkable before editing and record validation/skips before
  done.

Likely research-only material:

- General prompt-writing advice and Codex product setup.

Open question:

- Whether `localize-repair-validate` should be translated fully into plain
  actions.

### GitHub Copilot Coding-Agent Docs

Most useful extraction:

- Coding-agent tasks should have a clear problem, acceptance criteria, and file
  or repo context; broad, ambiguous, sensitive, and domain-heavy tasks need
  extra care.

Strongest behavior pressure:

- Stop or narrow when the selected issue lacks a checkable proof target.

Likely research-only material:

- GitHub-specific cloud-agent workflow and PR iteration mechanics.

Open question:

- How much "unsuitable task" language belongs in `implement` now that `triage`
  owns readiness.

### di Biase et al. Change Decomposition

Most useful extraction:

- Separating different concepts supports reviewers and reduces wrong reports,
  while not guaranteeing more defect discovery.

Strongest behavior pressure:

- When a second concept appears, split, ask, or record follow-up.

Likely research-only material:

- Detailed experimental design.

Open question:

- How to distinguish legitimate coupled edits from tangled changes in one
  concise gate.

### Kudrjavets et al. Small Changes / Time To Merge

Most useful extraction:

- Small size/composition did not predict faster merge in the studied datasets.

Strongest behavior pressure:

- Do not justify bounded slices with speed folklore.

Likely research-only material:

- Dataset-specific time-to-merge analysis.

Open question:

- Whether this contrast needs runtime wording or just synthesis guardrails.

### Bosu et al. Useful Code Reviews

Most useful extraction:

- More files in a change correlated with a lower proportion of useful review
  comments.

Strongest behavior pressure:

- Treat touched-file spread as review-size smell even when LOC is modest.

Likely research-only material:

- Reviewer experience modeling and comment classifier details.

Open question:

- Whether file spread should be a stop condition or a re-check condition.

### Pascarella et al. Information Needs

Most useful extraction:

- Reviewers need rationale, context, necessity, expertise cues, and
  splittability/recoverability signals.

Strongest behavior pressure:

- Final evidence should make the diff understandable without hidden scratch
  context.

Likely research-only material:

- Full taxonomy of reviewer information needs.

Open question:

- Which reviewer-context items belong in Facet 1 versus Review And Lock.

### Anthropic Effective Agents

Most useful extraction:

- Clear success criteria and simple feedback loops matter more than complex
  agent patterns.

Strongest behavior pressure:

- Use the simplest workflow that can prove the slice.

Likely research-only material:

- Agent architecture pattern taxonomy.

Open question:

- Whether Anthropic material adds enough beyond OpenAI/GitHub docs for Prompt
  05.

### Agentless / SWE-agent

Most useful extraction:

- Localize, edit/repair, and validate with tool feedback.

Strongest behavior pressure:

- Find the relevant seam before editing and let command output steer only
  in-scope fixes.

Likely research-only material:

- ACI, benchmark, leaderboard, and framework terminology.

Open question:

- Whether `localize-repair-validate` is a useful leading word or should be
  compressed into ordinary verbs.

## 11. Handoff To Triage

Strongest extracted leading words:

- `tracer bullet`
- `one self-contained change`
- `vertical slice`
- `support slice`
- `one concept`
- `reviewable change`
- `file spread`
- `success criteria`
- `localize-repair-validate`
- `tool feedback`

Strongest behavior rules:

- Lock one behavior/support proof, likely touched areas, validation target, and
  non-goals before editing.
- Keep code, proof, and rationale together for one self-contained change.
- Treat layer-only work as support unless it proves an observable behavior path.
- Choose one required variation/path and record non-required adjacent work.
- Stop/split/ask when a second independent concept appears.
- Treat broad file spread as a re-bound signal.
- Keep validation failures inside the slice; record or ask about adjacent
  failures.
- Do not justify bounded slices by guaranteed speed.

Strongest evidence gates:

- The final diff can be summarized as one concept with one proof story.
- Related proof travels with the diff and would catch the promised behavior
  being wrong.
- Every touched file/area has an in-scope reason.
- The selected behavior/support outcome is proven through the highest useful
  path.
- The final note gives rationale, validation, skipped checks, residual risk,
  and follow-ups without relying on hidden scratch context.

Extraction gaps:

- Strong empirical support is concentrated in code review, not product slicing.
- Walking skeleton needs careful triage so it remains conditional.
- Support-slice language needs a concise honesty gate.
- Agentic papers add useful action staging, but their framework vocabulary
  should probably not survive into runtime text.

Promising but uncertain source material:

- Reinertsen batch-size economics, Cockburn primary walking-skeleton material,
  SPIDR split patterns, and Elephant Carpaccio were not promoted in Prompt 03
  and remain outside this extraction.
- Specification by Example may be stronger for Facet 5 Semantic Proof than this
  bounded-slice facet.

Prompt 05 should triage first:

- Whether `tracer bullet`, `one self-contained change`, or `bounded slice` is
  the primary runtime leading word.
- Whether `support slice` belongs in runtime as a named escape hatch for docs,
  config, tests, refactors, and harness work.
- Which stop/split rule is crispest: second concept, proof outside slice, file
  spread, or missing success criteria.
- Which evidence gates should stay in Facet 1 versus move to Semantic Proof,
  Review And Lock, or the engineering contract.
