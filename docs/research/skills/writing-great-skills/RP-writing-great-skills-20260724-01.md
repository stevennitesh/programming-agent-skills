---
artifact_id: RP-writing-great-skills-20260724-01
---

# Writing Great Skills Deploy Research Packet

## Research contract

- Campaign: `2026-07-24-writing-great-skills-7d0da40-r2`
- Applicable fixed point: Git `HEAD`
  `7d0da40a218114aa138265557ea2454361dcd147`; M0 checkpoint file SHA-256
  `91cbc7118903226cf22a6e41f8123343c1ef3be1c1ac73a294057566362d61c9`;
  semantic fingerprint
  `05e00f6d0b189165c0ef321bcc753d265e204b864bff3804cb64cfb8aa6ae8f0`.
- Research date and freshness check: 2026-07-24.
- Question: which methods, vocabulary, conditions, and alternatives best
  support the settled intended behavior of `writing-great-skills`, including
  the mandatory M0 evaluation compatibility contract?
- Caller use: evidence intake for Deploy Prompt 2. This packet may admit or
  reject H1 hypotheses but cannot choose exact runtime wording or establish
  behavioral efficacy.
- Authorized mutation: create this note only.
- Exclusions: no M0, synthesis, runtime, relationship, evaluation, test,
  method, installation, manifest, or Git-state changes; no behavioral
  evaluation; no successor unit.
- Return owner: the Deploy Campaign coordinator.

## Blind independent discovery record

This section was recorded before opening Matt Pocock, Superpowers, Ponytail,
the current canonical target package, active target synthesis, prior research,
or historical candidate conclusions. Its only local behavioral input was the
frozen M0 checkpoint.

### Search and access log

Searches covered official skill behavior and evaluation guidance, modular
ownership and information hiding, software verification and change impact,
adaptive experimental design, negative controls, treatment-effect
heterogeneity, subgroup analysis, sample-size/power counterpressure, and
terminal interpretation. Discovery-only results based on snippets, community
posts, Wikipedia, Reddit, ResearchGate, Scribd, or inaccessible abstracts were
not used as load-bearing evidence. The 1972 Parnas article was discoverable at
its DOI but its full ACM text was not accessible through the research
interface; only its bibliographic abstract is used below, with that limit.

### Independent concepts and techniques

| ID | Retained claim | Label and method classification | Conditions, counterpressure, and exact limit | H1 consequence |
| --- | --- | --- | --- | --- |
| I-01 | A skill should state a repeatable task, inputs, workflow, output, and final checks; its name and description help the host recognize relevance, and smaller composable skills are preferred to one massive end-to-end skill. | `direct`; `independently-supported` for bounded workflow and observable routing metadata. [OpenAI Academy, “Using skills,” lines 47-99](https://openai.com/academy/skills/) | Official product guidance, current on 2026-07-24, but not comparative evidence for any exact description wording and not a rule that every workflow must be split. | Preserve an observable job-to-be-done and closest exclusions in routing metadata; do not admit a wording-specific H1 without direct controls. |
| I-02 | Information hiding is a criterion for modular decomposition: organize around design decisions likely to change rather than a chronological processing flow. | `direct` at abstract depth; `independently-supported`. [Parnas, “On the Criteria to Be Used in Decomposing Systems into Modules,” DOI 10.1145/361598.361623](https://doi.org/10.1145/361598.361623) | The accessible record is the article abstract, not full text. It supports modular ownership in general, not this repository’s exact “one owner” vocabulary or file boundaries. | Supports local contract slices and pointers to foreign owners; no stronger H1 is warranted from this source alone. |
| I-03 | Verification should trace implementation to requirements, distinguish intended from unintended behavior, choose techniques appropriate to the objective, and analyze the impact of change; verification does not establish that the requirements themselves are correct. | `direct`; `independently-supported`. [NIST SP 500-234, pp. 4, 6, 14-16](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication500-234.pdf) and [NIST IR 8397](https://csrc.nist.gov/pubs/ir/8397/final) | SP 500-234 is 1996 healthcare-oriented guidance and IR 8397 is security-focused minimum guidance. Both are transferable only at the general V&V-method level. Neither prescribes token budgets or proves LLM behavior. | Trace clauses to intended behavior, use impact-matched proof, and keep structural, relationship, and behavioral claims in distinct proof lanes. |
| I-04 | AI evaluation should document test sets, metrics, tools, uncertainty, benchmark comparisons, deployment-like conditions, independent assessment, and limits of generalization. | `direct`; `independently-supported`. [NIST AI RMF Core, Measure 1-2](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) | AI RMF 1.0 is voluntary, use-case-agnostic, and under revision as of 2026-07-24. It supplies evaluation discipline, not an exact experiment or terminal vocabulary. | Keep exact task/model/host/tools/configuration/rubric identities and root-owned judgment; bound transfer claims. |
| I-05 | An eval requires representative test data and explicit testing criteria tied to ground truth or a grader; prompt reliability is judged over the test set rather than by inspecting wording alone. | `direct`; `independently-supported`. [OpenAI, “Working with evals,” lines 1027-1030 and 1203-1314](https://developers.openai.com/api/docs/guides/evals) | Official API guidance demonstrates mechanics and representative data, not a causal A/B protocol, cohort design, or universal sample count. | Supports fixed fixtures and rubrics but leaves causal isolation and adaptive sampling to stronger experimental-method sources. |
| I-06 | Adaptive designs require prospective rules, including adaptation and stopping rules, because data-dependent unplanned changes can bias inference and undermine trial integrity. | `direct` and `corroborated`; `independently-supported`. [FDA, “Adaptive Design Clinical Trials,” 2019](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/adaptive-design-clinical-trials-drugs-and-biologics-guidance-industry) and [ACE CONSORT explanation](https://www.bmj.com/content/369/bmj.m115) | Clinical-trial methods are an analogy, not a direct standard for agent evaluations. Formal type-I-error claims do not transfer to five qualitative LLM samples. | Preserve pre-registration and adaptive M0-first/H1-next gates; treat them as disciplined decision rules, not statistical guarantees. |
| I-07 | A negative control is chosen so the hypothesized causal mechanism should not operate; an unexpected effect can expose confounding, selection, or measurement bias, but a clean negative control cannot validate the whole design. | `direct`; `independently-supported`. [Lipsitch, Tchetgen Tchetgen, and Cohen, 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/) | Originates in epidemiology. A wrong-condition fixture is useful only when its facts truly remove the entry predicate while holding other arm inputs fixed. | Preserve wrong-condition M0/H1 pairs after positive contribution; use them to detect indiscriminate steering, never as positive credit for a rejected candidate. |
| I-08 | Conditional effects should be assessed in pre-specified, well-defined subgroups with an explicit rationale and analysis plan; subgroup analyses are vulnerable to low power, multiplicity, post-hoc selection, and overinterpretation. | `direct` and `corroborated`; `independently-supported`. [Kent et al., treatment-effect heterogeneity framework](https://pmc.ncbi.nlm.nih.gov/articles/PMC4450361/) and [PATH statement](https://pmc.ncbi.nlm.nih.gov/articles/PMC7531587/) | Clinical populations and formal interaction tests do not map directly to qualitative agent rubrics. Entry-positive cohorts must be defined from observable facts before sampling, and transfer outside them remains unknown. | Preserve separate entry-positive and wrong-condition cohorts and judge conditional efficacy within the registered positive condition; never dilute situational effects with non-triggering cases. |
| I-09 | A result threshold does not measure effect importance, and non-crossing of a threshold is not evidence for the null; conclusions should consider effect magnitude, uncertainty, context, and design quality. | `direct`; `independently-supported`. [American Statistical Association, p-value statement overview](https://www.amstat.org/news-listing/2021/10/08/asa-p-value-statement-viewed-150-000-times) and [ASA editorial overview](https://www.amstat.org/news-listing/2021/10/08/editorial-calls-time-on-statistically-significant-in-research) | These sources address statistical inference, while the local rubric is qualitative and uses no p-values. The transferable counterpressure is against bright-line sample-count inference. | Five is a minimum replication floor, never automatic sufficiency. Material variance or borderline effect must yield `needs-more-evidence`, not forced acceptance or rejection. |

### Blind synthesis for mandatory M0 evaluation compatibility

The mandatory compatibility contract is professionally defensible as a
disciplined, small-sample decision protocol when its claims remain narrow:

- `Defect-correction` and `quality-lift` are distinct registrations because a
  nonviable control and a viable-but-weaker control answer different questions.
  NIST V&V separates correctness against requirements from information about
  quality, while statistical guidance warns against treating any threshold as
  effect importance.
- Entry-positive cases identify the condition under which an effect is
  hypothesized; wrong-condition cases act as negative controls for
  indiscriminate steering. The entry predicate, task facts, rubric, and
  adaptation rules must be fixed prospectively.
- The M0-first gate is necessary: without the registered control deficit, H1
  cannot receive causal correction or lift credit. The H1 gate and later
  wrong-condition gate conserve samples while keeping data-dependent choices
  within predeclared rules.
- Conditional efficacy must be stated only for the registered entry-positive
  condition. Applicability frequency and efficacy are separate quantities.
- The six terminal dispositions encode materially distinct evidence states.
  In particular, `reject-no-control-deficit` is not proof of equivalence,
  `reject-insufficient-contribution` is not regression,
  `reject-regression` requires an observed critical or protected-behavior
  regression, and unresolved variance belongs in `needs-more-evidence`.

The most important counterpressure is that this protocol is not a powered
statistical trial. Five fresh controls/candidates are a pragmatic replication
floor only. It cannot support prevalence, formal significance, model or host
transfer, or a claim that absence of an observed deficit proves absence of a
possible deficit. Root-owned qualitative judgment improves fixture isolation
but can introduce evaluator bias; fixed criteria, source-traceable facts,
independent review where feasible, and explicit uncertainty are necessary.

### Blind alternatives and rejected lanes

- A single ungated before/after comparison is cheaper but cannot distinguish
  candidate contribution when M0 has no registered deficit; rejected.
- Mixing triggering and non-triggering cases into one average obscures
  conditional effects and makes applicability frequency masquerade as
  efficacy; rejected.
- Always running H1 and wrong-condition arms supplies more data but invites
  post-hoc stories and spends evaluation effort where the causal prerequisite
  failed; retain only as a separately justified exploratory lane, not candidate
  credit.
- A fixed five-sample accept/reject rule is simple but conflicts with
  uncertainty and heterogeneity guidance; rejected in favor of five as a floor
  with predeclared extension conditions.
- Structural or prose snapshot checks are useful for machine contracts but
  cannot establish wording-caused agent behavior; rejected for behavioral
  claims.
- Full Parnas text, formal power calculations, and statistical interaction
  tests were not admitted as requirements: access was incomplete for the first,
  and the latter two would imply quantitative assumptions absent from this
  qualitative agent protocol.

## Post-blind package and current observations

### Verified package registry

| Source | Identity and worktree | Access depth | Authority and limits |
| --- | --- | --- | --- |
| Matt Pocock Skills | `https://github.com/mattpocock/skills.git` at `ed37663cc5fbef691ddfecd080dff42f7e7e350d`; clean worktree checked 2026-07-24 | Complete target package: `SKILL.md` SHA-256 `8c38389dbcfdb3605690c5ce2fe0fa433e7a2f2371a7f1e697d080d81d15fdea`, `GLOSSARY.md` SHA-256 `7c8b520536aa90fdd5ceeedfbfc5e24e21df0dd480619d9f2bba38c959f3c49e`, and `agents/openai.yaml`; no scripts, examples, or tests exist in that directory | Primary only for its own vocabulary and rules. It defines predictability, leading words, target-and-condition context pointers, progressive disclosure, completion criteria, single-source pruning, and no-op tests. It does not independently prove those rules or exact wording. |
| Superpowers | `https://github.com/obra/superpowers.git` at `d884ae04edebef577e82ff7c4e143debd0bbec99`; clean worktree checked 2026-07-24 | Complete `skills/writing-skills/` runtime and its directly referenced testing, persuasion, best-practice, graph, helper, and worked-example files. Principal hashes: `SKILL.md` `6b8d08fe863318be8480ae8428e169640309fa9208df84bb0510012764454146`; testing reference `c711346852c911b24a84aa161e0cff06a4cd7f4e2fa9e9c0a266cead5afcbade` | Primary for pack behavior only. It uses no-guidance baselines, failure-shaped tests, fresh runs, repeated samples, direct inspection, and explicit counterexamples. “No skill without a failing test,” five-plus repetitions, pressure scripts, and prohibition-heavy discipline are pack policies, not universal professional thresholds. |
| Ponytail | `https://github.com/DietrichGebert/ponytail` at `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`; clean worktree checked 2026-07-24 | Complete `skills/ponytail/SKILL.md` SHA-256 `46a57e26a2632e7fa40eae6a3cf3011ccdc4d8db19d8f8617907d6b5deef055e`; benchmark overview SHA-256 `8e73fa466327170d9e5094e4b935d56f40bfd67a156e1685a06d4764750d8f2c`; applicable prompt configurations, arms, deterministic gates, agentic rubric/judge, and seeded task definitions inspected | Primary for its own minimization ladder and benchmark construction. It separates correctness/safety gates from LOC, cost, and completeness, discloses structural-only checks and workload/model limits, and reports that a one-line simplification can drop a guard. Its percentage results do not transfer to this skill. |
| Current canonical target | Repository worktree at fixed Git `HEAD` `7d0da40a218114aa138265557ea2454361dcd147` | Complete four-file package: `SKILL.md` `a97f2f20b9482c5acc4bca4c5f323521c355703cbaa7d49f228debd8cc88d311`; `GLOSSARY.md` `6c092d1ae5b0be3af7cca7594c7d3218415b754acc12ea052d914f6beea3ebac`; `BEHAVIOR-EVALS.md` `db05d6ba958235ec4e0cf7ceb9e5c80731dc06bf66e9e7c7743653e16d2939f6`; `agents/openai.yaml` `8619a54e8c098122a7f3881394f84ca89b684366e848233a29ad18b6ec363935` | Primary for current compatibility only. It already contains observable invocation and exclusions, bounded Audit/Author authority, one-owner relationships, conditional pointers, behavior-preserving cuts, claim-matched proof, the mandatory M0 evaluation protocol, typed Return/completion, and implicit invocation. Current presence proves neither minimum necessity nor efficacy. |

The upstream checkouts were not fetched. Their exact local commits and clean
worktrees are the applicable identities; no claim is made that they equal
remote tips on 2026-07-24.

### Pack mechanics and targeted verification

1. **Matt: leading words and pointer repair.** Matt proposes pretrained
   “leading words” as compact steering anchors and says a must-have weak pointer
   should be sharpened before content is pulled inline. The live Agent Skills
   guidance independently supports only the latter premises: reference files
   should be loaded conditionally and the pointer should name the exact file and
   activation condition
   ([best practices, lines 145-147](https://agentskills.io/skill-creation/best-practices)).
   It also says to cut content the agent already handles and to test uncertainty
   rather than assume a no-op
   ([lines 105-132](https://agentskills.io/skill-creation/best-practices)).
   No independent owner inspected establishes “leading word” repetition as a
   generally effective method. Classification: pointer formulation
   `independently-supported`; leading-word steering `unverified`.

2. **Superpowers: baseline-first and failure-shaped guidance.** The pack’s
   no-guidance baseline, same-task candidate comparison, fresh contexts,
   repeated samples, rubric inspection, and counterexamples align with live
   Agent Skills guidance: run with and without the skill, isolate every run,
   use observable assertions, prefer scripts for mechanical checks, use blind
   comparison for holistic quality, inspect variance, and remove assertions
   that pass both arms
   ([evaluating skills, lines 67-108, 142-157, 173-185, 242-282](https://agentskills.io/skill-creation/evaluating-skills)).
   Counterpressure from the same owner says rigid `ALWAYS`/`NEVER` directives
   are often less reliable than purpose-bearing instructions and warns against
   over-constraining
   ([lines 299-320](https://agentskills.io/skill-creation/evaluating-skills)).
   Classification: controlled comparison and failure-shaped admission
   `independently-supported`; the universal TDD analogy, pressure recipe,
   prohibition tables, and five-plus count `pack-specific`.

3. **Ponytail: minimization under preserved floors.** The pack does not treat
   shortness as sufficient: it preserves explicit requirements, safety, data
   loss prevention, comprehension, and a runnable check, while its benchmarks
   gate correctness/safety separately from LOC and cost. This agrees with NIST
   V&V’s requirements trace and intended/unintended behavior distinction and
   Agent Skills’ advice to remove instructions only when baseline behavior
   already supplies them. The benchmark itself documents counterexamples:
   single-shot prose inflated some apparent savings, a minimal one-line arm
   dropped a guard, model transfer was uneven, and cost direction depended on
   workload. Classification: behavior-preserving minimization
   `independently-supported`; Ponytail’s exact ladder and benchmark effect
   sizes `pack-specific`.

4. **Description and disclosure conflict.** Superpowers says a description
   must contain only trigger conditions, whereas the current Agent Skills
   specification says it describes both what the skill does and when to use it
   ([specification, lines 144-158](https://agentskills.io/specification)).
   The optimization guide supports concise user-intent triggers, close negative
   cases, repeated invocation trials, and held-out validation
   ([optimizing descriptions, lines 65-79, 82-135, 170-175](https://agentskills.io/skill-creation/optimizing-descriptions)).
   Therefore the absolute “when only” rule is `contested`; the current
   description’s observable outcome plus closest exclusions remains the better
   supported local formulation.

## Historical intake and evidence disposition

Applicable local language packets were inspected after blind discovery:
`matt-pocock-skills-vocabulary.md`,
`superpowers-skill-pack-vocabulary.md`,
`ponytail-skill-pack-vocabulary.md`,
`03-high-signal-steering-words.md`, and
`04-agentic-bridge-vocabulary.md`. They use the same three upstream revisions
and preserve useful source traces for pointer, completion, baseline, safety,
quality, and transfer vocabulary. They are `historical-admission-only`: their
claims were checked against the exact packages and current online owners rather
than copied as current conclusions.

The preceding deploy research packet
`writing-great-skills-deploy-2026-07-24-7d0da40.md` used the same Git fixed
point, upstream revisions, and 2026-07-24 source identities. Its progressive
disclosure, evaluation-isolation, NIST boundary, and Parnas lanes are
`lane-limited`: source identity and general claims match, but this campaign’s
mandatory M0 evaluation contract and intended application are broader, so
those conclusions were independently rechecked and redistilled here.

The failed Prompt 5 final manifest and transcript were used only as correction
evidence that the frozen compatibility contract is mandatory M0. They show the
prior P1 failed canonical proof because it omitted defect-correction versus
quality-lift registration, entry-positive and wrong-condition cohorts,
adaptive gates, conditional-efficacy judgment, and terminal dispositions.
They provide no H1 admission or efficacy evidence.

The predecessor C0-G04 result is
`historical-admission-only` for exact prior M0 tree
`175c70bbe0ee79fad197f44ba32f0786b9bb94250ef22da21e66ded47d9e0341`:
five controls scored 8/8, H1 and wrong-condition sampling did not run, and the
disposition was `reject-no-control-deficit`. It cannot establish the control
behavior of newly derived M0 bytes.

### Current C0-G04 classification

C0-G04 is **not a current H1 candidate from this Research Pass**. The repair
method remains independently supportable under its condition, but the current
canonical package already names each support-file target and its activation
condition, and this campaign has no fresh observation that must-have branch
material is being missed. The entry predicate therefore lacks current
evidence. Exact consequence:

`not-admitted-no-current-entry-observation`; reconsider only if Prompt 2 has
new, source-traceable current evidence of a must-have pointer miss or derives a
distinct M0 weakness. The prior `reject-no-control-deficit` result neither
admits nor rejects any newly materialized bytes. No other C0 unit was reopened.

## Decision-ready classifications

| Method or claim | Research status | Method class | Evidence and counterpressure | H1 consequence |
| --- | --- | --- | --- | --- |
| Observable outcome and nearest exclusions in routing metadata | supported | `independently-supported` | OpenAI Academy and Agent Skills specification/optimization; Superpowers’ “when only” absolute conflicts with the specification | Preserve M0; no H1 unless positive/near-miss invocation tests expose a deficit |
| Common behavior inline; branch-only material behind a direct target-and-condition pointer | supported | `independently-supported` | Agent Skills specification/best practices, Anthropic package guidance, and current package observation; hidden critical content and deep chains are counterpressure | Preserve M0; repair only after a current observed miss |
| One semantic owner with sufficient local contract slice | supported | `independently-supported` at software-method level | Parnas information hiding and NIST requirements/interface trace; skill-file application is inference | Preserve M0; do not copy foreign procedure |
| Behavior-preserving cuts based on baseline contribution, not shorter prose alone | supported | `independently-supported` | Agent Skills eval guidance, NIST V&V, and Ponytail’s disclosed safety/completeness counterexamples | Preserve M0; any cut needs affected proof, not byte reduction alone |
| Fixed task, runtime, evidence, rubric, isolated arm delta, fresh context, direct inspection, and bounded transfer | supported | `independently-supported` | Agent Skills evaluation guidance, OpenAI eval mechanics, and NIST AI RMF | Preserve M0; this is the minimum causal envelope for wording claims |
| Separate `defect-correction` and `quality-lift` registration | supported | `independently-supported` as a local operational distinction | NIST separates requirement correctness from quality/reliability evidence; Agent Skills compares both hard assertions and holistic quality and removes always-pass criteria | Preserve mandatory M0 vocabulary; no claim that the labels are an external standard |
| Entry-positive cohort separated from wrong-condition cohort | supported | `independently-supported` | Pre-specified treatment-effect heterogeneity plus negative-control method; near-miss trigger tests provide an agent-skill analogue | Preserve M0; entry facts must uniquely determine the expected branch |
| Adaptive M0-first, H1-next, wrong-condition-last gates | supported | `independently-supported` as disciplined design | FDA/ACE prospective adaptive rules plus Agent Skills baseline-first comparison and removal of always-pass assertions | Preserve M0; gates are decision discipline, not formal statistical guarantees |
| Judge efficacy conditionally on entry-positive cases while keeping applicability separate | supported | `independently-supported` | Heterogeneity guidance, NIST context-specific TEVV, and Agent Skills pattern analysis | Preserve M0; do not average non-triggering cases into efficacy or infer prevalence from fixtures |
| Five fresh samples as a minimum floor | supported only as local compatibility | `unverified` as a universal threshold | Upstreams use three, five-plus, or ten depending on purpose; ASA and Agent Skills emphasize variance and additional runs | Preserve M0 floor because intent requires it; never treat five as automatic sufficiency |
| Six exact terminal dispositions | supported as local compatibility | `pack-specific` vocabulary with independently supported distinctions | Evaluation sources distinguish no baseline signal, no material delta, regression, uncertainty, and invalid protocol, but do not prescribe these exact tokens | Preserve all six exact M0 tokens and their meanings; do not generalize them as an external standard |
| Leading words, emphatic prohibition, pressure tables, or sequence splitting as default steering | unknown or conflicted | `unverified` / `contested` | Upstream observations are narrow; Agent Skills cautions against rigid directives and over-constraint; no current registered deficit | Do not admit an H1 from this research |

## Intent-adjacent candidates and alternatives

No beyond-M0 H1 is currently justified. The independently supported methods
are already represented in the frozen minimum or lack a current entry-positive
deficit.

The following are deferred, not admitted:

- pointer-repair escalation, only after a fresh observed must-have miss;
- stronger routing vocabulary, only after positive and close-negative
  invocation controls expose a deficit;
- leading-word compression, only after a registered no-op or steering deficit;
- prohibition/rationalization hardening, only for a demonstrated discipline
  failure and against a positive-form alternative;
- extra sample-count or power language, only if Prompt 3 can define a
  quantitative estimand and operating characteristics—which current qualitative
  proof does not.

Rejected alternatives remain: ungated candidate sampling, mixed triggering and
non-triggering averages, automatic acceptance after five, structural proxy
credit for behavioral claims, immediate inlining of all conditional material,
and shortest-bytes-first pruning.

## Limits, gaps, and saturation

- No inspected source proves exact wording efficacy, real-world applicability
  frequency, a universal five-sample threshold, cross-model/host transfer, or
  unbiased root judgment.
- Clinical and epidemiologic methods are transferred only at the design
  principle level. This packet makes no p-value, power, confidence, or formal
  causal-identification claim for qualitative agent samples.
- The Parnas claim is abstract-depth because the full publisher text was not
  accessible through the research interface.
- Anthropic material bundled by Superpowers was checked against the current
  live guidance where relevant; host-specific mechanics remain non-transferable.
- Prior campaign artifacts are not current proof. The failed Prompt 5 records
  establish only mandatory compatibility; C0-G04 establishes only its exact
  historical admission lane.
- Root-owned judgment can reduce worker contamination while retaining evaluator
  bias. Fixed rubrics, source-fact traceability, direct inspection, and
  independent review where feasible mitigate but do not eliminate that risk.

Every load-bearing claim is classified, the strongest applicable governing or
primary owner and a credible counterposition were inspected, all upstream
mechanics that could affect H1 received targeted verification, and another
bounded source is unlikely to change the classifications or current
no-H1 consequence. Remaining unknowns belong to candidate-owned proof, not
additional Research.

## Research decision and caller boundary

Research status: `answered`.

Deploy decision: `research-complete`. Independent evidence supports the frozen
M0 behavior, including its mandatory evaluation compatibility contract, under
the limits above. No evidence shows that M0 omitted behavior essential to
settled intent, and no current evidence admits C0-G04 or another beyond-minimum
H1.

This packet may inform Deploy Prompt 2. It does not authorize Prompt 2, choose
exact runtime wording, alter M0, or provide behavioral credit. Return owner:
Deploy Campaign coordinator for `writing-great-skills`.
