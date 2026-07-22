# Grill With Docs Composition Synthesis

Status: Prompt 5 complete. Accepted candidate `09438242574437c91ed631a1dd59010f3c02752b51b8eb93d096259fab65def7` is canonical and installed with matching hashes; its experimental package and manifest entry are removed. Prompt 4 evidence was reused because bytes and claims were unchanged.

Runtime authority currently remains in:

- `skills/custom/grill-with-docs/SKILL.md` and `skills/custom/grill-with-docs/agents/openai.yaml`;
- Grilling for the interview and intact Grilling exit packet;
- Domain Modeling for domain meaning, persistence, ADR handling, and the authoritative cumulative Domain Delta;
- `docs/synthesis/skill-context-relationships.md` for the current pack-wide relationship map; and
- the current structural and behavioral proof surfaces.

The sibling [Grilling Decision-Frontier Synthesis](grilling.md) and [Domain Modeling Durable-Truth Synthesis](domain-modeling.md) own component behavior. This synthesis owns only their composition.

## How To Read This Document

Consistent with [ADR-0007](../../adr/0007-synthesis-preserves-exhaustive-research-runtime-skills-compress.md):

1. **Orientation** states the selected future design.
2. **Normative Design** is the sole authority for future runtime behavior.
3. **Evidence And Decisions** preserves exhaustive research, admissions, rejections, and current-runtime comparison without creating rules.
4. **Extraction And Proof** tells Deploy Prompt 3 where each admitted behavior belongs and how later prompts prove it.

When another layer conflicts with Normative Design, correct the other layer. A confirmed decision enters runtime only through the destination named in the extraction map.

# Layer One: Orientation

## North Star

Grill With Docs is an explicit, direct-user composer for one bounded repo-backed decision that needs both relentless Grilling and active Domain Modeling. It returns the intact Grilling packet and Domain Modeling's current cumulative Domain Delta as one result, then stops.

The composer owns only admission, pre-question disclosure, scheduling, Relay, combined status, and Return. It does not own questioning, semantic judgment, persistence, ADR approval, component payloads, caller continuation, or downstream execution.

## Simplest Credible Baseline

The selected design control is Matt Pocock's complete one-line skill:

```text
Run a /grilling session, using the /domain-modeling skill.
```

That is the smallest credible expression of the core outcome: compose Grilling with Domain Modeling. The repository adapts the slash-command vocabulary to `$grilling` and `$domain-modeling`, and the Codex platform requires `agents/openai.yaml` to make the composer explicit-only. Everything else must earn admission as a delta from this baseline.

## Minimum Viable Runtime

```text
Admit -> Compose [Grill <-> Relay <-> Model] -> Return
```

- **Admit** accepts only an explicit direct-user request needing both components, locks mutation authority, and gives the required disclosure before the first question.
- **Compose** runs one Grilling session with Domain Modeling active.
- **Relay** carries each settled material answer to Domain Modeling and any collision back before dependent progress.
- **Return** derives one combined status, preserves both component payloads intact, reports an exact blocker and re-entry condition when blocked, and stops.

`Relay` is a repeated callback inside `Compose`, not a peer phase. Pre-question disclosure is part of `Admit`. Joint eligibility is part of `Return`. The runtime needs neither separate `Disclose` and `Join` stages nor a state machine.

## Composer Vocabulary

| Term | Meaning |
| --- | --- |
| **Composition fit** | One explicit direct-user request needs both a bounded Grilling interview and active Domain Modeling |
| **Settled material answer** | An answer Grilling has integrated as decision-bearing under its own rules |
| **Relay** | Opaque transport of each settled material answer to Domain Modeling and any returned collision or blocker to Grilling before dependent progress |
| **Component payload** | The complete Grilling exit packet or authoritative cumulative Domain Delta, preserved under its owner's schema |
| **Combined status** | `Confirmed`, `Evidence gap`, or `Blocked`, derived by the composer without replacing component states |

These are composer-local terms, not additions to the repository domain model.

# Layer Two: Normative Design

## Contract Map

| Concern | Owner | Destination | Failure return |
| --- | --- | --- | --- |
| Explicit-only platform policy | Grill With Docs metadata | `agents/openai.yaml` | Candidate is not extractable without `allow_implicit_invocation: false` |
| Direct composition fit, modes, and pre-question disclosure | Grill With Docs | [Admit](#admit) | Exact mismatch or `Blocked` with exact blocker and re-entry condition |
| Interview and exit packet | Grilling | Component-owned | Preserve its result intact |
| Domain semantics, mutation, ADR handling, and cumulative Domain Delta | Domain Modeling | Component-owned | Preserve its collision, blocker, and delta intact |
| Settled-answer and collision transport | Grill With Docs | [Compose And Relay](#compose-and-relay) | Pause dependent progress; return `Blocked` if a current delta cannot be obtained |
| Combined status, packet, and stop boundary | Grill With Docs | [Return](#return) | `Blocked`; start nothing |
| Completion | Grill With Docs | [Completion](#completion) | Remain incomplete or `Blocked` |

## Admit

Grill With Docs is explicit-only and admits only a direct user. Admit when the user explicitly invokes it for one bounded repo-backed decision that needs both user-owned ambiguity resolution through Grilling and active Domain Modeling.

Reject a mismatch before starting either component. Name the narrower owner when the work needs only Grilling or only Domain Modeling, but do not invoke that owner. The composer is not a router.

Lock only the shared subject and Source Trace plus Domain Modeling's two independent mutation modes:

- context action defaults to `render only`; use `persist authorized` only when the user separately grants that authority; and
- ADR action defaults to `offer only`; create an ADR only after separate explicit approval for an identified candidate.

Before Grilling asks its first question, tell the user the effective context action, the separate ADR approval gate, that a domain collision may reopen or block a branch, and that confirmation starts no downstream work. This disclosure reports authority and grants none.

Each component validates its own inputs and authority. The composer does not invent a universal entry packet, caller identity, opaque identifiers, return-owner field, or generalized handoff contract.

Admit completes when the work fits both components, their subject and source agree, the effective mutation modes are explicit, and the disclosure has been made. A missing or contradictory requirement returns `Blocked` with the exact blocker and re-entry condition.

## Compose And Relay

Run one Grilling session with Domain Modeling active throughout.

Grilling exclusively owns participant authority, factual legwork, materiality, frontier selection, questioning, bounds, Evidence gap, confirmation, its exit packet, and its completion criterion.

Domain Modeling exclusively owns domain-consequence classification, semantic resolution, context routing, context and ADR mutation, verification, the authoritative current cumulative Domain Delta, and its completion criterion.

After every settled material answer:

1. relay the answer with the shared subject and source to Domain Modeling;
2. receive Domain Modeling's authoritative current cumulative Domain Delta;
3. carry that delta opaquely without filtering, merging, versioning, or keeping a bridge ledger;
4. relay any material collision or blocker to Grilling intact; and
5. allow dependent questioning to continue only after Grilling integrates the returned result.

Grilling decides whether an answer is settled and material. Domain Modeling decides whether its domain consequence is no-change, resolved, contradictory, rendered, persisted, or blocked. A cumulative no-change Domain Delta is valid. If Domain Modeling cannot return a current delta, return `Blocked` rather than continuing silently or relabeling the failure as Grilling's Evidence gap.

## Return

When Grilling reaches a terminal candidate, derive one combined status from current component results without re-performing either completion criterion or asking for a second confirmation:

| Status | Eligibility |
| --- | --- |
| `Confirmed` | Grilling returns its complete confirmed packet; Domain Modeling returns a current complete delta; no material nondeferred collision or blocker remains |
| `Evidence gap` | Grilling returns its legitimate complete Evidence-gap packet; Domain Modeling returns a current complete delta through the last settled answer |
| `Blocked` | Admission, component integrity, Relay, collision processing, mutation verification, payload currency, or compatibility cannot close |

Only Grilling originates `Evidence gap`. A Domain Modeling failure is `Blocked` at the composer boundary.

Return only:

```text
Status: Confirmed | Evidence gap | Blocked
Grilling exit packet: <attached intact when available>
Domain Delta: <attached intact when available>
Composition blocker and re-entry condition: <Blocked only>
```

The direct user is necessarily the recipient, so caller identifiers and return-owner fields are noise and are omitted. Do not copy admission data, disclosure text, callback history, component semantics, or continuation instructions into the packet.

Return to the user and stop. `Confirmed` selects no next route. `Evidence gap` preserves Grilling's exact uninvoked evidence owner. `Blocked` explains safe re-entry without performing recovery.

## Completion

Complete only when:

- Admit either establishes direct dual-capability fit or returns the exact mismatch;
- the mutation modes and required disclosure are explicit before questioning;
- both components retain their contracts;
- every settled material answer and returned collision traverses Relay before dependent progress;
- Domain Modeling alone supplies a current cumulative Domain Delta;
- Return derives exactly one allowed status from intact current component results;
- a blocked result names the exact blocker and re-entry condition; and
- no downstream workflow starts.

Composer completion never substitutes for component completion.

## Relationships

The future runtime has only these executable relationships:

| Source | Relationship | Target | Trigger and return |
| --- | --- | --- | --- |
| Direct user | Explicitly invoke | `$grill-with-docs` | One bounded repo-backed decision needs both components; receive the combined packet and stop |
| `$grill-with-docs` | Compose | `$grilling` | Preserve its complete interview contract and intact exit packet |
| `$grill-with-docs` | Compose | `$domain-modeling` | Relay every settled material answer and preserve its authoritative cumulative Domain Delta |

Wayfinder, Triage, and Improve Codebase caller integrations are deferred. They are not admitted runtime branches, entry fields, Return fields, or Prompt 3 extraction work. Recommendation-only or suggestion-only references may continue to tell the user that the explicit skill exists, but they confer no admission or continuation authority.

The current relationship index still describes the current canonical skill and therefore remains unchanged in Prompt 2. It becomes an affected promotion surface only after the experimental candidate is accepted and the canonical invocation policy and caller edges actually change.

# Layer Three: Evidence And Decisions

## Baseline Evidence

Prompt 1 inspected all required checked-out upstreams and the complete current canonical package:

| Candidate | Observed state | Result |
| --- | --- | --- |
| Matt Pocock | clean `ed37663cc5fbef691ddfecd080dff42f7e7e350d`, dated 2026-07-21 | Matching one-line package selected as simplest credible baseline; its explicit invocation is retained, while slash-command and write-authority assumptions are adapted to this repository and platform |
| Superpowers | clean `d884ae04edebef577e82ff7c4e143debd0bbec99`, dated 2026-07-02 | No matching or equivalent package found |
| Ponytail | clean `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`, dated 2026-07-15 | No matching or equivalent package found |
| Prior canonical | one-file implicit composer with direct, Wayfinder, Triage, and Improve Codebase admission | Historical composition evidence, not current authority |

Freshness is bounded to those Prompt 1 observations. No behavioral claim was proved by the upstream comparison.

## Prior Runtime Versus Promoted Design

The prior canonical used:

```text
Admit -> Disclose -> Compose [Grill <-> Relay <-> Model] -> Join -> Return
```

It was implicitly invocable, admitted three workflow callers in addition to direct use, transported caller identifiers and return ownership, and named Disclose and Join as peer stages.

The promoted design changes those points deliberately: explicit-only, direct-user-only, no caller packet, disclosure folded into Admit, and joint eligibility folded into Return. It preserves render-only default, separate ADR approval, every-answer Relay, Domain Modeling's cumulative-delta ownership, intact component payloads, three combined statuses, exact blocked re-entry, and no downstream execution.

## Mechanism-Admission Ledger

| Mechanism beyond one-line baseline | Baseline failure or required contract | Owner | Cheaper alternative | Load | Admission and destination |
| --- | --- | --- | --- | --- | --- |
| Codex component names | Slash-command syntax is not this repository's skill vocabulary | Platform adaptation | Keep slash syntax | Two names | **admit**: inline composition sentence |
| Explicit-only metadata | Human judgment must select every use | `agents/openai.yaml` | Implicit dual-condition description | Human cognitive load, lower ambient context load | **admit**: metadata |
| Direct dual-capability admission | One-line baseline can run for single-capability work | Grill With Docs | Trust user selection alone | Small entry gate | **admit**: inline Admit |
| Render-only default and separate ADR approval | Composition is not mutation consent | Domain Modeling owns action; composer locks it | Always write | Small authority gate | **admit**: inline Admit; detailed procedure component-owned |
| Pre-question disclosure | User must know mutation and no-execution boundaries before answering | Grill With Docs | Separate Disclose stage | Four compact facts | **admit**: fold into Admit |
| Every-settled-answer Relay | Exit-only modeling can discover collisions after dependent questioning | Composer transports; components interpret | Model once at exit | Repeated callback | **admit**: inline Compose |
| Cumulative Domain Delta | Composer-side reconstruction duplicates semantic reduction | Domain Modeling | Composer ledger | Conditional component work | **caller-owned** by Domain Modeling; carry opaquely |
| Collision return before dependent progress | Continuing can compound a contradicted model | Grilling integrates; composer transports | Report collision only at exit | Pause branch | **admit**: inline Compose |
| Three combined statuses | Component outputs need one coherent terminal signal | Grill With Docs | Return two unjoined statuses | Small Return table | **admit**: inline Return |
| Intact component payloads | Flattening loses owner-specific recovery semantics | Component owners | Universal schema | Two opaque attachments | **caller-owned**, preserved inline in Return |
| Exact blocker and re-entry condition | `Blocked` without recovery is not actionable | Grill With Docs | Status alone | One conditional field | **admit**: inline Return |
| No downstream execution | Confirmation grants no next-route authority | Direct user | Auto-route | One stop guard | **admit**: inline boundary and Return |
| Caller integrations | Current callers can supply identities and continuation contracts | Wayfinder, Triage, Improve Codebase | Direct use first | Branch and coordination load | **defer**: no Prompt 3 destination |
| Caller identifiers and return-owner fields | Needed only by deferred callers | Caller owners | Direct user as implicit recipient | Packet noise | **reject** from direct runtime |
| Separate Disclose and Join stages | Their behaviors remain necessary | Composer | Fold into adjacent gates | Navigation load | **reject** as stages; behavior admitted in Admit and Return |
| Universal schema, bridge ledger, callback history, state machine | No proved baseline failure requires durable composer state | none | Opaque transport | High runtime and maintenance load | **reject** |
| Evaluation and promotion machinery | Needed to prove and ship, not execute | Later deploy prompts | Runtime prose | Non-runtime process load | **non-runtime**: Layer Four and validation records |

## Rejected, Deferred, And Residual Complexity

Rejected runtime hypotheses are implicit invocation, universal entry or return schemas, caller identity plumbing, a bridge ledger, callback history, a normative state machine, separate Disclose and Join phases, component restatement, and automatic continuation.

Deferred caller integrations are Wayfinder, Triage, and Improve Codebase. Each would require its own observable trigger, supplied authority, identity, Return contract, relationship edge, and behavioral proof before admission. Prompt 3 must not prebuild extension fields for them.

Residual unavoidable complexity is limited to three control-backed behavior deltas—mutation authority and admission disclosure, combined terminal eligibility, and exact safe failure—plus the minimum protected Relay ownership seam. Prompt 4's corrected upstream control performed ordered Relay 5/5 without detailed composer guidance, so the final candidate collapses that procedure while retaining the confirmed transport boundary. The small `Blocked` field is the only branch-specific inline contract; keeping its exact re-entry data beside status derivation is cheaper and safer than a disclosed runtime file.

# Layer Four: Extraction And Proof

## Prompt 3 Extraction Map

The experimental package is one thin skill file plus platform metadata. No supporting runtime reference, script, schema, template, or asset is admitted.

| Classification | Behavior or surface | Exact destination | Prompt 3 action |
| --- | --- | --- | --- |
| Baseline | Compose Grilling with Domain Modeling | `skills/experimental/grill-with-docs/SKILL.md` opening outcome | Start from the one-line core using `$` vocabulary |
| Add | Direct dual-capability gate, render-only default, ADR offer-only default, and pre-question disclosure | Inline `Admit` | Extract the common entry gate |
| Add | Every-answer Relay, collision return, opaque cumulative delta | Inline `Compose` | Extract the repeated callback without component procedure |
| Add | Three statuses, intact payloads, blocker and re-entry, stop boundary | Inline `Return` | Fold joint eligibility into Return |
| Add | Checkable end condition | Inline completion | Protect authority, Relay currency, payload integrity, and no execution |
| Platform adaptation | Explicit-only invocation | `skills/experimental/grill-with-docs/agents/openai.yaml` | Set `policy.allow_implicit_invocation: false`; keep description concise and explicit-use oriented |
| Caller-owned | Interview, questioning, Evidence gap, confirmation, Grilling packet | Grilling runtime | Point by ownership; do not copy |
| Caller-owned | Domain semantics, persistence, ADR mechanics, cumulative Domain Delta | Domain Modeling runtime and disclosed references | Point by ownership; do not copy |
| Deferred | Wayfinder, Triage, Improve Codebase integrations | None | Do not create fields, branches, or references for future callers |
| Non-runtime | Upstream evidence, admission ledger, rationale, evaluation and promotion procedure | This synthesis and Prompt 3 validation record | Keep out of runtime |
| Rejected | Universal schema, caller packet, bridge ledger, callback history, state machine, separate Disclose and Join stages | None | Do not extract |

The smallest coordinated experimental cohort is only `grill-with-docs`. Grilling and Domain Modeling already expose the required component contracts; Prompt 3 verifies compatibility read-only and changes them only if it finds a concrete contradiction that makes extraction impossible. Caller skills and the current relationship index are outside Prompt 3 because their integrations are deferred and canonical behavior has not changed.

## Proof Ownership And Phases

| Phase | Owner | Proves | Must not claim |
| --- | --- | --- | --- |
| Prompt 3 structural proof | Deploy Prompt 3 | Complete package inventory, explicit-only metadata, exact admitted surfaces, no undeclared files, readable candidate, and structural integrity | That wording changes multi-turn behavior |
| Prompt 4 behavior proof | Deploy Prompt 4 | Direct admission, disclosure timing, Relay order, collision pause, delta ownership, statuses, intact Return, blocked re-entry, and no execution against fresh controls | Promotion or installed parity |
| Prompt 5 promotion proof | Deploy Prompt 5 | Accepted candidate becomes canonical; affected current relationship and policy surfaces are reconciled; canonical tests and validation pass; installed mirror is synchronized when authorized by that prompt | New caller integrations |

Structural tests may assert machine-consumed policy and package shape. Semantic outcomes require behavior evaluation; they must not be encoded as brittle phrase-presence tests.

## Prompt 4 Behavioral Matrix

| Normative owner | Positive cases | Promotion-blocking negative cases |
| --- | --- | --- |
| Admit | Explicit direct dual-capability request admits; context defaults render-only; ADR defaults offer-only; disclosure precedes questioning | Implicit selection, single-capability admission, inferred write authority, late disclosure, or caller-specific fields |
| Compose and Relay | Every settled material answer reaches Domain Modeling; no-change is valid; collision returns before dependent questioning | Composer filters or merges, reconciles only at exit, fabricates delta state, or continues through collision |
| Return | Current component results yield exactly Confirmed, Evidence gap, or Blocked; payloads stay intact; blocker includes re-entry; nothing downstream starts | Second confirmation, false Confirmed, Domain failure relabeled Evidence gap, flattened payload, caller fields, vague Blocked, or continuation |

Use fixed realistic controls and fresh candidate contexts under the Writing Great Skills behavior-evaluation contract. Record evidence limits and residual gaps; do not treat structural assertions as semantic proof.

## Prompt 3 Extraction Readiness (Satisfied)

Prompt 3 classified every surface without inventing a decision:

- the exact baseline is quoted and its platform adaptations are named;
- every delta has an admission, owner, cheaper alternative, load, and destination;
- all common-path runtime behavior is inline, with component procedure caller-owned;
- no disclosed Grill With Docs runtime file is required;
- caller integrations and their fields are explicitly deferred or rejected;
- proof phases distinguish structure, behavior, promotion, and installation; and
- current canonical and relationship evidence is labeled current rather than normative future behavior.

No extraction choice remained between competing spines, invocation policies, caller sets, packet schemas, or proof methods.

## Prompt 4 Acceptance Decision

**Accepted and promoted to canonical source** at exact tree hash `09438242574437c91ed631a1dd59010f3c02752b51b8eb93d096259fab65def7`.

The upstream control failed admission/disclosure, one-component non-invocation, and all three combined-status Returns in all five samples. The final candidate passed every fixed case in five fresh contexts, as did the repaired pre-prune control; no critical failure or prune regression appeared. Ordered Relay was already correct in the neutral upstream control, so detailed Relay procedure was removed and only the protected seam remains. Evidence and residual limits are recorded in [`2026-07-22-grill-with-docs-post-candidate-behavior-eval.md`](../../validation/transcripts/2026-07-22-grill-with-docs-post-candidate-behavior-eval.md).

Prompt 5 reused this evidence because candidate bytes and affected claims remained unchanged. Executable caller integrations remain removed; Wayfinder, Triage, and Improve Codebase now recommend the explicit direct-user composer and stop.
