# Skill Context Relationships

Purpose: map context owners, pointers, and cross-skill relationships so skill edits do not duplicate setup docs or creep across workflow boundaries.

Scope: `skills/current/**` markdown files, their direct supporting files, `README.md`, and `AGENTS_SKILL_PACK_GUIDE.md`.

## Graph

```mermaid
flowchart TD
  Guide["README / AGENTS_SKILL_PACK_GUIDE<br/>suggestion map only"] --> AskMatt["ask-matt<br/>router skill"]

  AskMatt --> Setup["setup-matt-pocock-skills"]
  Setup --> AgentDocs["repo-local setup surface<br/>AGENTS.md + docs/agents/*"]
  AgentDocs --> Tracker["issue-tracker.md"]
  AgentDocs --> Labels["triage-labels.md"]
  AgentDocs --> DomainRouter["domain.md"]
  AgentDocs --> Contract["engineering-contract.md"]

  DomainRouter --> Context["CONTEXT.md / CONTEXT-MAP.md"]
  DomainRouter --> ADRs["docs/adr/"]
  DomainModel["domain-modeling"] --> Context
  DomainModel --> ADRs

  AskMatt --> Shape["grilling / grill-with-docs / decision-mapping / prototype"]
  AskMatt --> Handoff["handoff"]
  GrillDocs["grill-with-docs"] --> Grilling["grilling"]
  GrillDocs --> DomainModel
  Grilling -. "durable memory" .-> GrillDocs
  Decision["decision-mapping"] --> Grilling
  Decision --> DomainModel
  Decision --> Prototype["prototype"]
  Prototype --> Handoff["handoff"]
  Prototype --> DomainModel

  Shape --> ToPrd["to-prd"]
  ToPrd --> DomainRouter
  ToPrd --> TmpPrd[".tmp/to-prd/*.md"]
  ToPrd --> Tracker
  ToPrd --> Labels
  ToPrd --> ToIssues["to-issues"]
  ToIssues --> Tracker
  ToIssues --> Labels
  ToIssues --> Ready["ready-for-agent issues"]

  Triage["triage"] --> Tracker
  Triage --> Labels
  Triage --> DomainRouter
  Triage --> AgentBrief["AGENT-BRIEF.md"]
  Triage --> OutOfScope["OUT-OF-SCOPE.md / .out-of-scope/"]
  Triage --> Ready

  Ready --> Implement["implement"]
  Ready --> Parallel["parallel-implement"]
  Implement --> Contract
  Implement --> Review["review"]
  Implement --> Tracker
  Parallel --> Contract
  Parallel --> Tracker
  Parallel --> DomainRouter
  Parallel --> WorkerBrief["WORKER-BRIEF.md"]
  Parallel --> IntegratorBrief["INTEGRATOR-BRIEF.md"]
  Parallel --> Ledger["RUN-LEDGER.md / .tmp/parallel-implement/"]
  Parallel --> Review
  Parallel -. "approved high risk only" .-> CPR["convergent-pr-review"]
  WorkerBrief --> TDD
  IntegratorBrief --> Review
  IntegratorBrief -. "ledger-approved only" .-> CPR
  Review --> Tracker
  Review --> Contract
  Review -. "local PR / high risk" .-> CPR
  CPR --> Contract

  TDD["tdd"] --> Contract
  TDD --> DomainRouter
  Debug["diagnosing-bugs"] --> Contract
  Debug --> DomainRouter
  Debug -. "architecture cause" .-> Arch["improve-codebase-architecture"]
  Arch --> Contract
  Arch --> DomainRouter
  Arch --> CodeDesign["codebase-design"]
  Arch --> DomainModel
  Arch --> HtmlReport["HTML-REPORT.md / .tmp/architecture-reviews/"]
  Arch --> Implement
  Arch --> ToIssues
  Arch --> ToPrd

  TDD --> TddRefs["tests.md / mocking.md / refactoring.md"]
  TddRefs -. "uncertain repro" .-> Debug
  TddRefs -. "larger design follow-up" .-> CodeDesign
  TddRefs -. "larger design follow-up" .-> Arch
  CodeDesign --> DesignRefs["DEEPENING.md / DESIGN-IT-TWICE.md"]
  Writing["writing-great-skills"] --> Glossary["GLOSSARY.md"]
```

## Invocation Map

Source: `skills/current/*/agents/openai.yaml`.

| Skill | Invocation |
| --- | --- |
| `ask-matt` | explicit-only |
| `codebase-design` | implicitly invocable |
| `convergent-pr-review` | implicitly invocable |
| `decision-mapping` | explicit-only |
| `diagnosing-bugs` | implicitly invocable |
| `domain-modeling` | implicitly invocable |
| `grilling` | implicitly invocable |
| `grill-with-docs` | explicit-only |
| `handoff` | explicit-only |
| `implement` | explicit-only |
| `improve-codebase-architecture` | explicit-only |
| `parallel-implement` | explicit-only |
| `prototype` | explicit-only |
| `review` | implicitly invocable |
| `setup-matt-pocock-skills` | explicit-only |
| `tdd` | implicitly invocable |
| `to-issues` | explicit-only |
| `to-prd` | explicit-only |
| `triage` | explicit-only |
| `writing-great-skills` | implicitly invocable |

## Context Owners

| Owner | Owns | Read by / pointed to |
| --- | --- | --- |
| `README.md`, `AGENTS_SKILL_PACK_GUIDE.md` | Public and installed suggestion maps only | Humans, agents choosing a route |
| `setup-matt-pocock-skills` | Creates repo setup surface and seed docs | `ask-matt`, setup gates in planning/tracker skills |
| `docs/agents/issue-tracker.md` | Tracker operations and PR-as-request rules | `to-prd`, `to-issues`, `triage`, `implement`, `parallel-implement`, `review` |
| `docs/agents/triage-labels.md` | Category/state role to label mapping | `to-prd`, `to-issues`, `triage`, `implement`, `parallel-implement` |
| `docs/agents/domain.md` | Routing to `CONTEXT.md`, `CONTEXT-MAP.md`, ADRs | `to-prd`, `triage`, `tdd`, `diagnosing-bugs`, `improve-codebase-architecture`, `parallel-implement` |
| `docs/agents/engineering-contract.md` | Coding discipline, proof, `.tmp` cleanup, review/lock | `implement`, `tdd`, `diagnosing-bugs`, `improve-codebase-architecture`, `parallel-implement`, `review`, `convergent-pr-review` |
| `domain-modeling` | Mutates domain glossary and ADRs | `grill-with-docs`, `decision-mapping`, `prototype`, `triage`, `improve-codebase-architecture` |
| `review` | Ordinary fixed-point Standards/Spec review | `implement`, `parallel-implement`; escalates to `convergent-pr-review` for high risk |

## Supporting Files

| Skill | Supporting files own |
| --- | --- |
| `writing-great-skills` | `GLOSSARY.md`: skill-authoring vocabulary |
| `codebase-design` | `DEEPENING.md`: dependency/seam discipline; `DESIGN-IT-TWICE.md`: alternative interface exploration |
| `domain-modeling` | `CONTEXT-FORMAT.md`, `ADR-FORMAT.md`: durable language and ADR formats |
| `tdd` | `tests.md`, `mocking.md`, `refactoring.md`: examples and branch mechanics |
| `prototype` | `LOGIC.md`, `UI.md`: branch mechanics; `SKILL.md` owns lifecycle and boundary |
| `triage` | `AGENT-BRIEF.md`: ready-for-agent brief format; `OUT-OF-SCOPE.md`: rejected-work knowledge base |
| `setup-matt-pocock-skills` | Tracker, label, domain, and engineering-contract seed docs |
| `improve-codebase-architecture` | `HTML-REPORT.md`: report format and visual style |
| `parallel-implement` | `WORKER-BRIEF.md`, `INTEGRATOR-BRIEF.md`, `RUN-LEDGER.md`: lane contracts and run ledger |

## Boundary Notes

- Suggestion maps suggest; `ask-matt` routes; neither teaches workflow procedures.
- Setup docs own tracker, labels, domain routing, and engineering-contract details. Skills should point there instead of restating those mechanics.
- `domain-modeling` is the only skill that should write domain glossary/ADR truth; readers follow `docs/agents/domain.md`.
- `to-prd` owns parent PRD synthesis and tracker publication; `to-issues` owns implementation issue slicing.
- `triage` owns incoming issue/PR state transitions and ready-for-agent briefs; do not re-triage `$to-issues` output.
- `implement` owns one selected item; `parallel-implement` owns batch orchestration and serialized integration.
- `review` is the ordinary closeout gate; `convergent-pr-review` is an approved high-risk/local-PR route, not default review.
- `convergent-pr-review` may run its own read-only reviewer passes only when selected as the review route; it is not a second implementation orchestrator.
- `.tmp/` artifacts are disposable unless a skill explicitly preserves them as source, report, or ledger evidence.
