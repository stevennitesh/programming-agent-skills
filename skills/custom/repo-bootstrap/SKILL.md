---
name: repo-bootstrap
description: "Use only when the current user explicitly asks to inspect, create, or reconcile one bounded repository's Programming Agent Skills setup; apply only an exact approved delta."
---

# Repo Bootstrap

Reconcile one repository's pack-facing setup without replacing repository-owned
choices or starting the workflow that requested setup.
Other skills read the installed `docs/agents/*` contracts directly. They may
recommend `$repo-bootstrap` and stop for a setup gap, but they never invoke or
load this package as runtime guidance.

## 1. Inspect

Resolve the repository root and record the current `HEAD`, index, worktree, and
the contents of any file that may change. Inspect existing setup pointers,
repository-owned commands, remotes, and only the setup branches relevant to the
request or an observed incompatibility.

When managed setup already exists, run
[scripts/validate_setup.py](scripts/validate_setup.py) as discovery. Compare an
applicable target with its current owner; a marker or validator result is
structural evidence, not proof that the setup works.

## 2. Reconcile

Preserve repository instructions, confirmed choices, local additions, staged
content, and unrelated work. Ask only about a consequential choice that the
repository does not settle.

- Load one tracker seed only when tracker setup applies:
  [GitHub](issue-tracker-github.md), [GitLab](issue-tracker-gitlab.md), or
  [Local Markdown](issue-tracker-local.md). Another tracker needs a concrete
  operation and read-back map.
- Load [triage-labels.md](triage-labels.md) only when an active selected workflow
  needs labels. Reuse or map existing labels before proposing creation.
- Load [domain.md](domain.md) only to choose or repair domain routing.
  `$domain-modeling` owns domain truth.
- Reconcile parallel support only when the user requested it or
  `$parallel-implement` returned that exact blocker. Follow its current lane
  configuration requirements; do not create worktrees or lane directories.

Prefer the detected tracker. Default domain routing to single-context unless
independent models or language require multiple contexts.

## 3. Propose

Show the exact local edits, external operations, preserved content, unresolved
conflicts, and nearest useful proof. With no delta, change nothing and continue
to Verify. Otherwise wait for the current user's approval of that exact delta.

## 4. Apply

Refresh every affected target before writing. If an affected target changed,
stop and propose again. Apply only the approved setup-owned edits and create
only approved missing labels.

Setup approval does not authorize domain truth, tracker items, worktrees,
dependency installation, staging, commits, pushes, or changes to `HEAD`.

Read back each external effect. If an operation fails or its result is unknown,
stop, inspect the affected state, and report what is known to have happened and
the safest next action. Do not retry blindly or assume rollback.

## 5. Verify

Run the validator and inspect the changed files and diff. Read back applicable
tracker configuration and labels. Run a repository command only when it can
disprove a claim made by the setup change. Confirm that unrelated work, the
index, and `HEAD` were preserved.

Complete when the applicable setup is compatible and every external change was
read back, or when the exact blocker and observed partial state have returned
to the user. Leave the recommending workflow unstarted.
