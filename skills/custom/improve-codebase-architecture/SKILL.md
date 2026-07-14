---
name: improve-codebase-architecture
description: Survey a codebase for architectural friction, rank deepening candidates in a visual report, then pressure-test the chosen candidate.
---

# Improve Codebase Architecture

Own one outcome: a source-traced architecture survey whose selected deepening candidate is pressure-tested and routed. Load `$codebase-design` as survey vocabulary; use its direct design pass only for the selected candidate.

## Boundary

- The survey may write one disposable report under ignored `.tmp/architecture-reviews/`.
- `$research` may write one cited note only with caller approval for that tracked mutation; otherwise record a named evidence gap.
- Selected-candidate domain writes flow only through `$grill-with-docs` and its gates.
- Keep product code, other tracked docs, tracker state, the index, and commits unchanged. Reopen an ADR only for material new friction.

## Process

### 1. Trace

**Trace.** Follow a user-named module, subsystem, or pain point. Otherwise start with recently changed hotspots and widen only when churn is scattered.

Build the **Source Trace** from the request, repo instructions, routed engineering and domain docs, relevant ADRs, current implementation, representative callers and tests, and operational constraints. Without domain routing, use `CONTEXT-MAP.md`, root `CONTEXT.md`, and local domain or ADR docs.

Name the survey regions and evidence gaps. For a missing load-bearing external fact, name one source question; invoke `$research` only under the approved note boundary above.

### 2. Scout

**Scout.** Use direct fresh-context read-only scouts when independent judgment matters and the survey partitions cleanly. Start each with `fork_turns="none"` when supported. Give each a self-contained frame, shared vocabulary, one bounded region or pressure, source pointers, mutation boundary, and output contract. Exclude parent hypotheses, preferred candidates, and peer results. Scouts inspect and report only; they never edit files, mutate external state, or spawn. The main agent alone owns synthesis, filtering, ranking, and the report.

When continuity matters more than independence, fork only the minimum necessary recent context and do not call the result independent. Use one pass for a small or unpartitionable repo.

Scout friction: repeated concept jumps, caller-spread decisions, shallow or leaking seams, implementation-bound tests, pass-through indirection, and unclear ownership.

### 3. Filter

**Filter.** Apply the **deletion test**: removing pass-through indirection eliminates complexity; removing an earning module redistributes it. Keep only candidates where a deeper owner could concentrate behavior behind a smaller interface and plausibly improve depth, leverage, locality, or the caller-facing test surface.

Account for every survey region with evidence or a named gap. Give every surviving candidate a Source Trace and deletion-test result. Exclude cleanup-only work and speculative abstraction.

### 4. Report

**Report.** Confirm `.tmp/architecture-reviews/` is ignored; otherwise recommend `$repo-bootstrap` and stop. Read [HTML-REPORT.md](HTML-REPORT.md) completely, then write one self-contained report there.

Show current friction, the responsibility that could consolidate, and a validation angle; leave dependency classification and interface contracts to the selected-candidate pass. Number and rank the candidates, end with one **Top recommendation**, return the absolute report path, ask the user to select one candidate, and stop.

### 5. Grill

**Grill.** After selection, invoke `$grill-with-docs` with the candidate, report path, Source Trace, and survey bounds. It owns the interview and durable domain capture.

Return its **Evidence gap** packet and stop. Only a **Confirmed** packet proceeds. Invoke `$codebase-design` only when the confirmed candidate still needs dependency classification, seam discipline, or meaningfully different interface alternatives; collect its design packet.

### 6. Route

**Route.** Classify the confirmed candidate and recommend exactly one next skill:

- **single-slice** — `$implement` when one bounded slice can complete the intent with clear proof;
- **multi-slice** — `$to-tickets` when the settled direction needs dependency-ordered slices;
- **underspecified** — `$to-spec` when intent, acceptance, architecture, or validation remains unresolved.

Return an **architecture packet** with the report path, chosen candidate, Source Trace, `$grill-with-docs` exit packet, any `$codebase-design` packet, classification, and recommended route with reason. Stop without starting downstream work.

## Completion

The survey pass is complete only when every region is accounted for, every reported candidate passes both filters, the numbered report and Top recommendation exist, its absolute path is returned, and tracked state stayed within the boundary.

The selected-candidate pass is complete only from a Confirmed grilling exit, with domain and ADR outcomes accounted for, any required design packet present, and exactly one downstream route recommended without execution.
