# Implement Deploy Prompt 1 — M0 Checkpoint

Date: 2026-07-24
Skill: `implement`
Unit: Deploy Prompt 1 only
Operation: `$writing-great-skills` Audit
Starting Git HEAD: `94d68e78d8812e9a2ceffd093e729402cac1cff2`
Checkpoint state: frozen, blind to the current `implement` body and all research-derived material

## Blindness and authority boundary

This pass used only the campaign request, repository-owned intent, domain and
engineering decisions, caller contracts, relationship-owner contracts, and
tracker compatibility contracts. It did not inspect the current target skill
body, target synthesis conclusions, historical evaluations, experimental
candidates, promotion records, upstream packages, outside research, or prior
research notes. A broad literal reference search exposed one line from the
target package's `agents/openai.yaml`; that line was not opened as an authority,
did not settle any decision, and contributed no M0 clause.

Prompt 1 authorizes this record only. It does not authorize runtime
materialization, research, target edits, tests of target behavior, installation,
staging, commit, or push.

## Source identities

The campaign request is the non-file authority received by the unit on
2026-07-24: run only Deploy Prompt 1 for `implement`, write only this decision
record, preserve the named dirty files, and stop.

Process authorities:

| SHA-256 | Source |
| --- | --- |
| `dd9cc9fa91dacfbeaddb73a82488ff9dcb921f4e7626cb9e12beb2c1cefff2ee` | `C:\Users\steve\.agents\skills\writing-great-skills\SKILL.md` |
| `7e513d1d2ae38f99c61c748830b0bb81a9f47707231e20fdb9a07dbcc164c274` | `C:\Users\steve\.agents\skills\writing-great-skills\GLOSSARY.md` |
| `ce92bfe83ed741b379cbe52db97bdaac6f6734c39516d33cf2da5df822fa6597` | `docs/synthesis/methods/deploy-prompts.md` |

Local intent authorities:

| SHA-256 | Source |
| --- | --- |
| `d93d25a1e8bf09f01fb9eee054682940539a072c5f489e99435dbe6e10cde314` | `AGENTS.md` |
| `bae0de4372439edc96e91c5132967755797bc4628c8b2fef03591b6779fde8e1` | `CONTEXT.md` |
| `c3d52491ca8b98f229965e2602212fc4474ef2fedf8be73bc8f08c24300ef829` | `docs/agents/engineering-contract.md` |
| `94ccdc414542b44be2fe38d7ebe2e59fd809c09848642243c3a805749c6adb99` | `docs/agents/domain.md` |
| `d79c8dbdc0e3c77583b461ac2d50eb678d0ce77aed69a9e759e3c0818646f933` | `docs/agents/issue-tracker.md` |
| `06f253d31ea852376950b4b8c163f2a1e60c5be131492b3cb76d05be92b58ded` | `docs/agents/triage-labels.md` |
| `eb0ca5b54a8dbdd35a2fd170734006460e7f7a5a0f93ad8ce29264c8bcc76b75` | `docs/adr/0001-agents-primes-contract-teaches-skills-execute.md` |
| `850e1bb0a2204c351f14a5a094d196c530e66e194b49f379755787d5bdc009ff` | `docs/adr/0002-setup-installs-repo-local-engineering-contract.md` |
| `5c043765d4679a272e096fa492b0b52b71f4c519216e98630e11031149177f34` | `docs/adr/0003-skills-encode-local-contract-slices.md` |
| `91e14650e896b63115fbec818b3d01ca506d27ab92a501303f8f164fe8311552` | `docs/adr/0005-separate-active-and-experimental-skill-trees.md` |
| `2bbf8e9c2b9c0c86d8aa3abff2a66bdfb946a9a120dbff3d5d640966398d7c05` | `skills/custom/skill-router/SKILL.md` |
| `3bf863a8856d04a6a1c4f23b3aae6cbf5388544129662c55cc733c2d9c23bbbf` | `skills/custom/skill-router/agents/openai.yaml` |
| `27355fa8228231ead0062581f565394a570414012e6ac11afb311e97aef0c7b9` | `skills/custom/to-tickets/SKILL.md` |
| `a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94` | `skills/custom/to-tickets/agents/openai.yaml` |
| `3a1ce646fd247181d3d4ae5758a55b1e16f0573a465d5b5dd8ce4f24636f3ec4` | `skills/custom/triage/SKILL.md` |
| `7e1b504b365975b68677aa144f3208c8e6775a12bfa18ffa50a0f9b0f5457b30` | `skills/custom/triage/ATTENTION-SCAN.md` |
| `2f893a26f0511f7ad9ef6f38483d4b3a759122dedac62892d9cc09bc0cd62c70` | `skills/custom/triage/SPECIFIC-ITEM.md` |
| `60bc0928cf3fce5a75cf737c659c2c47f65a7ef2e5a64d8bd9f1625b6f0421e9` | `skills/custom/triage/QUICK-OVERRIDE.md` |
| `35a62dbbb2e2e368656fd7c69ec4d912f111675039315167e15ae3691ac4ea69` | `skills/custom/triage/OUT-OF-SCOPE.md` |
| `529e173c30d34f2dcc0b19ba98cddb8dded77c6cf51fbe4dc4e5a2d435bf7ad0` | `skills/custom/triage/AGENT-BRIEF.md` |
| `9ca3a7fa4d32472348142b77d1723982c8296248b27fbb21a11a999cc10a50de` | `skills/custom/triage/AGENT-BRIEF-EXAMPLES.md` |
| `3bf863a8856d04a6a1c4f23b3aae6cbf5388544129662c55cc733c2d9c23bbbf` | `skills/custom/triage/agents/openai.yaml` |
| `8e7384da3f449f459b417c6c5e6eecf99d37dfe70cabc25508768897f611edc5` | `skills/custom/parallel-implement/SKILL.md` |
| `d289f553a633be8d5ab4de2e6d2031d045ef023f29cb9f3ad537565c493d1b7b` | `skills/custom/diagnosing-bugs/SKILL.md` |
| `d9ef3372e04c488b227009cd14ef0ed84fa4335056d48219bc6cbf8a80a970bd` | `skills/custom/diagnosing-bugs/agents/openai.yaml` |
| `3c40b46601971434c5a0ab437e3172b02ad59880c06d3c50e6058f74251c3806` | `skills/custom/tdd/SKILL.md` |
| `03235a5bf4ade1f6d9c580e9210f2d0d7ee3ce8a7f773be0bd39b940ad625fdd` | `skills/custom/review/SKILL.md` |
| `da8d687c07a2ff3807d40fecec12ee30651d18e305cc2ded9cfe9ffd881e4a2b` | `skills/custom/convergent-pr-review/SKILL.md` |
| `260af2de992135a3b0497040da0534faaf7fd12d89b5729cdf1db5e29dfc7ce8` | `skills/custom/resolving-merge-conflicts/SKILL.md` |
| `d79c8dbdc0e3c77583b461ac2d50eb678d0ce77aed69a9e759e3c0818646f933` | `skills/custom/repo-bootstrap/issue-tracker-github.md` |
| `b2306fc978d12a17658f30bf48a5e80e3f28407e1daa904d03298a0ba463e709` | `skills/custom/repo-bootstrap/issue-tracker-gitlab.md` |
| `4c8c31836b0e6428e51eb8b169b9126b1f905ed4988d5cc116c766d8bbe51e36` | `skills/custom/repo-bootstrap/issue-tracker-local.md` |

## M0 checkpoint

Fingerprint method: SHA-256 of the exact UTF-8 text between the
`fingerprint-start` and `fingerprint-end` marker lines, excluding both marker
lines. Line endings are LF and the hashed payload includes its final LF.

M0 checkpoint fingerprint: `sha256:ff4ea3bc80cc12820d1debe8142d26832a0449d392ec843439118157902affbc`

<!-- fingerprint-start -->
### Intended contract and viability floor

**Outcome.** Deliver exactly one selected, bounded Ready-for-agent item into an
accepted, proved, reviewed, and committed repository result, including
tracker-recorded closeout when the item is tracker-backed, or return a truthful
nonterminal packet that preserves recoverable work and names the exact safe
continuation.

**Invocation.** Admit one user- or caller-selected bounded item whose outcome,
observable acceptance, commitment boundary, scope authority, and Source Trace
are settled. A tracker-backed item must satisfy its configured Ready-for-agent
contract: one bounded slice, dependency state, proof lane, expected write
scope, parallel-safety judgment, and scope fence. A direct caller packet may
supply agent-owned execution facts during Chartering, but may not omit a
user-owned commitment. Preserve any settled work-unit form, learning role,
migration phase, verification evidence, domain/ADR pointers, supported edge
and error cases, and out-of-scope statements in its source packet. Valid
`$to-tickets`, `$triage`, and diagnosis Returns may supply the selected item.

**Exclusions and handoffs.**

- Unsettled source, missing readiness facts, contradictory acceptance, or a
  defective ticket graph returns to the source, triage, or ticket-shaping
  owner without production mutation.
- An explicitly requested exhaustive parent graph belongs to
  `$parallel-implement`; `implement` does not dispatch or close a parent
  campaign.
- Review-only work belongs to `$review` or `$convergent-pr-review`.
- Conflict-only reconciliation belongs to `$resolving-merge-conflicts`.
- Uncertain bug causality belongs to `$diagnosing-bugs`; red-testable new
  behavior or a fully known red-capable bug loop belongs to `$tdd` as the
  implementation caller's inner proof owner.
- Product decisions, architecture commitments, public/data contracts,
  security or privacy posture, agreed scope, permissions, irreversible
  external actions, and residual-risk acceptance remain user or caller owned.

**Authority.** `implement` owns the single-item Charter, repository mutation
within the bounded slice, selection of technique within settled commitments,
integration of returned inner-loop work, proportionate proof, repair of
admitted in-scope review findings within a pre-recorded budget, intentional
staging and commit of the accepted tree, and tracker closeout through the
configured tracker contract. It does not own ticket shaping, parent-graph
delivery, diagnosis or TDD procedure, formal review judgment, tracker
transport semantics, new commitments, unbounded cleanup, push without explicit
authority, or conflict-operation completion without separate authority.

**Caller and relationship obligations.**

- `$skill-router`, `$to-tickets`, and `$triage` may hand off one selected,
  complete Ready-for-agent item; their source ownership and readiness facts
  remain authoritative.
- The target repo's `AGENTS.md` points to command, engineering, tracker, label,
  and domain owners. Missing or incompatible required setup returns a
  `$repo-bootstrap` precondition before work-item or tracker mutation.
- `$diagnosing-bugs` and `$tdd` return evidence to `implement`; neither owns
  scope, review, staging, commit, tracker mutation, push, or Lock.
- `$review` or `$convergent-pr-review` receives an immutable candidate,
  required Spec, Charter, Source Trace, fixed point, and proof. It returns
  judgment only and grants no repair or successor-snapshot authority.
- For a tracker-backed item, configured GitHub, GitLab, or Local Markdown
  rules own claim, release, closeout, and Mutation read-back. The configured
  close rule wins. A direct untracked item does not fabricate tracker state.
- `$parallel-implement` owns parent graphs and never uses this single-item
  completion result as authority to close the parent early.

**Safe failure Return.** Any nonterminal return names status (`partial` or
`blocked`), the failed gate, observed repository and tracker state, retained
changes and evidence, actor/claim state, skipped checks, residual risk,
authority needed, and one safest recovery or resume action. It releases a
claim when active work ends, leaves incomplete items open, performs no unsafe
progression, and never describes a staged handoff or checkpoint as
implementation completion.

**Completion.** Complete only when the selected acceptance and relevant
state-boundary branches are proved on the exact accepted tree; required formal
review has accepted an immutable snapshot and every admitted repair has
received a successor review within budget; current repository identity still
matches that accepted snapshot; the accepted tree is intentionally committed
with unrelated state excluded; applicable configured tracker closeout and
affected relationship read-back succeed; any claim is released; disposable
state is removed or named; required push, when separately authorized, is
verified; and the final Return records evidence, skipped checks, residual risk,
commit identity, tracker state or `not applicable`, and external-delivery
state.

**Irreversible order.**

1. Validate setup, packet completeness, readiness, blockers, repository state,
   and authority before claiming or production mutation.
2. For a tracker-backed item, claim through the configured tracker and read the
   claim back before implementation; record claim as not applicable for a
   direct item.
3. Freeze the Charter and fixed point before choosing technique or changing
   production.
4. Prove a narrow behavior path before expanding; reconcile the full assigned
   acceptance and affected state branches before review.
5. Pin and complete formal review before admitting any repair.
6. Repair only an admitted, Charter-preserving batch within budget; each
   successor tree receives fresh formal review.
7. Reconcile final proof and identity before intentional staging and commit.
8. Close out applicable tracker state only after acceptable review and commit;
   apply Mutation read-back and release any claim.
9. Push only when separately authorized, then verify the exact approved commit
   at the remote.

**Compatibility and safety.** Preserve the configured GitHub, GitLab, or Local
Markdown tracker semantics; repository commands and setup contracts; existing
public, data, security, privacy, and compatibility commitments; unrelated dirty
and index state; and pre-existing dead work outside the slice. Use
expand-migrate-contract for non-atomic incompatible changes. External writes,
live or production instrumentation, sensitive data, destructive Git actions,
dependency additions, public test hooks, migrations, cutovers, permissions,
and other irreversible changes require their owning authority and
proportionate rollback or partial-state proof.

### Semantic behavior unit ledger

| ID | Semantic unit and local authority | Cheapest neutral expression | Entry and wrong-condition cases | Failure Return | Proof |
| --- | --- | --- | --- | --- | --- |
| M0-U01 | Admit one selected bounded ready item. Authority: user/caller, router, To Tickets, Triage, Diagnosing Bugs, and tracker Ready-for-agent contract. | State the single-item trigger, settled commitment minimum, and tracker-backed additions. | Enter for one complete selected item. Wrong: raw request, unsettled commitment, incomplete tracker packet, parent graph, review-only task. | Typed source/readiness/setup/routing packet; no production or tracker mutation. | Direct and tracker-backed included fixtures; excluded invocation fixtures; packet-field read-back. |
| M0-U02 | Apply target-repo setup and domain routing. Authority: AGENTS, ADR-0001/0002/0003, domain and engineering contracts. | Follow repo pointers; require only directly relevant local contract slices. | Enter before tracker access or code exploration. Wrong: required surface absent or incompatible. | `$repo-bootstrap` precondition with unchanged work-item and tracker state. | Pointer trace and missing/incompatible setup fixtures. |
| M0-U03 | Reconcile work item, dependencies, repo state, authorities, and fixed point. Authority: tracker contract and engineering Source Trace. | Read the complete packet and current state; record identities and gaps. | Enter after setup. Wrong: blocker unresolved, item claimed, source conflict, fixed point ambiguous, unsafe dirty overlap. | Blocked packet naming observed state, conflict, and safe recovery; no claim. | Read-back of packet, blocker/frontier, Git status, fixed point, and authority matrix. |
| M0-U04 | Claim a tracker-backed item as concurrency guard; record not applicable for a direct item. Authority: configured tracker contract and direct caller boundary. | Apply configured claim and immediately refetch affected state, or make no tracker mutation. | Enter only after U03 passes. Wrong: competing claim, partial mutation, mismatched read-back, or fabricated tracker target. | Report applied/failed operations and safest recovery; do not implement; release only an owned partial claim when safe. | Before/after tracker capture and Mutation read-back, plus direct-item no-mutation fixture. |
| M0-U05 | Freeze one Charter and bounded slice. Authority: engineering contract plus source owner. | Record outcome, acceptance, supported paths, proof, commitment boundary, non-goals, fixed point, repair budget, expected writes, and scope fence. | Enter after the claim/not-applicable gate. Wrong: missing or conflicting user-owned commitment. | Decision-needed packet; preserve state and release any claim when work stops. | Clause-to-source trace; every acceptance and exclusion has one disposition. |
| M0-U06 | Explore and choose technique without changing commitments. Authority: engineering contract. | Inspect real seams and alternatives; select one narrow observable path. | Enter with settled Charter. Wrong: stronger option changes scope/public/data/security/privacy/architecture commitment or needs new permission. | Decision packet naming alternatives and commitment delta; no out-of-authority mutation. | Source Trace, alternatives considered, selected seam, and authority check. |
| M0-U07 | Route uncertain diagnosis or red-capable inner development to its owner and integrate only its bounded Return. Authority: Diagnosing Bugs and TDD relationship contracts. | Invoke the matching owner with Charter slice and retain implementation ownership. | Enter when bug facts are uncertain or behavior is red-testable. Wrong: returned packet changes scope, lacks required RED/cause proof, or requests caller-owned authority. | Return or resume with exact evidence/decision gap; do not claim delegated work as complete. | Owner-matched packet fields, diff scope, RED/GREEN or cause-gate evidence. |
| M0-U08 | Implement one narrow path, then all assigned acceptance and supported state branches. Authority: engineering contract and ready item. | Mutate only authorized files; prove the narrow path before expansion. | Enter after technique choice or acceptable inner-loop Return. Wrong: acceptance contradiction, out-of-scope write, unsafe irreversible step, unrelated failure. | Preserve recoverable work; name exact failed branch, state, and required authority or diagnosis. | Focused semantic seam, relevant nearby proof, state-boundary matrix, and diff-to-scope map. |
| M0-U09 | Simplify and reconcile the candidate while proof remains valid. Authority: engineering Simplify and Lock contracts. | Remove authored scaffolding and accidental complexity; preserve unrelated work. | Enter after behavior proof. Wrong: cleanup alters commitments, proof, or unrelated state. | Retain last proved candidate or return exact reconciliation blocker. | Re-run affected proof, complete diff read-back, disposable-state inventory. |
| M0-U10 | Obtain formal read-only review of one immutable candidate. Authority: Review or Convergent PR Review. | Supply Charter, required Spec, Source Trace, fixed point, snapshot, and proof; accept only its terminal report. | Enter after current candidate proof and actor quiescence. Wrong: snapshot incomplete/drifted, required Spec missing, review incomplete, or blocker admitted. | Keep any tracker item open and claimed only while active; return review blocker and immutable state. | Snapshot identity, review report, drift gate, and complete finding ledger. |
| M0-U11 | Repair only admitted Charter-preserving findings within the recorded budget, then obtain fresh successor review. Authority: caller-owned repair budget and review's no-mutation boundary. | Admit one bounded batch; mutate through the appropriate implementation/proof owner; repin and rereview. | Enter only for admitted in-scope blockers. Wrong: ambiguous, decision-required, out-of-scope, over-budget, or exhausted successor review. | Decision or blocked packet with stable finding IDs, retained snapshot, and no unreviewed acceptance claim. | Finding dispositions, repair diff, affected proof, successor snapshot, fresh terminal review. |
| M0-U12 | Reconcile exact accepted tree, validation, work state, and residual risk before Git delivery. Authority: engineering Lock. | Compare current identities to reviewed snapshot; run canonical or justified proportionate checks. | Enter after acceptable final review. Wrong: drift, failing required check, unexplained extra change, unaccepted residual risk. | Blocked packet; do not stage, commit, close, or push. | Identity comparison, current proof commands/results, Spec/Standards check, work-state inventory. |
| M0-U13 | Intentionally stage and commit only the accepted tree. Authority: implementation caller and tracker definition of implemented; Git delivery remains bounded by user authorization. | Exclude unrelated index/worktree state; commit exact accepted content and verify identity. | Enter after U12. Wrong: unrelated staged content, hook changes bytes, commit failure, tree mismatch, or commit authority absent. | Exact Git state and safe next action; no tracker closeout. | Staged diff, commit result, committed tree versus accepted tree, post-commit status. |
| M0-U14 | Apply configured tracker closeout and relationship read-back when tracker-backed; record not applicable for a direct item. Authority: tracker contract, label mapping, and direct caller boundary. | Post evidence, set implemented state, apply configured close rule, release claim, and refetch item/dependents, or make no tracker mutation. | Enter only after acceptable review and verified commit. Wrong: partial mutation, false-ready dependent, failed release, close rule ambiguity, or fabricated tracker target. | Partial-publication recovery with applied/failed operations and safest correction; never report complete. | Exact closeout packet, labels/status/open state, claim absence, dependent frontier read-back, plus direct-item no-mutation fixture. |
| M0-U15 | Perform separately authorized push and verify it, or record push as not authorized/not required. Authority: explicit user/caller permission. | Push only the approved commit under named authority and compare remote identity. | Enter after commit, only if required and authorized. Wrong: no authority, remote drift, rejection, wrong destination. | Preserve local completion evidence; report external-delivery blocker and no verified push. | Remote/ref identity equals approved commit, or explicit not-authorized/not-required record. |
| M0-U16 | Return terminal completion or truthful nonterminal state. Authority: engineering Lock, tracker contract, and relationship owners. | Emit one packet accounting for scope, proof, review, commit, tracker applicability, claims, external delivery, cleanup, and risk. | Complete only after every applicable prior gate. Wrong: any unchecked completion predicate or staged handoff. | `partial` or `blocked` with one safe continuation; any tracker item remains open unless closeout actually read back. | Packet-to-gate audit and final Git/tracker read-back. |

### Runtime-clause specification

The later M0 runtime must express these clauses without adding behavior:

| Clause | Required runtime meaning | Unit(s) |
| --- | --- | --- |
| C01 | Trigger on exactly one selected bounded item with settled commitments; require the configured Ready-for-agent additions when tracker-backed; exclude parent-graph, shaping, review-only, and conflict-only work. | U01 |
| C02 | Load repo-owned setup, tracker, label, domain, and engineering slices; stop for setup incompatibility. | U02 |
| C03 | Read and reconcile the complete packet, dependencies, fixed point, current Git/tracker state, authorities, and unrelated work before mutation. | U03 |
| C04 | Claim a tracker-backed item through the configured tracker and require Mutation read-back before implementation; fabricate no tracker state for a direct item. | U04 |
| C05 | Freeze the Charter, bounded slice, scope fence, proof lanes, state branches, and repair budget; return user-owned commitment gaps. | U05 |
| C06 | Explore alternatives and choose technique inside settled commitments; escalate commitment changes. | U06 |
| C07 | Route uncertain bugs to diagnosis and red-testable behavior to TDD as inner owners; integrate only contract-complete Returns. | U07 |
| C08 | Implement a narrow observable path, expand across acceptance and state branches, and preserve scope, safety, compatibility, and unrelated work. | U08 |
| C09 | Simplify authored work and reconcile full diff, proof, and disposable state. | U09 |
| C10 | Pin one immutable proved candidate and obtain the applicable formal read-only review with required Spec. | U10 |
| C11 | Admit only one Charter-preserving repair batch within budget and require fresh successor review; return all other findings for decision. | U11 |
| C12 | Lock exact reviewed bytes through current validation, identity comparison, work-state reconciliation, and explicit residual-risk acceptance. | U12 |
| C13 | Stage and commit only the accepted tree; verify the committed tree and preserve unrelated index/worktree state. | U13 |
| C14 | When tracker-backed, close out through the configured tracker only after review and commit and read back item, claim, relationships, and frontier; otherwise record tracker closeout as not applicable. | U14 |
| C15 | Push only with separate authority and verify the exact approved commit; otherwise record the boundary. | U15 |
| C16 | Return `complete` only at the full gate; otherwise return `partial` or `blocked` with retained state and one safe continuation. | U16 |

### Clause-to-intent cut audit

| Clause(s) | Viability or required local contract |
| --- | --- |
| C01, C05 | User/caller selection, Router and Ready-for-agent contracts, Diagnosing Bugs Return; one bounded slice and Charter vocabulary |
| C02 | ADR-0001/0002/0003, setup ownership, domain routing |
| C03, C06, C08, C09, C12, C16 | Engineering Source Trace, commitment boundary, bounded slice, proof, stewardship, and Lock |
| C04, C14 | Configured tracker claim, closeout, release, dependency, and Mutation read-back contracts |
| C07 | Diagnosing Bugs and TDD caller/Return boundaries |
| C10, C11 | Review and Convergent PR Review read-only, immutable-snapshot, finding, and successor-authority boundaries |
| C13 | Tracker's `implemented` meaning and caller-owned Git delivery responsibilities retained by inner skills |
| C15 | Explicit external-mutation authority and delivery verification |

Cut result: every clause maps to the viability floor or a named required local
contract. No research-derived method, leading term, current-runtime behavior,
optional parent orchestration, generic coding advice, duplicated tracker
transport procedure, or installer/promotion behavior is admitted to M0.

### Complete M0 viability suite

The viability suite tests only the intended minimum:

1. **Invocation matrix:** admit a direct selected item with settled commitments
   and a tracker-backed item satisfying the configured Ready-for-agent
   contract; reject raw, commitment-incomplete, tracker-incomplete, claimed,
   blocked, parent-graph, graph-shaping, review-only, and conflict-only packets
   with the correct owner and no mutation.
2. **Setup matrix:** valid configured setup proceeds; absent or incompatible
   required setup returns one `$repo-bootstrap` precondition before tracker or
   production mutation.
3. **Tracker compatibility:** GitHub, GitLab, and Local Markdown fixtures each
   prove claim/read-back, release, post-review-and-commit closeout, configured
   close behavior, relationship/frontier read-back, and partial-mutation
   recovery; a direct-item fixture proves no tracker state is fabricated.
4. **Charter completeness:** every ready-item acceptance, exclusion, supported
   path, state branch, proof lane, expected write, dependency, and scope fence
   maps to the frozen Charter or a returned commitment gap.
5. **Authority guards:** commitment, permission, security/privacy, migration,
   irreversible action, dependency/public-hook, push, conflict-finish, and
   residual-risk decisions stop at their correct owner.
6. **Inner-owner routing:** uncertain bug facts return through Diagnosing Bugs;
   known red-capable work returns through TDD; incomplete or scope-changing
   packets cannot satisfy implementation proof.
7. **Tracer and expansion:** one semantic path is proved before expansion; all
   distinct acceptance and applicable state-boundary branches pass through
   caller-facing seams.
8. **Scope and stewardship:** only expected durable writes appear; unrelated
   dirty/index state and pre-existing out-of-slice work are byte-preserved;
   authored disposable/scaffolding state is removed or explicitly retained.
9. **Review routing and immutability:** ordinary and high-risk/local-PR
   candidates reach the correct review owner with required Spec and Charter;
   incomplete, blocked, or drifted review cannot advance.
10. **Repair controls:** admitted in-scope repair inside budget receives
    affected proof and fresh successor review; ambiguous, out-of-scope,
    decision-required, over-budget, and exhausted cases stop without
    unauthorized mutation.
11. **Lock and Git identity:** required current checks pass or skips are
    justified; accepted snapshot equals current and committed tree; unrelated
    index content is excluded; hook-induced drift blocks closeout.
12. **Closeout ordering:** applicable tracker closeout cannot occur before
    acceptable review and verified commit; completion cannot occur before
    applicable closeout, claim release, affected read-back, cleanup accounting,
    and applicable push verification. Direct work records tracker state as not
    applicable.
13. **Failure safety:** inject failure at claim, implementation, proof, review,
    repair, staging, commit, tracker mutation, release, and push; each Return
    names exact retained state and one safe continuation, leaves applicable
    incomplete tracker work open, and makes no false completion claim.
14. **Completion packet:** terminal output accounts for Source Trace, Charter,
    changed scope, proof, review decision, repair generations, commit, tracker
    and claim state, external delivery, cleanup, skipped checks, and residual
    risk.

### Limitations and evidence gaps

- Prompt 1 does not test exact runtime wording, invocation reliability,
  behavioral efficacy, or compatibility with the uninspected current target.
- No current target bytes, upstream package, research result, synthesis,
  evaluation, candidate, or promotion evidence was inspected or reused.
- The viability suite is specified, not executed; Prompt 3 materializes exact
  M0 bytes and Prompt 4 owns behavior execution.
- Tracker transport examples were read as compatibility contracts; no live
  tracker mutation was performed.
- The intended contract permits push only when separately authorized. Research
  should test whether that conditional belongs inline or behind a branch
  pointer without changing the authority boundary.

### Research questions grouped by intended behavior

**Admission and Charter**

- Which professional delivery practices best prevent an apparently ready work
  item from hiding unresolved acceptance, dependencies, state branches, or
  commitment decisions?
- What evidence distinguishes useful implementation Charters from process
  overhead for small single-item work?

**Exploration, implementation, and proof**

- Which methods reliably balance alternative exploration against timely
  commitment for one bounded repository slice?
- What evidence supports narrow end-to-end proof before expansion, and under
  what conditions should state-boundary coverage widen?
- Which counterpressure shows when test-first, diagnostic, prototype, or direct
  implementation routes are inappropriate?

**Review and repair convergence**

- What review/repair sequencing reduces defect escape without inviting
  unbounded cleanup or reviewer-driven scope expansion?
- How should a repair budget and successor-review requirement scale with risk,
  and what failure modes arise from one-batch versus iterative repair?

**Git, tracker, and external completion**

- What practices best preserve unrelated work while proving that committed
  bytes equal reviewed bytes?
- Which ordering and recovery patterns make tracker closeout truthful under
  partial external mutation?
- When is push part of single-item completion, and what authorization and
  remote-identity proof are necessary?

**Completion and safe failure**

- Which completion criteria most reliably prevent checkpoints, staged
  handoffs, or green focused tests from being mistaken for end-to-end delivery?
- What minimum nonterminal packet enables safe resumption without turning the
  implementation skill into a parent orchestrator?

Authorized successor research-note path:
`docs/research/implement-2026-07-24.md`
<!-- fingerprint-end -->

## Re-entry protocol

Re-entry must:

1. verify Git HEAD remains
   `94d68e78d8812e9a2ceffd093e729402cac1cff2` for this frozen checkpoint or
   record the expected campaign-owned transition;
2. recompute every listed local-authority identity and the checkpoint
   fingerprint;
3. verify the campaign request, target name, blindness boundary, and the single
   authorized research-note path;
4. revisit only a named decision delta when all identities hold; and
5. require a fresh blind Prompt 1 pass for unexpected authority, intent, or
   checkpoint drift.

## Prompt 1 proof

- Complete read-back covered the campaign contract, authoring skill and
  glossary, repository primer and owning contracts, applicable ADRs, complete
  caller surfaces that define single-item admission, and relationship owners
  for diagnosis/TDD, review, conflict handling, and tracker compatibility.
- The unit ledger covers each independent trigger, action, judgment, branch,
  gate, Return, and completion condition and gives every unit an authority,
  neutral expression, correct/wrong entry, failure Return, and proof.
- The clause-to-intent audit maps all 16 runtime clauses and admits no
  source-derived technique.
- The viability suite is separate from later improvement claims.
- The checkpoint fingerprint and all local file identities were recomputed
  after writing.
- The campaign's ambient managed-install dry-run
  (`--skip-global-agents`) reported 25/25 unchanged with an empty changed
  cohort. It was inspected only as starting-state evidence and reused for no
  M0 behavior claim.
- Proportionate proof only: no target tests or full suite were run.

Authorized unit completed: Deploy Prompt 1
Decision: ready-for-research
Campaign shape: not-yet-classified; blind Prompt 1 does not inspect current or materialize H1
Runtime identities: M0 checkpoint frozen; current, exact M0 runtime bytes, and H1 remain uninspected or unmaterialized
Artifacts changed: docs/validation/transcripts/2026-07-24-implement-prompt1-m0.md
Evidence used or reused: local intent authorities and relationship-owner contracts listed above; no prior candidate proof reused
Residual gaps: exact runtime wording, current/M0/H1 identity, research support, behavioral efficacy, and executed viability proof remain for successor units
Recommended next unit: Deploy Research Pass using the authorized research-note path above
Git HEAD: 94d68e78d8812e9a2ceffd093e729402cac1cff2 -> 94d68e78d8812e9a2ceffd093e729402cac1cff2
Git delivery: pending
Exact stop reason: Prompt 1 froze the blind M0 checkpoint and the Shared Run Contract forbids starting its successor.
