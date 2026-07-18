---
name: improve-codebase
description: Survey a bounded codebase, classify evidence-backed improvement candidates as elimination, concentration, retention, or investigation, rank the best next move in a visual report, and route an explicitly selected candidate. Use explicitly when existing code is bloated, hard to change, or the right improvement is uncertain.
---

# Improve Codebase

Own one outcome: one verified improvement report, or one explicitly selected candidate resolved, reclassified, and routed without downstream execution. Load `$codebase-design` as survey vocabulary; use its direct pass only for a selected candidate.

**Survey: Trace -> Scout -> Classify -> Sequence -> Rank -> Report -> Return.**

If the invocation names `Candidate N` and a report, read [SELECTED-CANDIDATE.md](SELECTED-CANDIDATE.md) completely and run only that branch. Otherwise run the Survey and stop.

## Boundary

- Write and later update one disposable report only under ignored `.tmp/improvement-reviews/`.
- Keep product code, other tracked docs, tracker state, the index, commits, and external systems unchanged.
- Survey scouts are read-only. Selected-candidate writes flow only through an invoked skill's own gates.
- Flag domain or ADR pressure; durable domain changes belong to `$grill-with-docs` and `$domain-modeling`.

## Survey

### Trace

**Trace.** A user-named module, subsystem, path, or pain point wins. Otherwise inspect a bounded commit-history window, anchor repeated-change hotspots to commits or paths, and start there. When history is thin or churn is scattered, widen deliberately through entry points, manifests, ownership boundaries, and representative workflows. Partition an explicitly whole-codebase request into named regions.

Build the **Source Trace** from the request, repo instructions, routed engineering and domain docs, relevant ADRs, current implementation, representative callers and tests, history, and operational constraints. Name every survey region and evidence gap.

### Scout

**Scout.** Use direct fresh-context read-only scouts when independent judgment matters and the regions partition cleanly. Start each with `fork_turns="none"` when supported. Give each one bounded region or pressure, the shared vocabulary, source pointers, mutation boundary, and output contract. Exclude parent hypotheses, preferred candidates, and peer results. Scouts inspect and report only; they never edit, mutate external state, or spawn. The main agent alone classifies, sequences, ranks, and reports.

Use one pass for a small or unpartitionable repo. Scout repeated concept jumps, caller-spread decisions, shallow or leaking seams, implementation-bound tests, pass-through indirection, duplicate policy, dead compatibility, and unclear ownership.

### Classify

**Classify.** Apply the **deletion test**: if removing the code makes complexity disappear, **Eliminate** it; if complexity spills into callers, **Concentrate** it behind an earning owner. Mark a region **Retain** when its current boundary already earns its cost. Mark **Investigate** only when one precise evidence question blocks a safe disposition.

Account for every region. Number only `Eliminate`, `Concentrate`, and `Investigate` candidates; keep `Retain` regions in the survey ledger. Exclude speculative work that lacks both evidence and a decision-relevant investigation question.

Each numbered candidate records:

- region, disposition, Source Trace, observed friction, and deletion-test result;
- behavior and commitment boundary;
- elimination target or responsibility to concentrate;
- proof seam;
- uncertainty: `none`, `source`, `runnable`, or `user-decision`, with one evidence route when present;
- sequence relationship, risk, blast radius, rank rationale, next skill, and exact pickup invocation.

Set the provisional owner by disposition: `Eliminate` points to `$simplify-code` after selected-candidate verification; `Concentrate` points to selected design or delivery resolution; `Investigate` points to its one evidence route; `Retain` has no next skill. Every numbered card's immediate pickup remains `$improve-codebase Candidate N from <absolute-report-path>` so the selected branch verifies and reclassifies before handoff.

### Sequence

**Sequence.** Relate overlapping candidates as:

- **Independent** — either earns its place alone;
- **Preparatory for Candidate N** — remove noise before evaluating or designing the other candidate;
- **Absorbed by Candidate N** — the other change replaces this work, so avoid duplicate churn;
- **Residual after Candidate N** — revisit only what remains after the other change.

### Rank

**Rank.** Compare evidence and proofability; total concepts, coordination, caller burden, or dependencies removed; recurring friction; risk and reversibility; and overlap. Prefer `Eliminate` when otherwise tied. Rank an `Investigate` candidate first only when its exact question unlocks more value than the supported alternatives. Name one **Top recommendation** without numeric scoring.

### Report

**Report.** Confirm `.tmp/improvement-reviews/` is ignored; otherwise recommend `$repo-bootstrap` and stop. Read [HTML-REPORT.md](HTML-REPORT.md) completely, then write one self-contained report there.

Reread the report and, when supported, render or open it. Verify that it is offline and script-free, candidate IDs and anchors resolve, the survey ledger accounts for every region, visuals match dispositions, and the Top recommendation or **No candidate recommended** verdict matches the classified set.

### Return

Return the absolute report path and the Top recommendation or **No candidate recommended**. For a non-empty report, include the exact pickup `$improve-codebase Candidate N from <absolute-report-path>` and stop. Do not resolve, select, research, prototype, grill, design, or execute a candidate during the Survey.

## Completion

The Survey is complete only when every region is classified with evidence or one precise gap; every numbered candidate has the required packet; sequencing and ranking account for overlap; the verified report matches the set; the absolute path and any pickup are returned; and the mutation boundary held. A verified **No candidate recommended** report is complete.
