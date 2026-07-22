---
name: repo-bootstrap
description: "Bootstrap or reconcile a target repo's verified setup surface for the Programming Agent Skills pack."
---

# Repo Bootstrap

Own one outcome: a compatible, verified repo-local **setup surface**.

**Inventory. Reconcile. Choose. Draft. Provision. Verify.**

## Inventory

Inspect before asking. Read repository identity and tracker access; `AGENTS.md` and configured fallback instructions; repo-owned command sources; existing `docs/agents/`, context files, and ADRs; `.gitignore`, `.tmp/`, `.scratch/`; and hosted-tracker labels when accessible. Inspect workspace and package manifests, independently owned source roots, existing domain vocabularies, and ADR streams.

Treat a command as verified only when repo config, CI, or maintained documentation owns it. Surface conflicting sources.

Inventory completes when the tracker candidate, verified commands, existing setup surface, domain layout, local-state policy, settled choices, and access blockers are known.

## Reconcile

When a prior setup surface exists, treat this run as a **reconcile**, not a reset.

[setup-schema.json](setup-schema.json) owns the current fingerprint. A missing `programming-agent-skills setup-schema` marker identifies a legacy setup; a different fingerprint identifies an outdated setup.

- **Preserve.** Carry forward the confirmed tracker, label mapping, domain layout, PR/MR intake policy, close policy, verified commands, repo invariants, and repo-specific contract additions.
- **Delta.** Propose only changes required by the current pack.
- **Re-ask.** Revisit a choice only when missing, ambiguous, incompatible, explicitly reopened, or contradicted by current evidence.
- **Conflict.** Surface incompatible repo policy and wait for the user's decision.

## Choose

Resolve only unsettled choices, one answer at a time. Lead with the discovered recommendation and its consequence.

- **Tracker.** Choose [GitHub](issue-tracker-github.md), [GitLab](issue-tracker-gitlab.md), [Local Markdown](issue-tracker-local.md), or another tracker with an explicit operation map. Prefer the detected remote; otherwise recommend Local Markdown. For hosted trackers, settle external PR/MR intake and implemented-item closure. GitHub default: yes for closure. GitLab default: no. Intake defaults to no.
- **Labels.** Use [triage-labels.md](triage-labels.md) as the role set. Reuse matching labels, map local names, and propose only missing labels for creation after approval.
- **Domain.** Default to single-context (`CONTEXT.md`, `docs/adr/`). Propose multi-context (`CONTEXT-MAP.md` plus routed context docs and ADRs) only when independently owned domain vocabularies, decisions, or responsibilities span source roots. Workspace manifests trigger inspection but do not prove multiple contexts. `$domain-modeling` owns later domain-file creation and changes.

Verified commands, the four local contracts, and `.tmp/`/`.scratch/` policy are setup invariants, not extra choices.

## Draft

Show the exact proposed delta:

- the `AGENTS.md` patch with the engineering primer, verified commands, invariants, pointers, and `<!-- programming-agent-skills setup-schema: 1:04d85ba5be57 -->`;
- all four `docs/agents/*.md` results;
- the `.gitignore` delta;
- preserved repo-specific additions and unresolved conflicts;
- tracker labels and policies;
- access blockers and the verification plan.

Wait for approval before any file write or tracker mutation.

## Provision

Apply only the approved delta. Reconcile existing local contracts in place. Preserve repo-specific additions.

- **Primer.** Update or create a short `AGENTS.md` with `Explore imaginatively. Converge under proof. Simplify ruthlessly.`, verified commands, local invariants, the current marker, and pointers to the four local contracts. When the portable engineering-contract owner is present, replace its portable title and owner preamble with the installed-pack primer and engineering-contract pointer; preserve repo-specific material.
- **Contracts.** Reconcile the selected tracker template into `docs/agents/issue-tracker.md`; [triage-labels.md](triage-labels.md) into `docs/agents/triage-labels.md`; [domain.md](domain.md), with its layout resolved, into `docs/agents/domain.md`; and [engineering-contract.md](engineering-contract.md) into `docs/agents/engineering-contract.md`. For another tracker, use the approved operation map.
- **State.** Keep `.tmp/` contents ignored and `.scratch/` trackable without replacing unrelated ignore rules.
- **Labels.** For GitHub or GitLab, create only approved missing mapped and fixed labels; preserve existing labels and descriptions.

Treat dependency installation or broad environment mutation as a separate user-approved action.

## Verify

Run [scripts/validate_setup.py](scripts/validate_setup.py) against the target repo. Then smoke-test tracker read access, verify hosted labels, run the cheapest repo-owned command proving the recorded command surface, run `git diff --check`, and read back every changed file and tracker mutation. Report skipped checks.

Setup completes only when the validator passes and tracker access, labels or local status vocabulary, verified commands, preserved additions, and approved mutations are confirmed. Otherwise report **Setup incomplete**, the blocker, and the exact next action.
