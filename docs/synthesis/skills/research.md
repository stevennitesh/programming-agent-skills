# Research Evidence And Runtime Design Synthesis

Status: exhaustive design reference for a future Research rewrite; not an executable contract.

Runtime authority remains in:

- `skills/custom/research/SKILL.md`;
- `skills/custom/research/agents/openai.yaml`;
- the target repository's source, domain, engineering, and note conventions;
- each caller's question, decision, artifact, and next-transition authority;
- `docs/synthesis/skill-context-relationships.md`;
- tests and behavior evaluations; and
- the installed mirror.

The current canonical and installed Research skill family are identical. The current skill is intentionally compact and already protects the one-question, primary-source, one-note, caller-return, and no-write boundaries. This synthesis does not claim those instructions exhibit a behavioral failure, does not change runtime files, and does not authorize installation. A future rewrite must first lock its control and then prove that the candidate improves evidence judgment or predictability without adding research ceremony that costs more than it prevents.

## How To Read This Document

This synthesis uses the same four-layer architecture as Parallel Implement and Wayfinder:

1. **Orientation** states the outcome, selected design, vocabulary, and explanatory flow.
2. **Normative Design** is the sole authority for proposed Research behavior and relationships.
3. **Evidence And Rationale** preserves current-runtime evidence, deliberate non-changes, rejected machinery, and deferred hypotheses without adding rules.
4. **Extraction And Verification** places the design into runtime surfaces and defines the proof required before promotion.

Change proposed runtime behavior in Layer Two; explain it in Layer Three; place and prove it in Layer Four. The Design Verdict summarizes what is selected but creates no runtime authority. The Normative Home Index gives every behavior one owner. The Runtime Ownership And Change Map owns file placement. The Migration And Acceptance Matrix owns case coverage only.

Use this index for direct navigation:

| Question | Owning section |
| --- | --- |
| What outcome should Research own? | [North Star](#north-star) |
| What is selected, preserved, deferred, or rejected? | [Design Verdict](#design-verdict) |
| What compact runtime path is proposed? | [Leading-Word Research Model](#leading-word-research-model) and [End-To-End Explanatory Flow](#end-to-end-explanatory-flow) |
| Where does each proposed rule live? | [Normative Home Index](#normative-home-index) |
| When should Research run? | [Invocation And Admission](#invocation-and-admission) |
| What must the caller provide? | [Research Contract](#research-contract) |
| What may Research read, write, or decide? | [Authority And Mutation Boundary](#authority-and-mutation-boundary) |
| Which action is legal now and when is it complete? | [Derived Route Contract](#derived-route-contract) and [Operation And Completion Contracts](#operation-and-completion-contracts) |
| Which source owns which claim? | [Source Ownership And Evidence Roles](#source-ownership-and-evidence-roles) |
| How much evidence is enough? | [Assurance And Proportionality](#assurance-and-proportionality), [Triangulation And Conflict](#triangulation-and-conflict), and [Saturation Gate](#saturation-gate) |
| What does the claim ledger mean? | [Claim Ledger And Result Status](#claim-ledger-and-result-status) |
| When are research scouts economical? | [Scout Contract And Economics](#scout-contract-and-economics) |
| What may the note prove? | [Artifact Authority Contract](#artifact-authority-contract) and [Research Note Contract](#research-note-contract) |
| How are citations and containment verified? | [Verification Contract](#verification-contract) |
| What does Research return? | [Return Contract](#return-contract) |
| Which context loads for each branch? | [Runtime Context Loading Contract](#runtime-context-loading-contract) |
| Which skills may call or receive Research? | [Relationship Ownership](#relationship-ownership) |
| How should the eventual skill read? | [Proposed Runtime Semantic Surface](#proposed-runtime-semantic-surface) |
| Where does each rewrite change belong? | [Runtime Ownership And Change Map](#runtime-ownership-and-change-map) |
| What must pass before promotion? | [Staged Behavior-Evaluation Protocol](#staged-behavior-evaluation-protocol), [Migration And Acceptance Matrix](#migration-and-acceptance-matrix), and [Promotion Gate And Residual Gaps](#promotion-gate-and-residual-gaps) |

When any diagram, rationale, ownership row, or acceptance case disagrees with Layer Two, correct that other surface.

# Layer One: Orientation

## North Star

Research owns one outcome: answer one bounded source question with claim-level, freshness-aware, citation-verified evidence, then return that evidence to its owner through either one authorized durable note or a no-write result.

Research is a bounded evidence leaf. It may judge what the inspected evidence supports, conflicts with, or leaves unknown. It never owns the product, design, domain, implementation, tracker, policy, or personal decision that the evidence informs.

The quality target is not maximum source count or maximum apparent certainty. It is the smallest sufficient evidence set that preserves:

- exact question and scope;
- claim-specific authority;
- applicable version, date, jurisdiction, and fixed point;
- material counterevidence and conflict;
- citation entailment;
- explicit limits and unknowns;
- caller and mutation boundaries; and
- a checkable stopping reason.

A faster or cheaper research route is better only when these gates remain unchanged. Search volume, scout count, note length, and citation count are not quality metrics by themselves.

## Design Verdict

| Stratum | Selected shape | Runtime status |
| --- | --- | --- |
| Research core | One bounded question; one claim ledger; claim-owned evidence; proportional assurance; explicit conflict and unknowns; one saturation gate; one verified answer | Ready for counterfactual design evaluation before extraction |
| Output branches | One exact authorized tracked note, or cited inline evidence, blocker, or inadmissible packet with no tracked mutation | Preserve and sharpen |
| Delegated leaf | Accept a complete caller packet and return to that caller without selecting its decision or next transition | Preserve and formalize |
| Scout model | One root evidence judge, serial by default; direct fresh read-only scouts only for substantial disjoint source lanes whose likely reading savings exceed dispatch and verification cost | Add as a simple economic gate, not an orchestration system |
| Progressive disclosure | Keep universal research judgment in `SKILL.md`; disclose the durable note schema and optional scout packet only when their branch fires | Candidate runtime shape; prove pointer reliability before promotion |
| Rejected machinery | Mandatory source counts, numeric confidence scores, complete query logs, citation databases, knowledge graphs, automatic note indexing, always-parallel background research, automated source ranking, or a persistent research ledger | Excluded |
| Deferred hypotheses | Automatic note refresh, reusable source caches, formal systematic-review mode, machine-verifiable citation extraction, and adaptive scout width | Require observed need and independent proof |

The first rewrite remains one linear skill. It adds no helper, provider, state machine, search database, or campaign ledger.

## Proposed Invocation Description

> Research one bounded source question against claim-owning evidence and return a citation-verified answer, conflict, or blocker. Use when a direct user requests durable cited research or an authorized caller supplies one source question, scope, freshness, return owner, and note authority. Write at most one repo-local Markdown note; otherwise return cited inline evidence without changing tracked state.

This wording is a candidate, not runtime authority. Its evaluation must distinguish Research from generic lookup, open-ended literature review, diagnosis, prototyping, stakeholder elicitation, current-user judgment, and multi-decision planning.

## Capability Boundary

Research answers source questions. Route by the authority needed to resolve the gap:

| Gap | Owner |
| --- | --- |
| Inspectable primary or claim-owning sources can answer one bounded question | Research |
| Existing behavior, symptom, or cause is uncertain and must be reproduced or instrumented | `$diagnosing-bugs` |
| A runnable design or behavior verdict is required | `$prototype` |
| The current user owns a preference, trade-off, term, commitment, or judgment and the exchange is conversation-only | `$grilling` |
| The current user owns that decision and repo-backed durable domain capture must remain active | `$grill-with-docs` |
| One identifiable external stakeholder owns unavailable information | `$to-questionnaire` |
| A bounded interface, seam, adapter, ownership, or migration design must be chosen | `$codebase-design` |
| Several interdependent decisions and prerequisites need a durable route | `$wayfinder` after explicit human selection |

Research may expose that the question belongs elsewhere. It returns the classification without invoking another resolver or laundering that resolver's work into source research.

## Research Vocabulary

| Term | Meaning |
| --- | --- |
| **Research question** | One bounded question whose answer can be materially changed by inspecting sources; it may contain dependent subclaims but not unrelated decisions |
| **Supported decision or artifact** | The caller-owned use for the answer; it fixes relevance but grants Research no decision authority |
| **Load-bearing claim** | A proposition whose removal or reversal would materially change the answer, status, or caller use |
| **Owning source** | The source with authority for that claim kind in the applicable version, jurisdiction, time, or repository state |
| **Discovery source** | A secondary index, summary, snippet, citation trail, or lead used to find evidence; it does not support a load-bearing claim unless it owns a distinct synthesis claim |
| **Counterevidence** | Applicable evidence that weakens, narrows, or contradicts a proposed claim |
| **Claim ledger** | The in-memory and returned mapping from each load-bearing claim to status, evidence, applicability, freshness, counterevidence, and limits |
| **Saturation** | The checkable point where another bounded search pass yields no better applicable authority, new material claim, or unresolved counterevidence, or where an exact access or evidence boundary prevents closure |
| **Research note** | One time-bounded cited Markdown artifact; it records evidence as of a fixed point and is never self-updating truth |

## Leading-Word Research Model

The eventual runtime should expose this compact spine:

```text
Frame -> Trace -> Scout -> Appraise -> Triangulate -> Saturate -> Write -> Verify -> Return
```

- **Frame** locks one question, caller use, scope, freshness, assurance, and mutation authority.
- **Trace** decomposes the likely answer into load-bearing claims and maps each claim to its likely owning source class.
- **Scout** finds and reads evidence; it may delegate only disjoint read-only source lanes.
- **Appraise** judges authority, applicability, directness, freshness, methodological fit, and source limitations.
- **Triangulate** reconciles scope differences, seeks counterevidence, and classifies every load-bearing claim.
- **Saturate** proves why further bounded search is redundant or unable to close an exact gap.
- **Write** creates or updates exactly one authorized note; no-write branches skip it.
- **Verify** checks citation entailment, status, freshness, source identity, output completeness, and work containment.
- **Return** gives the evidence owner one terminal packet and stops.

Scout is an operation even when the root performs it alone. Parallel scouts are optional mechanics inside Scout, not a separate outcome.

## End-To-End Explanatory Flow

```mermaid
flowchart TB
    START["Direct or caller-invoked Research"] --> FRAME["Frame one question and caller use"]
    FRAME --> ADMIT{"Source-answerable and bounded?"}
    ADMIT -->|No| WRONG["Return inadmissible or exact missing-contract packet"]
    ADMIT -->|Yes| TRACE["Trace load-bearing claims to owning source classes"]
    TRACE --> LANES{"Substantial disjoint source lanes?"}
    LANES -->|No| ROOT["Root reads serially"]
    LANES -->|Yes| SCOUTS["Open bounded read-only scouts"]
    ROOT --> APPRAISE["Appraise authority, applicability, freshness, and method"]
    SCOUTS --> VERIFY_SCOUTS["Root verifies included scout citations"]
    VERIFY_SCOUTS --> APPRAISE
    APPRAISE --> TRIANGULATE["Seek counterevidence and reconcile scope"]
    TRIANGULATE --> CLASSIFY{"Every load-bearing claim classified?"}
    CLASSIFY -->|No| MORE{"A bounded lane can change the result?"}
    MORE -->|Yes| ROOT
    MORE -->|No| BLOCKED["Record unknown or conflict and saturation boundary"]
    CLASSIFY -->|Yes| SATURATE["Record saturation evidence"]
    BLOCKED --> SATURATE
    SATURATE --> WRITE{"Exact note authority?"}
    WRITE -->|Yes| NOTE["Write or update one cited note"]
    WRITE -->|No| INLINE["Assemble cited inline result"]
    NOTE --> VERIFY["Verify note, citations, status, and containment"]
    INLINE --> VERIFY
    VERIFY --> RETURN["Return answered, conflicted, blocked, or inadmissible packet"]
```

The diagram is explanatory. Layer Two owns admission, authority, classification, saturation, mutation, completion, and Return.

# Layer Two: Normative Design

## Normative Home Index

| Concern | Sole normative home |
| --- | --- |
| Invocation reach and question admission | [Invocation And Admission](#invocation-and-admission) |
| Required caller and direct-user input | [Research Contract](#research-contract) |
| Evidence judgment, decision ownership, and mutation scope | [Authority And Mutation Boundary](#authority-and-mutation-boundary) |
| Legal route from current working evidence | [Derived Route Contract](#derived-route-contract) |
| Operation entry, completion, and legal terminal branch | [Operation And Completion Contracts](#operation-and-completion-contracts) |
| Claim-specific source authority and source roles | [Source Ownership And Evidence Roles](#source-ownership-and-evidence-roles) |
| Required evidence depth | [Assurance And Proportionality](#assurance-and-proportionality) |
| Claim statuses and result status derivation | [Claim Ledger And Result Status](#claim-ledger-and-result-status) |
| Freshness and fixed-point applicability | [Freshness And Applicability](#freshness-and-applicability) |
| Counterevidence, conflict, and inference | [Triangulation And Conflict](#triangulation-and-conflict) |
| Scout admission, context, and return | [Scout Contract And Economics](#scout-contract-and-economics) |
| Search stopping evidence | [Saturation Gate](#saturation-gate) |
| What each research artifact proves | [Artifact Authority Contract](#artifact-authority-contract) |
| Durable note shape and one-file rule | [Research Note Contract](#research-note-contract) |
| Citation, answer, and filesystem proof | [Verification Contract](#verification-contract) |
| Context-loading triggers | [Runtime Context Loading Contract](#runtime-context-loading-contract) |
| External result forms | [Return Contract](#return-contract) |
| Overall terminal completion | [Completion Contract](#completion-contract) |
| Composition edges and exclusions | [Relationship Ownership](#relationship-ownership) |

## Invocation And Admission

Research remains narrowly implicitly invocable. Preserve `policy.allow_implicit_invocation: true` so a direct request for durable source evidence or an authorized caller's bounded source ticket can reach it. The description must require one source question and one cited note or cited return; it must not compete with generic web lookup, open-ended literature review, debugging, prototyping, interviewing, design, or decision-making.

Admit only when all predicates hold:

1. exactly one bounded research question exists;
2. inspectable sources can materially answer it;
3. one caller-owned decision, artifact, ticket, or requested understanding fixes relevance;
4. scope and exclusions distinguish a sufficient answer from a general topic survey;
5. applicable time, version, repository fixed point, and jurisdiction are known or explicitly irrelevant;
6. required assurance is proportionate and feasible with available source access;
7. one return owner is known; and
8. note authority is either one exact path, a direct user's general authorization to choose the repo convention, or `none`.

A comparative question remains one question only when all compared claims support one terminal answer under one scope and assurance standard. Split unrelated questions or caller uses before research.

For a direct user, infer obvious contract fields from the request and repository. Ask only when a missing field would materially change the evidence search, answer, or write authority. For a caller invocation, return every missing caller-owned field together; do not start partial research or ask the user to reconstruct caller context.

An inadmissible request returns the exact mismatch and evidence owner. Research does not invoke the alternative owner.

## Research Contract

Every admitted run locks:

```text
Caller and return owner:
Research question:
Supported decision, artifact, ticket, or requested understanding:
Scope and explicit exclusions:
Target repository and fixed point, when applicable:
Freshness: as-of date, version, jurisdiction, or not time-sensitive:
Assurance: ordinary | consequential | high-stakes, with reason:
Authorized source access and known constraints:
Authorized note path: <absolute repo-local path> | choose repo convention | none:
Write authority: create | update | none:
Time or source budget, when caller-bounded:
```

The contract controls relevance and sufficiency. It does not predetermine the answer, require a preferred conclusion, or permit Research to make the supported decision.

When the caller supplies a fixed source list, treat it as a required starting set, not a prohibition on necessary counterevidence, unless the caller explicitly bounds the work to summarizing only those sources. A summary-only request must be labeled as such and cannot claim a broader research conclusion.

## Authority And Mutation Boundary

Research owns:

- question framing inside the locked contract;
- read-only source discovery and inspection;
- claim decomposition;
- source-role, authority, applicability, freshness, and methodological judgment;
- counterevidence search and conflict classification;
- the claim ledger;
- one cited answer;
- exactly one authorized research note when permitted; and
- the terminal research packet.

The caller owns:

- the supported decision or artifact;
- acceptance of consequences outside the evidence question;
- tracker, specification, domain, ADR, implementation, configuration, and external mutation;
- whether to continue, widen, or commission another question; and
- the next workflow transition.

Scouts own only read-only evidence collection for their assigned lane. They do not classify the final answer, write the note, mutate any repository or external system, dispatch peers, or choose the caller's route.

External source use is read-only. Disposable captures may live under the target's authorized temporary convention and must be removed or explicitly returned as residual disposable state. A tracked run creates or updates exactly one authorized note. It never updates an index, README, bibliography database, source file, domain file, ADR, tracker item, or generated registry. When the repo convention requires a second tracked mutation, return the exact publication blocker or use the no-write branch.

Pre-existing dirty work remains user-owned. Verification compares the starting and ending state and proves the run added changes only to the authorized note, without claiming the whole worktree was otherwise clean.

## Derived Route Contract

This table is the sole proposed authority for which Research action or terminal branch is legal. It derives route from current working evidence and adds no persisted lifecycle or helper state.

| Current evidence | Legal action or return | Illegal shortcut |
| --- | --- | --- |
| Required contract field is missing | Complete **Frame** from repository evidence or return all missing caller-owned fields | Searching under an ambiguous question, freshness bound, or write authority |
| The question is multi-owner, decision-owned, runnable, causal, stakeholder-owned, or otherwise inadmissible | Return `inadmissible` with the correct evidence owner | Simulating another skill inside Research |
| Contract passes but load-bearing claims and source roles are not mapped | **Trace** | Searching a topic without a claim or authority map |
| Mapped claims lack inspected evidence | **Scout** serially or through admitted source lanes | Writing from snippets, summaries, memory, or unverified scout prose |
| Evidence exists but authority, applicability, freshness, method, or directness is unevaluated | **Appraise** | Counting citations as support |
| A claim lacks counterevidence check, contains unresolved scope divergence, or depends on inference | **Triangulate** | Choosing the newest, most official-looking, or most numerous source without claim-specific judgment |
| All load-bearing claims are classified but saturation is unproved | **Saturate** | Stopping because one plausible answer or arbitrary source count was reached |
| Saturation passes and exact note authority exists | **Write**, then **Verify** | Mutating another tracked file or publishing a note before the evidence state is explicit |
| Saturation passes and note authority is `none` | Assemble inline evidence, then **Verify** | Creating a tracked note or returning uncited prose |
| Verified note or inline result exists | **Return** | Continuing into the caller's decision or next workflow |

## Operation And Completion Contracts

This table is the sole proposed authority for operation completion. The named sections explain unique mechanics but cannot advance a run before this row passes.

| Operation | Enter when | Complete when | Legal nonterminal return |
| --- | --- | --- | --- |
| **Frame** | A direct or caller request reaches Research | One question, caller use, scope, exclusions, applicability, assurance, access, return owner, note path, and write authority are explicit; Admission is decidable | Complete missing-field packet or `inadmissible` packet; no research or mutation |
| **Trace** | Admission passes | Every provisional load-bearing claim has one likely owning source class, applicability bound, and search lane; known source disagreement and inference needs are visible | Exact untraceable-claim blocker |
| **Scout** | At least one mapped claim lacks inspected evidence | Every admitted lane returns direct source identities, inspected evidence, dates or versions, counterevidence, gaps, and limits; the root verifies every citation it may use | Access or source-availability blocker with attempted lanes |
| **Appraise** | Evidence has been inspected | Each source used for a load-bearing claim has a recorded role, authority, applicability, directness, freshness, methodological fit when relevant, and limitation | Exact source-fitness gap |
| **Triangulate** | Proposed claims and appraised evidence exist | Each load-bearing claim is `supported`, `conflicted`, or `unknown`; scope differences are reconciled; applicable counterevidence and inference premises are explicit | Material conflict or unknown remains visible for Saturate and terminal status |
| **Saturate** | Every load-bearing claim is classified | The best applicable authority was inspected; the required disconfirmation pass ran; one final bounded pass found no material new authority, claim, or counterevidence, or an exact access/evidence boundary explains why closure is impossible | `conflicted` or `blocked` evidence state; never a falsely answered result |
| **Write** | Saturation passes and note mutation is authorized | Exactly one new or existing authorized note contains the contract, answer, claim ledger, conflicts, limits, source trace, saturation basis, and caller-use boundary | Publication blocker with no extra tracked mutation |
| **Verify** | A note or inline result is assembled | Citation entailment, source identity, applicability, freshness, claim coverage, status derivation, answer limits, caller boundary, and filesystem containment all pass | Exact verification failure; preserve evidence and leave no false completion |
| **Return** | Verification passes or an earlier typed nonresearch branch applies | One complete terminal packet reaches the direct user or delegating caller and no downstream work starts | None |

## Source Ownership And Evidence Roles

Source selection is claim-specific. “Primary” describes proximity, not universal authority or quality. Use the source that owns the exact claim in the applicable state.

| Claim kind | Likely owning evidence | Common false substitute |
| --- | --- | --- |
| Actual behavior in the target repository | Source, configuration, tests, runtime evidence, and governing docs at the pinned fixed point, each for the fact it exposes | README summary, stale issue, memory, or a test interpreted as all supported behavior |
| Supported product, API, or library contract | Versioned official documentation, specification, release notes, and tagged source for the requested version | Current unversioned docs for an older version, blog tutorial, search snippet, or source implementation presented as a supported public contract |
| Standard, policy, regulation, or legal text | Issuing body's official text for the applicable edition, jurisdiction, and effective date | News summary, commentary, draft text, or another jurisdiction |
| Organization, product, schedule, or current-state fact | Current first-party record or authoritative API as of the locked date; independent corroboration when the claim is contested or self-interested | Cached snippet, undated page, or third-party aggregator |
| Empirical effect or performance claim | Original study, data, and method for what that study establishes; relevant replications or evidence syntheses for generality | Abstract-only reading, vendor benchmark generalized beyond its setup, or a single study treated as field consensus |
| Historical event or decision | Contemporaneous record, official archive, repository history, or direct artifact for the event | Later recollection presented as the original record |
| Aggregate synthesis | A methodologically relevant systematic review, standard, or official synthesis for the aggregate claim, with primary evidence inspected when a load-bearing limitation or dispute requires it | Treating every secondary source as discovery-only even when the synthesis itself owns the claim |

Assign each inspected source one or more roles:

- **owning:** directly governs or establishes the claim in the applicable scope;
- **corroborating:** independently supports an already owned claim;
- **counterevidence:** narrows or contradicts the proposed claim;
- **discovery:** points to evidence but does not support the claim used in the answer; or
- **inaccessible:** identified but not inspected, and therefore never cited as support.

Search-result pages, snippets, unsourced generated summaries, and scout narration are discovery evidence only. A citation points to the inspected source itself.

## Assurance And Proportionality

Assurance changes evidence depth, not the caller's decision authority:

| Assurance | Passing evidence |
| --- | --- |
| **Ordinary** | One exact owning source may support a stable normative or repository fact after applicability and contradiction checks; synthesis claims still expose their premises |
| **Consequential** | Every load-bearing claim has the best applicable owner plus independent corroboration or an explicit reason one uniquely authoritative source is sufficient; material counterevidence is actively sought |
| **High-stakes** | Applicable official, jurisdictional, versioned, and current authorities are inspected; methodological and scope limits are explicit; unresolved disagreement or missing professional judgment blocks a definitive answer |

Raise assurance when the question is volatile, contested, safety-critical, financially or legally consequential, or likely to be generalized beyond the evidence. Do not lower caller-required assurance silently. When the available evidence cannot satisfy the tier, return `blocked` or `conflicted` rather than filling the gap with source count or confident prose.

No fixed minimum citation count applies. One authoritative standard may conclusively own a narrow normative claim. Ten derivative articles may add no evidence. Empirical generalization, disputed history, self-interested first-party claims, and current-state claims often require independent evidence.

## Claim Ledger And Result Status

Every load-bearing claim records:

```text
Claim ID and proposition:
Status: supported | conflicted | unknown
Fact or labeled inference:
Owning evidence and citation:
Corroborating evidence:
Counterevidence:
Applicable version, date, jurisdiction, or fixed point:
Authority and methodological limit:
Answer impact:
```

Claim status means:

- **supported:** the applicable owning evidence directly supports the fact, or the labeled inference follows from cited supported premises without material unreconciled counterevidence;
- **conflicted:** applicable evidence materially disagrees after version, time, jurisdiction, population, definition, and source-purpose differences are reconciled; and
- **unknown:** a load-bearing claim lacks inspectable sufficient evidence under the locked assurance and access boundary.

The terminal research status derives mechanically from load-bearing claims:

| Research status | Predicate |
| --- | --- |
| `answered` | Every load-bearing claim is supported; remaining limits do not change the answer |
| `conflicted` | At least one load-bearing claim remains materially conflicted and no load-bearing claim is unknown for a more fundamental reason |
| `blocked` | At least one load-bearing claim is unknown because evidence, access, freshness, applicability, or authority is insufficient |

`inadmissible` is a typed pre-research return, not a research status. Non-load-bearing uncertainty remains in limits and never upgrades a result to false certainty.

## Freshness And Applicability

Every load-bearing citation records the dimensions that can change its meaning:

- as-of or access date for current facts;
- product, API, library, specification, or policy version;
- jurisdiction and effective date;
- repository path and fixed point for local code claims;
- population, environment, dataset, method, and evaluation window for empirical claims; and
- document edition or archived identity for historical sources.

Applicability precedes recency. A newer source for the wrong version or jurisdiction does not supersede the correct governing source. When two sources describe different scopes, record a scoped divergence rather than a false conflict.

A note is evidence as of its recorded bounds. Research never claims it will remain current. Updating an existing note requires a new authorized run against the exact path, a new freshness basis, and full verification; Git history, not an invented note-level revision ledger, preserves prior text.

## Triangulation And Conflict

Triangulation has four duties:

1. search for evidence that could falsify or materially narrow each proposed load-bearing claim;
2. distinguish normative intent, actual implementation, observed behavior, and empirical generalization;
3. reconcile differences in version, date, jurisdiction, definition, population, environment, and source purpose; and
4. label synthesis as inference and expose its cited premises.

Do not resolve conflict by majority vote, source prestige alone, or newest-date wins. Prefer the source applicable to the exact claim and state. When two applicable authorities genuinely disagree, preserve the disagreement, explain its answer impact, and return `conflicted` unless a higher governing authority or caller-locked rule resolves it.

An official vendor source owns its supported contract and statements, not independent proof of comparative superiority. Source code owns implementation at a revision, not necessarily the promised public contract. A paper owns what its data and method support, not universal generality. A test owns its exercised behavior, not every intended path.

## Scout Contract And Economics

The root is the sole evidence judge and note author. Research runs serially by default.

Open a direct scout only when all conditions hold:

1. the lane is a substantial body of reading rather than one page or query;
2. it has a disjoint source family, claim cluster, version, jurisdiction, or evidence role;
3. its likely reading time saved exceeds dispatch, context loading, root citation verification, and synthesis cost;
4. the root can inspect each return promptly; and
5. source access and the mutation boundary remain read-only.

Begin with no more than two scouts. Add another only when a still-unsearched independent lane remains material after early returns. The platform's five-subagent capacity is a ceiling, not a target. Bundle tiny related source checks with the root rather than creating lanes.

Independent judgment uses `fork_turns="none"` and a complete file-backed or prompt-bounded scout packet. Continuity work may receive the minimum recent context necessary but is not called independent. Scouts do not spawn.

Each scout receives:

```text
Research contract and return owner:
Assigned claim IDs and source lane:
Scope and exclusions:
Freshness, version, jurisdiction, and fixed point:
Assurance and disconfirmation duty:
Authorized source access:
Required source identities and citation anchors:
Return path or packet shape:
Mutation: none
```

Each scout returns:

```text
Lane and claim IDs:
Sources inspected, with direct identities:
Proposed supported, conflicted, and unknown claims:
Authority, applicability, freshness, and method:
Counterevidence and scope divergence:
Inaccessible or uninspected leads:
Limits and what was not checked:
Mutation confirmation: none
```

The root verifies every citation used in the final answer or note. Scout count, summaries, and consensus never substitute for source appraisal or saturation.

## Saturation Gate

Saturation is claim-driven, not query-count-driven. It passes only when:

1. every load-bearing claim is classified;
2. the best known applicable owning source was inspected or its exact access failure is recorded;
3. the assurance-specific corroboration or unique-authority reason is complete;
4. one bounded disconfirmation pass ran against the proposed answer;
5. conflicts were reconciled by scope or preserved as material conflict; and
6. the last bounded search pass produced no better authority, new load-bearing claim, or material counterevidence, or an exact source/access boundary makes further closure impossible.

Record the saturation basis, not every query. A blocked result records attempted source lanes, inaccessible owning evidence, and what observable change would permit another run. A caller time or source budget may end search, but it cannot convert unknown evidence into an answered result.

## Artifact Authority Contract

| Artifact or surface | Owns or proves | Must not substitute for |
| --- | --- | --- |
| Research Contract | Question, relevance, bounds, assurance, output authority, and return owner | Predetermined answer or caller decision |
| Search result, index, summary, or discovery source | A lead to inspect | Support for a load-bearing claim |
| Inspected source | The exact claims supported within its authority and applicability | Broader scope, another version, freshness not observed, or the final synthesis |
| Scout packet | Read-only lane evidence and gaps | Root appraisal, citation verification, status, note authority, or caller return |
| Claim ledger | Current mapping from claims to evidence, conflict, unknowns, and limits | The underlying sources or a separate durable state file |
| Research note | One cited time-bounded synthesis at the authorized path | Live truth, automatic freshness, caller decision, domain truth, specification, or implementation authority |
| Inline result | One verified no-write answer, conflict, or blocker | Durable repo state or permission to write a note |
| Return packet | Verified output identity, status, answer, citations, limits, saturation, and boundary | Downstream execution or acceptance by the caller |

When a note, ledger, scout packet, or source disagree, reconcile the claim against the inspected owning evidence and current applicability. Never edit a citation label or status merely to make the artifacts agree.

## Research Note Contract

Write only when the Research Contract authorizes `create` or `update` and one repo-local path is exact or may be chosen from an existing convention. Prefer the repo's established research-note location. When none exists and the direct user authorized a note without an exact path, use `docs/research/<slug>.md`. A caller must supply an exact path or explicitly delegate convention choice.

The durable note uses this semantic shape:

```text
Title: the research question
Status: answered | conflicted | blocked
Supports: caller-owned decision, artifact, ticket, or requested understanding
Scope and exclusions
Freshness: as-of, version, jurisdiction, and repository fixed point
Assurance and saturation basis

Answer
  concise answer with claim-level citations

Claim Ledger
  claim, status, fact or inference, evidence, counterevidence, and limit

Conflicts, Unknowns, And Limits
  material disagreement, inaccessible evidence, applicability limits, and what is not proved

Source Trace
  direct source identity, role, authority, applicable version or date, and supported claim IDs

Caller Use Boundary
  what the evidence may inform, what Research did not decide, and return owner
```

Exact Markdown rendering belongs in the future note-format surface. The schema must keep citations next to the claims they support; a bibliography alone is insufficient. Discovery-only and inaccessible sources may appear in limits but never as supporting citations.

A `conflicted` or `blocked` note is valid when the authorized caller requested durable research evidence and Saturation passes on the conflict or access boundary. It must not present an unsupported one-paragraph answer as settled.

## Verification Contract

Verification proves all applicable gates:

### Evidence

- every load-bearing claim appears in the ledger and answer;
- every supporting citation resolves to an inspected direct source rather than a search result or scout summary;
- the cited source entails the adjacent claim within its authority and applicability;
- inference is labeled and its premises are cited;
- material counterevidence, conflicts, unknowns, freshness risks, and assurance limits remain visible; and
- result status matches the claim-status predicates.

### Output

- the answer stays inside the Research Contract and caller-use boundary;
- the Return Contract is complete;
- a note was reread from disk, exists at the authorized path, and matches the verified answer; and
- inline evidence contains direct citations and makes no durability claim.

### Containment

- starting and ending work state were compared;
- pre-existing work remains preserved;
- this run added tracked changes only to the authorized note, or no tracked changes for the inline, blocked-without-note, or inadmissible branch; and
- disposable captures were removed or returned as explicit residual state.

Citation existence without entailment is a failed verification. A syntactically complete note without a supported status is not complete.

## Runtime Context Loading Contract

Load the smallest complete context for the selected branch:

| Trigger | Load now | Keep out |
| --- | --- | --- |
| Every invocation | `SKILL.md`, direct request or complete Research Contract, target repo instructions, and already named source pointers | Full caller conversation, unrelated tickets, every possible source, note schema, scout schema, or rationale |
| Exact authorized note branch | Proposed `NOTE-FORMAT.md`, existing note when updating, repo note convention, and starting work-state evidence | Scout procedure when no scouts are admitted; unrelated publication indexes |
| Scout economic gate passes | Proposed `SCOUT-BRIEF.md` and only the assigned lane's contract | Parent conclusion, peer returns, note-writing procedure, caller decision, or unrelated claim lanes |
| Repository claim | Exact governing source, tests, config, docs, ADRs, and fixed point needed for that claim | Whole repository by default |
| External source claim | Direct applicable source plus only necessary discovery and counterevidence paths | Broad web context unrelated to the claim ledger |
| Return-only or inadmissible branch | Contract, evidence pointer, exact missing gate, and Return Contract | Note and scout references |

The main skill must retain source appraisal, claim status, saturation, verification, Return, and completion because every research path needs them. Do not hide universal evidence judgment behind an optional reference.

## Return Contract

Every terminal Research invocation returns one of four forms:

| Return | Use when | Required content |
| --- | --- | --- |
| `answered` | Every load-bearing claim is supported | Question, concise answer, claim ledger summary, direct citations or note path, freshness and assurance, limits, saturation basis, mutation result, and return owner |
| `conflicted` | Applicable evidence remains materially conflicted | Question, competing claims and sources, reconciled scope differences, unresolved conflict, answer impact, saturation basis, note path or inline citations, and return owner |
| `blocked` | A load-bearing claim remains unknown | Question, exact missing evidence or access, attempted lanes, available supported evidence, observable unblock condition, note path when authorized, mutation result, and return owner |
| `inadmissible` | The request fails Admission or belongs to another evidence owner | Failed predicate, settled contract fields, correct owner, evidence already available, mutation `none`, and return owner |

For a caller-invoked run, return to that caller and stop. Do not recommend or invoke another skill, decide the caller's ticket, or mutate its state. For a direct user invocation, the answer may be terminal with `Next: none`; otherwise recommend at most one evidence owner or next skill and stop.

Every written return includes the absolute note path and confirms `create` or `update`. Every no-write return states `Tracked mutation: none`.

## Completion Contract

Research completes exactly one admitted run only when:

- the Research Contract is locked and every load-bearing claim is classified;
- the applicable assurance, triangulation, and Saturation gates pass;
- the answer, conflict, or blocker matches the claim-ledger-derived status;
- every supporting citation passes direct-source identity and entailment verification;
- freshness, applicability, inference, counterevidence, limits, and what is not proved remain explicit;
- exactly one authorized note changed or tracked mutation is `none`;
- pre-existing work and disposable-state obligations reconcile;
- one complete Return reaches the direct user or delegating caller; and
- no caller-owned decision, mutation, or downstream route has started.

An `inadmissible` run completes only when every failed or missing Admission predicate is returned together, the correct evidence owner and return owner are named, available evidence is preserved, and mutation is `none`.

A written `conflicted` or `blocked` note is completion only for durable evidence capture. It is never equivalent to an answered question or caller acceptance.

## Relationship Ownership

This table is the sole proposed authority for Research composition edges. Caller syntheses own their local trigger and packet construction; Research owns Admission, evidence procedure, note authority, and return.

| Caller | Verb | Callee | Trigger and return |
| --- | --- | --- | --- |
| Direct user | Invoke | `$research` | One bounded source question needs durable cited evidence or the user explicitly names `$research`; return the verified note, inline answer, conflict, blocker, or inadmissible packet |
| `$skill-router` | Recommend and stop | `$research` | One source question needs a cited repo-local note; the later Research invocation runs its own Admission |
| `$grilling` | Recommend and stop | `$research` | A source evidence gap blocks the current user-owned decision; Research later returns evidence without making that decision |
| `$to-questionnaire` | Recommend and stop | `$research` | The apparent stakeholder gap is answerable from inspectable sources; Research later runs independently |
| `$wayfinder` | Invoke | `$research` | One selected Research ticket supplies a complete contract; return answer, citations, limits, status, and approved note pointer to that ticket without selecting another operation |
| `$improve-codebase` | Invoke | `$research` | One selected candidate has one source-resolution need; return evidence, one authorized note pointer or `none`, and limits so Improve Codebase can reclassify |
| `$research` | Recommend and stop | `$diagnosing-bugs` | Admission shows the missing authority is causal reproduction or diagnosis rather than source evidence |
| `$research` | Recommend and stop | `$prototype` | Admission shows the question needs one runnable design or behavior verdict |
| `$research` | Recommend and stop | `$grilling` | Admission shows the current user owns the unresolved preference, trade-off, term, or commitment and the exchange is conversation-only |
| `$research` | Recommend and stop | `$grill-with-docs` | Admission shows the current user owns the unresolved repo-backed decision and durable domain capture must remain active |
| `$research` | Recommend and stop | `$to-questionnaire` | Admission shows one identifiable external stakeholder owns unavailable material knowledge |
| `$research` | Recommend and stop | `$codebase-design` | Admission shows one bounded interface, seam, adapter, ownership, or migration design must be chosen |
| `$research` | Recommend and stop | `$wayfinder` | Admission shows several interdependent decisions and non-conversational prerequisites need a durable route; the user must start Wayfinder later |

Research has no direct delivery relationship to To Spec, To Tickets, Implement, Parallel Implement, Domain Modeling, or tracker providers. It may name evidence implications but never creates their artifacts or starts their procedures.

# Layer Three: Evidence And Rationale

Everything in this layer informs the selected design but creates no runtime rule.

## Current Source Trace

| Source | Evidence retained for synthesis |
| --- | --- |
| Current canonical `skills/custom/research/SKILL.md` | Compact one-question boundary; primary-source trace; optional fresh-context scouts; supported/conflicted/unknown claim classification; one authorized note or no-write return; verification and caller return |
| `skills/custom/research/agents/openai.yaml` | Research is currently narrowly implicitly invocable |
| Git history for Research | The skill was deliberately simplified from explicit ownership and completion sections into one linear leading-word spine, then hardened around source authority, fresh scout context, one-file publication, verification, and caller return |
| Current upstream `mattpocock/skills` Research | Retains the seed idea: background reading against primary sources and one cited Markdown file in the repo; it does not supply this pack's authority, no-write, conflict, caller-return, or verification contracts |
| `docs/synthesis/skill-context-relationships.md` | Research is a bounded evidence owner used by Skill Router, Grilling, Wayfinder, Improve Codebase, and source-answerable Questionnaire gaps |
| Wayfinder runtime and synthesis | Research is AFK, answers one authoritative source ticket, and returns answer, citations, limits, and an approved note pointer without owning map state |
| Improve Codebase selected-candidate contract | Research receives one question, supported decision, scope, freshness, and `authorized note path: none` unless approved, then returns to caller reclassification |
| Structural tests | Protect fresh-context scouts, the two output branches, one-note order, status vocabulary, note shape, verification, and return ordering |
| Behavior-evaluation fixtures 11 and 35 | Protect no-write versus approved-note authority, pre-dirty containment, primary-source claims, conflicts, blocked lanes, second-file prohibition, citation verification, and caller decision ownership |

The upstream source inspected for this synthesis is the [current primary repository file](https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/research/SKILL.md). Future extraction must refresh that comparison rather than treating this snapshot as permanently current.

## Current Strengths To Preserve

- The current skill is already small enough to read cover to cover.
- Its one-question and one-note boundary makes mutation and caller return legible.
- `supported`, `conflicted`, and `unknown` are better than an unsupported confidence score.
- Fresh-context scouts are explicitly read-only and subordinate to root judgment.
- The evidence gate recognizes search repetition and uncloseable gaps.
- Verification distinguishes written-note proof from the no-write branch and preserves dirty work.
- Caller-invoked research returns instead of choosing the supported decision.

These strengths argue for a controlled rewrite, not an exhaustive runtime manual.

## Design Gaps Requiring Counterfactual Proof

The current text leaves several important decisions implicit. These are candidate failure hypotheses, not established behavioral failures:

- Admission does not sharply distinguish one source question from literature survey, diagnosis, prototype, stakeholder evidence, user judgment, or multi-question work.
- “Primary source” is too coarse to explain when a standard, source code, versioned docs, original study, or systematic review owns a particular claim.
- The claim ledger does not explicitly distinguish direct facts, labeled inference, discovery sources, counterevidence, or inaccessible leads.
- Freshness is named but applicability across version, jurisdiction, repository fixed point, population, and evaluation window is not fully specified.
- The current gate does not require a bounded disconfirmation pass or define saturation strongly enough to resist both premature stopping and endless browsing.
- Scout parallelism has a material-improvement predicate but no compact economic or width discipline.
- The durable note template does not record assurance, saturation basis, fact-versus-inference, or the caller-use boundary.
- Status derivation from claim status remains implicit.
- Citation presence is verified, but claim-to-source entailment and direct-source identity are not explicit.
- Caller packets are described in prose rather than one complete reusable contract.

Each proposed addition must prove it changes behavior under a realistic control. If the current skill already behaves correctly, prune the addition as a no-op.

## Why Claim-Owned Evidence Beats Primary-Source Absolutism

Directness matters, but authority is contextual. A specification owns a normative interface; source code owns implementation at a revision; an issuing body owns the effective standard; an original paper owns its data and method; and a systematic review may own an aggregate synthesis claim. Calling all secondary material invalid would discard legitimate synthesis authority, while treating every official or original source as sufficient would overstate self-interested, stale, narrow, or methodologically weak evidence.

The selected design therefore preserves primary-source pressure while making the actual rule claim-specific: inspect the evidence that owns the proposition in the applicable state, then triangulate when the claim, consequence, or source role requires it.

## Why Saturation Is A Gate

Research has two symmetric failure modes. It can stop at the first plausible source, or continue searching after the answer and uncertainty have stabilized. Arbitrary source counts solve neither problem. The claim ledger plus one disconfirmation pass and one no-new-material-evidence pass create a checkable middle boundary.

This does not make research mechanically complete. It makes the judgment inspectable: what claims matter, which authority owns them, what could falsify them, what remains unknown, and why another bounded pass is unlikely to change the result.

## Why Scouts Stay Optional

Independent source lanes can reduce elapsed reading time and confirmation bias. They also repeat context, searches, summaries, and root verification. For one narrow source question, a strong serial owner is usually cheaper and more coherent. The selected rule therefore treats parallel reading like any other economic decomposition: disjoint substantial lanes only, no duplicated conclusion prompts, and root verification before use.

## Deliberate Non-Changes

- Keep Research implicitly invocable under a narrow description.
- Keep one bounded question and one return owner.
- Keep exactly one tracked note as the maximum durable mutation.
- Keep a no-write branch for caller invocations without note authority.
- Keep source discovery and external access read-only.
- Keep the root as sole evidence judge and note author.
- Keep `supported`, `conflicted`, and `unknown` as claim statuses and `answered`, `conflicted`, and `blocked` as research statuses.
- Keep callers responsible for decisions, artifacts, tracker state, and next transitions.
- Keep local repo evidence, official external sources, specifications, original research, and source code within one general Research capability.
- Add no provider-specific browser, search, academic database, repository host, or citation-manager procedure.
- Add no executable helper in the first rewrite.
- Preserve unrelated dirty work and the target repository's note convention.

## Rejected Machinery

| Rejected idea | Reason |
| --- | --- |
| Mandatory two-source or three-source rule | Source count does not establish authority, applicability, independence, or entailment |
| Numeric source-quality or answer-confidence score | Compresses incomparable authority and uncertainty dimensions into false precision |
| Complete query and browsing ledger | High token and maintenance cost; saturation needs only claim-impacting lanes and blocked attempts |
| Always start a background agent | Wastes context and time for narrow questions and splits evidence judgment from the owner |
| One scout per claim | Creates coordination proportional to claim count rather than reading economics |
| Persistent citation database, knowledge graph, or evidence JSONL | Duplicates source and note state without a proved recovery or reuse need |
| Automatic repo-note indexing | Exceeds the one-note authority and couples Research to publication setup |
| Auto-refresh or “current forever” notes | Freshness must be rerun against an explicit as-of contract |
| Research-owned recommendation or decision | Crosses the bounded evidence-leaf boundary |
| Full systematic-review procedure for ordinary engineering research | Adds screening, protocol, and bias machinery disproportionate to common source questions |

## Deferred Hypotheses

| Hypothesis | Evidence required before admission |
| --- | --- |
| Dedicated systematic-review mode | Repeated source questions genuinely need reproducible search strings, inclusion/exclusion screening, study-quality appraisal, and a flow record; separate invocation and artifact boundaries are proved |
| Citation-entailment helper | Manual citation errors recur; a helper can detect them without claiming semantic judgment or requiring a duplicate claim schema |
| Source cache or reusable evidence bundle | Repeated questions inspect the same versioned sources; invalidation and provenance are cheaper than fresh inspection |
| Automatic note refresh | A target repo owns freshness policy, triggers, mutation authority, review, and non-destructive update behavior |
| Adaptive scout width beyond the simple gate | Real evaluations show elapsed-time improvement after dispatch and verification cost, with no worse conflict, citation, or token tail |
| Durable claim-ledger sidecar | One note cannot preserve required evidence state without duplication, drift, or poor caller usability |

# Layer Four: Extraction And Verification

Extract the proposed behavior once. Keep universal evidence judgment in the main skill, branch-only artifact and scout mechanics behind sharp pointers, callers limited to packet construction and return use, and tests focused on semantic contracts rather than incidental prose.

## Proposed Runtime Semantic Surface

The eventual main skill should read approximately as:

```text
Outcome and bounded evidence-leaf boundary
Narrow implicit invocation and Admission
Research Contract
Frame -> Trace -> Scout -> Appraise -> Triangulate -> Saturate
Source ownership, assurance, claim status, and result status
Authorized note -> NOTE-FORMAT pointer | no-write branch
Optional parallel Scout -> SCOUT-BRIEF pointer
Verify
Return
Completion
```

This is a semantic target, not approved final wording. `SKILL.md` keeps the evidence rules every path needs. The note schema and scout packet may move behind precise context pointers only if evaluation proves those pointers fire reliably. If disclosure causes omissions, keep the compact contract inline rather than preserving a file split for appearance.

## Runtime Ownership And Change Map

The `Must not absorb` column is part of the design.

| Bundle | Surface | Owns | Proposed delta | Must not absorb |
| --- | --- | --- | --- | --- |
| `R1` | `skills/custom/research/SKILL.md` | Outcome, invocation, Admission, Research Contract, authority, leading-word route, source ownership, assurance, claim and result statuses, freshness, triangulation, saturation, context pointers, Verify, Return, and completion | Realize the proposed semantic surface; sharpen claim-owned evidence, proportional assurance, disconfirmation, saturation, citation entailment, pre-dirty containment, and caller return | Full note template, full scout prompt, caller workflow, provider/browser procedure, academic-review protocol, citation database, or source-scoring algorithm |
| `R1` | New `skills/custom/research/NOTE-FORMAT.md` | Durable note fields, claim-ledger rendering, source-trace rendering, note-only verification, and update semantics | Move the detailed note schema behind the exact authorized-note trigger if behavior evaluation shows no omission | Universal evidence judgment, Admission, search procedure, caller decision, route selection, or publication index mutation |
| `R1` | New `skills/custom/research/SCOUT-BRIEF.md` | Complete optional scout assignment and compact read-only return packet | Disclose only when the scout economic gate passes; preserve fresh-context independence and root verification | Scout-selection judgment, final classification, note writing, caller context, peer dispatch, or mutation authority |
| `R1` | `skills/custom/research/agents/openai.yaml` | Narrow implicit invocation policy and concise human-facing metadata | Preserve `allow_implicit_invocation: true`; describe one bounded source question, cited note or return, and evidence-leaf boundary | Runtime procedure, caller catalog, source taxonomy, or note schema |
| `R2` | Wayfinder runtime and synthesis | Research-ticket selection, complete caller packet, map state, claim, outcome, and next transition | Reconcile only fields required by the accepted Research Contract and Return; preserve AFK participation and caller ownership | Research source procedure, note schema, scout economics, or evidence status redefinition |
| `R2` | Improve Codebase selected-candidate contract | One candidate's source-resolution question and later reclassification | Supply the complete Research Contract with note path `none` unless authorized; receive the bounded return | Research procedure or final evidence judgment |
| `R2` | Grilling, Grill With Docs, To Questionnaire, and Skill Router surfaces | Their existing recommendation predicates and stop boundaries | Preserve the conversation-only versus repo-backed domain-capture admission split; update only if Research Admission or Return changes an accepted edge | Research procedure, automatic invocation, or caller continuation |
| `R2` | `docs/synthesis/skill-context-relationships.md` | Invocation policy, composition index, context ownership, supporting-file index, and boundary note | Index the accepted Research edges and any new disclosed references without copying procedure | Caller-local packets, source taxonomy, or completion rules |
| `R3` | `tests/test_skill_pack_contracts.py` | Structural protection | Cover invocation, semantic-surface roles, note and scout pointer triggers, statuses, mutation boundary, caller return, and relationship uniqueness | Exact prose order beyond machine-consumed contracts or claims of behavioral success |
| `R3` | `docs/validation/evals/core-workflows.md` and evaluation transcripts | Counterfactual behavior proof | Extend current Research fixtures across Admission, source ownership, applicability, assurance, triangulation, saturation, citations, scouts, note containment, and Return | Template echoes or source-count proxies for judgment quality |
| `R3` | Installed mirror `C:\Users\steve\.agents\skills\research` | Validated runtime copy | Synchronize only after the coordinated canonical candidate and behavior gate pass | Independent edits, partial synchronization, or authority over canonical source |

No helper or target-repo setup change belongs in the first rewrite. If `NOTE-FORMAT.md` or `SCOUT-BRIEF.md` fails its context-loading evaluation, collapse that contract back into `SKILL.md` rather than adding more pointers.

## Staged Extraction Plan

Implementation stages order work; they do not authorize partial installation.

| Stage | Bundles | Outcome | Boundary |
| --- | --- | --- | --- |
| `I1` | `R1` | Extract the complete Research-owned candidate and its optional references in canonical source | Every normative concern has one runtime destination; reference triggers and anti-duplication boundaries are explicit |
| `I2` | `R2` | Reconcile caller packets, return boundaries, invocation index, and supporting-file ownership | Each caller supplies only its owned contract and consumes the return without absorbing Research procedure |
| `I3` | `R3` | Replace brittle structural snapshots where necessary, add counterfactual behavior evaluation, validate, and synchronize after authorization | Positive and negative cases pass; no promotion-blocking residual gap remains; installed hashes match |

## Staged Behavior-Evaluation Protocol

Evaluation phases prove claims, not document completeness. Build the coordinated canonical candidate first. Do not synchronize the installed mirror until every applicable phase passes.

| Evaluation phase | Claims proved | Representative scenarios |
| --- | --- | --- |
| `E0`: Control lock | The current skill or no-guidance arm exhibits the precise claimed failure before candidate evaluation | One fixed red-capable scenario per promoted change, with current skill hash and source snapshot |
| `E1`: Invocation and attention | One source question invokes; wrong-owner or multi-question work does not; the Research Contract and correct branch pointers are found without speculative loading | Direct note request, caller packet, generic lookup, multi-question survey, runnable question, user decision, missing field, note and no-note branches |
| `E2`: Ordinary evidence work | Claim tracing, source ownership, applicability, assurance, appraisal, inference, triangulation, saturation, and citations produce a supported answer with proportionate legwork | Stable official contract, versioned API, pinned repo behavior, current fact, empirical claim, summary-only source list, unique authority, and independent corroboration |
| `E3`: Conflict, failure, scouts, and containment | Material conflict and unknowns remain visible; scout economics and root verification hold; one-note or no-write mutation boundaries survive dirty work and access failures | Version divergence, jurisdiction mismatch, official-versus-implementation drift, inaccessible owner, misleading search snippet, stale page, scout disagreement, pre-dirty note update, second-file convention, and disposable capture |
| `E4`: Integrated promotion | Callers, relationships, canonical files, references, tests, evaluations, installation, and mirror parity agree | Wayfinder and Improve Codebase returns, recommendation-and-stop callers, full validation, scoped install, and hash parity |

For every promoted behavioral claim, fix the prompt, Research Contract, repository and source snapshot, tool availability, model, reasoning tier, runtime settings, skill hash, and rubric across arms. Run at least five independent fresh-context samples per arm. Use the current skill as control where behavior overlaps and a no-candidate-guidance control for genuinely new behavior. Stop when the control does not exhibit the claimed failure.

Judge the actual answer, inspected sources, citations, source applicability, search decisions, mutation state, and return packet. String matches and note headings are structural evidence only. Record median, range or variance, worst observed result, protocol deviations, unavailable token or timing telemetry, and residual gaps.

Scout-efficiency claims additionally record agent-controlled elapsed time, fresh contexts, root verification load, duplicated source inspection, total tokens when available, citation defects, and worst-case result. Do not claim a scout strategy is better merely because it used more agents or finished one synthetic case faster.

## Migration And Acceptance Matrix

This matrix supplies implementation order and cases. The linked Layer Two sections remain the behavior authority.

| Implementation / evaluation | Bundles | Behavior | Positive case | Negative control | Verification |
| --- | --- | --- | --- | --- | --- |
| `I1,I2 / E1` | `R1,R2` | Invocation and Admission | A direct durable-evidence request or complete caller packet for one source-answerable question reaches Research and locks one contract; a direct user-owned mismatch recommends Grilling for conversation-only work or Grill With Docs for repo-backed durable capture | Generic lookup, open-ended survey, multiple unrelated questions, diagnosis, prototype, stakeholder evidence, user judgment, or incomplete caller packet starts research or mutation; the two interview entries are collapsed or invoked automatically | Invocation-policy test, caller packet fixtures, and fresh-context classification samples |
| `I1 / E1` | `R1` | Semantic surface and context loading | A fresh run identifies outcome, boundary, leading route, note or no-write branch, Verify, Return, and completion; only the note or scout reference whose predicate fires loads | The skill preloads both references, hides universal appraisal in a branch file, misses a required pointer, or loads caller workflow | Structural reference tests and context inventories across direct, delegated, note, inline, and scout branches |
| `I1 / E2` | `R1` | Research Contract and Trace | One bounded question maps every provisional load-bearing claim to an applicable source class and search lane | Topic-first browsing, predetermined conclusion, fixed source list treated as proof, or unrelated subquestions expand silently | Contract and claim-map fixtures plus output inspection |
| `I1 / E2` | `R1` | Source ownership and roles | Each claim uses the source that owns it in the applicable state; discovery, owning, corroborating, counterevidence, and inaccessible roles stay distinct | Search snippets, blogs, scout prose, wrong version, official marketing, source code, or a single paper are used beyond the claims they own | Claim-to-source adjudication scenarios and citation inspection |
| `I1 / E2` | `R1` | Assurance and proportionality | A narrow stable normative claim closes from one exact owner after contradiction check; consequential, contested, empirical, or high-stakes claims receive the required corroboration and limits | Mandatory source count adds derivative sources, or one source yields broad certainty where assurance requires more | Ordinary, consequential, unique-authority, empirical, contested, and high-stakes scenario set |
| `I1 / E2` | `R1` | Freshness and applicability | Version, date, jurisdiction, fixed point, population, environment, and method are recorded only where they affect meaning; applicability wins over nominal recency | A newer wrong-version source supersedes the governing source, or an undated result is called current | Version, jurisdiction, repo-SHA, current-fact, and empirical-window fixtures |
| `I1 / E2,E3` | `R1` | Triangulation, inference, and status | Scope divergence is reconciled; direct facts and labeled inference remain distinct; supported, conflicted, and unknown claims derive answered, conflicted, or blocked correctly | Majority vote, prestige, newest-date wins, hidden counterevidence, unlabeled inference, or unsupported answered status succeeds | Conflict and status table scenarios with output inspection |
| `I1 / E2` | `R1` | Saturation | Best authority, assurance, disconfirmation, conflict handling, and a no-new-material-evidence pass produce a checkable stop | First plausible source, arbitrary count, time budget, or endless low-value browsing substitutes for saturation | Search-sequence fixtures and control-versus-candidate behavior evaluation |
| `I1 / E2,E3` | `R1` | Citations and verification | Every load-bearing claim cites an inspected direct source that entails it; inference premises and limitations remain visible | Citation exists but supports only the topic, points to a search result, comes only from a scout, or omits applicability | Citation-entailment rubric, direct-source checks, and manual output inspection |
| `I1 / E3` | `R1` | Scout economics and independence | Serial is default; at most two initial disjoint substantial lanes open; root verifies included citations; later widening has a material unsearched lane | One page gets a scout, five scouts start because slots exist, peers see conclusions, scouts write, or consensus replaces appraisal | Fixed serial, two-lane, duplicated-lane, disagreement, and capacity scenarios with time/token evidence when available |
| `I1 / E3` | `R1` | One-note and no-write containment | An authorized new or existing note is the only run-created tracked delta; inline, blocked-without-note, and inadmissible runs leave tracked state unchanged; dirty work survives | Research edits an index or source file, overwrites unrelated dirty work, claims the repo was clean, or writes a note from `none` authority | Pre/post work-state fixtures, pre-dirty update, second-file convention, and disposable-capture checks |
| `I1 / E3` | `R1` | Note contract | Answered, conflicted, and blocked notes preserve contract, answer, ledger, limits, source trace, saturation, and caller-use boundary | Bibliography without claim citations, false settled answer in a blocked note, live-truth claim, or missing caller boundary passes | Note-shape structural tests plus semantic note-reread rubric |
| `I1,I2 / E3,E4` | `R1,R2` | Return and caller authority | Caller-invoked runs return one complete packet and stop; direct runs may end with `Next: none` or one recommendation | Research changes caller state, decides its artifact, starts another skill, or forces a recommendation after a complete answer | Wayfinder and Improve Codebase caller fixtures plus direct-user behavior evaluation |
| `I1-I3 / E4` | `R1-R3` | Integrated promotion | Canonical runtime, optional references, callers, relationships, tests, evals, validation, and installed hashes agree | Partial file split, unresolved caller mismatch, unproved behavior claim, or independent mirror edit is promoted | Focused tests, full pytest, `scripts.validate_skills`, both diff checks, changed-file read-back, installation dry-run, scoped sync after authorization, and hash parity |

## Promotion Gate And Residual Gaps

The promotion record names each behavioral claim, implementation stage, evaluation phase, control and candidate hashes, fixed source and repository snapshots, Research Contract, sample count, tools, model and reasoning tier, rubric, median, variance or range, worst result, source-access deviations, unavailable telemetry, critical failures, and residual gaps.

A critical failure blocks promotion regardless of averages:

- unauthorized tracked or external mutation;
- fabricated, inaccessible, search-result-only, or non-entailing citation used as support;
- wrong version, date, jurisdiction, fixed point, population, or method materially changes the answer;
- material conflict, counterevidence, inference, or unknown is hidden;
- `answered` is returned while a load-bearing claim is conflicted or unknown;
- Research makes the caller's decision, mutates caller state, or starts downstream work;
- a scout writes, dispatches peers, receives contaminating conclusions, or substitutes for root verification;
- pre-existing work is overwritten or a second tracked file changes;
- note and inline branches claim the wrong durability or mutation state; or
- the Return Contract is incomplete.

Promote only when E0 demonstrates the claimed failure, the candidate materially reduces it, variance does not expose a new unstable tail, and no new critical failure appears. Additional text, source checks, scouts, or references must improve behavior enough to repay their attention, token, time, and maintenance cost.

A residual gap blocks promotion when it affects invocation, Admission, question scope, caller authority, note authority, source identity, source role, applicability, assurance, claim classification, counterevidence, saturation, citation entailment, mutation containment, result status, Return completeness, or caller ownership. Noncritical uncertainty may remain only when the promotion record names the evidence limit, operational consequence, and later validation owner.

Static validation proves structure. Upstream comparison supplies design pressure. Neither proves that the rewrite researches better.

## Completion Criterion For The Future Rewrite

The rewrite is complete only when every normative concern has one indexed home; the main skill exposes the proposed semantic surface without becoming a research manual; Admission reliably distinguishes Research from neighboring evidence owners; one complete Research Contract drives claim-owned source work; every load-bearing claim is appraised, triangulated, classified, saturated, and citation-verified; note and no-write branches preserve their exact mutation and durability boundaries; optional scouts improve their admitted cases without worsening token, citation, or worst-case results; every caller retains its decision and next transition; every acceptance row passes its positive and negative cases under the required evaluation phase; no promotion-blocking residual gap or critical failure remains; canonical validation passes; and the installed mirror matches the separately authorized validated source exactly.
