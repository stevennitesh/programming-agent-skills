---
name: repo-bootstrap
description: "Bootstrap or reconcile a target repo for this engineering skill pack: verified commands, tracker lifecycle, label roles, domain routing, engineering contract, and work-state policy."
---

# Repo Bootstrap

Bootstrap or reconcile the repo-local **setup surface** the custom skill pack reads.

A repo is **ready** only when its agent primer points to verified commands and complete local contracts, its chosen tracker is usable, required labels exist, disposable work stays in ignored `.tmp/`, and durable local state stays trackable in `.scratch/`.

**Inventory, Reconcile, Choose, Draft, Provision, Verify.**

## 1. Inventory

Inspect before asking:

- `git remote -v` and `.git/config`: tracker host and repository identity.
- `AGENTS.md` plus configured Codex fallback instruction files: setup-schema marker, existing commands, invariants, pointers, prior setup output, or the portable fallback heading `Portable Engineering Contract`.
- `README`, contribution docs, manifests, lockfiles, task runners, and CI: canonical setup, focused-test, full-test, lint/format, typecheck, and build commands.
- `docs/agents/`, `CONTEXT.md`, `CONTEXT-MAP.md`, root and context-local ADR directories.
- `.gitignore`, `.tmp/`, and `.scratch/`: disposable and tracked-local-state policy, plus any existing local tracker.
- For a detected GitHub or GitLab remote, read tracker access and label inventory when credentials permit.

Treat a command as verified only when repo config, CI, or maintained docs own it. Surface conflicting command sources.

Inventory is complete when the tracker candidate, instruction target, verified command set, existing setup surface, domain layout, local-state policy, and access blockers are known.

## Reconcile Existing Setup

When a prior setup surface exists, treat this run as a **reconcile**, not a reset.

[setup-schema.json](setup-schema.json) defines the current contract fingerprint. A missing `programming-agent-skills setup-schema` marker identifies a legacy setup; a different fingerprint identifies an outdated setup. Compare its capabilities with the current contract; preserve compatible local choices and propose only the missing delta.

- **Preserve:** confirmed tracker, label mappings, domain layout, PR/MR request policy, close policy, verified commands, repo invariants, and repo-specific contract additions.
- **Delta:** propose only changes required by the current pack.
- **Re-ask:** revisit a choice only when it is missing, ambiguous, incompatible, or explicitly reopened by the user.
- **Conflict:** surface current-pack requirements that conflict with preserved repo policy and wait for the user to resolve them.

## 2. Choose

Resolve these three decisions **one at a time**. Carry forward every reconciled choice. For each unresolved decision, explain the consequence, recommend the discovered default, and wait for the answer.

### A. Tracker

Choose where specs and work items live:

- **GitHub**: GitHub Issues through the GitHub connector; use `gh` only when the connector lacks the required operation.
- **GitLab**: GitLab Issues through `glab`.
- **Local Markdown**: durable, version-controlled files under `.scratch/<feature>/`.
- **Other**: capture the exact create, read, list, comment, label/state, parent-child, dependency, claim, closeout, and close operations.

Prefer the detected remote. Otherwise recommend Local Markdown.

For GitHub or GitLab, ask:

- **External PRs/MRs as a triage surface?** Default: no.
- **Close implemented work items after closeout?** GitHub default: yes, so dependency and sub-issue progress match the ready frontier. GitLab default: no. The `implemented` state preserves searchable outcome history either way.

### B. Labels

Map two category roles and six state roles:

- Categories: `bug`, `enhancement`
- States: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `implemented`, `wontfix`

Also reserve `$wayfinder` labels: `wayfinder:map`, `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, and `wayfinder:task`.

Reuse matching tracker labels. Propose the role names as defaults and list only missing labels for creation after approval. Record HITL/AFK participation in ticket bodies, not labels. Local Markdown uses the mapped values directly.

### C. Domain Layout

Choose:

- **Single-context**: root `CONTEXT.md` and `docs/adr/`.
- **Multi-context**: root `CONTEXT-MAP.md` routing to context glossaries and ADRs.

Record the choice in `docs/agents/domain.md`. Domain files remain lazy: `$domain-modeling` creates or changes them when language or decisions resolve.

Then explain the fixed setup outputs: verified commands in `AGENTS.md`, the engineering contract, tracker and label contracts, domain routing, and `.tmp/`/`.scratch/` policy. These are pack invariants, not extra choices; surface any repo-policy conflict.

## 3. Draft

Show the exact proposed setup before writing:

- the `AGENTS.md` patch, including the current setup-schema marker, verified commands, local invariants, and setup pointers;
- all four `docs/agents/*.md` files;
- the `.gitignore` delta;
- preserved choices and repo-specific additions, plus any conflict that requires a decision;
- tracker labels to reuse or create;
- tracker access blockers and the verification plan.

Wait for approval before file writes or tracker mutations.

## 4. Provision

### Agent Primer

Always update or create `AGENTS.md`; custom planning skills use it as the boot surface.

Keep it short:

- `## Commands`: verified repo-owned setup and validation commands, with config pointers when useful.
- compact non-negotiable local invariants.
- this installed-pack block:

```markdown
## Agent skills

<!-- programming-agent-skills setup-schema: 1:859a503ba864 -->

This repo uses the Programming Agent Skills engineering pack.

AGENTS primes. Repo-local docs teach. Skills execute.

Before nontrivial coding, read `docs/agents/engineering-contract.md`.

### Pointers

- Issue tracker operations: `docs/agents/issue-tracker.md`
- Triage label roles: `docs/agents/triage-labels.md`
- Domain docs and ADR routing: `docs/agents/domain.md`
- Engineering contract: `docs/agents/engineering-contract.md`
```

Update existing sections in place and preserve repo-specific commands, architecture, release rules, and source-of-truth routing.

When `AGENTS.md` contains the portable fallback contract, replace its portable title and owner preamble plus its generic `North Star`, `Working Loop`, `Hard Gates`, `Shape Before Build`, `Implementation Taste`, and `Review And Report` sections with the installed-pack block and engineering-contract pointer. Keep repo-specific material. Keep other agent instruction files unchanged unless Codex configuration or the user makes them part of this setup.

### Local Contracts

Reconcile existing local contracts in place. Preserve repo-specific additions. Surface any incompatibility with current requirements in Draft and carry it as an explicit user decision.

Write:

- [issue-tracker-github.md](issue-tracker-github.md), [issue-tracker-gitlab.md](issue-tracker-gitlab.md), or [issue-tracker-local.md](issue-tracker-local.md) to `docs/agents/issue-tracker.md`;
- [triage-labels.md](triage-labels.md) to `docs/agents/triage-labels.md`;
- [domain.md](domain.md) to `docs/agents/domain.md`, replacing its layout placeholder;
- [engineering-contract.md](engineering-contract.md) to `docs/agents/engineering-contract.md`.

The tracker contract must define:

- tracker interface and PR/MR request-surface policy;
- packet storage, the shared ready-for-agent contract, parent-child links, blocking edges, ready query, claim/release, mutation read-back, closeout state, and close policy;
- Codex-ready brief transport;
- `$wayfinder` map/ticket transport, participation, frontier, outcomes, and map completion.

For another tracker, write the same contract from the user's operation map.

### Disposable And Tracked Local State

Require `.tmp/` contents to be ignored without replacing unrelated ignore rules.

Keep `.scratch/` trackable without replacing unrelated ignore rules. It is durable, version-controlled local work state; Local Markdown tracker files live there when selected.

For GitHub or GitLab, create only missing mapped and fixed labels after approval. Preserve existing labels and descriptions.

## 5. Verify

Run `scripts/validate_setup.py` from this skill against the target repo. Then:

- smoke-test read access through the configured tracker interface;
- verify every connector-backed label exists;
- run the cheapest practical repo-owned command that proves the recorded command surface is usable;
- run `git diff --check`;
- read back every changed file and report skipped checks.

Treat dependency installation or broad environment mutation as a separate user-approved action.

Setup is complete only when `AGENTS.md` carries the current setup-schema marker; all four local contracts, tracker access, labels or local status vocabulary, domain layout, command pointers, any preserved repo-specific additions, and local-state policy are verified. Otherwise report **Setup incomplete**, the blocker, and the exact next action.
