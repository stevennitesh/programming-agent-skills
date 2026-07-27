# Research Promotion And Installation

Status: `complete`

Authority: 2026-07-23 Deploy Campaign, Deploy Prompt 5. This record owns
canonical promotion, experimental cleanup, and managed installation evidence.
It does not stage, commit, push, or begin another skill.

## Drift And Accepted Identity

- Git fixed point:
  `4359f7afeeec29a9c8692b18c1586afb041f9bf4`
- accepted Prompt 4 record:
  `docs/validation/transcripts/2026-07-23-research-behavior-eval.md`
- completed Pruning Pass:
  `docs/validation/transcripts/2026-07-23-research-pruning.md`
- frozen B0, behavior-complete C1, and final C1 tree:
  `0961494db521e812540fb36052a1efdd60f22958d1e6e0ba40115ec47da9334f`
- pre-promotion canonical tree:
  `ae255d2b12e88bfa8882c7c5c00116b0267df3fa88345b75819bf95112c477b2`
- package inventory: `SKILL.md`, `agents/openai.yaml`
- accepted byte, task, claim, and evidence-contract drift: none
- campaign shape: `pruning-only`

The live inactive candidate and frozen B0 were byte-identical before
promotion. Prompt 4 evidence remained exact-reusable because final bytes,
fixed tasks, claims, worker class, runtime, tools, authority, evidence, and
rubrics were unchanged.

## Canonical Promotion

`writing-great-skills` ran in Author mode. The exact accepted candidate replaced
only `skills/custom/research/SKILL.md`; the invocation policy was already
byte-identical. The final canonical package hash is:

`0961494db521e812540fb36052a1efdd60f22958d1e6e0ba40115ec47da9334f`

Directly affected canonical proof was updated in
`tests/test_skill_pack_contracts.py` to protect semantic machine contracts:
narrow implicit invocation, the four canonical sections, claim and terminal
status vocabularies, one-note versus no-write containment, Verify-before-Return
order, caller custody, no downstream start, and the rejected Research Scout
surface. The test does not freeze incidental prose or line numbers.

Relationship delta remained none. Skill Router, Grilling, and To Questionnaire
still recommend and stop; Wayfinder and Improve Codebase still invoke one
bounded Research unit and retain caller state and transition authority.

Canonical proof before lifecycle cleanup:

- exact canonical-to-C1 byte comparison: identical;
- focused Research contracts and relationship trace: `3 passed`;
- `python -m scripts.pytest_focused`: `59 passed`;
- `python -m scripts.validate_skills`: passed;
- `git diff --check`: passed; and
- `git diff --cached --check`: passed.

## Synthesis And Lifecycle Reconciliation

`docs/synthesis/skills/research.md` now records the promoted canonical identity,
six-unit runtime, unchanged relationships, Compact Scout
`rejected-no-control-failure`, `pruning-not-needed`, proof pointers, deliberate
non-changes, and residual evidence limits. Superseded future-tense construction
instructions, duplicated active designs, and raw campaign chronology were
removed. Concise decision-changing history remains.

Only `skills/experimental/research/` and its manifest entry were removed.
Every other experimental candidate and manifest entry was preserved.
`docs/validation/evals/research-b0/` and all campaign transcripts remain as
evidence.

## Managed Installation

The supported pre-install dry-run reported:

```text
Managed skills: 25 in C:\Users\steve\.agents\skills
Updated skills: research
Unchanged skills: 24
Global bootstrap: present
```

The changed cohort was exactly the authorized skill. The first supported sync
was sandbox-blocked at the managed install lock. The same supported installer
was retried with the required scoped approval and completed:

```text
Installed 25 custom skills into C:\Users\steve\.agents\skills
Global bootstrap: present
```

Canonical and installed Research tree hashes both equal:

`0961494db521e812540fb36052a1efdd60f22958d1e6e0ba40115ec47da9334f`

The post-install dry-run reported all 25 managed skills unchanged. Installed-
aware `scripts.validate_skills` passed. The installed mirror was never edited
directly.

## Final Validation

- canonical tree:
  `0961494db521e812540fb36052a1efdd60f22958d1e6e0ba40115ec47da9334f`
- installed tree:
  `0961494db521e812540fb36052a1efdd60f22958d1e6e0ba40115ec47da9334f`
- canonical-to-installed parity: exact
- experimental Research directory: absent
- experimental Research manifest entry: absent
- post-install dry-run: clean
- full `python -m pytest`: `204 passed, 4 skipped`
- affected Markdown gate: passed for canonical Research, reconciled synthesis,
  and this lifecycle record
- final `python -m scripts.validate_skills`: passed
- both final diff checks: passed

## Deliberate Non-Changes And Residuals

No caller, relationship index, invocation policy, other skill, other
experimental candidate, frozen B0, historical evaluation, or installed file
was independently changed. `tests/test_deploy_prompt_contracts.py` and unrelated
dirty work were preserved.

Residual evidence limits remain live network/provider behavior, actual host
note create/update and reread, elapsed/token/backend telemetry, host automatic
invocation instrumentation, and generalization beyond the fixed packets,
worker class, and recorded runtime. No unavailable telemetry was inferred.

Authorized unit completed: Deploy Prompt 5 for `research`
Decision: complete
Campaign shape: pruning-only
Runtime decision: exact source-derived minimum promoted; Compact Scout rejected-no-control-failure; pruning-not-needed
Artifacts changed: canonical Research package, directly affected Research contract assertions, reconciled Research synthesis, Research promotion/install record, experimental Research directory and manifest entry
Evidence used or reused: exact Prompt 4 fixed-packet evidence, completed Pruning Pass, exact hashes and byte comparison, focused canonical proof, relationship trace, managed install dry-runs, sync receipt, canonical-installed parity
Residual gaps: live network/provider and host note behavior; elapsed, token, backend, and host invocation telemetry; generalization beyond fixed packets/runtime
Recommended next unit: none
Git HEAD: 4359f7afeeec29a9c8692b18c1586afb041f9bf4 -> 4359f7afeeec29a9c8692b18c1586afb041f9bf4
Git delivery: pending
Exact stop reason: Deploy Prompt 5 promoted and installed only Research; canonical, lifecycle, full-suite, Markdown, parity, and diff proof passed, so the campaign stops before Git delivery
