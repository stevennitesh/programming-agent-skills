# Upstream refresh, 2026-09-05

Read-only comparison of upstream instructions against this pack at
`9733d619d9d1104a1791b2e2392aeb1a3b189da1`. This is research intake, not adoption
authority or behavioral validation. Only the four local upstream clones were
updated; this note records the result. Historical research pins remain intact.

## Refreshed identities

All clones are under `.tmp/repos/`. Each started clean on `main`, was fetched
with `git fetch --prune origin`, and updated with
`git merge --ff-only origin/main`. All four passed final checks for a clean
checkout and `HEAD == origin/main` against the freshly fetched refs.

| Source / clone | Before refresh | Updated commit | New commits |
| --- | --- | --- | ---: |
| Matt Pocock / `mattpocock-skills` | `5b15a47f2d7150f545fbcacbfe381787fc0230dc` | `3cca18b368ae95cdbdebbff572ccafa662551015` | 5 |
| Pstack / `cursor-plugins` | `46125561306434d8a1d7745d540d8932ab0cd2a2` | `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | 60 repository-wide, 7 touching `pstack/` |
| Superpowers / `superpowers` | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | 0 |
| Ponytail / `ponytail` | `2ed6c52c9d7e5e56942508591085fd45dea277d3` | `974d940a1c5344210874150b98ff0d2c861fab6a` | 3 |

Pstack is a directory in Cursor's plugins repository. Its refresh changes 29
paths under `pstack/`; unrelated marketplace plugins are outside this assessment.
Feature branches fetched by Git are not included in the recommendations.

## Recorded research pins versus current clones

The vocabulary research records older snapshots, distinct from today's
pre-refresh clone commits:

| Source | Recorded research pin | Commits to updated main | Pin owner |
| --- | --- | ---: | --- |
| Matt Pocock | `ed37663cc5fbef691ddfecd080dff42f7e7e350d` | 145 | [Vocabulary research](language/matt-pocock-skills-vocabulary.md) |
| Superpowers | `d884ae04edebef577e82ff7c4e143debd0bbec99` | 53 | [Vocabulary research](language/superpowers-skill-pack-vocabulary.md) |
| Ponytail | `16f29800fd2681bdf24f3eb4ccffe38be3baec6b` | 7 | [Vocabulary research](language/ponytail-skill-pack-vocabulary.md) |

No exact durable Pstack research pin was found in the searched research
records. Its captured pre-refresh checkout is the comparison baseline here.
Do not mistake that checkout for an adopted-source pin. These historical
ranges were screened through history, release notes, and relevant source
files, not exhaustively re-audited or behaviorally tested.

## Useful changes and local correspondence

### Matt Pocock

Today's substantive addition is the experimental
[retro skill](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/retro/SKILL.md).
It reviews session evidence for navigation, automated checks, coding standards,
global instructions, tool economy, no-op instructions, and information access.
The last category asks whether missing logs or read-only service access
prevented good work.

Assessment: useful as a lens within existing context-hygiene work. Navigation,
enforcement, and pruning substantially overlap with
`skills/custom/context-hygiene/SKILL.md` and
`skills/custom/writing-for-agents/SKILL.md`. Information access and tool-call
cost are worth explicitly considering when session evidence identifies those
problems. A separate new skill is not yet justified. Do not import the claim
that reviewers need no exploration, or move all coding standards out of
implementation; our engineering contract deliberately guides construction.

The other fresh change excludes `misc/` from local skill linking and removes
stale links owned by that directory. Our installer already limits managed
installation to `skills/custom/`, so the principle is covered.

Since the older research pin, upstream also added the experimental
[implement-spec skill](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/in-progress/implement-spec/SKILL.md):
a dependency frontier, worktree implementers, a merger, then whole-PR review.
Our parallel-implement already covers that basic graph and supplies more
explicit custody, shared-resource, integration-proof, and cleanup rules.
No replacement is warranted from this source comparison.

### Pstack

The new
[plan validator](https://github.com/cursor/plugins/blob/93b00b89ef425a9c1bac0d0b317dfc49c930ac99/pstack/skills/poteto-mode/scripts/check-plan.mjs)
checks a prescribed plan structure, evidence labels, lane counts, and review
and performance blocks. Its accompanying playbook makes checked items depend
on named evidence. That traceability is useful when a long-running plan
actually needs it. However, this implementation checks document shape and
strings, not whether the evidence exists or proves success. It mandates ten
live lanes, a specific model, screenshots, and performance checks per PR.
Do not import those requirements into ordinary work or treat validator success
as behavioral proof.

The
[TypeScript guidance](https://github.com/cursor/plugins/blob/93b00b89ef425a9c1bac0d0b317dfc49c930ac99/pstack/skills/typescript-best-practices/references/patterns.md)
now favors existing runtime schemas over hand-written guards and derives types
from schemas. It explicitly avoids adding a dependency for one guard. Our
engineering contract already says to derive boundary types from authoritative
schemas using existing tooling and validate at the owning boundary. Good
reinforcement, little new policy needed.

The revised
[shipping playbook](https://github.com/cursor/plugins/blob/93b00b89ef425a9c1bac0d0b317dfc49c930ac99/pstack/skills/poteto-mode/playbooks/shipping.md)
removes mandatory Graphite usage, resolves the forge, lands the bottom PR, and
rechecks state after each merge. This is relevant if we add stacked-PR delivery.
Its patch-ID reuse rule needs care: an unchanged patch does not prove unchanged
behavior when its base, dependencies, or callers move. Preserve our existing
proof-invalidation rules instead of using patch identity alone.

Other changes include explicit-only invocation metadata for five skills,
model-default changes, branding, and a Grok Bot webhook UI skill. These are
primarily host-specific. Do not copy their metadata or model identifiers into
Codex without checking the current runtime's contract.

### Superpowers

No new main-branch changes today. Compared with our older research pin,
[v6.2 and v6.3](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/RELEASE-NOTES.md)
add plan-scoped scratch state, resume-the-implementer fix rounds, batching of
small similar tasks, proportionate brainstorming, safer worktree cleanup,
and less redundant prose. These were already present in the local clone.

The current
[test-writing reference](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/test-driven-development/writing-good-tests.md)
gives useful examples of independently derived expectations and tests that
catch behavior breaks rather than merely detect edited constants or strings.
Our engineering contract and TDD skill already express the main discipline.
Use the examples as reference if a concrete test-quality gap appears.

The release notes report behavioral regressions from one attempted prose cut.
Those are upstream-reported results, not reproduced evidence about this pack
or Astra. They support testing candidate deletions rather than assuming every
shorter instruction performs equally well.

### Ponytail

Today's three commits only add Trendshift badges to README translations.
Compared with the older research pin, the additional changes concern Grok Build
packaging, Copilot host detection, and hook compatibility. The
[core skill](https://github.com/DietrichGebert/ponytail/blob/974d940a1c5344210874150b98ff0d2c861fab6a/skills/ponytail/SKILL.md)
has no diff from `16f2980`. There is no new general engineering guidance to
adopt from this update.

## Recommendation and limits

Prioritize the retrospective's information-access and tool-economy questions
when observed failures warrant them. Retain the plan-to-evidence connection as
an optional idea for long-running work. Most other useful upstream principles
already have local owners. Avoid importing another coordinator, universal
verification ceremony, or host-specific adapters without a concrete need.

This assessment establishes source changes and static correspondence only.
It does not establish improvements in quality, cost, or completion time.
No active skill, installed skill, historical pin, or Git delivery was changed.
