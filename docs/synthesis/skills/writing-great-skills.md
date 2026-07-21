# Writing Great Skills Design Synthesis

Status: selected design promoted to canonical runtime on 2026-07-21. This
document remains design and evidence, not runtime authority.

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

`docs/synthesis/methods/source-to-skill-flow.md` owns rewrite cadence. This
synthesis owns the selected design and its acceptance obligations, not a second
implementation runbook.

The evidence snapshot is the working tree inspected on 2026-07-20 and refreshed
through the 2026-07-21 authoring-boundary evaluation and canonical promotion.
The accepted concise package now lives under
`skills/custom/writing-great-skills/`; the dated evaluation remains bounded
promotion evidence.

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
| Invocation | Keep implicit invocation and front-load distinct create/edit, audit/review, and behavioral-proof triggers. |
| Package | Keep one short `SKILL.md`, one authoring glossary, one behavioral-evaluation reference, and one policy file. |
| Operations | Use `Audit` for strictly read-only judgment and `Author` for explicitly authorized canonical persistence. |
| Spine | Use `Trace -> Own -> Shape -> Prune -> Prove`. Select the operation before the spine. |
| Behavioral evaluation | Make counterfactual evaluation a triggered `Prove` branch, not a peer operation. A direct evaluation request may enter that branch without authoring authority. |
| Vocabulary | Keep `GLOSSARY.md` limited to durable authoring concepts and failure modes. |
| Proof | Match proof to the claim and stop after canonical structural, relationship, and behavioral evidence. |
| Delegation | Own independence requirements for evidence, not permission or mechanics for dispatching workers. |
| Growth | Add no helper, schema, ledger, template, or new reference until observed variance proves the current package insufficient. |

The local design intentionally differs from upstream. Upstream remains source
pressure, not runtime authority. This pack needs Codex-specific invocation,
single-owner composition, canonical editing, and counterfactual proof; it does
not need to copy upstream invocation policy or runtime shape.

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
`Prove` branch. It does not create a third operation or grant canonical mutation.

## Trace

Resolve the request, operation, canonical source, affected surfaces, current
upstream when relevant, relationships, and available evidence before judgment
or mutation.

A bounded Trace follows only surfaces capable of changing the requested
behavior. It still includes the canonical line, invocation policy when affected,
the disclosed target behind an affected pointer, each affected owner or
relationship, and the smallest relevant structural or behavioral proof.

A full Trace inventories before judgment:

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

Installed mirrors and manifests are outside default Trace. Inspect them only
when the user explicitly requests installation-state evidence, report what is
observed, and leave repair to the installation owner.

An inventory is not completion. Mark each item `affected`, `preserve`, `owned
elsewhere`, `historical evidence`, `drift`, or `not applicable`. Classify each
relevant upstream difference as `keep local`, `adapt`, `adopt`, `reject`, or
`defer`. A full audit refreshes upstream rather than trusting an old checkout,
package label, or transcript.

## Own

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

## Shape

Expose the applicable semantic roles in this order:

```text
Outcome
Boundary and authority
Operation or branch
Steps or peer reference
Return
Completion
```

These are semantic roles, not mandatory headings. Linear procedures, routers,
composers, state machines, templates, and flat reference keep the form their
behavior needs.

Keep common-path steps and compact universal reference in `SKILL.md`. Put
branch-only reference behind a pointer that names both the target and the
observable condition for loading it. Co-locate a concept's definition, rule,
caveat, and failure consequence. Split a skill only for independent invocation,
irreducible branch load, or observed premature completion that survives a
sharper local completion criterion.

Use a leading word only when it recruits a useful prior, changes behavior
against the current default, and stays precise at each use. Prefer established
language, define ambiguity once, repeat the word rather than its explanation,
and test behavior in realistic context. Decorative metaphors, generic quality
adjectives, and synonyms without distinct gates are no-op candidates.

## Prune

Prune in this order:

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

## Prove

Use the lowest evidence that proves the claim:

| Claim | Required evidence |
| --- | --- |
| Exact bytes, links, policy, or parser-consumed fields | Read-back and focused structural checks. |
| Ownership or composition | Caller/callee trace and representative relationship workflow. |
| Wording changes invocation, judgment, action, context loading, Return, or completion | Counterfactual evaluation through `BEHAVIOR-EVALS.md`. |
| Canonical package is coherent | Relevant focused tests, skill validation, diff checks, and changed-file read-back. |

`BEHAVIOR-EVALS.md` alone owns Diagnose, Control, Sample, Stress, Judge, and
Record mechanics. The runtime skill states only the predicate for loading it and
the required result. When a realistic no-guidance control does not exhibit the
claimed failure, reject the guidance as a no-op candidate.

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
| Structural contract tests | Preserve implicit policy, disclosed references, and format-neutral semantic roles. | Literal assertions protect wording and shape, not agent behavior. |
| Core fixtures 28, 46, and 51 | Preserve evidence independence, pruning counterfactuals, and counterfactual instruction forms. | Only fixture 28 has inspected historical live-child evidence. |
| 2026-07-13 validation transcript | Preserve bounded independent evidence and then-current validation facts. | Its runtime and hashes predate the promoted rewrite. |
| Upstream inspected 2026-07-20 | Retain Predictability, information hierarchy, split pressure, leading words, no-op pruning, and positive targets. | Its user-invoked policy and all-reference runtime target a different environment. |
| Promoted concise canonical package | Realize the selected Audit/Author operations, five-word spine, typed Return, and canonical-only completion in the active package. | Promotion does not prove untested behavioral claims. |
| 2026-07-21 authoring-boundary evaluation | Accept the `skill-creator` scaffolding boundary, Writing Great Skills semantic ownership, and canonical stop for the tested new-package scenario. | One 5-by-5 scenario does not prove Audit, invocation recall, existing-skill rewriting, or cross-model stability. |

Current upstream classification:

- keep or adapt Predictability, information hierarchy, observed split pressure,
  leading-word collapse, no-op pruning, and positive targets;
- adopt one distinct description trigger per real branch;
- reject upstream's explicit-only policy and all-reference runtime shape; and
- treat examples as evidence, not runtime obligations.

## Deliberate Non-Changes And Rejections

- Keep one `SKILL.md`, one glossary, one behavioral-evaluation reference, and
  one invocation policy file.
- Keep implicit invocation; explicit-only conversion still lacks evidence and a
  replacement discovery path.
- Keep semantic roles format-neutral rather than imposing a universal template.
- Keep behavioral mechanics in `BEHAVIOR-EVALS.md`; do not restate them in the
  synthesis or runtime skill.
- Keep durable authoring concepts in `GLOSSARY.md`; do not add operation, proof,
  mutation, or Return procedure.
- Add no helper, schema, ledger, generated trigger, semantic duplication lint,
  line ceiling, or token ceiling without observed recurring failure.
- Keep generic delegation mechanics outside the skill.
- Keep installation, mirrors, manifests, promotion, publishing, and Git delivery
  outside the skill and outside its default full Trace.
- Do not copy `skill-creator` scaffolding instructions into this package.
- Do not synchronize experimental or installed drift as part of synthesis or
  canonical skill authoring.

Deferred experiments remain explicit-only conversion, separate Audit and Author
skills, machine-readable evaluation records, per-model no-op profiles,
automatic trigger or context-pointer scoring, semantic duplication detection,
and a pack-wide inventory helper. Adopt one only after a fixed control shows a
recurring failure and the candidate removes more variance than complexity it
adds.

## Extraction Ownership

| Surface | Promoted canonical delta | Must not absorb |
| --- | --- | --- |
| `SKILL.md` | Defines strict Audit and bounded Author; uses `Trace -> Own -> Shape -> Prune -> Prove`; exposes sharp glossary and behavioral-proof predicates; returns typed canonical-only completion. | Glossary definitions, experiment procedure, scaffolding, relationship catalog, installation, or delivery. |
| `GLOSSARY.md` | Carries only accepted durable authoring concepts and failure modes. | Runtime steps, operation contracts, proof procedure, Return packets, or temporary candidate wording. |
| `BEHAVIOR-EVALS.md` | Owns complete counterfactual mechanics, invocation and premature-completion diagnoses, contamination controls, record fields, and evidence-independence rules. | Canonical editing, generic worker mechanics, installation, or language ontology. |
| `agents/openai.yaml` and frontmatter | Preserve explicit implicit-invocation policy and concise create/edit, audit/review, and behavioral-proof triggers. | Runtime workflow or output procedure. |
| Relationship map | Indexes the `skill-creator` scaffolding versus semantic-quality boundary once. | Copied owner procedures or invented invocation. |
| Tests and evaluation fixtures | Protect operation discovery, authority, pointers, semantic role order, pruning, proof predicates, and canonical-only completion. | Claims that strings prove behavior or that installation belongs to this skill. |
| `CONTEXT.md` and ADR 0004 | No change unless a later rewrite changes durable vocabulary or artifact ownership. | Skill-local procedure or candidate wording. |
| Installer, manifests, installed mirror, publishing, and Git | No change. They remain outside this design and its completion. | Writing-quality judgment or canonical authoring authority. |

The 2026-07-21 promotion resolved the `SKILL.md` operation and spine, reconciled
the two owned references, and updated only affected policy, relationships,
tests, and evaluation evidence. Follow
[`source-to-skill-flow.md`](../methods/source-to-skill-flow.md) for later
rewrites. Installation and delivery never enter the authoring order.

## Promotion Acceptance Obligations

Promotion does not erase the remaining evidence gaps. The runtime remains
subject to these acceptance obligations:

1. create/edit, audit/review, and direct behavioral-proof prompts invoke the
   skill without false-firing on general prompts, code review, plugins, or
   delivery work;
2. Audit remains read-only and exact suggestions grant no mutation authority;
3. Author changes only the requested canonical skill and directly affected
   proof or relationship surfaces;
4. new-package scaffolding stays with `skill-creator`, while semantic judgment
   for both new and existing skills stays with Writing Great Skills;
5. full Trace accounts for every canonical, disclosed, upstream, relationship,
   test, evaluation, and routing surface without requiring mirror inspection;
6. `Trace -> Own -> Shape -> Prune -> Prove` remains discoverable and each word
   changes a distinct decision or action;
7. glossary concepts, runtime operations, evaluation mechanics, collaboration
   policy, and delivery mechanics each have one owner;
8. no-op, duplicated meaning, branch disclosure, and safety preservation pass
   positive and negative cases;
9. behavioral claims load `BEHAVIOR-EVALS.md`, run uncontaminated controls and
   candidates, and record variance and residual gaps;
10. canonical structural and relationship checks pass, unrelated work is
    preserved, and Return stops before installation or delivery.

## Remaining Evidence Gaps

- No current fixed study proves the two-operation selector or that each word in
  the five-word spine independently changes behavior.
- No current study proves the revised invocation description improves recall
  without adjacent false positives.
- The 2026-07-21 study supports canonical-only Author completion in one
  new-package scenario; strict Audit and broader authority leakage remain
  unproved.
- No current negative-control scenario proves the behavioral-evaluation pointer
  loads only at the `Prove` predicate.
- The 2026-07-21 study supports the `skill-creator` boundary for a new package;
  no current scenario proves it for an existing-skill rewrite.
- Current independent-sample evidence for the promoted runtime is limited to the
  bounded authoring-boundary study; the remaining design claims lack current
  behavioral evidence.
- Runtime telemetry may remain unavailable; future records must state the gap
  rather than invent it.

A later claim of full behavioral acceptance requires current, proportionate
evidence for every obligation, no critical behavioral regression, passing
canonical checks and read-back, preserved unrelated work, and a truthful Return
that stops before installation and delivery.
