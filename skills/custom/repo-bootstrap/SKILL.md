---
name: repo-bootstrap
description: "Use only when the current user explicitly asks to inventory or reconcile one bounded repository's Programming Agent Skills setup surface; provision only an explicitly approved exact delta."
---

# Repo Bootstrap

Own a compatible, verified repo-local **setup surface**.

Run only when the current user names it for one bounded repository. Another
skill may recommend it and stop; that grants no execution,
mutation, resumption, or completion authority. Inventory through Draft is
read-only. Provision may apply only the exact displayed, approved delta.

## Inventory

Resolve the repository root, authority, and starting working-tree, index, and
`HEAD`. Without mutation authority, a non-empty delta remains proposal-only.

Inspect before asking: `AGENTS.md`, the four `docs/agents/` contracts,
`.gitignore`, `.tmp/`, `.scratch/`, repo-owned command sources, tracker
configuration and read-back capability, labels, and applicable context, ADR,
manifest, ownership, and domain-layout evidence.

When any managed file or setup marker exists, run
[scripts/validate_setup.py](scripts/validate_setup.py) read-only, then compare
every managed surface directly with its owner. The aggregate
[setup-schema.json](setup-schema.json) identity is structural evidence, not a
pack version, semantic proof, or persisted-state proof.

Treat commands as verified only when owned by repository configuration, CI, or
maintained documentation. Report conflicting evidence.

## Reconcile

Classify each surface as `compatible`, `delta`, `conflict`, or
`not applicable`. Preserve confirmed choices, verified commands, repository
invariants, additions, relationship modes, and unrelated work. Revisit only
missing, ambiguous, incompatible, reopened, or contradicted choices. Repository
policy remains authoritative; a `conflict` blocks only its affected delta until
the user resolves it.

## Choose

Ask one unsettled choice at a time with its recommendation and consequence.

- **Tracker.** Load exactly one selected guide:
  [GitHub](issue-tracker-github.md), [GitLab](issue-tracker-gitlab.md), or
  [Local Markdown](issue-tracker-local.md). Another tracker requires an
  approved operation and read-back map. Prefer the detected remote; otherwise
  Local Markdown. External PR/MR intake defaults to no; implemented-item
  closure defaults to yes for GitHub and no for GitLab. A GitHub relationship
  mode requires authenticated operation and independent read-back; prefer
  native, then portable, or return the blocker.
- **Labels.** Use [triage-labels.md](triage-labels.md); reuse or map existing
  labels and propose only missing labels.
- **Domain.** Default to single-context (`CONTEXT.md`, `docs/adr/`). Choose
  multi-context only when independent models, language, responsibilities, or
  consistency boundaries need `CONTEXT-MAP.md` routing. Structure is evidence,
  not proof. `$domain-modeling` owns domain truth.

## Draft

Show the exact local and external delta, policies and relationship modes,
preserved additions, conflicts or blockers, and proof plan. The `AGENTS.md`
result includes:

`<!-- programming-agent-skills setup-schema: 1:8113e40631ff -->`

With zero delta, mutate nothing and continue to Verify. Otherwise wait for
approval. Narrowing requires a new exact proposal; refusal or deferral returns
**Proposal only** with the unapplied delta and unchanged-state evidence.

## Provision

After approval, refresh the working-tree, index, and `HEAD`. Before each effect,
reread its target and revalidate authority, capability, approved parameters,
and preconditions. Stop on a load-bearing change; never recompute a delta under
old approval.

Apply only the approved delta:

- create or reconcile a short `AGENTS.md` with `Explore imaginatively.
  Converge under proof. Simplify ruthlessly.`, verified commands, invariants,
  the marker, and four contract pointers; replace any portable contract owner
  preamble with this primer;
- create or reconcile the selected tracker guide,
  [triage-labels.md](triage-labels.md), resolved [domain.md](domain.md), and
  [engineering-contract.md](engineering-contract.md) into `docs/agents/`;
- keep `.tmp/` ignored and `.scratch/` trackable without replacing unrelated
  ignore rules;
- create only approved missing GitHub or GitLab labels.

Do not alter domain truth, tracker items, the index, or `HEAD`; stage, commit,
push, install dependencies, or broadly mutate the environment. Those remain
separately authorized owner work.

Read back every effect before dependent effects. On failure or indeterminate
state, stop mutation, reread affected targets, and classify every approved
effect as `applied`, `failed`, `unknown`, or `not attempted`. Never retry
without new proof or assume rollback.

## Verify

Run the validator and compare every managed surface with its tracker, label,
domain, or engineering-contract owner. Verify tracker and relationship
read-back, labels or local status vocabulary, the cheapest safe repo-owned
command, `git diff --check`, and preservation of unrelated work, index, and
`HEAD`.

Separate source-verified commands from commands executed now. Name each skipped
check and its unproved claim; any required skip returns **Setup incomplete**.

Complete only with a verified zero delta or verified approved delta. Return
changed, unchanged, and preserved surfaces; proof, skipped checks, and residual
gaps. Otherwise return **Setup incomplete** with the blocker, every approved
effect's classification, and the safest next action. The recommending workflow
remains unstarted.
