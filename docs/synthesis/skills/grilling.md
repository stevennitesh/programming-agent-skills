# Grilling Runtime Design Synthesis

Status: Deploy Prompt 5 complete. Canonical and installed Grilling are byte-identical at tree hash `5c6ab5e504123fdaa79db33fc436f361e8e9383bf028892970a9efee4b54cf63`, and Grilling's experimental package and manifest entry are removed. Canonical Grilling is executable authority; this document authorizes no downstream execution by itself.

Executable authority is `skills/custom/grilling/SKILL.md` and `skills/custom/grilling/agents/openai.yaml`. `C:\Users\steve\.agents\skills\grilling` is the verified managed distribution copy, never independent authority. The accepted evaluation fixture remains under `docs/validation/evals/grilling-pruning-pre-prune/` as evidence, not runtime.

## Design Verdict

Rebuild the experimental candidate from Matt Pocock's small Grilling primitive, then admit only the local mechanisms needed for bounded questioning, composition, recoverable gaps, and caller return. Grilling remains one implicitly invocable, conversation-only skill whose purpose is to grill until shared understanding is explicitly confirmed. It writes nothing, invokes no evidence owner, chooses no downstream route, and starts no work.

The simplest credible baseline is the complete upstream package at Matt Pocock checkout `ed37663cc5fbef691ddfecd080dff42f7e7e350d`:

- `.tmp/mattpocock-skills/skills/productivity/grilling/SKILL.md`
- `.tmp/mattpocock-skills/skills/productivity/grilling/agents/openai.yaml`

The minimum viable runtime is the baseline behavior plus six admitted deltas: bounded materiality, a conditional caller seam, composed Relay, semantic progress, typed evidence gaps, and a status-discriminated Return. The explicit no-execution boundary is preserved from upstream and sharpened for composition. No supporting runtime file is justified.

## Baseline Comparison

All observations below are from the local ignored checkouts. Each checkout was clean when inspected; commit date records local checkout freshness, not a network freshness guarantee.

| Candidate | Local revision and observed date | Relevant package | Disposition |
| --- | --- | --- | --- |
| Matt Pocock | `ed37663cc5fbef691ddfecd080dff42f7e7e350d`, 2026-07-21; `HEAD`, `origin/main`, and `origin/HEAD` aligned | `skills/productivity/grilling/` | **Selected baseline.** It supplies relentless branch-by-branch interviewing, one question at a time, recommendations for decisions, factual inspection, human-owned decisions, explicit confirmation, and no action before confirmation. |
| Superpowers | `d884ae04edebef577e82ff7c4e143debd0bbec99`, 2026-07-02; `HEAD`, `origin/main`, and `origin/HEAD` aligned; tag `v6.1.1` | No Grilling package. Closest analogue: `skills/brainstorming/SKILL.md` | Adjacent evidence only. It supports context inspection, one-question turns, recommendations with tradeoffs, approval, and YAGNI. Reject its mandatory design sections, design-doc write and commit, visual companion, user spec review, and automatic transition to `writing-plans`; those violate Grilling's bounded conversation-only purpose. |
| Ponytail | `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`, 2026-07-15; `HEAD`, `origin/main`, and `origin/HEAD` aligned | No Grilling package or behaviorally equivalent interview skill. Closest relevant package: `skills/ponytail/SKILL.md` | Simplification pressure only. Its minimum-solution ladder supports pruning, but its code-first persistence, execution posture, and coding-only scope are not Grilling behavior. No runtime clause is imported. |
| Current local canonical | `skills/custom/grilling/SKILL.md`; identical current experimental body at inspection | Promoted seven-stage local design | Evidence for local composition and recovery needs, not the selected text baseline. It over-specifies authority roles, attribution, history, stages, and clarification count relative to the confirmed minimum. It remains runtime authority until later promotion. |

Matt Pocock's `.out-of-scope/question-limits.md` also rejects a numeric question cap: difficulty determines interview length, natural-language steering is the control surface, and redundant questions are a prompt-quality failure rather than a quantity failure. The accepted design therefore uses semantic progress, not a counter.

## Normative Design

This section is the sole normative authority for Prompt 3. Later rationale and proof sections may explain or test it, but may not add runtime behavior.

### Outcome And Boundary

Grilling achieves shared understanding of one bounded plan, design, decision, or idea and leaves it unexecuted. It may inspect available evidence read-only. It asks only material questions, one at a time, and gives one recommended answer with the decisive tradeoff for each decision. Participant-held facts are asked neutrally.

Direct use defaults decision ownership, confirmation, and return to the user. A caller may instead supply the subject, authority, identifiers, and return owner. Grilling preserves those fields without taking caller continuation authority.

Grilling owns the interview, materiality, confirmation gate, gap classification, and its exit packet. It does not own domain consequences, evidence work, durable capture, routing, planning, specification, tickets, implementation, tracker state, Git state, or external state.

### Minimum Viable Runtime

Prompt 3 must extract this semantic contract into `skills/experimental/grilling/SKILL.md`. It may tighten incidental wording only when every clause, leading word, owner, branch, and returned field remains behaviorally equivalent.

```md
---
name: grilling
description: Grill the user relentlessly about a bounded plan, decision, or idea until shared understanding is confirmed. Use when the user wants to stress-test their thinking or uses a "grill" trigger phrase. Conversation-only and before action.
---

# Grilling

Interview relentlessly until shared understanding is confirmed. Grilling writes nothing and starts nothing downstream.

**Bound.** Use caller-supplied subject, authority, identifiers, and return owner; otherwise the user owns decisions, scope changes, confirmation, and return. Ask only material choices whose plausible answers change the outcome or commitment boundary, another material dependency, or a stated human-judgment consequence.

**Grill.** Find inspectable facts instead of asking. Put decisions to their owner one at a time, with one recommendation and decisive tradeoff; ask participant-held facts neutrally. Follow dependency order, incorporate each answer and deferral, and reopen invalidated decisions. Continue while clarification advances or corrects a branch; a repeated non-answer makes that decision authority unavailable.

Under composition, **Relay** every settled material answer and pause dependent progress until any domain collision or blocker returns. Grilling owns materiality, not domain consequences.

**Confirm.** Present the decisions, deferrals, and evidence limits. Continue until confirmation authority explicitly accepts shared understanding. Confirmation starts nothing.

**Gap.** When required branches remain and neither evidence nor available authority can advance them, return `Evidence gap` with kind `evidence` or `decision authority`, missing input, impact, and exactly one uninvoked owner. Choose `$research` for an authoritative source, `$prototype` for runnable design evidence, `$diagnosing-bugs` for causal or reproduction uncertainty, `$to-questionnaire` for an external stakeholder, `$handoff` for cross-session continuation, and the caller or `none` otherwise.

**Return.** Always return status, bound, confirmed decisions, return owner, and `Downstream execution: none`. Add caller identifiers when supplied. For `Evidence gap`, add kind, missing input, impact, and uninvoked owner. Return to the caller or user and stop.
```

Keep `policy.allow_implicit_invocation: true` in `skills/experimental/grilling/agents/openai.yaml`.

### Mechanism Admission Ledger

| Mechanism | Pressure and evidence | Cheapest sufficient form | Runtime destination | Proof owner |
| --- | --- | --- | --- | --- |
| Bounded materiality | Upstream's open-ended interview can become redundant or expand into adjacent choices; the out-of-scope note rejects a hard count | One consequence predicate tied to outcome, commitment boundary, dependency, or stated human judgment | `Bound`, inline and universal | Prompt 4 multi-turn behavior evaluation |
| Conditional caller seam | Grill With Docs and its named callers must preserve subject, authority, identifiers, and return ownership; direct use should stay simple | One caller-override sentence with user defaults | `Bound`, inline and universal | Prompt 4 direct/composed contrast |
| Composed Relay | Grill With Docs must pass every settled material answer to Domain Modeling and return collisions before dependent questioning | One conditional paragraph; no generic packet schema | `Relay`, inline but branch-only | Prompt 4 ordered composition case; Grill With Docs owns transport proof |
| Semantic progress | A fixed question cap truncates hard interviews, while unlimited paraphrase does not advance understanding | Continue only while clarification advances or corrects a branch; repeated non-answers make that authority unavailable | `Grill`, inline and universal | Prompt 4 redundant-question negative control |
| Typed evidence gap | A blocked interview needs a recoverable next owner without silently invoking work | Two gap kinds, missing input, impact, and one category-mapped uninvoked owner | `Gap`, inline and conditional | Prompt 4 owner-selection cases; each named skill owns any later work |
| Status-discriminated Return | Direct and composed callers need a small stable result without a forensic transcript | Common fields always; gap fields only for `Evidence gap`; preserve supplied identifiers | `Return`, inline and universal | Prompt 4 packet and caller-return cases |
| Explicit no-execution boundary | Upstream confirmation gate prevents premature action; composition must not turn confirmation into continuation authority | Opening guard, Confirm guard, and returned `Downstream execution: none` | Opening, `Confirm`, and `Return` | Prompt 4 withheld-confirmation and no-action cases |

Every admitted delta has a behavioral reason, a smaller rejected alternative, one destination, and a later proof owner. No mechanism may enter another runtime surface by implication.

### Placement And Ownership Classification

| Behavior or information | Classification | Destination or owner |
| --- | --- | --- |
| Relentless branch-by-branch interview, dependency order, one question at a time, factual inspection, human-owned decisions, explicit confirmation | Baseline behavior | Inline in experimental `SKILL.md` |
| Bounded materiality, semantic progress, confirmation summary, typed Gap, recoverable Return, no-execution guard | Grilling-owned admitted behavior | Inline in experimental `SKILL.md` |
| Subject, authority, caller identifiers, return owner, and any continuation after Return | Caller-owned input and behavior | Caller supplies and receives; Grilling preserves only |
| Transport of settled answers and returned collisions | Composer-owned transport with callee-owned pause/integration obligation | Grill With Docs owns transport; Grilling's conditional `Relay` owns its pause and response |
| Domain-consequence classification, Domain Delta, persistence, and ADR work | Domain Modeling-owned behavior | Outside Grilling runtime |
| Research, prototype, diagnosis, questionnaire, handoff, or caller recovery work | Named owner behavior, uninvoked by Grilling | Outside Grilling runtime; Gap names one owner only |
| Display name, short description, and implicit-invocation policy | Platform adaptation | Experimental `agents/openai.yaml`: upstream interface values plus repository policy |
| Baseline comparison, admission rationale, rejected machinery, migration state, proof method | Non-runtime evidence | This synthesis and later evaluation records |
| Supporting reference, durable interview state, question counter, confidence score, route catalog | Rejected or deferred machinery | No destination |

### Relationship Ownership

The accepted executable edges do not change:

| Source | Relationship | Target | Boundary |
| --- | --- | --- | --- |
| Direct user | Invoke | `$grilling` | Grill one bounded subject, return the packet, and stop |
| `$skill-router` | Recommend and stop | `$grilling` | The user starts the conversation-only interview later |
| `$grill-with-docs` | Compose | `$grilling` | Preserve Grilling's complete interview contract, Relay each settled answer, receive its packet, and own the combined return |
| `$to-questionnaire` or `$research` | Recommend and stop | `$grilling` | The current user owns the remaining decision |
| `$grilling` | Name uninvoked owner | `$research`, `$prototype`, `$diagnosing-bugs`, `$to-questionnaire`, or `$handoff` | Identify one blocked recovery owner without invoking it |

Grilling owns materiality, not domain consequence. Grill With Docs remains the sole composer of Grilling with Domain Modeling. Domain Modeling alone owns durable domain truth. Evidence owners act only after a separately authorized invocation. The relationship index already expresses these edges and therefore needs no Prompt 2 edit.

## Rejected, Deferred, And Residual Complexity

### Rejected From Runtime

- The `cited | participant-supplied | inferred` attribution taxonomy. Ordinary evidence discipline is sufficient; Grilling only needs to present evidence limits at confirmation.
- Four separately named authority roles on every direct invocation. The caller override plus user defaults preserves ownership without making direct use ceremonial.
- The seven-stage `Bound -> Find -> Grill -> Integrate -> Confirm | Gap -> Return` spine. `Find` and `Integrate` are ordinary interview work inside `Grill`; keeping them as peer stages adds navigation without a distinct user-facing gate.
- A hard one-clarification allowance or numeric question budget. Progress is semantic, and the upstream out-of-scope decision rejects counters.
- Material rejected-option history and a supersession ledger. Confirmed decisions, current deferrals, and evidence limits are enough for shared understanding and caller recovery.
- Agreement on a downstream route before confirmation. Shared understanding and route selection are different decisions.
- A supporting reference, universal packet schema, operations manual, durable interview state, confidence score, or caller catalog.
- Automatic evidence-owner invocation, automatic continuation, or any action after confirmation.
- Superpowers' design-document write, commit, review, visual-companion, and `writing-plans` transition behaviors.
- Ponytail's persistent coding mode, code-first output, and execution posture.

### Deferred Hypotheses

- Add a support file only if repeated fresh-context behavior evidence shows one conditional branch cannot remain reliable after inline tightening.
- Add a new Gap owner only after a real blocked case demonstrates a distinct owner with an accepted relationship edge and proof plan.
- Expand caller fields only after a caller cannot preserve identity or recover the result through the current seam.
- Add more progress machinery only after a fixed control proves repeated non-progress that the present semantic rule does not correct.

### Residual Unavoidable Complexity

Only three local complexities remain beyond upstream: composed Relay ordering, typed recovery ownership, and a caller-recoverable Return. They are unavoidable because existing callers require collision-safe composition and blocked sessions must stop without losing ownership. Everything else stays in ordinary model capability, caller contracts, relationship documentation, or proof records.

## Source Trace And Domain Delta

The design reconciles the complete selected Matt Pocock package and question-limit note; Superpowers' complete Brainstorming package; Ponytail's complete core package; the current canonical and experimental Grilling packages; Grilling's OpenAI policy; Grill With Docs and Domain Modeling synthesis; the pack relationship index; the experimental manifest; current structural tests and evaluation ownership; `docs/synthesis/README.md`; and ADRs 0003, 0004, 0005, and 0007.

The Domain Delta is `no-change`. The accepted terms are local skill-contract vocabulary and do not alter repository-wide ubiquitous language, bounded-context responsibility, or an ADR-worthy architectural decision.

## Reconciliation With Current Surfaces

The current canonical and experimental Grilling bodies were identical at inspection. They encode the older detailed design and remain untouched by Prompt 2. Their presence does not override this accepted next design:

- canonical remains current runtime authority until a later promotion;
- experimental is stale and is the only runtime package Prompt 3 may replace;
- the experimental manifest's existing origin record must be refreshed by Prompt 3 to describe the new candidate provenance and lifecycle;
- Grill With Docs, Domain Modeling, and the relationship index keep their current edges because the new packet preserves their required subject, identifiers, Relay pause, terminal status, and return owner; and
- the existing Grilling evaluation prose is historical evidence, not proof of the new minimum runtime. Prompt 4 must create fresh control/candidate evidence.

No competing synthesis paragraph, table, historical note, or current runtime may be read as permission to reintroduce a rejected mechanism into the Prompt 3 candidate.

## Prompt 3 Extraction Contract

Prompt 3 is ready to execute with no design choice left open.

### Exact Baseline

Read the complete Matt Pocock Grilling package at checkout `ed37663cc5fbef691ddfecd080dff42f7e7e350d`. Treat its `SKILL.md` behavior as Add-preserving baseline material, then apply only the admitted deltas in this synthesis. Superpowers, Ponytail, and current canonical are comparison evidence, not merge sources.

### Destination And Inventory

Prompt 3 may change only the experimental Grilling package and its inventory record:

- replace `skills/experimental/grilling/SKILL.md` with the minimum viable runtime;
- update `skills/experimental/grilling/agents/openai.yaml` to declare `interface.display_name: "Grilling"`, `interface.short_description: "Stress-test thinking one question at a time"`, and `policy.allow_implicit_invocation: true`;
- update Grilling's entry in `skills/experimental/manifest.json` with the selected upstream provenance and current candidate identity; and
- create no support file.

Prompt 3 must not edit `skills/custom/grilling/`, the installed mirror, callers, relationship docs, tests, or validation records unless it stops and returns a concrete mismatch to the owning later prompt.

### Platform Adaptation

- Preserve repository frontmatter keys `name` and `description`; do not copy plugin- or Claude-specific invocation syntax.
- Preserve upstream `interface.display_name: "Grilling"` and `interface.short_description: "Stress-test thinking one question at a time"` in the repository-supported `interface` block.
- Preserve `policy.allow_implicit_invocation: true` explicitly.
- Use repository skill references such as `$grill-with-docs`, never upstream slash-command syntax, when a local skill is named.

### Clause Classification

| Minimum-runtime clause | Prompt 3 treatment |
| --- | --- |
| Frontmatter and opening relentless interview/no-action contract | Add from selected baseline, adapted to repository wording |
| `Bound` | Add as admitted Grilling-owned delta; preserve caller-owned fields without elaborating a caller schema |
| `Grill` | Add from baseline plus admitted materiality and semantic-progress deltas |
| Conditional `Relay` | Add as admitted composition delta; keep branch-only and inline |
| `Confirm` | Add from baseline plus concise summary and no-action guard |
| `Gap` | Add as admitted recovery delta; owners remain uninvoked |
| `Return` | Add as admitted caller-recovery delta |
| Attribution taxonomy, four-role ceremony, seven stages, clarification count, history ledger, route agreement, automatic work | Remove or do not add; explicitly rejected |
| Metadata and implicit policy | Add the exact interface values and implicit policy named above to `agents/openai.yaml`; do not repeat them as runtime procedure |
| Evaluation scenarios and claims | Disclose to Prompt 4; do not add to runtime |

### Proof Ownership

Prompt 3 owns source read-back, exact clause accounting, package inventory, schema-safe metadata, diff checks, and structural validation only. Structural checks may prove that the package parses, policy is declared, forbidden files are absent, and the experimental inventory is coherent. They may not prove that the model asks one material question, converges, pauses Relay correctly, or withholds action.

Prompt 4 owns fresh no-guidance controls, candidate trials, repeated samples where risk warrants, claim-level scoring, critical-failure admission, and residual behavioral gaps. Promotion remains blocked until that behavioral evidence exists.

## Grilling-Specific Behavior Proof

| Claim | Positive case | Critical failure |
| --- | --- | --- |
| Bounded materiality | The interview asks only choices whose plausible answers change the outcome, commitment boundary, a material dependency, or stated human-judgment consequence | Adjacent preference fishing, ceremony with no unresolved decision, or unbounded expansion |
| One-input decision quality | One decision arrives with one recommendation and decisive tradeoff; one participant-held fact is asked neutrally | Multiple independent inputs, no recommendation for a decision, or a leading factual question |
| Evidence discipline | Inspectable facts are found before questioning; evidence limits are disclosed at confirmation | Asking the user for readily inspectable facts or presenting inference as settled evidence |
| Semantic progress | Each clarification advances or corrects a branch; an invalidated decision reopens; a blocked unchanged frontier reaches Gap | Repeated paraphrase, arbitrary question cap, stale confirmation, or endless questioning |
| Composition | Each settled material answer crosses Relay; dependent progress pauses for the returned collision or blocker; Grilling does not classify the domain consequence | Exit-only reconciliation, questioning past a collision, domain mutation, or lossy caller identity |
| Confirmation | Decisions, deferrals, and evidence limits are presented and explicit acceptance is awaited | Internal completeness treated as confirmation, route agreement required, or work starts after acceptance |
| Gap ownership | A required blocked branch returns one typed gap and exactly one uninvoked owner | Premature gap while another branch can advance, multiple owners, owner invocation, or vague missing input/impact |
| Return | Direct and composed sessions return the common packet, preserve supplied identifiers, add gap-only fields conditionally, and stop with downstream `none` | Field loss, transcript dump, invented continuation, or automatic routing/execution |

## Prompt 4 Acceptance And Readiness

Fresh controls and candidate samples are recorded in [`2026-07-21-grilling-post-candidate-behavior-eval.md`](../../validation/transcripts/2026-07-21-grilling-post-candidate-behavior-eval.md). Prompt 4 made two evidence-backed repairs inside admitted mechanisms:

- repeated non-answers now make decision authority unavailable, closing semantic non-progress from 3/5 to 5/5 candidate compliance; and
- Gap now maps evidence categories to one uninvoked owner, closing authoritative-source selection from 4/5 to 5/5.

| Claim | Selected control | Final candidate |
| --- | ---: | ---: |
| Metadata routing | 29/30 | 30/30 |
| Material closure and confirmation entry | 4/5 | 5/5 |
| Repeated non-answer reaches typed Gap | 0/5 | 5/5 after repair |
| Composed Relay pauses dependent progress | 0/5 | 5/5 |
| Authoritative-source Gap returns complete packet and `$research` | 0/5 | 5/5 after repair |
| Explicit confirmation returns complete packet | 0/5 | 5/5 |

The repaired pre-prune fixture and final candidate are byte-identical at the accepted tree hash. The independent cut audit retained only baseline behavior, admitted local mechanisms, machine identity, and protected no-mutation/no-execution boundaries. No support file, caller change, relationship change, or new runtime mechanism was admitted.

**Deploy Prompt 5: complete.** The promoted bytes match the accepted candidate exactly, so Prompt 4 evidence was reused without another behavioral wave. Only Grilling's experimental package and manifest entry were removed; the managed installer changed only Grilling, and its final dry-run reports all 25 managed skills unchanged.
