# To Tickets Deploy Campaign: Prompt 1 M0 Checkpoint

- Skill: `to-tickets`
- Unit: Deploy Prompt 1
- Audit operation: `$writing-great-skills` Audit
- Campaign epoch: `2026-07-25`
- Starting Git `HEAD`: `8752406cf437629787c2abec5f66c3c0e6eda8b1`
- Historical incumbent authority: commit `b2df62a1879ffe4c5624656f63712c723fcdb44a`; not read in Prompt 1
- Authorized research-note path: `docs/research/to-tickets-deploy-2026-07-25.md`
- Prompt 1 decision: `ready-for-research`

The content strictly between the markers below is the immutable Prompt 1 stage
capsule. Its identity is the SHA-256 digest of those exact UTF-8 bytes,
including the first and last newline inside the markers.

<!-- BEGIN TO-TICKETS PROMPT-1 M0 CAPSULE -->

## Intended Contract

### Outcome

On explicit invocation, turn one settled, bounded, authoritative source into
one verified, exhaustive, dependency-ordered graph of one or more
Ready-for-agent implementation tickets through the configured tracker. Each
ticket is an independently completable bounded slice with enough Source Trace,
acceptance, proof, scope, state, and execution-profile information for its
implementation owner. Preserve source commitments, publish no false-ready
frontier, return one typed result, recommend exactly one delivery owner only
after verified success, and stop without implementation or delivery.

### Invocation and exclusions

`to-tickets` is explicit-only. Admit a user or caller that explicitly selects
the skill and supplies one settled source whose remaining work is ticket
creation, repair, or dependency ordering.

Closest exclusions:

- unsettled outcome, acceptance, commitment, public or data contract,
  security or privacy posture, migration policy, or scope belongs to its
  source or shaping owner;
- durable parent-spec synthesis belongs to `to-spec`;
- raw incoming classification and verification belong to `triage`;
- one already selected Ready-for-agent item belongs to `implement`;
- delivery of an existing exhaustive parent-backed graph belongs to
  `parallel-implement`;
- implementation, review, tracker closeout, installation, Git delivery, and
  domain-truth mutation remain outside this skill.

### Authority

- The user and settled source own outcome, commitments, acceptance, scope,
  exclusions, supported states, public and data contracts, security and
  privacy posture, compatibility, migration, rollback, and agreed tradeoffs.
- `to-tickets` owns source coverage, implementation slicing, ticket boundaries,
  dependency order, graph completeness, ticket execution profiles, frozen
  publication packets, configured tracker publication, mutation read-back,
  recovery evidence, Return, and completion.
- The configured tracker contract owns transport, parent/child and blocking
  mechanics, label or state mapping, ready-frontier semantics, claims,
  closeout, and Mutation read-back.
- The engineering contract owns the meanings of Source Trace, bounded slice,
  commitment boundary, proof seam, proof lane, tracer bullet, semantic proof,
  state-boundary matrix, residual risk, and safe mutation boundaries.
- `triage` owns incoming classification and verification. A valid
  `to-tickets` result is already Ready-for-agent and is not retriaged except
  for an explicit state or brief correction.
- `implement` and `parallel-implement` own delivery. They may return an
  incomplete or contradictory ticket or graph as a repair packet; that packet
  supplies evidence but does not override source authority.
- Domain and ADR owners retain domain truth. Setup ownership remains with
  `repo-bootstrap`.

### Accepted source forms

Accept one exact, identity-bearing settled source, including:

- a verified parent specification;
- a direct settled packet with enough commitment authority to create one or
  more implementation items;
- one verified selected improvement candidate whose direction, commitment
  boundary, and multi-slice need are settled;
- one verified audit finding or cohesive cluster whose remediation intent is
  settled and for which only slicing remains; or
- one exhaustive repair packet from an implementation consumer, reconciled
  against its original source.

A source may be parent-backed or direct. Do not require a parent when local
caller contracts admit a direct settled source. A direct graph cannot qualify
for parent-delivery routing unless an authoritative parent relationship is
later supplied.

### Safe failure Return

Return exactly one of:

- `setup-precondition`: required tracker, label, domain-routing, or engineering
  setup is missing or incompatible; state is unchanged and
  `$repo-bootstrap` is the one recommendation;
- `source-gap`: source identity, authority, commitment coverage, supported
  state, acceptance, dependency meaning, or another source-owned fact is
  missing, ambiguous, inaccessible, or contradictory; name affected fields,
  exact owner, and unchanged tracker state;
- `existing-state-conflict`: target state is divergent, ambiguous, claimed,
  partially authored by another actor, or cannot be reconciled without
  authority; return observed identities and the smallest needed authorization
  or source delta without mutation;
- `publication-recovery`: an authorized tracker transition failed, was
  partial, was indeterminate, or mismatched read-back; return the frozen graph
  identity, every applied and failed operation, exact observed items and
  relationships, current ready frontier, and the safest configured recovery
  action; never repeat an indeterminate create; or
- `ready-graph`: every gate and read-back passes for either a newly published
  graph or a byte-and-semantics-matching existing graph.

On `ready-graph`, return source and parent identities, graph identity, ordered
ticket pointers, dependency edges, ready frontier, per-ticket execution
profiles and state matrices, publication or reuse read-back, residual gaps,
and exactly one next recommendation. Recommend `implement` with the first
ready ticket in tracker order by default. Recommend `parallel-implement` only
when the user explicitly requested a top-level parent-delivery run and the
verified graph is non-empty, exhaustive, Ready-for-agent, and parent-backed.

### Completion and irreversible order

Complete only when setup and source authority resolve; every in-scope
commitment maps to the graph; every ticket satisfies the Ready-for-agent
contract; dependencies are acyclic and yield a non-empty frontier; applicable
state matrices and execution profiles are complete; the target state was
reconciled; every authorized transition was read back; no false-ready or
duplicate item remains; unrelated state is preserved; and one typed Return is
supported by observed state.

The mutation order is:

1. read setup, source, target parent, related children, dependency
   relationships, labels or states, claims, and current frontier;
2. freeze and validate the complete ticket graph and exact publication plan
   before any durable mutation;
3. verify that the invocation or an explicit follow-up authorizes the exact
   configured tracker transition;
4. create missing child packets in a recoverable non-ready state, or use one
   configured atomic graph operation when it provides equivalent proof;
5. read back each unique create before another operation could duplicate it;
6. attach and verify parent/child and dependency relationships;
7. verify coverage, acyclicity, ordering, packet bytes or normalized
   semantics, and the derived frontier while children remain non-ready;
8. activate Ready-for-agent state in dependency order and read back each
   transition; and
9. refetch the complete affected graph and verify bodies, relationships,
   labels or states, claims, comments, open/closed status, and final frontier.

If the configured tracker cannot provide a recoverable non-ready or atomic
publication route, return `setup-precondition` before creation. A failed
relationship transition leaves created items non-ready. A failed readiness
transition returns the exact safe or exposed frontier and performs no
unverified compensation.

## State-Location Ledger

| State or artifact | Owner and authoritative location | Allowed transition | Required order and read-back | Failure Return | M0 unit and viability case |
| --- | --- | --- | --- | --- | --- |
| Setup surface | Repository `AGENTS.md` and routed `docs/agents/*` owners | Read only | Verify compatibility before source or tracker mutation | `setup-precondition` | M02; V02 |
| Settled source | Supplied parent, packet, selected-candidate report, audit item, or repair packet at its exact supplied location | Read and identity-freeze only | Read complete decision-bearing source and pointers before graph design; preserve authority | `source-gap` | M03-M04; V03-V05 |
| Existing parent and related graph | Configured GitHub or GitLab connector, or Local Markdown `.scratch/` tracker | Read; reuse exact match; mutate only under exact authority | Inspect parent, children, relationships, roles, claims, and frontier before any create; full read-back | `existing-state-conflict` | M05; V06-V07 |
| Frozen graph and publication plan | Invocation-local immutable packet, identified by exact content digest | Freeze before durable mutation; no hidden delta after authority | Validate coverage, tickets, edges, profiles, matrices, and operations before publish | `source-gap` or unchanged prepublication failure | M06-M13; V08-V13 |
| Newly created connector tickets | Configured tracker child-item locations | Verified absence to recoverable non-ready item; never repeat unknown create | Create only after graph freeze; refetch exact ID, body, metadata, and state immediately | `publication-recovery` | M14; V14 |
| Local Markdown ticket files | `.scratch/<feature>/issues/*.md` under the configured Local Markdown tracker | Verified absence to non-ready files, then verified Ready-for-agent content | Read back exact files and affected parent/dependents after each transition | `publication-recovery` | M14-M17; V17 |
| Parent/child relationships | Native tracker relationship or configured fallback parent task list and child parent pointer | Add only frozen relationships; reconcile no unrelated parent content | All children exist and read back before relationship mutation; refetch both ends | `publication-recovery` | M15; V15 |
| Dependency relationships | Native blocking links or configured `Blocked by` representation | Add only frozen DAG edges | Create endpoints first; verify every edge and derived frontier before readiness | `publication-recovery` | M10, M15; V08, V15 |
| Ready-for-agent state | Mapped tracker label or Local Markdown status on each child | Recoverable non-ready to `ready-for-agent` after graph verification | Activate after all bodies and relationships verify; refetch each item and frontier | `publication-recovery` | M16-M17; V16, V19 |
| Category role | Mapped tracker label or Local Markdown category, when settled by source | Apply exactly the source-settled role; do not invent one | Apply with final packet and read back; absence is preserved when source does not settle it | `source-gap` if required authority is contradictory; otherwise `publication-recovery` | M08, M16; V18 |
| Worktree | Repository worktree; mutation applies only for configured Local Markdown tracker files | Connector mode: unchanged. Local Markdown: only frozen tracker-file delta | Read back status and exact authorized paths; preserve unrelated work | `publication-recovery` or `existing-state-conflict` | M14, M21; V17, V20 |
| Git index and committed tree | Repository Git index and current `HEAD` | No transition | Verify unchanged before Return | `publication-recovery` | M21-M22; V17, V20 |
| Git remote | Not applicable; issue-tracker connector is not Git delivery | No transition | No push, PR, merge, or deployment | `publication-recovery` if an unauthorized effect occurred | M21; V20 |

## Semantic Behavior Unit Ledger

| ID | Behavior and local authority | Cheapest neutral expression | Entry case | Wrong-condition case | Failure Return | Proof |
| --- | --- | --- | --- | --- | --- | --- |
| M01 | Explicit-only invocation; relationship owner and invocation map | Run only when the user explicitly selects `to-tickets` for settled implementation slicing | Explicit skill selection plus settled source | Implicit discovery, raw triage, one ready item, or existing graph delivery | Do not invoke; name the owning route | Metadata policy and fixed routing fixtures |
| M02 | Setup gate; `repo-bootstrap`, repository primer, tracker, label, domain, and engineering owners | Verify the configured setup can create, relate, label, and read back work items before mutation | Compatible GitHub, GitLab, or Local Markdown setup | Missing owner, operation, mapping, marker, or read-back | `setup-precondition` with unchanged state | Complete setup-owner trace and incompatible/missing fixture |
| M03 | Source admission; user, source owner, `to-spec`, selected-candidate, and audit finding contracts | Accept one exact settled bounded source whose remaining work is slicing | Verified parent spec or other admitted settled packet | Missing identity, inaccessible pointer, unsettled decision, or incompatible repair packet | `source-gap` with affected fields and owner | Complete source read-back and admitted/rejected form fixtures |
| M04 | Commitment authority; user, source, domain, ADR, and engineering owners | Preserve every source-owned commitment and choose only implementation technique | Slice choices stay within commitments | Any slice would choose outcome, public contract, security posture, migration policy, or scope | `source-gap`; no tracker mutation | Bidirectional source-to-graph trace and ADR/domain consistency check |
| M05 | Target-state reconciliation; tracker Mutation read-back contract | Distinguish verified absence, exact reusable graph, divergence, and unknown state | Absent or exact matching target | Conflicting child, claim, relationship, partial graph, or uncertain prior create | `existing-state-conflict`; no new create | Full parent/child/relationship/claim/frontier read-back |
| M06 | Exhaustive commitment ledger; source and tracker Ready-for-agent contract | Account once for every in-scope requirement, exclusion, deferral, dependency, risk, and proof obligation | Every commitment maps to one or more tickets or graph-level fence | Omitted, duplicated, contradicted, or ownerless commitment | `source-gap` when authority is missing; otherwise correct before publish | Bidirectional commitment coverage matrix |
| M07 | Slice judgment; engineering contract and Triage Ready brief owner | Prefer independently completable vertical behavior slices; admit support or migration slices only with observable value and proof | One behavior can be implemented and judged within its fence | File-choreography tasks, speculative scaffolding, cross-owned slice, or arbitrary microtasking | Correct locally; `source-gap` only for source-owned uncertainty | Deletion/cut audit plus independent-completion fixtures |
| M08 | Ticket packet; tracker Ready-for-agent contract plus `implement` caller contract | Give each ticket bounded slice, Source Trace, observable acceptance, dependency state, proof lane, expected write scope, parallel-safety note, scope fence, and preserved work-unit, learning, migration, verification, domain/ADR, edge/error, and exclusion facts when applicable | Complete packet supports one implementation Charter | Missing readiness field, fabricated category, unobservable acceptance, or proof below the useful seam | Correct locally or `source-gap` for missing authority | Required-field structural check and consumer relationship trace |
| M09 | Stateful work; engineering state-boundary matrix and Parallel Implement consumer | Record applicable initial/absent, reusable, legacy/incompatible, access-path, variant, lifecycle, and high-risk interactions without Cartesian padding | State affects correctness | Stateful ticket has no supported branches or invents unsupported variants | `source-gap` when supported states are unsettled | Matrix branch coverage fixture and `not applicable` control |
| M10 | Dependency graph; tracker blocking owner and `parallel-implement` | Freeze a complete acyclic graph with explicit blockers, ordered children, and a non-empty ready frontier | One or more tickets with valid partial order | Cycle, orphan, false blocker, hidden dependency, empty frontier, or closure that would create false readiness | Correct locally or `source-gap`; no publish while invalid | Graph structural check, edge read-back, frontier derivation cases |
| M11 | Per-ticket execution profile; `parallel-implement` Trace/Select contract | Record semantic ownership, expected production writes, proof seams and scarce proof resources, dependency order, overlap, serial tripwires, and inspectability | Every ticket and pair can be conservatively qualified | Independence is guessed from filenames, unspecified, or contradictory | Correct to serial/uncertain; `source-gap` for missing source fact | Pairwise profile matrix and downstream acceptance trace |
| M12 | High-risk ordering; engineering safety and `parallel-implement` | Put one production-path tracer first for protected data, permissions, trust, irreversible state, migrations, or cutovers; include retry, rollback, and partial-state proof | High-risk transition exists | Risk is parallelized or scheduled after dependent irreversible work without proof | `source-gap` when policy is unsettled; otherwise correct before publish | High-risk ordering fixture and required proof-field check |
| M13 | Mutation authority and frozen plan; user safety boundary | Freeze exact title/body/roles/relationships/order and require authority for that configured tracker transition | Explicit create/repair request covers exact plan | Read-only request, changed plan after authority, or unclear external-mutation scope | `existing-state-conflict` or exact authority request; unchanged state | Plan digest, authority trace, and no-mutation control |
| M14 | Recoverable creation; tracker transport owner | Create only verified-missing items in a recoverable non-ready state, reading each unique result back | Authorized absent graph and supported safe route | Target appears, create result is unknown, or connector lacks safe non-ready/atomic route | `publication-recovery` or pre-create `setup-precondition` | Absent/create/read-back case and indeterminate-create negative control |
| M15 | Relationship activation; tracker parent/child and blocking owner | Link verified endpoints exactly as frozen while all new children remain non-ready | Every endpoint exists with matching packet | Missing endpoint, relationship mismatch, partial native/fallback update | `publication-recovery`; preserve created non-ready items | Both-end relationship read-back and frontier check |
| M16 | Readiness activation; tracker role owner | Apply the mapped Ready-for-agent state only after bodies and graph relationships verify | Complete verified graph | Any packet or edge is unverified, claim exists, or activation partially fails | `publication-recovery` with exact exposed frontier | Pre-activation non-ready assertion and per-item state read-back |
| M17 | Full Mutation read-back; tracker contract | Refetch every affected item and dependent and verify bodies, relationships, roles, claims, comments, status, and resulting frontier | All planned operations report success or exact reuse | Partial, indeterminate, stale, or mismatched observable state | `publication-recovery` | Full graph read-back compared with frozen normalized semantics |
| M18 | Partial-state recovery Return; tracker safety contract | Stop on first unsafe or indeterminate transition and report exact applied, failed, and observed state without duplicate creates or invented rollback | Any publication failure | Continuing after unknown state or claiming atomic success from partial evidence | `publication-recovery` | Injected partial/unknown transition cases |
| M19 | Default delivery recommendation; relationship owner and `implement` admission | Recommend `implement` with the first dependency-ready ticket in tracker order | Verified graph without qualified explicit parent-delivery request | Recommending implementation before graph proof or selecting a blocked/later ticket | No success Return; correct recommendation | Ready-query ordering fixture |
| M20 | Conditional parent-delivery recommendation; relationship owner and `parallel-implement` admission | Recommend `parallel-implement` only for an explicitly requested top-level parent-delivery run over a verified exhaustive non-empty parent-backed graph | All named conditions hold | Direct graph, delegated request, generic desire for concurrency, incomplete graph, or no explicit delivery request | Recommend `implement` instead | Positive and closest-negative routing fixtures |
| M21 | Mutation boundary; relationship, tracker, and engineering owners | Change only configured tracker state; no code, domain truth, implementation, review, index, commit, remote, or delivery mutation | Connector or Local Markdown publication | Any unrelated path, Git index/commit, source, domain, or delivery effect | `publication-recovery` or blocked boundary report | Git/worktree/read-back and allowed-path comparison |
| M22 | Completion and typed Return; writing-great-skills completion vocabulary and caller contracts | Return one typed result only after every applicable gate closes; stop before delivery | Verified success, exact reuse, or supported safe failure | Narrative success without complete graph/read-back, multiple recommendations, or successor execution | Non-success typed Return with exact failed gate | End-to-end viability cases and successor-not-started assertion |

## Runtime-Clause Specification

| Runtime clause | Units | Neutral minimum expression |
| --- | --- | --- |
| Metadata and description | M01 | Explicitly split one settled bounded source into a verified dependency-ordered Ready-for-agent ticket graph; exclude shaping, triage, and delivery. Set implicit invocation to false. |
| Outcome, authority, and boundary | M04, M21 | State the one graph outcome, source-owned commitments, `to-tickets`-owned slicing/publication, foreign owners, and no implementation or Git delivery. |
| Admission and setup | M01-M03 | Require explicit selection, one admitted settled source, complete routed setup, and safe configured tracker operations. |
| Trace and reconcile | M03-M06 | Freeze source identity and authority, inspect exact target state, distinguish absence/match/divergence/unknown, and build bidirectional commitment coverage. |
| Slice and graph | M07-M12 | Produce complete independently completable ticket packets, applicable state matrices, a DAG and frontier, execution profiles, and high-risk order. |
| Freeze and publish | M13-M18 | Freeze an authority-matched plan, create recoverably, attach relationships before readiness, read back every transition, and stop safely on partial state. |
| Return and completion | M19-M22 | Return one typed packet, choose one qualified recommendation, prove the final graph or failure state, and start no successor. |

## Clause-to-Intent Cut Audit

### Kept

Every runtime clause above maps to the viability floor or one required local
caller, tracker, relationship, compatibility, or safety contract. In
particular, the execution profile and state matrix remain because
`parallel-implement` rejects a graph missing them, and recoverable
non-ready-first publication remains because tracker Mutation read-back and
false-frontier safety require it.

### Cut from M0

- No professional slicing methodology, ticket-size heuristic, scoring model,
  source-derived terminology, or current-runtime behavior is admitted before
  research and incumbent inspection.
- No requirement for a durable parent when a local caller admits a direct
  settled packet.
- No concurrency promise; the graph records evidence needed for later
  qualification and defaults uncertainty to serial delivery.
- No source shaping, research, prototype, design selection, implementation,
  formal review, closeout, deployment, installation, staging, commit, push,
  or successor execution.
- No duplicate tracker transport procedure beyond pointers and the local
  transition order that directly governs safe ticket publication.
- No category invention when the settled source does not own a category.
- No mandatory local draft file; an invocation-local frozen packet is enough
  unless the configured tracker requires a safe durable staging mechanism.
- No historical-incumbent preservation by existence and no current-body
  wording or package layout assumption.

## Complete M0 Viability Suite

| Case | Setup and input | Expected behavior and proof |
| --- | --- | --- |
| V01 Explicit invocation | Explicit `to-tickets` selection and settled verified parent spec | Admitted; no successor starts during slicing |
| V02 Setup incompatibility | Missing create, relationship, role, or read-back capability | `setup-precondition`; unchanged tracker; one `repo-bootstrap` recommendation |
| V03 Parent-backed source | Complete parent spec with several commitments | Every commitment maps bidirectionally; parent identity is preserved |
| V04 Direct settled source | Verified selected multi-slice improvement packet without a parent | Graph may publish without fabricated parent; parent-delivery route remains ineligible |
| V05 Source authority gap | Acceptance, supported state, security posture, or migration policy is contradictory or missing | `source-gap`; exact owner and affected tickets; no tracker mutation |
| V06 Exact existing graph | Existing children, packets, edges, roles, and frontier normalize to the frozen graph | `ready-graph` by reuse; no duplicate mutation |
| V07 Divergent or unknown state | Existing child differs, is claimed, or prior create result is unknown | `existing-state-conflict`; observed identities; no create |
| V08 Graph structure | Mixed independent and blocked slices | Complete DAG, ordered children, explicit edges, correct non-empty frontier |
| V09 Cycle or hidden dependency | Candidate graph cycles or omits a source-required dependency | No publish; correct locally or `source-gap` if source authority is needed |
| V10 Stateful slice | Correctness depends on absent, reusable, incompatible, access-path, and lifecycle state | Applicable state-boundary matrix is present and acceptance/proof cover each branch |
| V11 Stateless slice | State does not affect semantics | Explicit `not applicable`; no fabricated matrix branches |
| V12 High-risk transition | Protected data, trust, migration, cutover, or irreversible state exists | Production-path tracer precedes dependents and includes retry, rollback, and partial-state proof |
| V13 Execution overlap | Two tickets share semantic ownership, writes, proof resources, or a serial tripwire | Profile marks serial/uncertain; no concurrency claim |
| V14 Partial creation | One create succeeds and a later create is indeterminate | Created item remains non-ready; `publication-recovery` names exact ID and forbids duplicate retry |
| V15 Relationship failure | Children exist but a parent or dependency link fails | No readiness activation; both-end observations and safest repair returned |
| V16 Partial readiness | Relationships verify but one Ready-for-agent transition fails | `publication-recovery` with exact ready and non-ready sets and derived frontier |
| V17 Local Markdown | Configured tracker is `.scratch/` | Only frozen tracker files change; worktree read-back passes; index and `HEAD` remain unchanged |
| V18 Category authority | Source settles a category, or deliberately does not | Settled role is exact; no role is invented when absent |
| V19 Full read-back mismatch | Connector reports success but body, edge, state, claim, or frontier differs | `publication-recovery`; no success or delivery recommendation |
| V20 Mutation boundary | Successful connector or Local Markdown run | No code, source, domain, review, Git index/commit/remote, or delivery mutation |
| V21 Default route | Verified graph with no explicit top-level parent-delivery request | Recommend first ready ticket to `implement` |
| V22 Parent-delivery route | Explicit top-level parent-delivery request plus exhaustive non-empty verified parent-backed graph | Recommend `parallel-implement` and stop |
| V23 Parent-delivery negatives | Direct graph, delegated request, incomplete graph, or generic parallel preference | Do not recommend `parallel-implement`; use default route or failure Return |
| V24 Completion | Every gate passes or one safe failure is fully observed | Exactly one typed Return, exact residual gaps, unrelated state preserved, no successor started |

The suite is the complete M0 viability claim. It makes no claim that a later
research-informed addition improves behavior or that exact future wording
causes the behavior.

## Proof Outline

- Read back every local intent authority named in the source identity manifest
  and verify its digest before re-entry.
- Structurally validate the unit ledger, clause map, state-location ledger,
  and V01-V24 coverage so every unit has entry, wrong-condition, failure
  Return, and proof.
- Materialize M0 later only from this capsule, then run the complete viability
  suite through fixed positive, closest-negative, partial-mutation, reuse,
  relationship, routing, and completion fixtures.
- Use normalized heading-bounded semantic checks for prose and exact checks
  only for machine tokens, paths, marker text, status names, and hashes.
- Use tracker fakes or isolated Local Markdown fixtures for mutation cases.
  External live publication is not required to prove M0 semantics and must not
  be performed without separate exact authority.
- For any later claim that exact wording changes invocation, judgment, action,
  context loading, Return, or completion, use uncontaminated fresh-context
  controls under `writing-great-skills/BEHAVIOR-EVALS.md`; structural checks
  alone do not support that claim.

## Local Source Identity Manifest

All digests are SHA-256 of exact file bytes.

| Classification | Local authority | SHA-256 | Contract contribution |
| --- | --- | --- | --- |
| affected | `AGENTS.md` | `d93d25a1e8bf09f01fb9eee054682940539a072c5f489e99435dbe6e10cde314` | Setup marker, commands, boundaries |
| affected | `CONTEXT.md` | `bae0de4372439edc96e91c5132967755797bc4628c8b2fef03591b6779fde8e1` | Pack vocabulary and artifact owners |
| affected | `docs/agents/engineering-contract.md` | `c3d52491ca8b98f229965e2602212fc4474ef2fedf8be73bc8f08c24300ef829` | Source Trace, slices, proof, state, safety |
| preserve | `docs/agents/domain.md` | `94ccdc414542b44be2fe38d7ebe2e59fd809c09848642243c3a805749c6adb99` | Domain and ADR routing |
| affected | `docs/agents/issue-tracker.md` | `d79c8dbdc0e3c77583b461ac2d50eb678d0ce77aed69a9e759e3c0818646f933` | Ready contract, relationships, frontier, mutation read-back |
| affected | `docs/agents/triage-labels.md` | `06f253d31ea852376950b4b8c163f2a1e60c5be131492b3cb76d05be92b58ded` | Role mappings |
| affected | `docs/synthesis/skill-context-relationships.md` | `15bb4ab6cd4cda5256b45aae4c7bb887a153f62cc63dbd2203d0f3b68ea1ad69` | Invocation, ownership, callers, Returns |
| preserve | `GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md` | `d75a2407cc8e39c0b936b3c2d5eb8473949fc6aaeabdfd520185ddc9c36a5f24` | Bootstrap boundary |
| affected | `skills/custom/to-spec/SKILL.md` | `00e26469482d657f6201ad33051f2d4c1d3554c91d6780e7402f41ca8158d7fd` | Verified parent source and handoff |
| affected | `skills/custom/to-spec/agents/openai.yaml` | `a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94` | Explicit caller invocation |
| preserve | `skills/custom/triage/SKILL.md` | `3a1ce646fd247181d3d4ae5758a55b1e16f0573a465d5b5dd8ce4f24636f3ec4` | Ready output is not retriaged |
| affected | `skills/custom/triage/AGENT-BRIEF.md` | `529e173c30d34f2dcc0b19ba98cddb8dded77c6cf51fbe4dc4e5a2d435bf7ad0` | Ready packet and slice forms |
| preserve | `skills/custom/triage/AGENT-BRIEF-EXAMPLES.md` | `9ca3a7fa4d32472348142b77d1723982c8296248b27fbb21a11a999cc10a50de` | Branch evidence emphasis |
| affected | `skills/custom/implement/SKILL.md` | `4418cf9e1355a1247a56b9f08fa0ea7d0819fa8d67de1b164a047336caab4aec` | Single-ticket admission contract |
| affected | `skills/custom/implement/agents/openai.yaml` | `c1d01d8e94556c59e864834d7e16d1a370033d1960d4ac9525af5dfff7db97ec` | Explicit delivery boundary |
| affected | `skills/custom/parallel-implement/SKILL.md` | `7865a223b1e724142c3afd31912151ca0ee4ba8f2a61c01c52fea7e9e920019c` | Exhaustive graph, profile, matrix, routing |
| affected | `skills/custom/parallel-implement/agents/openai.yaml` | `e209a55b28a7700bc6cf895277f4553cb4d7feac57021f810335d4581c6e038e` | Explicit parent-delivery boundary |
| affected | `skills/custom/parallel-implement/references/WORKER-BRIEF.md` | `9f5bdc155ebc3fc5b33276f19938063c89321532aa7b5b5178853f95f763ec0f` | Ticket-owned worker inputs |
| preserve | `skills/custom/parallel-implement/references/RUN-LEDGER.md` | `b0aa0288d58f5bcd5eda6328cfc6332bd820f32788404b8442570efad993b370` | Parent/children runtime compatibility |
| affected | `skills/custom/improve-codebase/SKILL.md` | `ed2a156e0a92af9ea46dedcf47a63596346976333f7b59705b5bc066fef3b23b` | Selected multi-slice source route |
| affected | `skills/custom/improve-codebase/SELECTED-CANDIDATE.md` | `d8795dc6209422bbd9d7678f9e32ccff915e87fa0b907fb163306de4d3066b50` | Settled candidate packet |
| affected | `skills/custom/audit-codebase/SKILL.md` | `637a1462c6aa54b2e6f83b1cfce7b0e75809f402eb5a51b1b4f5b5558d052e64` | Verified audit-source boundary |
| affected | `skills/custom/audit-codebase/DEFECT-CONTRACT.md` | `a74e8f15e40259946169dd94fd8440dbea7ec7f5835c749e5ffab2b1cfd7f5b5` | Settled multi-item remediation route |
| preserve | `skills/custom/repo-bootstrap/SKILL.md` | `5cd0a9fc5617babdebb6f04b9450e0c41a6ea893e20c9af8cb3907dc7963f92d` | Setup precondition owner |
| preserve | `skills/custom/repo-bootstrap/setup-schema.json` | `66e70f04e8288110ef38d32b01aac63fe68f9f7098beabecb0e96d70b0baa497` | Setup compatibility fingerprint |
| affected | `skills/custom/skill-router/SKILL.md` | `2bbf8e9c2b9c0c86d8aa3abff2a66bdfb946a9a120dbff3d5d640966398d7c05` | Explicit route and closest exclusions |
| affected | `skills/custom/skill-router/agents/openai.yaml` | `3bf863a8856d04a6a1c4f23b3aae6cbf5388544129662c55cc733c2d9c23bbbf` | Explicit-only route compatibility |
| preserve | `docs/adr/0001-agents-primes-contract-teaches-skills-execute.md` | `eb0ca5b54a8dbdd35a2fd170734006460e7f7a5a0f93ad8ce29264c8bcc76b75` | Context ownership |
| preserve | `docs/adr/0002-setup-installs-repo-local-engineering-contract.md` | `850e1bb0a2204c351f14a5a094d196c530e66e194b49f379755787d5bdc009ff` | Setup ownership |
| preserve | `docs/adr/0003-skills-encode-local-contract-slices.md` | `5c043765d4679a272e096fa492b0b52b71f4c519216e98630e11031149177f34` | Local contract slice |
| preserve | `docs/adr/0004-validator-enforces-publishing-hygiene-not-language.md` | `9e769eb02eec437867cd59e90553bb6dc981352b2a424f3eaadbae4bc354684e` | Proof boundary |
| preserve | `docs/adr/0005-separate-active-and-experimental-skill-trees.md` | `91e14650e896b63115fbec818b3d01ca506d27ab92a501303f8f164fe8311552` | Active/experimental separation |
| preserve | `docs/adr/0006-domain-modeling-records-approved-adrs.md` | `1ce3289aaacf00e93fb1239f39504bab7d7724fd59c27cda6b22d1b6805822ef` | Domain mutation boundary |
| preserve | `docs/adr/0007-synthesis-preserves-exhaustive-research-runtime-skills-compress.md` | `a8b37fa83c820a08bf0e10998e1301d537cefa5d797b49edcabbb308644c8962` | Runtime compression boundary |
| process authority | `C:\Users\steve\.agents\skills\writing-great-skills\SKILL.md` | `b3a4ec9fd5c7059d566c27fca3da133b21e0d392a8cb035b4213a2a44930d1fe` | Audit semantics and proof |
| process authority | `C:\Users\steve\.agents\skills\writing-great-skills\GLOSSARY.md` | `73397064f51504f128c559c6a037dcd0d491f7950cffdecf226a535188002278` | Invocation and completion vocabulary |

Coverage classification:

- `affected`: the trigger, ticket shape, state matrix, graph, publication,
  Return, or completion contract depends on the source.
- `preserve`: the source owns a boundary or compatibility rule that M0 points
  to without importing its procedure.
- `owned elsewhere`: tracker transport and closeout, setup provisioning,
  source shaping, domain truth, implementation, formal review, installation,
  and Git delivery.
- `historical evidence`: none read or reused.
- `drift`: none observed among allowed local authorities.
- `not applicable`: `pyproject.toml` was not needed for target behavior;
  target synthesis, target runtime, target tests, historical evaluations,
  promotion records, experimental candidates, upstream packages, installed
  mirrors, Git history, and outside research were not inspected.

User authority is additionally identified by the exact Prompt 1 brief, the
starting `HEAD` above, and historical-incumbent identifier
`b2df62a1879ffe4c5624656f63712c723fcdb44a`; the incumbent bytes and Git
history were deliberately not read.

## Limitations and Evidence Gaps

- This is a blind intent-derived specification. It makes no claim about the
  incumbent runtime, existing tests, prior evaluations, professional
  correctness, or wording efficacy.
- The local repository configures GitHub, but M0 preserves the pack's required
  GitHub, GitLab, and Local Markdown compatibility. Exact transport mechanics
  remain with each configured tracker contract.
- No live tracker mutation, connector capability probe, external publication,
  or behavioral sample was performed in Prompt 1.
- A recoverable non-ready-first publication route is required by the safety
  floor. Research may compare transaction and recovery techniques but may not
  weaken the no-false-ready or no-duplicate-create requirements.
- The exact runtime wording, package split, and proof fixtures remain to be
  materialized and tested in later authorized units.
- The research note path is authorized for the Research Pass only; Prompt 1
  did not create or inspect it.

## Research Questions Grouped by Intended Behavior

### R1: independently completable slicing

- What evidence-backed methods distinguish a behavior slice from file or
  component tasking while preserving independently observable value?
- Under what conditions do support slices or migration stages improve delivery
  safety, and what proof prevents them from becoming speculative scaffolding?
- What counterpressure limits decomposition, ticket count, or cross-ticket
  coordination?

### R2: dependency graph and delivery qualification

- What methods best expose semantic, data, sequencing, and proof dependencies
  without inventing unnecessary ordering?
- What evidence supports conservative concurrency qualification across
  ownership, write sets, proof resources, and irreversible transitions?
- Which graph checks most reliably detect hidden dependencies, false-ready
  frontiers, and incomplete follow-up coverage?

### R3: stateful and irreversible work

- What evidence-backed ticket information is needed for migrations, cutovers,
  protected data, permissions, trust boundaries, rollback, retry, and partial
  state?
- When does a production-path tracer reduce risk, and what conditions or
  counterexamples make it insufficient?

### R4: Ready-for-agent packet quality

- Which information fields measurably improve implementation accuracy,
  autonomy, and proof without copying source or downstream procedure?
- How should acceptance and proof lanes be expressed so semantic correctness
  is testable at the highest useful seam?
- What omissions most often force downstream reconstruction or unsafe scope
  widening?

### R5: publication, idempotency, and recovery

- What transaction patterns are appropriate when issue trackers lack atomic
  multi-item creation and relationship updates?
- What read-back and idempotency evidence prevents duplicate items, partial
  graph activation, or false readiness after uncertain connector results?
- What is the cheapest portable recovery packet across GitHub, GitLab, and
  Local Markdown?

### R6: invocation, Return, and completion

- What neutral wording best distinguishes ticket slicing from parent-spec
  synthesis, triage, single-item implementation, and parent-graph delivery?
- Which completion wording prevents early success before full graph and
  mutation read-back?
- Which exact candidate clauses need fresh behavioral controls rather than
  structural proof?

Authorized research-note path:
`docs/research/to-tickets-deploy-2026-07-25.md`.

## Re-entry Contract

Re-entry must:

1. verify repository `HEAD` remains
   `8752406cf437629787c2abec5f66c3c0e6eda8b1` unless the campaign transition
   explicitly authorizes a new fixed identity;
2. re-hash every local and process authority in the identity manifest;
3. verify the exact capsule markers and content fingerprint;
4. verify the user brief still names the same skill, epoch, source allowlist,
   forbidden categories, historical-incumbent identifier, mutation boundary,
   and proof budget; and
5. revisit only an exact identified decision delta.

Unexpected `HEAD`, authority, identity, allowlist, or capsule drift requires a
fresh blind Prompt 1 pass. Later research, synthesis, runtime, incumbent, or
evaluation artifacts cannot waive or silently amend this checkpoint.

<!-- END TO-TICKETS PROMPT-1 M0 CAPSULE -->

Content fingerprint: `sha256:16b6fbd4bde2486c29ab3bb5d5e246f2be305f1d6cfe6f3609a98ec5b61a1006`
