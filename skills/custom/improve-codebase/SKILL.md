---
name: improve-codebase
description: Survey a bounded codebase, classify and rank evidence-backed opportunities to eliminate, concentrate, retain, or investigate, then route one explicitly selected candidate. Use explicitly when code is bloated, hard to change, or the best improvement is uncertain.
---

# Improve Codebase

**Outcome:** one verified improvement report, or one selected candidate reclassified and routed. Downstream execution stays outside this skill.

Load `$codebase-design` as survey vocabulary; invoke its direct pass only from the selected-candidate branch.

**Survey: Trace -> Scout -> Classify -> Sequence -> Rank -> Report -> Return.**

When the invocation names `Candidate N` and a report, read [SELECTED-CANDIDATE.md](SELECTED-CANDIDATE.md) completely and run only that branch. Otherwise run the Survey.

## Boundary

- Mutate only one ignored `.tmp/improvement-reviews/` report; selected resolvers write only through their own gates.
- Keep product code, other tracked docs, tracker state, the index, commits, and external systems unchanged.
- Scouts are fresh-context, read-only, and non-spawning.

## Survey

### Trace

**Trace. Caller bound wins.** Otherwise use bounded history to find repeated-change hotspots. When history is thin or churn scattered, widen through entry points, manifests, ownership boundaries, and representative workflows. Partition a whole-codebase request into named regions.

Build the **Source Trace** from the request, repo instructions, routed engineering and domain docs, ADRs, implementation, representative callers and tests, history, and operational constraints. Name every region and evidence gap.

### Scout

**Scout.** Dispatch direct scouts only for cleanly partitioned regions; start them with `fork_turns="none"` when supported. Give each one region or pressure, shared vocabulary, source pointers, mutation boundary, and output contract—no parent hypotheses, preferred candidates, or peer results. The root alone owns Classify through Return.

Use one root pass for a small or unpartitionable repo. Inspect concept jumps, caller-spread decisions, shallow or leaking seams, implementation-bound tests, pass-through indirection, duplicate policy, dead compatibility, and unclear ownership.

### Classify

**Classify. Deletion test.** Complexity that disappears is **Eliminate**; complexity that spills into callers is **Concentrate** behind an earning owner. A boundary that earns its cost is **Retain**. One precise evidence question blocking a safe disposition is **Investigate**.

**Ledger.** Account for every region. Number only `Eliminate`, `Concentrate`, and `Investigate`; keep `Retain` in the survey ledger. Reject speculation without both evidence and a decision-relevant question.

Each numbered candidate records:

- region, disposition, Source Trace, observed friction, and deletion-test result;
- behavior and commitment boundary;
- elimination target or responsibility to concentrate;
- proof seam;
- resolution need: `none`, `repository`, `source`, `runnable`, `user-decision`, or `design`, with one evidence route when present;
- sequence relationship, risk, blast radius, rank rationale, provisional destination, and exact immediate pickup invocation.

**Destination.** `Eliminate` -> `$simplify-code`; `Concentrate` -> selected design or delivery resolution; `Investigate` -> its evidence route; `Retain` -> none. Every numbered card's immediate pickup is `$improve-codebase Candidate N from <absolute-report-path>` so this skill verifies and reclassifies before handoff.

### Sequence

**Sequence.** Encode overlap as:

- **Independent** — no required ordering;
- **Preparatory for Candidate N** — precedes evaluation or design of N;
- **Absorbed by Candidate N** — N replaces this work;
- **Residual after Candidate N** — revisit only what remains after N.

### Rank

**Rank.** Compare evidence and proofability; concepts, coordination, caller burden, or dependencies removed; recurring friction; risk and reversibility; and overlap. Prefer `Eliminate` on ties. Rank `Investigate` first only when its question unlocks more value than supported alternatives. Name one **Top recommendation** without numeric scoring.

### Report

**Report.** Require `.tmp/improvement-reviews/` to be ignored; otherwise recommend `$repo-bootstrap` and stop. Read [HTML-REPORT.md](HTML-REPORT.md) completely and write one self-contained report there.

**Verify.** Reread and, when supported, render or open the report. Prove it is offline and script-free; anchors resolve; the ledger covers every region; visuals match dispositions; and the Top recommendation or **No candidate recommended** matches the classified set.

### Return

**Terminal.** Return the absolute report path and the Top recommendation or **No candidate recommended**. For a non-empty report, include `$improve-codebase Candidate N from <absolute-report-path>`. Start no candidate resolution or execution.

## Completion

Complete when the Boundary holds; the Ledger covers every region; candidate packets, overlap, ranking, and Verify pass; and the absolute path plus any pickup are returned. A verified **No candidate recommended** report is complete.
