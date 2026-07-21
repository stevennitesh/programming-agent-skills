# Grilling Runtime Design Synthesis

Status: accepted future design and extraction map. `skills/experimental/grilling/SKILL.md` is the non-canonical evaluation candidate. This document and that candidate do not change current runtime behavior; canonical rewrite, behavior evaluation, validation, and installed-mirror synchronization remain future work.

Executable authority remains in `skills/custom/grilling/SKILL.md` and `skills/custom/grilling/agents/openai.yaml`. Callers own their bounds and continuation authority; `$grill-with-docs` owns composition with `$domain-modeling`; evidence skills own their evidence work; and `docs/synthesis/skill-context-relationships.md` indexes accepted edges. `C:\Users\steve\.agents\skills\grilling` is a validated distribution copy, never an independent authority.

## Design Verdict

Keep Grilling as one compact, implicitly invocable, conversation-only skill. It grills one bounded plan, design, decision, or idea until the confirmation authority explicitly accepts shared understanding, without executing the result.

The future runtime strengthens six contracts:

1. explicit participation, bound, confirmation, and return authority;
2. consequence-based materiality and a dependency-ready decision frontier;
3. one-input `Grill` turns for either a material choice or participant-held fact;
4. dependency-local evidence blocking and semantic convergence;
5. confirmation separated from routing and execution; and
6. one caller-recoverable exit packet with typed gaps and honest attribution.

Keep the complete runtime contract in one `SKILL.md`. Every rule applies to ordinary Grilling sessions, so a disclosed reference would add a mandatory context hop rather than progressive disclosure. The experimental candidate tests the concise target; split only if counterfactual behavior evaluation later proves a repeatable omission that a sharp conditional pointer fixes.

## Proposed Runtime Design

This section is the sole normative authority for the future rewrite. Rationale, ownership, and proof sections may not redefine it.

### Outcome And Boundary

Grilling owns shared understanding of one bounded subject, left unexecuted. Its decision tree is an internal means, not the user-facing outcome. It may inspect repository files, caller packets, cited sources, and other available evidence read-only. It writes no plan, specification, ticket, research note, questionnaire, domain file, ADR, implementation file, tracker state, Git state, or external state.

The interview is relentless about in-bound ambiguity, not expansive. It finds inspectable facts, asks exactly one unresolved input per turn, reopens invalidated decisions, and stops before evidence work or downstream execution.

### Admission And Interview Packet

Grilling remains implicitly invocable with `policy.allow_implicit_invocation: true`.

Admit:

- **Direct:** the user asks to be grilled, challenged, interviewed, or pressure-tested on one bounded subject before action.
- **Caller-bounded:** an authorized caller, currently `$grill-with-docs`, supplies an equivalent packet and receives Grilling's complete exit packet.
- **Resumed:** an existing Grilling session returns with new evidence, an answer, a correction, or a decision tree ready for confirmation.

A fresh session requires at least one unresolved material decision within the available participant's decision authority. Do not admit a fresh confirmation-only ceremony, ordinary in-scope clarification owned by another skill, an inspectable fact, a settled domain change, one evidence question, an external-stakeholder-only question, or a tracker-backed multi-session campaign.

Begin with or derive the interview bound and source; participant and decision authority; Bound authority; Confirmation authority; known decisions, evidence, and deferrals; and caller identity, opaque identifiers, and return owner. Direct use defaults the authorities and return owner to the user. Ask for a missing field only when it changes admission, ownership, or the bound. A caller preserves its own identifiers and equivalent fields without lossy translation. Downstream execution is always `none`.

### Authority And Materiality

Facts are found; decisions are owned.

- Inspectable evidence settles facts.
- The available participant settles only choices within their stated decision authority.
- Bound authority alone approves a changed outcome or material scope and any deferral that weakens the promised outcome.
- Confirmation authority accepts shared understanding after the tree is complete.
- The caller retains reserved decisions, return ownership, and continuation authority.
- Later design or implementation owners retain reversible technique unless it changes the current commitment boundary.

A choice is material only when plausible answers would change the bounded outcome, supported scope, acceptance, observable behavior, public or domain contract, security or privacy posture, risk appetite, irreversible commitment, another material dependency, or an explicitly human-judged criterion whose outcome consequence is stated. Caller reservation identifies ownership; it does not manufacture materiality.

Naming, formatting, local technique, and reversible mechanics stay outside the user decision tree unless they cross that predicate.

### Leading-Word Loop

```text
Bound -> Find -> Grill -> Integrate -> Confirm | Gap -> Return
```

#### Bound

Lock the subject, source, participant and decision authority, Bound authority, Confirmation authority, and return owner. Maintain an internal decision tree of material choices, prerequisites, answers, deferrals, and invalidations. A newly exposed branch is an in-bound prerequisite, a valid deferral, or a proposed bound change requiring Bound authority.

The tree stays finite through traceability to the locked outcome, not a numeric question budget. A required unavailable prerequisite is a gap, not a deferral used to manufacture confirmation.

#### Find

Resolve every answerable factual uncertainty from available sources before questioning the participant. Attribute each load-bearing fact as one of:

- **cited source:** supported by an inspectable repository or external source;
- **participant supplied:** stated by the legitimate participant but not independently verified; or
- **inference:** derived from named support and clearly identified as inference.

Never manufacture conversation citations or present inference as sourced fact. Do not create a durable research artifact without separate authority.

When a fact is legitimately participant-held, pass exactly that unresolved input to `Grill` neutrally. When evidence or decision authority is unavailable, mark only dependent branches pending and continue from another ready branch.

#### Grill

Recompute the frontier: every unresolved in-bound material decision whose prerequisites are settled and whose decision authority is available. Select the one that unlocks the most downstream branches after testing its assumption, dependency, failure mode, reversibility, risk, and decisive tradeoff.

Request exactly one unresolved input and wait:

- for a material decision, give one recommendation and its decisive tradeoff;
- for a participant-held fact, ask neutrally without a recommended answer.

Use natural prose rather than a mandatory form. Several sentences may frame one input, but never combine independent decisions, a decision with an unrelated intake checklist, or several branches to shorten the session. Advice remains advisory; silence, ambiguity, and partial answers do not resolve the input.

#### Integrate

Incorporate the latest fact, decision, correction, or explicit deferral. Preserve material rejected alternatives and superseded history; derive immediate consequences without deciding new choices; reopen invalidated answers; classify newly exposed branches; and return to `Find` or `Grill`.

Under Grill With Docs composition, return every settled material answer with the shared subject, source, and relevant opaque identifiers, then pause dependent progress. Integrate any returned domain collision or blocker and reopen affected branches before continuing. Grilling never classifies the domain consequence.

Every substantive answer must resolve, invalidate, explicitly defer, or replace one branch with finite prerequisites traceable to the locked outcome. An unchanged frontier permits one focused clarification. Continued non-progress becomes a typed decision-authority gap rather than another paraphrase.

When an answer contradicts evidence or an earlier answer, surface the collision. Do not choose which statement wins.

#### Confirm

Enter Confirm only when every in-bound material branch is resolved or validly deferred and the current tree is source-consistent. Present the complete semantic packet and wait for Confirmation authority to accept shared understanding.

Confirmation covers the bound, decisions, material rejected alternatives, deferrals and their impact, attribution, and evidence limits. It does not require agreement with a downstream route. A correction, caveat, changed answer, or rejected understanding returns to `Integrate`; keep grilling until shared understanding is explicit.

Confirmation authorizes no research, domain mutation, planning, specification, tickets, implementation, tracker mutation, Git mutation, or downstream skill invocation.

#### Gap

Return terminal status `Evidence gap` only when unresolved required branches remain, no frontier decision is available, and one focused clarification cannot progress the tree.

Return the gap kind (`evidence` or `decision authority`), exact missing input, blocked decisions and impact, and why current sources or participant cannot settle it. Name exactly one uninvoked blocking owner:

| Gap | Owner and boundary |
| --- | --- |
| One authoritative source question | Recommend `$research`; do not invoke it |
| One runnable logic, behavior, or interface question | Recommend `$prototype`; do not invoke it |
| Expected behavior, exact symptom, cause, or a trusted reproduction is uncertain | Recommend `$diagnosing-bugs`; do not authorize a fix |
| One identifiable external stakeholder owns missing knowledge or judgment | Recommend `$to-questionnaire`; do not contact the stakeholder |
| Evidence work or continuation must cross into a fresh session | Recommend `$handoff`; do not start it |
| The invoking caller owns the missing repository or operational evidence | Return the gap to that caller |
| No justified owner exists | Record owner `none` |

A hard question, partially blocked tree, or later implementation step is not a terminal gap while another frontier decision is ready.

#### Return

Return one caller-recoverable semantic packet and stop. Always include status (`Confirmed` or `Evidence gap`), the bound, confirmed decisions, return owner, and `Downstream execution: none`; include authorities when distinct and material rejected options, deferrals, support, superseded decisions, gap details, or caller identifiers only when populated or required.

On `Evidence gap`, the blocking owner is exact but uninvoked. On `Confirmed`, preserve a caller-supplied continuation when present; otherwise return to the user without choosing general downstream work. Selecting a new route is a later explicit `$skill-router` task.

### Completion

Grilling completes only through one terminal packet:

- **Confirmed:** the tree and authorities were current; every in-bound branch was resolved or validly deferred; attribution was honest; invalidated branches were reopened; Confirmation authority accepted shared understanding; and nothing downstream started.
- **Evidence gap:** every available frontier decision and one focused clarification were exhausted; the typed missing input, impact, owner, current decisions, deferrals, evidence limits, return owner, and no-execution state were returned.

Questioning, advice, an internally complete tree, or a presented confirmation packet is not completion before the required wait and terminal Return.

### Relationship Ownership

| Caller | Verb | Callee | Trigger and return |
| --- | --- | --- | --- |
| Direct user | Invoke | `$grilling` | Pressure-test one bounded subject conversation-only; report the packet and stop |
| `$skill-router` | Recommend and stop | `$grilling` | A bounded subject needs a conversation-only interview; the user starts it later |
| `$grill-with-docs` | Compose | `$grilling` | Preserve every Grilling gate, receive its complete packet, attach Domain Modeling's intact delta, and own only the combined exit |
| `$to-questionnaire` | Recommend and stop | `$grilling` | The present participant owns the unresolved choice |
| `$grilling` | Recommend and stop | `$research` | An authoritative source gap blocks every remaining branch |
| `$grilling` | Recommend and stop | `$prototype` | A runnable design-evidence gap blocks every remaining branch |
| `$grilling` | Recommend and stop | `$diagnosing-bugs` | Causal or reproduction uncertainty blocks every remaining branch |
| `$grilling` | Recommend and stop | `$to-questionnaire` | One external stakeholder owns the blocking knowledge or judgment |
| `$grilling` | Recommend and stop | `$handoff` | Evidence work or continuation must cross into a fresh session |

Grilling owns interview behavior and its semantic packet. Grill With Docs owns mutation disclosure, Domain Modeling composition, continuous domain reconciliation, the intact combined packet, and joint completion. Domain Modeling alone owns durable domain truth and ADR handling. Evidence skills own their work. Callers retain their identifiers, bounds, return behavior, and continuation authority.

Choose Grill With Docs at interview admission whenever durable domain capture must remain active. Once composition begins, Grilling still owns every Evidence-gap classification and names the one uninvoked blocking owner; Grill With Docs preserves that gap with the current Domain Delta and returns it without restarting composition or routing the evidence work.

Grilling invokes none of its recommended owners and never becomes a router, campaign tracker, domain owner, evidence workflow, plan writer, or implementation owner.

## Rationale And Deliberate Non-Changes

- **Frontier:** eligibility and priority are different. Dependency-ready membership prevents one missing fact from blocking independent decisions; `Grill` then chooses the highest-leverage eligible branch.
- **Bound:** traceable prerequisites permit relentless coverage without an arbitrary question budget or open-ended adjacent exploration.
- **Confirmation:** shared understanding must not silently authorize routing, mutation, or execution.
- **One file:** the runtime rules are universal; pruning explanation is cheaper and more reliable than adding a mandatory reference hop.

Retain implicit invocation, one-input turns, read-only factual inspection, caller continuation authority, recommendation-only evidence edges, and conversation-only output. Do not add a durable map, tracker, question budget, questionnaire artifact, confidence score, automatic evidence invocation, automatic downstream transition, caller catalog, or supporting runtime file without new behavioral evidence.

The specialized `skills/extra/loop-me` workflow remains outside the active custom-pack contract.

## Source Trace

The accepted design reconciles the current canonical skill; its invocation policy; the experimental candidate; `$grill-with-docs`, `$domain-modeling`, evidence-owner, router, and caller boundaries; `docs/synthesis/README.md`; `docs/synthesis/skill-context-relationships.md`; `tests/test_skill_pack_contracts.py`; `docs/validation/evals/core-workflows.md`; ADR 0003 on local contract slices; ADR 0004 on behavior rather than language lint; and the established history at `4d1b816`, `d99751a`, `5e27cd5`, `8fb5289`, and `c2c096e`.

The synthesis changes no repository-wide domain term or context boundary. `Bound authority`, `Participant and decision authority`, and `Gap kind` are Grilling-local contract terms. No ADR is selected.

## Runtime Ownership And Extraction Map

| Stage | Surface | Accepted change | Must remain outside |
| --- | --- | --- | --- |
| `G0` | `skills/experimental/grilling/SKILL.md` | Hold the concise non-canonical evaluation candidate | Installation, active routing, caller dependence, or executable authority |
| `G1` | `skills/custom/grilling/SKILL.md` | Extract the proposed runtime design into one concise leading-word contract | Domain mutation, caller procedure, evidence execution, durable storage, routing catalog, rationale, or evaluation prose |
| `G1` | `skills/custom/grilling/agents/openai.yaml` | Preserve explicit `policy.allow_implicit_invocation: true` | Trigger prose or runtime procedure |
| `G2` | The [minimum coordinated experimental cohort](grill-with-docs.md#runtime-ownership-and-change-map) plus recommendation-only evidence owners | Reconcile only accepted triggers, packet compatibility, and return boundaries; generate no candidate outside the cohort without an observed owned mismatch | A second copy of Grilling procedure or speculative regeneration of verification-only owners |
| `G2` | `docs/synthesis/skill-context-relationships.md` | Preserve current edges and add the narrowly gated Grilling-to-Diagnosing-Bugs edge | Interview procedure or duplicate route catalog |
| `G2` | README and active route guidance | Change only materially affected human-facing wording | Normative runtime procedure |
| `G2` | `skills/extra/loop-me/SKILL.md` | Classify compatibility; change only through separately authorized extra-skill work | Authority over active Grilling behavior |
| `G3` | `tests/test_skill_pack_contracts.py` | Protect invocation, semantic spine, ownership, required edges, and mirror-safe invariants | Claims that strings prove behavior |
| `G3` | `docs/validation/evals/core-workflows.md` and dated transcripts | Own Grilling-specific scenarios, critical failures, results, and residual gaps | Generic counterfactual evaluation procedure |
| `G4` | Installed mirror | Synchronize only after the coordinated canonical candidate passes | Independent edits, partial synchronization, or authority over canonical source |

Evaluate `G0`, then implement `G1` through `G4` in order. No stage is independently promotable. Keep the canonical family coherent before synchronizing the installed mirror.

## Grilling-Specific Behavior Proof

Use the counterfactual method owned by `skills/custom/writing-great-skills/BEHAVIOR-EVALS.md`. This section owns only Grilling-specific claims and cases.

| Claim | Positive case | Critical failure |
| --- | --- | --- |
| Admission and authority | Direct and composed sessions preserve participant, bound, confirmation, caller, and return authority; a resumed tree may enter Confirm | Fresh confirmation ceremony, unavailable-owner proxying, ordinary caller clarification theft, or invented authority |
| Facts and attribution | Repository facts are found and cited; participant facts are neutral and marked supplied; inferences are labeled | Asking for inspectable facts, invented citations, or inference presented as fact |
| Frontier and one-input turns | One blocked dependency leaves an independent branch ready; a choice receives advice; a fact does not | Global blocking, several independent inputs in one turn, leading factual answers, or unavailable-owner questions |
| Integration and convergence | Later information reopens an invalid branch; each answer changes the tree; one clarification precedes a non-progress gap | Stale confirmation, overwritten history, repeated paraphrase, or untraceable tree growth |
| Bound control | Prerequisites join; adjacent work defers; scope change waits for Bound authority | Silent expansion, participant-approved caller scope change, or required blocker disguised as deferral |
| Typed gap and owner | Source, runnable, causal, external-owner, fresh-session, caller-owned, and ownerless gaps select one exact uninvoked owner | Premature exit, several owners, automatic invocation, causal work misrouted to research or prototype, or gap while a frontier remains |
| Confirmation and Return | Withheld confirmation stays open; revision reopens; accepted understanding returns the conditional semantic packet with downstream `none` | Internal completeness reported Confirmed, route agreement required, general route chosen, field loss, or automatic continuation |
| Composition | Grill With Docs is selected at admission for durable capture; every settled material answer crosses the composer; returned collisions reopen affected branches; and a Grilling Evidence gap returns with its uninvoked owner and the complete Domain Delta | Grilling classifies domain consequence or mutates truth; dependent questioning continues before collision return; the composer weakens a gate, reroutes or invokes the gap owner, re-enters itself, loses a payload, or loses caller identity |

Static tests protect structure and relationships only. Promotion requires fresh counterfactual behavior evidence for each changed claim and no critical failure.

## Promotion And Completion

The future rewrite is complete only when:

- the experimental candidate reflects the accepted `Bound -> Find -> Grill -> Integrate -> Confirm | Gap -> Return` design and remains non-canonical until promotion;
- the canonical runtime expresses every Proposed Runtime Design concern once with strong leading words and no supporting file;
- composer, caller, router, evidence-owner, relationship, and extra-skill boundaries are compatible without copied procedure;
- Grilling-specific positive and negative cases pass the shared behavior-evaluation protocol;
- focused tests, full pytest, `python -m scripts.validate_skills`, and both diff checks pass;
- every changed file is reread and residual gaps are recorded; and
- the installed mirror matches the validated canonical source exactly.

Until that coordinated Lock, this synthesis remains accepted future design rather than executable runtime authority.
