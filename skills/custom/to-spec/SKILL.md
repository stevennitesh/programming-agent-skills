---
name: to-spec
description: Synthesize settled source into a source-traced parent spec and publish it to the configured tracker.
---

# To Spec

Create the **parent spec**: the durable product and engineering intent artifact sometimes called a PRD.

This is **synthesis**. Treat the source as settled, recover its intent, ground it in repo context, choose the proof seam, and publish a spec a fresh Codex session can trust.

Use the target repo's `AGENTS.md` for tracker, label, and domain docs. If a required setup document or named tracker operation is absent or incompatible with this skill, stop and recommend `$repo-bootstrap`.

## Process

### 1. Trace Source

Trace the current conversation, supplied artifacts, and directly required context they name. Read every supplied artifact in full, including decision-bearing comments and directly required linked context.

Explore enough code to identify current modules, existing seams, proof surfaces, and relevant prior art. Use domain glossary terms for product concepts. Load `$codebase-design` as shared architecture vocabulary while this spec workflow remains authoritative. Surface conflicts with the domain glossary or ADRs.

Record every relied-on source in `Source Trace`.

A **material gap** is the only reason to pause: ask when an unsettled decision would change product intent, scope, architecture, or proof. Put every non-blocking uncertainty in `Open Questions`.

### 2. Choose Proof Seam

Choose the highest existing seam that proves user-visible behavior. Propose and justify a new load-bearing seam only when existing seams cannot prove the spec.

Before drafting, name the seam, behavior proven, relevant prior art, and regression risks. Apply the material-gap gate when the choice is unsettled; otherwise cite its source in `Source Trace`.

### 3. Write And Publish

Pass the **fresh-session test**: a new Codex session can recover the shared understanding from the spec alone.

Sections:

- `Source Trace`
- `Problem Statement`
- `Desired Outcome`
- `User Stories`
- `Accepted Decisions`
- `Deferred Or Rejected Options`
- `Edge Cases And Failure Modes`
- `Proof Seams And Testing Notes`
- `Out Of Scope`
- `Open Questions`
- `Further Notes` - omit when empty

Number each user story and name its actor, capability, benefit, edge cases, and acceptance branches.

Keep proof notes at spec level: seams, proof points, likely tracer bullets, useful fixtures, prior patterns, and regression risks.

Include file paths or code snippets only when a durable contract or prototype finding encodes a decision more precisely than prose.

**Coverage gate:** before publishing, account for every source-visible commitment, actor, flow, constraint, edge case, failure mode, prototype finding, and scope boundary in the appropriate section, or mark it explicitly irrelevant in `Source Trace`.

**Publication scope:** mutate only the `.tmp/` draft and one published parent spec. Treat supplied artifacts as sources unless the user explicitly asks to update them. `$to-tickets` owns implementation slicing, blocking edges, and `ready-for-agent` state.

Draft under `.tmp/to-spec/<slug>.md`.

Publish through the tracker and label docs routed by `AGENTS.md`.

Apply the tracker's **Mutation read-back** rule. Verify the published body and metadata against the draft. After successful verification, delete the disposable draft unless the user explicitly asks to preserve it. Preserve and report the draft when publication or read-back is blocked.

End with the published parent reference, any intentionally preserved draft path, and a recommendation for `$to-tickets` when implementation slicing is next.

## Completion Criteria

Complete only when every supplied artifact was fully read, every relied-on source is traced, the coverage gate passes, every material gap is resolved, remaining gaps are recorded in `Open Questions`, the spec is repo-grounded, proof-seam-aware, passes the fresh-session test, and the published parent was read back successfully. The disposable draft is deleted after success or intentionally preserved and reported after a blocker or explicit user request.
