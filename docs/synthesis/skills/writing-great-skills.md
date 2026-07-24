# Writing Great Skills Design Synthesis

Status: Deploy Prompt 5 promoted the behaviorally accepted candidate into the
canonical package on 2026-07-21 at tree hash
`c7c02f4f9896cd5bf6e6c25886e77785a9f80c0ccea0d02f7aaa6fc85076dcc4`.
The Author phase migrated directly affected structural proof and stopped after
canonical proof. The separately owned continuation retired the experimental
copy and manifest entry, then synchronized the managed installed mirror at the
same hash. Git delivery was not performed.

Canonical runtime authority remains in:

- `skills/custom/writing-great-skills/SKILL.md`;
- `skills/custom/writing-great-skills/GLOSSARY.md`;
- `skills/custom/writing-great-skills/BEHAVIOR-EVALS.md`; and
- `skills/custom/writing-great-skills/agents/openai.yaml`.

`CONTEXT.md` owns pack artifact and vocabulary boundaries,
`docs/synthesis/skill-context-relationships.md` indexes accepted relationships,
and ADR 0004 keeps semantic language judgment out of mechanical validation.
Tests and behavioral evaluations prove the canonical design; they do not define
it. Installation, mirror synchronization, publishing, and Git delivery remain
with their existing owners.

`docs/synthesis/methods/deploy-prompts.md` owns rewrite cadence. This
synthesis owns the selected design and its acceptance obligations, not a second
implementation runbook.

The evidence snapshot is the working tree inspected through 2026-07-21, the
2026-07-21 authoring-boundary evaluation, the Prompt 4 metadata, full-package,
and pruning-equivalence studies, and freshly fetched upstream HEAD
`ed37663cc5fbef691ddfecd080dff42f7e7e350d`. The promoted package under
`skills/custom/writing-great-skills/` is now executable authority; the prior
active baseline and Prompt 4 candidate remain historical evidence.

# Verdict

## Outcome

Writing Great Skills owns one outcome:

> Make a canonical Codex skill produce a predictable process through the
> smallest behavior-changing semantic surface.

Predictability means a stable process, not identical output. Concision,
discoverability, context cost, and maintainability serve that outcome. A short
skill is worse when it hides authority or weakens completion; a long skill is
worse when it dilutes attention, duplicates meaning, or keeps branch-only
material in the common path.

## Ownership Boundary

Writing Great Skills supplies the instructions and judgment for creating,
auditing, and improving canonical skill behavior. It may edit the requested
canonical skill package and the smallest proof surfaces needed to establish the
change. It stops after canonical proof.

It does not own:

- new-package scaffolding, generated metadata, or generic package mechanics;
- installation, installed mirrors, manifests, synchronization, or promotion;
- publishing, staging, commits, pushes, or other delivery work; or
- generic subagent dispatch policy, worker topology, or collaboration settings.

Installation requires separate user or caller authority. Writing Great Skills
neither grants nor consumes that authority.

The bundled `skill-creator` remains installed. It leads new skill packages and
structural scaffolding; Writing Great Skills supplies semantic-quality judgment.
For an existing skill, Writing Great Skills leads behavior, wording, ownership,
context disclosure, and pruning. A structural branch uses `skill-creator` only
for its package mechanics. Neither owner copies the other's procedure.

## Selected Design

| Decision | Selected design |
| --- | --- |
| Invocation | Keep implicit invocation as a required local discovery contract. Treat the description as an always-loaded routing predicate: name observable request or caller triggers, add the closest exclusion only when necessary, and omit explicit-name reach, runtime procedure, and body-summary detail. |
| Package | Keep one short `SKILL.md`, one authoring glossary, one behavioral-evaluation reference, and one policy file. |
| Operations | Use `Audit` for strictly read-only judgment and `Author` for explicitly authorized canonical persistence. |
| Authoring behavior | Require source and authority resolution, single ownership, a discoverable caller-facing contract, behavior-preserving pruning, and claim-matched proof. The exact `Trace -> Own -> Shape -> Prune -> Prove` labels and fixed sequence are not independently admitted runtime mechanisms. |
| Semantic roles | Make outcome, authority, applicable action, Return, and completion discoverable. Defer the invented `Semantic Skill Surface` name and any fixed role order. |
| Behavioral evaluation | Make counterfactual evaluation a triggered behavior-proof branch, not a peer operation. A direct evaluation request may enter that branch without authoring authority. |
| Vocabulary | Keep `GLOSSARY.md` limited to durable authoring concepts and failure modes. |
| Proof | Match proof to the claim and stop after canonical structural, relationship, and behavioral evidence. |
| Delegation | Retain independence requirements for evidence, not permission or mechanics for dispatching workers. |
| Growth | Add no helper, schema, ledger, template, or new reference until observed variance proves the current package insufficient. |

The local design intentionally differs from upstream. Upstream remains source
pressure, not runtime authority. This pack needs Codex-specific invocation,
single-owner composition, canonical editing, and counterfactual proof; it does
not need to copy upstream invocation policy or runtime shape.

## Simplest Credible Baseline

The design control is Matt Pocock's current upstream
[`writing-great-skills`](https://github.com/mattpocock/skills/blob/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/productivity/writing-great-skills/SKILL.md)
package at `ed37663cc5fbef691ddfecd080dff42f7e7e350d`. It expresses the core
Predictability outcome through one explicit-only, all-reference `SKILL.md`, one
glossary, and one policy file. It already owns invocation cost, description
pressure, information hierarchy, split pressure, leading words, no-op pruning,
and positive targets.

Use it as the baseline for aggregate load and behavioral controls, not as local
runtime authority. The local design adds only Codex discovery, action and
mutation authority, pack ownership, counterfactual proof, and a typed
canonical-only Return. Upstream's examples and exact file shape remain source
evidence rather than required runtime.

## Minimum Viable Runtime

The smallest coherent local runtime is the baseline's Predictability,
information-hierarchy, pruning, and leading-word core plus these admitted
deltas:

- an implicitly invocable, trigger-only routing description;
- a read-only Audit path and explicitly authorized canonical Author path;
- source and authority resolution before judgment or mutation;
- one owner for each affected behavior and relationship;
- discoverable outcome, authority, applicable action, Return, and completion;
- preservation of non-intuitive safety and ownership contracts while no-ops
  and duplicated meaning are removed;
- claim-matched proof, with counterfactual mechanics loaded only for behavioral
  claims; and
- a typed Return that stops after canonical proof.

Only irreversible order is normative: authority and source resolution precede
judgment or mutation, and proof follows the candidate it evaluates. The exact
five-word spine and a universal semantic-role order are not runtime contracts.
The compact full-audit inventory may stay inside the conditionally inline
`full audit` branch in `SKILL.md`: creating another reference would cost more
pointer and maintenance load than this branch saves. `BEHAVIOR-EVALS.md`
remains the sole disclosed procedure for counterfactual evaluation.

## Mechanism Admission Ledger

| Mechanism | Baseline failure or required caller contract | Evidence | Owner | Cheaper alternative | Runtime, caller, proof, and maintenance load | Admission and destination |
| --- | --- | --- | --- | --- | --- | --- |
| Implicit invocation | Ordinary create/edit, audit/review, and behavioral-proof requests must reach the semantic owner without the human remembering its name. | Confirmed Prompt 1 caller contract; invocation behavior remains unproved. | Frontmatter and `agents/openai.yaml` | Upstream explicit-only policy | One always-loaded description; invocation evaluation | `admit` in metadata; evidence gap |
| Codex invocation vocabulary and policy | Upstream's `model-invoked` / `user-invoked` and `disable-model-invocation` contracts describe a different runtime and would misstate local reachability. | Current Codex `policy.allow_implicit_invocation` contract and confirmed local discovery decision. | `GLOSSARY.md`, frontmatter, and `agents/openai.yaml` | Copy upstream terminology literally | Small glossary adaptation and policy proof | `admit` local `implicitly invocable` / `explicit-only` vocabulary and `allow_implicit_invocation`; `reject` upstream runtime terms |
| Trigger-only description predicate | An implicit description must select observable requests without carrying runtime procedure or body summary. | Confirmed Prompt 1 contract; current literal tests are structural only. | Frontmatter description, shaped by `SKILL.md` | Upstream identity-plus-branches description | Small common-path rule; positive and adjacent-negative evaluation | `admit` in `SKILL.md` and metadata; evidence gap |
| Audit and Author authority | Review wording must not grant mutation; canonical persistence must stay bounded. | Non-intuitive safety boundary; Author boundary partly supported by the 2026-07-21 evaluation. | `SKILL.md` | Repeated ad hoc authority prose | Two compact modes; Audit and leakage evaluation | `admit` in `SKILL.md` |
| Source and coverage resolution | Full audits and bounded edits need current authority and affected-surface coverage. | Required Audit/Author caller contract. | `SKILL.md` | Unclassified repository scan | Compact bounded rule plus conditionally inline full-audit inventory | `admit`; full-audit branch inline because a new pointer costs more |
| Single ownership and relationship facts | Pack composition requires one rule, authority, evidence, Return, and completion owner. | Relationship map; `skill-creator` boundary evaluation. | `SKILL.md` and relationship map | Copy foreign procedure | Small common rule and relationship trace | `admit` |
| Five authoring behaviors | Local authoring needs resolution, ownership, shaping, pruning, and proof. | Required caller and safety contracts; exact labels add no measured value. | `SKILL.md` | Upstream flat reference | Compact behavior rules; scenario proof | `admit` behaviors; `defer` exact mnemonic and fixed sequence |
| Discoverable semantic roles | Authority, action, Return, and completion must not disappear into presentation. | Ownership and safety contracts; structural proof only for presentation. | `SKILL.md` | Fixed template or named surface | One compact rule; no separate vocabulary mechanism | `admit` roles; `defer` `Semantic Skill Surface` name and fixed order |
| Cut test and protected contracts | Relevance alone does not distinguish no-ops from safety-bearing guidance. | Baseline no-op rule, fixture 46, and non-intuitive safety boundary. | `SKILL.md` | Word-count or relevance-only pruning | Small runtime rule; behavior evaluation for claims | `admit` |
| Counterfactual behavior protocol | Static prose and tests cannot prove wording changes behavior. | ADR 0004, fixture 51, and successful repository evaluations. | `BEHAVIOR-EVALS.md` | Inline procedure or one-shot judgment | Branch-only reference; at least five fresh samples per arm for a behavioral claim | `disclose` |
| `skill-creator` and canonical stop | The baseline can absorb scaffolding, installation, and delivery into semantic completion. | 2026-07-21 evaluation improved 10/25 to 25/25 with zero candidate critical failures. | `skill-creator`, `SKILL.md`, and caller | One undifferentiated workflow | Compact boundary; relationship proof | `admit` boundary; scaffolding and delivery are `caller-owned` |
| Typed Return and completion | Generic completion leaked post-edit ownership. | 2026-07-21 evaluation. | `SKILL.md` | Unstructured prose return | Compact status and evidence shape | `admit` |
| Mirror inspection | Installation-state evidence is sometimes requested but repair belongs elsewhere. | Ownership contract. | Installation owner; Audit may report | Default mirror scan | Conditional read-only clause | `admit` as a conditionally inline boundary; repair is `caller-owned` |
| Evidence independence | Candidate leakage can invalidate a behavioral control. | Fixture 28 history and behavioral-evaluation contract. | Writing Great Skills for evidence; ambient policy for dispatch | Skill-owned worker topology | Branch-only proof discipline | `admit` boundary; mechanics are `caller-owned` |
| Literal tests, synthesis ledgers, helpers, and schemas | These can protect or explain behavior but do not create it. | ADR 0004 and Prompt 1 cut test. | Tests, synthesis, or future owning tool | Treat them as runtime guidance | Maintenance and coupling without demonstrated behavior | `non-runtime`; reject new machinery until observed failure |

## Residual Unavoidable Complexity

The local package necessarily carries one always-loaded description, two
authority modes, one compact condition for full-audit coverage, one ownership
boundary with `skill-creator`, one typed Return, and one disclosed behavioral
protocol. These mechanisms buy Codex discovery, mutation safety, pack
composition, and valid behavioral evidence that the explicit-only reference
baseline does not supply.

The design admits no additional helper, schema, ledger, template, reference,
generated trigger, line ceiling, or token ceiling. The behavioral protocol is
the largest proof load, but placing it behind one observable predicate keeps it
off the common path. Aggregate runtime load remains one compact instruction
surface plus the baseline glossary and one branch-only evaluation reference.

# Contract

## Admission And Authority

Invoke Writing Great Skills when the primary object is a Codex skill's
invocation, instructions, ownership, composition, context loading, leading
words, completion, pruning, or behavioral proof. General prompt rewriting,
ordinary code review, repository implementation, plugin scaffolding, and
post-edit delivery remain with their own owners.

Select one primary operation from the requested authority:

| Operation | Entry | Mutation | Return |
| --- | --- | --- | --- |
| **Audit** | Inspect, review, compare, explain, or design without write authority | None. Exact replacement wording remains advisory. | Verdict, impact-ordered findings, exact candidates when useful, deliberate non-changes, behavior at risk, and evidence limits. |
| **Author** | Create or edit an explicitly authorized canonical skill or skill-design artifact | Only the requested canonical package and smallest directly affected proof or relationship surfaces. | Changed canonical surfaces, behavior changed, proof, deliberate non-changes, and residual gaps. |

Any persisted artifact uses bounded Author authority. Authorizing a synthesis or
report does not authorize runtime edits. Authorizing canonical edits does not
authorize installation or delivery. Preserve unrelated work throughout.

A direct request to test whether wording changes behavior enters the read-only
behavior-proof branch. It does not create a third operation or grant canonical
mutation.

## Source And Coverage Resolution

Resolve the request, operation, canonical source, affected surfaces, current
upstream when relevant, relationships, and available evidence before judgment
or mutation.

Bounded work follows only surfaces capable of changing the requested
behavior. It still includes the canonical line, invocation policy when affected,
the disclosed target behind an affected pointer, each affected owner or
relationship, and the smallest relevant structural or behavioral proof.

A full audit inventories before judgment:

- every file in the canonical skill package, including policy, disclosed
  references, scripts, templates, assets, and schemas;
- current upstream and recorded upstream decisions;
- callers, routers, composers, handoffs, return consumers, and relationship
  records;
- every owned gate, output, mutation boundary, failure branch, and completion
  criterion;
- structural tests, behavioral fixtures, current evidence records, and known
  residual gaps; and
- documentation or setup surfaces that publish or route the canonical skill.

Installed mirrors and manifests are outside default source and coverage
resolution. Inspect them only
when the user explicitly requests installation-state evidence, report what is
observed, and leave repair to the installation owner.

An inventory is not completion. Mark each item `affected`, `preserve`, `owned
elsewhere`, `historical evidence`, `drift`, or `not applicable`. Classify each
relevant upstream difference as `keep local`, `adapt`, `adopt`, `reject`, or
`defer`. A full audit refreshes upstream rather than trusting an old checkout,
package label, or transcript.

## Single Ownership

Give each behavior one owner for its rule, admission predicate, authority,
inputs, outputs, evidence, failure return, and completion. Another surface may
name only its own trigger, expected outcome, and return boundary.

Check every relationship through four facts:

| Fact | Requirement |
| --- | --- |
| Callee | Name the skill or reference that owns the behavior. |
| Trigger | State the observable condition that selects it. |
| Authority | Preserve the owner's output, mutation, and completion authority. |
| Return | State what comes back and where the caller resumes or stops. |

Use the pack's accepted relationship verbs: `Load`, `Invoke`, `Compose`, `Hand
off`, and `Recommend and stop`. Routers select one next skill or `none` and stop.
Do not copy relationship catalogs into runtime skills.

The `skill-creator` relationship is an ownership boundary, not an invitation to
duplicate its scaffolding workflow. Writing Great Skills may judge the resulting
canonical instructions; it does not absorb initialization or metadata-generation
mechanics owned by the bundled creator.

## Discoverable Contract

Make the applicable outcome, boundary and authority, current action or branch,
Return, and completion criterion discoverable. These are behavior obligations,
not a named surface, mandatory headings, or a fixed order. Linear procedures,
routers, composers, state machines, templates, and flat reference keep the
form their behavior needs. Authority must precede mutation and proof must
follow the candidate it evaluates; no other universal sequence is admitted.

Treat an implicitly invocable description as an always-loaded routing
predicate. Name observable request or caller triggers, add the closest
exclusion only when an adjacent false positive needs separating, and omit
explicit-name reach, runtime procedure, and body-summary detail. Each distinct
trigger must select a real branch rather than rename another trigger.

Keep common-path steps and compact universal reference in `SKILL.md`. Put
branch-only reference behind a pointer that names both the target and the
observable condition for loading it. Co-locate a concept's definition, rule,
caveat, and failure consequence. Split a skill only for independent invocation,
irreducible branch load, or observed premature completion that survives a
sharper local completion criterion.

The compact full-audit inventory is the one justified inline branch: the
condition is explicit, the checklist is shorter than a new reference plus its
pointer and ownership contract, and full-audit omission would weaken the
promised coverage. Reopen this exception only if observed context competition
or maintenance drift makes disclosure cheaper.

Use a leading word only when it recruits a useful prior, changes behavior
against the current default, and stays precise at each use. Prefer established
language, define ambiguity once, repeat the word rather than its explanation,
and test behavior in realistic context. Decorative metaphors, generic quality
adjectives, and synonyms without distinct gates are no-op candidates.

## Behavior-Preserving Pruning

Apply behavior-preserving cuts in this order:

1. Protect non-intuitive mechanics, semantic and safety rules, authority,
   required outputs and proof, irreversible sequencing, safe failure actions,
   and completion criteria.
2. Restore single ownership before deleting duplicated foreign behavior.
3. Remove stale exposition and disclose live branch-only material.
4. Ask, "If I cut this, what behavior changes?" Delete the sentence when the
   answer is none.
5. Collapse repeated meaning into one rule and intentional emphasis into a
   leading word.
6. Co-locate, disclose, or split remaining sprawl only when the earlier cuts
   preserve behavior.
7. State the positive target first; keep negation only for a necessary hard
   guardrail paired with the safe action.

Line count, word count, headings, and validator tokens are not pruning verdicts.
ADR 0004 keeps semantic language judgment outside mechanical validation.

## Claim-Matched Proof

Use the lowest evidence that proves the claim:

| Claim | Required evidence |
| --- | --- |
| Exact bytes, links, policy, or parser-consumed fields | Read-back and focused structural checks. |
| Ownership or composition | Caller/callee trace and representative relationship workflow. |
| Wording changes invocation, judgment, action, context loading, Return, or completion | Counterfactual evaluation through `BEHAVIOR-EVALS.md`. |
| Canonical package is coherent | Relevant focused tests, skill validation, diff checks, and changed-file read-back. |

`BEHAVIOR-EVALS.md` alone owns Diagnose, Control, Sample, Stress, Judge, and
Record mechanics. The runtime skill states only the predicate for loading it and
the required result. Register defect correction or quality lift before
sampling. When a realistic control exhibits neither the expected defect nor a
meaningful pre-registered quality deficit, reject the guidance as a no-op
candidate.

Writing Great Skills owns evidence independence: fixed task evidence and
rubrics, fresh contexts when sampling, no candidate leakage into controls, and
root-held judgment. Ambient collaboration policy owns whether and how workers
are dispatched.

Proof stops at canonical quality. Name skipped checks and residual risk, then
return. Do not install, synchronize, publish, stage, commit, or push.

## Return And Completion

Audit returns `complete`, `partial`, or `blocked`; resolved authority and
coverage; verdict; impact-ordered findings; exact candidates when useful;
deliberate non-changes; behavior at risk; and evidence limits.

Author returns `complete`, `partial`, or `blocked`; canonical files changed;
behavior added, changed, or removed; structural, relationship, and behavioral
proof; preserved unrelated state; deliberate non-changes; and residual risk.

Complete only when the selected operation's coverage is accounted for; every
affected invocation surface, owner, relationship, pointer, gate, output,
mutation boundary, Return, and completion criterion has one classified home;
current upstream differences are decided; claimed relationships and behavior
have proportionate current evidence; canonical checks pass or skips are named;
unrelated work is preserved; and the Return states the actual terminal
condition without extrapolating into installation or delivery.

# Evidence And Extraction

## Decision Evidence

| Evidence | Design consequence | Limit |
| --- | --- | --- |
| Current canonical package | Preserve Predictability, compact disclosure, pruning discipline, source-first canonical edits, explicit Audit/Author authority, and typed Return. | Canonical bytes and structural checks do not prove the behavioral gaps below. |
| `CONTEXT.md` and relationship map | Keep vocabulary, runtime, synthesis, and relationship owners separate. | The `skill-creator` boundary is indexed; broader caller coverage still needs scenario evidence. |
| ADR 0004 | Keep language quality under judgment and behavioral proof. | Mechanical tests cannot prove semantic quality. |
| Structural contract tests | Preserve implicit policy, disclosed references, and machine-consumed or deliberately literal contracts. | Literal assertions protect wording and shape, not agent behavior or admission. Current canonical description assertions outran this synthesis; treat them as canonical-only structural evidence, not experimental design authority. |
| Core fixtures 28, 46, and 51 | Preserve evidence independence, pruning counterfactuals, and counterfactual instruction forms. | Only fixture 28 has inspected historical live-child evidence. |
| 2026-07-13 validation transcript | Preserve bounded independent evidence and then-current validation facts. | Its runtime and hashes predate the promoted rewrite. |
| Upstream HEAD `ed37663cc5fbef691ddfecd080dff42f7e7e350d`, inspected 2026-07-21 | Retain Predictability, information hierarchy, split pressure, leading words, no-op pruning, and positive targets as the simplest credible baseline. | Its user-invoked policy and all-reference runtime target a different environment. |
| Promoted concise canonical package | Preserve useful Audit/Author authority, authoring behaviors, typed Return, and canonical-only completion as evidence for extraction. | Current bytes do not automatically admit the exact five-word spine, named semantic surface, fixed order, or later un-synthesized wording. |
| 2026-07-21 authoring-boundary evaluation | Accept the `skill-creator` scaffolding boundary, Writing Great Skills semantic ownership, and canonical stop for the tested new-package scenario. | One 5-by-5 scenario does not prove Audit, invocation recall, existing-skill rewriting, or cross-model stability. |
| Confirmed Deploy Prompt 1 packet, 2026-07-21 | Admit implicit discovery and the trigger-only description as required local contracts; retain semantic roles while deferring the exact spine mnemonic, named surface, and fixed role order. | Participant confirmation settles design and caller contracts, not behavioral effectiveness. |
| Deploy Prompt 4 evaluation, 2026-07-21 | Accept metadata routing at 45/45, the full-package candidate at 55/55 versus upstream's 10/55, and pruning equivalence at 25/25 per arm. | Inactive metadata routing and action sequences were simulated; canonical integration, installation, and delivery remain later proof. |

Current upstream classification:

- keep or adapt Predictability, information hierarchy, observed split pressure,
  leading-word collapse, no-op pruning, and positive targets;
- adapt upstream invocation concepts to Codex's `implicitly invocable` and
  `explicit-only` vocabulary and `policy.allow_implicit_invocation` mechanics;
  reject upstream `model-invoked`, `user-invoked`, and
  `disable-model-invocation` as local runtime terms;
- adopt one distinct description trigger per real branch;
- reject upstream's explicit-only policy and all-reference runtime shape; and
- treat examples as evidence, not runtime obligations.

## Deliberate Non-Changes And Rejections

- Keep one `SKILL.md`, one glossary, one behavioral-evaluation reference, and
  one invocation policy file.
- Keep implicit invocation as a required local caller contract; explicit-only
  conversion would remove ordinary natural-language discovery.
- Keep the description trigger-only. Do not let runtime procedure, explicit
  name reach, or body-summary detail consume its routing surface.
- Keep outcome, authority, applicable action, Return, and completion
  discoverable without imposing a named semantic surface or fixed order.
- Keep the five authoring behaviors, but do not protect the exact
  `Trace -> Own -> Shape -> Prune -> Prove` mnemonic or sequence as an
  independently admitted behavior.
- Keep behavioral mechanics in `BEHAVIOR-EVALS.md`; do not restate them in the
  synthesis or runtime skill.
- Keep durable authoring concepts in `GLOSSARY.md`; do not add operation, proof,
  mutation, or Return procedure.
- Add no helper, schema, ledger, generated trigger, semantic duplication lint,
  line ceiling, or token ceiling without observed recurring failure.
- Keep generic delegation mechanics outside the skill.
- Keep installation, mirrors, manifests, promotion, publishing, and Git delivery
  outside the skill and outside its default source and coverage resolution.
- Do not copy `skill-creator` scaffolding instructions into this package.
- Do not synchronize experimental or installed drift as part of synthesis or
  canonical skill authoring.

Deferred hypotheses remain the exact five-word spine as a behavior-changing
mechanism, the `Semantic Skill Surface` name, a fixed semantic-role order,
explicit-only conversion, separate Audit and Author skills, machine-readable
evaluation records, per-model no-op profiles, automatic trigger or
context-pointer scoring, semantic duplication detection, and a pack-wide
inventory helper. Reject a universal heading template and any new helper,
schema, ledger, or reference without an observed failure. Adopt a deferred
hypothesis only after a fixed control shows a recurring failure and the
candidate removes more variance than complexity it adds.

## Extraction Ownership

| Surface | Promoted canonical delta | Must not absorb |
| --- | --- | --- |
| `SKILL.md` | Defines strict Audit and bounded Author; carries the admitted authoring behaviors without treating their current labels or fixed sequence as a mechanism; makes outcome, authority, applicable action, Return, and completion discoverable; shapes the trigger-only description; returns typed canonical-only completion. | The deferred five-word mnemonic or fixed semantic-role order, glossary definitions, experiment procedure, scaffolding, relationship catalog, installation, or delivery. |
| `GLOSSARY.md` | Carries only accepted durable authoring concepts and failure modes. Preserve Codex's `implicitly invocable` / `explicit-only` vocabulary and `policy.allow_implicit_invocation` mechanics rather than copying upstream runtime terms. The experimental candidate must remove the `Semantic Skill Surface` name and fixed-order requirement while preserving any admitted underlying meaning in `SKILL.md`. | Upstream `model-invoked`, `user-invoked`, or `disable-model-invocation` as local mechanics; runtime steps; operation contracts; proof procedure; Return packets; temporary candidate wording; or a renamed replacement for the deferred surface. |
| `BEHAVIOR-EVALS.md` | Owns complete counterfactual mechanics, defect-correction and quality-lift controls, invocation and premature-completion diagnoses, contamination controls, record fields, and evidence-independence rules. | Canonical editing, generic worker mechanics, installation, or language ontology. |
| `agents/openai.yaml` and frontmatter | Set Codex `policy.allow_implicit_invocation: true` and preserve concise create/edit, audit/review, and behavioral-proof triggers. | Upstream `disable-model-invocation`, runtime workflow, or output procedure. |
| Relationship map | Indexes the `skill-creator` scaffolding versus semantic-quality boundary once. | Copied owner procedures or invented invocation. |
| Tests and evaluation fixtures | During Prompt 3, update structural proof only for machine-consumed policy, metadata, links, and schemas; record semantic obligations for Prompt 4 instead of encoding them as prose assertions. Keep canonical literal tests untouched during extraction. If promotion later changes their owned runtime, replace prose-coupled protection for the deferred exact spine, named surface, fixed order, or unproved wording with the least brittle structural or behavioral evidence appropriate to the admitted contract. | Prompt 3 structural assertions for semantic behavior; claims that strings prove behavior or admission; or claims that installation belongs to this skill. |
| `CONTEXT.md` and ADR 0004 | No change unless a later rewrite changes durable vocabulary or artifact ownership. | Skill-local procedure or candidate wording. |
| Installer, manifests, installed mirror, publishing, and Git | No change during the Author phase. Promotion lifecycle and managed installation continue only under their separate authority. | Writing-quality judgment or canonical authoring authority. |

The earlier pre-Deploy promotion record from 2026-07-21 remains historical
evidence. Deploy Prompts 1 and 2 supersede its exact-spine and named-surface
decisions for this promoted candidate while preserving the admitted operations,
behaviors, references, policy, ownership, and Return. Follow
[`deploy-prompts.md`](../methods/deploy-prompts.md) for later
rewrites. Installation and delivery never enter the authoring order.

## Promotion Acceptance Obligations

Prompt 4 assessed these obligations against the inactive candidate. Promotion
must preserve them while moving the accepted bytes onto the canonical surface:

1. create/edit, audit/review, and direct behavioral-proof prompts invoke the
   skill without false-firing on general prompts, code review, plugins, or
   delivery work;
2. the description selects observable request or caller triggers, uses the
   nearest necessary exclusion, and carries no explicit-name reach, runtime
   procedure, or body-summary detail;
3. Audit remains read-only and exact suggestions grant no mutation authority;
4. Author changes only the requested canonical skill and directly affected
   proof or relationship surfaces;
5. new-package scaffolding stays with `skill-creator`, while semantic judgment
   for both new and existing skills stays with Writing Great Skills;
6. full-audit coverage accounts for every canonical, disclosed, upstream, relationship,
   test, evaluation, and routing surface without requiring mirror inspection;
7. source and authority resolution, single ownership, discoverable outcome and
   authority, behavior-preserving pruning, and claim-matched proof remain
   behaviorally complete without relying on the exact five-word mnemonic,
   `Semantic Skill Surface` name, or fixed semantic-role order;
8. glossary concepts, runtime operations, evaluation mechanics, collaboration
   policy, and delivery mechanics each have one owner;
9. no-op, duplicated meaning, branch disclosure, and safety preservation pass
   positive and negative cases;
10. behavioral claims load `BEHAVIOR-EVALS.md`, run uncontaminated controls and
   candidates, and record variance and residual gaps;
11. canonical structural and relationship checks pass, unrelated work is
    preserved, and Return stops before installation or delivery.

## Prompt 4 Behavioral Acceptance

The refreshed upstream remained
`ed37663cc5fbef691ddfecd080dff42f7e7e350d`. Prompt 4 independently challenged
every admitted mechanism, froze the expanded pre-prune package at
`208491d50213134b0190143e7928319dcba2ddc0313e47539df068f8593e52af`,
reperformed the instruction-unit cut audit, and accepted final candidate hash
`9822b2eb486e7e4a31589cd02a0667981639ef3c2df810da3d6945f6e650f77c`.

Commit preflight then removed one trailing blank line from each of two support
files and corrected the frozen fixture's UTF-8 representation. No instruction,
gate, pointer, policy, or rubric changed. The current candidate hash is
`c7c02f4f9896cd5bf6e6c25886e77785a9f80c0ccea0d02f7aaa6fc85076dcc4`;
the current pre-prune fixture hash is
`23fb951a230df6c929803f02d3ad16586471a14f4169632eddaf39c725c34bc2`.

Fresh-context evidence established:

- metadata-level routing: upstream 25/45 versus candidate 45/45, with all four
  positive natural-language families and all five adjacent negatives stable
  across five contexts;
- full-package behavior: upstream 10/55 versus candidate 55/55 for typed Audit
  and Author returns, source and ownership resolution, the `skill-creator`
  boundary, full-audit classifications, conditional mirror handling, and
  counterfactual proof; and
- pruning equivalence: 25/25 fixed cases for both the admitted pre-prune
  control and final candidate, with zero observed critical failures.

The evaluation record is
[`2026-07-21-writing-great-skills-post-candidate-behavior-eval.md`](../../validation/transcripts/2026-07-21-writing-great-skills-post-candidate-behavior-eval.md).
The exact five-word mnemonic, `Semantic Skill Surface` name, and fixed role
order remain unadmitted; no sampled failure justified a helper, schema, ledger,
template, new reference, generated trigger, or ceiling.

## Prompt 5 Promotion Evidence

Prompt 5 read back the accepted experimental and promoted canonical trees at
the same hash,
`c7c02f4f9896cd5bf6e6c25886e77785a9f80c0ccea0d02f7aaa6fc85076dcc4`.
The canonical package retained the accepted four-file shape. Its policy file
now follows the repository's default LF contract, so the obsolete active-
baseline CRLF exception was removed from `.gitattributes` without changing
policy meaning.

Canonical proof passed 59 focused skill-pack contract tests, direct custom-skill
validation, and diff checks. The managed-install preview reported only
`writing-great-skills` updated and 24 managed skills unchanged. The scoped
install skipped the unchanged global bootstrap, installed 25 managed skills,
and source-to-installed validation and direct tree-hash comparison passed.

The first parallel full-suite run had one unrelated empty-subprocess-output
failure in a Parallel Implement helper test. That exact test passed serially,
and a fresh full-suite rerun passed 191 tests with 4 skips. The transient result
does not affect the promoted package but remains recorded rather than hidden.

## Remaining Integration Gaps

- Metadata routing was simulated during Prompt 4. Canonical policy, package,
  reference, and relationship structure now have promotion-time proof; live
  host discovery remains unobserved.
- Fixed cases simulated action sequences and terminal packets rather than
  mutating representative skill packages.
- The grouped Audit case proved strict read-only behavior and typed Return but
  did not add a separate contradictory-authority stress wave; that additional
  ten-context study was disproportionate after the broader suite passed.
- Exact model, reasoning, token, and timing telemetry was unavailable and must
  not be inferred.

## Promotion Readiness

Decision: `promoted-canonical-and-installed`.

Prompt 5 promoted the accepted bytes without changing their tree hash and
replaced prose-coupled protection for the deferred exact spine and named
surface with package, policy, reference, and relationship checks. After the
canonical Author Return, the separately owned lifecycle retired the
experimental copy and manifest entry, ran the managed installer, and proved
source-to-mirror parity. No promotion-blocking integration gap remains. Git
delivery remains unauthorized.
