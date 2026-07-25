# Writing Great Skills deploy research packet

<!-- research-packet:start -->

## Research contract

- **Status:** answered (`research-complete`)
- **Question:** Which independently supported methods, conditions, alternatives,
  failure modes, and counterpressure best support the frozen M0 behavior, with
  particular attention to the hypothesis that missed must-have branch material
  should first receive a sharper pointer naming target, trigger, and action,
  while inlining is reserved for a fresh observed failure of that repaired
  pointer?
- **Caller use:** evidence input for Prompt 2 of campaign
  `2026-07-24-writing-great-skills-7d0da40`; this note does not select H1,
  change M0, or prove wording efficacy.
- **Fixed point:** Git `7d0da40a218114aa138265557ea2454361dcd147`;
  M0 checkpoint
  `.scratch/deploy-campaigns/2026-07-24-writing-great-skills-7d0da40/m0-checkpoint.json`,
  verified SHA-256
  `33b6bb9b9e4a5571f92552ada39870588b4272a62d4111bfaef0b1b00c8d0aac`.
- **Scope:** invocation predictability; semantic ownership and information
  hierarchy; behavior-preserving compression; claim-matched evaluation; safe
  authority, Return, and completion.
- **Exclusions:** local intent revision, runtime wording, M0/H1 construction,
  efficacy proof, installation, Git delivery, and the reserved incumbent
  reconciliation record.
- **Note authority:** create only this file.
- **Freshness:** online sources checked 2026-07-24.
- **Return owner:** Deploy Campaign coordinator for `writing-great-skills`.

## Blind independent discovery

This section was recorded before inspecting Matt Pocock, Superpowers,
Ponytail, the current canonical `writing-great-skills` package, applicable
local language packets, or prior campaign conclusions. The intended-behavior
facets came only from the verified M0 checkpoint.

### Discovery log

| Lane | Search terms | Strongest owner inspected | Counterpressure sought |
| --- | --- | --- | --- |
| Skill invocation and disclosure | `agent skills specification progressive disclosure references description` | Agent Skills specification and creation guidance | Over-broad descriptions, excessive always-loaded detail, and deep reference chains |
| Pointer clarity | `descriptive link text target condition before instruction` | Google developer documentation style guide and W3C WCAG link-purpose guidance | Cross-references that are vague or force irrelevant loading |
| Semantic ownership | `Parnas information hiding modules criteria decomposition original paper` | Parnas, *On the Criteria to Be Used in Decomposing Systems into Modules* | Decomposition overhead and the risk of hiding needed context |
| Behavioral evaluation | `agent evaluation controlled comparison contamination blind grading harness` | OpenAI evaluation-method publications | Harness effects, contamination, reward hacking, broken tasks, and transfer limits |
| Authority and safe completion | `NIST AI RMF roles responsibilities human oversight fail safely residual risk` | NIST AI RMF 1.0 Core | Context-dependent applicability and the limits of voluntary governance guidance |

### Independent findings before pack inspection

1. **Conditional progressive disclosure is independently supported for
   task-specific resources.** The Agent Skills specification defines three
   loading tiers—metadata, activated instructions, and resources loaded as
   needed—and recommends focused reference files and shallow reference chains
   ([specification](https://agentskills.io/specification#progressive-disclosure)).
   Its authoring guidance makes the operational condition explicit: naming the
   file and the condition that requires it is more useful than a generic
   “see references” pointer
   ([best practices](https://agentskills.io/skill-creation/best-practices#structure-large-skills-with-progressive-disclosure)).
   This directly supports `target + trigger + load/read action`; it does not
   establish that any particular model will follow one exact sentence.

2. **Pointer purpose should be understandable at the decision point.** Google’s
   technical-writing guidance says to use descriptive link text and place
   conditions before instructions
   ([style highlights](https://developers.google.com/style/highlights)).
   W3C’s link-purpose guidance likewise requires the purpose to be determinable
   from the link text or its immediate context
   ([WCAG 2.2 understanding 2.4.4](https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html)).
   Applying human documentation guidance to an agent instruction is an
   **inference**, but it independently supports sharpening a weak pointer before
   duplicating its destination.

3. **Inlining everything is not the safe default.** The Agent Skills authoring
   guidance warns that overly comprehensive skills can make relevant material
   harder to extract and trigger unproductive paths, while advising that
   specificity should increase with task fragility
   ([best practices](https://agentskills.io/skill-creation/best-practices#aim-for-moderate-detail)).
   Thus “always inline must-have content” is rejected as a general rule.
   Conditional material may deserve inlining when it is common, safety-critical,
   or a repaired reference is freshly observed to fail, but that last escalation
   condition remains a candidate-specific hypothesis requiring direct proof.

4. **One-owner boundaries have a professional software-design analogue.**
   Parnas argues that decomposition quality depends on the criterion used and
   demonstrates information-hiding modules as a route to comprehensibility and
   changeability
   ([CACM paper and abstract](https://doi.org/10.1145/361598.361623)).
   Mapping that principle from software modules to instruction ownership is a
   **synthesis**, not a claim made by Parnas. It supports keeping foreign
   procedure in its owner while exposing a sufficient local interface.

5. **Wording-effect claims require controlled, claim-matched evidence.**
   OpenAI’s evaluation guidance distinguishes capability, safeguard, and
   controlled-comparison claims; for comparison it calls for fixed tasks,
   scoring, and budget, plus explicit checks for reward hacking, contamination,
   broken tasks, refusals, and evaluation awareness
   ([trustworthy evaluations](https://openai.com/index/trustworthy-third-party-evaluations-foundations/)).
   OpenAI’s GDPval method also uses blind comparison and detailed rubrics, while
   explicitly declining to substitute its less-reliable automated grader for
   experts
   ([GDPval method](https://openai.com/index/gdpval/#how-we-grade-model-performance)).
   These sources support isolated arms, hidden candidate cues, predeclared
   rubrics, sample inspection, and bounded conclusions—not a universal sample
   count or efficacy for this skill.

6. **Authority and completion should expose roles, limits, and residual risk.**
   NIST AI RMF 1.0 calls for documented, differentiated roles and
   responsibilities, contextualized system limits and human oversight,
   deployment-similar performance evidence, safe failure beyond knowledge
   limits, and documentation of residual negative risk
   ([AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)).
   This is independently supportive of explicit mutation authority, typed
   failure, proof limits, and terminal handoff. It is voluntary, organization-
   level risk guidance, so applying it to a repository skill is a bounded
   **inference**, not a requirement.

### Blind provisional answer

The current-compatible repair hypothesis has a sound professional basis as an
ordered experiment:

1. keep branch-only material in its owner;
2. make the pointer name the exact target, the condition that activates it, and
   the action to load or apply it;
3. directly observe whether the repaired pointer retrieves and uses the
   must-have material under an entry-positive task; and
4. inline only the smallest missed behavior if that controlled observation
   still fails or if the branch is no longer truly conditional.

Steps 1–2 are independently supported. Steps 3–4 are a synthesis from
claim-matched evaluation and context-load counterpressure. No source inspected
in the blind phase proves the exact escalation policy or its efficacy for
Codex.

## Post-blind source inspection

### Upstream and current observations

| Source | Identity and worktree | Access depth | Observed behavior and limits |
| --- | --- | --- | --- |
| Matt Pocock Skills | `https://github.com/mattpocock/skills.git`, `ed37663cc5fbef691ddfecd080dff42f7e7e350d`; clean worktree on 2026-07-24 | Target directory `skills/productivity/writing-great-skills/`: complete `SKILL.md` and `agents/openai.yaml`; relevant complete definitions and failure modes in `GLOSSARY.md`. The directory has no scripts or examples. | Defines a “context pointer” as target plus reach condition and states the exact pack rule: sharpen a weak must-have pointer first, then inline only if sharpening fails ([fixed SKILL](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/productivity/writing-great-skills/SKILL.md), [fixed glossary](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/productivity/writing-great-skills/GLOSSARY.md)). This is direct evidence of pack wording, not independent professional support or efficacy. |
| Superpowers | `https://github.com/obra/superpowers.git`, `d884ae04edebef577e82ff7c4e143debd0bbec99`; clean worktree on 2026-07-24 | Complete `skills/writing-skills/SKILL.md`, `testing-skills-with-subagents.md`, `persuasion-principles.md`, `graphviz-conventions.dot`, and `render-graphs.js`; targeted progressive-disclosure, evaluation, and missed-reference sections of `anthropic-best-practices.md`; worked evaluation example inspected. The referenced generic TDD skill was not opened because its procedure is foreign to this bounded question. | Uses baseline-first testing, minimal repairs for observed failures, repeated samples, direct output inspection, and observable predicates. It recommends heavy reference outside the main file but keeps most principles inline. Its claim that descriptions should contain only triggers conflicts with current OpenAI, Agent Skills, and Anthropic guidance that descriptions state both what and when; treat that rule as pack-specific, not general ([fixed skill](https://github.com/obra/superpowers/blob/d884ae04edebef577e82ff7c4e143debd0bbec99/skills/writing-skills/SKILL.md)). Its absolute testing law and exact replication counts are also pack rules, not independently established universal thresholds. |
| Ponytail | `https://github.com/DietrichGebert/ponytail`, `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`; clean worktree on 2026-07-24 | Complete `skills/ponytail/SKILL.md`; benchmark `README.md`, behavior configuration, prompt registry, and the issue-245/217 result inspected. Scripts, all examples, and other historical results were not re-traversed; the applicable whole-tree language packet below supplied historical intake only. | Makes minimization conditional on comprehension and preserves requested behavior, security, accessibility, and data-loss handling as floors ([fixed skill](https://github.com/DietrichGebert/ponytail/blob/16f29800fd2681bdf24f3eb4ccffe38be3baec6b/skills/ponytail/SKILL.md)). Its issue-245 evaluation reports that an operational “grep every caller” directive changed capable-model behavior while smaller-model results stayed near baseline; issue 217 did not reproduce ([fixed result](https://github.com/DietrichGebert/ponytail/blob/16f29800fd2681bdf24f3eb4ccffe38be3baec6b/benchmarks/results/2026-06-22-issue-245-217-comprehension.md)). These are narrow pack-owned observations, valuable as counterpressure against structural or prose-only confidence, not transferable efficacy proof. |
| Current canonical package | Repository HEAD `7d0da40a218114aa138265557ea2454361dcd147`; parent worktree had pre-existing campaign scratch/transcript files and this authorized note | Complete `skills/custom/writing-great-skills/{SKILL.md,GLOSSARY.md,BEHAVIOR-EVALS.md,agents/openai.yaml}` | Already preserves implicit invocation; target-and-condition pointers for both support files; common-inline/branch-only disclosure; claim-matched direct controls; typed Return; and a stop before installation or delivery. The `Load [GLOSSARY.md] when ...` and `load [BEHAVIOR-EVALS.md] ...` clauses already include an action. Current existence proves compatibility only, not M0 authority or efficacy. No omission essential to frozen intent was found. |

### Historical local language intake

The language packets were read only after blind discovery and are
`historical-admission-only`: they preserve vocabulary and source traces but do
not prove current behavior or this campaign’s lifecycle.

- `docs/research/language/matt-pocock-skills-vocabulary.md` at the same Matt
  revision corroborates the pack-specific pointer, hierarchy, completion, and
  pruning vocabulary and explicitly warns that target existence does not prove
  reliable firing.
- `docs/research/language/superpowers-skill-pack-vocabulary.md` at the same
  Superpowers revision preserves hard-gate, control, evaluation, and
  rationalization vocabulary; its missing external `superpowers-evals`
  checkout limits efficacy claims.
- `docs/research/language/ponytail-skill-pack-vocabulary.md` at the same
  Ponytail revision preserves the distinction among correctness, safety,
  completeness, and reduction, and documents narrow benchmark transfer limits.
- `docs/research/language/03-high-signal-steering-words.md` and
  `04-agentic-bridge-vocabulary.md` distinguish professional priors from an
  observable trigger, action, and completion criterion. They are candidate
  language, not current instructions.
- `docs/research/language/upper-bound-engineering-language.md` was not needed:
  it is a broad cross-pack synthesis, while the narrower packets and primary
  sources closed this question.

The prior `writing-great-skills` campaign research note and the reserved
incumbent-reconciliation record were not opened or used.

### Targeted independent verification after pack inspection

The exact Matt wording triggered a narrow verification search rather than
automatic adoption.

- Anthropic’s live skill-authoring guidance says that when an agent misses
  important referenced material, make the link more explicit or prominent,
  then iterate from observed use; when a file is repeatedly read, consider
  moving its content into the main `SKILL.md`
  ([authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#observe-how-claude-navigates-skills)).
  It separately warns that nested references can cause partial reads and
  recommends one-level-deep references. This directly corroborates the repair
  premises and their observation condition.
- Anthropic’s architecture description confirms the cost model: instructions
  bring linked references into context only when accessed, while unused files
  remain out of context
  ([Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work)).
- Agent Skills guidance independently says to name the exact file and the
  activation condition, rather than use a generic pointer
  ([best practices](https://agentskills.io/skill-creation/best-practices#structure-large-skills-with-progressive-disclosure)).
- No independent owner located states the exact universal rule “inline only
  after one sharpened-pointer failure.” The ordered policy is therefore a
  synthesis of the direct repair advice, progressive-disclosure cost model,
  and observed-use escalation—not a quoted standard.

### Source-claim labels

| Retained item | Claim label | Provenance | Limitation |
| --- | --- | --- | --- |
| Staged metadata, instruction, and resource loading | `corroborated` | OpenAI manual, Agent Skills, and Anthropic | Architecture and authoring guidance, not wording efficacy |
| Explicit file target plus observable loading condition | `corroborated` | Agent Skills, Anthropic, Google, and W3C | Google/W3C apply to human documentation; agent-specific sources carry the method |
| Sharpen first, then consider the smallest inline repair after an observed persistent miss | `synthesis` | Anthropic observe-refine guidance plus Agent Skills load counterpressure; Matt supplies the exact pack rule | No independent source states the exact universal order |
| One semantic owner exposed through a sufficient pointer/interface | `inference` | Parnas information hiding plus cross-pack ownership observations | Parnas does not discuss agent skills |
| Fixed-condition, contamination-aware behavioral comparison | `corroborated` | OpenAI evaluation playbook and GDPval method | Exact local sample floors and efficacy remain unproved |
| Matt, Superpowers, and Ponytail mechanics | `direct` | Exact pinned upstream files | Direct only for what each pack says or reports |
| Applying NIST roles, safe failure, and residual risk to a repository skill | `inference` | NIST AI RMF 1.0 | Voluntary organization-level guidance |

## Classifications and answer

### Load-bearing claim ledger

| Claim | Research status | Method class | Evidence, counterevidence, and answer impact |
| --- | --- | --- | --- |
| An implicit skill’s description should state observable scope and closest boundaries concisely. | supported | `independently-supported` | OpenAI’s current manual says implicit matching depends on the description and recommends concise, front-loaded scope and boundaries; Agent Skills provides positive/negative trigger evaluation. Superpowers’ “when only, never what” rule conflicts with OpenAI, Agent Skills, and Anthropic’s “what and when,” so the absolute upstream rule is rejected. Current description is compatible; no H1 need is established. |
| Branch-only material should remain behind a direct conditional pointer when it is not needed on every applicable run. | supported | `independently-supported` | Agent Skills, OpenAI, and Anthropic all describe staged/on-demand resource loading; Agent Skills cautions against deep chains. Counterpressure: overly broad always-loaded detail can bury relevance, while hidden common or critical content can be missed. H1 must preserve the common-versus-conditional decision. |
| A weak must-have pointer should first be repaired to name target, trigger, and load/apply action. | supported | `independently-supported` | Agent Skills gives the exact target-plus-condition form; Google says put conditions before instructions; W3C supports destination purpose at the decision point; Anthropic says missed links should become explicit/prominent. Applying human link guidance to agents is inferential, but the agent-specific sources close the claim. |
| Inlining should be considered only after fresh observation shows the repaired pointer still misses, or evidence shows the material is actually common/repeatedly needed. | supported | `independently-supported` | Anthropic directly supports observe-refine-test, explicit/prominent link repair, and considering main-file placement for repeatedly used content. Agent Skills supplies the context-load counterpressure. Matt states the exact order but has only pack authority. The strict ordering is a bounded synthesis supported as a conservative experiment, not as a universal law or efficacy claim. This is the strongest intent-adjacent H1 candidate. |
| Each behavior or foreign procedure should have one owner exposed through a sufficient interface. | supported | `independently-supported` | Parnas supports information-hiding decomposition for comprehensibility/changeability; applying module boundaries to skill semantics is a bounded inference. Upstream cross-references show the alternative but also demonstrate risks of vague ownership and copied procedure. H1 should not duplicate the glossary or evaluation protocol into the main file. |
| Compression is safe whenever wording becomes shorter. | conflicted | `contested` | Professional and platform guidance favor concise, focused instructions, but Ponytail’s own evidence shows a bare minimal prompt can drop safeguards, and Agent Skills warns that specificity should rise with fragility. The claim is rejected: shorter is a load proxy, not the objective; preserve behavior and safety first. |
| Exact wording changes observable behavior when structural checks pass. | unknown | `unverified` | OpenAI’s evaluation guidance requires claim-matched controlled comparison and validity checks; pack results show model and task dependence. The structural-only claim is rejected: link presence, hashes, or sentence review cannot prove pointer use. Prompt 4 must supply fresh direct controls if Prompt 2 admits the candidate. |
| Fixed tasks, scoring, budgets, hidden candidate cues, baseline deficit, repeated samples, and direct output inspection support a causal wording comparison. | supported | `independently-supported` | OpenAI calls for equivalent conditions and explicit validity checks; GDPval uses blind comparison and detailed rubrics. Exact sample floors remain local protocol choices. Results must stay bounded to tested model, host, task, tools, and runtime. |
| Explicit authority, safe failure, evidence limits, residual risk, and a terminal handoff improve responsible completion. | supported | `independently-supported` | NIST AI RMF 1.0 supports differentiated roles, documented limits/oversight, deployment-similar evidence, safe failure, and residual-risk reporting. It is organization-level voluntary guidance, so local application is a bounded inference. M0 already contains these behaviors; no extra H1 is justified by research alone. |
| Leading-word repetition, prohibition tables, or sequence splitting reliably improves behavior. | unknown | `unverified` | The packs instruct or report narrow pack-specific cases, but no applicable independent source and exact current-compatible control established general benefit. Keep these out of H1 absent a separately registered defect. |

### Decision-ready answer

The frozen M0 behavior is professionally supportable without reopening intent.
The strongest current-compatible H1 opportunity is narrowly conditional:

`explicit pointer repair` -> require the pointer to name the exact file or
owner, observable activation condition, and load/apply action -> expected M0
weakness is a fresh entry-positive miss of must-have branch guidance ->
observable gate is whether the exact repaired pointer causes that guidance to
be loaded and applied under fixed controls -> comparative proof is M0 versus
the repaired-pointer H1, with candidate language absent from the control.

If that H1 still misses, or fresh evidence shows the content is common rather
than conditional, test the smallest inline semantic slice as a separate
candidate. Do not preemptively inline the whole support file. This ordering is
independently supported as a bounded repair strategy, but only candidate-owned
proof can show that exact local wording contributes.

No evidence shows that M0 omitted behavior essential to its settled intent.
Therefore the research decision is `research-complete`, not `intent-reopen`.

### Alternatives, failure modes, and rejected lanes

- **Inline immediately:** rejected as the default because it duplicates
  ownership and spends context on wrong-condition runs; retain as the smallest
  fallback for a persistent observed miss or actually common behavior.
- **Keep a generic link and rely on file existence:** rejected; target
  existence does not encode the activation condition or prove retrieval.
- **Move all semantics into the support file:** rejected for common authority,
  safe-failure, Return, and completion behavior that every applicable run
  needs.
- **Add emphatic wording, leading words, or prohibitions before reproducing a
  miss:** rejected as unregistered and potentially counterproductive.
- **Treat repeated upstream usage as professional consensus:** rejected;
  repetition proves only shared pack practice.
- **Use pack benchmark percentages or earlier campaigns as efficacy proof:**
  rejected because runtime, model, host, tasks, and protocols do not match this
  campaign.
- **Practitioner conversation:** not used; published primary/official evidence
  resolved the operational condition.

## Source registry, limits, and stopping basis

### Independent source registry

| Source and identity | Access depth | Authority and retained claim | Limitation |
| --- | --- | --- | --- |
| [OpenAI Codex manual, Build skills](https://learn.chatgpt.com/docs/build-skills.md), fetched through the official manual helper; local cache reported current on 2026-07-24 | Complete Build Skills section | Current OpenAI owner for Codex skill loading, implicit invocation, description scope, progressive disclosure, and invocation policy | Product documentation, not evidence that exact wording changes behavior |
| [Agent Skills specification](https://agentskills.io/specification) and [best practices](https://agentskills.io/skill-creation/best-practices) | Exact progressive-disclosure, reference, moderate-detail, and control-calibration sections | Governing format plus official authoring guidance for staged loading and explicit conditional pointers | Cross-host standard/guidance; host behavior and model reliability can differ |
| [Agent Skills description optimization](https://agentskills.io/skill-creation/optimizing-descriptions) | Trigger design, positive/negative queries, repeat-run guidance | Primary owner for description-specific evaluation guidance | Suggested query counts and thresholds are heuristics, not universal statistical guarantees |
| [Anthropic Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) and [authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Exact loading architecture, nested-reference, evaluation/iteration, and navigation-observation sections | Claim-owning product guidance for on-demand resources and missed-reference repair | Claude-specific; transferred only where the common file-loading model applies |
| [Google developer documentation style highlights](https://developers.google.com/style/highlights) | Exact condition-order and descriptive-link rules | Official technical-writing guidance | Human-reader documentation guidance; agent application is corroborating inference |
| [W3C WCAG 2.2 link-purpose understanding](https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html) | Exact purpose/context section and failures | Governing accessibility explanation for destination clarity at the link | Human accessibility standard, not agent-behavior evidence |
| [Parnas, 1972](https://doi.org/10.1145/361598.361623) | Publisher abstract and bibliographic identity | Original claim owner for information-hiding decomposition benefits and tradeoff | Skill-ownership mapping is inference; full article text was not required for the retained abstract-level claim |
| [OpenAI trustworthy evaluation playbook](https://openai.com/index/trustworthy-third-party-evaluations-foundations/) and [GDPval method](https://openai.com/index/gdpval/#how-we-grade-model-performance) | Exact claim/harness/validity and blind-grading sections | Primary OpenAI evaluation-method claims | Broad evaluation guidance; it does not select this campaign’s sample count or prove this skill |
| [NIST AI RMF 1.0 Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) | Govern, Map, Measure, and Manage outcomes relevant to roles, limits, safe failure, and residual risk | Consensus governing framework for AI risk-management practices | Voluntary, organization-level, and currently under revision; repository-skill adaptation is inference |

### Limits and stopping basis

- Online sources were checked on 2026-07-24. The three supplied upstream
  checkouts were not fetched; identity is the exact local commit, not a claim
  about remote tip freshness.
- The current canonical package was read completely. Upstream inspection was
  bounded to the exact target packages and mechanics material to this question;
  whole-tree language packets supplied historical inventory only.
- No source proves exact runtime wording, current-model efficacy, real-world
  prevalence, cross-model transfer, or the universal superiority of pointer
  repair over inlining.
- Independent discovery preceded every pack/current/language conclusion. A
  later targeted search found a direct claim-owning corroboration for missed
  reference repair and found no decisive contradiction.
- Every load-bearing claim is classified. Another bounded source is unlikely
  to change the method, conditions, alternatives, classification, or H1
  consequence; remaining uncertainty belongs to candidate-owned behavioral
  proof.

## Caller-use boundary and Return

This packet may inform Prompt 2’s H1 admission and pre-registration. It does not
authorize Prompt 2, alter M0, select exact wording, or count as behavioral
evidence. Return owner: Deploy Campaign coordinator for
`writing-great-skills`.

<!-- research-packet:end -->
