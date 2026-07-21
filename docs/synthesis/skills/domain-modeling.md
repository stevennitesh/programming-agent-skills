# Domain Modeling Durable-Truth Synthesis

Status: selected future design and coordinated extraction map. The inactive compact Steps 1-3 candidate is preserved under `skills/experimental/domain-modeling/`. This document and candidate are not runtime authority; the active canonical skill, its disclosed references, callers, tests, and installed mirror remain authoritative until the complete coordinated candidate is behaviorally proved, validated, promoted, and synchronized.

Current runtime authority remains in:

- `skills/custom/domain-modeling/SKILL.md` for active Domain Modeling behavior;
- `skills/custom/domain-modeling/CONTEXT-FORMAT.md` for active context-record representation;
- `skills/custom/domain-modeling/ADR-FORMAT.md` for active ADR assessment and representation;
- `skills/custom/domain-modeling/agents/openai.yaml` for active invocation policy;
- each target repository's routed `CONTEXT.md`, `CONTEXT-MAP.md`, and ADRs for accepted project truth and decisions;
- `docs/adr/0006-domain-modeling-records-approved-adrs.md` for the accepted ADR-recording ownership decision;
- `$grill-with-docs` for composition with `$grilling`;
- each invoking caller for supplied authority, continuation, and return;
- `$repo-bootstrap` for the domain-routing setup surface;
- `docs/synthesis/skill-context-relationships.md` for the pack-wide relationship index; and
- tests, behavioral evaluations, and installed mirrors only at their owned verification boundaries.

The experimental Domain Modeling candidate depends on the narrowly implicit residual-router candidate preserved under `skills/experimental/skill-router/`. The active custom Router remains explicit-only, so the Router edge and Domain Modeling candidate cannot promote independently.

## Guide

This synthesis has four authority layers:

1. **Orientation** states the selected outcome, vocabulary, boundary, and leading-word model.
2. **Normative Design** is the sole authority for proposed Domain Modeling behavior.
3. **Evidence And Rationale** preserves decision-changing pressure and deliberate exclusions without creating rules.
4. **Extraction And Verification** assigns every accepted change to one owner and one proof path.

Key paths: [runtime spine](#leading-word-runtime-model), [authority gates](#authority-gates), [representation branches](#representation-branches), and [migration matrix](#migration-and-acceptance-matrix).

# Layer One: Orientation

## North Star

Domain Modeling makes each in-scope change to durable project meaning explicit, source-traced, authority-settled, correctly represented, safely persisted or exactly rendered, and recoverable through one complete Domain Delta.

It owns:

- canonical terms and context-scoped ubiquitous language;
- concept and bounded-context boundaries;
- cross-context contracts and authority;
- durable domain invariants;
- contradictions among accepted records, evidence, decisions, and implementation; and
- assessment of plausible ADR candidates and recording of explicitly approved ADR-worthy decisions.

It does not own the participant interview, the underlying non-domain design decision, repository setup, code alignment, caller continuation, or downstream execution.

## Design Verdict

Keep one narrowly implicit Domain Modeling skill with two disclosed representation branches and one linear semantic spine.

| Concern | Selected design |
| --- | --- |
| Invocation | Admit durable-truth change or persistence, plus assessment or recording of an already-settled ADR-worthy decision |
| Participant judgment | Return unsettled judgment through the caller or, for a standalone terminal residual, the implicit Skill Router; `$grill-with-docs` owns the interview |
| Direct authority | Treat the direct user as decision authority unless the Source Trace names another owner |
| Context mutation | Require explicit persistence intent; otherwise Render exact domain-record changes |
| ADR mutation | Keep separate explicit approval and the branch mechanics in `ADR-FORMAT.md` |
| Representation | Keep exact context and ADR forms behind sharp pointers |
| Reconciliation | Reconcile only on material state changes |
| Return | Use a compact Domain Delta with semantic, persistence, and blocker state kept distinct |
| Promotion | Coordinate the Domain Modeling rewrite with the implicit residual Router and affected callers |

Do not add an ontology engine, event-storming method, code-renaming workflow, generic architecture process, persistent delta ledger, or third runtime reference.

## Durable-Truth Boundary

**Domain truth** is accepted project meaning for domain terms, boundaries, relationships, and invariants. **Source facts** are evidence-settled observations about current behavior or state. **Domain records** are routed context files and ADRs that persist accepted meaning and explicitly approved durable decisions.

Accepted vocabulary is consumed through repository routing without invoking Domain Modeling. Domain Modeling starts only when durable truth must change or be persisted, a material contradiction must be accounted for, or an already-settled decision needs ADR assessment or recording.

Domain Modeling may inspect code, tests, contracts, plans, issues, research, and runtime evidence when they can change a fact, expose a collision, or reveal a material consequence. It mutates only routed context records and explicitly approved ADRs. It returns all code, test, plan, spec, tracker, setup, and implementation consequences to their owners.

## Domain Vocabulary

| Term | Meaning |
| --- | --- |
| **Domain truth** | Accepted project meaning settled by named decision authority; current implementation may support or contradict it but does not silently redefine it |
| **Source fact** | An evidence-settled observation about current behavior or state |
| **Domain record** | Routed context files and ADRs that persist accepted domain truth and approved durable decisions |
| **Ubiquitous language** | Context-scoped canonical language used consistently with one meaning inside its owning context, never a forced global vocabulary |
| **Owning context** | The bounded context responsible for a concept's meaning, invariants, and changes |
| **Context relationship** | A cross-context contract with an explicit type and singular or joint authority model |
| **Domain contradiction** | An unresolved collision among accepted records, evidence, decisions, current usage, or context ownership |
| **Domain Delta** | The complete return packet for semantic resolution, per-target persistence, blockers, consequences, and return ownership |

Process states live beside their owning gates rather than in this vocabulary.

## Leading-Word Runtime Model

```text
Trace -> Challenge -> Resolve -> Reconcile -> (Persist -> Verify | Render) -> Return
```

| Leading word | Runtime meaning |
| --- | --- |
| **Trace** | Establish the subject, routed truth, load-bearing evidence, decision authority, mutation modes, target boundary, caller, and return owner |
| **Challenge** | Test proposed meaning through Overload, Alias, Leakage, Boundary, and Contradiction |
| **Resolve** | Record the accepted semantic core or the exact unresolved choice under its rightful authority |
| **Reconcile** | Update the cumulative delta and affected relationships after a material state change |
| **Persist** | Apply only explicitly authorized domain-record or approved ADR changes |
| **Verify** | Reread every changed domain record and reconcile actual state with the delta |
| **Render** | Produce directly applicable domain-record wording without writing |
| **Return** | Deliver the complete Domain Delta to its owner and stop |

## Explanatory Flow

```mermaid
flowchart TB
    START["Direct, invoked, or composed entry"] --> TRACE["Trace routing, truth, evidence, and authority"]
    TRACE --> CONSEQUENCE{"Durable consequence?"}
    CONSEQUENCE -->|No| NONE["Return minimal no-change delta"]
    CONSEQUENCE -->|Yes| CHALLENGE["Challenge collisions and boundaries"]
    CHALLENGE --> SETTLED{"Evidence and decision authority sufficient?"}
    SETTLED -->|No| OPEN["Record blocker or terminal residual"]
    SETTLED -->|Yes| RESOLVE["Resolve semantic core"]
    RESOLVE --> RECONCILE["Reconcile delta and relationships"]
    RECONCILE --> MODE{"Authorized action"]
    MODE -->|Context write or approved ADR| PERSIST["Persist, then Verify"]
    MODE -->|No write authority| RENDER["Render exact changes"]
    PERSIST --> RETURN["Return complete delta"]
    RENDER --> RETURN
    OPEN --> RETURN
    NONE --> RETURN
```

The diagram explains sequence. Layer Two alone owns the proposed gates and behavior.

# Layer Two: Normative Design

## Authority Gates

| Decision | Authority | Open branch |
| --- | --- | --- |
| Does Domain Modeling fit? | Domain Modeling admission | Consume routed truth, return to the current owner, or decline the pass |
| Is a source fact settled? | Inspectable evidence | Record an `evidence` blocker and keep dependent meaning open |
| Is domain meaning settled? | Direct user absent a named conflict, or caller-named domain authority | Return the exact contested choice; do not interview or invent agreement |
| Is a context boundary settled? | Named domain authority | Preserve responsibility, relationship, and authority conflicts in the delta |
| May a context record change? | Explicit persistence request or caller mode | Render exact context changes and write nothing |
| May an ADR be created? | Explicit approval for one identified candidate | Preserve the offered, deferred, declined, or unapproved outcome |
| Is persistence verified? | Fresh read-back of every changed target | Return exact per-target failure state; never claim intended state |
| May another workflow start? | User or caller with pre-existing continuation authority | Return and stop; delegate only an eligible standalone terminal residual to Skill Router |

## Invocation And Admission

Domain Modeling remains implicitly invocable under two narrow triggers:

1. durable domain truth itself must change or be persisted; or
2. an already-settled decision needs ADR assessment or explicitly approved recording.

It admits direct, caller-invoked, and `$grill-with-docs`-composed forms. Ordinary vocabulary consumption, a possible future gap, implementation work implied by a resolution, or an unsettled non-domain decision does not admit the skill.

A direct request to decide contested meaning is participant-judgment work, not standalone Domain Modeling interview authority. When that distinction is already visible, normal invocation or Skill Router should select `$grill-with-docs`. When Domain Modeling discovers it after admission, it records the unresolved choice and completes its pass; an eligible standalone terminal residual may then go to the implicit Router. Domain Modeling never invokes its composer directly.

Composed Domain Modeling accepts every settled material answer relayed from Grilling with its shared subject, source, and opaque identifiers. It maintains and returns the authoritative cumulative Domain Delta and returns domain collisions before dependent questioning continues. Caller-invoked Domain Modeling returns blockers to its caller rather than routing around it.

Admission grants no mutation or continuation authority.

## Inputs And Authority Lock

A structured packet is required only at caller and composer boundaries. Preserve caller identifiers and equivalent fields rather than translating them into a lossy universal schema.

The packet provides:

- bounded subject, governing source, and candidate consequences;
- relevant routed truth, accepted decisions, and pending Domain Delta;
- named decision and boundary authority;
- context action: `persist authorized` or `render only`;
- authorized paths or routing boundary;
- ADR action: `offer only` or approved candidate identifiers;
- caller and return owner; and
- caller continuation authority.

Standalone Trace derives the same authority lock from visible sources. The direct user is decision authority unless evidence names another owner. Missing persistence intent becomes `render only`; missing ADR approval remains `offer only`. Missing decision authority, routing, or return ownership stays open rather than widening authority.

## Trace And Routing

Trace only sources capable of changing an in-scope resolution:

- the request or caller packet;
- repository instructions and `docs/agents/domain.md` when present;
- the routed `CONTEXT-MAP.md`, relevant `CONTEXT.md` files, and relevant ADRs;
- accepted sources named by the caller; and
- code, tests, data contracts, runtime evidence, or downstream consumers only when they can settle a fact or expose a material collision.

Distinguish accepted domain truth, source facts, current usage, proposed language, caller-settled decisions, contradictions, and unavailable evidence. Historical sources and widespread code usage are evidence, not automatic semantic authority.

Select domain records in this order:

1. follow configured `docs/agents/domain.md` routing;
2. for configured multi-context routing, follow root `CONTEXT-MAP.md` to relevant contexts;
3. for configured single-context routing, use root `CONTEXT.md` and root ADRs;
4. without configured routing, an existing root `CONTEXT-MAP.md` selects multi-context; otherwise use the safe single-context fallback.

Missing domain records do not justify empty placeholders. Create a first record only for an authorized settled resolution.

A single-to-multi-context transition is two-owner work. Domain Modeling returns the accepted topology and exact routing requirement; Repo Bootstrap changes and verifies the setup mode; Domain Modeling resumes persistence only after routing agrees. Directory layout, package count, and service boundaries do not establish bounded contexts by themselves.

## Challenge

Challenge each proposed resolution through five lenses:

- **Overload:** one term names materially different concepts;
- **Alias:** several terms accidentally name one concept;
- **Leakage:** implementation detail or imported jargon poses as project domain meaning;
- **Boundary:** scope, context responsibility, relationship contract, or authority is unclear; and
- **Contradiction:** accepted records, ADRs, evidence, decisions, or observable behavior disagree.

Use concrete normal, edge, failure, inclusion, and exclusion examples only where they can change the resolution. Challenge completes when each material collision is settled or becomes an exact blocker with owner and impact.

## Resolve

Every resolution has a fixed semantic core:

- accepted term or decision;
- precise meaning independent of implementation;
- owning context;
- load-bearing sources; and
- decision authority.

Add included or excluded edges, aliases, conflicts, relationships, downstream consequences, or ADR candidacy only when material.

Record only domain-specific concepts. Generic technical vocabulary, ordinary business words, and code-index entries stay outside context records.

Evidence settles descriptive claims about current behavior. Named authority may settle normative intent despite contrary implementation, but the Domain Delta must expose the mismatch and return alignment work to its owner. Never persist a descriptive claim against contrary evidence.

Unsettled participant judgment remains unresolved. Domain Modeling may sharpen the exact choice and consequences, but Grilling owns the participant interview. Under composition, return the choice to Grilling. Under caller invocation, return it to the caller. For an eligible standalone terminal residual, invoke the implicit Router with the complete residual packet; the Router may select `$grill-with-docs` and starts nothing.

## Reconcile

Reconcile after a material resolution, newly discovered or cleared blocker, authority or scope change, supersession, persistence outcome, or verification outcome. Supporting observations remain in the Source Trace and do not trigger ceremonial packet rewrites.

When a new resolution supersedes an earlier one, mark the earlier meaning superseded, reconcile every affected context relationship and ADR status, and expose downstream consequences. Never leave two active canonical meanings without an explicit context distinction.

In composition, Domain Modeling receives each settled material answer with the shared subject, source, and relevant opaque identifiers. It classifies the domain consequence, updates its authoritative cumulative Domain Delta, returns any collision before dependent Grilling progress, and returns a minimal cumulative no-change delta when the considered subject has no durable consequence. Grilling remains the sole owner of answer materiality, questioning, and confirmation.

The cumulative delta uses caller identifiers and ordered material reconciliation events. Do not invent versions, hashes, or a persisted session ledger.

## Persistence Authority

Context action and ADR action are independent.

- **Persist authorized:** an explicit request such as persist, record, update the glossary, or an exact caller mode permits only routed in-scope context-record changes.
- **Render only:** resolve and reconcile normally, then return exact domain-record wording, target, placement, and relationship effects without writing.

Words such as resolve, decide, model, inspect, or review do not authorize persistence. ADR approval never authorizes unrelated context, code, spec, plan, tracker, setup, or implementation mutation. Context authority never authorizes ADR creation.

Before writing after user interaction or caller return, refresh routing and every target. Reconcile intervening edits and preserve unrelated work. If the target or authority is ambiguous, Render or return the exact blocker.

## Representation Branches

Read `CONTEXT-FORMAT.md` whenever Persist or Render must create or change a glossary, invariant, context map, or relationship. The main skill owns semantic resolution and mutation authority; the format owns exact representation.

The accepted future context format must support:

- canonical definitions in one owning context;
- optional context-owned `Invariants` for settled domain rules;
- singular controlling authority or explicit joint owners with a change rule;
- `customer-supplier`, `conformist`, `shared kernel`, and `translation` as preferred relationship labels;
- a custom relationship label only with explicit meaning, contract, and authority;
- owner, reference, or translation for cross-context language; and
- repeated shared definitions only for a genuine explicitly governed shared kernel.

An owning context defines canonical meaning. A consuming context relies on the relationship contract without duplicating the definition. A translation relationship defines each context's local term and mapping. Exact rendered output names the target path, insertion or replacement scope, complete wording, affected relationships, and ordering dependency.

Open the ADR branch only for a settled decision that plausibly represents a durable tradeoff. Read `ADR-FORMAT.md`; it solely owns worthiness predicates, approval mechanics, location, numbering, and representation. Domain Modeling is the pack's single ADR recorder, not the universal decision owner. Non-domain decisions arrive settled from their product, interface, architecture, or engineering owner. Ordinary resolutions omit ADR status.

## Persist, Verify, Or Render

For authorized multi-target persistence:

1. refresh and preflight every routed target;
2. apply only the bounded accepted changes;
3. stop on the first write or verification failure;
4. reread every attempted and changed domain record; and
5. reconcile the actual per-target state into the Domain Delta.

Never automatically roll back verified changes, continue best-effort mutation after failure, or overwrite broadly. A partial failure returns the exact verified and failed targets, current contents relevant to recovery, owner, impact, and re-entry requirement. Semantic completion remains blocked until the inconsistent domain record is repaired.

Render follows the same representation and relationship rules but writes nothing.

## Domain Delta And Return

Every Domain Delta has a fixed core:

```text
Domain subject and source:
Decision and mutation authority:
Resolution: no-change | resolved | partial | unresolved
Persistence: complete | partial | failed | not-applicable
Persistence entries: <target>: rendered | verified | failed
Open blockers: <zero or more typed entries>
Resolved or open consequences:
Return owner:
Caller continuation authority: preserved | not supplied
```

Each blocker uses one class and names its exact condition, owner, impact, and re-entry requirement:

- `authority`;
- `evidence`;
- `contradiction`;
- `routing/setup`; or
- `persistence/verification`.

Add resolved terms, context boundaries, relationships, invariants, material conflicts, downstream consequences, changed paths and read-back, rendered changes, and ADR outcomes only when present. Conditional sections may be absent; unresolved material may not be compressed away.

`Resolution` reports semantic state. `Persistence` reports whether every in-scope persistence obligation reached its intended per-target result. A deliberate combination of verified and rendered targets may be `complete`; `partial` is reserved for an incomplete or failed obligation. A composed no-change result contains only the considered subject and source, `Resolution: no-change`, `Persistence: not-applicable`, no blockers, and the return owner.

Pass completion means every consequence and blocker is accounted for and safely returned; it does not mean the domain is resolved. A caller decides whether a returned blocker prevents its broader completion. `$grill-with-docs` cannot return Confirmed while a material nondeferred domain blocker remains.

Return caller-invoked results to the caller and composed results to `$grill-with-docs`. A standalone pass with material residual work may invoke the implicit Skill Router only after the pass is terminal, the residual is outside Domain Modeling, and no owned handoff applies. The Router returns one route or `none` and starts nothing. Domain Modeling then surfaces the recommendation and stops.

Domain Modeling completes when Trace is current; every consequence is resolved, explicitly no-change, or represented by an exact blocker; every material state change was reconciled; each authorized target is verified or returned with exact failure state; each rendered target is directly applicable; every plausible ADR branch has an outcome; mutation stayed within domain scope; the Domain Delta is complete; and Return starts no downstream work.

# Layer Three: Evidence And Rationale

## Current-To-Proposed Gap

The active five-step runtime already protects routed tracing, collision discovery, fact-versus-authority separation, lazy creation, context versus ADR authorization, domain-only mutation, read-back, and a complete delta. The future design retains that core and closes these gaps:

| Current pressure | Selected response |
| --- | --- |
| Direct resolution language can imply write authority | Require explicit persistence intent; otherwise Render |
| Domain Modeling and Grilling can both appear to own questions | Make Grilling the sole participant interviewer; route standalone terminal judgment residuals through the implicit Router |
| Reconcile also describes post-write read-back | Reserve Reconcile for semantic state and Verify for read-back |
| A scalar result conflates semantic and persistence state | Separate resolution, aggregate persistence, per-target results, and blockers |
| One blocker field cannot represent concurrent conditions | Use a small typed blocker ledger |
| Cross-context copying duplicates definitions | Use owner, reference, translation, or explicitly governed shared kernel |
| Durable invariants lack a representation | Add an optional context-owned Invariants branch |
| ADR mechanics appear in several owners | Put the complete conditional branch in `ADR-FORMAT.md` |
| Caller catalogs and staged codes dominate the synthesis | Keep provider contracts local and use one plain-language migration matrix |
| Generic evaluation protocol is repeated | Point to the Writing Great Skills evaluation owner and keep only Domain Modeling cases |

## Failure Pressure

The rewrite must resist:

- invocation for ordinary vocabulary consumption;
- code popularity silently redefining accepted meaning;
- user decision authority silently becoming write or ADR authority;
- Domain Modeling interviewing a participant or invoking its own composer;
- directories being mistaken for bounded contexts;
- false cross-context uniformity or duplicated canonical definitions;
- unnamed joint ownership behind `shared kernel`;
- generic vocabulary or implementation detail entering a glossary;
- ordinary decisions producing ceremonial ADR classifications;
- successful write commands substituting for read-back;
- rollback or continued mutation widening a partial failure;
- a short return hiding contradictions, failures, or caller identity; and
- standalone blockers bypassing the residual Router or caller-owned handoffs.

## Non-Obvious Rationale

**Participant judgment stays outside Domain Modeling.** Domain Modeling owns semantic analysis and durable records. `$grill-with-docs` owns the only composed participant interview. Direct invocation would create a cycle because the composer already contains Domain Modeling; a terminal residual through the implicit Router preserves both ownership boundaries.

**Reconciliation is event-triggered.** Exit-only reconciliation can let dependent interview branches advance past an invalidating collision. Updating after every observation is ceremonial. Material state changes are the smallest safe trigger.

**Context and ADR representation stay disclosed.** Every pass needs semantic and authority gates, but only Persist, Render, or a plausible ADR candidate needs exact representation mechanics.

**Partial state is preserved, not rolled back.** Cross-file persistence cannot be truly atomic, while automatic rollback can overwrite intervening work. Preflight, bounded writes, read-back, and exact recovery state are safer than a second mutation campaign.

**No Domain Delta file is selected.** A compact core and conditional branches fit the main runtime contract. Add another file only after observed omission persists despite a sharp inline schema.

## Deliberate Non-Changes

- Keep Domain Modeling narrowly implicit.
- Keep accepted-vocabulary consumption in repository domain routing.
- Keep Domain Modeling as the only context-record and approved-ADR writer.
- Keep Repo Bootstrap as routing-setup owner.
- Keep `$grill-with-docs` as the sole composer with Grilling.
- Keep context persistence and ADR creation independently authorized.
- Keep first domain records lazy and non-ceremonial.
- Keep unresolved meaning out of accepted records.
- Keep downstream code, plan, spec, tracker, setup, and external mutation out of scope.
- Keep installed mirrors equal to validated canonical source before promotion.

## Deferred Hypotheses

Do not promote without demonstrated control failure:

- event storming, domain storytelling, or another mandatory discovery method;
- an ontology, schema, graph database, or automatic term extractor;
- automatic code, test, or API renaming;
- automatic context inference from workspace layout;
- repository-wide vocabulary scanning on every invocation;
- a persisted Domain Delta ledger or third runtime reference;
- richer mandatory ADR templates or automatic creation;
- automatic context-relationship inference; or
- context persistence before routing setup verifies a multi-context transition.

# Layer Four: Extraction And Verification

## Proposed Runtime Semantic Surface

The future `skills/custom/domain-modeling/SKILL.md` should read approximately as:

```text
Outcome and narrow implicit admission
Durable-truth and participant-judgment boundary
Caller packet or standalone authority lock
Trace and routing pointer
Challenge -> Resolve -> Reconcile
Persist -> Verify | Render -> CONTEXT-FORMAT pointer
Conditional ADR branch -> ADR-FORMAT pointer
Compact Domain Delta
Caller, composer, or residual-Router Return
Pass completion
```

Keep universal authority, mutation scope, sequencing, pointer triggers, Return, and completion in the main file. Keep exact context-record representation in `CONTEXT-FORMAT.md`, exact ADR mechanics in `ADR-FORMAT.md`, and evidence plus migration detail here.

## Migration And Acceptance Matrix

Implement in dependency order. Rows assign owned changes and cases; they do not create runtime rules beyond Layer Two.

| Order and owner | Accepted change | Positive case | Negative control | Proof |
| --- | --- | --- | --- | --- |
| 1. Domain Modeling `SKILL.md` | Extract the narrow admission, authority lock, selected spine, participant boundary, compact delta, caller return, and completion | Settled domain persistence completes through the correct mode and return | Vocabulary consumption invokes the skill, resolve implies write, or the skill interviews the user | Structural contract plus fresh-context invocation and authority evaluation |
| 2. `CONTEXT-FORMAT.md` | Add optional invariants, explicit singular or joint relationship authority, preferred labels plus custom escape, and owner/reference/translation representation | Single-owner, translated, and governed shared-kernel examples render coherently | Definitions are copied into consumers, joint ownership is unnamed, or a false type is forced | Format examples, relationship fixtures, and changed-file read-back |
| 3. `ADR-FORMAT.md` | Own the complete conditional worthiness, approval, placement, numbering, and representation branch | One settled approved candidate records correctly while ordinary resolutions skip the branch | Domain-write authority creates an ADR or an unsettled decision is recorded | Candidate matrix, approval control, location fixture, and read-back |
| 4. Domain Modeling policy and description | Preserve explicit `allow_implicit_invocation: true` under the two narrow triggers | Durable-truth change and settled ADR recording admit | Ordinary work, future gaps, and underlying design decisions compete for invocation | Invocation-policy assertion and fresh-context routing samples |
| 5. Skill Router candidate and vocabulary | Promote the narrowly implicit terminal-residual Router, accept the complete Domain Modeling residual packet, and narrow its broad domain route to settled persistence or ADR recording while participant judgment selects `$grill-with-docs` | Standalone terminal judgment residual selects `$grill-with-docs` or another narrow owner and executes nothing | Domain Modeling invokes its composer, Router sends unsettled judgment back to Domain Modeling, or unfinished in-scope work is delegated | Router control/candidate evaluation, loop guard, relationship assertion, and policy parity |
| 6. `$grill-with-docs` | Preserve Grilling as sole question owner, relay every settled material answer, receive Domain Modeling's authoritative cumulative Domain Delta, and keep Domain Modeling blockers out of Confirmed | Domain collision returns before dependent questioning and the final delta remains intact | Composer filters domain relevance, accumulates the delta, settles meaning, reroutes a component result, or confirms with a nondeferred blocker | Multi-turn composition evaluation and packet comparison |
| 7. Composer-defined cohort, Repo Bootstrap, and relationship index | Apply the [minimum coordinated experimental cohort](grill-with-docs.md#runtime-ownership-and-change-map); pass compatible packets, preserve known handoffs, sequence routing setup before multi-context persistence, and index only accepted edges. Verify Repo Bootstrap and recommendation-only or suggestion-only owners without generating unrelated candidates unless an observed mismatch requires an owned change | Cohort caller, residual-Router, and setup boundaries remain intact | Caller catalogs are copied locally, verification-only owners are regenerated speculatively, or Domain Modeling mutates setup | Active-surface relationship audit and setup fixture |
| 8. `CONTEXT.md` vocabulary | During coordinated promotion, persist Source fact, Domain truth, Domain record, and Ubiquitous language without overwriting intervening Active/Experimental skill vocabulary | Active vocabulary matches the promoted behavior | Future candidate language is published before coordinated promotion or current unrelated terms are lost | Domain read-back and vocabulary-owner audit |
| 9. Tests and Domain Modeling evaluations | Protect ownership, pointers, policy, return shape, negative controls, and integrated composer/Router cases | Structural and behavioral claims each have proportionate proof | Static strings are reported as semantic or mutation proof | Focused pytest, behavioral evaluation records, and residual-gap review |
| 10. Canonical validation and mirrors | Validate the complete coordinated candidate, then synchronize all in-scope installed mirrors | Canonical source, callers, setup, tests, and installed hashes agree | Partial promotion or mirror drift leaves incompatible authority | Full pytest, `scripts.validate_skills`, install preview/sync, diff checks, read-back, and hash parity |

## Domain-Specific Behavioral Evaluation

Use [`writing-great-skills/BEHAVIOR-EVALS.md`](../../../skills/custom/writing-great-skills/BEHAVIOR-EVALS.md) as the sole generic protocol. Demonstrate a realistic control failure before adding guidance; keep runtime, settings, tools, repository fixtures, authority, and rubric fixed; use at least five fresh samples per arm for each behavioral claim; and inspect every flagged result.

Domain Modeling-specific scenarios must cover:

- settled persistence versus unsettled participant judgment;
- direct, caller, and composed authority locks;
- single- and multi-context routing, including setup-first transition;
- all five Challenge lenses;
- normative intent versus descriptive implementation fact;
- owner, reference, translation, joint governance, and custom relationship type;
- Render, verified persistence, deliberate verified-plus-rendered completion, and injected partial failure;
- plausible ADR candidate versus ordinary resolution;
- compact resolved, partial, unresolved, and no-change deltas;
- concurrent blocker classes;
- caller return, composer collision return, and standalone terminal residual routing; and
- mutation and downstream non-execution boundaries.

Critical failures are invented settlement, wrong-context persistence, unauthorized context or ADR creation, a participant interview owned by Domain Modeling, recursive composer invocation, missing relationship authority, hidden implementation contradiction, omitted blocker, false verification, automatic rollback, hidden partial state, incomplete delta, caller-identity loss, or downstream execution.

Several claims may share one fixed scenario and sample set when the rubric scores each claim independently. Structural tests protect literals and relationships only; they do not replace behavioral or filesystem proof.

## Promotion Gate

Promote only the coordinated candidate. The record must identify every promoted behavior claim, its Layer Two owner, source changes, fixed scenario and repository state, control and candidate hashes, runtime, sample count, rubric, result distribution, worst outcome, critical failures, protocol deviations, unavailable telemetry, and residual gaps.

Promotion requires:

- one runtime owner for every admitted behavior, representation branch, relationship, and completion gate;
- the implicit Router and Domain Modeling residual edge promoted together;
- `$grill-with-docs`, callers, setup routing, and the relationship index compatible with the new packet and return contracts;
- context and ADR formats matching their selected ownership;
- all positive and negative cases passing with no critical regression;
- canonical tests, full validation, setup validation, diff checks, and changed-file read-back passing;
- the rendered `CONTEXT.md` vocabulary reconciled with intervening active/experimental work; and
- installed Domain Modeling, both disclosed references, Router, and every in-scope caller mirror matching validated canonical source.

A residual gap blocks promotion when it affects invocation, semantic or participant authority, routing, context ownership, relationship completeness, mutation authority, ADR approval, read-back truth, partial-state recovery, blocker accounting, Domain Delta completeness, caller return, Router loop safety, composer compatibility, or installed parity. Noncritical uncertainty may remain only with its evidence limit, behavioral consequence, and later validation owner.
