# Repo Bootstrap M0 Checkpoint

Campaign: `repo-bootstrap-fce-20260727-r2`
Skill: `repo-bootstrap` (`SK-001`)
Composition epoch: `FCE-20260727-01`, revision `2`
Starting Git HEAD: `297f6aaa474479c46153a324d6f49b9f3817617e`
Prompt section fingerprint: `sha256-v1:93ea1616aed7ee59ca0d3a24dfe5a79706ec0ba730c3d78fe3ab8de149f527f8`

Content fingerprint: `sha256-v1:f92d52e18a3b06248b3e1da377cc25a87201f530708222379e9922a68c532dfa`

<!-- repo-bootstrap-prompt1-m0:v1:begin -->
## Intended Contract

### Outcome

Reconcile one target repository's verified setup surface before engineering
work. The surface consists of:

- a short `AGENTS.md` primer with verified commands, owning pointers, local
  invariants, and a compatible setup-schema marker;
- the repo-owned engineering contract, tracker contract, label mapping,
  domain-routing guidance, and `.tmp/`/`.scratch/` work-state policy;
- compatible per-file and aggregate setup identities plus a complete-surface
  validator; and
- when applicable, every mapped and fixed label in the configured tracker.

This is reconciliation, not replacement: preserve compatible local choices
and unrelated work, propose only the exact missing, incompatible, or outdated
delta, apply only an authorized delta, and verify it by read-back.

### Invocation And Exclusions

`repo-bootstrap` is explicit-only. It runs only after a human names it with a
bounded target repository, including after another skill recommends it and
stops.

Positive entry: a selected engineering route needs a missing, incompatible, or
outdated setup surface.

Nearest exclusions:

- route choice belongs to `skill-router`;
- a bounded source-answerable question belongs to `research`;
- a module, interface, seam, adapter, ownership-boundary, or caller-facing
  test-surface decision belongs to `codebase-design`;
- implementation slicing and dependency order belong to `to-tickets`;
- domain language, `CONTEXT.md`, `CONTEXT-MAP.md`, and ADR truth belong to
  `domain-modeling`;
- work-item lifecycle belongs to tracker-using skills and the tracker contract;
- pack acceptance, epoch Lock, installation, Git delivery, and another skill's
  decision, proof, Return, or completion are outside this skill.

### Authority And Relationships

The caller owns the bounded target Source Trace and inspection/mutation
authority. `repo-bootstrap` owns setup inventory, compatibility judgment,
the exact reconciliation proposal, authorized setup-file changes, missing-label
provisioning, complete validation, mutation read-back, and its verified report.

Inspection authority permits an audit and proposal, not mutation. Before any
file or tracker mutation, the exact bounded delta requires explicit approval.
External mutation additionally requires a resolved configured tracker,
authenticated transport, and authority for that target.

`handoff`, `implement`, `parallel-implement`, `skill-router`, `to-spec`,
`to-tickets`, `triage`, and `wayfinder` may only recommend `repo-bootstrap` and
stop. Their recommendation supplies one target, reason, and caller-owned Source
Trace; it does not execute, mutate, resume, or complete this skill. After a
later explicit invocation, `repo-bootstrap` returns its own verified report and
does not resume the recommending workflow.

### Safe Failure, Completion, Order, Compatibility, And Safety

Safe failure returns the exact incompatible, unavailable, unresolved, or
unauthorized boundary; the proposed but unapplied delta; any operations already
applied; and the safest recovery. A partial read, validator alone, or
unverified external mutation never establishes compatibility.

Complete only when every required setup owner is compatible, every authorized
transition has been read back at its authoritative location, complete setup
validation passes, unrelated work is preserved, and the report names exact
changed and unchanged surfaces. Otherwise return the exact blocker.

Required order:

1. Resolve target, Source Trace, tracker, and authority.
2. Inventory all applicable setup and state locations without mutation.
3. Compare with the supported contract and classify every surface.
4. Produce one exact proposal and obtain approval.
5. Preflight all required local and external transitions.
6. Reconcile local setup files while preserving compatible local choices.
7. Provision only missing mapped and fixed labels.
8. Read back every changed authoritative location.
9. Validate the complete surface and return the verified report or exact
   partial-failure packet.

Compatibility and safety rules:

- the aggregate setup identity is a compatibility contract, not a pack version;
- the primer points to owning docs instead of copying their procedures;
- engineering, tracker, labels, and domain routing remain in their owners;
- setup does not create missing domain docs or alter domain truth;
- only missing labels are created, after approval, through configured transport;
- working tree, index, committed tree, and unrelated state are preserved;
- this skill never stages, commits, pushes, resets, or discards work; and
- structural validation does not replace mutation read-back.

## State-Location Ledger

| State | Authority | Allowed transition and order | Failure Return |
| --- | --- | --- | --- |
| Supported setup contract | Pack-owned seeds, identities, aggregate schema, and validator | Read exact identities before target comparison | Unavailable/inconsistent contract; no mutation |
| Primer | Target working-tree `AGENTS.md` | Reconcile approved setup surface; reread marker, commands, pointers, invariants | Exact missing, incompatible, or conflicting surface |
| Engineering contract | Target `docs/agents/engineering-contract.md` | Reconcile after approval; reread identity and owners | Exact conflict |
| Tracker contract | Target `docs/agents/issue-tracker.md` | Resolve tracker, then reconcile and reread | Unresolved tracker or lifecycle conflict |
| Label mapping | Target `docs/agents/triage-labels.md` | Resolve before remote delta; reconcile and reread | Invalid, incomplete, or conflicting mapping |
| Domain routing | Target `docs/agents/domain.md` | Reconcile routing only; reread topology behavior | Incompatible routing or truth-mutation request |
| Domain truth | Target `CONTEXT.md`, `CONTEXT-MAP.md`, and routed ADRs | Read only when topology requires; preserve bytes | Return `domain-modeling` boundary |
| Work-state policy | Setup-owned primer/engineering passages | Reconcile policy; never clean or stage work | Conflict or threatened unrelated work |
| Working tree | Target working tree | Approved setup edits only; refresh, diff, and reread | Applied/conflicting paths and recovery |
| Git index | Target index | No transition; require unchanged before/after | Unexpected drift; stop |
| HEAD/committed tree | Target Git object state | No transition; require identical HEAD | Exact transition; stop |
| Tracker labels | Configured tracker remote | Create approved missing labels only; refetch | Applied/failed labels and recovery |
| Tracker items | Configured remote issues/PRs | No mutation | Unauthorized mutation boundary |
| `.tmp/`/`.scratch/` | Target local state | No cleanup, staging, or delivery | Exact threatened or changed path |

## M0 Semantic Unit Ledger

| Unit | Behavior and neutral expression | Entry / wrong condition | Failure Return | Proof |
| --- | --- | --- | --- | --- |
| M0-01 | Resolve target, Source Trace, tracker, and authority before inspection. | Entry: explicit setup reconciliation. Wrong: routing, research, design, tickets, or another owner. | Name owner or unresolved target/authority; no mutation. | V-01, V-07–V-10 |
| M0-02 | Inventory every applicable owner, identity, tracker, Git location, and topology once. | Entry: target and inspection authority resolved. Wrong: location inapplicable. | Mark exact unavailable location; do not infer. | V-01–V-04, V-11, V-12 |
| M0-03 | Classify each surface and derive only the necessary delta. | Entry: complete inventory. Wrong: compatible local or foreign difference. | Return conflict and non-destructive recovery. | V-01–V-03, V-11 |
| M0-04 | Present exact local/remote delta; mutate only after approval and preflight. | Entry: safe non-empty delta. Wrong: audit, no-op, unauthorized, or unready. | Proposal or blocker with zero mutation. | V-02–V-05 |
| M0-05 | Apply approved setup-owned local changes only. | Entry: approved delta and successful preflight. Wrong: domain truth, index, HEAD, or unrelated work would change. | Applied/blocked paths; stop further mutation. | V-01, V-02, V-11, V-12 |
| M0-06 | Create only missing required labels and refetch them. | Entry: missing labels plus external authority. Wrong: current, inapplicable, or unavailable. | Missing/applied/failed labels and recovery. | V-03, V-05, V-06 |
| M0-07 | Reread files/labels, check Git preservation, and run complete validation. | Entry: changed or current surface. Wrong: read-back or scope incomplete. | Return unverified/partial; never claim completion. | V-01–V-03, V-05, V-06, V-12 |
| M0-08 | Return exact compatible, changed, unchanged, blocked, preserved, proof, and residual surfaces; stop. | Entry: verified surface or exact blocker. Wrong: downstream execution requested. | Return boundary with downstream work unstarted. | V-01–V-12 |

## Runtime-Clause Specification And Cut Audit

| Clause | Units | Required behavior and cut reason |
| --- | --- | --- |
| RC-01 Entry/exclusion | M0-01 | Explicit-only entry, nearest owners, and eight stopping edges own invocation safety. |
| RC-02 Authority gate | M0-01, M0-04 | Inspection/mutation separation, approval, and preflight own safe failure. |
| RC-03 Inventory | M0-02 | Complete applicable owners and locations own setup coverage. |
| RC-04 Compatibility | M0-03 | Exact identities plus local-choice preservation prevent blind replacement. |
| RC-05 Local reconciliation | M0-05 | Approved setup-owned edits realize CAP-001 local mutation. |
| RC-06 External provisioning | M0-06 | Missing-label creation realizes the external setup contract. |
| RC-07 Proof/read-back | M0-07 | Validation, read-back, and preservation establish claimed state. |
| RC-08 Return/completion | M0-08 | Exact report, blocker, stop, and completion satisfy SK-001. |

No clause is justified only by current behavior, research, historical evidence,
candidate wording, installation, delivery, or pack acceptance.

## Complete M0 Viability Suite Design

No behavioral sample is executed in Prompt 1.

| Case | Initial facts | Required observable result |
| --- | --- | --- |
| V-01 Missing local surface | Authorized target; one owner absent; preflight ready | Exact proposal; after approval add only missing owned surface; read-back, validation, report |
| V-02 Incompatible/outdated | Identity conflict plus unrelated local content | Minimal proposal; approval gate; preserve compatible and unrelated bytes |
| V-03 Current compatible | All owners and labels compatible | Verified no-op; zero mutation |
| V-04 Inspection only | No mutation authority | Safe inventory, exact unapplied delta, zero mutation |
| V-05 External preflight failure | Labels missing; transport/authority unavailable | Block before avoidable local mutation; exact blocker and recovery |
| V-06 Missing labels | Valid mapping, approval, subset missing | Create only missing labels; refetch; preserve existing labels |
| V-07 Research negative (PS-003) | Bounded source-answerable question | Exclude setup; identify `research`; no inventory/mutation |
| V-08 Design negative (PS-007) | One bounded design decision | Exclude setup; identify `codebase-design`; no mutation |
| V-09 Ticket negative (PS-012) | Settled source needs slices/order | Exclude setup; identify `to-tickets`; no mutation |
| V-10 Router/edge boundary (PS-025; REL-012/015/032/059/079/083/085/089) | Caller detects setup precondition or user asks only for route | One recommendation; setup remains unstarted until explicit invocation |
| V-11 Domain ownership | Domain docs absent or truth change requested | Routing only; no truth creation/change; exact owner boundary |
| V-12 Dirty state | Unrelated working-tree/index changes | Preserve unrelated work; index/HEAD unchanged; exact report |

Later proof lanes: deterministic identities; focused owner/pointer/marker
semantics; clean/fail/restored validator control; exact file and Git read-back;
connector label read-back; and fresh behavioral cases for invocation, approval,
preservation, failure, stopping, and completion. Structural checks never
substitute for behavioral or mutation proof.

## Local Source Identity Manifest

| Source | Identity |
| --- | --- |
| Deploy Prompt 1 section | `sha256-v1:93ea1616aed7ee59ca0d3a24dfe5a79706ec0ba730c3d78fe3ab8de149f527f8` |
| `docs/synthesis/skill-pack.md` | `sha256-v1:74e70c063cdcd5672680e1043e974dfc48d7026c438822948118f163ad6402a0` |
| Admission slice | `sha256-v1:37ad7e952f8864229bec8f32bcaf97bda6029367a4fcd35a1c16c321cacde552` |
| `AGENTS.md` | `sha256-v1:d93d25a1e8bf09f01fb9eee054682940539a072c5f489e99435dbe6e10cde314` |
| `CONTEXT.md` | `sha256-v1:1267d137661b9f023b30c776bf6190eb9eaf4de607ed53b5891fae31e53dc169` |
| Engineering contract | `sha256-v1:c3d52491ca8b98f229965e2602212fc4474ef2fedf8be73bc8f08c24300ef829` |
| Domain routing | `sha256-v1:94ccdc414542b44be2fe38d7ebe2e59fd809c09848642243c3a805749c6adb99` |
| Tracker contract | `sha256-v1:d79c8dbdc0e3c77583b461ac2d50eb678d0ce77aed69a9e759e3c0818646f933` |
| Label mapping | `sha256-v1:06f253d31ea852376950b4b8c163f2a1e60c5be131492b3cb76d05be92b58ded` |
| Relationship map | `sha256-v1:c2fde0afb864c2dc19f699d2ca5ffc9ec14cbc1950c3c8a4b20d382500a8c4fe` |
| ADR-0008 | `sha256-v1:5fa8981188f8ac513e1d192b14391ee1ac44dc3ffc24d036a749feedcd306fb1` |
| ADR-0009 | `sha256-v1:26f392e8c645f587052681e4f401b8d078cccf87519b58b1a9008ffd1d8213a2` |
| Campaign manifest | Contract `b8825d1a0542a272c1dccebd67685b276c4a2ad57d7fa9a240e9a1ddf1746e4a`; campaign `903e31d7a397d508145e5a6387d411cf7d0ba096468ca60ae9c6b3e29b296a93` |

## Audit Coverage

- Affected: CAP-001/SK-001 outcome, invocation, setup state/mutations, eight
  relationships, validator/labels, Return, and completion.
- Preserve: owning docs' detail, caller Source Trace/exit, compatible local
  configuration, and unrelated work.
- Owned elsewhere: domain truth, routing, research, design, tickets, work-item
  lifecycle, pack proof, installation, delivery, and epoch Lock.
- Historical evidence: none inspected or admitted.
- Drift: none observed in the frozen local-authority identity set.
- Not applicable: current/experimental runtime, installed mirror, upstream,
  prior synthesis/research/evaluations/campaigns, and behavioral sampling.

## Research Questions

Authorized note:
`docs/research/skills/repo-bootstrap/RP-repo-bootstrap-FCE-20260727-01-r2.md`.

Compatibility and reconciliation:

- How should compatible local configuration be distinguished from managed
  setup drift?
- What is the smallest safe reconciliation beside user-owned content, and when
  must reconciliation stop?

Authority and durable state:

- How should local and external approval scopes be made auditable?
- Which preflight patterns minimize partial local-plus-remote setup?
- What read-back distinguishes accepted mutation from partial or stale state?

Verification and completion:

- How can aggregate identities establish compatibility without overstating
  behavioral correctness?
- What smallest negative control proves the validator detects its intended
  violation?
- What report shape exposes changed, unchanged, blocked, and preserved state
  without duplicating owning contracts?

Context ownership:

- How can setup preserve routing without creating domain truth?
- When is additional topology context necessary, and when should it remain
  unloaded?

## Limitations

- No current or experimental target runtime, target synthesis, research,
  upstream package, installed mirror, historical campaign/evaluation/transcript,
  or target-repository runtime was inspected.
- No behavioral case, validator, campaign verification, installation, tracker
  mutation, Git mutation, or full suite ran.
- This freezes behavior-complete intent and viable suite design only. Exact
  runtime wording, current compatibility, method support, and efficacy remain
  unproved.
- Fixtures, model/host configuration, registrations, candidate bytes, and
  acceptance thresholds belong to later stages.
- The admitted slice has no hard-proof predecessor.

## Decision

Every viability axis is settled. Each trigger, authority, state transition,
relationship, safe failure, Return, and completion condition has one owner.
Every clause maps to CAP-001 or a required local contract, and the suite can
test the intended contract without Prompt 1 sampling.

Decision: `ready-for-research`.
<!-- repo-bootstrap-prompt1-m0:v1:end -->
