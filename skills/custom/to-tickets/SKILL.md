---
name: to-tickets
description: Create and publish approved, dependency-ordered ready-for-agent tickets from settled source material.
---

# To Tickets

Create **ready-for-agent tickets** from settled source material.

Default to **tracer bullets**: independently grabbable vertical slices through the real system, each demoable or verifiable independently. Use **support slices** when they unblock or de-risk a named tracer bullet.

Apply the **setup gate**: use the target repo's `AGENTS.md` for tracker, label, domain, and packet docs. If a required setup document or named tracker operation is absent or incompatible with this skill, stop and recommend `$repo-bootstrap`.

## Process

### 1. Trace Source

Trace the current conversation, repo `AGENTS.md` and named docs, explicit user approvals, and every supplied parent artifact in full, including decision-bearing comments and directly required linked context.

Identify parent source, user-facing outcome, accepted decisions, out-of-scope boundaries, and prototype findings.

A **source gap** is a needed decision outside the trace; return it to the caller before slicing.

### 2. Map Work

Explore enough code to name stable seams, **proof lanes**, and support slices that materially de-risk tracer bullets.

Use domain vocabulary from the source trace. Use ADR and glossary pointers when they affect ticket shape.

Leave patch design and exact file choices to implementation.

### 3. Draft Slices

Split the work into dependency-ordered tickets with clear **blocking edges**.

Every ticket satisfies the tracker's **Ready-for-agent contract**. Add the slicing fields this skill owns:

- Parent reference
- Why this slice
- What to build: end-to-end behavior or support change
- Relevant context: source trace and applicable glossary, ADR, or prototype pointers

Tracer-bullet tickets deliver one narrow behavior across every needed layer. Support slices name the tracer bullet they unblock or de-risk and the proof that makes them done.

Cut tickets for distinct behaviors, branches, failure modes, permission boundaries, state transitions, integration seams, migration risks, or required support work. Start with the happy-path tracer bullet when the end-to-end path is still unproven.

Size each ticket for one fresh implementation session.

A **wide refactor** is a mechanical **blast-radius** change that cannot land green as a tracer bullet. Use **expand-contract**: expand first; migrate callers in green batches, each blocked by expand; contract only after every batch. If no batch can stay green alone, use one integration branch and a final integrate-and-verify ticket blocked by every batch.

Use file paths or code snippets only for durable contracts or prototype findings that encode a decision more precisely than prose.

**Coverage gate:** before review, account for every source-visible implementation commitment and scope boundary—including accepted decisions, behaviors, constraints, edge cases, failure modes, and prototype findings—by mapping it to a ticket, the parent's deferred or out-of-scope set, or an explicit no-ticket reason.

### 4. Review Breakdown

Show the proposed breakdown before publishing:

```markdown
1. <Ticket title>
   Blocked by: <none / ticket title>
   Covers: <user stories or behavior>
   Proof lane: <observable acceptance through a repo-owned seam, command, or artifact>
   Why this slice: <one sentence>
   Write scope: <stable modules, interfaces, commands, docs, or discover during implementation>
   Parallel safety: <independent after blocker / overlaps with sibling issues / serialize because...>
```

Apply the **approval gate**: ask the user to approve granularity, order, blocking edges, acceptance criteria, proof lanes, write scope, and parallel safety. Iterate until approved.

### 5. Publish

Publish approved tickets in dependency order, blockers first, through `docs/agents/issue-tracker.md`. Follow the repo docs it points to for labels and packet conventions.

Record parent and child links, ticket order, blocking edges, source trace, durable context pointers, readiness, proof lanes, write scopes, and parallel safety according to the repo packet convention.

Apply the tracker's **Mutation read-back** rule to the parent and every published ticket. Verify bodies, relationships, blocking edges, labels or state, and the resulting ready frontier. Treat a partial publication as blocked and report the safest recovery.

**Publication scope:** publish only the approved tickets and required parent, dependency, and packet metadata. Preserve the parent's intent and lifecycle state; change its body only when the tracker convention requires child links. End before implementation execution, code review, or closeout.

Name the initial **ready frontier**: published tickets that are unblocked and unclaimed under the tracker convention.

End with the published ticket references, packet path when applicable, initial ready frontier, and exactly one next action: resolve the named blocker when the frontier is empty; recommend `$implement` for the first ready ticket when the frontier is singular or write-overlapping; recommend `$parallel-implement` when at least two frontier tickets have non-overlapping write scopes and proof lanes.

## Completion Criteria

Complete only when the setup, coverage, and approval gates pass; no source gap remains; every ticket satisfies the Ready-for-agent contract; approved tickets are published blockers-first with explicit blocking edges; publication is read back without partial failure; required label and packet conventions are satisfied; publication stayed inside scope; and the initial ready frontier plus one next action are reported.
