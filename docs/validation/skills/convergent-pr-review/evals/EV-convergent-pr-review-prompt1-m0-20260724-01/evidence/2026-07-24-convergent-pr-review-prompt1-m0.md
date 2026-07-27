# Convergent PR Review Deploy Prompt 1: M0 Checkpoint

- Campaign epoch: `2026-07-24`
- Operation: `writing-great-skills` Audit
- Starting Git `HEAD`: `f3be70c31dd8f2ae9f12a75248065ef313790bda`
- Target: `convergent-pr-review`
- Decision-bearing region: the content between the M0 checkpoint markers below
- Fingerprint rule: SHA-256 of the exact UTF-8 bytes between the marker lines,
  excluding both marker lines and their adjacent single line feeds
- Content fingerprint: `sha256:469734af7b346c0f327d07fbd2a001d8b3f76cd985aa7c9468a53c6944326e4e`

<!-- BEGIN M0 CHECKPOINT -->

## Intended Contract

`convergent-pr-review` is the root-owned terminal release gate for one immutable
local pull request, release candidate, or bounded high-risk diff. It captures
one review snapshot, traces Standards and the caller-authorized Spec as
separate axes, obtains direct fresh-context review passes when capacity allows,
and lets the root admit findings only after direct verification against the
snapshot and the shared Finding Contract. It returns exactly one read-only
release decision and leaves repair, mutation, successor snapshots, tracker
work, merge, publication, and delivery to the caller.

| Axis | Minimum contract |
| --- | --- |
| Outcome | One terminal, Lock-usable release decision for the exact immutable review snapshot, with admitted findings, coverage, skipped checks, and residual risk. |
| Invocation | Apply to a local PR, release candidate, or caller-bounded high-risk diff selected for independent review. The skill is implicitly invocable from that observable request or an authorized caller packet. |
| Exclusions | Ordinary branch, WIP, staged, or since-X review remains with `review`. An immutable repository-baseline correctness, domain-robustness, methodology, model-risk, leakage, validation, analytics, or performance audit remains with `audit-codebase`. Implementation, repair, tracker mutation, PR mutation, merge, publication, and Git delivery are outside the skill. |
| Root authority | The top-level root alone pins the snapshot, defines reviewer lanes, dispatches direct reviewers, owns the candidate ledger, verifies evidence, admits findings, resolves duplicates, assigns the terminal decision, and returns control. Delegated invocation stops before Pin with `incomplete`. |
| Caller authority | The caller owns the Charter, commitment boundary, fixed point when supplied, target, `Spec required`, Source Trace, required proof, review mode, carried finding IDs, Repair delta, risk acceptance, and all later mutation or successor-snapshot authority. |
| Reviewer authority | A direct reviewer may inspect only its factual brief and immutable snapshot, perform safe read-only verification, and return candidates. It does not mutate, spawn, see peer conclusions, admit findings, decide release, or start a successor. |
| Read-only safety | Files, Git state, dependencies, trackers, PR state, external systems, and successor snapshots remain unchanged. Read-only verification must not alter the target or its environment. |
| Modes | `initial` judges the complete selected snapshot. `remediation` requires the original Charter, prior snapshot identity, carried IDs, caller-owned Repair delta, remaining acceptance, fixed point, and successor target, and closes only carried outcomes plus affected seams. `assurance` rechecks an already reviewed immutable target for a caller-stated reason without creating repair authority. |
| Standards axis | Trace repository instructions, routed guidance, maintained configuration, meaningful nearby conventions, and the fallback smell baseline only when local Standards are thin. |
| Spec axis | Respect `Spec required: yes \| no`. Trace caller-supplied source first, then captured-commit material, then one matching repository source. A missing, conflicting, unreadable, or unresolved required Spec makes coverage `incomplete`; an absent optional Spec is explicitly skipped. |
| Finding admission | Apply `review/FINDING-CONTRACT.md` after candidate generation. Admit only a directly verified Anchor, Reach, Evidence, Impact, and Proportion. Preserve stable IDs through remediation. Evidence gaps are incomplete coverage, not findings. |
| Advisories | Only when enabled by the caller, apply `review/ADVISORY-CONTRACT.md` and keep verified nonblocking opportunities separate. Advisories have no severity, never alter confidence or a terminal decision, and grant no repair authority. |
| Independent coverage | Direct reviewer contexts are fresh and fact-only. Normal capacity is at least two completed fresh reviewers. Exact reduced-capacity fallbacks keep required axes covered, disclose reduced confidence, and never produce plain `pass`. |
| Safe failure Return | Routing, root-guard, target, fixed-point, source, capture, reviewer, evidence, protocol, coverage, report, or drift failure returns `incomplete` with the exact blocker and verified partial evidence. A verified blocking finding returns `blocked`. |
| Terminal decisions | `pass`, `pass with residual risk`, `blocked`, or `incomplete`. Plain `pass` requires complete coverage, normal independent capacity, no admitted blocker, no decision-bearing residual risk, and no drift. |
| Completion | Every applicable axis and lens is covered or explicitly blocks; every candidate is accepted, rejected, duplicate, or resolved from dispute; every carried ID is disposed; drift checks pass; the decision packet is complete; and control returns to the caller with mutation and successor-snapshot authority both `none`. |
| Irreversible order | Route and root guard precede Pin; Pin precedes source tracing and dispatch; independent judgment precedes root verification and admission; admission precedes severity and decision; drift read-back precedes Return. No later stage may retroactively change the captured snapshot. |
| Compatibility | Preserve caller packets from `review`, `implement`, and `parallel-implement`; the shared finding and advisory interfaces; separate Standards and Spec axes; the three review modes; root-only direct fresh-context fanout; exact capacity disclosures; the five-state candidate ledger; and the four terminal decisions. |

## State-Location Ledger

The runtime reads durable repository and optional PR state but owns no durable
mutation. Snapshot capture and ledgers may remain in root context; they do not
authorize repository artifacts.

| State or artifact | Owner and authoritative location | Allowed transition and required order | Read-back | Failure Return | M0 units and viability cases |
| --- | --- | --- | --- | --- | --- |
| Caller review packet | Caller; invocation context or caller-owned durable packet | Read completely before Pin; freeze the supplied Charter, mode, target, fixed point, Spec requirement, proof, skips, and risk. Do not rewrite it. | Echo identities and required fields in the final report. | Missing or contradictory decision-bearing fields -> `incomplete`. | M0-02 through M0-05; V02, V05-V07 |
| Fixed point | Caller-supplied Git object, otherwise the repository-resolved default-branch merge base | Resolve once before target comparison and retain the exact object identity. Later movement of a symbolic baseline ref does not replace the pinned object. | Verify that the recorded object and its captured content remain available; do not reinterpret later ref movement as target drift. | Ambiguous or unavailable fixed point -> `incomplete`. | M0-06; V08 |
| Git-addressed target | Caller-supplied commit/tree or resolved local PR head and diff | Resolve to exact commit/tree and capture all selected diff bytes before tracing or dispatch. | Re-resolve the recorded object identity and verify captured content identity before Return. | Missing, empty, partial, or identity-mismatched target -> `incomplete`. | M0-06, M0-18; V08, V21 |
| Connected PR target, when supplied | Caller-selected PR; connector or local Git metadata plus exact base/head objects and diff content | Read metadata and content without changing PR state; pin exact base/head and diff before reviewer work. | Re-read only the fields needed to detect target-content or head drift. | Unavailable required PR surface or changed target identity -> `incomplete`. | M0-06, M0-18; V09, V21 |
| Live local target, when explicitly selected | Working tree and index: `HEAD`, index tree, staged diff, unstaged diff, status, and in-scope untracked paths and content | Capture the complete composite before tracing or dispatch; hash untracked bytes; reviewers inspect only captured content. | Recompute every captured surface before Return and compare with the pinned composite. | Any target-surface drift or incomplete capture -> `incomplete`; do not recapture. | M0-06, M0-18; V10, V21 |
| Standards sources | Repository instructions, routed guidance, maintained configuration, test/tool docs, meaningful nearby conventions, and conditional shared smell baseline | Trace after Pin. Load the fallback baseline only when repository Standards are thin. | Record exact sources and skipped optional checks. | Missing required Standards evidence -> `incomplete`; optional unavailable checks -> residual risk. | M0-08; V11 |
| Spec sources | Caller source, captured-commit references, or one matching repository source in that order | Trace after Pin under the supplied `Spec required` value. | Record exact source or `skipped`. | Missing/conflicting required Spec -> `incomplete`; absent optional Spec -> skip. | M0-09; V12-V13 |
| Reviewer briefs and returns | Root-owned ephemeral dispatch and return packets | Freeze one fact-only brief per lane after coverage planning; dispatch direct fresh contexts; collect typed returns before admission. | Verify lane identity, freshness, snapshot identity, assigned axis/lens, read-only boundary, coverage, and packet completeness. | Protocol breach or missing decision-bearing fields -> zero credit and affected coverage `incomplete` unless safely rerun within the same snapshot. | M0-10 through M0-13; V14-V17 |
| Candidate ledger | Root-owned ephemeral ledger keyed by stable candidate ID | Create from reviewer observations; transition `candidate` to `accepted`, `rejected`, `duplicate`, or `disputed`; resolve every dispute from evidence before decision. | Reconcile every return item and carried ID exactly once. | Unresolved candidate, dispute, duplicate, or carried ID -> `incomplete`. | M0-14 through M0-16; V18-V19 |
| Finding and advisory records | Finding Contract and, when enabled, Advisory Contract; root-owned report content | Verify before admission; finding admission precedes severity; advisory admission stays separate. | Recheck each accepted record against the snapshot and owning schema. | Unverifiable required finding claim -> affected coverage `incomplete`; advisory uncertainty -> omit or record skipped optional verification. | M0-15 through M0-17; V18-V20 |
| Terminal report | Root-owned inline Return to caller | Decide only after ledger closure and drift read-back. No persisted report is required by M0. | Reconcile snapshot, sources, coverage, decisions, findings, advisories, skips, residual risk, and authority fields. | Malformed or internally inconsistent report -> `incomplete`. | M0-19, M0-20; V22-V25 |

## Semantic Behavior Unit Ledger

| Unit | Trigger and owned behavior | Local authority | Cheapest neutral expression | Entry and wrong-condition cases | Failure Return | Proof |
| --- | --- | --- | --- | --- | --- | --- |
| M0-01 | Route only a local PR, release candidate, or bounded high-risk diff; reject ordinary diff and repository-baseline audit ownership. | User request; router; relationship map; `review`; `audit-codebase`; README | State the positive target and nearest exclusions in the description and first gate. | Entry: selected high-risk release diff. Wrong: ordinary diff or open-ended baseline audit. | `incomplete` routing blocker; for a baseline audit, recommend `audit-codebase` and stop. Never hand back to `review` after the high-risk route starts. | Structural invocation/exclusion check plus V01-V03. |
| M0-02 | Enforce top-level root ownership before Pin. | Root-only relationship boundary; compatibility tests; user request | Check invocation ownership first. | Entry: top-level root. Wrong: delegated worker or nested reviewer invocation. | `incomplete` before Pin with root-only blocker. | Structural guard-order check and V04. |
| M0-03 | Preserve the global read-only boundary. | Engineering contract; review relationship boundary; user request | Permit inspection and safe verification only; enumerate protected mutation surfaces once. | Entry: read-only review. Wrong: request or attempted file, Git, dependency, tracker, PR, external, repair, or successor mutation. | `incomplete` at the violating gate; report observed state and do not continue mutation. | Mutation-boundary inspection and V25. |
| M0-04 | Admit `initial` mode and freeze its complete caller packet. | `review`; `implement`; `parallel-implement`; runtime compatibility tests | Require Charter, Source Trace, fixed point/target, Spec requirement, required proof, skips, and risk. | Entry: new exact snapshot. Wrong: incomplete or contradictory packet. | `incomplete` before reviewer dispatch. | Packet contract check and V05. |
| M0-05 | Admit `remediation` and `assurance` without widening their authority. | `review`; `parallel-implement` ledger and caller contracts; compatibility tests | Remediation carries original Charter, prior identity, IDs, Repair delta, remaining acceptance, fixed point, and successor; assurance keeps the accepted target and caller reason. | Entry: exact carried state. Wrong: changed Charter, missing IDs/delta, unproved successor, changed assurance target, or mode ambiguity. | `incomplete`; return exact missing or conflicting identity. | Mode fixtures V06-V07. |
| M0-06 | Pin one complete immutable fixed point and target before other review work. | Engineering contract fixed-point/review-snapshot vocabulary; review caller; compatibility tests | Resolve exact Git objects or capture the full live composite and identities. | Entry: one resolvable nonempty target. Wrong: ambiguous, empty, partial, or multiple targets. | `incomplete`; do not infer or silently switch target. | Identity read-back and V08-V10. |
| M0-07 | Freeze the applicable lens and coverage plan before dispatch. | Engineering proof discipline; caller Charter; user request | Map every required axis/lens to sources, snapshot surfaces, proof seams, and one owner. | Entry: pinned snapshot and settled Charter. Wrong: unbounded lens, missing required axis, or no evidence seam. | `incomplete` for the uncovered cell. | Coverage-matrix integrity and V14. |
| M0-08 | Trace Standards independently. | Engineering contract; `review`; smell baseline contract | Read repository Standards first; use the fallback only when they are thin. | Entry: Standards axis. Wrong: treating fallback preference as governing or skipping available local Standards. | `incomplete` when required Standards cannot be resolved; otherwise name optional skips. | Source precedence and V11. |
| M0-09 | Trace Spec independently under `Spec required`. | `review`; `implement`; `parallel-implement`; compatibility tests | Use caller source, captured-commit reference, then one repository source; record `skipped` only when optional. | Entry: yes/no value supplied or standalone default. Wrong: missing required Spec or inferred intent from implementation/tests. | `incomplete` when required; explicit skip when optional. | Source precedence and V12-V13. |
| M0-10 | Dispatch direct fresh-context reviewers with factual isolated briefs. | User request; relationship boundary; compatibility tests; AGENTS delegation policy | Use `fork_turns="none"`; include immutable snapshot, assigned axis/lens, sources, read-only boundary, and typed return only. | Entry: frozen coverage plan and available direct capacity. Wrong: inherited conclusions, peer outputs, candidate cues, nested spawn, or shared writes. | Invalid lane gets zero credit; rerun only if the same snapshot and unbiased brief remain valid, else `incomplete`. | Brief diff/identity check and V14-V15. |
| M0-11 | Require each reviewer to judge only its assigned axis/lens and return a complete typed packet. | Compatibility test contract; review relationship | Return `status`, `axis`, `lens`, `coverage`, `findings`, `advisories`, `skipped checks`, and `blockers`. | Entry: assigned reviewer. Wrong: terminal release vote, out-of-lens claims, missing coverage, or mutation. | Zero credit and affected coverage gap. | Schema check and V15. |
| M0-12 | Apply exact completed-reviewer capacity modes without pretending independence. | User request; compatibility tests; root-owned orchestration boundary | At least two fresh completed reviewers is normal. Exactly one adds separated root coverage and reduced confidence. Zero uses separated root passes and reduced confidence. | Entry: completed-return count after bounded capacity reconciliation. Wrong: counting dispatches, failed lanes, duplicates, or inherited contexts as completed fresh reviewers. | Any uncovered required lens/evidence axis -> `incomplete`. Reduced-capacity execution never returns plain `pass`. | Capacity fixtures V16-V17. |
| M0-13 | Keep Standards and Spec judgment separate and cover every required lens. | Engineering contract; `review`; relationship map | Partition factual reviewer briefs or root fallback passes so conclusions from one axis do not seed the other. | Entry: applicable axis/lens. Wrong: merged rubric, cross-axis ranking pressure, or optional Spec promoted to required. | `incomplete` for contaminated or uncovered required coverage. | Isolation inspection and V14-V17. |
| M0-14 | Normalize all observations into one root-owned candidate ledger. | Root-only relationship boundary; compatibility tests | Assign stable IDs and one state: `candidate`, `accepted`, `rejected`, `duplicate`, or `disputed`. | Entry: reviewer or root-pass observation. Wrong: untracked observation, lost duplicate, unstable carried ID, or reviewer-admitted finding. | `incomplete` until every item and carried ID has one reconciled disposition. | Ledger completeness and V18. |
| M0-15 | Root-verify each finding candidate against the immutable snapshot and shared Finding Contract. | `review/FINDING-CONTRACT.md`; engineering proof discipline | Verify Anchor, Reach, Evidence, Impact, and Proportion before severity. | Entry: candidate observation. Wrong: speculative, preference-only, unsupported-environment, adjacent cleanup, missing-evidence, or optional-hardening claim. | Reject unsupported candidate; required unavailable evidence becomes incomplete coverage, not a finding. | Contract gate trace and V18-V19. |
| M0-16 | Resolve duplicates and disagreements from evidence, not votes. | Root-owned verification; semantic-proof contract | Compare claims, anchors, scenarios, and evidence; preserve contrary evidence; consolidate true duplicates while retaining provenance. | Entry: overlapping or conflicting candidates. Wrong: majority vote, agreement as proof, silent discard, or unresolved dispute. | Unresolved material dispute -> `incomplete`; verified blocker may still yield `blocked` only when its own admission is complete. | Candidate trace and V18-V19. |
| M0-17 | Admit optional advisories separately and keep them nonblocking. | Shared Advisory Contract; relationship map; compatibility tests | Load the advisory contract only when enabled; verify scenario, evidence, and plausible benefit; keep a separate ledger. | Entry: caller enabled advisories. Wrong: disabled, violated contract mislabeled advisory, severity assignment, or decision/confidence influence. | Omit unsupported advisory or record optional skipped verification; never change the release decision. | Advisory/no-demotion checks and V20. |
| M0-18 | Re-read every target surface needed to detect snapshot drift. | Compatibility tests; review snapshot contract | Compare exact Git target identity or all live composite surfaces: `HEAD`, index tree, staged diff, unstaged diff, status, and untracked paths/content. | Entry: ledger closed, before decision Return. Wrong: changed target or attempted recapture. Baseline symbolic-ref movement alone is not target drift. | `incomplete`, preserve verified partial evidence, and do not recapture. | Drift fixtures V21. |
| M0-19 | Derive exactly one terminal decision from admitted blockers, coverage, independence, and residual risk. | Caller Lock contracts; Finding Contract; compatibility tests | `blocked` for admitted blocking findings; `incomplete` for unresolved required coverage/protocol/drift; `pass with residual risk` for complete nonblocking review with material residual or reduced capacity; plain `pass` only under the strict clean/full-capacity condition. | Entry: verified closed ledger and no drift. Wrong: unresolved dispute, unaccepted blocker, advisory-driven decision, or plain pass under reduced capacity. | Return the corresponding non-accepting status; never soften a blocker into residual risk. | Decision-table fixtures V22-V24. |
| M0-20 | Return the complete terminal packet to the caller and stop. | `review`, `implement`, `parallel-implement`, relationship map, Finding Contract | Report mode, fixed point, snapshot identity, target, sources, capacity/confidence, coverage, admitted findings, carried dispositions, advisories when enabled, skips, residual risk, drift, and authority fields. | Entry: terminal decision. Wrong: missing identity/evidence, repair instructions treated as authority, successor work, or caller not restored. | `incomplete` report blocker if packet cannot be made internally consistent. | Return-schema/read-back check and V25. |

## Runtime-Clause Specification

| Clause | M0 units | Neutral minimum runtime expression |
| --- | --- | --- |
| C01 Invocation and exclusions | M0-01 | The description names one local PR, release candidate, or bounded high-risk diff; it excludes ordinary diff review and repository-baseline audit work. |
| C02 Root and read-only guard | M0-02, M0-03 | A first gate requires the top-level root and holds a complete read-only mutation boundary through Return. |
| C03 Mode and caller packet | M0-04, M0-05 | One compact mode branch preserves initial, remediation, and assurance inputs without copying caller procedures or granting Repair. |
| C04 Pin and state custody | M0-06, M0-18 | Pin exact fixed-point and target identities once; capture complete live state when applicable; compare target surfaces before Return without recapture. |
| C05 Source and coverage trace | M0-07 through M0-09 | Map required axes/lenses, trace Standards and Spec separately under local precedence, and expose unavailable evidence. |
| C06 Independent reviewer protocol | M0-10 through M0-13 | Dispatch fact-only direct fresh contexts, require the typed return, and apply explicit normal/one/zero completed-reviewer modes with honest confidence. |
| C07 Candidate convergence | M0-14 through M0-16 | Root owns one five-state ledger, applies the shared finding gates, resolves duplicates and disputes from evidence, and closes every carried ID. |
| C08 Optional advisory branch | M0-17 | A single conditional pointer loads the shared advisory contract only when enabled and keeps advisories outside findings, confidence, and decision. |
| C09 Terminal decision and Return | M0-19, M0-20 | Derive one of four decisions from verified state, return the complete Lock-usable evidence packet, restore caller control, and stop with no mutation or successor authority. |

## Clause-To-Intent Cut Audit

Every proposed runtime clause maps to the viability floor or a required local
compatibility contract:

- C01-C03 own invocation, authority, exclusions, caller obligations, and safe
  early Return.
- C04 owns immutable state custody and drift safety.
- C05-C07 own separate judgment, proof, independent coverage, finding
  admission, and convergence.
- C08 preserves the locally owned optional advisory relationship without
  affecting release.
- C09 owns the terminal decision, report, completion, and stop boundary.

The following are excluded from M0 because no local minimum contract grants
them: implementation or Repair procedure; tracker or PR mutation; staging,
commit, merge, push, publication, or deployment; consensus voting; reviewer
release votes; auto-fixing; a repository-wide audit lens; upstream-derived
method names; current-runtime clauses protected only by existence; historical
candidate language; research claims; and behavioral-effectiveness claims.

## M0 Viability Suite

| Case | Condition | Required observable result | Proof lane |
| --- | --- | --- | --- |
| V01 | Direct request for independent review of one local PR or bounded high-risk release diff | Invoke M0 and begin root guard/Pin. | Invocation behavior sample |
| V02 | Ordinary WIP, staged, branch, or since-X diff | Return routing mismatch without starting a competing ordinary pass. | Invocation wrong-condition sample |
| V03 | Immutable repository-baseline audit request | Recommend `audit-codebase` and stop before Pin. | Relationship structural check plus behavior sample |
| V04 | Delegated or nested invocation | Return `incomplete` root-only blocker before target capture. | Root-guard behavior sample |
| V05 | Complete initial caller packet | Freeze all required fields and continue. | Packet contract check |
| V06 | Remediation with exact Charter, prior identity, carried IDs, Repair delta, remaining acceptance, and successor | Limit judgment to carried outcomes, delta, affected seams, and exercised remaining acceptance. | Mode behavior fixture |
| V07 | Assurance with same reviewed target and caller reason | Recheck the immutable target without creating repair or successor authority. | Mode behavior fixture |
| V08 | Resolvable Git fixed point and target | Capture exact objects and diff; reviewers see fixed bytes. | Git identity check |
| V09 | Supplied connected PR with exact base/head/diff | Capture read-only PR identity and content; leave PR state unchanged. | Connector/local identity proxy |
| V10 | Explicit live local target with untracked content | Capture the full composite including untracked bytes. | Composite snapshot check |
| V11 | Strong repository Standards and thin-Standards variant | Prefer local Standards; load fallback only in the thin variant. | Source-precedence structural and behavior check |
| V12 | `Spec required: yes` with missing or conflicting source | Return `incomplete`; do not infer intent. | Source wrong-condition fixture |
| V13 | `Spec required: no` with no Spec | Record Spec as skipped and continue Standards coverage. | Source optional fixture |
| V14 | At least two valid fresh reviewers covering every required axis/lens | Normal-capacity coverage is eligible for any evidence-supported terminal decision. | Dispatch/return identity inspection |
| V15 | Reviewer brief leaks parent hypothesis, peer result, or terminal cue; or return omits required fields | Give the lane zero credit and safely rerun only if unbiased same-snapshot conditions remain. | Payload isolation/schema check |
| V16 | Exactly one valid fresh completed reviewer | Run separated root coverage for missing lenses, disclose reduced confidence, and forbid plain `pass`. | Capacity behavior fixture |
| V17 | Zero valid fresh completed reviewers | Run separated root passes, disclose missing independence and reduced confidence, and forbid plain `pass`; uncovered required evidence returns `incomplete`. | Capacity behavior fixture |
| V18 | Overlapping, conflicting, and carried candidate IDs | Ledger retains stable IDs and closes every item as accepted, rejected, duplicate, or evidence-resolved dispute. | Ledger contract check |
| V19 | Speculative candidate and directly evidenced blocking candidate | Reject the speculative item; admit the blocker only after all five Finding Contract gates and return `blocked`. | Finding admission fixture |
| V20 | Advisories disabled/enabled and a violated contract mislabeled advisory | Disabled branch stays unloaded; enabled valid opportunity stays separate; violated contract remains a finding; decision is unchanged by advisories. | Advisory relationship and behavior fixture |
| V21 | Any captured target surface changes after Pin; baseline symbolic ref alone moves in a separate variant | Target drift returns `incomplete` without recapture; movement of a ref after an exact fixed point was pinned does not replace that object or create target drift. | Drift identity check |
| V22 | Full required coverage, two or more fresh completed reviewers, no blocker, no material residual, no drift | Return plain `pass`. | Decision table check |
| V23 | Complete coverage, no blocker, but reduced capacity or accepted residual risk | Return `pass with residual risk`, with exact residual and confidence disclosure. | Decision table check |
| V24 | Missing required source/evidence/lens, unresolved dispute, protocol failure, or drift | Return `incomplete` with verified partial evidence and exact blocker. | Decision table check |
| V25 | Any terminal decision | Return a complete caller-bound report with `Mutation authority: none` and `Successor snapshot authority: none`; start no Repair or downstream work. | Return contract and mutation inspection |

## Viability And Proof Outline

Prompt 1 proof is structural and intent-derived only:

1. Read back every listed local authority and complete caller package capable
   of changing the review contract.
2. Verify that every viability-floor axis has an owner, M0 unit, clause, safe
   failure Return, and viability case.
3. Verify the state-location ledger covers caller packet, fixed point,
   Git-addressed/connected/live targets, source state, reviewer packets,
   candidate state, and terminal Return without granting mutation.
4. Verify one-to-one semantic ownership, required order, shared Finding and
   Advisory pointers, caller/callee verbs, exact mode/capacity/decision
   compatibility, and the clause-to-intent cut audit.
5. Apply Markdown gates to this bounded record, run skill-pack validation, and
   run both repository diff checks.

Later M0 proof must keep structural and behavioral lanes separate. Deterministic
checks own package inventory, invocation policy, headings/tokens required by
machine compatibility, shared-contract pointers, unit/clause coverage, and
absence of forbidden mutation or reverse handoff. Fresh behavioral fixtures
own invocation, root guard, mode branches, axis separation, reviewer isolation,
degraded capacity, evidence admission, advisory separation, drift, terminal
decision, and completion. No behavioral effectiveness is claimed by this
checkpoint.

## Research Questions Grouped By Intended Behavior

The future Research Pass may investigate these clusters without changing the
intended contract:

1. **Immutable review state:** defensible methods for capturing local PR,
   Git-addressed, connected-PR, index, worktree, and untracked content; target
   drift versus fixed-object baseline identity; and limits of read-only
   verification.
2. **Independent review coverage:** methods for partitioning Standards, Spec,
   security, reliability, and other caller-required lenses; preserving
   independence; avoiding shared-error convergence; and interpreting
   one-reviewer or root-only fallback evidence.
3. **Evidence convergence:** methods for claim verification, duplicate
   reconciliation, disagreement handling, finding burden of proof, severity
   after admission, and limits of agreement as evidence.
4. **Release decisions:** conditions distinguishing accept, accept with
   residual risk, blocking findings, and incomplete evidence; honest
   confidence under degraded capacity; and safeguards against false clean
   conclusions.
5. **Review modes:** sound scope and evidence requirements for initial,
   remediation, and assurance review while retaining stable IDs and immutable
   targets.
6. **Nonblocking advisories:** reliable separation of verified opportunities
   from violated contracts, findings, confidence, repair authority, and release
   decisions.
7. **Invocation and completion:** observable trigger wording, nearest
   exclusions, root-only execution, read-only safety, typed reviewer returns,
   and terminal caller restoration.

Exactly one future research note is authorized:
`docs/research/skills/convergent-pr-review/RP-convergent-pr-review-20260724-01.md`.

## Local Source Identity Manifest

All identities were read from the clean worktree at the starting `HEAD`.
`sha256` identifies file bytes; `git-tree` and `git-blob` identify complete
committed package/file content.

| Authority | Identity | Contract contribution |
| --- | --- | --- |
| User campaign brief, epoch 2026-07-24 | Conversation authority; starting `HEAD` `f3be70c31dd8f2ae9f12a75248065ef313790bda` | Prompt 1 scope, blind boundary, one-write boundary, research-note authorization, proof, and Return contract |
| `AGENTS.md` | `sha256:d93d25a1e8bf09f01fb9eee054682940539a072c5f489e99435dbe6e10cde314` | Commands, fresh campaign pointer, preservation, and diff checks |
| `CONTEXT.md` | `sha256:bae0de4372439edc96e91c5132967755797bc4628c8b2fef03591b6779fde8e1` | Artifact owners, active/experimental/install boundary, local vocabulary, and historical-evidence status |
| `docs/agents/engineering-contract.md` | `sha256:c3d52491ca8b98f229965e2602212fc4474ef2fedf8be73bc8f08c24300ef829` | Fixed point, review snapshot, Spec/Standards separation, proof, residual risk, read-only proxy, and Lock |
| `docs/agents/domain.md` | `sha256:94ccdc414542b44be2fe38d7ebe2e59fd809c09848642243c3a805749c6adb99` | Local context/ADR routing |
| `docs/agents/issue-tracker.md` | `sha256:d79c8dbdc0e3c77583b461ac2d50eb678d0ce77aed69a9e759e3c0818646f933` | Caller-owned PR/tracker transport and mutation boundary |
| `docs/synthesis/skill-context-relationships.md` | `sha256:15bb4ab6cd4cda5256b45aae4c7bb887a153f62cc63dbd2203d0f3b68ea1ad69` | Runtime verbs, caller/callee edges, root-only terminal review, shared contracts, audit exclusion, and no reverse handoff |
| `docs/synthesis/methods/deploy-prompts.md` | `sha256:d3ce058b1af22e43db51913869649dc6d75f31d97af7b2eb3f1248d84b07277f` | Shared Model, Run Contract, proof budget, and Prompt 1 checkpoint schema |
| ADR 0001 | `sha256:eb0ca5b54a8dbdd35a2fd170734006460e7f7a5a0f93ad8ce29264c8bcc76b75` | Primer/contract/skill ownership split |
| ADR 0003 | `sha256:5c043765d4679a272e096fa492b0b52b71f4c519216e98630e11031149177f34` | Skills encode only their local contract slice |
| ADR 0004 | `sha256:9e769eb02eec437867cd59e90553bb6dc981352b2a424f3eaadbae4bc354684e` | Language judgment remains semantic, not validator-owned |
| ADR 0005 | `sha256:91e14650e896b63115fbec818b3d01ca506d27ab92a501303f8f164fe8311552` | Active canonical and inactive experimental trees remain separate |
| ADR 0007 | `sha256:a8b37fa83c820a08bf0e10998e1301d537cefa5d797b49edcabbb308644c8962` | Runtime compression and synthesis provenance ownership |
| `README.md` | `sha256:dc630154d9c2d61124c93c6cd6ae4af5b1b813fb50bd661e47cc0af7456c0bcb` | Human-facing route: ordinary diff vs local PR/high-risk diff vs baseline audit |
| `review` complete package | `git-tree:1321a4f09b4227c7d0c0ec1abfc9cff0d5cafd6d` | One-way handoff, Pin/Trace/Admit/Return, shared Finding and Advisory Contracts, baseline fallback, report fields |
| `implement` complete package | `git-tree:5f8f54d96f86c9a36d2129160ca2f1cad866aaec` | Caller Charter, exact candidate, proof/risk packet, formal-route selection, Repair and Lock ownership |
| `parallel-implement` complete package | `git-tree:24aa1add89f01c960182e9594fb112c66068fb21` | Root caller, exact integration target, initial/remediation/assurance ledger compatibility, repair/review budgets, terminal decision consumption |
| `skill-router` complete package | `git-tree:82c11c78b8c3a83d7ada581adaa54a04524b04e5` | Direct route for local PR/high-risk diff and exclusion route for repository-baseline audit |
| `audit-codebase` complete package | `git-tree:990920d7b4f1b5c43cf4fb7f55a12268f7ad2a60` | Baseline-audit ownership, terminal non-release outcome, root/read-only boundary |
| `tests/test_skill_pack_contracts.py` relevant compatibility gates | `git-blob:8fa5bfc2f9ff20571a6993a7edaf24358c7d8b59` | Root guard, direct fresh context, typed reviewer packet, capacity modes, five ledger states, four decisions, mode fields, shared contracts, drift surfaces, and relationship edges |
| Installed `writing-great-skills/SKILL.md` | `sha256:dd9cc9fa91dacfbeaddb73a82488ff9dcb921f4e7626cb9e12beb2c1cefff2ee` | Audit authority, ownership, cuts, proof, and completion |
| Installed `writing-great-skills/GLOSSARY.md` | `sha256:7e513d1d2ae38f99c61c748830b0bb81a9f47707231e20fdb9a07dbcc164c274` | Invocation, information hierarchy, steering, completion, and pruning vocabulary |

The current target body and package metadata, installed target mirror, target
synthesis, prior target research, upstream packages, target historical
evaluations, experimental candidates, and promotion records were deliberately
not inspected. They have no Prompt 1 identity or authority in this checkpoint.

## Limitations And Re-entry

- M0 is a behavior-complete specification, not materialized runtime bytes.
- Current, M0 runtime, H1, V1, P1, canonical, and installed target identities
  are intentionally unknown at Prompt 1. Campaign shape cannot be classified
  until later authorized inspection and synthesis.
- No outside professional evidence, upstream observation, current-runtime
  observation, historical target proof, or behavioral sample supports this
  checkpoint.
- The exact number and partition of reviewer lenses beyond required local axes
  remains caller- and Charter-dependent. M0 requires complete coverage and
  exact capacity disclosure, not a fixed universal lens catalog.
- Read-only verification that is unsafe or unavailable remains a named
  evidence gap; a structural proxy cannot become semantic runtime proof.
- Re-entry must verify starting/current `HEAD`, every local source identity,
  this bounded-content fingerprint, and the blind-boundary exclusions.
  Unexpected drift requires a fresh blind Prompt 1 pass. Revisit only an
  explicitly authorized decision delta.

## Prompt 1 Decision

- Status: `ready-for-research`
- Intended contract: settled on every viability-floor axis.
- M0 checkpoint: behavior-complete and clause-mapped.
- Campaign shape: `pending` because current and H1 identities remain blind and
  unmaterialized.
- Runtime identities: current `blind`; M0 `specification-only`; H1, V1, P1,
  canonical, and installed `pending`.
- Existing evidence disposition: local source and compatibility contracts are
  current structural intent evidence only; behavioral evidence is `missing`.
- Residual gaps: professional-method evidence, current/upstream observation,
  exact runtime construction, candidate-owned viability, contribution,
  pruning, invocation, and completion proof remain for later authorized units.

Authorized unit completed: Deploy Prompt 1: Freeze M0
Decision: ready-for-research
Campaign shape: pending
Runtime identities: current=blind; M0=specification-only; H1=pending; V1=pending; P1=pending; canonical=pending; installed=pending
Artifacts changed: docs/validation/transcripts/2026-07-24-convergent-pr-review-prompt1-m0.md
Evidence used or reused: fresh local intent read-back and structural compatibility authorities; controller-supplied baseline validation passed and managed-install dry-run reported 25 unchanged with no changed cohort; no behavioral evidence reused
Residual gaps: independent research, current/upstream inspection, exact runtime identities, and candidate-owned behavioral proof
Recommended next unit: Deploy Research Pass
Git HEAD: f3be70c31dd8f2ae9f12a75248065ef313790bda -> f3be70c31dd8f2ae9f12a75248065ef313790bda
Git delivery: pending
Exact stop reason: M0 is frozen from local intent; stop before Research

<!-- END M0 CHECKPOINT -->
