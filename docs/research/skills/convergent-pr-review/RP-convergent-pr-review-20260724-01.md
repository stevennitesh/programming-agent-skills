---
artifact_id: RP-convergent-pr-review-20260724-01
---

# Convergent PR Review Research Packet

- Campaign epoch: `2026-07-24`
- Target: `convergent-pr-review`
- Question: Which methods, vocabulary, conditions, alternatives,
  counterpressure, and limits best support the settled intended behavior of
  `convergent-pr-review`?
- Caller use: decision-ready evidence for Deploy Prompt 2; not authority for
  local intent, exact runtime wording, or behavioral efficacy.
- M0 checkpoint:
  `docs/validation/transcripts/2026-07-24-convergent-pr-review-prompt1-m0.md`
- M0 content fingerprint:
  `sha256:469734af7b346c0f327d07fbd2a001d8b3f76cd985aa7c9468a53c6944326e4e`
- Research packet fingerprint:
  `sha256:e1da6bc137e036d4dbb81174728eea0ed77cfa9d5bfcfcfa4e77af526747d9d7`
- Applicable state: repository `HEAD`
  `f3be70c31dd8f2ae9f12a75248065ef313790bda`, sources accessed
  `2026-07-24`
- Authorized write: this file only
- Return owner: Deploy Campaign coordinator

<!-- BEGIN RESEARCH PACKET -->

## Scope And Evidence Rules

This packet investigates the seven M0 research clusters: immutable review
state, independent coverage, evidence convergence, release decisions, review
modes, nonblocking advisories, and invocation/completion. It excludes changing
M0, deciding exact H1 wording, implementing a runtime, evaluating behavioral
effectiveness, promotion, installation, and Git delivery.

Source labels are `direct`, `corroborated`, `synthesis`, `inference`, or `thin`.
Method classifications are independently and separately
`independently-supported`, `contested`, `pack-specific`, or `unverified`.
Observed package behavior will not inherit professional authority, and
professional evidence will not settle local intent.

## Phase 1: Blind Independent Discovery

This section was recorded before opening any upstream package, the current
canonical target package, target synthesis, or historical target candidate
conclusion. The search began from the M0 intended behavior and actively sought
alternatives, falsifying evidence, conditions, and failure modes.

### Blind Source Registry

All sources below were inspected on `2026-07-24`.

| ID | Source identity and authority | Access depth | Principal use and limit |
| --- | --- | --- | --- |
| S01 | Git project, [`git-status` manual, last changed in Git 2.53.0](https://git-scm.com/docs/git-status/2.53.0.html) | Complete relevant Description, porcelain v2, pathname, submodule, Background Refresh, and untracked-file sections | Governs status surfaces and documents that ordinary `status` may write cached index data; it does not create an atomic dirty-tree snapshot. |
| S02 | Git project, [`git-rev-parse` 2.52.0](https://git-scm.com/docs/git-rev-parse/2.52.0.html), [`gitrevisions`, last changed 2.42.0](https://git-scm.com/docs/gitrevisions), and [`gitglossary` 2.54.0](https://git-scm.com/docs/gitglossary/2.54.0.html) | Complete relevant object-format, `--verify`, object-name, ref, index, submodule, and superproject definitions | Governs full object identity and ref/object distinctions; an OID identifies Git content, not external state or authenticity. |
| S03 | Git project, [`git-diff` 2.55.0](https://git-scm.com/docs/git-diff/2.55.0.html), [`git-ls-files` 2.55.0](https://git-scm.com/docs/git-ls-files/2.55.0.html), [`git-hash-object`, last changed 2.43.0](https://git-scm.com/docs/git-hash-object/2.43.0.html), and [`git-fsck` 2.53.0](https://git-scm.com/docs/git-fsck/2.53.0.html) | Complete relevant comparison, stage/OID, raw-hash, write flag, strict/full verification, helper, and filter sections | Governs diff/index/byte identity and object verification. Diffs omit untracked content; `fsck` integrity is not review completeness. |
| S04 | IETF Independent Stream, [RFC 8493, “The BagIt File Packaging Format (V1.0),” October 2018](https://www.rfc-editor.org/rfc/rfc8493.html) | Sections 2.1.3, 2.4, 3, 5.1, 5.4, and 6.1.1 | Governs its `complete` and `valid` manifest vocabulary and integrity/security limits. Applying it to review snapshots is an inference, not a Git mandate. |
| S05 | NIST, [SP 800-218 SSDF 1.1, February 2022, DOI 10.6028/NIST.SP.800-218](https://doi.org/10.6028/NIST.SP.800-218) | Executive Summary; PW.2.1, PW.7, PW.8, RV.1, and RV.2 | Governing secure-development guidance for independent qualified review, code review/analysis, issue triage, testing, and risk response. It is outcome-oriented and does not prescribe a universal reviewer count or PR decision vocabulary. |
| S06 | NIST Joint Task Force, [SP 800-53 Rev. 5, September 2020, DOI 10.6028/NIST.SP.800-53r5](https://doi.org/10.6028/NIST.SP.800-53r5) | CA-2 and enhancement CA-2(1), CA-7, RA-7, and SA-11(7) | Governs risk-scaled assessor independence, current/relevant evidence reuse, continuous/change monitoring, risk acceptance, and coverage verification for security controls. PR application is analogical. |
| S07 | NIST Joint Task Force, [SP 800-53A Rev. 5, January 2022](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53Ar5.pdf) | Sections 3.2-3.3 and relevant assessment-plan/determination material | Governs sufficient evidence, targeted assessment, coverage/depth, and `satisfied`/`other than satisfied`; it does not prescribe a distinct four-label PR release taxonomy. |
| S08 | NIST Joint Task Force, [SP 800-37 Rev. 2, December 2018, DOI 10.6028/NIST.SP.800-37r2](https://doi.org/10.6028/NIST.SP.800-37r2) | Tasks A-6, R-3, R-4, and Appendix F | Governs separation of assessment from risk authorization, conditional authorization, denial, remediation tracking, and reassessment. Federal-system authorization is only an analogy to PR release. |
| S09 | NASA, [NASA-STD-8739.8B, approved 2022-09-08](https://standards.nasa.gov/sites/default/files/standards/NASA/B/0/NASA-STD-87398-Revision-B_1.pdf) | Sections 1.1 and 4.4; SWE-204 material | Governs mandatory/recommended language, objective evidence, technical/managerial/financial IV&V independence, risk-driven rigor, nonconformance closure, and improvement opportunities. Its mission/safety context is higher assurance than ordinary PR review. |
| S10 | NASA Software Engineering Handbook, [“Peer Review and Inspections Including Checklists,” updated 2017-05-30](https://swehb.nasa.gov/spaces/7150/pages/16449965/7.10%2B-%2BPeer%2BReview%2Band%2BInspections%2BIncluding%2BChecklists) | Complete planning, roles, preparation, meeting, rework, follow-up, barriers, and lessons sections | Authoritative NASA practice guidance for perspectives, criteria, individual preparation, defect classification, open-item disposition, and exit criteria. It endorses team consensus, which is not itself proof. |
| S11 | NASA, [NASA-STD-8739.9, 2013, Change 1 (2016), revalidated 2018](https://standards.nasa.gov/sites/default/files/standards/NASA/Baseline/1/nasa-std-87399_with_change_1.pdf) | Relevant preparation, logging, classification, moderator, tracking, and closeout sections | Primary historical formal-inspection method. The standard is inactive and not current NASA-mandatory authority. |
| S12 | OASIS, [SARIF 2.1.0 Plus Errata 01, 2023-08-28](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html) | Sections 3.27.2-3.27.4, 3.27.9-3.27.10, 3.27.16-3.27.17, 3.27.31, and Appendix B | Governs result states, GUID/correlation identity, fingerprints, occurrence count, and severity restrictions for static-analysis interchange. It standardizes representation, not finding truth or deduplication correctness. |
| S13 | CVE Program, [CNA Operational Rules 4.1.0, effective 2025-05-14](https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.1.0.pdf) | Sections 4.1, 4.2.2.1, 4.2.11-4.2.12, 4.5.3.6-4.5.3.10, and 4.6 | Governs reasonable evidence, scope/extent, merge/split, rejection, and dispute for CVE records. General-review transfer is analogical. |
| S14 | FIRST, [CVSS v3.1 Specification](https://www.first.org/cvss/v3.1/specification-document) | Sections 1.1 and 3.3 | Governs vulnerability impact/exploitability and report confidence. CVSS is security-specific and its score is not a finding-admission test. |
| S15 | IETF, [RFC 7282, “On Consensus and Humming in the IETF,” June 2014](https://www.rfc-editor.org/rfc/rfc7282.html) | Sections 3-4 and 6 | Direct authority for IETF consensus: resolve technical objections rather than count votes. It is not a code-review standard. |
| S16 | Basili et al., [“The Empirical Investigation of Perspective-Based Reading,” 1996](https://www.cs.umd.edu/~mvz/handouts/emp_pbr.pdf) | Full author manuscript and experiment limitations | Original controlled NASA/GSFC evidence for differentiated perspectives and wider simulated-team coverage; team results unioned individuals rather than observing interaction. |
| S17 | Perry, Porter, and Votta, [“Empirical Studies of Software Inspections at AT&T,” IEEE TSE 28(7), 2002, DOI 10.1109/TSE.2002.1019483](https://doi.org/10.1109/TSE.2002.1019483) | Study claims available through the primary record | Original inspection evidence: reviewers rarely found the same defects, two outperformed one, and four did not outperform two in that context. It cannot set a universal reviewer count. |
| S18 | Bianchi, Lanubile, and Visaggio, [controlled nominal-versus-interacting inspection study, METRICS 2001, DOI 10.1109/METRIC.2001.915514](https://doi.org/10.1109/METRIC.2001.915514) | Primary paper findings and limits | Original evidence that interacting teams can lose singleton true defects. Participants and requirements-inspection task limit generality. |
| S19 | Knight and Leveson, [“An Experimental Evaluation of the Assumption of Independence in Multi-Version Programming,” IEEE TSE 12(1), 1986](https://doi.org/10.1109/TSE.1986.6312924) | Full author-accessible paper and DOI record | Original evidence that nominally independent implementations can fail dependently under shared specification/tooling. It is not a reviewer study. |
| S20 | Lorenz et al., [“How Social Influence Can Undermine the Wisdom of Crowd Effect,” PNAS 108(22), 2011](https://doi.org/10.1073/pnas.1008636108) | Full primary paper and indexed record | Original evidence that peer estimates reduced diversity and increased confidence without corresponding accuracy gains in estimation tasks. It supports sealed initial judgments, not a ban on later evidence discussion. |
| S21 | Kim et al., [“Correlated Errors in Large Language Models,” ICML 2025, PMLR 267](https://proceedings.mlr.press/v267/kim25e.html) | Full conference record and paper | Primary large-scale evidence over 350 models that LLM errors remain substantially correlated, including across architectures/providers. The tasks were not code review. |
| S22 | Smit et al., [“Should we be going MAD?,” ICML 2024, PMLR 235](https://proceedings.mlr.press/v235/smit24a.html) | Full conference record and paper | Primary evidence that multi-agent debate did not reliably beat self-consistency/ensembling and was tuning-sensitive. It bounds claims that interaction or more agents inherently improves truth. |
| S23 | Sadowski et al., [“Modern Code Review: A Case Study at Google,” ICSE-SEIP 2018](https://storage.googleapis.com/gweb-research2023-media/pubtools/4476.pdf) | Full paper | Primary industrial evidence that ordinary Google review commonly used one reviewer at scale. Specialist reviews such as security were excluded, so it does not negate elevated high-risk assurance. |
| S24 | Google Engineering Practices, [“The Standard of Code Review”](https://google.github.io/eng-practices/review/reviewer/standard.html) and [“How to write code review comments”](https://google.github.io/eng-practices/review/reviewer/comments.html) | Complete pages; page revision identity unavailable | Identifiable practitioner guidance to approve improvement without demanding perfection and label required, optional, nit, and FYI comments distinctly. It is local Google practice, not a governing standard. |
| S25 | Cochrane, [Handbook, current Chapter 5](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-05), plus [Buscemi et al. 2006](https://pubmed.ncbi.nlm.nih.gov/16765272/) | Relevant duplicate-extraction and disagreement-resolution sections plus primary study record | Cross-domain evidence that consequential subjective extraction benefits from independent duplication while costing more; verified-single fallback is cheaper but more error-prone in the cited study. |
| S26 | U.S. GAO, [Government Auditing Standards 2024 Revision, GAO-24-106786](https://www.gao.gov/assets/d24106786.pdf) | Competence, sufficiency, limitations, corroboration/referencing, quality review, and post-release evidence sections | Governing audit evidence discipline for competent capacity, supported conclusions, explicit limitations, and unresolved-quality concerns. Audit application to PR review is analogical. |
| S27 | UK Government Digital Service, [“How service assessments work,” updated 2024-05-09](https://www.gov.uk/service-manual/service-assessments/how-service-assessments-work) | Complete green/amber/red disposition guidance | Governing operational alternative for conditional progression; policy-specific and not valid where risk cannot be accepted. |

### Blind Findings By Intended Behavior

#### Immutable review state

1. **Pin content, not names.** A full, object-format-qualified commit OID is a
   defensible identity for committed Git content; a branch or tag name is an
   indirect ref and may move. Verify untrusted revisions as exactly one
   existing commit and retain the resolved OID. This is `direct` from S02 and
   `independently-supported`.

2. **Treat live state as a composite manifest.** Git distinguishes `HEAD`,
   index, tracked worktree, untracked paths, ignored policy, and nested
   submodule state. Porcelain v2 plus stage/OID enumeration identifies
   classifications, but untracked bytes require separate raw hashing. Exact
   path-set equality plus per-entry hashes is a `synthesis` across S01-S04 and
   is `independently-supported` for declared scope.

3. **Read-only is a command property, not an intent label.** `git status`
   normally refreshes and writes cached index data. A strict inspection must
   suppress optional locks and helpers/fetches and use an allowlisted command
   surface; commands that create tree/commit/stash objects are mutations even
   if they do not move a ref. This is `direct` from S01-S03 and
   `independently-supported`.

4. **Drift detection is not atomic capture.** Pre/post and closing equality can
   detect many changes but cannot prove a sequential dirty-worktree read was
   never a mixed epoch. Writer quiescence, filesystem/VM snapshotting, or an
   isolated immutable copy is needed for temporal atomicity. This is an
   `inference` from Git's separate state surfaces and is `unverified` as a
   portable Git-only guarantee.

5. **Integrity is not authenticity or semantic completeness.** OID/hash checks
   establish byte integrity inside their declared scope; signer trust, ignored
   inputs, external dependencies, ACLs/xattrs, and semantic correctness need
   separate evidence. This is `corroborated` by S02-S04 and
   `independently-supported`.

#### Independent review coverage

1. **Use qualified, role-independent judgment scaled to risk.** NASA and NIST
   define independence through non-authorship, freedom from conflicts and
   adverse influence, and risk-scaled rigor. A fresh prompt alone does not
   satisfy those definitions. This is `corroborated` by S05, S06, and S09 and
   `independently-supported`.

2. **Different perspectives widen search.** Planned perspectives tied to
   stakeholders and quality goals, individual preparation before interaction,
   and explicit lens coverage are supported by NASA practice and
   perspective-based-reading experiments. The exact best partition remains
   task- and expertise-dependent. This is `corroborated` by S10, S11, and S16
   and `independently-supported`.

3. **Preserve initial judgment before convergence.** Social-influence and
   inspection evidence supports sealed first passes because early exposure can
   reduce diversity or lose singleton true defects. Later structured
   evidence-sharing can still clarify and reject false positives. This is
   `corroborated` by S18 and S20 and `independently-supported` under those
   conditions.

4. **Do not count agents as independent votes.** Shared models, training,
   specifications, or prompts can correlate errors; multi-agent debate is not
   inherently superior to noninteractive alternatives. This is
   `corroborated` by S19, S21, and S22 and `independently-supported` as
   counterpressure. The consequence is to verify claims directly, disclose
   common-mode risk, and avoid vote-based admission.

5. **Capacity labels must describe evidence actually obtained.** One genuinely
   independent reviewer plus root/tool verification is degraded single-review
   evidence; root-only self-check is not independent review. Neither NIST nor
   NASA mandates a universal count, and ordinary industrial review often uses
   one reviewer. Exact `two/one/zero` thresholds and the prohibition on a plain
   pass under reduced capacity remain local intent, not a universal
   professional result. The method is `contested` as a universal count but
   `independently-supported` as honest capacity disclosure.

#### Evidence convergence

1. **Separate candidate, evidence, and admitted finding.** A report becomes a
   finding only after evaluation of verifiable evidence against explicit
   criteria. Missing required assurance evidence is an incomplete coverage
   condition, not proof that the suspected defect exists. This is a
   `synthesis` across S05, S07, S10-S13 and
   `independently-supported`.

2. **Use an accountable adjudicator and preserve provenance.** Inspectors may
   generate candidates; a moderator/assessor role owns disposition. Record
   accepted, rejected, duplicate/correlated, and unresolved/disputed states
   with the evidence that drove each transition. This is `corroborated` by
   S10-S13 and `independently-supported`.

3. **Deduplicate by logical condition, not similar wording or votes.** Stable
   occurrence IDs, correlation IDs/fingerprints, multiplicity, merge/split
   history, and retained source provenance allow duplicate observations to
   remain auditable while one canonical condition is judged. This is
   `synthesis` from S12-S13 and `independently-supported`; the exact
   fingerprint algorithm is `unverified` and local.

4. **Resolve disagreements from artifact, criterion, scenario, and evidence.**
   Polls and agreement measure social support, not truth. Preserve material
   counterevidence and an unresolved state when entailment cannot be closed.
   This is `corroborated` by S11, S13, S15, S17-S18 and
   `independently-supported`.

5. **Admit before severity.** Determine that a problem exists and establish its
   reachable impact before assigning severity; keep report confidence and
   impact distinct. This is `corroborated` by S12 and S14 and
   `independently-supported`, with security-specific scoring details excluded
   from general findings.

#### Release decisions, modes, and advisories

1. **Separate assessment from authorization.** An assessor reports whether
   criteria and evidence are satisfied; a named risk owner accepts residual
   risk. A release skill can return an evidence-bound decision but must not
   silently invent risk acceptance. This is `corroborated` by S06-S08 and
   `independently-supported`.

2. **Incomplete is not clean.** Missing, stale, inapplicable, unreliable, or
   insufficiently covered evidence must name the affected scope and cannot be
   treated as a successful clean assessment. This is `corroborated` by S07,
   S10, and S26 and `independently-supported`.

3. **Conditional acceptance is policy-dependent.** NIST permits risk
   acceptance with justification and operational limits; GDS permits a
   time-bounded amber progression. Safety, legal, or caller policy may instead
   forbid progression. `Pass with residual risk` is therefore
   `independently-supported` only when the authorized caller owns that risk;
   it is `contested` as an unconditional assessor power.

4. **Reassessment must preserve identity and affected reach.** Corrected items
   are reassessed, original findings remain traceable, and changed conditions
   or dependencies widen the affected scope. Reused evidence must remain
   current, relevant, valid, and sufficiently independent. This is
   `corroborated` by S06-S10 and `independently-supported`.

5. **Keep mandatory defects and optional opportunities distinct.** NASA's
   `shall`/`should` split, separate nonconformance and improvement lanes, and
   Google's required/optional/nit/FYI practice all support a separate
   nonblocking advisory channel. Advisories must not override a violated
   criterion or acquire release authority. This is `corroborated` by S09 and
   S24 and `independently-supported`; exact advisory schema remains local.

6. **Use explicit readiness and completion criteria.** Plan scope, criteria,
   materials, perspectives, evidence, roles, and exit conditions; close or
   explicitly block every open item before Return. This is `corroborated` by
   S07, S10-S11, and S26 and `independently-supported`.

### Alternatives And Counterpressure Retained

| Proposed default | Credible alternative or counterpressure | Disposition |
| --- | --- | --- |
| Two or more direct reviewers | One qualified independent reviewer is allowed by governing assessment guidance and common in ordinary industrial review; four reviewers did not outperform two in one inspection study. | Exact count is local and risk-dependent. Preserve M0 compatibility but do not claim a universal optimum. |
| Independent noninteractive passes | Structured discussion can expose reasoning and reject false positives; NASA inspection guidance uses moderated consensus. | Keep sealed first judgments, then root evidence reconciliation. Do not ban discussion or treat consensus as proof. |
| Human-style multi-agent debate | Self-consistency or noninteractive ensembling can match or beat debate; same-family models have correlated errors. | Prefer factual isolated lanes and direct verification; do not add debate or voting without candidate-owned proof. |
| Complete live-state capture with Git | No Git-only operation supplies an atomic identity for a dirty multi-file worktree; status itself may write index metadata. | Scope-qualify completeness, use non-mutating capture mechanics, and return incomplete when quiescence/atomicity required but unavailable. |
| Every verified issue blocks | Google and risk frameworks permit minor/accepted residuals; some safety or policy regimes do not. | Blocking follows violated caller criteria and authorized risk tolerance, not review preference. |
| Reuse prior review evidence | Current/relevant/valid evidence can reduce repeated work; changed identity, configuration, independence, or affected dependencies invalidates or narrows reuse. | Reuse only by exact stated conditions and retain original finding identity. |
| Missing evidence is a finding | Some compliance systems record missing required evidence as an adverse determination. | In this skill, keep suspected defect unproved and classify required missing evidence as incomplete coverage unless the governing requirement itself makes evidence absence the violated criterion. |

### Rejected Or Pruned Blind Lanes

- Popularity, review-count rules of thumb, and vendor claims were discovery
  only; they do not establish professional validity or local fit.
- Generic “groupthink” rhetoric was rejected in favor of narrower evidence on
  social influence, correlated errors, conflicts of interest, and directive
  pressure.
- Multi-agent debate papers claiming task-specific gains were not generalized
  to code review; the more decision-relevant result is that protocol,
  heterogeneity, correlation, and task conditions matter.
- CVSS numeric scoring was rejected as a general finding-admission or PR
  release model.
- Formal inspection yield percentages were rejected as transferable
  effectiveness guarantees because process, artifact, participants, and era
  differ.
- No practitioner conversation was needed: published authoritative and primary
  evidence resolved the operational conditions at research scope.

### Blind-Phase Stop

The strongest governing/primary owners and material counterpositions covered
all seven intended-behavior clusters. Further independent discovery was
unlikely to change the provisional methods, their conditions, or their limits.
At this point the blind evidence record was frozen. Upstream, current-package,
synthesis, and historical target inspection had still not begun.

## Phase 2: Upstream, Current, And Historical Intake

Phase 2 began only after the blind record above was written to this file.
Inspection then proceeded in the required order: the three frozen upstream
checkouts, the complete current canonical package, its synthesis and
hash-bound historical conclusions, and the applicable local language packets.

The initial Git reads of each upstream checkout failed with Git's dubious
ownership guard. Inspection resumed with a command-local
`-c safe.directory=<exact checkout>` override. No global or repository
configuration was changed. No checkout was fetched, updated, checked out,
tested, or edited.

### Frozen Upstream Registry

| Pack | Fixed identity and state | Access depth | Review behavior observed | Limits |
| --- | --- | --- | --- | --- |
| Matt Pocock Skills | `https://github.com/mattpocock/skills.git`; commit `ed37663cc5fbef691ddfecd080dff42f7e7e350d`; tree `04b0fcb78e3de7c58744fcba2528354cc64ab988`; `main` equals local `origin/main`; clean; 167 tracked files | All tracked paths inventoried and searched; 32 review, routing, documentation, metadata, and implementation-flow files read semantically; remaining 133 paths classified by owner and relevance | Resolves a fixed point, then runs separate Standards and Spec reviewers in parallel and deliberately preserves their reports without cross-axis merging or reranking. Missing optional Spec skips that axis. Reviewers receive live diff commands, and the aggregator does not verify or admit findings. | No immutable captured diff handoff, reviewer-capacity fallback, typed candidate ledger, root evidence admission, or terminal release decision. No review fixtures or behavioral tests. Frozen local checkout only. |
| Superpowers | `https://github.com/obra/superpowers.git`; commit/tree `d884ae04edebef577e82ff7c4e143debd0bbec99` / `795caed14920f27a1d2d152a09b4720194f64472`; tag `v6.1.1`; `main` equals local `origin/main`; clean; 172 tracked paths | Complete tracked inventory; all current review skills, reviewer prompts, review-package scripts, direct review dependencies, applicable historical design records, and shipped review-facing tests read semantically; remaining paths classified and searched | Pins base/head SHAs, can materialize a range-named review package, distrusts the implementer report, asks the reviewer for file/line evidence, routes `Cannot verify from diff` to controller judgment, separates important findings from recommendations, and requires fresh completion evidence. One reviewer returns severity and readiness verdicts. | No redundant independent reviewers over one target, quorum, cross-reviewer convergence, formal admission, or capacity fallback. A reviewer prompt suggests `git worktree add` while also calling the review read-only. Shipped tests protect workflow shape more than finding correctness; behavioral evals moved to an unavailable external repository. |
| Ponytail | `https://github.com/DietrichGebert/ponytail`; commit `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`; tree `956c22dde535d6e9a222c1e01a180c6e45d54a7e`; `main` equals local `origin/main`; clean; 156 tracked paths | Complete inventory; canonical review/audit skills, every review dispatch and injection path, applicable tests, benchmark owners, relevant result notes, and package/runtime metadata read semantically; remaining files classified and searched | Implements one narrow diff-only over-engineering pass with `delete`, `stdlib`, `native`, `yagni`, and `shrink` tags, replacement advice, an estimated net-line terminal, and explicit correctness/security/performance exclusions. Offline benchmarks separately use fixed rubrics, known-good/bad self-tests, and a completeness judge. | No immutable snapshot contract, finding proof/admission, severity, reviewer isolation/plurality, convergence, capacity fallback, or release decision. Review-output correctness is not behavior-tested. Benchmark gates test the main construction skill, not the review skill, and their results are model/task/scorer bounded. |

#### Pack observations and disposition

- Matt's fixed point and separate Standards/Spec axes are
  `pack-specific` mechanics built from an `independently-supported` separation
  of criteria and perspectives. Retaining reports verbatim without root
  verification or duplicate handling is not suitable for H1.
- Superpowers' SHA-bounded review package, evidence-before-claims discipline,
  technical verification of feedback, and `Cannot verify from diff` branch are
  useful pack observations. The exact single-reviewer severity/readiness
  verdict is `pack-specific` and conflicts with M0's root-only terminal
  decision. Its suggested linked-worktree creation is outside M0's strict
  read-only boundary.
- Ponytail's explicit scope exclusion and evaluator negative controls are
  useful. Its delete-oriented taxonomy, `Lean already. Ship.` terminal, and
  `net: -N lines possible` score are `pack-specific`; importing them would
  narrow or distort a release-correctness review.
- Repetition across Matt and Superpowers supports only shared pack usage of
  separate “right thing” and “built right” judgments. It does not by itself
  prove behavioral efficacy or the optimal number of reviewers.

### Current Canonical Package

The complete current package contains two tracked files and was clean:

| Surface | Identity | Complete observation |
| --- | --- | --- |
| `skills/custom/convergent-pr-review/` | `git-tree:d2210fc11b357f1e2f69408a8a21bd9d422c677a` | Complete package inventory: `SKILL.md` and `agents/openai.yaml`; no package-local script, test, fixture, schema, or reference file. |
| `SKILL.md` | `git-blob:15feebd0924f654c83471a1f7dda5e897a3c5743`; `sha256:da8d687c07a2ff3807d40fecec12ee30651d18e305cc2ded9cfe9ffd881e4a2b` | Implements root-only and terminal read-only boundaries; Pin/Trace/Isolate/Challenge/Verify/Return; three modes; separate Standards and Spec; fresh direct reviewers; exact two/one/zero/uncovered capacity rows; root-owned five-state ledger; shared finding/advisory contracts; drift; and four decisions. |
| `agents/openai.yaml` | `git-blob:b17490601a06bb1736795ba577374241e930a78f`; `sha256:0db70780b798c1cd76dd76a999d55e023249ebe2c1ba57b3beba2fea56985a18` | Keeps implicit invocation and names one immutable high-risk target, fresh reviewer coverage, and one terminal decision. |

The shared contracts directly loaded by the current skill were also read:
`FINDING-CONTRACT.md` at
`sha256:f99446f46d3f6f31b58d0dfecb31c3602742d1e7f8b14f43414f0575b7a6cc95`,
`ADVISORY-CONTRACT.md` at
`sha256:5edf5100cd8ff6d924d93866100f0c2c80f17751c999985105eb5bf0a6003972`,
and `SMELL-BASELINE.md` at
`sha256:966b35b7da2690a5df33d697b43b3c0bd41891b1a5e554c2f0b266610ac2259f`.
They respectively own five-gate finding admission, optional nonblocking
advisories, and fallback-only maintainability prompts.

Current behavior is substantially compatible with M0. Research-visible
precision opportunities remain:

1. “Record the index tree” and “record status” name evidence surfaces but do
   not constrain the exact command recipe. `git write-tree` creates objects,
   and default `git status` may write cached index metadata, so an agent can
   violate the promised read-only boundary while believing it is only
   inspecting.
2. Live-state capture names the right composite surfaces but does not require a
   full, object-format-qualified manifest, a command allowlist, a before/after
   Git-administration check, or an explicit atomicity limit.
3. Fresh context, direct-child identity, and nonparticipation are useful local
   isolation conditions, but the current word `independent` does not disclose
   same-model, same-training, same-specification, or same-prompt common-mode
   risk.
4. The typed reviewer return records coverage, skipped checks, and blockers,
   but the root Return lacks a per-lens coverage table. Reviewer count can
   therefore be mistaken for coverage.
5. Candidate closure is required, yet no explicit valid status/verification
   state table distinguishes every rejected, duplicate, and disputed terminal
   combination.
6. The current decision prose does not fully order stale capture, an admitted
   blocker, uncovered required lenses, and optional uncertainty. Its early
   `incomplete` paths also lack one exact report form.
7. Remediation preserves carried IDs in the brief but does not require an
   explicit disposition for every carried ID in Return or name affected-reach
   expansion.

These are candidate improvements, not research-proven runtime defects.

### Synthesis And Hash-Bound Historical Conclusions

The complete current synthesis,
`docs/synthesis/skills/convergent-pr-review.md`, was read at
`sha256:8ac88b787d761ad66bb5074950742a59e304034922a69e5a64c1317fdda7212b`.
It is an exhaustive proposed design and extraction map, not executable
authority. It independently identifies many of the current-package precision
gaps above, proposes a finite lens plan, artifact-authority table, valid ledger
states, decision precedence, early Return, and affected remediation reach, and
requires control-versus-candidate behavior evaluation. Those conclusions are
`historical-admission-only` for this pass: they may supply hypotheses and
collision checks after blind discovery, but they cannot establish
professional validity or H1 efficacy.

The package has twelve path-affecting commits from 2026-07-10 through
2026-07-19; the synthesis has one introducing commit on 2026-07-20. Commit
history was inspected to establish lineage, not to treat superseded wording as
current behavior.

Four cited historical evaluation records were inspected:

| Record | Identity and evidence | Limit |
| --- | --- | --- |
| Root-only orchestration, 2026-07-18 | `sha256:916c361fa6adc08ee1ee4d79047f1489ce759ad2cd7c96bcfef66284c798e53e`; five no-skill controls failed and five candidate samples passed the delegated root-guard rubric at candidate hash `e28eec5a...` | Proves one bounded routing predicate at a prior skill hash only. |
| Coordinated v2, 2026-07-18 | `sha256:56646a6d0fbe03095a905c8857a8b6884748565c4e92b3b901bdec12e0376095`; five controls failed the full rubric and five candidate samples passed capacity, advisory, route, root-guard, friction, and slot-policy cases at candidate hash `e28eec5a...` | Classification simulation, not live reviewer correctness, ledger transitions, or current-hash proof. |
| Cohesion follow-up, 2026-07-12 | `sha256:e2a90662bc2c8bf165c0922aff20a788776977f8c7b34a86cad2eadfad948282`; recorded the one-way Review-to-Convergent high-risk handoff at hash `eb6c8101...` | Older hash and composition-boundary evidence only. |
| Cohesion boundary, 2026-07-13 | `sha256:e8458ca632347e4e583ae5c0943e42ebcedf0c98f1ac0c76030764a09da2e12f`; simulated fresh-context isolation and four decision states at hash `1ca78d72...` | Contract simulation; no live review children for the exact reviewer protocol. |

### Applicable Local Language Intake

The applicable sections of six packets were inspected after upstream and
current behavior:

| Packet identity | Applicable intake | Disposition and limit |
| --- | --- | --- |
| `03-high-signal-steering-words.md`; `sha256:32bc41dc17525f51c53c528daf10e2f7f046ae9f05d3b63d1e96784d469ca41c` | `fixed-point review`, evidence, proof, bounded slice, residual risk | Candidate professional/local vocabulary; not current runtime or behavioral proof. |
| `04-agentic-bridge-vocabulary.md`; `sha256:d56adad6c5066d9f02215ca96b78b8213de5fbbbb2fbc9c1397eb30d1d644f01` | fixed point, completion criterion, criteria-bound judgment, context isolation, evidence | Agent-control bridge only; each term still needs an observable action and gate. |
| `upper-bound-engineering-language.md`; `sha256:dab0407c917ffa7f17f1f4e41c7b2b1b69978c76887cd69f9c75e16574657572` | fixed-point dual-axis review, qualified independence, evidence before claims, completion, behavior-gate/evaluator self-test | Cross-pack synthesis explicitly leaves behavioral transfer and local suitability untested. |
| `matt-pocock-skills-vocabulary.md`; `sha256:ad812a4bee0f478c3dbacb0f17b8b27dc45fc8176f24a7c768facf98b49a5b65` | fixed point, two-axis review, completion criteria | Same frozen upstream identity; source profile, not independent corroboration. |
| `superpowers-skill-pack-vocabulary.md`; `sha256:93b9eb80d80ee45891310767fd976b6ff39e155459fbcd6df86b02f65f634e27` | two-verdict task review, file-backed review package, evidence before claims, technical verification of feedback | Same frozen upstream identity; narrower task protocol and no current behavioral eval corpus. |
| `ponytail-skill-pack-vocabulary.md`; `sha256:5fdcc282b7b3e394911f3da3a11ecf948bdf53b67f95e3a6c3aa0cbc5971ff9b` | explicit scope boundary, behavior gate, instrument-first negative control, qualified baseline | Same frozen upstream identity; complexity-review vocabulary and quantitative terminal are not general release-review methods. |

Every packet is `historical-admission-only`. Its original `direct`,
`corroborated`, `synthesis`, `inference`, or `thin` label was retained.
Repetition with the same frozen checkout was not counted as new support.

## Targeted Verification Of Newly Observed Mechanics

Only mechanics first observed or made decision-relevant in Phase 2 were
verified. All sources were inspected on `2026-07-24`.

| ID | Source and access | Verified mechanic | Classification and H1 consequence |
| --- | --- | --- | --- |
| T01 | Git project, [`git-worktree` current manual](https://git-scm.com/docs/git-worktree.html), complete Description, `add`, and Details material | `git worktree add` creates a linked worktree, checks out content, and adds repository-resident administrative metadata. It may also create a branch when a commit-ish is omitted. | `independently-supported`: the Superpowers suggestion is a Git-state mutation and cannot appear in an M0/H1 read-only reviewer recipe. A temporary directory outside the main checkout does not make the operation read-only. |
| T02 | Git project, [`git-status` current manual](https://git-scm.com/docs/git-status.html), Background Refresh | Default `git status` may refresh and write cached index stat data; `git --no-optional-locks status` suppresses that optional write path. | `independently-supported`: H1 should make non-mutating status invocation observable rather than rely on the adjective “read-only.” |
| T03 | Git project, [`git-write-tree` current manual](https://git-scm.com/docs/git-write-tree.html), complete manual | `git write-tree` creates a tree object from the current index and writes it to the object database. | `independently-supported`: it is unsuitable for a strict no-Git-mutation index identity. H1 needs a read-only index-entry manifest or must disclose that the requested identity cannot be obtained under the boundary. |

No newly observed upstream mechanic supplied evidence that voting, a
reviewer-owned readiness verdict, linked-worktree creation, or a quantitative
line-reduction score would improve M0. Those lanes were rejected rather than
searched for corroboration.

## Final Method Classifications And H1 Candidate Lanes

### Method classifications

| Method | Classification | Applicability, alternatives, and consequence |
| --- | --- | --- |
| Full content OIDs for committed targets plus a declared composite manifest for live state | `independently-supported` | Strong for byte identity within declared Git/path scope. It does not prove authenticity, semantic completeness, ignored/external state, or atomic capture. H1 should qualify those limits. |
| Non-mutating capture command surface with optional-lock/helper suppression and Git-administration read-back | `independently-supported` | Stronger than a general read-only promise. Exact cross-version/cross-platform command syntax remains to be validated as candidate-owned proof. |
| Portable Git-only atomic identity for a dirty multi-file worktree | `unverified` | Sequential equality detects drift but not a mixed-epoch capture. Quiescence or an external snapshot is the alternative; otherwise Return `incomplete` when atomicity is required. |
| Qualified non-author review, differentiated perspectives, and sealed initial judgments | `independently-supported` | Supported under risk- and expertise-dependent conditions. Fresh context is an isolation mechanism, not the whole professional definition of independence. |
| At least two fresh contexts as the universal optimum | `contested` | Two outperformed one but four did not outperform two in one study; standards allow one qualified assessor and ordinary industrial review commonly uses one. Preserve the exact M0 capacity rule as local intent, not universal science. |
| Multi-agent debate, consensus, or vote count as truth | `contested` | Correlated errors and social influence weaken vote semantics; structured later discussion can still expose counterevidence. H1 should preserve blind first passes and root evidence adjudication. |
| Candidate/evidence/finding separation, stable provenance, explicit duplicate/dispute states, and admission before severity | `independently-supported` | Strong across assurance, inspection, interchange, and vulnerability-record sources. Exact fingerprint or dedup algorithm remains `unverified` and should not be invented in H1. |
| Required evidence gap as `incomplete`, not clean and not automatically a finding | `independently-supported` | A target's violation of a requirement to supply proof may still be a finding; reviewer inability to obtain evidence is a coverage condition. H1 should keep the two cases explicit. |
| Assessment separated from caller risk acceptance | `independently-supported` | Supports M0's caller-owned Lock/risk boundary. Conditional progression is `contested` where policy, safety, or law forbids acceptance. |
| Stable finding identity plus affected-reach reassessment | `independently-supported` | Supports remediation without reopening untouched scope; changed dependencies widen the assessed reach. |
| Severity-free, nonblocking advisory annex | `independently-supported` | Supported as a requirements-versus-improvement distinction. The exact local advisory schema is `pack-specific`. |
| Matt's verbatim two-report aggregate | `pack-specific` | Axis preservation is useful; no root verification or convergence makes the exact aggregate unsuitable. |
| Superpowers' single reviewer severity/readiness verdict and range file | `pack-specific` | The frozen range package is useful context transport; reviewer-owned release judgment conflicts with M0. |
| Ponytail's delete tags and net-line terminal | `pack-specific` | Useful only for a bounded complexity lens and carries false-precision risk. |
| Exact runtime effect of any proposed term or clause | `unverified` | Requires Prompt 2's exact H1 and later control/treatment behavioral evaluation; source appeal cannot substitute. |

### Intent-adjacent H1 candidates

These are decision lanes for Prompt 2, not approved wording. Each remains
compatible with the frozen M0 floor.

| Candidate term or method | Recruited behavior | Expected M0 weakness addressed | Observable H1 gate | Comparative proof |
| --- | --- | --- | --- | --- |
| **Non-mutating snapshot manifest** | Resolve full committed OIDs; enumerate live `HEAD`, index entries/stages/OIDs, tracked worktree bytes, untracked paths/bytes, ignored policy, and nested state through an allowlisted non-writing surface; record object format and capture limits. | M0-06/M0-18 name the surfaces but not the safe acquisition mechanics, leaving room for default `status`, `write-tree`, helpers, fetch, or partial path/hash capture. | V08-V10/V21 variants record identical `.git` administration/index hashes before and after capture, reject `worktree add`/`write-tree`, detect same-status byte drift, and expose ignored/submodule/atomicity limits. | Run fixed clean, staged, unstaged, untracked, same-status-content, submodule, and concurrent-writer fixtures against M0 and H1; require the control to exhibit the targeted capture/mutation failure before promoting. |
| **Qualified review coverage** | Record for each lane its assigned perspective, non-authorship/participant status, fresh-context mechanism, shared model/spec/prompt dependencies, completed coverage, and common-mode limit; seal the first report before challenge. | M0-10/M0-12 can let “fresh context” and reviewer count imply stronger professional independence than was actually obtained. | V14-V17 expose every required lens and achieved capacity without calling root self-check independent; same-model/common-spec correlation is disclosed and never converted into votes. | Seed contaminated, implementation-participant, inherited-context, same-model-agreement, one-fresh, and zero-fresh cases; compare capacity truth, singleton-defect preservation, and false-consensus language. |
| **Evidence tuple plus correlation identity** | Normalize each candidate as criterion/anchor, supported scenario and reach, direct evidence, impact, origin, and stable correlation/duplicate links before severity. | M0-14/M0-16 require a five-state ledger but do not prescribe enough evidence shape to make superficial duplicate collapse or disagreement resolution auditable. | V18-V19 retain singleton supported findings, collapse only same-condition duplicates, link cross-axis overlap, preserve contrary evidence, and leave no candidate/unverified item. | Seed true duplicates with different wording, similar wording for distinct causes, cross-axis overlap, one true singleton, and one popular false claim; compare admission and loss rates. |
| **Coverage determination before release classification** | Close every required lens/evidence cell as supported, other-than-supported with reason, or not assessed; only then derive the release state by explicit precedence. | M0-19 defines four decisions, but missing evidence, verified blockers, optional uncertainty, and stale capture can still be narrated inconsistently without one ordered table. | V22-V24 exercise stale-plus-blocker, blocker-plus-uncovered-lens, uncovered-no-blocker, optional-not-checked, degraded-clean, and full-clean cases with no false-clean axis. | Table-driven control/candidate samples score the exact decision, coverage disclosure, partial verified evidence, and caller-owned residual-risk boundary. |
| **Affected-reach reassessment** | Preserve carried IDs; map Repair delta, callers/dependencies, remaining acceptance, resolved/still-admitted/disproved/incomplete dispositions, and any newly affected seam. | M0-05/M0-20 require carried state but can lose an ID, reopen untouched scope, or miss a Repair-created regression without an explicit reach map. | V06 and remediation variants dispose every carried ID exactly once, reject ID drift, limit unchanged scope, and widen only through evidenced dependencies. | Compare original/successor fixtures with one fixed finding, one unchanged finding, one disproved claim, one Repair regression, and one irrelevant untouched surface. |
| **Instrument-first behavior evaluation** | Prove each evaluator accepts known-good behavior and rejects a lazy-plausible bad output before spending samples on H1. | M0's viability suite can be weakened by structural word checks or a scorer that rewards the requested format rather than the behavior. | Each promoted claim has a red-capable negative control, exact target identity, fixed rubric/settings, and known-good/bad scorer self-test. | This belongs to later evaluation, not runtime. Compare M0/H1 only when the control reproduces the claimed failure and the instrument discriminates semantics rather than term presence. |

### Rejected lanes after reconciliation

- Do not create a linked worktree, tree object, stash, branch, commit, or
  persistent ledger inside a strict read-only review.
- Do not replace root evidence admission with majority vote, consensus, model
  debate, reviewer severity, or reviewer readiness.
- Do not present exactly two reviewers as a professionally established optimum.
- Do not import Ponytail's net-line score or delete-only scope into a release
  correctness gate.
- Do not add a snapshot helper, machine schema, or persistent reference merely
  because the current prose is dense. First prove irreducible mechanical
  variance under an exact H1 candidate.
- Do not use a hash, Git object ID, or clean `status` as proof of authenticity,
  complete environmental state, atomic capture, or semantic correctness.

## Gaps, Stopping Basis, And Caller Boundary

### Intent result

No inspected professional evidence showed that M0 omitted behavior essential
to its settled intended outcome. Professional definitions qualify what
“independent” can honestly mean, but M0 already requires factual isolated
passes, rejects inherited/participant lanes, preserves separated root fallback,
forbids vote-based admission, reports residual risk, and makes direct root
verification decisive. Common-mode disclosure and a non-mutating capture
recipe are therefore H1 refinement candidates inside M0-06, M0-10, M0-12,
M0-14, M0-18, and M0-19, not grounds to rewrite Prompt 1.

### Residual evidence gaps

- No direct controlled study establishes the optimal reviewer count or
  perspective partition for high-risk PRs, and no source proves that fresh LLM
  contexts produce statistically independent errors.
- The exact non-mutating Git command recipe still needs candidate-owned
  validation on supported Git versions and platforms. In particular, a
  portable Git-only atomic dirty-tree capture remains unverified.
- No direct study compares the proposed evidence tuple, coverage determination,
  or affected-reach map against this skill's current ledger.
- Upstream source inspection proves instructed mechanics, not their runtime
  effect. Matt has no review behavior fixtures; Superpowers' behavioral corpus
  is external and unavailable; Ponytail does not evaluate its review skill.
- Historical local evaluations are hash- and scenario-bound and do not prove
  the current runtime or a future H1.
- External standards are analogical outside their governing security, audit,
  safety, vulnerability, or evidence-synthesis domains. Their conditions and
  risk levels must remain visible.
- No practitioner conversation was needed because the governing and primary
  sources resolved every material operational condition at research scope.

### Stopping basis

Every load-bearing M0 research cluster now has:

1. governing or original primary support and a material counterposition;
2. observed behavior and explicit limits for all three frozen upstreams;
3. complete current-package identity and behavior inspection;
4. synthesis, historical, and language-packet intake separated from current
   authority and behavioral proof;
5. targeted official verification for every newly decision-relevant Git
   mechanic; and
6. one explicit method classification and H1 consequence.

Further source searching was unlikely to change a method, condition,
classification, intent result, or H1 lane. The remaining gaps require an exact
candidate and comparative behavior, not another general source.

Caller-use boundary: this packet supports Deploy Prompt 2 only. It does not
select exact H1 language, change M0, authorize runtime/synthesis/test/install
edits, claim behavioral efficacy, or perform Git delivery.

<!-- END RESEARCH PACKET -->

## Research Pass Decision

Status: `research-complete`

```text
Authorized unit completed: Deploy Research Pass
Decision: research-complete
Campaign shape: pending
Runtime identities: current=git-tree:d2210fc11b357f1e2f69408a8a21bd9d422c677a; M0=specification-only@sha256:469734af7b346c0f327d07fbd2a001d8b3f76cd985aa7c9468a53c6944326e4e; H1=pending; V1=pending; P1=pending; canonical=pending; installed=pending
Artifacts changed: docs/research/skills/convergent-pr-review/RP-convergent-pr-review-20260724-01.md
Evidence used or reused: fresh blind primary-source discovery; complete frozen-upstream and current-package inspection; synthesis, historical evaluations, and language packets as historical-admission-only; no behavioral evidence reused
Residual gaps: optimal reviewer count, statistically independent LLM review, portable atomic dirty-tree capture, exact safe Git recipe, and candidate behavioral effect remain unproved
Recommended next unit: Deploy Prompt 2
Git HEAD: f3be70c31dd8f2ae9f12a75248065ef313790bda -> f3be70c31dd8f2ae9f12a75248065ef313790bda
Git delivery: pending
Exact stop reason: Research saturated without reopening intent; stopped before Prompt 2.
```
