# To Spec Deploy Campaign — Prompt 1 M0 Checkpoint

<!-- BEGIN TO-SPEC-2026-07-25-PROMPT1-CAPSULE -->

<!-- BEGIN TO-SPEC-2026-07-25-M0-FINGERPRINTED-CONTENT -->

## Capsule Metadata

| Field | Value |
| --- | --- |
| Skill | `to-spec` |
| Campaign epoch | `2026-07-25` |
| Authorized unit | Deploy Prompt 1: Freeze M0 |
| Delivery mode | Bare Deploy Campaign; Prompt 5 promotion and install authorized; Git delivery not authorized |
| Starting Git HEAD | `b9750babea998c4bc0f5809972a8651934218eca` |
| Audit operation | `writing-great-skills` Audit |
| Decision | `ready-for-research` |
| Authorized successor mutation | `docs/research/skills/to-spec/RP-to-spec-20260725-01.md` only |
| Historical incumbent constraint | The user identifies commit `f3be70c31dd8f2ae9f12a75248065ef313790bda` as C0 for exact later materialization; it was not inspected and is not M0 authority. |

## Intended Contract

### Outcome

`to-spec` turns one identity-bearing source with settled commitment authority into one durable, verified parent specification in the configured issue tracker. The parent owns intent for later implementation slicing. The skill may create a disposable local draft while synthesizing, but the tracker packet becomes authoritative only after publication read-back.

### Invocation And Exclusions

- Invocation is explicit-only. Admit a direct request to create one parent specification from a named source in one target repository.
- Accept a direct settled packet or a verified return from an allowed caller: a `Confirmed` `grill-with-docs` packet with its current Domain Delta, a closed Wayfinder map whose destination is settled parent-spec source, a verified selected improvement routed as specification-ready, or a verified audit finding or cohesive cluster whose expectation and evidence are fixed.
- A caller return does not waive source sufficiency. Missing identity, commitment authority, acceptance, supported behavior, or another source-owned decision returns `source-gap`.
- Exclude conversational shaping, research, runnable design investigation, domain truth mutation, ADR approval, implementation-ticket slicing, triage, implementation, review, installation, Git delivery, and downstream execution.
- Load `codebase-design` only as vocabulary when a bounded interface, seam, adapter, module, or caller-facing proof surface must be stated. The specification retains artifact and completion authority.

### Authority

- The user and accepted source own outcome, commitments, acceptance, scope, exclusions, supported states, public and data contracts, security and privacy posture, compatibility, migration, rollback, and agreed tradeoffs.
- Repository domain documents and ADRs own accepted language and durable decisions. `to-spec` consumes and preserves them; it never writes domain truth.
- `docs/agents/issue-tracker.md` owns tracker transport, packet location, relationship mechanics, and mutation read-back. `docs/agents/triage-labels.md` owns role-to-label mapping.
- `codebase-design` owns shared module and interface vocabulary, not specification decisions.
- `to-spec` owns source coverage, parent-spec synthesis, the disposable draft, the frozen publication packet, one authorized tracker create or exact reuse, publication verification, failure Return, and completion.
- `to-tickets` owns implementation slicing and dependency-ordered Ready-for-agent children. `repo-bootstrap` owns repair of a missing or incompatible setup surface.

### Parent Specification Contract

A successful parent packet has one title and body and accounts for:

1. outcome and Source Trace with exact source identities;
2. commitment boundary: in scope, exclusions, non-goals, and source-authorized deferrals;
3. observable desired behavior and acceptance criteria;
4. supported paths, states, lifecycle transitions, edge cases, and failure behavior;
5. public interfaces, caller obligations, data contracts, ordering, and errors when applicable;
6. security, privacy, permissions, trust, and irreversible-state constraints when applicable;
7. compatibility, migration, rollback, and cutover obligations when applicable;
8. accepted domain terms, governing ADRs, and surfaced conflicts;
9. proof seams, proof lanes, and evidence required for acceptance;
10. risks, residual gaps, and implementation constraints needed by later slicing.

Every in-scope commitment maps to at least one body section or acceptance criterion. A success packet has no unresolved material commitment, ownerless requirement, or contradiction. A source-authorized deferral names its owner and boundary. The parent does not contain implementation tickets or mark itself `ready-for-agent`.

### Safe Failure Return

Return exactly one status:

| Status | Condition | Required Return |
| --- | --- | --- |
| `setup-precondition` | The configured tracker, label map, domain routing, or required read-back operation is missing or incompatible. | Missing surface, observed state, preserved state, and unstarted recommendation for `$repo-bootstrap`. |
| `source-gap` | Source identity, access, authority, commitment, acceptance, supported behavior, or another source-owned fact is missing, ambiguous, or contradictory. | Exact affected field, owner, evidence inspected, and re-entry condition; no tracker mutation. |
| `existing-state-conflict` | A possible or existing parent cannot be proven absent or exact, or it differs from the frozen packet without explicit update authority. | Candidate identities, observed difference or uncertainty, and smallest authority needed; no create or update. |
| `publication-recovery` | A tracker create or later publication operation is failed, partial, stale, mismatched, or indeterminate. | Frozen packet identity, applied and failed operations, observed tracker state, preserved draft, and safest tracker-owned recovery action. Never repeat an indeterminate create. |
| `ready-spec` | One newly published or exactly reused parent packet and its applicable tracker state read back as intended. | Source identity, parent pointer and identity, publication or reuse proof, residual gaps, and one unstarted `$to-tickets` recommendation. |

### Completion, Order, Compatibility, And Safety

The irreversible order is: verify setup and source authority; inspect existing tracker state; synthesize and validate the complete packet; freeze its identity; confirm that the explicit invocation authorizes the one configured transition; create only after verified absence; immediately refetch the unique create; apply only source-authorized tracker metadata; refetch the complete affected parent state; then remove the disposable draft or preserve it for recovery. Stop further mutation on the first unsafe, failed, or indeterminate transition.

Complete only on `ready-spec` when the source, commitment coverage, parent packet, applicable roles and state, and publication or exact reuse all verify; the disposable draft is removed or intentionally preserved for named recovery; unrelated state is preserved; one next recommendation is returned; and no successor starts.

Required compatibility:

- preserve the issue tracker as the durable packet owner and obey Mutation read-back;
- use mapped label strings only for source-authorized applicable roles, never invent a category, and never apply Ready-for-agent state to the parent;
- preserve accepted domain terms and expose ADR conflicts rather than overriding them;
- produce a parent source that `to-tickets` can identity-check and slice without rediscovering commitments;
- retain caller payload identities and, for `grill-with-docs`, the intact confirmed packet and current Domain Delta;
- retain Wayfinder resolution pointers rather than copying ticket-owned chronology;
- keep active runtime procedure in the eventual skill package, local contracts with their owners, and historical evidence outside runtime.

## Applicable State-Location Ledger

| State or artifact | Owner and authoritative location | Allowed transition | Required order | Read-back | Failure Return | M0 units | Viability cases |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Accepted source packet and pointers | User or caller-owned source locations | Read only; bind exact identities into Source Trace | Before synthesis | Reopen every decision-bearing pointer and compare identity | `source-gap` | U03-U05 | V03, V05, V06 |
| Domain vocabulary and ADRs | Routed `CONTEXT.md`, `CONTEXT-MAP.md`, and `docs/adr/` per `docs/agents/domain.md` | Read only; preserve terms and flag conflicts | Before finalizing packet | Re-read cited terms and decisions | `source-gap` | U05 | V06 |
| Existing parent candidate | Configured tracker issue packet | Read only during preflight; classify verified absence, exact reuse, conflict, or unknown | Before any draft-backed create | Refetch candidate body, comments, roles, state, and relationships | `existing-state-conflict` | U07 | V08 |
| Disposable specification draft | `.tmp/to-spec/<source-slug>.md` | Create or replace only for the admitted source; delete after verified success or preserve with identity on recovery | After authority closes; before publication | Exact-byte read-back and digest | `source-gap` before mutation or `publication-recovery` after tracker mutation | U08-U11, U15 | V09, V10 |
| Frozen publication packet | In-memory packet plus the exact disposable draft identity | Freeze title, body, source identity, applicable role operations, and intended tracker transition; immutable after authorization | Before external mutation | Recompute exact packet digest immediately before create | `existing-state-conflict` or `publication-recovery` | U10-U12 | V07-V10 |
| Durable parent specification | Configured issue tracker issue body and comments | Verified absence to one create, or exact existing packet to reuse; no divergent update in M0 | Only after frozen packet and authority | Immediate unique-create refetch, then complete parent refetch | `publication-recovery`; never repeat an indeterminate create | U13-U14 | V08, V10, V11 |
| Parent labels, state, assignee, and relationships | Configured tracker under tracker and label contracts | Apply only source-authorized applicable metadata; parent remains outside Ready-for-agent child state | After issue identity verifies | Refetch labels, state, assignee, relationships, open/closed status, and affected frontier | `publication-recovery` | U13-U14 | V11 |
| Working tree outside the disposable draft | Repository owner | Read only | Throughout | `git status --short` and scoped path checks | Typed failure matching the blocked stage | U02, U16 | V13 |
| Git index, committed tree, `HEAD`, and remotes | Git and Prompt 6 owners | No transition | Throughout | Start/end `HEAD`; status confirms no staging | `blocked` at campaign-protocol level if `HEAD` changes | U16 | V13 |

Connector and remote tracker state are applicable because publication is durable and external. Installed mirrors, deployment state, and target runtime publication are not applicable to M0 execution. Git objects are read only; Git delivery is outside `to-spec`.

## Semantic Behavior Unit Ledger

| Unit | Independently owned behavior | Local authority | Cheapest neutral expression | Entry case | Wrong-condition case | Failure Return | Proof |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U01 | Explicit invocation gate | Relationship Invocation Map; Skill Router; README | Admit only a direct `to-spec` selection for one parent specification. | User names `to-spec` and one target/source. | Implicit shaping or generic planning request. | Stop outside the skill; no mutation. | Invocation positive and nearest-exclusion controls. |
| U02 | Setup compatibility gate | `repo-bootstrap`; tracker, label, and domain contracts | Verify configured publication and read-back surfaces before drafting for mutation. | Tracker supports create, inspect, and read-back. | Missing tracker operation or incompatible setup marker. | `setup-precondition`. | Structural setup fixture with no-write negative case. |
| U03 | Source type, identity, and access admission | User; Skill Router; caller contracts; Audit finding contract | Accept one named source and bind every decision-bearing pointer to an exact identity. | Direct packet or allowed verified caller return is accessible. | Missing pointer, stale caller payload, or multiple unresolved sources. | `source-gap`. | Accepted caller fixtures and inaccessible/stale negatives. |
| U04 | Commitment-authority sufficiency | Engineering commitment boundary; caller contracts; `to-tickets` source contract | Require source-owned outcome, scope, acceptance, supported behavior, and applicable contracts; never choose user commitments. | All material decisions are settled or explicitly deferred by their owner. | Preference, public contract, migration, or tradeoff needs a user decision. | `source-gap` naming owner and re-entry condition. | Coverage matrix and one owner-gap negative per commitment class. |
| U05 | Domain and ADR preservation | `docs/agents/domain.md`; ADRs; relationship owner | Read only relevant domain sources, use accepted terms, and surface conflicts. | Terms and ADRs support the packet. | Proposed requirement contradicts a governing ADR or invents missing language. | `source-gap`. | Term trace and ADR-conflict fixture; no domain writes. |
| U06 | Vocabulary-only module/interface design | `codebase-design` caller contract; relationship owner | Apply module, interface, seam, adapter, leverage, depth, and locality terms without transferring artifact authority. | A bounded caller-facing design surface belongs in the spec. | The question needs an unresolved design verdict or broad survey. | `source-gap`; name the unresolved source-owned decision. | Packet vocabulary trace and ownership assertion. |
| U07 | Existing-state and duplicate-create gate | Tracker Mutation read-back; safety boundary | Classify verified absence, exact reuse, divergence, and unknown before creation. | Search and refetch prove no parent or an exact parent. | Similar, claimed, divergent, stale, or indeterminate parent exists. | `existing-state-conflict`. | Absent, exact-reuse, divergent, and unknown tracker fixtures. |
| U08 | Parent packet synthesis | README outcome; relationship ownership; engineering contract | Render the complete parent contract with locally owned vocabulary and no ticket slicing. | Source is sufficient. | Required section or applicable branch is missing. | `source-gap` before publication. | Parsed heading/field checks plus semantic coverage review. |
| U09 | Bidirectional commitment coverage | Engineering Source Trace and proof discipline; `to-tickets` compatibility | Map every requirement, exclusion, deferral, risk, and proof obligation to the parent and map every parent commitment back to authority. | Ledger closes with no orphan. | Omitted, duplicated, contradictory, or ownerless commitment. | `source-gap`. | Bidirectional ledger checker and controlled orphan negative. |
| U10 | Parent validity gate | Intended Parent Specification Contract | Reject unresolved material choices, implementation tickets, false Ready-for-agent status, invented roles, and unverifiable acceptance. | Packet is behavior-complete and parent-scoped. | Packet contains child slices, vague acceptance, or unowned labels. | `source-gap`. | Semantic rubric and focused structural negatives. |
| U11 | Disposable draft and exact packet identity | CONTEXT work-state policy; relationship map | Write one `.tmp/to-spec/` draft and verify exact bytes and digest. | Frozen title/body are ready. | Draft differs from the packet or overlaps unrelated work. | `source-gap` before tracker mutation. | Exact-byte read-back, digest, and scoped status. |
| U12 | External mutation authorization and irreversible gate | User invocation; engineering authorization boundary | Freeze operations and proceed only when the explicit request authorizes that exact one-parent transition. | Target repo, source, title/body, and create are authorized. | Request is read-only, target is ambiguous, or packet changed. | `existing-state-conflict` with exact authority needed. | Frozen-operation comparison and changed-packet negative. |
| U13 | Create/reuse and metadata sequencing | Tracker contract; label map; state ledger | Create once after verified absence or reuse exact state; immediately refetch; then apply only authorized metadata. | Unique create or exact reuse verifies. | Create outcome is failed/unknown, or metadata is partial. | `publication-recovery`; stop mutations. | Tracker fake covering create, reuse, timeout, partial metadata, and no-repeat. |
| U14 | Complete publication reconciliation | Tracker Mutation read-back | Refetch the parent and affected state; compare body, roles, state, assignee, relationships, and frontier with the frozen plan. | All observations match. | Stale, partial, indeterminate, or mismatched state. | `publication-recovery`. | Full read-back fixture with one mismatch per observable class. |
| U15 | Draft disposition | CONTEXT work-state policy; relationship draft boundary | Delete the draft after verified success; preserve and name its identity on recovery. | `ready-spec` or post-create failure. | Draft disappears before recovery is safe or remains unnamed after success. | `publication-recovery` when recovery evidence is at risk. | Success cleanup and failure-preservation checks. |
| U16 | Typed Return, completion, and stop | Relationship runtime composition; Shared Run Contract | Return one supported status; on success recommend `$to-tickets` and stop. | Verified parent exists and all gates close. | Success claimed without read-back, successor begins, or unrelated state changed. | Matching failure status; campaign-level `blocked` on HEAD drift. | Return-schema, no-successor, scoped-state, and start/end HEAD checks. |

## Runtime-Clause Specification

| Runtime clause | Units | Required observable behavior | Viability-floor mapping | Clause-to-intent cut result |
| --- | --- | --- | --- | --- |
| Description | U01 | Explicitly selected conversion of settled source into a verified tracker parent spec; closest exclusions are shaping, tickets, and delivery. | Invocation, outcome, exclusions | Keep; routing predicate. |
| Outcome and ownership preamble | U03-U06 | Name one outcome and divide source, domain, tracker, design-vocabulary, spec, ticket, setup, and Git ownership. | Outcome, authority, relationships, compatibility | Keep; prevents boundary transfer. |
| Admit | U01-U07 | Verify setup, source identity, commitment sufficiency, relevant domain decisions, caller integrity, and existing parent state before mutation. | Invocation, authority, safe failure, safety | Keep; every gate has an entry and wrong-condition branch. |
| Synthesize | U08-U10 | Build the complete parent packet and bidirectional commitment ledger; reject ownerless or child-level work. | Outcome, caller obligation, completion | Keep; minimum artifact semantics. |
| Freeze | U11-U12 | Write/read back the disposable draft, freeze packet and operations, and confirm exact authority. | Irreversible order, safety | Keep; prevents drift across commitment boundary. |
| Publish | U13-U15 | Create once or reuse exact state, read back each transition, stop on first uncertainty, reconcile complete parent state, and dispose or preserve the draft truthfully. | Irreversible order, safe failure, completion | Keep; durable-state viability. |
| Return | U16 | Emit exactly one typed status, evidence and recovery information, or a verified parent plus one unstarted recommendation. | Return, completion, relationships | Keep; closes without chaining. |
| Completion | U15-U16 | Require verified authority, coverage, packet, tracker state, draft disposition, unrelated-state preservation, and no successor. | Completion, safety | Keep; sharp terminal criterion. |

Cut audit result: every retained runtime clause maps to at least one viability-floor axis or required local contract. Research methods, current-runtime compatibility behaviors, implementation technique, ticket schema duplication, tracker transport commands, label literals, domain-writing procedure, generic engineering philosophy, installation, and Git delivery are excluded from M0 runtime wording because their owners retain them or they are not needed for the minimum behavior.

## Complete M0 Viability Suite

This suite proves only M0 viability. It makes no later improvement, wording-efficacy, or professional-validity claim.

| Case | Scenario | Required observation | Units |
| --- | --- | --- | --- |
| V01 | Direct explicit `to-spec` request with one settled source | Invocation admits exactly one parent-spec run. | U01 |
| V02 | Generic planning, shaping, ticketing, or implementation request without explicit selection | `to-spec` does not begin and no state changes. | U01 |
| V03 | Missing source identity, inaccessible pointer, contradictory authority, or unsettled commitment | `source-gap` names the field, owner, and re-entry condition; no draft-backed tracker mutation. | U03-U04 |
| V04 | Missing or incompatible tracker, label, domain-routing, or read-back surface | `setup-precondition` recommends `$repo-bootstrap` and preserves state. | U02 |
| V05 | Each allowed caller shape: direct settled packet, confirmed Grill packet plus current Domain Delta, closed Wayfinder source map, specification-ready improvement, and verified audit finding/cluster | Accepted only when exact identities and commitment authority are complete; caller pointers remain intact. | U03-U04 |
| V06 | Relevant accepted term and governing ADR, plus a contradictory-ADR control | Accepted vocabulary is preserved; contradiction returns `source-gap`; domain files never change. | U05 |
| V07 | Spec containing an applicable interface/state/compatibility branch and proof seam | Parent headings and commitment ledger are complete; design vocabulary remains subordinate; no implementation tickets appear. | U06, U08-U10 |
| V08 | Tracker states: verified absence, exact existing parent, divergent candidate, and unknown query result | Create once, exact reuse, `existing-state-conflict`, and `existing-state-conflict` respectively; no duplicate create. | U07, U12-U13 |
| V09 | Successful draft freeze before publication | Exact draft bytes and packet digest match; only `.tmp/to-spec/` changes locally before external mutation. | U11-U12 |
| V10 | Create timeout or partial metadata/read-back | `publication-recovery` records applied/failed operations and draft identity; no repeated indeterminate create or further mutation. | U13-U15 |
| V11 | Successful new publication and exact reuse | Complete refetch matches title, body, applicable labels/state, assignee, relationships, status, and affected frontier; parent is not Ready-for-agent. | U13-U14 |
| V12 | Successful completion | `ready-spec` returns source and parent identities, evidence, gaps, and one unstarted `$to-tickets` recommendation. | U16 |
| V13 | Any run, including failures | No domain, source, code, index, `HEAD`, remote Git, installation, ticket-child, or unrelated worktree mutation; draft disposition is truthful. | U02, U05, U15-U16 |

### Proof Outline

1. Parse future metadata and assert explicit-only invocation.
2. Use fixed direct and caller-return fixtures for source admission, identity, and commitment coverage.
3. Parse a candidate parent body and heading-bounded normalized semantics; run a controlled missing-section, orphan-commitment, invented-label, child-ticket, and vague-acceptance negative.
4. Use a deterministic tracker fake for absent, exact-reuse, divergent, unknown, create-success, create-timeout, partial metadata, stale read-back, and complete reconciliation branches. Assert mutation order and no repeated create.
5. Verify exact draft bytes, digest, success deletion, and failure preservation.
6. Verify no writes outside the authorized local draft and configured tracker transition, no staging, unchanged `HEAD`, one typed Return, and no successor execution.
7. Run affected Markdown gates and `python -m scripts.validate_skills`; do not run the full suite in Prompt 1.

## Audit Coverage Classification

| Surface | Classification | Disposition |
| --- | --- | --- |
| User campaign brief and C0 constraint | `affected` | Settles blind boundary, mutation path, later exact C0 identity, proof budget, and Return. |
| Repo/domain/tracker/label authorities | `affected` | Own source hierarchy, domain consumption, durable packet, mutation read-back, and label mapping. |
| Relationship owner and README | `affected` | Own explicit invocation, callers, parent-spec publication, design vocabulary load, and stop routes. |
| `skill-router`, `grill-with-docs`, Wayfinder, selected-improvement, and audit-finding caller surfaces | `affected` | Define admissible source shapes and payload integrity. |
| `to-tickets` | `affected` | Downstream consumer contract determines the minimum usable parent source and handoff boundary. |
| `repo-bootstrap` | `affected` | Owns setup-precondition recovery; remains uninvoked. |
| `codebase-design` | `affected` | Vocabulary-only caller contract; direct design procedure remains outside the allowed and necessary scope. |
| Engineering contract and ADRs | `preserve` | Their local Source Trace, commitment, proof, state, and ownership slices are referenced without copying the full contract. |
| Domain mutation and ADR approval | `owned elsewhere` | `domain-modeling`; no mutation authorized. |
| Tracker transport mechanics and role strings | `owned elsewhere` | Setup docs; eventual runtime points to them. |
| Ticket slicing and Ready-for-agent graph | `owned elsewhere` | `to-tickets`; no ticket schema is imported into the parent workflow. |
| Installation, publication of runtime, and Git delivery | `owned elsewhere` | Prompt 5 and Prompt 6 owners; untouched in Prompt 1. |
| Historical incumbent C0, target synthesis, target runtime, experimental target, evaluations, tests, upstream packages, research, and installed mirrors | `historical evidence` or `owned elsewhere` | Deliberately not inspected; they cannot authorize M0. |
| Local intent authority drift | `not applicable` at freeze | No drift observed during the blind pass; re-entry rules below govern future drift. |

## Local Source Identity Manifest

Repo-local identities are SHA-256 over exact working-tree bytes plus Git blob object identity. External skill identities are SHA-256 over exact bytes. The deploy-method file identity covers the file, but only `Shared Model`, `Shared Run Contract`, `Proportionate Proof Budget`, and `Deploy Prompt 1: Freeze M0` were read as authority.

| Source | Bytes | SHA-256 | Git blob | Role |
| --- | ---: | --- | --- | --- |
| `AGENTS.md` | 1873 | `d93d25a1e8bf09f01fb9eee054682940539a072c5f489e99435dbe6e10cde314` | `7b80f0d525b11b41d751b60733dcb4188c0e6bf4` | Repo primer and campaign pointer |
| `CONTEXT.md` | 8645 | `bae0de4372439edc96e91c5132967755797bc4628c8b2fef03591b6779fde8e1` | `93df3de0e3cc6f644fd5185a904b974e54746ddf` | Pack invariants, owners, work state, vocabulary |
| `README.md` | 11916 | `dc630154d9c2d61124c93c6cd6ae4af5b1b813fb50bd661e47cc0af7456c0bcb` | `6f24cf9116397b0ac7449608d74c43abe3a44c5a` | Human outcome and representative routes |
| `docs/agents/engineering-contract.md` | 8601 | `c3d52491ca8b98f229965e2602212fc4474ef2fedf8be73bc8f08c24300ef829` | `5fc37b60ee66e5159f7a9115fc0c7de783d42270` | Commitment, Source Trace, proof, state, Lock |
| `docs/agents/domain.md` | 1629 | `94ccdc414542b44be2fe38d7ebe2e59fd809c09848642243c3a805749c6adb99` | `c81329fdbeb12fa0b51eb345c85f4b5ffe85d8b8` | Domain and ADR routing |
| `docs/agents/issue-tracker.md` | 8322 | `d79c8dbdc0e3c77583b461ac2d50eb678d0ce77aed69a9e759e3c0818646f933` | `1e429ce2806cc00223a73b69413c8fa976ff19c0` | Durable packet and mutation read-back |
| `docs/agents/triage-labels.md` | 2079 | `06f253d31ea852376950b4b8c163f2a1e60c5be131492b3cb76d05be92b58ded` | `103836d88d5ef6bb076bb3f52b2d3be4bad28e4f` | Role-to-label mapping |
| `docs/adr/0001-agents-primes-contract-teaches-skills-execute.md` | 676 | `eb0ca5b54a8dbdd35a2fd170734006460e7f7a5a0f93ad8ce29264c8bcc76b75` | `a07c533376578372431950b50caf50a10d01050d` | Information ownership |
| `docs/adr/0003-skills-encode-local-contract-slices.md` | 569 | `5c043765d4679a272e096fa492b0b52b71f4c519216e98630e11031149177f34` | `627e4cae56645f9ef1264dcd77ecb7d531263b91` | Local contract slices |
| `docs/adr/0005-separate-active-and-experimental-skill-trees.md` | 649 | `91e14650e896b63115fbec818b3d01ca506d27ab92a501303f8f164fe8311552` | `6028ccdae6155e9a4a8efc780855425bd5090a81` | Active versus experimental authority |
| `docs/adr/0007-synthesis-preserves-exhaustive-research-runtime-skills-compress.md` | 1343 | `a8b37fa83c820a08bf0e10998e1301d537cefa5d797b49edcabbb308644c8962` | `70ccbc273300b5fed238783e950758cc364010d0` | Synthesis/runtime ownership |
| `docs/synthesis/methods/deploy-prompts.md` | 59159 | `b56741c3394330c1b2664f1da06862786cf3b465ea23a4b39794a18dbcc6a2a8` | `d08ea5fa21bf0e83e8b656873492f5ed5d1c599a` | Allowed shared sections and Prompt 1 |
| `docs/synthesis/skill-context-relationships.md` | 33436 | `15bb4ab6cd4cda5256b45aae4c7bb887a153f62cc63dbd2203d0f3b68ea1ad69` | `ece9bda34ac0de04b86c098a5563c583f61c95b6` | Relationship owner |
| `skills/custom/skill-router/SKILL.md` | 4512 | `2bbf8e9c2b9c0c86d8aa3abff2a66bdfb946a9a120dbff3d5d640966398d7c05` | `fe78acc3263e62dce03b6fd3ce976f7d03086b5d` | Entry route |
| `skills/custom/grill-with-docs/SKILL.md` | 3073 | `4282dfc2c6efee78f38fe69fd208e4d126649ed982c1a2b7f9e10515fab0f01a` | `1eb076c008d62362d8eff5f575c085327cc8c87b` | Confirmed caller packet |
| `skills/custom/wayfinder/SKILL.md` | 10340 | `83f47a00f50032480d82f3c35597907d23959bf2fc4d035fa2b327dbf82e831e` | `1ec9c1b11aaec821ac25507f93475e15ece634d7` | Closed-map caller contract |
| `skills/custom/wayfinder/MAP-FORMAT.md` | 1853 | `129affae265dbde7f54b4978218269a2bfdab69f41dbd9f3940482615a791d91` | `4776f3c1078b64e60f8d5788a2926762de707fd6` | Map and pointer format |
| `skills/custom/improve-codebase/SELECTED-CANDIDATE.md` | 4267 | `d8795dc6209422bbd9d7678f9e32ccff915e87fa0b907fb163306de4d3066b50` | `8af3d9e762273bd03dfbb446ff21039879c61735` | Specification-ready candidate caller |
| `skills/custom/audit-codebase/DEFECT-CONTRACT.md` | 3086 | `a74e8f15e40259946169dd94fd8440dbea7ec7f5835c749e5ffab2b1cfd7f5b5` | `1038119cdb07d11a2c78441a0ed70290a6e43c68` | Audit finding caller |
| `skills/custom/to-tickets/SKILL.md` | 9504 | `c9430f9b873d1ba33cc9072fc5453e11097b6df482c2c5a1dd687744b3808ad1` | `5c8525ef301b56ddd65119b5bf5da7b4d9f84ada` | Complete downstream caller package |
| `skills/custom/repo-bootstrap/SKILL.md` | 5346 | `5cd0a9fc5617babdebb6f04b9450e0c41a6ea893e20c9af8cb3907dc7963f92d` | `0cc3cc660a77ac4bf62791bdece0cdca2f78c40c` | Setup recovery owner |
| `C:\Users\steve\.agents\skills\writing-great-skills\SKILL.md` | 4510 | `b3a4ec9fd5c7059d566c27fca3da133b21e0d392a8cb035b4213a2a44930d1fe` | — | Audit procedure |
| `C:\Users\steve\.agents\skills\writing-great-skills\GLOSSARY.md` | 1657 | `73397064f51504f128c559c6a037dcd0d491f7950cffdecf226a535188002278` | — | Invocation, pruning, completion vocabulary |
| `C:\Users\steve\.agents\skills\codebase-design\SKILL.md` | 2875 | `9fb50c72294242702d461d8db128353b65f463ca08b23727e3fbf66a69656c64` | — | Vocabulary-only caller-facing design contract |

## Limitations And Evidence Gaps

- This is a blind intent checkpoint. It does not inspect or make claims about the current `to-spec` runtime, historical incumbent bytes, experimental candidates, synthesis conclusions, target research, target evaluations, target tests, promotion records, upstream packages, outside research, or installed mirrors.
- The user-supplied C0 commit identity is recorded but deliberately unverified in Prompt 1. A later authorized unit must materialize exactly `f3be70c31dd8f2ae9f12a75248065ef313790bda` rather than substituting current bytes.
- Structural and owner-trace proof supports M0 completeness; no claim is made that future exact wording changes agent behavior.
- The configured repository tracker contract is GitHub, but Prompt 1 performs no connector or remote inspection. Runtime viability for tracker failure and idempotency remains to be proved with controlled fixtures in later authorized units.
- No target-local evidence was inspected because all target tests and evaluations are forbidden during this blind pass. No evidence is reused.
- The downstream minimum is derived from the complete `to-tickets` package, but no current parent-spec example was opened. Exact presentation choices remain a later technique question, not a behavior-decision gap.

## Research Questions Grouped By Intended Behavior

### Source Admission, Authority, And Traceability

- Which governing or primary requirements-engineering sources best distinguish a settled specification source from unresolved stakeholder or design decisions?
- What evidence-backed traceability form catches both omitted source commitments and invented specification commitments without forcing implementation detail?
- Under what conditions should a source-authorized deferral remain in a parent spec rather than block publication?

### Parent Specification Semantics

- Which independently supported specification structures most reliably preserve observable behavior, acceptance, supported state, failures, interfaces, data, non-functional constraints, compatibility, migration, rollback, and proof obligations?
- What counterevidence warns against template completeness that produces vague or cargo-cult sections?
- Which criteria distinguish parent-level intent and constraints from implementation-ticket slicing?

### Caller And Design Compatibility

- What neutral use of interface, seam, state, and caller-facing proof vocabulary improves specifications without letting an agent make unowned design commitments?
- What minimum identity and payload integrity should be required when consuming interview, map, audit, or improvement outputs?
- Which parent-spec fields most reduce rediscovery and false readiness in later dependency-ordered slicing?

### Durable Publication And Safe Failure

- What primary guidance supports idempotent issue creation, unique-create read-back, exact reuse, and safe recovery after timeout or partial mutation?
- Which tracker observations are necessary to distinguish verified absence, exact reuse, divergence, and unknown state?
- What local-draft disposition best preserves recovery evidence without turning disposable state into a second authority?

### Invocation, Return, And Completion

- Which wording hypotheses could improve explicit-only admission, typed failure selection, irreversible sequencing, and stopping before `$to-tickets`?
- What direct-control tasks can test each hypothesis without exposing candidate language to controls?
- What completion failures are most likely when a tracker create succeeds but later metadata or read-back is partial?

Authorized research-note path: `docs/research/skills/to-spec/RP-to-spec-20260725-01.md`.

## Re-entry Contract

Before Research Pass dispatch:

1. verify `HEAD` remains `b9750babea998c4bc0f5809972a8651934218eca`;
2. re-hash every local authority in the manifest and compare exact bytes, SHA-256, and Git blob identities;
3. extract only the content strictly between `<!-- BEGIN TO-SPEC-2026-07-25-M0-FINGERPRINTED-CONTENT -->` and `<!-- END TO-SPEC-2026-07-25-M0-FINGERPRINTED-CONTENT -->`, excluding both marker lines, and verify the recorded fingerprint;
4. verify the only Prompt 1 mutation is this checkpoint and the authorized future Research note path remains exactly the one recorded above;
5. revisit only an exact, expected authority decision delta. Any unexpected `HEAD`, authority, identity, or fingerprint drift requires a fresh blind Prompt 1 pass.

<!-- END TO-SPEC-2026-07-25-M0-FINGERPRINTED-CONTENT -->

## Content Fingerprint

- Bounds: exact bytes after the LF ending `<!-- BEGIN TO-SPEC-2026-07-25-M0-FINGERPRINTED-CONTENT -->` through the byte immediately before `<!-- END TO-SPEC-2026-07-25-M0-FINGERPRINTED-CONTENT -->`; marker lines are excluded.
- Algorithm: SHA-256 over the exact bounded UTF-8 bytes as stored.
- Digest: `94521f7c73c756fbeb53de3a04a551007fa473a44108683dd760e42ff5b185b1`

<!-- END TO-SPEC-2026-07-25-PROMPT1-CAPSULE -->
