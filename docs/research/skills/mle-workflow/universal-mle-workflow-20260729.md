---
artifact_id: RP-mle-workflow-20260729-01
---

# Universal MLE Workflow Research Note

## Research contract

- Question: Which project-agnostic practices should a universal Codex MLE
  workflow enforce across purpose, data, experimentation, delivery, operation,
  and risk without forcing unnecessary platform machinery?
- Caller use: evidence for revising `skills/extra/mle-workflow`.
- Scope: production or reproducibility-bound predictive ML, ranking,
  recommendation, forecasting, embedding, anomaly-detection, batch, online,
  streaming, edge, and model-refresh work. Generative AI and online learning
  are conditional branches, not assumed defaults.
- Exclusions: algorithm selection tutorials, framework-specific recipes,
  universal legal conclusions, sector-specific compliance, fixed metric
  thresholds, and mandatory MLOps products.
- Freshness: sources inspected on 2026-07-29. NIST AI RMF 1.0 is under revision;
  applicable laws, policies, library behavior, and security guidance require a
  project-time refresh.
- Authorized mutation for this research unit: create this note only.
- Return owner: the root author of `mle-workflow`.

## Answer

A universal workflow should align the entire ML system to one versioned
purpose-and-impact contract, scale evidence and controls to the project's
actual risk and operating mode, preserve lineage across every lifecycle
transition, and make promotion depend on deployment-relevant evidence.

The workflow should require:

1. purpose, affected parties, accountable ownership, non-ML alternatives, and
   failure costs before model optimization;
2. explicit data semantics, timing, provenance, split ownership, and leakage
   controls;
3. traceable experiments, meaningful baselines, deployment-shaped evaluation,
   uncertainty, and important slices;
4. layered tests for data, transformations, model behavior, pipeline,
   packaging, and serving;
5. an immutable candidate and release identity, enforced promotion gates, a
   proportionate rollout, correlated monitoring, and a rehearsable fallback;
6. feedback, retraining, incident, rollback, and retirement transitions that
   re-enter the same evidence gates; and
7. conditional privacy, security, fairness, robustness, and compliance work
   activated by the project's exposure and impact.

The agent must not invent stakeholder values, risk tolerance, consent, legal
applicability, or residual-risk acceptance. It should surface those owner-held
decisions and continue on independent work where safe.

## Claim ledger

### C1. Purpose and impact must precede model optimization

**Status: supported.**

NIST AI RMF 1.0 makes context mapping, intended purpose, users, expected
benefits and costs, risk tolerance, and go/no-go decisions part of lifecycle
risk management. It also treats governance as cross-cutting rather than a
single end-stage review. Google guidance separately warns that strong model
metrics do not guarantee product or business impact and recommends comparing
against a non-ML or simple baseline.

Sources:

- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- [NIST AI RMF 1.0 publication record](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)
- [Google: Measuring success](https://developers.google.com/machine-learning/managing-ml-projects/success)
- [Google: Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml)

Skill consequence:

- Lock the decision or action the model changes, intended and out-of-scope
  uses, users and affected non-users, benefit hypothesis, measurable outcome,
  guardrails, failure costs, non-ML baseline, owner, and rollback condition.
- Reopen that contract when users, context, data, objective, threshold, model,
  or governing obligations materially change.
- Stop only the dependent decision when an organization-owned value or risk
  tolerance is missing.

Limit: NIST is voluntary, use-case-agnostic guidance, not certification or a
legal safe harbor. Google guidance is experience-based, not proof that a simple
model is always optimal.

### C2. Documentation must be living evidence tied to exact artifacts

**Status: supported.**

Datasheets for Datasets proposes documenting dataset motivation, composition,
collection, processing, uses, limits, and maintenance. Model Cards proposes
documenting intended and out-of-scope uses, evaluation conditions, thresholds,
subgroup results, caveats, and recommendations. W3C PROV supplies a generic
entity-activity-agent derivation model.

Sources:

- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010)
- [Model Cards for Model Reporting](https://research.google/pubs/model-cards-for-model-reporting/)
- [W3C PROV-DM Recommendation](https://www.w3.org/TR/2013/REC-prov-dm-20130430/)

Skill consequence:

- Maintain a compact system decision record, data record, run record, and model
  or release record only when the project needs durable evidence.
- Bind records to immutable data, code, configuration, environment, evaluation,
  artifact, approval, deployment, and retirement identities.
- Treat missing reconstructability as an explicit evidence gap.

Limit: documentation improves traceability but does not prove truth, safety,
fairness, compliance, or independent assurance. W3C PROV does not require RDF
or a specific metadata store.

### C3. Data correctness includes semantics, availability time, and lineage

**Status: supported.**

The Open Data Contract Standard demonstrates a platform-neutral contract shape
covering semantics, quality, ownership, and service expectations. Original
leakage work and current official implementation guidance agree that features
must be legitimate at prediction time. Google and Breck et al. distinguish raw
data validation, transformed-data validation, cross-batch checks, and
training-serving skew.

Sources:

- [Open Data Contract Standard 3.1](https://bitol-io.github.io/open-data-contract-standard/latest/)
- [Leakage in Data Mining](https://www.cs.umb.edu/~ding/history/470_670_fall_2011/papers/cs670_Tran_PreferredPaper_LeakingInDataMining.pdf)
- [Data Validation for Machine Learning](https://proceedings.mlsys.org/paper_files/paper/2019/file/928f1160e52192e3e0017fb63ab65391-Paper.pdf)
- [Google: Monitoring ML pipelines](https://developers.google.com/machine-learning/crash-course/production-ml-systems/monitoring)
- [scikit-learn: Common pitfalls and data leakage](https://scikit-learn.org/stable/common_pitfalls.html)

Skill consequence:

- Record dataset owner, grain/key, field meaning and units, label definition,
  event time, availability time, ingestion time, backfill behavior, null/type/
  range/domain constraints, freshness, permitted use, and change policy.
- Prove point-in-time construction from what was knowable at decision time.
- Split before fitting learned transforms; fit preprocessing, selection,
  calibration, and threshold tuning only inside their declared ownership
  boundary.
- Validate raw, transformed, new-batch, and serving data separately where
  applicable.
- Classify point-in-time correctness as unknown when historical availability
  cannot be reconstructed.

Limits: ODCS is an emerging open specification, not a required file format.
Distribution change is not inherently an error. Feature stores, schema
registries, TFX, and specific validation products are optional implementations.

### C4. Evaluation boundaries must match the deployment claim

**Status: supported.**

Official scikit-learn guidance rejects test-set reuse and describes time-aware,
group-aware, stratified, and nested evaluation for different dependence
structures. NIST calls for uncertainty, benchmarks, documented test conditions,
and evaluation similar to deployment. Google recommends important slices,
absolute and relative gates, repeated runs where noise matters, and separation
of model and real-world outcomes.

Sources:

- [scikit-learn: Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)
- [scikit-learn: Probability calibration](https://scikit-learn.org/stable/modules/calibration.html)
- [Google: Experiments](https://developers.google.com/machine-learning/managing-ml-projects/experiments)
- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/)
- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)

Skill consequence:

- Predeclare deployment population, horizon, decision unit, primary metric,
  guardrails, minimum meaningful change, threshold policy, split ownership,
  slices, uncertainty method, and promotion gates.
- Use future-held-out evidence for future prediction and group-aware evidence
  for dependent entities. Persist split identity.
- Protect final-test evidence from feature, model, hyperparameter, calibration,
  and threshold selection.
- Report the source of variability, experimental unit, independent runs or
  resamples, interval meaning, and practical effect size.
- Require slice counts/coverage and both an absolute floor and allowable
  regression for important slices.
- Evaluate calibration only when probabilities drive decisions, confidence,
  abstention, or composition.

Limits: there is no universal split ratio, resampling method, metric, fairness
definition, number of seeds, confidence method, or threshold. The ML Test Score
is a useful rubric but its numeric bands and equal weighting are not universal.

### C5. Reproducibility means traceable replay plus bounded result stability

**Status: supported with a practical boundary.**

Google experiment guidance and the ML Test Score support versioned
specifications, run tracking, and training reproducibility. PyTorch explicitly
warns that complete reproducibility is not guaranteed across releases,
platforms, or devices.

Sources:

- [PyTorch: Reproducibility](https://docs.pytorch.org/docs/stable/notes/randomness.html)
- [Google: Experiments](https://developers.google.com/machine-learning/managing-ml-projects/experiments)
- [The ML Test Score](https://storage.googleapis.com/gweb-research2023-media/pubtools/4156.pdf)

Skill consequence:

- Record hypothesis, parent baseline, intended change, code revision, immutable
  data and splits, complete resolved config, dependencies, relevant hardware,
  randomness controls, metrics, artifacts, decision, and failed/neutral runs.
- Distinguish artifact reproducibility (recover exact inputs and outputs) from
  result reproducibility (repeat the claim within a declared tolerance or
  uncertainty envelope).
- Default diagnostic experiments to one intended change, but allow explicit
  ablation, factorial, or search designs.

Conflict resolution: one seed is not proof, and bitwise equality is not a
universal requirement. Strict determinism is a conditional debugging or audit
mode that may reduce performance.

### C6. ML testing must cover the system, not only model metrics

**Status: supported.**

The ML Test Score enumerates data, feature, model, pipeline, and monitoring
tests. Current Google deployment guidance separately requires input,
transformation, model-quality, infrastructure, and integration testing.
Hidden Technical Debt shows why system dependencies, feedback loops,
undeclared consumers, and configuration can dominate model-code risk.

Sources:

- [The ML Test Score](https://storage.googleapis.com/gweb-research2023-media/pubtools/4156.pdf)
- [Google: Deployment testing](https://developers.google.com/machine-learning/crash-course/production-ml-systems/deployment-testing)
- [Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html)

Skill consequence:

- Select tests across data/schema, transformations, model/API behavior,
  numerical and domain invariants, pipeline integration, artifact loading,
  train/inference parity, serving compatibility, absolute and relative quality
  gates, important slices, fallback, and rollback.
- Keep fast reduced-data coverage and proportionate production-like tests.
- Make promotion gates enforceable. A warning-only gate is not a gate.
- Inspect upstream producers, downstream consumers, feedback loops, shared
  transformations, and configuration after meaningful changes.

Limit: conventional unit tests remain valuable but are insufficient alone.
Partially trained golden-model comparisons can be flaky and weakly diagnostic.

### C7. Continuous training creates candidates; it does not authorize promotion

**Status: supported.**

Google's MLOps guidance distinguishes CI, delivery, and continuous training and
adds data/model validation, triggers, and metadata to ML pipelines. Production
monitoring guidance treats drift and staleness as signals requiring
investigation, not automatic proof of quality failure.

Sources:

- [Google: CI/CD and automated ML pipelines](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
- [Google: Monitoring ML pipelines](https://developers.google.com/machine-learning/crash-course/production-ml-systems/monitoring)

Skill consequence:

- Model lifecycle transitions as experiment -> candidate -> validated -> staged
  -> active -> rolled back or retired.
- Treat manual, schedule, qualified-new-data, degradation, policy, contract, or
  implementation triggers as candidate-generation events.
- Re-enter data, evaluation, security, promotion, and rollout gates for every
  candidate.
- Never allow drift -> retrain -> auto-promote.

Limit: frequent retraining is not inherently mature or safer. Fixing data,
instrumentation, policy, or serving defects may be the right response.

### C8. Rollout modes answer different evidence questions

**Status: supported.**

Google SRE guidance distinguishes shadowing/dry runs from canaries. Microsoft
experimentation research treats randomized online tests as causal evidence,
which is a different purpose from integration or limited-exposure validation.

Sources:

- [Google SRE: Canarying releases](https://sre.google/workbook/canarying-releases/)
- [Google SRE: Data processing pipelines](https://sre.google/workbook/data-processing/)
- [Microsoft Research: Anatomy of a Large-Scale Experimentation Platform](https://www.microsoft.com/en-us/research/publication/the-anatomy-of-a-large-scale-experimentation-platform/)

Skill consequence:

- Shadow or dry run: suppress user-visible effects and production writes;
  establish integration, parity, capacity, or skew evidence.
- Canary: use limited real exposure, concurrent control, version-scoped
  telemetry, representative traffic, and predeclared pause/abort/ramp rules.
- A/B: use controlled assignment and an analysis plan only when causal product
  impact is material, feasible, and ethical.
- Batch: use a dry run, skipped-write mode, bounded partition, or equivalent
  reversible boundary.

Limit: shadowing does not establish user benefit; canaries do not by themselves
establish causal lift; A/B tests are not always feasible or ethical.

### C9. Monitoring, feedback, incidents, and retirement are one lifecycle

**Status: supported, with unsettled implementation thresholds.**

NIST AI RMF requires production monitoring, incident response, feedback and
appeal mechanisms, override/deactivation, and decommissioning. NIST AI 800-4
organizes post-deployment monitoring across functionality, operations, human
factors, security, compliance, and wider impacts, while noting that methods and
thresholds remain immature. OpenTelemetry supplies vendor-neutral correlated
signals, not an ML semantic schema.

Sources:

- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- [NIST AI 800-4: AI System Monitoring](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-4.pdf)
- [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/)

Skill consequence:

- Correlate secure internal telemetry with release/artifact, config/data
  contract, and rollout cohort identities.
- Select applicable service, data/schema/freshness, skew, prediction, delayed
  outcome, calibration/error slice, business, feedback/appeal, security, and
  impact signals.
- Link actionable alerts to an owner and recovery playbook.
- Bound harm first during incidents through stop, fallback, traffic control, or
  rollback; preserve evidence and handle affected outputs/data.
- Treat retirement as a transition: stop traffic and training triggers,
  migrate consumers, mark artifacts non-promotable, retire resources and
  alerts, apply retention policy, and preserve required lineage.

Unknown: no universal cadence, drift threshold, alert threshold, or
automation/human balance is supported. Those values are project-owned.

### C10. Security and privacy must be capability-triggered

**Status: supported.**

NIST SSDF and its AI model-development profile require risk-based protection,
provenance, integrity, third-party verification, secure serialization, and
response criteria. NIST adversarial ML guidance organizes exposure by attacker
capability. Official Python and scikit-learn documentation warn that
pickle-like artifacts can execute code and that even ostensibly safer formats
can consume malicious resources. NIST Privacy Framework supports purpose,
flow, minimization, access, retention, and reassessment.

Sources:

- [NIST SSDF 1.1](https://doi.org/10.6028/NIST.SP.800-218)
- [NIST AI Model Development SSDF Profile](https://doi.org/10.6028/NIST.SP.800-218A)
- [NIST Adversarial Machine Learning](https://doi.org/10.6028/NIST.AI.100-2e2025)
- [NIST Privacy Framework](https://doi.org/10.6028/NIST.CSWP.10)
- [Python pickle documentation](https://docs.python.org/3/library/pickle.html)
- [scikit-learn: Model persistence](https://scikit-learn.org/stable/model_persistence.html)

Skill consequence:

- Inventory trust and exposure for data, code, dependencies, models,
  configuration, loaders, endpoints, outputs, logs, and consumers.
- Never execute an untrusted or potentially tampered executable model artifact.
- Bind promoted artifacts to origin, integrity evidence, code, data,
  preprocessing, configuration, dependencies, and approved runtime.
- Activate poisoning, evasion/abuse, privacy, supply-chain, red-team, resource
  exhaustion, or GenAI-specific branches only when corresponding access,
  sensitivity, impact, or architecture exists.
- Treat hashes, signatures, provenance, adversarial tests, and safer formats as
  evidence rather than guarantees.

Limits: NIST sources are outcome-oriented and risk-based. No universal workflow
should require adversarial training, red teaming, differential privacy, formal
verification, containers, SBOMs, or a particular serialization format for
every model.

### C11. Accountability and obligations remain owner-held

**Status: supported.**

NIST assigns documented roles, go/no-go decisions, override, and deactivation
responsibility. The OECD recommendation ties accountability and traceability
to lifecycle actors. Binding duties vary by jurisdiction, sector, operator
role, use, and date; the EU AI Act is one current example of staggered,
risk-tiered obligations.

Sources:

- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- [OECD Recommendation on AI](https://pp.oecd.ai/en/assets/files/OECD-LEGAL-0449-en.pdf)
- [EU Regulation 2024/1689](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A32024R1689)

Skill consequence:

- Record accountable owners and escalation routes for purpose, data use,
  deployment, residual risk, incident response, and retirement.
- Trigger a current obligations scan for jurisdiction, sector, operator role,
  use context, affected rights, data categories, and organizational policy when
  those facts matter.
- Never return a universal "responsible AI compliant" verdict.

Limit: the workflow cannot replace legal, privacy, safety, security, or domain
review.

## Retained universal behaviors

- Purpose and impact lock with a no-ML comparison
- Risk- and operating-mode calibration
- Data semantics, timing, provenance, contract, and reviewed change policy
- Deployment-shaped splitting and protected final evidence
- Immutable run, candidate, and release identity
- Baseline ladder and practical-effect comparison
- Uncertainty and important-slice evidence
- Layered system tests and enforceable promotion gates
- Train/inference equivalence or parity proof
- Explicit lifecycle transitions and candidate-only retraining
- Proportionate rollout with distinct evidence claims
- Correlated monitoring, feedback governance, incident recovery, and retirement
- Capability-triggered privacy, security, fairness, robustness, and compliance
- Honest unknown and residual-risk reporting

## Rejected or conditional behaviors

Do not make these universal:

- ML as the assumed solution
- one fixed architecture, model family, framework, cloud, or metadata product
- online serving, feature stores, containers, registries, Kubernetes, or GPUs
- fixed train/validation/test ratios or random splits
- fixed metrics, thresholds, slice lists, fairness definitions, or retrain cadence
- one seed or bitwise identity as complete reproducibility
- calibration when probabilities have no decision meaning
- A/B tests for every system
- continuous training or automatic promotion as a maturity goal
- drift as proof of degradation or attack
- documentation, signatures, or provenance as proof of safety
- model version in user-visible output when internal correlation is sufficient
- red teaming, adversarial training, differential privacy, or formal
  verification without an applicable threat or obligation
- legal or responsible-AI compliance conclusions by the agent
- the ML Test Score numeric bands as a universal readiness score

## Material conflicts and unknowns

- Determinism: exact replay is desirable but not portable across all libraries,
  devices, and releases. Require traceable inputs and a declared tolerance or
  result distribution.
- Automation: recurring mechanical gates benefit from automation, but rare or
  high-impact decisions may require owner approval. Enforceability, not
  automation alone, is universal.
- Drift: drift is diagnostic evidence. Direct outcome measurement is stronger
  when trustworthy labels exist, but interventions and selection can bias those
  labels too.
- Fairness and impact: relevant harms, populations, and metrics are contextual.
  Hard-coded attributes or metrics can be wrong and may create privacy issues.
- Monitoring: universal categories are supportable; universal thresholds,
  cadence, and validated drift methods are not.
- Legal applicability: changes with jurisdiction, sector, role, and date.
- Specialized systems: reinforcement learning, federated learning, generative
  AI, adaptive online learning, safety-critical control, and regulated domains
  need branch-specific evidence beyond this universal core.

## Stopping basis

Every load-bearing area of the project-agnostic lifecycle core has an inspected
claim-owning source: government risk and security frameworks, standards
bodies, original research, official framework documentation, or primary
industry systems work. The sources converge on the universal behaviors and on
the need for proportionate branching. The specialized-system research is not
exhaustive; the skill may use conservative triggers, authority boundaries,
safe-unknown outcomes, and escalation for those systems, but it must not claim
that this note supplies a complete generative-AI, adaptive-learning,
reinforcement-learning, federated-learning, safety-critical, or regulated
workflow. Remaining disagreement concerns local implementation, thresholds,
legal applicability, and specialized system types; more general research is
unlikely to change the universal core, while a concrete specialized project
can still require a narrower follow-up research pass.

Research status: `answered`.

Caller-use boundary: this note supports skill synthesis. It does not select
exact runtime wording, prove agent behavior, approve deployment, install the
skill, or accept project risk.

Return owner: root author of `skills/extra/mle-workflow`.
