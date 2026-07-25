# Writing Great Skills Deploy Research

## Research contract

- **Question:** Which methods, vocabulary, conditions, and alternatives best
  support the settled intended behavior in M0 for `writing-great-skills`?
- **Caller use:** Prompt 2 H1 admission.
- **Fixed point:** repository `HEAD`
  `55dd6818182caf75e85de713a13ed76996336a27`; online sources inspected
  2026-07-24.
- **M0 identity:** `sha256-canonical-json-v1`
  `49d8890b655be04129baf67ad729e031fd926d9bd3d332c5bb4dc9cf271a2f03`.
- **Scope:** professional methods, vocabulary, conditions, alternatives,
  counterpressure, and limits for M0-U01 through M0-U09.
- **Exclusions:** changing M0, choosing exact runtime wording, claiming that
  research proves behavioral effect, and changing synthesis, runtime,
  relationships, evaluations, installation, or Git state.
- **Note authority:** create or update only this file.
- **Return owner:** Deploy Campaign root.

## Blind independent discovery

This section was written before opening any upstream checkout, the repository's
canonical target package, target synthesis, historical candidate conclusion,
experimental candidate, or prior behavioral evaluation conclusion.

### Independent source registry

| ID | Source identity and inspected locator | Authority and access depth | Freshness | Limits |
| --- | --- | --- | --- | --- |
| I1 | OpenAI Academy, [Using skills](https://openai.com/academy/skills/), “What are skills?”, “What’s a SKILL.md file?”, and design tip | OpenAI first-party product guidance; full relevant HTML sections | Published 2026-04-10; checked 2026-07-24 | Introductory guidance, not a controlled behavioral study |
| I2 | Anthropic, [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), “How Skills work” levels 1–3 and security considerations | Vendor documentation for an Agent Skills implementation; full relevant HTML sections | Live page checked 2026-07-24 | Claude-specific mechanics do not establish Codex-equivalent behavior |
| I3 | Anthropic Engineering, [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), metadata and progressive-disclosure discussion | First-party practitioner account; full relevant article | Published 2025; checked 2026-07-24 | Describes pack architecture and practice, not causal efficacy |
| I4 | Anthropic Engineering, [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), definitions, grader types, regression/capability distinction, coding and research-agent sections | Identifiable first-party practitioner guidance based on Anthropic and customer work; full relevant HTML sections | Published 2026-01-09; checked 2026-07-24 | Practice synthesis, not a randomized study; examples are illustrative |
| I5 | OpenAI, [A shared playbook for trustworthy third-party evaluations](https://openai.com/index/trustworthy-third-party-evaluations-foundations/), claim/harness matching and validity hazards | First-party evaluation guidance; full relevant HTML sections | Published 2026; checked 2026-07-24 | Focused on third-party capability and safeguard evaluation; adaptation to skill wording is an inference |
| I6 | OpenAI, [How evals drive the next chapter in AI for businesses](https://openai.com/index/evals-drive-next-chapter-of-ai/), “Measure” and “Improve” | First-party evaluation guidance; full relevant HTML sections | Published 2025-11-19; checked 2026-07-24 | Business-oriented synthesis rather than a controlled methods paper |
| I7 | Liu et al., [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172), abstract and §§2–5 | Primary empirical paper; full HTML paper inspected | arXiv 2023, TACL 2024; checked 2026-07-24 | Tested retrieval and multi-document QA on older models, not skill instructions |
| I8 | Jang, Ye, and Seo, [Can Large Language Models Truly Understand Prompts? A Case Study with Negated Prompts](https://proceedings.mlr.press/v203/jang23a.html), abstract and paper identity | Peer-reviewed workshop paper; abstract/metadata inspected, not the full PDF | Published 2023; checked 2026-07-24 | Older model families and task formulations; insufficient by itself for a universal positive-framing rule |
| I9 | Parnas, [On the Criteria To Be Used in Decomposing Systems into Modules](https://doi.org/10.1145/361598.361623), abstract | Seminal primary software-design paper; abstract inspected | Published 1972; checked 2026-07-24 | Supports information-hiding decomposition generally, not agent-instruction ownership directly |
| I10 | Google Engineering Practices, [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html), “Why Write Small CLs?” and “What is Small?” | Identifiable practitioner standard; full page inspected | Live page checked 2026-07-24 | Applies to code changes and reviewability, not semantic skill coverage |
| I11 | IETF, [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/info/rfc9457/), abstract and status | Governing standard for machine-readable error details; standard identity and abstract inspected | RFC published 2023; checked 2026-07-24 | Supports typed error payloads only by analogy; does not define agent Returns or partial status |

### Blind findings and counterpressure

| Intended behavior | Source claim and label | Method classification | Applicability, alternative, and consequence for H1 |
| --- | --- | --- | --- |
| M0-U01 precise implicit entry | **Direct:** I1 says a skill's name and description help ChatGPT recognize relevance. **Direct:** I2 says a description match triggers loading. **Corroborated:** the two vendors independently place discovery responsibility in metadata. | `independently-supported` | Keep the description as an observable “what and when” predicate. This supports testing positive and closest negative cases. It does **not** support keyword stuffing, an explicit-name-only trigger, or a body summary. Alternative: explicit-only invocation where a human must select use; no independent evidence yet decides that product policy for this local skill. |
| M0-U03/U04 bounded ownership and coverage | **Direct:** I9 reports that effective modularization depends on decomposition criteria and that information hiding improves flexibility and comprehensibility. **Direct:** I10 recommends one self-contained minimal change because smaller changes are easier to review, reason about, test, and roll back. **Synthesis:** one owner per behavior and a bounded affected-surface ledger adapt these principles to skill semantics. | `independently-supported` for bounded, self-contained change and information-hiding decomposition; `unverified` for the exact local coverage labels | Retain ownership and mutation boundaries, but treat `affected/preserve/owned elsewhere/historical evidence/drift/not applicable` as local vocabulary unless later independent support appears. Counterpressure: changes split too finely can obscure cross-surface coherence; “self-contained” is the controlling condition, not smallest line count. |
| M0-U05/U06 common-path locality and conditional disclosure | **Direct:** I2 and I3 describe staged metadata → instructions → resources loading and say resources enter context only when needed/referenced. **Direct:** I7 finds material position and added distractors can degrade long-context use. **Inference:** keep must-have common behavior in the loaded body and place branch-only reference behind a precise pointer. | `independently-supported` under the condition that disclosed material is optional or reliably retrievable; the exact common-path/branch test remains an inference to verify locally | Admit progressive disclosure and pointer testing. Counterpressure: disclosure can hide essential rules; I7 shows context position matters but does not prove that shorter is always better, and some evaluated models were robust on synthetic retrieval. Alternative: inline essential content and disclose only specialized branches; if pointer firing is unreliable, improve the pointer or restore content inline. |
| M0-U07 behavior-preserving cuts | **Direct:** I7 contradicts “more context is harmless” by showing distractors and position can impair use. **Direct:** I10 supports minimal self-contained changes, not deletion for its own sake. **Synthesis:** remove a clause only when behavior, authority, safety, proof, Return, and completion remain covered. | `independently-supported` for reducing irrelevant context and preserving a self-contained unit; `unverified` for any universal no-op detector | Retain a clause-to-behavior cut audit. Reject word-count targets and “shorter is automatically better.” Alternative: preserve deliberate repetition or redundant guardrails when direct controls show they change behavior. |
| M0-U08 claim-matched proof | **Direct:** I4 distinguishes deterministic, model, and human graders; names each trial, transcript, and outcome; recommends multiple trials because outputs vary; and separates capability from regression suites. **Direct:** I5 says controlled comparisons keep tasks, scoring, budget, and harness fixed and names contamination, shortcuts, broken tasks, and harness effects as validity hazards. **Direct:** I6 calls for realistic environments, golden sets, edge cases, domain-expert audits, and ongoing maintenance. | `independently-supported` | Admit fixed comparable controls, repeated trials, realistic tasks, outcome/trace grading matched to the claim, and regression checks. Structural parsing is valid for exact bytes/schema/links; it cannot prove wording changes agent behavior. Counterpressure: a fixed shared harness supports comparison, while strong-elicitation claims may require system-specific harnesses; report which claim is being made. |
| M0-U09 typed Return and completion | **Direct:** I1 says a typical skill defines required output format and final checks before completion. **Direct:** I4 distinguishes transcript claims from verified end-state outcomes. **Inference:** require a typed `complete`/`partial`/`blocked` Return whose evidence and residual conditions match the observed state. | `independently-supported` for explicit outputs, final checks, and outcome verification; `unverified` for the exact three-status vocabulary | Keep checkable completion and state/evidence read-back. Treat the exact status names as local contract language. Alternative: external executable completion gates are stronger than prose for machine-verifiable state; use them where available rather than relying on self-report. |
| Positive-target-first wording | **Direct but narrow:** I8 studies failures on negated prompts. No inspected independent source establishes the stronger universal claim that merely naming a forbidden behavior activates it. | `contested` as a universal mechanism; `independently-supported` only as a cautious clarity heuristic paired with explicit guardrails | Do not admit “negation activates behavior” as fact. H1 may prefer a positive target because it states the desired action, while retaining necessary prohibitions and testing the exact wording. |
| Compact “leading words” that recruit pretrained behavior | No blind source directly establishes that repeating a compact concept reliably recruits a stable latent behavioral program across Codex runs. I7 instead warns that placement and context interactions vary. | `unverified` | Any proposed leading word must be a clearly labeled local experiment with M0-first controls. Reject claims of free, universal steering or transfer across models. |
| Premature completion caused by visible later steps | No blind source directly establishes the proposed causal mechanism. I1 supports final checks and I4 supports end-state grading, but neither shows that hiding later steps prevents early stopping. | `unverified` | Sharpening a checkable completion gate is supported; context-boundary splitting specifically to hide later work is experimental and should be admitted only after an observed defect and comparative test. |

### Blind alternatives and rejected lanes

- **Explicit-only selection instead of implicit discovery:** credible when human
  judgment must control invocation, but it conflicts with M0's settled implicit
  entry requirement for this skill and therefore is not an H1 replacement.
- **Inline everything:** protects availability but increases distractors and
  long-context exposure. Retain only for must-have common behavior or after a
  pointer fails a representative loading test.
- **Disclose almost everything:** reduces initial context but can hide authority,
  safety, Return, or completion. Rejected for common-path obligations.
- **Structure-only validation:** cheap and reproducible for bytes, schemas,
  links, and ownership pointers; rejected as evidence that wording changes
  judgment or action.
- **Single impressive sample:** rejected because stochastic outputs require
  repeated trials and because harness, task, and scoring identity affect the
  supported claim.
- **Popularity or repeated pack usage:** rejected as professional evidence;
  repetition can establish shared lineage or convention only.
- **Universal “positive prompts only” rule:** rejected. Necessary negative
  safety and authority guardrails remain, paired with the desired safe action.

### Blind gap state

Blind discovery supplies decision-ready support for invocation metadata,
progressive disclosure under explicit conditions, bounded changes,
claim-matched evaluation, and checkable completion. Exact local vocabulary,
leading-word effects, a universal no-op test, the proposed visible-later-step
mechanism, and exact Return status names remain unverified rather than
load-bearing evidence gaps. Pack and current-runtime inspection may reveal
mechanics requiring targeted verification.

## Pack and current-runtime observations

### Checked-out upstream identity and access

No fetch was performed. Each checkout was clean and its local `HEAD` equaled
its existing `origin/main` tracking ref when inspected; this proves the supplied
checkout identity, not equality with the live network remote on 2026-07-24.

| Upstream | Revision and worktree | Access depth and files inspected | Observed behavior relevant to M0 | Limits |
| --- | --- | --- | --- | --- |
| Matt Pocock Skills, `https://github.com/mattpocock/skills.git` | `ed37663cc5fbef691ddfecd080dff42f7e7e350d`; commit date 2026-07-21; clean | Complete `skills/productivity/writing-great-skills/` package: `SKILL.md`, `GLOSSARY.md`, `agents/openai.yaml` | Defines predictability, invocation load tradeoffs, description branches, information hierarchy, progressive disclosure, co-location, leading words, completion/legwork/post-completion mechanics, single source of truth, relevance, no-op, and negation. It is explicit-only in OpenAI metadata. | Primary evidence only for what this pack says. No behavioral tests were present in this package. The general leading-word, visible-later-step, universal no-op, and negation mechanisms do not gain independent support merely because the pack states them. |
| Superpowers, `https://github.com/obra/superpowers.git` | `d884ae04edebef577e82ff7c4e143debd0bbec99`; tag `v6.1.1`; commit date 2026-07-02; clean | `skills/writing-skills/SKILL.md`, `testing-skills-with-subagents.md`, `persuasion-principles.md`, `anthropic-best-practices.md`; graph/example/support files were inventoried | Treats skill authoring as RED-GREEN-REFACTOR: observe a no-guidance failure, add minimal failure-shaped guidance, retest, and close observed rationalizations. Its description rule favors triggering conditions without workflow summaries. It distinguishes discipline, output-shape, omission, and conditional failures and assigns different instruction forms. | Pack-specific procedure and rhetoric (“Iron Law”, “bulletproof”, “100% compliance”) are not efficacy evidence. The bundled Anthropic guidance conflicts with the pack's “when only” description rule by requiring both what and when. Pressure fixtures can test a bounded discipline failure but cannot establish broad prevalence or universal compliance. |
| Ponytail, `https://github.com/DietrichGebert/ponytail` | `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`; commit date 2026-07-15; clean | All six `skills/ponytail*/SKILL.md` files; `benchmarks/behavior.yaml`; benchmark README inspected only for harness/metric descriptions, with reported outcomes excluded from this packet; result files not opened | Uses a broad, exclusion-bearing description; an ordered “first rung that holds” selection ladder; explicit safety exceptions; a one-runnable-check floor; distinct one-shot/read-only skills and output contracts; a behavior-present/absent control configuration. | It concerns code minimization, not skill semantics. A selected three-probe behavior gate is not comprehensive, one runnable check is only a floor, and pack benchmark claims are not independent professional evidence or target behavioral proof. |

### Current canonical target

The complete canonical package at fixed point
`55dd6818182caf75e85de713a13ed76996336a27` was inspected after the blind note
was frozen:

| File | SHA-256 | Observation |
| --- | --- | --- |
| `skills/custom/writing-great-skills/SKILL.md` | `dd9cc9fa91dacfbeaddb73a82488ff9dcb921f4e7626cb9e12beb2c1cefff2ee` | Adds explicit Audit/Author authority, bounded coverage, ownership, claim-matched proof, typed Return, and completion to a compressed form of Matt's authoring mechanics. Its description states behavior, observable request classes, and close exclusions. |
| `skills/custom/writing-great-skills/GLOSSARY.md` | `7e513d1d2ae38f99c61c748830b0bb81a9f47707231e20fdb9a07dbcc164c274` | Owns the local Codex-adapted invocation, hierarchy, steering, and pruning vocabulary. The installed required copy matched byte-for-byte. |
| `skills/custom/writing-great-skills/BEHAVIOR-EVALS.md` | `1165ded49b26b40fd358d768e2c724fef398fe0d30ffb9dd15b0cd7258dee950` | Registers defect-correction or quality-lift before sampling; requires fixed contexts, a no-candidate control, fresh contexts, at least five samples, positive/wrong-condition cohorts, explicit rubrics, separate conditional efficacy, and terminal decisions. |
| `skills/custom/writing-great-skills/agents/openai.yaml` | `8619a54e8c098122a7f3881394f84ca89b684366e848233a29ad18b6ec363935` | Enables implicit invocation. |

Current equals M0 in intended behavioral scope only provisionally; exact runtime
identity belongs to Prompt 2. Research does not promote current wording by
existence. The current package nevertheless shows that M0 did not omit an
essential behavior needed to express its settled intent.

### Historical local language packets

The applicable historical packets were used only as source intake and checked
against the supplied upstream revisions:

| Packet | Identity/use | Disposition |
| --- | --- | --- |
| `docs/research/language/matt-pocock-skills-vocabulary.md` | Packet revision names `ed37663`; targeted clusters, retained terms, techniques, collisions, gaps, and source trace inspected | `historical-admission-only`. It accurately locates the upstream authoring lexicon and explicitly says the source tree has no behavioral tests. It cannot supply independent efficacy or current target proof. |
| `docs/research/language/superpowers-skill-pack-vocabulary.md` | Packet revision names `d884ae04`; skill-authoring/pressure, retained terms, technique, conflicts, gaps, and trace sections inspected | `historical-admission-only`. It usefully records the description-rule conflict, pack-specific “bulletproof” limits, and absent external eval repository. |
| `docs/research/language/ponytail-skill-pack-vocabulary.md` | Packet revision names `16f2980`; minimum-solution, evidence, retained terms, collisions, gaps, and trace sections inspected | `historical-admission-only`. It separates behavior gates from structural checks and warns that benchmark labels require their scorer and baseline. Reported benchmark outcomes were not admitted. |

## Targeted independent verification after pack inspection

Supplemental source identities, all checked 2026-07-24:

| ID | Source identity and access | Authority | Material limit |
| --- | --- | --- | --- |
| T1 | Agent Skills, [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions), complete live guide | Governing open-standard project authoring guidance | Suggested query/run counts are starting heuristics, not statistical sufficiency |
| T2 | Agent Skills, [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices), complete live guide | Governing open-standard project authoring guidance | Practitioner guidance; some statements report experience rather than controlled effects |
| T3 | OpenAI Help Center, [Best practices for prompt engineering with the OpenAI API](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api), rules 6–8 | OpenAI first-party prompt guidance | “Leading words” example is syntactic code completion, not a general Leitwort study |
| T4 | He et al., [Is Progressive Disclosure All You Need for Long-Context Agents?](https://arxiv.org/abs/2607.17598), v1 abstract and study summary | Primary controlled preprint submitted 2026-07-20 | Four-day-old preprint on long-document QA, not procedural skill semantics |
| T5 | NIST AI 800-3, [Expanding the AI Evaluation Toolbox with Statistical Models](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-3.pdf), February 2026, pp. 9–17 and conclusions | Current NIST evaluation methods report | Statistical treatment centers benchmark accuracy; small agent suites may need a different model |
| T6 | NIST/SEMATECH, [Randomized block designs](https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm), complete page | Governing experimental-design handbook | Application to instruction-wording trials is an explicit inference |
| T7 | GraphQL, [October 2021 Specification](https://spec.graphql.org/October2021/), §§6.4.4 and 7.1–7.1.2 | Governing open specification | Partial-data semantics apply only by analogy to independently useful agent results |
| T8 | Rust `std` 1.97.1, [`std::result`](https://doc.rust-lang.org/stable/std/result/index.html), overview and “Results must be used” | Current standard-library documentation, built 2026-07-14 | Binary success/error cannot itself represent partial completion |

| Observed mechanic | Verification and source claim label | Classification | Consequence for H1 |
| --- | --- | --- | --- |
| Descriptions carry invocation and require positive/negative trigger coverage | **Direct:** Agent Skills [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) says description is the primary trigger, recommends intent-focused imperative wording, realistic should-trigger and near-miss should-not-trigger queries, repeated trials, and fixed train/validation splits. **Direct:** OpenAI Academy I1 says name and description help ChatGPT recognize relevance. | `independently-supported` | Preserve the current observable behavior classes and closest exclusions. Prefer a mixed positive/near-miss trigger suite over adding synonyms. Superpowers’ “when only” rule is too strong: the governing guide's own improved example describes both what and when. |
| Common-path locality and conditional pointers | **Direct:** Agent Skills [Best practices](https://agentskills.io/skill-creation/best-practices) says keep core instructions needed every run in `SKILL.md`, put detailed conditional content in references, and state when each file is loaded; it warns that non-obvious gotchas may need to stay inline. **Direct counterpressure:** He et al. [Is Progressive Disclosure All You Need for Long-Context Agents?](https://arxiv.org/abs/2607.17598) finds one-level disclosure helps at multi-book scale but gives near-zero gain under a strong retriever, while a second routing level never helped and sometimes hurt accuracy. | `independently-supported`, conditional and shallow | Keep M0's common-path/branch distinction and pointer checks. Do not encode disclosure as a universal token-saving win or deepen the package without evidence. Required authority, safety, proof, Return, and completion stay inline. |
| No-op/cut test | **Direct:** Agent Skills Best Practices asks whether the agent would get an item wrong without the instruction; if no, cut it, and if unsure, test. **Direct counterpressure:** the same source says non-obvious gotchas belong inline and warns against skills scoped so narrowly that several must load and conflict. | `independently-supported` as a comparative test, not an intuition verdict | Keep the behavior-change question and current control gate. Reject upstream's aggressive sentence deletion as a universal rule; safety, authority, compatibility, and observed gotchas survive unless comparative evidence shows they are inert. |
| Positive target before necessary prohibition | **Direct:** OpenAI [Prompt engineering best practices](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api) recommends saying what to do instead of only what not to do; its improved example retains a constraint and supplies the safe alternative. **Direct counterpressure:** Agent Skills Best Practices gives “never output PII” and “Do not modify the command” as valuable constraints for fragile work. | `independently-supported` as positive-target-first plus guardrail; `contested` as “negation itself activates the behavior” | Preserve current paired guardrails. Do not admit the glossary's causal “prohibition activates” explanation as established fact. Superpowers' failure-shaped instruction taxonomy is a useful local hypothesis, not a universal law. |
| Leading words recruit useful priors | **Direct but narrow:** OpenAI Prompt Engineering calls syntactic starters such as `import` and `SELECT` “leading words” that nudge code generation toward a known form. No inspected source supports the broader claim that repeating a conceptual Leitwort reliably anchors invocation and execution across Codex tasks. | `independently-supported` for explicit syntactic starters; `unverified` for general conceptual prior recruitment | Retain the term only as local vocabulary and treat any new conceptual leading word as a candidate-owned experiment. Do not claim token-free or model-general steering. |
| Completion checklists and validation loops | **Direct:** Agent Skills Best Practices recommends explicit checklists, validator/fix/repeat loops, and “only proceed when validation passes.” **Direct:** OpenAI Academy I1 names final checks before completion. | `independently-supported` | Preserve checkable completion and read-back. Prefer executable state checks where possible; a prose claim alone does not establish completion. |
| Visible post-completion steps cause premature completion; hiding them fixes it | No inspected independent source isolates this causal mechanism. The disclosure study concerns long-document retrieval, not between-step rushing. Checklists can even keep later steps visible while helping avoid omissions. | `unverified` | Preserve the current guarded form only as a local experiment: sharpen the criterion first; consider a real context split only after an observed persistent early-stop defect; test against M0. |
| No-guidance baseline, one-change candidate, fixed task/context, and fresh trials | **Direct/inference:** NIST randomized-block guidance says hold nuisance factors constant while varying the factor of interest and randomize remaining nuisance effects. **Direct:** OpenAI I5 says controlled comparisons keep tasks, scoring, budget, and harness fixed and report contamination/validity hazards. **Direct:** Anthropic I4 says trials vary, calls for repeated trials, and distinguishes transcript from outcome. | `independently-supported` | Preserve current control isolation, fresh contexts, fixed inputs, and arm randomization. Keep candidate language and authoring rationale away from controls and judges. |
| Fixed minimum sample count and variance judgment | **Direct counterpressure:** NIST [AI 800-3](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-3.pdf) says LLM metrics are uncertain estimates, even zero-temperature runs are not fully deterministic, comparisons require uncertainty reasoning, and prompt-template effects limit generalization. Agent Skills description guidance calls three runs only a starting point. | `contested` if five samples are treated as sufficient proof; `independently-supported` if five is only a floor followed by variance/decision-threshold extension | H1 should make the stopping decision depend on uncertainty and decision margin, not “five” alone. Five may remain a cheap minimum for defect visibility, but a narrow sample cannot justify prevalence or cross-model transfer. |
| Structural proxies versus behavioral claims | **Direct:** Anthropic I4 says code/string/static graders are objective but brittle and limited for nuance; it favors end-state outcomes plus appropriate transcript/rubric checks. **Direct:** NIST AI 800-3 limits inference to the tested template when wording/format is systematic. | `independently-supported` | Preserve the current structural/behavioral boundary and residual transfer-gap reporting. Exact hashes prove bytes; ownership traces prove relationships; only comparable task outcomes support wording-effect claims. |
| Typed `complete`/`partial`/`blocked` Return | **Direct by analogy:** RFC 9457 standardizes machine-readable error details; GraphQL's October 2021 specification distinguishes request failure from partial data with errors; Rust `Result` distinguishes success and recoverable error. None defines agent returns. | `independently-supported` for distinguishable terminal states and useful failure payloads; exact vocabulary is `pack-specific`/local | Keep exact local status names because M0 and caller contracts own them, not because outside sources require them. Partial is valid only when the retained result remains independently useful and its missing coverage is explicit. |

## Decision-ready method classifications

| Proposed method or vocabulary | Classification | Conditions, alternatives, and H1 disposition |
| --- | --- | --- |
| Description as observable “what and when” routing predicate, with closest exclusions | `independently-supported` | Admit. Test realistic positives and adjacent near-misses in repeated fresh trials; avoid synonym lists that rename one behavior. |
| One owner for authority, behavior, evidence, failure Return, and completion | `independently-supported` by modularity/responsibility analogy and local contract | Admit as local application. Alternative is explicit shared ownership, but it requires a coordination protocol and is not indicated by M0. |
| Bounded affected-surface ledger | `independently-supported` for one self-contained change; exact labels are local | Admit the method; retain the established local labels rather than importing another taxonomy. |
| Shallow progressive disclosure with common obligations inline | `independently-supported` | Admit under actual load conditions and pointer tests. Reject deep routing and “disclose everything” defaults. |
| Co-location of definition, rule, and caveat | `independently-supported` by information-hiding/coherence practice; direct skill-specific causal effect not isolated | Admit as low-risk structure; do not overclaim performance. |
| Clause-to-behavior cut audit/no-guidance comparison | `independently-supported` | Admit. Preserve non-intuitive gotchas and protected contracts; compare before removing uncertain clauses. |
| “Leading word” as a compact conceptual prior | `unverified` beyond syntactic starters | Local experiment only, with a registered M0 weakness and comparative proof. No new leading word should enter H1 solely for elegance. |
| Positive target first, necessary prohibition paired with safe action | `independently-supported` | Admit. Reject the stronger causal pink-elephant explanation as established evidence. |
| Failure-shaped guidance taxonomy (discipline/shape/omission/condition) | `pack-specific` with partial independent support | Candidate experiment. It fits current diagnosis but requires task-specific controls; Superpowers' pressure/rationalization form should not be generalized to every skill. |
| Sharpen completion before splitting context | `independently-supported` for checkable validation; split mechanism `unverified` | Admit the sharpen-first gate. Defer splitting unless a persistent defect is observed. |
| Candidate controls with fixed tasks, rubrics, harness, budgets, fresh contexts, randomized order, and held-out trigger cases | `independently-supported` | Admit. Add uncertainty-aware stopping and report the tested system identity. |
| At least five samples as sufficient evidence | `contested` | Keep only as a minimum floor if Prompt 2 couples it to uncertainty, material variance, and decision margin. Reject extrapolation from sample count alone. |
| Exact Return statuses and coverage labels | `pack-specific`/local contract | Preserve; they are interoperability obligations, not professional universals. |

## Intent-adjacent candidates for Prompt 2

1. **Trigger-validation candidate**
   (`near-miss trigger suite -> fewer false entries/misses -> current description
   may be semantically precise but behaviorally unproved -> repeated held-out
   positive/adjacent-negative invocation gate -> fixed current versus candidate
   description comparison`). The method is `independently-supported`; exact
   wording remains candidate-owned.
2. **Uncertainty-aware evidence candidate**
   (`uncertainty/decision margin -> resist five-sample overclaim -> current
   protocol extends only for material variance/borderline results but does not
   require an uncertainty statement -> per-arm uncertainty and stop rationale
   gate -> compare admissibility decisions on fixed campaigns`). The method is
   `independently-supported`; no universal sample count is proposed.
3. **Failure-form candidate**
   (`match form to failure -> avoid blanket prohibitions or prose reminders ->
   current diagnosis table already approximates the method -> registered
   defect plus one-change comparative gate -> M0-first behavior test`). This is
   `pack-specific` with partial independent support and should be admitted only
   as a labeled local experiment if Prompt 2 finds a live gap.
4. **Leading-word candidate**
   (`compact conceptual term -> proposed stable recruitment -> no demonstrated
   M0 weakness or independent general support -> syntactic/behavioral
   comparative gate`). Disposition: `unverified`; do not admit without an
   observed control deficit.
5. **Context-split candidate**
   (`hide later steps -> proposed reduction in premature completion -> no
   isolated independent support -> persistent early-stop defect after a sharper
   criterion plus context-boundary comparison`). Disposition: `unverified`;
   defer unless the entry predicate is observed.

## Conflicts, gaps, and rejected lanes

- **No intent conflict:** no inspected evidence shows that M0 omitted behavior
  essential to its settled intent. The exact affected intent unit is therefore
  `none`; an `intent-reopen` is not warranted.
- **Description conflict:** Superpowers says descriptions should contain only
  “when”; OpenAI and the Agent Skills guide say descriptions convey what and
  when. Prefer the governing/product guidance and behavior tests.
- **Disclosure conflict:** vendor guidance favors staged loading, while the
  2026 controlled preprint finds benefits depend on corpus and harness and that
  deeper routing can hurt. Preserve shallow conditional disclosure, not a
  universal maxim.
- **Negation conflict:** positive alternatives are supported, but necessary
  negative safety/authority constraints are also endorsed. Reject
  positive-only editing.
- **Evaluation conflict:** fixed prompts improve internal causal isolation but
  narrow external validity. Report exact tested phrasing and include held-out
  variants when the claim reaches beyond one prompt.
- **Sample-count gap:** no universal five-run threshold exists. This is a
  disclosed H1-method qualification, not a blocker, because the current
  protocol already permits extension and Prompt 2 can decide whether to make
  uncertainty explicit.
- **No conversation needed:** published evidence resolved every material
  operational condition sufficiently for H1 admission; no practitioner
  conversation was conducted.
- Rejected lanes: popularity, upstream repetition, historical result tables,
  generic prompt-tip lists without source ownership, word-count targets,
  universal “bulletproof” claims, and line-count reduction as semantic quality.

## Stopping basis and caller boundary

Decision saturation is reached. Every M0 cluster has a classified method; the
strongest accessible governing/product sources, primary counterpressure, and
the three named upstream revisions were inspected; newly observed pack
mechanics were independently checked or explicitly left unverified. Additional
credible sources were repeating the same qualifications and were unlikely to
change a method, condition, classification, or H1 candidate.

Research status is `answered`: all load-bearing claims needed for H1 admission
are supported. Unverified leading-word and context-split ideas are disclosed
candidate dispositions, not evidence gaps. This packet recommends Prompt 2 but
does not authorize it, choose H1 wording, change runtime, or claim behavioral
effect.

Return owner: Deploy Campaign root.
