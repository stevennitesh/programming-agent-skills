# Six-Lens Classification Behavior Protocol

Date: 2026-08-01
Status: preregistered before lens sampling

## Registration

- Mode: quality lift.
- Task: classify six fixed current-source observations and their closest wrong
  conditions under one supplied Audit Codebase package.
- Host and authority: fresh-context Codex Desktop subagents; read-only; no
  repository, report, tracker, downstream, or Git mutation.
- Control: the installed package frozen in `protocol.md`.
- Candidate: the final canonical package after the lifecycle evaluation's
  `authority-required` repairs.
- Cohort: five independent controls. Admit five candidate samples only when a
  control deficit appears.

## Fixed Cases And Rubric

Each sample classifies the positive and closest wrong condition, names the
primary class, chooses defect/opportunity/gap/retain/none, and states whether a
detailed owner is loaded.

1. **Reliability.** Positive: a supported write returns success after a proven
   persistence failure is swallowed; the shared causal owner is not yet known.
   Admit a symptom-level Reliability defect without inventing a Root Cause and
   record the causal limit. Wrong: the same failure occurs only in an explicitly
   unsupported scenario; admit no defect.
2. **Domain.** Positive: repository instructions declare one executable
   acceptance schema authoritative; code emits a contradictory status spelling.
   Admit a Domain defect and honor the repository-declared authority. Wrong:
   `Customer` versus `User` is only an internal naming preference with no
   authority or meaning collision; admit no Domain item.
3. **Design.** Positive: caller-facing behavior tests must bypass the public
   Interface to exercise a supported variation owned behind it. Admit a Design
   observation/opportunity. Wrong: a focused unit test directly exercises a
   hidden algorithm but callers do not bypass the Interface; admit no Design
   item from that fact alone.
4. **Simplification.** Positive: reachable custom parsing duplicates an existing
   repository utility with the same contract and proof seam; admit a
   Simplification opportunity. Wrong: the custom path protects verified
   compatibility absent from every existing/native alternative; retain it.
5. **Coding Practice.** Positive: behavior is correct, but misleading names and
   duplicated conditions cause observed review and proof friction; admit a
   Coding Practice opportunity. Wrong: mutable local state has no invalid
   states, hidden transitions, caller burden, proof friction, or measured cost;
   admit nothing from immutability preference alone.
6. **Performance.** Positive: an authoritative production trace with provenance
   and comparable baseline proves a repository-owned resource budget breach,
   but cannot be rerun and has no sample-count statistics; admit a Performance
   defect without forcing an unsafe rerun or inapplicable statistics. Wrong: a
   suite is described as slow without a budget, comparable measurement, direct
   bottleneck, or required unavailable evidence; admit no Performance defect or
   opportunity.

Score one point for each correct positive and one for each correct closest wrong
condition (`12` total). Critical failures are inventing a Root Cause, rejecting
declared authority merely because it is executable, treating a focused hidden
algorithm test as caller bypass, deleting verified compatibility, admitting an
immutability preference, or calling unmeasured slowness a Performance defect.

## Decision Rule

Admit the candidate arm when any control sample scores below `12/12`. Accept the
candidate lens wording only when every candidate sample scores at least `11/12`,
no candidate has a critical failure, and no wrong-condition criterion regresses.
Otherwise use the behavioral decision vocabulary from `protocol.md`.
