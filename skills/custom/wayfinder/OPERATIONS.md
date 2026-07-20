# Wayfinder Operations

Read only the operation selected by `SKILL.md`'s state table. `SKILL.md` owns the Mutation Envelope, Graph Growth, Reconcile, Return, and completion table. [MAP-FORMAT.md](MAP-FORMAT.md) owns persisted fields. The target tracker mapping supplies provider objects and primitives only.

## Qualification And Chart

Use only when the stable destination-identity lookup returns zero maps.

1. **Qualify.** Invoke `$grill-with-docs` only far enough to settle the destination, scope, route-closing condition, authority, initial dependency graph, finite budgets, domain mode, and exact evidence gaps. Pass the locked domain-persistence mode and ADR boundary: `authorized now` permits only confirmed domain writes with read-back and Source Trace; `deferred to Closeout` permits only a pending domain delta and no domain write; ADR creation always remains separately approval-gated. Read [Design Coherence Frame](../codebase-design/DESIGN-COHERENCE.md#frame); record each criterion as a sourced Constraint, bounded Question, Evidence gap, or evidenced non-applicability without choosing architecture. Read [MAP-FORMAT.md](MAP-FORMAT.md) while drafting the packet.
2. **Admit.** Require one bounded destination, route-closing condition, and affirmed authority; at least two interdependent unresolved material decisions; at least one non-conversational dependency; durable tracker-backed sequencing; in-scope obligations; finitely tethered fog; a frontier or one waiting trigger; represented design concerns; approved graph-derived outcome and expansion budgets with their calculations and named contingency or `none`; and every required tracker mapping and capability.
3. **Reject.** Admission mutates nothing. A missing tracker capability recommends `$repo-bootstrap` and stops. Other terminal residuals invoke `$skill-router` with attempted route, reason, settled state, residual work, evidence, exclusions, and `Excluded route: $wayfinder unless material new evidence appears`; return its one recommendation or `none` without downstream execution.
4. **Approve.** Using [MAP-FORMAT.md](MAP-FORMAT.md), present the exact map, children, edges, fog, authority, design and domain state, budgets, allowed resolver types, resolver contracts, expected returns, participation, judgment criteria, mutation boundaries, and initial state as one mutation packet. Obtain destination-owner approval and record its evidence; any changed packet needs fresh approval.
5. **Chart.** Keep [MAP-FORMAT.md](MAP-FORMAT.md) open. Repeat the stable identity lookup. On zero, create only the map and rerun the identity-wide lookup. Create children, fog, exclusions, and edges only when exactly that new map is canonical and its provider identity is the one just created.
6. **Verify.** Read [MAP-FORMAT.md](MAP-FORMAT.md) while reading back the complete representation and derived initial frontier or wait. Resolve no ticket, retain no claim, Return, and stop.

When a different, multiple, zero-after-create, or unreadable identity appears, stop before children with created-map evidence and the exact recovery or classification owner.

## Advance

Advance processes exactly one frontier ticket toward one substantive outcome or one authorized external wait.

1. Orient and select the named frontier ticket or the first in map order.
2. Verify its reserved outcome or correction unit and reconcile total, reserved, used, and uncommitted capacity.
3. Under the Mutation Envelope, invoke exactly one locked resolver with its default participation and return:
   - **Research — AFK:** `$research`; return answer, citations, limits, and approved note.
   - **Prototype — conditional:** `$prototype`; use `shape/feel` HITL, objective `design evidence` AFK, or explicitly human-reserved evidence HITL; return verdict, evidence, limits, and cleanup state.
   - **Diagnosis — AFK by default:** `$diagnosing-bugs`; use HITL only when reproduction requires live human action; return reproduction, cause status, evidence, regression seam, and blocker without fixing.
   - **Questionnaire — external:** before invoking `$to-questionnaire`, pass every delegated field persisted in [MAP-FORMAT.md](MAP-FORMAT.md); return one artifact and needed-back ledger without sending or interpreting answers. A missing delegated field is a transient incomplete attempt, not an external wait.
   - **Grilling — HITL:** `$grill-with-docs`; return one user-owned decision, complete domain delta, deferrals, and ADR outcome or evidence gap under the locked persistence mode.
   - **Design — AFK by default:** `$codebase-design`; use objective locked criteria. Use HITL when a public contract, irreversible migration, product tradeoff, or named owner reserves judgment; return one bounded design packet and acceptance evidence.
   - **Task — AFK by default:** inspect and prove one bounded repository or operational fact directly; use HITL only when evidence gathering requires live human action. Return the supported answer, affected boundary, proof, disposable evidence, and blocker; make no durable mutation.
4. On a transient incomplete attempt, record recovery evidence, leave outcomes and counters unchanged, release and read back the claim, and Return. A repeated or confirmed persistent failure becomes Blocked only with one durable exact intervention or external prerequisite.
5. For a verified Questionnaire artifact, record `awaiting-external-response`, artifact, ledger, owner, and observable trigger; preserve its reservation and used counter; Reconcile to `active` when another frontier remains or `waiting` otherwise; release the claim and Return.
6. Otherwise record exactly one substantive `Resolved`, `Blocked`, or `Out Of Scope` outcome and convert its reservation to used.
7. Apply Graph Growth and Reconcile only direct tickets, dependencies, fog, domain candidates, design consequences, counters, and disposition. Complete the envelope and Return. Only when the required fresh Orient selects Closeout may this invocation enter Closeout; never start a second resolver or Advance.

Verified supplied Questionnaire answers are processed by a later Advance: trace the ledger and resolve, split, or exactly reblock the ticket.

## Maintain

Use only for `repairable-drift`.

1. Build one exact consequence-only repair packet with evidence for every change. The open charter pre-authorizes it only when accepted evidence and current contracts permit one result.
2. Under the Mutation Envelope, apply only contract-determined canonical-section, stale-fog, broken-pointer, scope-index, dependency, claim-metadata, or equivalent representation repairs.
3. Give affected fog items one Reconcile disposition. Record no substantive ticket outcome or material decision.

When repair permits discretion, changes meaning or scope, needs a decision, or requires an unavailable tracker capability, return `incompatible` with the owner. Closed records never use Maintain.

## Resume

Resume reconciles one newly satisfied liveness condition without resolver work or outcome-budget use.

1. Orient and select one recorded waiting trigger or blocker intervention whose evidence is observable.
2. Reject incomplete evidence, destination or scope change, and attempts to extend exhausted budgets.
3. Under the Mutation Envelope, run one branch:
   - **Wake:** verify waiting and needed-back evidence, then make its existing ticket dependency-ready or reconcile directly affected fog.
   - **Recover:** verify the intervention, then restore only the tickets, edges, fog, authority packet, or frontier it unlocks. An authority transfer requires the recorded outgoing and incoming approval or tracker-governed higher authority and changes no decision or budget.
4. Apply Graph Growth, persist `active`, `waiting`, or `blocked`, and Return. Other satisfied conditions remain for later Resume operations.

## Closeout

Closeout is `Gather -> Coherence -> Durability -> Seal`. Entry requires fresh proof that no unresolved ticket, tethered fog, external wait, material contradiction, exact blocker, or exhausted-budget decision remains. Gather, Coherence, and Durability hold no claim.

### Gather

Read every closure group in [MAP-FORMAT.md](MAP-FORMAT.md). Record all declared fields, evidence pointers, and the Gather provider-revision vector. Complete only when every obligation has one disposition and the packet supports Coherence.

### Coherence

Read [Design Coherence Check](../codebase-design/DESIGN-COHERENCE.md#check). Test without deciding, redesigning, or persisting:

- **Destination:** every accepted resolution supports the destination, scope, route-closing condition, and settled-engineering boundary.
- **Decision:** dependent decisions agree across public and data contracts, state and lifecycle, permissions, environments, migration, cutover, rollback, security, and compatibility.
- **Domain:** language, context ownership, and boundaries agree with canonical truth or one explicit pending delta; every collision is accounted for.
- **Design:** apply the shared Design Coherence Check to responsibilities, interfaces, dependencies, seams, migration, and proof.
- **Evidence:** every material conclusion has the source, runnable evidence, causal proof, human authority, external response, or repository proof required by its ticket.

Record `pass` evidence or typed gaps for every lens.

A material gap uses Graph Growth. Acquire a short Closeout-gap claim only to reopen or create one already-detected authorized obligation. Missing amendment, capacity, cohesion, authority, or scope returns its exact blocker without mutation.

### Durability

After Coherence passes, invoke `$domain-modeling` under the charter's persistence mode. Return `none`, verified persistence with paths, or a pending-authority/material-contradiction packet. ADR creation always requires explicit approval. Hold no claim during approval waits.

An already-accounted domain delta may persist consequence-only. New or changed material meaning returns through Graph Growth before any gap mutation.

### Seal

Under a Closeout-Seal Mutation Envelope:

1. Refetch every declared field and record the pre-Seal revision vector.
2. Compare field semantics with Gather, excluding expected claim transport; treat verified already-accounted domain persistence as equal.
3. On semantic change, release and Return for reorientation. Unrelated transport or formatting revision may refresh evidence and continue.
4. On equality, merge Durability and both vectors into the sealed packet; close as `delivered`; read back packet, state, and post-close revision.
5. Release the claim; read back absence and post-release revision; recommend `$to-spec`; stop.

## Terminate

Wayfinder classifies evidence; the destination owner confirms whole-map termination:

- `cancelled`: the destination remains valid but its owner stops;
- `superseded`: an approved successor owns the remaining purpose; or
- `out-of-scope`: the approved campaign boundary excludes the destination.

Without confirmation, keep the map open. With confirmation, use the Terminate Mutation Envelope to persist disposition, authority, reason, evidence, budgets, unresolved obligations, and recovery or successor boundary; close and read back; Return without Coherence, Durability, Seal, or To Spec.

## Reopen

Use only for a delivered map and one concrete To Spec return.

- **Direct in-scope consequence:** obtain an approved correction packet or amendment containing the To Spec evidence, in-scope classification, one cohesive dependency graph, acceptance authority, proof, and finite cumulative correction capacity. Under the Reopen envelope, preserve prior generations and open only the authorized frontier.
- **Destination or scope change:** leave the map immutable and qualify a successor.
- **Unclear classification:** stop for destination-owner judgment.

Every correction ticket traces to the same To Spec return, lies inside the original bound, belongs to one connected component, and restores the same failed closure condition. Independent gaps, wider work, missing cohesion, or exhausted capacity require a successor. After correction, Closeout restarts at Gather and adds one immutable generation.

A successor receives fresh Qualification, Admission, approval, budgets, state, graph, frontier, and claims. It explicitly imports or invalidates predecessor decisions and evidence; nothing else transfers.
