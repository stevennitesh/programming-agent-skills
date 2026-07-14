---
name: to-tickets
description: Create and publish approved, dependency-ordered ready-for-agent tickets from settled source material.
---

# To Tickets

Own one outcome: approved, dependency-ordered **ready-for-agent tickets** from settled source.

Use **tracer bullets** by default: independently grabbable, end-to-end slices that are independently verifiable. Use **support slices** only when they unblock or de-risk a named tracer bullet.

`docs/agents/issue-tracker.md` and its pointers own tracker transport, the Ready-for-agent contract, label and packet mechanics, and Mutation read-back.

Apply the **setup gate** through the target repo's `AGENTS.md`. If a required setup document or named tracker operation is absent or incompatible with this skill, stop and recommend `$repo-bootstrap`.

## Process

### 1. Trace

Trace the conversation, explicit approvals, repo instructions and named docs, and every supplied parent artifact in full, including decision-bearing comments and directly required linked context.

Record the parent source, user-facing outcome, accepted decisions, scope boundaries, and prototype findings.

A needed decision outside the trace is a **source gap**. Report it and stop before slicing.

### 2. Map

Inspect relevant code only far enough to name stable seams, **proof lanes**, and durable domain, ADR, glossary, or prototype pointers.

Leave patch design and exact file selection to implementation. Include paths or snippets only when they encode a durable decision more precisely than prose.

### 3. Slice

Cut dependency-ordered **tracer bullets** with explicit **blocking edges**. Size each for one fresh implementation session.

Every ticket satisfies the tracker's Ready-for-agent contract and adds:

- parent reference;
- why this slice;
- what to build;
- relevant Source Trace and durable context pointers.

Separate behavior, state transitions, failure or permission boundaries, integration risks, and support work when they require independent proof. Start with the happy-path tracer when the end-to-end route is unproven.

A support slice names the tracer bullet it de-risks and its proof.

For a mechanical **blast-radius** change that cannot land green as a tracer bullet, use **expand-contract**: expand; migrate callers in green batches; contract after every batch. If batches cannot remain green independently, use one integration branch and a final integrate-and-verify slice blocked by every batch.

Apply the **coverage gate**: map every source-visible implementation commitment and scope boundary to a ticket, an explicit deferral or exclusion, or a no-ticket reason.

### 4. Approve

Show each proposed ticket's title, blockers, covered behavior, proof lane, why, expected write scope, and parallel safety.

Get explicit user approval for granularity, order, blocking edges, acceptance criteria, proof lanes, write scopes, and parallel safety before publishing.

### 5. Publish

Publish only the approved tickets and required parent, dependency, and packet metadata, blockers first, through `docs/agents/issue-tracker.md`.

Preserve the parent's intent and lifecycle state. Change its body only when the tracker convention requires child links. Stop before implementation, review, or closeout.

Apply **Mutation read-back** to the parent, tickets, relationships, blocking edges, state, and resulting **ready frontier**. A partial publication is blocked; report applied and failed operations plus the safest recovery.

Return the published references, packet path when applicable, verified initial ready frontier, and exactly one next action:

- empty frontier: resolve the named blocker;
- one ready ticket or write-overlapping tickets: recommend `$implement`;
- at least two tickets with independent write scopes and proof lanes: recommend `$parallel-implement`.

Complete only when the setup, source, coverage, and approval gates pass; every ticket satisfies the Ready-for-agent contract; publication and read-back succeed; and the verified frontier plus one next action are returned.
