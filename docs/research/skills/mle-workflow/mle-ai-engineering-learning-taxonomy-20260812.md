---
artifact_id: RP-mle-ai-learning-taxonomy-20260812-01
---

# MLE and AI Engineering Learning Taxonomy and Source-Catalog Design

## Research contract

- Question: What broad topic taxonomy and source-catalog method should organize
  learning for machine learning engineering and AI engineering without becoming
  too specialized at the outset, while supporting a later specialization in
  stock markets, backtesting, financial predictive modeling, classification,
  and fintech?
- Caller use: organize future research, reading, distillation, exercises, and
  skill-maintenance work into a durable broad-first curriculum and source
  catalog.
- Scope: professional MLE and AI-engineering competencies, cross-cutting
  assurance, modern composed-AI systems, and a finance/fintech specialization.
- Exclusions: a complete university curriculum, a tool or vendor catalog,
  detailed algorithm tutorials, strategy selection, profitability claims,
  personalized investment advice, fixed universal proficiency thresholds, and
  implementation of the proposed catalog.
- Applicable repository state: commit
  `9ddb58a34ad363b7ce3bfac56430ee9eda56cad8`, inspected on 2026-08-12. The
  sibling [primary-source distillation map](./mle-ai-primary-sources-20260812.md)
  was treated as a working research artifact.
- Freshness: the repository and cited mutable sources were inspected on
  2026-08-12. Standards, regulations, security taxonomies, model-provider
  behavior, and market mechanics require project-time refresh.
- Authorized mutation: create this note only.
- Return owner: the user and future root author of `mle-workflow` research.

## Status and answer

**Status: answered.**

The earlier 14-topic list is a strong `mle-workflow` evidence map, but it is not
a balanced learning taxonomy for the complete MLE or AI-engineering surface. It
mixes prerequisites, lifecycle stages, statistical methods, cross-cutting
controls, domain specializations, and AI architectures at the same level.

Use this structure instead:

```text
8 broad learning domains
+ one mandatory assurance spine
+ a modern AI-engineering pathway
+ a finance and fintech pathway
+ later conditional specializations
```

For the source catalog, keep one canonical record per exact source and version,
but do not require one exclusive semantic `primary_topic`. Store multi-valued
subjects and claim-level authority, applicability, and limits. Keep learning
order in separate paths, and derive topic views rather than copying source
records.

No paper, standard, or framework owns this exact taxonomy. It is a labeled
synthesis. Its main premises are supported by:

- the breadth of computing competencies in the
  [ACM/IEEE-CS/AAAI CS2023 knowledge areas](https://csed.acm.org/knowledge-areas/),
  which separately expose mathematical foundations, AI, data management,
  software engineering, distributed computing, security, systems, and
  human-computer interaction;
- the industrial ML lifecycle studied by
  [Amershi et al.](https://www.microsoft.com/en-us/research/uploads/prod/2019/03/amershi-icse-2019_Software_Engineering_for_Machine_Learning.pdf);
- the system-level failure and maintenance model in
  [Sculley et al.](https://papers.nips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf);
- the AI lifecycle processes described by
  [ISO/IEC 5338](https://www.iso.org/standard/81118.html);
- the continuous, cross-cutting risk-management model in the
  [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/);
  and
- the operational reliability disciplines documented in the
  [Google SRE books](https://sre.google/books/).

## Debate method

Six independent lanes inspected the saved research packet and canonical
`mle-workflow` from fresh context:

1. general MLE professional surface;
2. modern AI-engineering surface;
3. financial markets and fintech;
4. catalog and information architecture;
5. adversarial challenge for omissions and category errors; and
6. broad-first learning sequence.

After the initial arguments, every lane received a convergence proposal and a
targeted cross-examination question. The remaining disagreement was about
organization rather than missing subject matter:

- one position preferred six workflow seams plus cross-cutting lenses;
- another preferred eight learning domains so prerequisites and professional
  competencies remain visible;
- all positions agreed that the original 14 peer topics were structurally
  mixed, finance should become one specialization umbrella, modern AI concerns
  must be integrated into the common core, and source classification must be
  many-to-many.

This packet chooses eight learning domains because its primary use is learner
navigation. The six workflow seams remain useful as claim-level catalog
metadata and for mapping sources into `mle-workflow`.

## Debate findings

### What was good about the original 14 topics

The original list gave strong coverage to:

- point-in-time data and leakage;
- experiment design and model selection;
- statistical inference and uncertainty;
- calibration and decision thresholds;
- causal, measurement, and proxy-validity boundaries;
- time-series validation;
- financial backtesting and strategy search;
- execution, costs, and capacity;
- ML testing and reliability;
- delivery and operation;
- risk and governance; and
- generative and tool-using systems.

These remain valuable concepts. The correction concerns their placement, not
their removal.

### What the original list underrepresented

The independent lanes consistently identified these missing or compressed
professional surfaces:

- programming and quantitative prerequisites;
- ordinary software engineering and collaboration;
- general data engineering beyond dataset validity;
- distributed systems and platform engineering;
- core model development and optimization;
- inference and runtime engineering;
- product design and human workflows;
- model sourcing, acquisition, and adaptation;
- resource economics and sustainability outside trading costs;
- organizational ownership, handoffs, and review independence; and
- portfolio construction and risk between predictions and trades.

### Why the original list was not one taxonomy

It mixed several independent axes:

- **prerequisites:** probability, statistics, programming, and optimization;
- **knowledge domains:** software, data, modeling, and security;
- **lifecycle stages:** framing, development, delivery, and operation;
- **methods:** calibration, inference, causal identification, and backtesting;
- **cross-cutting qualities:** reliability, reproducibility, provenance, and
  governance;
- **domain overlays:** finance and time series; and
- **architecture overlays:** retrieval, graders, and tool agents.

A source or competency naturally belongs to several axes. Treating all of them
as exclusive peers creates duplication and false impressions of coverage.

## The eight broad learning domains

### 1. Computational and quantitative foundations

First-pass objective: implement, test, and explain a simple predictive model
without hiding the calculation or data flow behind a framework.

Core topics:

- Python or another production-relevant language;
- SQL and tabular data manipulation;
- command-line and Linux fundamentals;
- Git and collaborative version control;
- data structures and basic algorithms;
- ordinary unit and integration testing;
- probability and conditional probability;
- random variables, expectation, variance, covariance, and distributions;
- sampling and estimation;
- descriptive and inferential statistics;
- linear algebra for vectors, matrices, decompositions, and projections;
- calculus and gradients at the level needed for optimization;
- optimization objectives and constraints;
- numerical precision, conditioning, and stability; and
- computational complexity and resource awareness.

These foundations should be learned in connection with working artifacts rather
than completed as an isolated mathematical prerequisite sequence.

First-pass evidence:

- a tested baseline calculation;
- a reproducible environment;
- version-controlled code and data-contract assumptions; and
- an explanation of the quantity computed and its uncertainty limits.

### 2. Purpose, product, domain, and human systems

First-pass objective: connect a prediction or generated output to the decision,
action, user, affected party, and failure it is supposed to change.

Core topics:

- problem formulation;
- domain understanding;
- non-ML and non-AI baselines;
- users, operators, and affected non-users;
- decision and action workflows;
- product, scientific, operational, and business claims;
- target quantities and intended use;
- automation level and human-AI allocation;
- success criteria and minimum useful improvement;
- failure costs and unacceptable behavior;
- feedback loops and intervention effects;
- ownership, authority, review, and escalation;
- override, appeal, recourse, and fallback;
- accessibility and capability communication; and
- stop, rollback, or retirement conditions.

Purpose must not become a brief “define the metric” exercise. Many deployed AI
systems are human-AI configurations. NIST explicitly treats human-AI
configuration, affected communities, context, and risk ownership as lifecycle
concerns in the
[AI RMF](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf).

First-pass evidence:

- a testable claim;
- a non-ML baseline;
- named users and affected parties;
- explicit failure conditions;
- human and automated decision boundaries; and
- an accountable owner and fallback.

### 3. Data engineering and information semantics

First-pass objective: explain exactly what every material record means, when it
was knowable, how it was produced, and how it reaches training and inference.

Core topics:

- data acquisition and source rights;
- entities, observations, keys, grain, units, and populations;
- labels, outcomes, annotation, and label maturity;
- schemas and semantic constraints;
- missingness and censoring;
- quality checks and anomaly detection;
- snapshots, versions, and revisions;
- event, publication, availability, ingestion, and cutoff times;
- point-in-time joins;
- selection and survivorship;
- batch, streaming, and event-driven data processing;
- storage models and query behavior;
- transformation and feature pipelines;
- fold-local learned transformations;
- provenance and derivation lineage;
- training-serving parity and skew;
- permissions, privacy, retention, and deletion; and
- synthetic, feedback, retrieved, and user-provided data where applicable.

W3C PROV provides a general entity-activity-agent model for provenance without
requiring a specific ML platform or serialization.
[PROV-DM](https://www.w3.org/TR/prov-dm/).

First-pass evidence:

- exact dataset or snapshot identity;
- entity grain, keys, units, and label definition;
- lineage and applicable permissions;
- schema and semantic checks;
- leakage tests; and
- a statement of what was knowable at the decision cutoff.

### 4. Model sourcing, development, adaptation, and experimentation

First-pass objective: establish a meaningful baseline, train a small candidate
family, and preserve enough evidence to explain and recover the selected
candidate.

Core topics:

- supervised learning:
  - regression;
  - binary and multiclass classification;
  - ranking and scoring;
- unsupervised and weakly supervised learning:
  - clustering;
  - dimensionality reduction;
  - anomaly detection;
- model families:
  - linear and generalized linear models;
  - decision trees and ensembles;
  - random forests and gradient boosting;
  - neural networks and representation learning;
- loss functions and training objectives;
- bias, variance, regularization, and capacity;
- feature engineering and representation choices;
- optimization and training dynamics;
- class imbalance and sampling policy;
- hyperparameter and architecture search;
- experiment tracking and run identity;
- baselines and comparison fairness;
- ablation and error analysis;
- build-versus-buy decisions;
- hosted models, open weights, and acquired components;
- prompting, fine-tuning, preference adaptation, distillation, calibration, and
  quantization where applicable;
- inherited limitations and provider or version change; and
- candidate freeze and selection history.

Classification for financial markets is not a separate first-level learning
domain. Classification is learned here; finance later specializes the target,
sampling, dependence, calibration, threshold, and economic-decision semantics.

First-pass evidence:

- a baseline ladder;
- exact run and configuration identities;
- recoverable transformation and model state;
- a fair candidate comparison;
- failed and neutral trials as well as successful trials; and
- a documented reason for selecting the frozen candidate.

### 5. Evaluation, inference, and decision evidence

First-pass objective: design the model's exam before serious candidate
iteration, then evaluate the frozen candidate against the actual decision and
deployment population.

Core topics:

- target population and evaluation population;
- observation, experimental, analysis, and resampling units;
- train, validation, calibration, and test ownership;
- independent and dependent data structures;
- leakage and split invariants;
- nested model selection;
- simple, incumbent, and competitive baselines;
- primary, secondary, and guardrail metrics;
- decision-relevant units and aggregation;
- uncertainty and variability sources;
- resampling and dependence-aware inference;
- important slices and failure subpopulations;
- calibration and proper scoring rules;
- decision thresholds and cost-sensitive decisions;
- construct, measurement, label, and proxy validity;
- confirmatory versus exploratory analysis;
- multiplicity and candidate-family accounting;
- adaptive holdout reuse and final evidence;
- causal identification when a causal claim is made;
- online experiments or field evidence when applicable;
- minimum useful improvement and decision rules; and
- claim-scoped limitations and safe failure.

Evaluation should bracket model development:

```text
evaluation contract preview
→ model development and selection
→ candidate freeze
→ final evaluation and decision evidence
```

This prevents the candidate from defining its own exam.

First-pass evidence:

- frozen evaluation ownership;
- split and leakage invariants;
- an independent metric or mechanical oracle;
- baseline-relative results;
- appropriately scoped uncertainty;
- untouched evidence or a valid reuse protocol; and
- explicit claim and limitation boundaries.

### 6. Software, platform, and inference engineering

First-pass objective: make another process exercise the same frozen
model-transform-policy unit through a tested interface under realistic resource
constraints.

This domain contains three distinct pillars.

#### 6.1 Software engineering

- modular design and responsibility boundaries;
- APIs and service or batch contracts;
- configuration and precedence;
- version control and review;
- dependency and environment management;
- packaging and build behavior;
- unit, integration, property, differential, and end-to-end tests;
- logging and error behavior;
- compatibility and migrations;
- maintainability and technical debt; and
- secure software-development practices.

#### 6.2 Distributed and platform engineering

- compute, storage, and networking;
- concurrency, consistency, and coordination;
- queues, streams, and event processing;
- caching and materialization;
- retries, idempotency, and deduplication;
- orchestration and scheduling;
- checkpointing, replay, and reconciliation;
- accelerators and heterogeneous compute;
- scaling and failure isolation;
- batch and streaming platforms;
- data and model artifact stores; and
- resource allocation and cost control.

#### 6.3 Inference and runtime engineering

- batch, request, streaming, and edge inference;
- model loading, routing, and version selection;
- preprocessing and postprocessing parity;
- latency and throughput;
- batching, caching, and scheduling;
- memory behavior and numerical precision;
- availability and graceful degradation;
- rate limiting and load shedding;
- capacity planning;
- unit cost and energy; and
- quality-latency-cost tradeoffs.

First-pass evidence:

- tested interfaces;
- environment and dependency identity;
- train-inference parity checks;
- malformed-input and failure behavior;
- artifact integrity; and
- basic latency, memory, and capacity observations.

### 7. Delivery, operations, reliability, and evolution

First-pass objective: distinguish producing a releasable candidate from
controlling an active system, and understand how the system changes, fails,
recovers, and retires.

#### 7.1 Delivery and release engineering

- experiment-to-candidate-to-release transitions;
- immutable candidate and release identities;
- artifact lineage and dependency identity;
- CI/CD and continuous-training distinctions;
- validation and promotion gates;
- compatibility and migration checks;
- batch activation, shadowing, canaries, and controlled experiments;
- rollout units and exposure limits;
- release authority; and
- rollback-unit design.

#### 7.2 Operations, reliability, and evolution

- service-level objectives and indicators;
- system, data, and model observability;
- mature-outcome monitoring;
- drift and shift as diagnostic signals;
- incidents, triage, containment, and communication;
- fallback, rollback, replay, and reconciliation;
- field feedback and corrective action;
- refresh and retraining as new candidate generation;
- adaptive and online state;
- dependency and provider change;
- capacity and cost monitoring;
- post-incident learning; and
- retirement and decommissioning.

First-pass evidence for a learning project can remain proportionate: a
demonstrated rerun, explicit candidate identity, and documented monitoring and
fallback concepts may be sufficient. Live rollout machinery activates only for
production-bound or fielded work.

### 8. Trust, security, privacy, safety, and governance

First-pass objective: recognize which exposures and impact conditions activate
additional controls, distinguish technical evidence from authorization, and
identify the owner of unresolved risk acceptance.

Keep the following sublanes visibly distinct.

#### 8.1 Security and supply chain

- threat modeling;
- least privilege and access control;
- secrets and credential handling;
- dependency and artifact provenance;
- software, model, and data supply chains;
- acquired components and hosted providers;
- untrusted inputs and outputs;
- poisoning, evasion, extraction, and abuse;
- prompt and resource injection where applicable;
- denial of service and resource abuse; and
- incident response and recovery.

#### 8.2 Privacy and data protection

- sensitive and personal data;
- collection and purpose limits;
- consent and permitted use;
- retention and deletion;
- access and disclosure;
- memorization and extraction;
- privacy-preserving methods where appropriate; and
- jurisdiction- and context-specific obligations.

#### 8.3 Safety, robustness, fairness, and affected parties

- plausible misuse and failure modes;
- robustness under relevant perturbations;
- high-impact and safety-critical exposure;
- harmful bias and disparate effects;
- important affected populations;
- human oversight and intervention;
- appeal, recourse, and override; and
- communication of limitations.

#### 8.4 Governance and accountability

- roles and decision authority;
- review independence and effective challenge;
- documentation and traceable decisions;
- risk tolerance and residual-risk ownership;
- policy and legal applicability;
- vendor and third-party governance;
- records and auditability; and
- change, incident, and retirement responsibility.

NIST treats governance as cross-cutting rather than a final checklist, and
separately exposes validity, safety, security, resilience, transparency,
privacy, explainability, and fairness characteristics.
[NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/).

## The mandatory assurance spine

Testing, provenance, documentation, reproducibility, reliability, resource
economics, and ownership should not become optional late-stage subjects. They
must be evidenced across their owning domains.

| Domain | Minimum assurance evidence |
|---|---|
| Foundations | Tested calculations, recoverable environment, version-controlled work |
| Purpose and product | Testable claim, baseline, failure conditions, human and owner boundaries |
| Data | Snapshot identity, lineage, schema checks, leakage and point-in-time tests |
| Model development | Run identity, frozen configuration, baseline comparison, repeatability |
| Evaluation | Split invariants, independent metric oracle, untouched evidence, uncertainty |
| Software and platform | Unit and integration tests, train-inference parity, artifact integrity, resource behavior |
| Delivery and operation | Release identity, telemetry, fallback, rollback, replay, incident evidence |
| Trust and governance | Threat tests, authorization boundaries, privacy and abuse controls, residual-risk owner |

The cross-cutting lenses are:

1. **Provenance, reproducibility, and documentation**
   - provenance and lineage are primarily owned by data and delivery;
   - artifact recoverability spans data, modeling, and software;
   - computational reproducibility is established through model-development
     and evaluation reruns;
   - replicability primarily concerns research and evaluation claims; and
   - documentation is produced by each domain rather than delegated to one
     universal document owner.

2. **Testing, assurance, and reliability**
   - every boundary earns the tests appropriate to its failure modes;
   - structural tests do not prove statistical or semantic validity;
   - offline model metrics do not prove field reliability; and
   - monitoring does not substitute for pre-release evidence.

3. **Resource economics and sustainability**
   - performance, capacity, latency, cost, compute, energy, and storage are
     considered in product, model, platform, delivery, and operating decisions;
   - financial transaction costs are a domain-specific projection, not the
     whole resource-economics topic.

4. **Accountability and process**
   - ownership, handoffs, review independence, change authority, on-call and
     incident learning, and retirement responsibility remain visible;
   - “cross-cutting” must not mean ownerless ceremony.

## Modern AI-engineering pathway

Modern AI engineering is not one optional `GenAI` appendix. Several concerns
are integrated into the eight-domain core:

- purpose includes human-AI configuration and autonomy;
- data includes training, adaptation, retrieval, user, synthetic, and feedback
  data plus provenance and rights;
- modeling includes foundation-model sourcing, hosted APIs, open weights,
  adaptation, inherited limitations, and provider change;
- evaluation includes component, composed-system, human-system, safety, and
  operational evidence;
- software and inference include prompts and context as system components,
  provider interfaces, routing, quality-latency-cost tradeoffs, and complete
  behavior-bearing configuration identity; and
- trust includes attack surfaces across models, prompts, context, tools,
  outputs, providers, and users.

The [Stanford foundation-model report](https://crfm.stanford.edu/report)
separately surfaces modeling, adaptation, data, systems, evaluation, security,
and human interaction. NIST's current GenAI profile treats data privacy,
intellectual property, confabulation, human-AI configuration, and value-chain
integration as distinct material concerns.
[NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf).

Every AI-engineering learner should also receive baseline conceptual literacy
in the following two architectural modules. Deep implementation controls
activate when the system actually has the capability.

### AI module A: retrieval, context, and memory

- corpus and knowledge-source selection;
- source permissions and access control;
- chunking and indexing;
- embeddings, retrieval, and reranking;
- freshness and provenance;
- context construction and conflict handling;
- citations and evidence grounding;
- conversation and durable memory;
- retrieved-data privacy and injection risk;
- answerability and abstention;
- retrieval-versus-generation diagnostics; and
- component and end-to-end evaluation.

RAG is one implementation family in this module, not the name of the entire
topic. The original RAG paper establishes the composition of parametric and
non-parametric memory in that method family.
[Lewis et al.](https://proceedings.nips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html).

### AI module B: agents, tools, and action

- workflow orchestration and planning;
- world, conversation, and task state;
- tool schemas and contracts;
- identity and permissions;
- confirmation and authorization requirements;
- side effects and forbidden actions;
- retries and idempotency;
- required and forbidden trajectory events;
- insufficient information and clarification;
- reconciliation and recovery;
- sandboxing and containment;
- prompt and resource injection;
- final-state correctness and policy adherence;
- repeated-run reliability; and
- end-to-end observability.

NIST's adversarial-ML taxonomy provides current vocabulary for direct prompting
attacks, indirect prompt injection, attacker resource control, poisoning,
privacy compromise, and security-utility tradeoffs.
[NIST AI 100-2e2025](https://www.nist.gov/publications/adversarial-machine-learning-taxonomy-and-terminology-attacks-and-mitigations-0).

### Later AI specialization map

After broad literacy, conditional specializations may include:

- NLP, vision, speech, audio, and multimodal systems;
- ranking, recommendation, and feedback-mediated systems;
- reinforcement learning and sequential decision systems;
- adaptive and online learning;
- weak-label, anomaly, and self-supervised systems;
- causal ML and online experimentation;
- federated and privacy-preserving ML;
- edge and intermittently connected systems; and
- safety-critical or regulated AI systems.

These are overlays on the common core rather than alternative foundations.

## Financial markets, quantitative ML, and fintech pathway

Finance should be one specialization umbrella. Time-series validation,
backtesting, and execution remain distinct second-level subjects, but they
should not occupy three peer positions in the universal MLE taxonomy.

Recommended order:

```text
markets, instruments, and institutions
→ point-in-time financial data
→ financial econometrics and predictive modeling
→ portfolio construction and risk
→ market microstructure and execution
→ strategy backtesting and search validity
→ fintech systems and model risk
```

Microstructure precedes backtesting because an execution-aware backtest cannot
be designed before the execution model is understood.

### Finance module 1: markets, instruments, and institutions

- equities and other major instrument families;
- exchanges, brokers, venues, and market sessions;
- orders and basic matching or execution mechanics;
- returns, wealth, cash, leverage, and benchmarks;
- dividends, corporate actions, delistings, and shorting;
- securities and identifier mappings;
- basic accounting and financial-statement structure; and
- market participants, incentives, and institutional constraints.

The initial goal is not advanced market microstructure. It is enough domain
understanding to avoid impossible return, price, and execution assumptions.

### Finance module 2: financial data and point-in-time research datasets

- historical investable universes;
- listings, delistings, and index membership;
- security and symbol identity over time;
- event, filing, publication, vendor-availability, and ingestion times;
- revision, restatement, and vintage identity;
- fiscal-period alignment;
- corporate actions, dividends, and split adjustments;
- trading halts and market-session eligibility;
- short availability and borrowability;
- alternative-data provenance and permissions;
- prediction cutoff; and
- earliest executable decision and fill time.

This is a finance specialization of the common data contract, not a replacement
for general data engineering.

### Finance module 3: financial econometrics, time series, and predictive modeling

- return, volatility, event, and cross-sectional targets;
- forecast origins and horizons;
- rolling and expanding evaluation;
- temporal, entity, and panel dependence;
- overlapping outcomes and label intervals;
- regression and classification for markets;
- ranking and cross-sectional scoring;
- probability estimation and calibration;
- feature timing and maturity;
- structural breaks and regimes;
- event studies and forecast comparison;
- baseline forecasts;
- horizon-specific loss and uncertainty; and
- prospective versus ex-post state or regime labels.

Classification is specialized here through the target and decision:

- direction or sign classification;
- event occurrence;
- default or credit outcomes;
- fraud and anomaly decisions;
- volatility or regime states;
- trade or allocation eligibility; and
- calibrated probability or ranking decisions.

The learner must preserve temporal and decision semantics rather than merely
apply a classifier to shuffled market rows.

### Finance module 4: portfolio construction and risk

This was the most important finance omission from the earlier 14-topic list.

- translating forecasts, probabilities, or scores into positions;
- diversification;
- covariance and correlation;
- factor and sector exposures;
- benchmark-relative risk;
- leverage, concentration, and turnover;
- liquidity and participation constraints;
- drawdown and tail risk;
- risk-adjusted performance;
- portfolio attribution; and
- rebalancing and constraint handling.

A predictive model does not uniquely determine an investable portfolio.
Portfolio selection is a separate decision problem. Markowitz's portfolio-
selection paper is the foundational source for the expected-return and
variance formulation.
[Markowitz](https://doi.org/10.1111/j.1540-6261.1952.tb01525.x).

### Finance module 5: market microstructure, execution, costs, and capacity

- order types and venues;
- bid-ask spreads and liquidity;
- fills, partial fills, cancellations, and unfilled orders;
- slippage and market impact;
- latency and time-of-day effects;
- short availability, borrow, and recalls;
- funding and financing;
- turnover and participation;
- target AUM and strategy capacity;
- execution benchmarks; and
- market-, venue-, scale-, style-, and period-specific cost models.

Larry Harris treats market structure, orders, liquidity, transaction-cost
measurement, and performance evaluation as one coherent practitioner body.
[Trading and Exchanges](https://academic.oup.com/book/52292).

### Finance module 6: quantitative strategy backtesting and search validity

- signal-to-order-to-fill chronology;
- frozen refit, recalibration, threshold, rebalance, and portfolio policies;
- rolling-origin outer evaluation;
- inner model and policy selection;
- overlapping labels and information intervals;
- purge, gap, and embargo controls;
- complete research-search records;
- adaptive selection and holdout reuse;
- multiple testing and candidate-family accounting;
- gross-versus-net candidate selection;
- transaction cost and capacity integration;
- dependence-aware performance uncertainty;
- untouched evidence;
- strategy baselines; and
- Reality Check, SPA, PBO, and DSR as distinct named methods.

Rolling-origin evaluation preserves chronology and supports horizon-specific
assessment, but it does not establish investability by itself.
[Hyndman and Athanasopoulos](https://otexts.com/fpp3/tscv.html).

Backtesting evaluates the intended data-to-position-to-order-to-fill procedure,
not merely a classifier score. No backtest statistic repairs point-in-time
errors, a missing search family, or unrealistic execution.

### Finance module 7: fintech systems, model risk, and regulatory context

Survey-level topics:

- brokerage, exchange, and market-data APIs;
- ledgers, reconciliation, and money movement;
- payments and settlement;
- credit scoring and underwriting;
- fraud, AML, KYC, sanctions, and surveillance;
- customer-facing financial applications;
- financial NLP and document processing;
- compliance and regulatory technology;
- model inventory and ownership;
- independent model validation and effective challenge;
- ongoing testing and monitoring;
- security, privacy, records, and auditability;
- third-party models and vendors; and
- jurisdiction-, institution-, product-, and use-specific obligations.

FINRA identifies model risk management, data governance, customer privacy,
cybersecurity, vendor management, books and records, and supervisory controls
as relevant considerations for AI in securities firms.
[FINRA AI considerations](https://www.finra.org/rules-guidance/key-topics/fintech/report/artificial-intelligence-in-the-securities-industry/key-challenges).

Detailed compliance is not a universal curriculum checklist. It must be
refreshed for the applicable jurisdiction, institution, product, role, and use.

## Mapping the original 14 topics into the new structure

| Original topic | New owner |
|---|---|
| Purpose and problem formulation | Domain 2: purpose, product, domain, and human systems |
| Data semantics and point-in-time correctness | Domain 3, with deeper temporal and finance projections |
| Provenance, documentation, and reproducibility | Mandatory assurance spine; primarily data, modeling, evaluation, software, and delivery |
| Experiment design and model selection | Domains 4 and 5 |
| Statistical inference and uncertainty | Foundations plus Domain 5 |
| Time-series forecasting and temporal validation | Domain 5 literacy plus finance or temporal-system specialization |
| Financial backtesting and strategy-search validity | Finance module 6 |
| Execution, transaction costs, and capacity | Finance module 5; general capacity and cost also belong to Domains 6 and 7 |
| Probabilities, calibration, and thresholds | Domain 5 |
| Causal inference, measurement, and proxy validity | Domain 5, with causal depth activated by causal claims |
| ML testing and system reliability | Mandatory assurance spine plus Domains 6 and 7 |
| Delivery, monitoring, adaptation, and incidents | Domain 7, with delivery and operation retained as separate pillars |
| Risk, security, governance, and affected parties | Domain 8 plus Domain 2 human-system framing |
| Generative AI, RAG, graders, and tool agents | AI concerns integrated across the core, plus retrieval/context and agent/tool modules |

## Source-catalog design

### Decision

Keep one canonical record per exact citable source and substantive version. Do
not require one exclusive semantic primary topic.

The catalog should support:

- multi-valued controlled subjects;
- claim-level authority roles;
- exact vocabulary and source anchors;
- applicability and limits;
- workflow-seam mappings;
- exact edition or version identity; and
- separate learning paths.

The W3C Data Catalog Vocabulary permits resources to have multiple themes, and
SKOS supports concept schemes with broader, narrower, and related relations
without forcing every interdisciplinary concept into one exclusive parent.
[DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) and
[SKOS](https://www.w3.org/TR/skos-reference/).

### Catalog invariants

```text
source facts live once
claim judgments live once
subject membership is multi-valued
learning order lives in paths
topic views contain references, not copies
```

### Source identity

`One source record` means one exact publication, edition, report, standard
version, or substantively distinct revision. It does not mean:

- one author;
- one family of papers;
- one title across several editions;
- one publisher landing page; or
- one bibliography entry that combines several methods.

Publisher pages, DOI resolvers, proceedings copies, and author manuscripts may
be locators for one record only when their content identity is established.

### Lean source record

```yaml
source_id: SRC-####
citation:
  title:
  creators:
  date:
  type:
  version:
  persistent_id:

locators: []
inspected_at:
subjects: []

claims:
  - claim_id: C1
    statement:
    authority_role:
      definition | governing | method | empirical | practitioner
    source_anchor:
    exact_terms: []
    applies_when:
    limits:
    workflow_seams: []
```

Minimum semantics:

- `source_id` identifies one exact citable source and version;
- `citation.version` prevents hybrid records across editions;
- `persistent_id` is a DOI, ISBN plus edition, report number, or equivalent;
- `subjects` is the only stored topical classification and is multi-valued;
- `authority_role` applies to a claim rather than being laundered across the
  entire publication;
- `source_anchor` identifies the section, page, table, equation, or other direct
  support;
- `applies_when` records the relevant population, method, system, period, or
  trigger;
- `limits` prevents unsupported transfer; and
- `workflow_seams` maps the claim to stable semantic owners rather than mutable
  line numbers.

Only catalog claims selected for learning or future workflow distillation. Do
not attempt to summarize every assertion in every source.

### Keep outside source records

- learning order and prerequisites;
- curriculum stage;
- implementation backlog status;
- skill-change or deployment status;
- duplicated topic summaries;
- prestige, popularity, or universal importance scores;
- people-to-follow lists;
- complete abstracts and biographies;
- exhaustive keywords;
- a mandatory `primary_topic` or `home_topic`;
- broad concept graphs before a retrieval need exists;
- refresh fields before a mutable-source case exists; and
- revision relations before a second substantive version exists.

Optional fields should be earned by observed need. Add a display-only
`home_topic` only if navigation cannot choose a shelf without it, and define it
as the first learning-path placement rather than the source's exclusive
subject.

### Learning paths and views

Recommended separation:

```text
docs/research/skills/mle-workflow/
  catalog.md
  sources/
    SRC-....md
  learning-paths/
    core.md
    ai-engineering.md
    finance-fintech.md
  existing dated research notes
```

This is a proposed future layout, not a currently authorized mutation.

`catalog.md` should be a thin generated or mechanically validated index.
Learning paths should contain source IDs, sequence, prerequisites, and a short
rationale. Topic and overlay views should contain references, not copied source
records or repeated claim prose.

### Reading progress versus competency progress

Track these separately.

Source-consumption state:

```text
queued
→ triaged
→ selected sections read
→ distilled
→ refreshed
```

Competency state:

```text
0 unknown
1 recognize and define
2 explain assumptions and common failures
3 apply with guidance
4 independently design, execute, and audit
```

Do not use page percentage as a mastery measure. `Read` does not mean `can
apply`. Advancement should include retrieval or teach-back plus an inspectable
exercise or artifact.

## Broad-first learning progression

Use a spiral rather than mastering each domain in isolation.

### Pass 1: a small reproducibility-bound predictive project

1. implement and test a simple baseline;
2. state the user or research question and decision;
3. define entity grain, keys, labels, and data cutoff;
4. freeze an evaluation preview before serious model iteration;
5. train one or two ordinary model families;
6. preserve run identity and error analysis;
7. evaluate the frozen candidate with an independent metric check;
8. expose it through a tested batch boundary; and
9. document applicable risks and limitations.

This pass should touch Domains 1 through 7 and identify Domain 8 triggers. It
does not require production deployment.

### Pass 2: engineering depth

- strengthen software architecture and automated tests;
- build a data pipeline and lineage record;
- add experiment and artifact tracking;
- study distributed and platform fundamentals;
- test inference parity and resource behavior;
- package an immutable candidate;
- understand release, monitoring, fallback, rollback, and incident concepts;
- perform security and privacy threat modeling; and
- preserve a complete evidence receipt.

### Pass 3: finance and fintech pathway

Build a point-in-time financial prediction project, then extend it through:

- portfolio translation and risk;
- market microstructure and execution assumptions;
- net strategy backtesting;
- complete search-family accounting;
- dependence-aware performance inference; and
- survey-level fintech operation and model risk.

### Pass 4: modern AI-engineering pathway

Build a composed AI application and study:

- acquired model and adaptation choices;
- prompt, context, retrieval, and memory identity;
- component and composed-system evaluation;
- model-grader limitations;
- human interaction and oversight;
- tool authority, state, and recovery;
- inference latency and cost;
- complete observability; and
- prompt, resource, data, model, and provider security boundaries.

The finance and AI pathways can proceed in either order after the common core.

## Claim ledger

### C1. The original 14 topics are insufficient as a universal learning taxonomy

**Status: supported as synthesis.**

The list omits or compresses several distinct competencies exposed by CS2023,
industrial ML lifecycle research, ML-systems research, SRE, and the canonical
workflow. It also elevates finance-specific and architecture-specific branches
to peer status with general foundations. No cited source claims that the exact
eight-domain alternative is uniquely correct.

Answer impact: retain the original list as a research and routing view, but do
not use it as the only professional curriculum.

### C2. Eight learning domains plus assurance and specializations provide a broad-first surface

**Status: supported as labeled synthesis.**

Every supplied original topic maps to at least one of the eight domains,
assurance lenses, or pathways. The added domains close the independently
identified gaps in programming, quantitative methods, software, data,
distributed systems, model development, inference, product/human factors, and
portfolio risk.

Answer impact: use the eight domains for navigation and learner competency;
retain lifecycle seams as catalog metadata.

### C3. Finance should be one specialization with distinct internal modules

**Status: supported.**

Forecast validation does not establish strategy validity, prediction does not
determine portfolio construction, and backtest validity depends on executable
market assumptions. These distinctions are supported by forecasting,
portfolio-selection, backtesting, and market-microstructure sources cited in
the finance pathway.

Answer impact: keep time series, portfolio/risk, microstructure/execution, and
backtesting distinct within finance, but not as universal MLE peer domains.

### C4. Modern AI concerns must be integrated into the core rather than isolated in one GenAI bucket

**Status: supported.**

Foundation-model sourcing, adaptation, human interaction, composed-system
evaluation, inference economics, component dependencies, and security span the
common system. Retrieval and tools add specific context, authority, state, and
effect boundaries.

Answer impact: integrate common AI responsibilities into Domains 2 through 8;
use retrieval/context and agents/tools as conditional architectural modules.

### C5. Source classification must be many-to-many and claim-addressable

**Status: supported.**

Interdisciplinary sources legitimately cover several subjects and may play
different authority roles for different claims. DCAT and SKOS permit
multi-theme and polyhierarchical classification. The research skill requires
authority and applicability to be judged per claim.

Answer impact: do not require one semantic primary topic; store source facts
once and attach multi-valued subjects and claim-level evidence judgments.

## Material alternatives and rejected structures

### Flat 14-topic list

Useful for the existing evidence map, but rejected as the complete learning
taxonomy because it mixes axes and underrepresents general engineering.

### Six workflow seams plus cross-cutting lenses

This was the strongest alternative:

1. purpose and human system;
2. data, labels, and measurement;
3. model development;
4. evaluation and decision evidence;
5. software, platform, and serving; and
6. release, operation, change, and retirement.

It is excellent for workflow and source-to-skill mapping. It was not selected
as the learner-facing top level because quantitative prerequisites, reliability,
and trust competencies could become less visible. Those six seams should remain
an available lifecycle view over the same source records.

### Lifecycle-only taxonomy

Rejected as the only view because `data → train → deploy → monitor` hides
persistent competencies such as software design, distributed systems,
security, human interaction, and statistical foundations.

### Tool or platform taxonomy

Rejected because it ages quickly and confuses implementations with durable
concepts. Spark, Kubernetes, MLflow, cloud services, model providers, vector
databases, and agent frameworks may be examples or exercises, not first-level
knowledge domains.

### Strict one-primary-topic catalog

Rejected because it creates false exclusivity and encourages authority to be
assigned to a publication rather than to the exact claim it supports.

## Limits and empirical remainder

- No source owns or empirically proves the exact eight-domain taxonomy.
- This packet supports organization; it does not prove that this curriculum
  produces better MLEs or AI engineers than an alternative curriculum.
- Depth expectations depend on target role. A research scientist, data
  engineer, platform engineer, applied AI engineer, quantitative researcher,
  and production MLE will specialize differently.
- Not every project activates every lifecycle stage, assurance control, AI
  module, or finance module.
- Production tooling should be proportional to the requested transition;
  learning the concept does not require deploying every project.
- Mathematical topics are load-bearing, but the taxonomy does not prescribe a
  complete mathematics syllabus.
- Security, privacy, regulations, standards, provider behavior, and market
  mechanics are mutable and require current verification.
- Detailed compliance is owner-, jurisdiction-, institution-, product-, and
  use-specific.
- Books and courses are synthesis and exercise sources; they do not replace
  original papers, specifications, standards, or governing text as claim
  owners.
- A source catalog does not establish mastery. Reading and competency evidence
  must remain separate.
- The catalog structure itself has not been implemented or behaviorally
  evaluated.

## Repository mapping

The current canonical `mle-workflow` already owns many lifecycle seams:

- purpose and delivery classification;
- system and delivery contracts;
- data and feature contracts;
- traceable experiments;
- an Evaluation Contract and conditional inference branches;
- error analysis and test portfolios;
- immutable candidate promotion;
- operation, refresh, incidents, rollback, and retirement; and
- capability-triggered risk branches.

The main gap addressed by this packet is not an established defect in the
workflow. It is a difference between:

- a workflow for executing valid ML work; and
- a learner-facing map of the wider competencies needed for MLE and AI-
  engineering roles.

Any future workflow, catalog, or curriculum edit requires separate authority.
This packet does not authorize changing the skill, synchronizing its installed
mirror, creating source-record directories, staging, committing, or publishing.

## Source identity and copy fidelity

The debate used the canonical repository files at the recorded commit, the
existing primary-source packet, official standards and frameworks, original or
publisher-hosted papers, and stable scholarly or author-hosted copies. Sources
were treated as authoritative only for their own definitions, contracts,
methods, reported studies, or practitioner guidance. No marketplace entry,
community skill, search snippet, or unsourced summary was used as a load-bearing
authority.

## Stopping basis

Six independent lanes completed an initial argument and a cross-examination
round. The final structure covers every original topic, every independently
identified professional gap, the common MLE lifecycle, modern AI system
boundaries, the requested finance and fintech surface, cross-cutting assurance,
and a non-duplicative catalog design. The remaining alternative concerns the
choice of learner-facing view, not missing subject matter. Additional domain-
specific sources would refine pathway depth without changing the broad
organization.

Tracked mutation: creation of this note only.

Caller-use boundary: this packet supports future curriculum, research,
distillation, and catalog decisions. It does not implement the catalog, decide
skill wording, establish behavioral efficacy, authorize installation or Git
delivery, or support financial profitability claims.

Return owner: the user and future root author of `mle-workflow` research.

Next: none.
