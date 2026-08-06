# To Spec Deploy Prompt 1 — Frozen M0

Campaign epoch: `2026-07-24-to-spec`

Operation: blind intent audit under `writing-great-skills`

Starting Git HEAD: `f3be70c31dd8f2ae9f12a75248065ef313790bda`

Blindness boundary: the target runtime, target synthesis, experimental target,
target-specific historical evaluations and transcripts, upstream packages,
promotion records, and outside research were not inspected. Current-runtime
identity and current-versus-M0 shape are intentionally unknown.

Ambient unrelated state, preserved without inspection:

- starting untracked
  `docs/validation/transcripts/2026-07-24-convergent-pr-review-prompt1-m0.md`;
- concurrently appeared `.scratch/`; and
- concurrently appeared untracked
  `docs/validation/transcripts/2026-07-24-review-prompt1-m0.md`.

<!-- M0-DECISION-CONTENT:START -->

## Intended Contract

### Outcome

`to-spec` turns one bounded packet of settled source into one durable parent
specification in the target repository's configured issue tracker. The
specification preserves source-owned commitments and becomes the intent owner
that `to-tickets` can later slice. The skill synthesizes, checks, publishes,
reads back, and returns the specification; it does not deliver the work.

### Invocation and exclusions

- Invocation is explicit-only.
- Admit a request only when settled source needs a durable parent spec.
- The source may be a direct settled packet, a closed Wayfinder map and its
  decisive resolutions, or a verified selected improvement candidate whose
  direction and commitment boundary are settled.
- Exclude conversational shaping, unresolved multi-decision wayfinding,
  source research, raw request triage, implementation-ticket slicing,
  implementation, parent delivery, review, installation, and Git delivery.
- A missing or incompatible setup surface returns a setup precondition and
  recommends `$repo-bootstrap`; no tracker or draft mutation begins.
- A decision-bearing source gap or conflict returns a source-gap packet; the
  skill does not answer a user-owned product decision.

### Authority

- The user and supplied settled source own outcome, commitments, acceptance,
  scope, exclusions, public and data contracts, security/privacy posture, and
  agreed product tradeoffs.
- Repository instructions, routed domain material, and ADRs own local
  vocabulary and durable decisions.
- The engineering contract owns Source Trace, bounded-slice,
  commitment-boundary, proof-seam, evidence, and state-boundary semantics.
- `codebase-design` supplies module, interface, seam, adapter, depth,
  leverage, and locality vocabulary only. `to-spec` retains artifact,
  publication, Return, and completion ownership; vocabulary loading does not
  authorize a direct design decision.
- `to-spec` owns faithful synthesis, coverage judgment, one disposable draft,
  one parent-spec publication, mutation verification, and its typed Return.
- The configured tracker contract owns transport, durable location,
  relationship mechanics, and Mutation read-back.
- `to-tickets` owns later implementation slicing, blocker order, readiness,
  and child publication. A parent spec contains no fabricated ready-ticket
  graph.

### Caller and relationship obligations

- Skill Router routes “settled source needs a durable parent spec” to
  `$to-spec` and stops.
- Wayfinder recommends `$to-spec` only after closure has produced settled
  parent-spec source; the closed map and decisive resolutions remain source
  pointers.
- Improve Codebase may recommend `$to-spec` for one verified `Concentrate`
  candidate whose settled direction needs a durable parent specification
  before slicing; its report, candidate identity, Source Trace, resolution
  evidence, commitment boundary, proof seam, limits, and overlap disposition
  remain inputs.
- On verified success, recommend `$to-tickets` and stop without invoking it.
- On setup incompatibility, recommend `$repo-bootstrap` and stop without
  tracker mutation.
- Parent-spec intent remains authoritative after child tickets exist.

### Safe failure Return

Return exactly one of:

1. `setup-precondition`: missing or incompatible routed setup, named evidence,
   unchanged tracker and draft state, and `$repo-bootstrap`.
2. `source-gap`: missing, inaccessible, ambiguous, or contradictory
   decision-bearing source, affected contract fields, unchanged tracker state,
   and the exact decision owner.
3. `existing-state-conflict`: the requested creation would duplicate,
   overwrite, or ambiguously reconcile durable state; observed identity,
   unchanged state, and the smallest authorization or source delta needed.
4. `publication-recovery`: applied and failed operations, draft identity,
   observed durable state, affected relationships, and the safest recovery
   that does not repeat an unknown mutation.
5. `published-spec`: verified durable pointer, source identity, coverage
   result, mutation read-back, residual gaps, and `$to-tickets` as the one next
   recommendation.

No failure Return claims publication when durable bytes, location, or
relationships are unknown or mismatched.

### Completion, order, compatibility, and safety

The irreversible order is:

```text
setup gate
-> complete source and repository trace
-> settledness and target-state gates
-> commitment coverage
-> disposable draft
-> draft read-back
-> one configured publication
-> durable mutation read-back
-> draft cleanup or named preservation
-> Return and stop
```

Completion requires one settled bounded source identity; every source-visible
commitment and boundary accounted for; one internally consistent parent spec;
one verified configured publication or an exact typed non-success Return;
unrelated state preserved; and no downstream owner started.

Compatibility includes GitHub issues, GitLab issues, and Local Markdown
`.scratch/<feature-slug>/SPEC.md` through the configured tracker contract.
Creation is the minimum supported transition. Updating or reconciling an
existing parent spec requires an explicitly identified target and explicit
authority; otherwise the safe result is `existing-state-conflict`.

The spec may describe security, privacy, migration, rollback, operability, and
irreversible implementation obligations, but `to-spec` performs none of those
effects. It publishes only the parent specification. It neither changes
domain truth nor invents public-contract choices.

## State-Location Ledger

| State or artifact | Owner | Authoritative location | Allowed transition | Required order | Read-back | Failure Return |
| --- | --- | --- | --- | --- | --- | --- |
| Supplied settled source | Source owner | User packet and every decision-bearing pointer it names | Read-only; identity captured | After setup gate, before drafting | Reopen every pointer and verify identity/sufficiency | `source-gap` |
| Routed setup contracts | Repository / `repo-bootstrap` | `AGENTS.md` and routed tracker, labels, domain, and engineering docs | Read-only | First | Verify required surfaces and operations exist and agree | `setup-precondition` |
| Domain language and decisions | Domain owners | Routed `CONTEXT.md`, `CONTEXT-MAP.md`, and applicable ADRs | Read-only | Before terminology and contract drafting | Trace every adopted term or decision to its owner | `source-gap` for conflict; no domain mutation |
| Existing parent-spec target | Configured tracker | GitHub/GitLab issue or Local Markdown `SPEC.md` when one is named or discovered for the same source | Read-only discovery; create only when absent; reconcile only with explicit authority | Before draft is approved for publication | Refetch/read the observed target and identity | `existing-state-conflict` |
| Disposable draft | `to-spec` | One ignored `.tmp/to-spec/<feature-slug>.md` file | Absent -> create -> revise in memory/file -> delete after verified publish; preserve exactly on uncertain publication | After all source gates, before durable mutation | Read exact draft bytes and run coverage checks | `source-gap` before publish; `publication-recovery` after attempted publish |
| GitHub parent spec | Tracker contract / `to-spec` publication | One GitHub issue body and comments | Absent -> one created issue; no label or child mutation required by M0 | After draft read-back | Refetch body, comments, labels/state, relationships, and open status | `publication-recovery` |
| GitLab parent spec | Tracker contract / `to-spec` publication | One GitLab issue description and notes | Absent -> one created issue; no label or child mutation required by M0 | After draft read-back | Refetch description, notes, labels/state, relationships, and open status | `publication-recovery` |
| Local Markdown parent spec | Tracker contract / `to-spec` publication | `.scratch/<feature-slug>/SPEC.md` | Absent -> create directory/file; later tracker owners may add ordered child links | After draft read-back | Reread exact file, state metadata if any, and relationships | `publication-recovery` |
| Child tickets and delivery state | `to-tickets` and delivery owners | Configured tracker child locations | No transition by `to-spec` | Only after a later explicit invocation | Not applicable in M0 | Stop after recommending `$to-tickets` |
| Git index, commits, remote code, installed skills | Git/delivery owners | Repository index, object database, remotes, installed mirror | No transition | Outside this skill | Confirm unchanged only when relevant to the invocation | Typed failure; never stage, commit, push, or install |

## Semantic Behavior Units

| Unit | Observable behavior and owner | Local authority | Cheapest neutral expression | Entry case | Wrong-condition case | Failure Return | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M0-01 | Admit only explicit settled-source-to-parent-spec work | Skill Router and invocation policy | One positive predicate plus closest exclusions | User explicitly requests a durable parent spec from settled source | Source is raw, disputed, or already sliced for delivery | `source-gap` or out-of-scope Return | Invocation fixtures and policy parse |
| M0-02 | Load and verify the routed setup surface before mutation | `AGENTS.md`, tracker/domain/setup owners | One setup gate with owner pointers | Required surfaces and publication operation exist | Tracker or routed contract is absent/incompatible | `setup-precondition` | Missing/present setup fixtures |
| M0-03 | Read the complete supplied packet and decision-bearing pointers | Source Trace contract | One exhaustive read gate | Direct packet, closed Wayfinder map, or selected-candidate packet is accessible | Pointer is missing, stale, inaccessible, or partial | `source-gap` | Source identity and pointer-coverage fixtures |
| M0-04 | Fix one bounded source identity and one intended parent-spec target | Bounded-slice and tracker contracts | Record source owner, identity, bound, and target mode | Exactly one source and new target are unambiguous | Multiple sources/targets or unclear update intent | `source-gap` or `existing-state-conflict` | Identity/read-back fixture |
| M0-05 | Inspect applicable durable state before creating | Tracker Mutation read-back and state-boundary contract | Query/read only the relevant parent target | No existing parent is present | Matching, divergent, or unknown existing parent exists | `existing-state-conflict` unless explicit reconciliation authority exists | Absent/same/divergent/unknown state cases |
| M0-06 | Build a commitment ledger without changing source-owned meaning | Commitment-boundary contract | Account for each commitment, exclusion, deferral, and open note once | Source decisions are settled and consistent | A missing/conflicting choice changes contract or acceptance | `source-gap` | Bidirectional source-to-spec trace |
| M0-07 | Preserve routed domain terms and ADR decisions | Domain routing and ADR owners | Use accepted terms; point to owners | Applicable terms/decisions agree with source | Source contradicts an ADR or invents unresolved domain language | `source-gap` with conflict named | Term and ADR trace |
| M0-08 | Apply deep-module vocabulary without transferring authority | Relationship owner and `codebase-design` vocabulary contract | Load vocabulary only where interface shape is already settled | Spec needs interface/seam/module description | A new public or ownership design decision is required | `source-gap`; no direct design pass | Relationship trace and authority fixture |
| M0-09 | Draft one behavior-complete parent spec | `to-spec` ownership and downstream `to-tickets` contract | One structured document covering the minimum content fields below | Ledger is complete and no decision gap remains | Draft would fabricate a commitment, ticket graph, or implementation result | `source-gap` | Section-semantic and ledger coverage checks |
| M0-10 | Make acceptance and proof observable | Engineering proof contract and Ready-for-agent consumer contract | Pair each requirement with acceptance, edge/error cases, and proof seam/lane authority | Behavior can be observed or a structural proxy is honestly bounded | Acceptance asserts output existence only or extrapolates unrun proof | `source-gap` or explicit residual gap | Requirement/acceptance/proof trace |
| M0-11 | Cover stateful compatibility and lifecycle obligations proportionately | State-boundary matrix contract | Include distinct supported branches and high-risk interactions only | Persistence, migration, compatibility, cache, session, or lifecycle state matters | Blind Cartesian matrix or missing material branch | `source-gap` | State-boundary coverage audit |
| M0-12 | Freeze and read back one disposable draft before publication | Relationship map `.tmp/to-spec` boundary and work-state contract | Write once, reread exact bytes, correct only synthesis defects | Draft is complete and publication-authorized | Draft path is not ignored/safe or bytes cannot be verified | `setup-precondition` or `source-gap`; no durable mutation | Exact-byte read-back and ignored-path check |
| M0-13 | Publish exactly one parent spec through configured transport | Tracker transport owner | Invoke only the configured create operation with frozen title/body | New GitHub, GitLab, or local target is absent and authorized | Transport differs, target is existing/unknown, or mutation authority is absent | `existing-state-conflict` or `publication-recovery` | Transport-specific mutation fixture |
| M0-14 | Verify the entire durable mutation and affected relationships | Tracker Mutation read-back | Refetch/reread created parent and compare intended state | Creation reports success | Any body, location, state, or relationship is unknown/mismatched | `publication-recovery` | Post-mutation exact semantic comparison |
| M0-15 | Preserve recovery evidence without repeating uncertain mutation | Tracker partial-mutation contract | Report applied/failed operations and keep exact draft | Publication is partial, failed, or unverifiable | Retrying might duplicate the parent | `publication-recovery` | Fault-injection/partial-state fixture |
| M0-16 | Reconcile disposable state after verified publication | Work-state policy | Delete verified draft; otherwise name preserved path and reason | Durable publication matches | Publication state is uncertain | `publication-recovery` with draft retained | Draft existence/read-back check |
| M0-17 | Return verified parent identity and stop at the owner boundary | Relationship owner | One typed result and one recommendation | Publication and cleanup/reconciliation are verified | Child slicing or delivery is requested in same run | `published-spec`, recommend `$to-tickets`, stop | Return-shape and no-successor checks |

## Runtime-Clause Specification

| Clause | Runtime requirement | Units |
| --- | --- | --- |
| C01 | Description names explicit settled-source parent-spec creation and excludes slicing or delivery | M0-01 |
| C02 | Setup gate loads routed tracker, labels, domain, and engineering owners; missing/incompatible setup returns `$repo-bootstrap` before mutation | M0-02 |
| C03 | Source gate reads the full supplied packet and every decision-bearing pointer, records identity/owner/bound, and rejects missing or conflicting commitment decisions | M0-03, M0-04, M0-06 |
| C04 | Existing-state gate distinguishes absent, same, divergent, and unknown parent targets; creation proceeds only from verified absence | M0-05 |
| C05 | Domain clause preserves routed vocabulary and ADRs without writing domain truth | M0-07 |
| C06 | Architecture clause loads `codebase-design` vocabulary only for already-settled module/interface meaning and retains spec ownership | M0-08 |
| C07 | Commitment clause accounts once for every requirement, exclusion, deferral, constraint, dependency, risk, and nonblocking open note | M0-06, M0-09 |
| C08 | Spec-content clause includes source identity and owner; problem/outcome; users/scenarios; scope and non-goals; requirements and invariants; interfaces/data/state; edge/error behavior; security/privacy; compatibility/migration/rollback; operability; dependencies/risks; acceptance and proof; decisions/deferrals/residual gaps; and downstream boundary | M0-09, M0-10, M0-11 |
| C09 | Acceptance clause maps observable criteria and proof authority to each commitment and names structural proxies and residual risk honestly | M0-10 |
| C10 | Stateful clause derives only applicable initial, reusable, legacy/incompatible, access-path, variant, and lifecycle branches | M0-11 |
| C11 | Draft clause uses one ignored `.tmp/to-spec/<feature-slug>.md`, freezes it, and reads exact bytes before publication | M0-12 |
| C12 | Publication clause delegates one create operation to the configured GitHub, GitLab, or Local Markdown contract; no child, label, implementation, Git, or domain mutation is added | M0-13 |
| C13 | Verification clause applies complete Mutation read-back and compares the durable parent to the frozen draft and intended relationships | M0-14 |
| C14 | Recovery clause reports exact partial state and preserves the draft when publication is not fully verified; it never blindly retries | M0-15, M0-16 |
| C15 | Success clause cleans disposable state, returns the verified parent pointer and coverage evidence, recommends `$to-tickets`, and stops | M0-16, M0-17 |
| C16 | Completion clause requires all units applicable to the selected branch and forbids success from an unknown durable state | M0-01 through M0-17 |

The runtime may arrange these clauses differently, but must preserve the
stated order, owners, branches, and observable Returns.

## Clause-to-Intent Cut Audit

Every retained clause maps to the viability floor or a required relationship:

| Clauses | Required intent |
| --- | --- |
| C01-C04 | Invocation, source authority, bounded slice, safe existing-state handling |
| C05-C06 | Domain and architecture ownership contracts |
| C07-C10 | Behavior-complete parent-spec outcome and downstream consumer needs |
| C11-C14 | Durable-state order, mutation safety, read-back, and recovery |
| C15-C16 | Completion and relationship Return |

The following behaviors are outside M0 and must not be imported merely because
another source or current runtime contains them:

- eliciting or choosing unsettled product intent;
- performing outside research or creating more than the one later-authorized
  research note;
- running a direct codebase-design pass or deciding a new public interface;
- writing `CONTEXT.md`, `CONTEXT-MAP.md`, or ADR truth;
- generating child tickets, dependencies, readiness labels, implementation
  profiles, or delivery plans owned by `$to-tickets`;
- triaging, implementing, reviewing, closing a parent, installing, staging,
  committing, or pushing;
- copying GitHub, GitLab, or Local Markdown transport procedures into the
  runtime instead of pointing to the configured owner;
- requiring labels or category roles for the parent when no local contract
  requires them;
- claiming implementation proof from a specification-time structural proxy;
- automatically reconciling or overwriting an existing parent spec.

## Complete M0 Viability Suite

| Case | Required observation | Units |
| --- | --- | --- |
| V01 Direct settled packet, GitHub | One issue created from complete source, exact body refetched, `$to-tickets` recommended, no child created | M0-01-M0-17 |
| V02 Direct settled packet, GitLab | One issue created and exact description/notes/state read back | M0-01-M0-17 |
| V03 Direct settled packet, Local Markdown | One `.scratch/<feature-slug>/SPEC.md` created and reread; no issue files created | M0-01-M0-17 |
| V04 Closed Wayfinder source | Map destination, decisive resolutions, scope, exclusions, and source links trace into the parent; Wayfinder state is unchanged | M0-03, M0-06, M0-09 |
| V05 Selected improvement candidate | Candidate identity, settled direction, commitment boundary, proof seam, limits, and overlap disposition trace into the parent | M0-03, M0-06, M0-09 |
| V06 Explicit-only invocation | Direct invocation admits; an adjacent raw request is not silently executed as `to-spec` | M0-01 |
| V07 Missing setup | Returns `setup-precondition`, recommends `$repo-bootstrap`, creates neither draft nor tracker item | M0-02 |
| V08 Inaccessible decision pointer | Returns `source-gap` with exact missing pointer and affected fields; no mutation | M0-03 |
| V09 Unsettled material choice | Names decision owner and affected commitments; does not choose or publish | M0-06 |
| V10 ADR/domain conflict | Names both authorities and the conflict; does not rewrite domain truth or publish | M0-07 |
| V11 New interface decision required | Uses vocabulary to expose the gap but does not run a direct design pass or fabricate the choice | M0-08 |
| V12 Existing matching parent | Returns verified existing identity or conflict according to explicit request authority; never duplicates | M0-05 |
| V13 Existing divergent parent | Returns `existing-state-conflict` with observed identity and required reconciliation authority; no overwrite | M0-05 |
| V14 Unknown target state | Treats timeout/permission ambiguity as unknown and performs no create retry | M0-05, M0-15 |
| V15 Coverage omission | Draft audit catches an unaccounted commitment, exclusion, error case, or proof obligation before publication | M0-06, M0-09-M0-12 |
| V16 Stateful behavior | Applicable initial/current/legacy/access/variant/lifecycle branches appear without a Cartesian checklist | M0-11 |
| V17 Publication reports failure before creation | Returns exact failed operation, unchanged observed state, and preserved draft | M0-15, M0-16 |
| V18 Publication succeeds but read-back mismatches | Returns `publication-recovery`, reports observed delta, preserves draft, and does not claim success | M0-14-M0-16 |
| V19 Publication result is indeterminate | Reports unknown durable state and safe inspection action; does not repeat create | M0-15 |
| V20 Verified success | Durable content and relationships match, disposable draft is removed, parent pointer and source identity return | M0-14-M0-17 |
| V21 Same-run request includes slicing | Parent publication may complete, but `$to-tickets` is only recommended and remains unstarted | M0-17 |
| V22 Unrelated work present | Only the draft and configured parent target change; unrelated worktree/tracker state remains exact | M0-12-M0-16 |

Behavioral fixtures must keep source facts, authority, initial state, configured
tracker, requested output, and mutation boundary worker-visible. Expected
branches and judgments remain evaluator-owned.

## Local Source Identity Manifest

All identities are SHA-256 of repository bytes at starting HEAD unless marked
as working-tree evidence.

| Source | Identity | Use and authority classification |
| --- | --- | --- |
| `AGENTS.md` | `d93d25a1e8bf09f01fb9eee054682940539a072c5f489e99435dbe6e10cde314` | Commands, pointers, preservation, unit boundary |
| `CONTEXT.md` | `bae0de4372439edc96e91c5132967755797bc4628c8b2fef03591b6779fde8e1` | Pack vocabulary, artifact ownership, active/experimental separation |
| `README.md` | `dc630154d9c2d61124c93c6cd6ae4af5b1b813fb50bd661e47cc0af7456c0bcb` | Human-facing outcome sequence and shaping-to-delivery boundary |
| `docs/agents/engineering-contract.md` | `c3d52491ca8b98f229965e2602212fc4474ef2fedf8be73bc8f08c24300ef829` | Source Trace, commitments, proof, state, Lock |
| `docs/agents/issue-tracker.md` | `d79c8dbdc0e3c77583b461ac2d50eb678d0ce77aed69a9e759e3c0818646f933` | Current GitHub transport and work-item lifecycle |
| `docs/agents/triage-labels.md` | `06f253d31ea852376950b4b8c163f2a1e60c5be131492b3cb76d05be92b58ded` | Role mapping; confirms no mandatory parent category/state assignment |
| `docs/agents/domain.md` | `94ccdc414542b44be2fe38d7ebe2e59fd809c09848642243c3a805749c6adb99` | Domain/ADR routing |
| `docs/adr/0001-agents-primes-contract-teaches-skills-execute.md` | `eb0ca5b54a8dbdd35a2fd170734006460e7f7a5a0f93ad8ce29264c8bcc76b75` | Setup docs point; skill executes |
| `docs/adr/0003-skills-encode-local-contract-slices.md` | `5c043765d4679a272e096fa492b0b52b71f4c519216e98630e11031149177f34` | Runtime carries only its local contract slice |
| `docs/adr/0007-synthesis-preserves-exhaustive-research-runtime-skills-compress.md` | `a8b37fa83c820a08bf0e10998e1301d537cefa5d797b49edcabbb308644c8962` | Checkpoint preserves decisions; later runtime compresses |
| `docs/synthesis/skill-context-relationships.md` | `15bb4ab6cd4cda5256b45aae4c7bb887a153f62cc63dbd2203d0f3b68ea1ad69` | Relationship owner, `.tmp` draft boundary, caller/callee Returns |
| `skills/custom/skill-router/SKILL.md` | `2bbf8e9c2b9c0c86d8aa3abff2a66bdfb946a9a120dbff3d5d640966398d7c05` | Explicit route predicate |
| `skills/custom/skill-router/agents/openai.yaml` | `3bf863a8856d04a6a1c4f23b3aae6cbf5388544129662c55cc733c2d9c23bbbf` | Explicit-only relationship evidence |
| `skills/custom/wayfinder/SKILL.md` | `83f47a00f50032480d82f3c35597907d23959bf2fc4d035fa2b327dbf82e831e` | Closed-map caller contract |
| `skills/custom/wayfinder/MAP-FORMAT.md` | `129affae265dbde7f54b4978218269a2bfdab69f41dbd9f3940482615a791d91` | Caller packet structure |
| `skills/custom/wayfinder/agents/openai.yaml` | `a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94` | Caller invocation policy |
| `skills/custom/improve-codebase/SKILL.md` | `ed2a156e0a92af9ea46dedcf47a63596346976333f7b59705b5bc066fef3b23b` | Selected-candidate caller boundary |
| `skills/custom/improve-codebase/SELECTED-CANDIDATE.md` | `d8795dc6209422bbd9d7678f9e32ccff915e87fa0b907fb163306de4d3066b50` | Specification-ready candidate packet |
| `skills/custom/to-tickets/SKILL.md` | `27355fa8228231ead0062581f565394a570414012e6ac11afb311e97aef0c7b9` | Downstream consumer contract and ownership exclusions |
| `skills/custom/to-tickets/agents/openai.yaml` | `a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94` | Explicit-only downstream policy |
| `skills/custom/codebase-design/SKILL.md` | `9fb50c72294242702d461d8db128353b65f463ca08b23727e3fbf66a69656c64` | Loaded vocabulary and retained caller authority |
| `skills/custom/repo-bootstrap/issue-tracker-github.md` | `d79c8dbdc0e3c77583b461ac2d50eb678d0ce77aed69a9e759e3c0818646f933` | Portable GitHub state/transport contract |
| `skills/custom/repo-bootstrap/issue-tracker-gitlab.md` | `b2306fc978d12a17658f30bf48a5e80e3f28407e1daa904d03298a0ba463e709` | Portable GitLab state/transport contract |
| `skills/custom/repo-bootstrap/issue-tracker-local.md` | `4c8c31836b0e6428e51eb8b169b9126b1f905ed4988d5cc116c766d8bbe51e36` | Portable Local Markdown state/transport contract |
| `tests/test_skill_pack_contracts.py` | `9ac7bd84b30e33fa10c198b94f34338ddf31e477c7088e375cee51a742d4ea1f` | Existing local evidence only: explicit policy, publication/read-back, relationship, and broad content-shape checks; not intent authority |

Starting repository identity:
`f3be70c31dd8f2ae9f12a75248065ef313790bda`.

## Limitations

- Blindness prevents current-runtime identity, current behavior disposition,
  current compatibility inspection, and current-versus-M0 comparison.
- No professional method, upstream package, outside research, target
  synthesis, promotion record, or target historical evaluation was inspected.
- The configured repository uses GitHub, so GitLab and Local Markdown
  compatibility are authority-derived but were not executed in this unit.
- This checkpoint specifies behavior and proof; it does not materialize or
  behaviorally evaluate M0.
- Existing tests were inspected only as local evidence. Current-target wording
  asserted by tests has no M0 authority by existence.
- Exact connector/API mutation schemas are transport-owned and must be
  verified when M0 is materialized and evaluated.
- Reconciliation of an existing parent spec is intentionally outside the
  creation minimum until explicit target and mutation authority are supplied.

## Research Questions by Intended Behavior

### Admission and source fidelity

- Which established specification practices best preserve source-owned
  commitments while exposing unresolved decisions instead of silently filling
  them?
- What evidence distinguishes a decision-complete source packet from a merely
  detailed but unsettled one?

### Specification completeness and usability

- Which parent-spec information fields most reliably support later vertical,
  dependency-aware ticket slicing without importing implementation technique?
- How should requirements, invariants, edge/error behavior, exclusions,
  acceptance, and proof seams be cross-traced with the least reader burden?
- What counterpressure warns against exhaustive templates that encourage
  irrelevant sections or false precision?

### Interfaces, state, compatibility, and risk

- What professional guidance supports describing already-settled interface,
  data, lifecycle, migration, rollback, security, privacy, and operability
  obligations without turning the spec into an implementation design?
- When is a state-boundary matrix useful in a parent spec, and what conditions
  keep it proportionate?

### Durable publication and recovery

- What established patterns prevent duplicate durable records when create
  operations time out or return indeterminate state?
- What is the minimum decision-ready recovery packet after a partial tracker
  mutation?

### Completion and downstream handoff

- What qualities make a parent spec sufficiently decision-complete for a
  separate ticket-slicing owner while keeping open nonblocking notes and
  residual risk honest?
- Which completion language best prevents the spec owner from drifting into
  ticket generation or implementation?

Authorized research-note path:
`docs/research/skills/to-spec/RP-to-spec-20260724-01.md`

## Checkpoint Integrity and Re-entry

Re-entry must verify:

1. Git HEAD remains
   `f3be70c31dd8f2ae9f12a75248065ef313790bda`.
2. Every manifest source retains its recorded identity.
3. The bounded content retains the fingerprint recorded below.
4. The blindness boundary remains intact until the Research Pass starts.
5. Any admitted intended-contract decision changes only its named units,
   clauses, viability cases, and dependent questions; unexpected authority or
   identity drift requires a fresh blind Prompt 1.

M0 is implementable from C01-C16 without research, current-only behavior, or
evaluator conclusions.

## Prompt 1 Decision

Decision: `ready-for-research`

Campaign shape: `undetermined` because current, exact M0 runtime, and H1 have
not been inspected or materialized.

Runtime identities: checkpoint only; M0/H1/V1/P1 byte identities do not yet
exist.

Proof outline: complete source identity read-back, checkpoint marker and
fingerprint verification, affected Markdown integrity, repository skill
validation, both diff checks, and unchanged HEAD.

Residual gaps are the research questions and limitations above; none prevents
an unambiguous neutral M0 runtime.

<!-- M0-DECISION-CONTENT:END -->

Content fingerprint algorithm: SHA-256 of the exact UTF-8 bytes strictly
between the marker lines, including the newline immediately after the start
marker and immediately before the end marker.

Content fingerprint:
`b19edb0b03a176b0e4f903c001f1705587d04a4306bbd05be8c3d625d3f7a726`

## Shared Run Contract Return

Authorized unit completed: Deploy Prompt 1 — Freeze M0 for `to-spec`

Decision: `ready-for-research`

Campaign shape: `undetermined`

Runtime identities: M0 checkpoint fingerprint
`b19edb0b03a176b0e4f903c001f1705587d04a4306bbd05be8c3d625d3f7a726`;
exact runtime identities not materialized

Artifacts changed:
`docs/validation/transcripts/2026-07-24-to-spec-prompt1-m0.md`

Evidence used or reused: local intent authorities and relationship owners in
the source identity manifest; existing contract tests as local evidence only;
no behavioral evidence reused

Residual gaps: research clusters and limitations recorded above

Recommended next unit: Deploy Research Pass for `to-spec`

Git HEAD: `f3be70c31dd8f2ae9f12a75248065ef313790bda` ->
`f3be70c31dd8f2ae9f12a75248065ef313790bda`

Git delivery: pending

Exact stop reason: Prompt 1 checkpoint frozen; Research Pass not started.
