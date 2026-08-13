---
artifact_id: RP-mle-ai-primary-sources-20260812-01
---

# MLE and AI Primary-Source Distillation Map

## Research contract

- Question: Which books, authors, papers, standards, and practitioner sources
  are worth distilling to support the methodology and vocabulary in the
  canonical `mle-workflow`, with special attention to financial time-series
  ML, stock-strategy research, and backtesting?
- Caller use: choose a source-backed learning and future skill-maintenance
  backlog without treating community skill text, books, or frameworks as
  correctness authority by themselves.
- Scope: the concept families currently owned by `skills/extra/mle-workflow`,
  including purpose, data timing and provenance, experiments, evaluation,
  statistical validity, promotion, operation, and conditional generative-AI
  risks. The finance lane covers forecasting, stock selection, strategy search,
  backtesting, execution, costs, capacity, and performance inference.
- Exclusions: a general survey of all MLOps or AI literature, algorithm
  tutorials, personalized investment advice, strategy selection, profitability
  claims, fixed universal thresholds, and implementation of skill changes.
- Applicable repository state: commit
  `9ddb58a34ad363b7ce3bfac56430ee9eda56cad8`, inspected on 2026-08-12.
- Freshness: sources were inspected on 2026-08-12. Fixed papers and books are
  cited at their named editions. NIST AI RMF 1.0 is under revision; current
  standards, regulations, vendor behavior, security taxonomies, and market
  mechanics require a project-time refresh.
- Authorized mutation: create this note only.
- Return owner: the user and future root author of `mle-workflow`.

## Answer

The current workflow is methodologically strong and broadly aligned with
primary and field-standard sources. It does not need a conceptual replacement.
The highest-value distillation work is to:

1. attribute named concepts to their actual owners;
2. label repository-created terms as local synthesis;
3. correct the reproducibility vocabulary;
4. make statistical units, uncertainty, causal assumptions, and multiplicity
   targets more exact; and
5. add a lean, conditional finance branch for point-in-time investability,
   complete search-family accounting, net executable economics, dependence-
   aware inference, and prospective regime claims.

Static correspondence is mostly **aligned**. The reproducibility terminology is
**materially different** from the clearest cross-disciplinary definitions.
Runtime behavior and empirical efficacy remain **unknown**: source alignment
does not show that skill wording changes agent behavior, and no workflow can
establish strategy profitability without applicable untouched evidence and
realistic execution.

## Vocabulary audit

### Established vocabulary already used well

- forecast origin and forecast horizon;
- rolling-origin or rolling forecasting-origin evaluation;
- point-in-time data eligibility;
- event, availability, ingestion, and prediction-cutoff times;
- data leakage and training-serving skew;
- nested cross-validation;
- selection bias and adaptive overfitting;
- proper scoring rules and calibration;
- construct and proxy validity;
- estimand or target quantity;
- multiplicity, family-wise error rate, and false discovery rate;
- concept drift and dataset shift;
- purging, gap, and embargo; and
- data snooping, survivorship bias, transaction costs, and market impact.

### Terms that need attribution or qualification

- `Purpose Lock`, `Delivery Contract`, `Evaluation Contract`, delivery classes,
  evidence rungs, and `test-exhausted` are repository-native synthesis. They
  should not be attributed verbatim to NIST, Google, or statistical literature.
- The field normally describes the risk behind `final-test exhaustion` as
  **adaptive reuse**, **holdout reuse**, **adaptive overfitting**, or **selection
  bias**. Restricted-feedback and reusable-holdout methods are valid exceptions
  to a blanket rule that any result viewing permanently exhausts a test set.
  Sources: [Dwork et al.](https://pubmed.ncbi.nlm.nih.gov/26250683/) and
  [Blum and Hardt](https://proceedings.mlr.press/v37/blum15.html).
- `Nested ownership` is useful local shorthand. When cross-validation is
  literally used, prefer **nested CV: inner model selection and outer
  performance evaluation**. Nested CV reduces selection bias but does not make
  fold estimates independent or automatically supply valid uncertainty.
  Sources: [Varma and Simon](https://pubmed.ncbi.nlm.nih.gov/16504092/),
  [Cawley and Talbot](https://jmlr.org/papers/v11/cawley10a.html), and
  [Bengio and Grandvalet](https://www.jmlr.org/papers/v5/grandvalet04a.html).
- The current `artifact reproducibility` versus `result reproducibility`
  distinction should become:
  - **artifact recoverability**: exact code, inputs, configuration, environment,
    and outputs can be retrieved;
  - **computational reproducibility**: rerunning with the same data, methods,
    code, and conditions yields consistent results; and
  - **replicability**: a new study or new data addresses the same scientific
    question.
  Because disciplines use conflicting conventions, the workflow should also
  describe the exact operation rather than rely on `reproducible` alone.
  Sources: [National Academies](https://nap.nationalacademies.org/read/25303/chapter/6)
  and [current ACM artifact terminology](https://prod-www.acm.bloomreach.cloud/publications/policies/artifact-review-and-badging-current).
- For forecasting literature, prefer **rolling forecasting origin**.
  `Walk-forward validation` is common practitioner wording but less exact.
- Ordinary K-fold CV is not universally invalid for time series. It can be
  valid for a narrower class of autoregressive models with uncorrelated errors.
  Financial strategies usually add chronology, nonstationarity, overlapping
  outcomes, portfolio dependence, and deployment-policy concerns that make
  temporal outer evaluation the safer default. Source:
  [Bergmeir, Hyndman, and Koo](https://robjhyndman.com/publications/cv-time-series/).
- `Reality Check`, `SPA`, `PBO`, `CSCV`, `DSR`, `purging`, `embargo`, `CPCV`,
  `triple-barrier`, and `meta-labeling` are named methods. Preserve their
  authors, assumptions, inputs, and validation targets rather than generalize
  them into universal requirements.
- Confirmatory comparisons should name their multiplicity target. **FWER**
  usually fits individually claim-bearing confirmatory families; **FDR** answers
  a different discovery-oriented question. Sources:
  [Holm](https://www.jstor.org/stable/4615733) and
  [Benjamini and Hochberg](https://www.math.tau.ac.il/~ybenja/MyPapers/benjamini_hochberg1995.pdf).
- Causal branches should name **exchangeability** and **consistency** alongside
  positivity and strategy-specific identification assumptions. Source:
  [Hernán and Robins](https://miguelhernan.org/s/hernanrobins_WhatIf_2jan25.pdf).
- Calibration evidence should emphasize a flexible calibration curve with
  uncertainty and sample support. Bin counts alone are support metadata, and
  an aggregate Brier or log score is not calibration-only evidence. Sources:
  [Gneiting and Raftery](https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf)
  and [Van Calster et al.](https://bmcmedicine.biomedcentral.com/counter/pdf/10.1186/s12916-019-1466-7.pdf).

## Priority 0: financial time-series and backtesting sources

### Forecast evaluation and temporal dependence

1. **Rob Hyndman and George Athanasopoulos, _Forecasting: Principles and
   Practice_.** Best starting point for forecast origin, horizon, naïve
   baselines, rolling-origin evaluation, expanding versus rolling windows,
   forecast errors, and probabilistic forecasts.
   [Book](https://otexts.com/fpp3/) and
   [time-series cross-validation chapter](https://otexts.com/fpp3/tscv.html).

2. **Leonard Tashman, “Out-of-Sample Tests of Forecasting Accuracy.”**
   Foundational treatment of rolling origins, multiple evaluation periods, and
   recalibration. [Paper](https://doi.org/10.1016/S0169-2070(00)00065-0).

3. **Francis Diebold and Roberto Mariano; Raffaella Giacomini and Halbert
   White; Raffaella Giacomini and Barbara Rossi.** These papers own central
   vocabulary for loss differentials, relative and conditional predictive
   ability, dependence-aware comparison, and changing relative performance.
   Sources: [Diebold-Mariano](https://doi.org/10.1080/07350015.1995.10524599),
   [Giacomini-White](https://doi.org/10.1111/j.1468-0262.2006.00718.x), and
   [Giacomini-Rossi](https://doi.org/10.1002/jae.1177).

4. **Shihao Gu, Bryan Kelly, and Dacheng Xiu, “Empirical Asset Pricing via
   Machine Learning.”** Strong stock-ML exemplar using disjoint temporally
   ordered training, validation, and testing periods. The authors explicitly
   treat validation as part of selection rather than truly untouched evidence.
   [Paper](https://academic.oup.com/rfs/article/33/5/2223/5758276).

### Strategy search and multiplicity

5. **Robert Arnott, Campbell Harvey, and Harry Markowitz, “A Backtesting
   Protocol in the Era of Machine Learning.”** Closest single source to a
   finance-specific Purpose Lock and Evaluation Contract: economic rationale,
   selection history, limited effective sample, holdout integrity,
   interpretability, and costs.
   [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3275654).

6. **Halbert White, “A Reality Check for Data Snooping,” and Peter Hansen, “A
   Test for Superior Predictive Ability.”** These own benchmark-versus-family
   inference under dependence. SPA improves power when many poor alternatives
   dilute the Reality Check. Neither method repairs leakage, unrealistic costs,
   or an incomplete candidate family.
   [White](https://doi.org/10.1111/1468-0262.00152) and
   [Hansen](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=264569).

7. **David Bailey, Jonathan Borwein, Marcos López de Prado, and Qiji Zhu,
   “The Probability of Backtest Overfitting.”** Distill for complete strategy-
   family accounting and selection instability. PBO estimates how often the
   in-sample winner ranks below the out-of-sample median; it is not a p-value or
   proof of profitability.
   [Paper](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf).

8. **David Bailey and Marcos López de Prado, “The Deflated Sharpe Ratio.”**
   Distill for finite-sample Sharpe uncertainty, non-normal returns, and trial
   multiplicity. The effective number of independent trials is the most
   assumption-sensitive input. DSR does not repair look-ahead, survivorship,
   serial dependence, or cost errors.
   [Paper](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf).

9. **Campbell Harvey, Yan Liu, and Heqing Zhu, “…and the Cross-Section of
   Expected Returns.”** Strong finance-specific evidence that ordinary single-
   test thresholds do not survive large factor and strategy searches. Import
   the multiplicity principle, not a universal numerical hurdle.
   [Paper](https://academic.oup.com/rfs/article-abstract/29/1/5/1843824).

### Financial performance and execution

10. **Andrew Lo, “The Statistics of Sharpe Ratios.”** Essential for serial
    dependence, time aggregation, annualization, uncertainty, and comparisons
    of Sharpe ratios. Mechanical square-root-of-time annualization is not
    generally valid. [Publication record](https://alo.mit.edu/publications/page/18/).

11. **Larry Harris, _Trading and Exchanges_.** Best bridge from predictions to
    executable decisions: orders, spreads, liquidity, fills, shorting, market
    impact, and transaction costs. [Book](https://academic.oup.com/book/52292).

12. **Robert Korajczyk and Ronnie Sadka; Andrea Frazzini, Ronen Israel, and
    Tobias Moskowitz; Robert Almgren and Neil Chriss.** These sources support
    modeling transaction costs, price impact, execution, and capacity, while
    showing that cost magnitudes depend on market, scale, style, venue, and
    period. Distill the control, not a universal basis-point haircut.
    [Korajczyk-Sadka](https://doi.org/10.1111/j.1540-6261.2004.00656.x),
    [Frazzini-Israel-Moskowitz](https://pages.stern.nyu.edu/~afrazzin/pdf/Trading%20Cost%20of%20Asset%20Pricing%20Anomalies%20-%20Frazzini%2C%20Israel%20and%20Moskowitz.pdf),
    and [Almgren-Chriss](https://doi.org/10.21314/JOR.2001.041).

13. **Stephen Brown, William Goetzmann, Roger Ibbotson, and Stephen Ross; William
    Beaver, Maureen McNichols, and Richard Price.** These own important evidence
    on survivorship, delistings, and historical populations. Survivorship bias
    does not have one guaranteed direction; preserve the full historically
    eligible population and measure the actual effect.
    [Brown et al.](https://academic.oup.com/rfs/article-abstract/5/4/553/1590264)
    and [Beaver et al.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=949601).

14. **James Hamilton and Jushan Bai with Pierre Perron.** These own major
    regime-switching and structural-break methods. They establish method
    definitions, not that regime switching improves a particular strategy.
    [Hamilton](https://ideas.repec.org/a/ecm/emetrp/v57y1989i2p357-84.html) and
    [Bai-Perron](https://ideas.repec.org/a/ecm/emetrp/v66y1998i1p47-78.html).

### Finance-specific contract worth distilling

For every example or decision, record as applicable:

```text
subject or event time
public release or dissemination time
vendor availability time
project ingestion time
revision or vintage identity
prediction cutoff
earliest executable order or fill time
```

The historical universe must also be point-in-time: membership, listings,
delistings, symbol and security mappings, corporate actions, dividends,
borrowability, and trading halts must reflect what existed at each decision
time. The backtest must preserve signal-to-order-to-fill chronology and report
net economics under stated fees, spread, slippage, market impact, borrow,
funding, turnover, size, capacity, and fill assumptions.

The search ledger should include every materially tried signal, feature,
transform, label, universe, horizon, holding period, window, split, model,
hyperparameter, threshold, portfolio rule, cost assumption, seed, and manual or
abandoned iteration that could have influenced selection.

### Financial evaluation mechanics and equations

These equations are useful distillation targets because they make the claimed
quantity and assumptions inspectable. They are not universal promotion rules.

#### Net strategy return

For a frozen strategy and declared accounting convention, report at least:

\[
R^{net}_t = R^{gross}_t
- C^{fees}_t
- C^{spread}_t
- C^{slippage}_t
- C^{impact}_t
- C^{borrow/funding}_t.
\]

The contract must define whether the quantity is per trade, per position,
portfolio-period return, arithmetic excess return, log return, or wealth
growth; how overlapping positions are aggregated; how cash and leverage are
treated; and whether turnover is one-way or round-trip. It must also name target
AUM, participation, liquidity, volatility, time of day, rebalance cadence,
latency, fill policy, cancellations, partial fills, unfilled orders, dividends,
corporate actions, delisting exits, short recalls, and financing where
applicable.

If costs can change which candidate is selected, selection must be rerun on net
economics. Subtracting a constant cost after selecting on gross performance
does not evaluate the deployable selection procedure.

#### Out-of-sample stock-prediction comparison

Gu, Kelly, and Xiu use a zero-return benchmark for stock-level prediction:

\[
R^2_{OOS} = 1 -
\frac{\sum_{i,t}(r_{i,t+1}-\hat r_{i,t+1})^2}
{\sum_{i,t}r_{i,t+1}^2}.
\]

A negative value means the fitted model loses to predicting zero under this
specific loss and population. It is not the ordinary centered in-sample
coefficient of determination and should retain the authors' denominator and
evaluation population when cited.

#### Forecast-comparison loss differential

For two fixed forecasting procedures, define:

\[
d_t = L(e_{1,t}) - L(e_{2,t}),
\qquad H_0:E[d_t]=0.
\]

Diebold-Mariano inference scales the average loss differential by an estimate
of its sampling variability. Multi-step overlapping forecasts induce serial
correlation, so the variance estimator must reflect the dependence. Nested-
model comparisons require methods designed for nesting rather than an
unqualified Diebold-Mariano test. Conditional predictive-ability questions are
different from an unconditional average comparison.

#### Reality Check and SPA family hypothesis

With benchmark-versus-candidate loss advantage

\[
d_{k,t}=L_{0,t}-L_{k,t},
\]

a family-level null can be written as:

\[
H_0:\max_k E[d_{k,t}]\le 0.
\]

White's Reality Check and Hansen's SPA require the supplied candidate family
and dependence-preserving resampling to correspond to the actual research
search. Missing failed or abandoned candidates weakens the target. SPA
studentizes candidate performance and reduces sensitivity to poor irrelevant
alternatives, but it does not replace point-in-time or execution validity.

#### Deflated Sharpe Ratio

For sample Sharpe ratio \(\widehat{SR}\), sample length \(T\), return skewness
\(\hat\gamma_3\), Pearson kurtosis \(\hat\gamma_4\), and multiplicity-adjusted
threshold \(SR_0\), Bailey and López de Prado define:

\[
DSR=\Phi\left(
\frac{(\widehat{SR}-SR_0)\sqrt{T-1}}
{\sqrt{1-\hat\gamma_3\widehat{SR}
+\frac{\hat\gamma_4-1}{4}\widehat{SR}^{2}}}
\right).
\]

Their expected-maximum threshold uses the estimated variance of Sharpe ratios
and an effective number of independent trials. DSR is a probability-like
quantity in \([0,1]\), not an “adjusted Sharpe ratio.” All Sharpe quantities
must use the same sampling frequency. If the effective independent-trial count
is not defensible, report sensitivity bounds instead of a single authoritative
DSR. The published formula addresses finite samples, skewness, kurtosis, and
selection but does not automatically repair serial dependence.

#### Probability of Backtest Overfitting

For each combinatorially symmetric split \(c\), let the in-sample winner's
out-of-sample relative rank be:

\[
\omega_c=\frac{r^{OOS}_c}{N+1},
\qquad
\lambda_c=\log\frac{\omega_c}{1-\omega_c}.
\]

Then:

\[
\widehat{PBO}
=\frac{1}{|C|}\sum_{c\in C}\mathbf 1\{\lambda_c<0\}.
\]

This estimates how often the in-sample winner falls below the out-of-sample
median of the supplied synchronized candidate matrix. It is a search-stability
diagnostic, not a p-value. It may not reproduce a chronological deployment path
under structural change, so use it alongside rather than instead of rolling-
origin evaluation.

#### Binary probability evaluation

The Brier score is:

\[
BS=\frac1n\sum_{t=1}^{n}(p_t-y_t)^2.
\]

The classical decomposition separates uncertainty, resolution, and
reliability. An aggregate Brier score does not isolate calibration. Report a
calibration or reliability curve with support and uncertainty, especially by
horizon, regime, prevalence, and decision-relevant score region.

Log loss is:

\[
-\frac1n\sum_t\left[y_t\log p_t+(1-y_t)\log(1-p_t)\right].
\]

It is strictly proper but heavily penalizes confident errors. Low forecast
loss does not establish tradable value, and profitable portfolio behavior does
not establish calibrated probabilities.

### Finance-specific invariants and failure tests

The following controls are worth making executable in any later finance branch:

- At forecast origin \(o\), every fitted transformation, imputer, scaler,
  selector, calibrator, threshold, and model uses only information available by
  \(o\).
- The evaluated procedure uses the same refit cadence, training-window rule,
  calibration, threshold selection, and portfolio construction intended for
  deployment.
- For outcomes such as \(y_t=r_{t+1:t+h}\), folds are separated using the full
  information and outcome intervals, not only row timestamps.
- Purging removes training examples whose information or label intervals
  overlap an evaluated interval. An embargo excludes post-test training
  observations whose information can still carry test-period dependence. A gap
  is a general temporal separation justified by horizon, maturity, release
  lag, or residual dependence.
- The same overlap and separation rules apply inside tuning and in outer
  assessment. An arbitrary percentage embargo is not evidence; derive or bound
  the interval and record the rationale.
- Full-sample normalization, revised data, current-universe selection, and
  same-close execution are separate leakage or simulation defects that purging
  does not repair.
- A same-close signal does not receive the same closing price unless a real
  auction or order mechanism supports that chronology.
- Regime detectors, break detectors, scaling choices, window lengths, and model
  switching are fitted or selected within the training or inner boundary.
- Ex-post regime labels are descriptive unless the same label was prospectively
  available. Evaluate the frozen adaptive procedure, not an oracle that uses
  future knowledge to switch models.
- Report metrics, bias, turnover, cost, drawdown, calibration, and coverage by
  forecast origin, horizon, and predeclared economically relevant period.
- “Alpha,” “edge,” or “strategy superiority” activates search-family and
  multiplicity controls even when the work is otherwise described as ordinary
  predictive modeling.

## Priority 0: core MLE systems sources

1. **D. Sculley et al., “Hidden Technical Debt in Machine Learning Systems.”**
   Owns the canonical ML-systems treatment of entanglement, the CACE principle,
   correction cascades, undeclared consumers, hidden feedback loops, unstable
   data dependencies, glue code, pipeline jungles, and configuration debt.
   [Paper](https://papers.nips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf).

2. **Eric Breck, Shanqing Cai, Eric Nielsen, Michael Salib, and D. Sculley, “The
   ML Test Score.”** Strong source for feature and data tests, model-development
   tests, infrastructure tests, monitoring, training-serving skew, canaries,
   and rollback. Its numeric rubric is author-specific, not a universal
   readiness certification.
   [Paper](https://storage.googleapis.com/gweb-research2023-media/pubtools/4156.pdf).

3. **Saleema Amershi et al., “Software Engineering for Machine Learning: A Case
   Study.”** Empirical industrial lifecycle vocabulary covering model
   requirements, collection, cleaning, labeling, features, training,
   evaluation, deployment, monitoring, and feedback loops.
   [Paper](https://www.microsoft.com/en-us/research/uploads/prod/2019/03/amershi-icse-2019_Software_Engineering_for_Machine_Learning.pdf).

4. **Martin Zinkevich, “Rules of Machine Learning.”** Concise practitioner
   source for simple baselines, pipeline instrumentation, freshness, iteration,
   and training-serving parity. Treat the numbered rules as Google experience,
   not universal laws.
   [Guide](https://developers.google.com/machine-learning/guides/rules-of-ml/).

5. **Eric Breck, Neoklis Polyzotis, Sudip Roy, Steven Whang, and Martin
   Zinkevich, “Data Validation for Machine Learning.”** Strong ML-specific
   source for reviewed schemas, single-batch and inter-batch validation,
   training-code assumptions, anomaly detection, and training-serving skew.
   [Paper](https://proceedings.mlsys.org/paper_files/paper/2019/file/928f1160e52192e3e0017fb63ab65391-Paper.pdf).

6. **NIST AI Risk Management Framework 1.0.** Official source for intended
   purpose, context, risk tolerance, TEVV, go/no-go decisions, monitoring,
   incident response, change management, and decommissioning. It is voluntary,
   non-sector-specific, under revision, and neither an implementation recipe
   nor a compliance verdict.
   [Framework](https://www.nist.gov/itl/ai-risk-management-framework) and
   [playbook](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook).

7. **Matei Zaharia et al., MLflow, and Manasi Vartak et al., ModelDB.** Original
   systems sources for experiment runs, parameters, code versions, metrics,
   artifacts, and model management. They own useful abstractions, not one
   universal run-record format.
   [MLflow](https://people.eecs.berkeley.edu/~matei/papers/2018/ieee_mlflow.pdf)
   and [ModelDB](https://people.csail.mit.edu/mvartak/papers/modeldb-hilda.pdf).

8. **Google SRE books and Continuous Delivery for Machine Learning.** Strong
   operational sources for reproducible releases, canaries, monitoring,
   incidents, rollback, and the distinction among continuous delivery,
   continuous deployment, and continuous training.
   [Google SRE books](https://sre.google/books/) and
   [CD4ML](https://martinfowler.com/articles/cd4ml.html).

## Priority 1: statistical and evaluation foundations

- **Stuart Hurlbert, “Pseudoreplication and the Design of Ecological Field
  Experiments.”** Distill the difference between observation count and the
  independently assigned or replicated experimental-unit count.
  [Paper](https://faculty.fiu.edu/~stoddard/courses/IBR/readings/Hurlbert_1984.pdf).
- **Stephen Bates, Trevor Hastie, and Robert Tibshirani, “Cross-validation: what
  does it estimate and how well does it do it?”** Useful for naming the target
  estimated by CV and limits of ordinary CV intervals.
  [Paper](https://arxiv.org/abs/2104.00673).
- **Brian Nosek et al., “The Preregistration Revolution,” and Eric-Jan
  Wagenmakers et al., “An Agenda for Purely Confirmatory Research.”** Own the
  modern exploration-versus-confirmation distinction and outcome-blind
  protocol commitments. Preregistration does not repair a poor design.
  [Nosek et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/) and
  [Wagenmakers et al.](https://journals.sagepub.com/doi/abs/10.1177/1745691612463078).
- **Standards for Educational and Psychological Testing; Abigail Jacobs and
  Hanna Wallach.** Validity evidence supports an interpretation for a proposed
  use, not a model or test in the abstract.
  [Standards](https://www.testingstandards.net/uploads/7/6/6/4/76643089/standards_2014edition.pdf)
  and [Measurement and Fairness](https://doi.org/10.1145/3442188.3445901).
- **Ziad Obermeyer et al.** Important empirical proxy failure: accurate
  prediction of cost did not validate cost as a proxy for illness.
  [Paper](https://escholarship.org/uc/item/6h92v832).
- **Jesse Dodge et al.; Maurizio Ferrari Dacrema et al.; Janez Demšar.** These
  support search-budget reporting, strong and fairly tuned baselines, and
  correct independent units in multi-dataset comparisons.
  [Dodge et al.](https://schwartz-lab-huji.github.io/publication/showyourwork/),
  [Ferrari Dacrema et al.](https://arxiv.org/abs/1907.06902), and
  [Demšar](https://www.jmlr.org/beta/papers/v7/demsar06a.html).

## Priority 1: data, provenance, and documentation

- **W3C PROV-DM and PROV-O.** Primary specifications for provenance entities,
  activities, agents, generation, usage, derivation, and responsibility. The
  conceptual model transfers; RDF and a particular serialization should not
  become universal requirements.
  [PROV-DM](https://www.w3.org/TR/prov-dm/) and
  [PROV-O](https://www.w3.org/TR/prov-o/).
- **Timnit Gebru et al., “Datasheets for Datasets.”** Lifecycle-oriented
  dataset documentation covering motivation, composition, collection,
  preprocessing, labeling, uses, distribution, and maintenance.
  [Paper](https://arxiv.org/abs/1803.09010).
- **Margaret Mitchell et al., “Model Cards for Model Reporting.”** Release-
  facing documentation of model identity, intended and out-of-scope uses,
  relevant factors, metrics, evaluation data, disaggregated results,
  limitations, and caveats. A card is documentation, not proof of safety or
  suitability. [Paper](https://arxiv.org/abs/1810.03993).
- **Emily Bender and Batya Friedman, “Data Statements for NLP.”** Primary source
  for speaker, annotator, curator, language population, and context. Keep it an
  NLP-specific branch. [Paper](https://aclanthology.org/Q18-1041/).
- **Nithya Sambasivan et al., “Data Cascades in High-Stakes AI.”** Empirical
  source for compounding downstream effects from organizational, collection,
  labeling, and domain-expertise failures. Do not use `cascade` as a synonym
  for an isolated defect. [Paper](https://research.google/pubs/everyone-wants-to-do-the-model-work-not-the-data-work-data-cascades-in-high-stakes-ai/).
- **Joëlle Pineau et al., “Improving Reproducibility in Machine Learning
  Research.”** Source for the NeurIPS reproducibility program, reporting
  checklists, code submission, and institutional practice.
  [Paper](https://www.jmlr.org/papers/v22/20-303.html).
- **Geir Sandve et al., “Ten Simple Rules for Reproducible Computational
  Research.”** Supports executable workflows, exact configuration and program
  identity, version-controlled scripts, random-state records, and preserved
  links from claims to results.
  [Paper](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285).

Datasheets, model cards, provenance reports, and audit views should remain
conditional projections from the workflow's existing contract and receipt
chain, not mandatory parallel sources of truth.

## Conditional modern generative-AI sources

These sources matter when the workflow covers RAG, model graders, prompt-
injection exposure, or tool-using agents. They should remain conditional for
primarily financial time-series work.

- **NIST AI 100-2e2025, Adversarial Machine Learning.** Direct prompting
  attacks, indirect prompt injection, poisoning, evasion, privacy compromise,
  attacker capabilities, and security-utility trade-offs.
  [Publication](https://www.nist.gov/publications/adversarial-machine-learning-taxonomy-and-terminology-attacks-and-mitigations-0).
- **NIST AI 600-1, Generative AI Profile.** Confabulation, value-chain and
  component integration, assurance thresholds, go/no-go criteria, and incident
  monitoring. [Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf).
- **HELM.** Scenario-based, multi-metric, transparent evaluation. HELM is a
  named framework, not a universal standard.
  [Paper](https://arxiv.org/abs/2211.09110).
- **RAGChecker.** Claim recall, context precision, context utilization, noise
  sensitivity, faithfulness, and hallucination diagnostics. Its automatic
  evaluator is itself a model-based proxy.
  [Paper](https://proceedings.neurips.cc/paper_files/paper/2024/hash/27245589131d17368cccdfa990cbf16e-Abstract-Datasets_and_Benchmarks_Track.html).
- **tau-bench, ToolSandbox, and AgentDojo.** Useful vocabulary for world state,
  policy adherence, required milestones, forbidden minefields, insufficient
  information, final-state correctness, repeated-run reliability, benign
  utility, utility under attack, and targeted attack success.
  [tau-bench](https://arxiv.org/abs/2406.12045),
  [ToolSandbox](https://machinelearning.apple.com/research/toolsandbox-stateful-conversational-llm-benchmark), and
  [AgentDojo](https://proceedings.nips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html).
- **Zheng et al., “Judging LLM-as-a-Judge.”** Position bias, verbosity bias, and
  self-enhancement bias. Model graders need frozen model, version, rubric,
  prompt, candidate ordering, decoding, and invalid-output policy, followed by
  property- and population-specific validation against a human or domain
  oracle. [Paper](https://papers.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html).

## Books and courses for synthesis and exercises

Books are useful for integrated explanations and examples. Original papers and
standards should remain the claim owners for named methods.

### Books

- Campbell, Lo, and MacKinlay,
  [_The Econometrics of Financial Markets_](https://press.princeton.edu/books/hardcover/9780691043012/the-econometrics-of-financial-markets)
- Larry Harris,
  [_Trading and Exchanges_](https://academic.oup.com/book/52292)
- Marcos López de Prado,
  [_Advances in Financial Machine Learning_](https://www.wiley-vch.de/de/fachgebiete/finanzen-wirtschaft-recht/advances-in-financial-machine-learning-978-1-119-48208-6)
- Marcos López de Prado,
  [_Machine Learning for Asset Managers_](https://www.cambridge.org/core/books/machine-learning-for-asset-managers/6D9211305EA2E425D33A9F38D0AE3545)
- David Aronson,
  [_Evidence-Based Technical Analysis_](https://www.wiley-vch.de/en/areas-interest/finance-economics-law/finance-investments-13fi/trading-13fi4/evidence-based-technical-analysis-978-0-470-00874-4)
- Hyndman and Athanasopoulos,
  [_Forecasting: Principles and Practice_](https://otexts.com/fpp3/)
- Hernán and Robins,
  [_Causal Inference: What If_](https://miguelhernan.org/s/hernanrobins_WhatIf_2jan25.pdf)
- Chen, Murphy, Parisa, Sculley, and Underwood,
  [_Reliable Machine Learning_](https://www.oreilly.com/library/view/reliable-machine-learning/9781098106218/)
- Chip Huyen,
  [_Designing Machine Learning Systems_](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/)
- Stefan Jansen,
  [_Machine Learning for Algorithmic Trading_](https://github.com/stefan-jansen/machine-learning-for-trading)

### Courses and speakers

- [Georgia Tech Machine Learning for Trading, Tucker Balch](https://lucylabs.gatech.edu/ml4t/)
- [Stanford CS329S, Chip Huyen](https://web.stanford.edu/class/cs329s/)
- [Scikit-learn MOOC](https://scikit-learn.org/stable/presentations.html)
- [MIT Finance Theory, Andrew Lo](https://ocw.mit.edu/courses/15-401-finance-theory-i-fall-2008/)

## People and groups worth following by topic

- ML systems: D. Sculley, Eric Breck, Martin Zinkevich, Neoklis Polyzotis,
  Saleema Amershi, Matei Zaharia, and Manasi Vartak.
- Statistical validity: Gavin Cawley, Nicola Talbot, Cynthia Dwork, Moritz
  Hardt, Tilmann Gneiting, Adrian Raftery, Miguel Hernán, and James Robins.
- Forecasting and financial inference: Rob Hyndman, Francis Diebold, Roberto
  Mariano, Raffaella Giacomini, Barbara Rossi, Halbert White, Peter Hansen,
  Campbell Harvey, Andrew Lo, David Bailey, and Marcos López de Prado.
- Market implementation: Larry Harris, Andrea Frazzini, Ronen Israel, Tobias
  Moskowitz, Robert Korajczyk, Ronnie Sadka, Robert Almgren, and Neil Chriss.
- Data and reporting: Timnit Gebru, Margaret Mitchell, Emily Bender, Hanna
  Wallach, Joëlle Pineau, and the W3C PROV Working Group.
- Conditional GenAI: the NIST adversarial-ML and ARIA teams, Stanford CRFM,
  RAGChecker authors, AgentDojo authors, and ToolSandbox authors.

Following people is useful for finding new work. Authority remains attached to
the exact publication, version, population, method, and claim rather than to a
person's reputation.

## Recommended distillation sequence

1. **Financial evidence contract:** forecast origin, horizon, data vintage,
   historical universe, prediction cutoff, executable fill time, benchmark,
   cost model, capacity, and claimed financial quantity.
2. **Research-search ledger:** every materially tried signal, feature, label,
   horizon, universe, model, split, threshold, cost assumption, and manual
   iteration.
3. **Temporal evaluation glossary:** rolling origin, overlapping label
   intervals, purge, gap, embargo, inner selection, outer assessment, and
   horizon-specific scoring.
4. **Finance inference guide:** Reality Check, SPA, PBO, DSR, Sharpe uncertainty,
   multiplicity, and the applicability and non-applicability of each method.
5. **MLE systems source map:** technical debt, contracts, experiment identity,
   training-serving skew, candidate promotion, monitoring, incidents, and
   retirement.
6. **Reproducibility correction:** artifact recoverability, computational
   reproducibility, rerun evidence, and replicability.
7. **Conditional GenAI appendix:** RAG, model graders, prompt injection, and
   stateful tool-agent evaluation.

## Material limits and conflicts

- No source makes one splitter, embargo length, cost rate, metric, significance
  threshold, or promotion gate universal.
- Random CV is not universally invalid for time series, but narrow validity
  results do not establish suitability for a chronological trading strategy.
- Survivorship bias and delisting corrections do not have one guaranteed
  direction; preserve the population and measure the effect.
- Transaction-cost studies disagree materially because their markets, trade
  sizes, styles, data, and periods differ. This supports context-specific cost
  models rather than a universal haircut.
- DSR, PBO, Reality Check, and SPA answer different questions. None subsumes the
  others, and none repairs leakage, point-in-time errors, or unrealistic
  execution.
- Documentation artifacts do not prove behavior, correctness, accountability,
  safety, fairness, or suitability.
- Drift and dataset-shift signals are diagnostic evidence, not proof of
  performance degradation.
- NIST frameworks are voluntary and do not establish legal compliance or a
  safety guarantee.
- GenAI benchmarks are bounded by their tasks, languages, models, attacks, and
  evaluator behavior. They should not become universal promotion gates.

## Source identity and copy fidelity

The load-bearing sources were inspected through official standards bodies,
publisher or proceedings pages, author-hosted manuscripts, or stable scholarly
records. ArXiv or author copies were used where they were the inspectable public
version of the named work. Publisher landing pages were used for bibliographic
identity when full text was not openly available. No private source, search
snippet, community skill, marketplace listing, or unsourced summary was used as
the authority for a methodological claim.

## Repository mapping and empirical remainder

The current `mle-workflow` already owns the appropriate integration seams:

- purpose and delivery classification;
- system and delivery contracts;
- data and feature contracts;
- traceable experiments and baseline comparison;
- deployment-shaped evaluation and conditional confirmatory inference;
- test portfolios and independent oracles;
- immutable candidate promotion;
- monitoring, refresh, incident, rollback, and retirement; and
- capability-triggered risk branches.

The finance material belongs in a conditional branch or tightly routed
reference, not as universal ceremony. Datasheets, model cards, and audit views
should be derived projections rather than duplicate sources of truth.

This note establishes source correspondence and vocabulary boundaries. It does
not establish runtime compliance with the workflow, behavioral efficacy of the
skill text, real-world model quality, or financial profitability. Any future
wording change still requires separate implementation authority and
claim-proportionate behavioral proof.

## Stopping basis

Each major concept family in the current workflow has at least one definition-
owning, original, official, or field-standard source; named finance methods have
their assumptions and non-applicability recorded; and the material contrary
lanes are preserved. Additional broad searches are unlikely to change the first
distillation priorities.

Status: answered.

Caller-use boundary: this note supports source selection, study, and a future
review or revision decision. It does not authorize edits to `mle-workflow`,
installed-skill synchronization, staging, commit, publication, or deployment.

Return owner: the user and future root author of `mle-workflow`.

Next: none.
