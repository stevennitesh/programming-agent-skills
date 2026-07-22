# Domain Modeling Durable-Truth Synthesis

Status: Prompt 5 complete. The accepted Domain Modeling package is canonical and globally installed; no experimental lifecycle entry remains.

Before Prompt 3, the canonical and experimental Domain Modeling packages were byte-identical. Prompt 3 replaced the stale lifecycle copy; Prompt 4 repaired direct-user meaning authority and false Context Mapping labels, froze pre-prune package `cfea0f22106e4a8ec231912afadd09ca717189dcb4b53eadb6ec19bdde44c6e0`, and accepted pruned candidate `88413f471ffcedccdf8b4b3a162a3068334c7befbcd28801165add6d29e8941b`. Prompt 5 promoted those exact bytes to `skills/custom/domain-modeling/`; accepted behavioral evidence was reused because no candidate byte or claim changed.

This synthesis has four roles:

1. **Baseline** identifies the smallest credible control.
2. **Normative Design** owns the selected future behavior.
3. **Admission And Decision Ledgers** preserve why each delta exists.
4. **Extraction And Proof** makes Prompt 3 mechanical without claiming behavioral proof.

## Baseline

The design control is Matt Pocock's checked-out `domain-modeling` package at `ed37663cc5fbef691ddfecd080dff42f7e7e350d`, inspected clean on 2026-07-21. Its smallest credible core is:

- change the domain model rather than merely consume vocabulary;
- challenge glossary conflicts and fuzzy language;
- use concrete scenarios to sharpen relationships and boundaries;
- cross-check descriptive claims against code;
- create domain records lazily;
- persist resolved ubiquitous language; and
- offer concise ADRs only for durable, surprising, real trade-offs.

The checked-out Superpowers baseline at `d884ae04edebef577e82ff7c4e143debd0bbec99` and Ponytail baseline at `16f29800fd2681bdf24f3eb4ccffe38be3baec6b` were clean and contained no matching or equivalent package. Freshness is limited to these local checkouts; no network refresh was performed.

The upstream package is a design control, not local runtime authority. Local additions must cure a demonstrated baseline failure, satisfy an accepted caller contract, or preserve a non-intuitive safety boundary.

# Normative Design

## Outcome And Admission

Domain Modeling keeps a project's context-scoped ubiquitous language, invariants, bounded contexts, relationships, and approved durable decisions coherent.

Keep it narrowly implicitly invocable when:

1. domain meaning, an invariant, a context boundary, or a context relationship must be clarified, changed, rendered, or persisted; or
2. an already-settled decision needs ADR assessment or explicitly approved recording.

Ordinary vocabulary lookup follows repository domain routing and does not invoke the skill. Generic planning, interface design, implementation, and non-domain decision settlement remain with their owners.

Use the leading instruction **Model, don't catalog**. Capture meaning, behavior, invariants, responsibility, and relationships; omit generic technical vocabulary, implementation indexes, and structure that exists only because of the current code layout.

## Minimum Runtime

```text
Trace -> Challenge -> Resolve -> (Persist -> Verify | Render) -> Return
```

### Trace

Establish the bounded subject, relevant domain records, load-bearing evidence, domain authority, mutation authority, ADR authority, caller, and return owner.

Follow the repository's configured domain-document route first. When no convention exists, use root `CONTEXT-MAP.md` for an existing multi-context model and root `CONTEXT.md` as the local fallback. These filenames are fallbacks, not universal DDD requirements. Create no empty record; create the first record only for an authorized settled resolution.

Treat code, tests, contracts, runtime behavior, and widespread usage as evidence about current implementation, not automatic authority over intended domain meaning. Bounded contexts follow model, language, responsibility, and consistency boundaries rather than directory, package, service, or repository size alone.

Direct use may ask focused domain-expert questions needed to resolve terms, invariants, boundaries, and relationships. Under `$grill-with-docs`, Grilling owns all questioning and Domain Modeling receives settled material answers. A caller-invoked pass returns unresolved choices to its caller.

### Challenge

Test only material uncertainty through three checks:

- **Language collisions:** overloaded terms, accidental synonyms, and implementation language leaking into the domain model.
- **Model boundaries:** unclear responsibility, invariant ownership, relationship contract, language ownership, or change authority.
- **Contradictions:** accepted records, evidence, participant decisions, and current implementation disagree.

Use normal, edge, failure, inclusion, and exclusion scenarios only when they can change the model. Finish with each material collision resolved or represented by an exact blocker and owner.

### Resolve

Settle the canonical term or decision, implementation-independent meaning, owning context, load-bearing sources, and decision authority. Add aliases, invariants, boundaries, relationships, conflicts, and consequences only when material.

Evidence settles source facts. The direct user unless a source names another authority, or the caller's named domain authority, settles intended meaning. When intended truth and implementation differ, preserve the accepted truth, expose the contradiction, and return alignment work to its owner. Keep unresolved meaning out of durable domain records.

For context relationships, always record interaction direction, responsibility, contract, language ownership, and change authority. Apply a recognized DDD Context Mapping pattern only when it accurately describes the relationship. The context-format reference owns Partnership, Shared Kernel, Customer/Supplier Development, Conformist, Anticorruption Layer, Open-host Service, Published Language, Separate Ways, and Big Ball of Mud as optional recognized patterns. Never force a pattern or use `translation` as though it were itself a standard relationship pattern.

### Persist, Verify, Or Render

Lock context and ADR mutation separately:

- `persist authorized` requires an explicit persistence request or exact caller mode and permits only routed domain-record changes;
- otherwise use `render only` and return directly applicable wording, target, placement, and relationship effects; and
- ADR creation requires separate explicit approval for one identified candidate.

Read `CONTEXT-FORMAT.md` only when rendering or persisting language, invariants, context maps, or relationships. Read `ADR-FORMAT.md` only for a plausible already-settled ADR candidate.

Domain Modeling remains the repository's single recorder for approved ADRs, including non-domain engineering decisions. The originating product, domain, interface, architecture, or engineering workflow owns settlement; the disclosed ADR branch owns only worthiness assessment, explicit approval, representation, persistence, and verification.

For authorized persistence, refresh routing and every target, preflight the bounded set, write only accepted changes, and reread each attempted and changed record. On the first write or verification failure, preserve verified changes, stop further mutation, and return exact partial state. Do not automatically roll back or continue best-effort writes.

Repository setup remains owned by `$repo-bootstrap`. When a managed domain-routing surface must change, Domain Modeling returns the accepted topology and exact setup requirement to the user or caller and stops. Persistence may resume only in a later invocation after setup read-back agrees.

### Return

Return the complete Domain Delta to the direct user, caller, or `$grill-with-docs` and stop. Domain Modeling is a leaf: it never invokes Skill Router, its composer, or downstream execution.

Every Domain Delta has four common fields:

```text
Semantic outcome: no-change | resolved | partial | unresolved
Persistence outcome: complete | partial | failed | not-applicable
Blockers and consequences:
Return owner:
```

Add authority, resolved language, context boundaries, invariants, relationships, per-target rendered or verified state, caller identifiers, ADR outcomes, and continuation authority only when present or required by the caller. Each blocker names its condition, owner, impact, and re-entry requirement. A no-change result stays minimal.

Under `$grill-with-docs`, accept every settled material answer, including one with no durable consequence. Update and return the authoritative cumulative Domain Delta before dependent questioning continues; return collisions or blockers without deciding interview materiality or branching. This is a disclosed composer contract, not a universal `Reconcile` stage.

## Completion

Complete when Trace is current; every in-scope consequence is resolved, explicitly no-change, or represented by an exact blocker; each intended target is verified, rendered, or returned with exact failure state; every plausible ADR candidate has an outcome; mutation stayed inside routed domain records and approved ADRs; the Domain Delta is complete; and Return starts no downstream work.

# Admission And Decision Ledgers

## Mechanism-Admission Ledger

| Mechanism beyond baseline | Baseline failure or required contract | Owner | Cheaper alternative considered | Load | Admission |
| --- | --- | --- | --- | --- | --- |
| Narrow implicit trigger and lookup exclusion | Passive vocabulary consumption otherwise competes with active modeling | Description and admission | Make explicit-only | Permanent description load | admit |
| Source fact versus intended meaning | Popular code can silently redefine accepted domain truth | Trace and Resolve | Treat code as authority | Small semantic distinction | admit |
| Context-scoped invariants and relationships | Glossary-only records omit load-bearing DDD model boundaries | Resolve and `CONTEXT-FORMAT.md` | Glossary only | Conditional representation | admit |
| Repository routing first, filename fallback | Mandatory local filenames do not fit every repository | Trace; setup owned by Repo Bootstrap | Always require `CONTEXT.md` | Small routing branch | admit |
| Direct focused domain questioning | The baseline's core clarification work cannot proceed from unsettled expert meaning | Direct Domain Modeling | Always require the composer | Small direct branch | admit |
| Composed Grilling ownership | Two interview owners create branching and confirmation conflicts | `$grill-with-docs` and Grilling | Let Domain Modeling ask inside composition | Conditional caller contract | caller-owned |
| Explicit persist versus render | Resolution language otherwise implies write authority | Persistence gate | Always write resolved truth | Small universal authority gate | admit |
| Separate ADR approval | Domain persistence authority otherwise creates unrelated ADRs | `ADR-FORMAT.md` | One combined write grant | Conditional safety gate | admit |
| Universal ADR recorder | ADR-0006 and callers require one mutation owner without transferring decision authority | Disclosed ADR branch | Each workflow writes its own ADR | Conditional branch and maintenance | disclose |
| Read-back and bounded partial failure | Successful commands do not prove persisted truth; rollback can overwrite intervening work | Persistence branch | Best-effort writes or automatic rollback | Conditional failure procedure | disclose |
| Four-field Domain Delta with conditional detail | Callers need semantic, persistence, blocker, and return state without a universal forensic wrapper | Return | Fixed nine-field schema | Small common schema | admit |
| Cumulative composed Domain Delta | Exit-only capture can lose collisions before dependent questioning | Disclosed composer branch | Rebuild at exit | Conditional caller load | disclose |
| Mandatory five Challenge lenses | Three plain checks express the same DDD pressure | none | Retain invented lens names | Common-path steering | reject |
| Universal `Reconcile` stage | Ordinary reconciliation already occurs in Resolve, Verify, and Return | none | Keep seven-word spine | Common-path step | reject |
| Domain Modeling to Skill Router residual edge | Adds no domain capability and couples promotion to routing machinery | none | Return residual and stop | Cross-skill and proof load | reject |
| Mandatory partial relationship taxonomy | False labels create worse models than explicit semantics | `CONTEXT-FORMAT.md` | Four preferred labels plus custom | Representation and correctness risk | reject |
| Ontology, automatic extraction, automatic renaming, mandatory event storming | No demonstrated baseline failure | none | Add speculative method or tooling | High runtime and maintenance load | defer |

## Confirmed Prompt 1 Decisions

1. Use Matt Pocock's package as the simplest credible baseline.
2. Keep universal ADR recording only as a disclosed branch; decision authority remains upstream.
3. Reduce the Domain Delta to four common fields plus conditional detail.
4. Require semantic relationship facts and use DDD pattern names only when accurate.
5. Remove `Reconcile` from the universal runtime spine.
6. Collapse five invented Challenge lenses into three plain DDD checks.
7. Remove direct Skill Router invocation and make Domain Modeling a leaf.
8. Permit focused domain-expert questions on direct invocation; preserve Grilling ownership under composition.
9. Follow repository routing first and use local filenames only as fallback conventions.

## Six-Category Coverage

| Category | Closed decision | Residual evidence limit |
| --- | --- | --- |
| Ambiguity | Separate source facts, intended meaning, mutation modes, relationship semantics, and direct versus composed questioning | Behavioral reliability unproved |
| Ownership | Domain authority settles meaning; Domain Modeling records domain truth and approved ADRs; Grilling owns composed questioning; Repo Bootstrap owns managed routing; callers own continuation | Caller compatibility needs Prompt 4 proof |
| Simplification | Baseline-first five-stage runtime, four-field common return, three Challenge checks | Exact wording remains Prompt 3 work |
| Navigation | Common path inline; context, ADR, composition, and persistence-failure mechanics disclosed at their branch owners | Pointer-following behavior unproved |
| Leading words | Keep Model, Trace, Challenge, Resolve, Persist, Verify, Render, and Return; remove Reconcile as a separate stage | Invocation and steering effects unproved |
| Unnecessary complexity | Reject Router coupling, fixed universal filenames, mandatory partial taxonomy, forensic return fields, and speculative DDD machinery | Aggregate candidate load must be rechecked in Prompt 4 |

## Deliberate Non-Changes

- Keep Domain Modeling narrowly implicit.
- Keep accepted-vocabulary consumption in repository routing.
- Keep context persistence and ADR creation independently authorized.
- Keep first domain records lazy and non-ceremonial.
- Keep unresolved meaning out of durable records.
- Keep code, plan, spec, tracker, setup, and implementation mutation out of scope.
- Keep the composer transport-only: Grilling asks; Domain Modeling models and returns its delta.
- Keep installed mirrors outside synthesis authoring and promotion.

## Historical Evidence And Limits

The existing canonical package, structural tests, relationship index, ADR-0006, domain-routing guide, and prior workflow fixtures establish current ownership and safety pressure. They do not prove that the proposed wording improves invocation, judgment, context loading, mutation behavior, Return, or completion.

The prior experimental copy has no valid treatment/control contrast because it is byte-identical to canonical. Treat its manifest description as lifecycle drift, not behavioral evidence. Prompt 3 must create a new hash-identified candidate; Prompt 4 must select realistic controls, prove control failures before crediting added guidance, and evaluate pruning equivalence from an admitted pre-prune snapshot.

# Extraction And Proof

## Prompt 3 Semantic Surface

Prompt 3 should build a new experimental package from this order:

```text
Narrow implicit description
Outcome and Model leading instruction
Meaning, context-mutation, and ADR authority
Trace -> Challenge -> Resolve -> (Persist -> Verify | Render) -> Return
Four-field Domain Delta with conditional additions
Direct versus composed questioning branch
Completion
```

Keep universal authority, mutation scope, sequence, pointer triggers, Return, and completion in `SKILL.md`. Keep exact context representation and the optional recognized Context Mapping patterns—Partnership, Shared Kernel, Customer/Supplier Development, Conformist, Anticorruption Layer, Open-host Service, Published Language, Separate Ways, and Big Ball of Mud—in `CONTEXT-FORMAT.md`. Keep ADR worthiness, approval, placement, numbering, record form, and verification in `ADR-FORMAT.md`.

## Prompt 3 Classification Matrix

| Surface or behavior | Classification | Destination | Admission basis |
| --- | --- | --- | --- |
| Upstream challenge, scenarios, code cross-check, lazy records | Baseline | `SKILL.md` | Simplest credible control |
| Narrow trigger and lookup exclusion | Add | description | Invocation collision |
| Fact versus meaning authority | Add | `SKILL.md` | Semantic safety |
| Direct focused questions | Add | `SKILL.md` | Core DDD clarification |
| Render versus persist and read-back | Add | `SKILL.md` plus conditional format pointer | Mutation safety |
| Context-scoped invariants and relationship semantics | Add | `CONTEXT-FORMAT.md` | DDD completeness |
| Universal ADR recording mechanics | Disclose | `ADR-FORMAT.md` | ADR-0006 caller contract |
| Composed cumulative delta | Disclose | sharp branch in `SKILL.md`; composer procedure stays foreign | Required caller contract |
| Setup mutation | Caller-owned | `$repo-bootstrap` | Existing owner |
| Non-domain decision settlement and downstream execution | Caller-owned | originating workflow | Authority boundary |
| Prompt 1 rationale, ledgers, baseline hashes, migration state | Non-runtime | this synthesis | Evidence only |
| Reconcile step, five named lenses, Router edge, fixed nine-field return | Rejected | none | Confirmed simplification |
| Mandatory methods and automatic tooling | Deferred | none | No demonstrated failure |

## Prompt 3 Extraction Result

Complete. Prompt 3 classified every proposed behavior without inventing a decision and:

- replaced rather than blessed the stale byte-identical experimental copy;
- used the confirmed baseline and classifications above;
- updated the experimental manifest to the new package identity and truthful baseline;
- preserved the already-reconciled direct-question and leaf Return relationships;
- recorded pruning decisions for every instruction-bearing unit in `docs/validation/transcripts/2026-07-21-domain-modeling-extraction-pruning-evidence.md`; and
- stopped before behavioral evaluation, promotion, installation, or Git delivery.

## Prompt 4 Proof Obligations

Behavioral evaluation must cover:

- invocation for domain clarification or durable capture versus ordinary lookup;
- direct focused questioning versus composed Grilling ownership;
- source fact versus intended domain truth;
- repository-specific routing and fallback behavior;
- language, boundary, and contradiction challenges;
- accurate relationship semantics and optional Context Mapping patterns;
- render, verified persistence, and injected partial failure;
- plausible ADR assessment versus unauthorized creation;
- minimal no-change, resolved, partial, and unresolved deltas;
- cumulative composer collision ordering; and
- leaf Return with no Router or downstream execution.

Critical failures are invented settlement, false DDD pattern labels, directory-derived bounded contexts, unauthorized persistence or ADR creation, missing relationship authority, hidden implementation contradiction, false verification, automatic rollback, omitted partial state or blocker, caller-identity loss, Domain Modeling taking over composed questioning, Router invocation, or downstream execution.

Prompt 4 is complete. Claim-matched controls exposed failures in settled-ADR routing, persistence verification, Context Mapping accuracy, partial-failure Return, composed question ownership, and leaf completion. An initial candidate wave passed every case except Context Mapping: three of five samples invented Conformist, and one also invented Open-host Service. A narrow reference repair produced 5/5 accurate pattern choices on a fresh affected-arm rerun. The repaired pre-prune and final packages both returned the same pruned completion behavior at 5/5. Full results, deviations, and residual gaps are recorded in `docs/validation/transcripts/2026-07-21-domain-modeling-post-candidate-behavior-eval.md`.

## Prompt 5 Promotion Result

Complete. Prompt 5 promoted accepted hash `88413f471ffcedccdf8b4b3a162a3068334c7befbcd28801165add6d29e8941b` byte-for-byte to `skills/custom/domain-modeling/`, reused the unchanged Prompt 4 behavioral evidence, and proved the canonical package before lifecycle cleanup. The relationship index already represented the selected invocation and ownership edges, so it required no change.

The Domain Modeling experimental directory and only its manifest entry were removed. The managed installer then synchronized the canonical package to `C:\Users\steve\.agents\skills\domain-modeling`. A concurrent global-bootstrap change triggered the transactional guard; the supported `--skip-global-agents` path preserved that unrelated file and installed the skill pack. Canonical and installed Domain Modeling hashes match, the post-install dry run reports all managed skills unchanged, and complete proof is recorded in `docs/validation/transcripts/2026-07-22-domain-modeling-promotion-install-evidence.md`.
