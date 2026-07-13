---
name: improve-codebase-architecture
description: Survey a codebase for architectural friction, rank deepening candidates in a visual report, then pressure-test the chosen candidate.
---

# Improve Codebase Architecture

Run an **architecture survey**: find friction, rank real **deepening opportunities**, and help the user choose one.

This skill owns wide candidate discovery. Load `$codebase-design` as shared vocabulary; keep its direct design pass for one chosen candidate.

## Ownership

- **Architecture survey:** Own the Source Trace, scouts, deletion-test filtering, candidate ranking, visual report, and architecture packet.
- **`$grill-with-docs`:** Own the chosen-candidate interview and durable domain capture.
- **`$codebase-design`:** Own dependency classification, seam discipline, interface alternatives, and the design packet.
- **Downstream skills:** Own specs, tickets, implementation, tracker mutation, staging, and commits.
- **Mutation boundary:** The initial pass writes only a disposable report under ignored `.tmp/architecture-reviews/`. A `$research` lane may also write one cited note only when the caller approves that tracked mutation. Product code, other tracked docs, tracker state, the index, and commits stay unchanged. Chosen-candidate domain writes flow only through `$grill-with-docs` and its gates.

Use repo domain language for business concepts and `$codebase-design` vocabulary for architecture claims. ADRs mark decisions the survey reopens only when material new friction exists.

## Process

### 1. Orient

Build the **Source Trace** from:

- the request and repo instructions;
- `docs/agents/engineering-contract.md` when present;
- `docs/agents/domain.md` and its routed glossary and ADRs;
- the current implementation, representative callers, and tests;
- operational constraints relevant to the suspected seams.

Without domain routing, fall back to `CONTEXT-MAP.md`, root `CONTEXT.md`, and local ADR or domain docs.

When a load-bearing external fact is missing, name the exact source question. Invoke `$research` and link its note only when the caller approves that tracked mutation; otherwise record a named evidence gap.

Orienting is complete when the planned survey regions, domain and ADR constraints, relevant callers and tests, and known evidence gaps are named.

### 2. Scout

Use independent **scouts** when available and the repo or survey lenses can be partitioned. Give each scout the shared vocabulary, one bounded region or pressure, and a requirement to return source pointers. The main agent owns synthesis, deduplication, filtering, ranking, and the report. Use one pass for a small or unpartitionable repo.

Follow architectural friction first, checklist second.

Look for:

- one concept requiring repeated jumps across modules;
- shallow interfaces that expose nearly as much as their implementations;
- behavior or decisions spread across callers;
- pure helpers whose call choreography holds the real bugs;
- caller-facing tests blocked by implementation detail;
- seams that leak implementation knowledge;
- pass-through adapters or wrappers;
- owned modules mocked instead of proved through their interfaces;
- ownership that is difficult to locate.

Apply the **deletion test** to each suspected module or cluster. Removing pass-through indirection should eliminate complexity; removing an earning module would redistribute it. A candidate earns its place when a deeper owner could concentrate that behavior behind a smaller interface.

Apply the **deepening gate**: keep only candidates that plausibly improve **depth**, **leverage**, **locality**, or the caller-facing test surface. Exclude cleanup-only work and speculative abstraction.

Scouting is complete when every planned region or pressure returned evidence or a named gap, and every surviving candidate has a Source Trace and deletion-test result.

### 3. Report

Apply the **storage gate**: confirm `.tmp/architecture-reviews/` is ignored. If it is not, stop and recommend `$repo-bootstrap`.

Write one HTML report under `.tmp/architecture-reviews/`. Keep generated reports outside the index and commits.

Read [HTML-REPORT.md](HTML-REPORT.md) for report fields, visual style, tone, and diagram patterns.

Apply the **survey gate**: show the current friction, responsibility that could consolidate, and validation angle. The chosen-candidate pass owns dependency classification and interface contracts.

Number every candidate, rank them, and end with one **Top recommendation**. Open the report when possible and always report its absolute path.

Then ask:

> Which candidate number would you like to explore? I recommend Candidate N because ...

The initial pass stops here until the user selects a candidate.

### 4. Pressure-Test The Candidate

After selection, invoke `$grill-with-docs` with the candidate and Source Trace as its caller packet.

Pressure-test:

- constraints and public-contract commitments;
- current callers and behavior that could move behind the interface;
- seam, adapter, and substitute hypotheses;
- validation;
- bounded migration;
- out-of-scope boundaries.

Invoke `$codebase-design` when dependency classification, seam discipline, or meaningfully different interface alternatives are needed.

Treat load-bearing rejections as ADR candidates. Treat timing-only reasons as deferrals.

Honor `$grill-with-docs`'s **Confirmed** and **Evidence gap** exits. Only a Confirmed exit proceeds to classification.

### 5. Classify And Hand Off

Classify the confirmed candidate:

- **single-slice:** one bounded slice can complete the architectural intent;
- **multi-slice:** the direction is settled but completion needs dependency-ordered slices;
- **underspecified:** intent, acceptance, architecture, or validation remains unresolved.

Recommend exactly one route:

- `$implement` for a ready single-slice candidate with clear proof;
- `$to-tickets` for a settled multi-slice candidate;
- `$to-spec` for an underspecified candidate or one needing a durable parent spec.

Return an **architecture packet** containing:

- report path and chosen candidate;
- Source Trace;
- `$grill-with-docs` exit packet;
- `$codebase-design` design packet when used;
- classification;
- recommended route and reason.

Return the recommendation and stop. The user starts downstream execution.

## Completion Criteria

The initial pass is complete only when every planned survey region is accounted for; every reported candidate is source-traced and passes the deletion and deepening gates; the numbered visual report and Top recommendation exist; the report path is returned; tracked state remains unchanged except for any approved `$research` note; and the user is asked to select a candidate.

The chosen-candidate pass is complete only after a Confirmed grilling exit; every resolved domain or ADR outcome is accounted for; any required design packet exists; the architecture packet is returned; and exactly one downstream route is recommended without executing it.
