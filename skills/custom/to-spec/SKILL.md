---
name: to-spec
description: Synthesize settled source into a source-traced parent spec and publish it to the configured tracker.
---

# To Spec

Own one outcome: a source-traced **parent spec** that preserves settled product and engineering intent for a fresh Codex session.

Use the target repo's `AGENTS.md` for tracker, label, and domain pointers. If a required setup document or named tracker operation is absent or incompatible with this skill, recommend `$repo-bootstrap` and stop.

## Process

### 1. Trace

Trace the settled source: the conversation; every supplied artifact in full; decision-bearing comments; required linked context; and relevant code, prior art, domain terms, and ADRs. Surface domain or ADR conflicts. Record every relied-on source in `Source Trace`.

Load `$codebase-design` as shared architecture vocabulary; this skill retains spec ownership.

Pause only for a **material gap**: an unsettled decision that would change product intent, scope, architecture, or proof. Record other uncertainty in `Open Questions`.

### 2. Choose

Choose the highest existing **proof seam** that proves user-visible behavior. Add a new load-bearing seam only when no existing seam can prove the spec.

Record the seam, behavior proved, prior art, and regression risks. A disputed load-bearing choice is a material gap.

### 3. Draft

Draft under `.tmp/to-spec/<slug>.md`. Pass the **fresh-session test**: the spec alone recovers the shared understanding.

Use these sections:

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

Write a comprehensive, numbered set of user stories that exhausts every source-visible actor, capability, benefit, edge case, and acceptance branch. Keep proof notes to seams, proof points, likely tracer bullets, fixtures, prior patterns, and regression risks. Include paths or snippets only when a durable contract or prototype finding preserves a decision more precisely than prose.

### 4. Cover

Apply the **coverage gate**: account for every source-visible commitment, actor, flow, constraint, edge case, failure mode, prototype finding, and scope boundary, or mark it irrelevant in `Source Trace`.

### 5. Publish

Mutate only the draft and one parent spec. Supplied artifacts remain sources unless the user explicitly asks to update them. `$to-tickets` owns implementation slicing, blocking edges, and `ready-for-agent` state.

Publish through the tracker contract routed by `AGENTS.md`. Apply **Mutation read-back** to body and metadata. Delete the draft after successful read-back; preserve and report it when blocked or explicitly requested.

Return the parent reference, any preserved draft path, and recommend `$to-tickets` and stop when implementation slicing is next.

Complete only after Trace and Cover pass, no material gap remains, publication is read back, and draft cleanup or preservation is reported.
