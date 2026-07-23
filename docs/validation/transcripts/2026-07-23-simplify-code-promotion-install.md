# Simplify Code Prompt 5 Promotion And Installation

Status: `complete`

Authority: 2026-07-23 Deploy Campaign, Deploy Prompt 5. Canonical promotion
used `writing-great-skills` in Author mode; experimental retirement and managed
installation used Prompt 5's separate lifecycle authority. This record does
not authorize or perform Prompt 6, staging, commit, or push.

## Preconditions And Identity

- starting Git HEAD:
  `4359f7afeeec29a9c8692b18c1586afb041f9bf4`;
- campaign shape: `behavioral-candidate`;
- Prompt 4 record:
  [2026-07-23-simplify-code-behavior-eval.md](2026-07-23-simplify-code-behavior-eval.md),
  status `accepted`;
- Pruning Pass record:
  [2026-07-23-simplify-code-pruning.md](2026-07-23-simplify-code-pruning.md),
  status `complete`, disposition `pruning-not-needed`;
- accepted and pruning-complete C1 tree SHA-256:
  `f3fa29e016e1ad88f77088e7b001f80db4a139b51d7da2125146fdda5c8cef06`;
- exact package inventory: `SKILL.md`, `agents/openai.yaml`;
- manifest candidate identity before retirement: exact C1 hash above;
- relationship delta: none.

The candidate package, manifest entry, Prompt 4 record, pruning record,
synthesis claims, and Git HEAD were read back before promotion. Their exact
identities and decisions agreed. Behavior-complete bytes and claims had not
drifted.

## Canonical Promotion

The exact accepted C1 package was promoted to
`skills/custom/simplify-code`. Complete package read-back established:

| Surface | SHA-256 |
| --- | --- |
| Canonical tree | `f3fa29e016e1ad88f77088e7b001f80db4a139b51d7da2125146fdda5c8cef06` |
| `SKILL.md` | `97c2ab427bd71154c1f04bc72a1ba3e632c72406be52a88c633af86a3d2e68c4` |
| `agents/openai.yaml` | `8ef184a5a1fdf5bb4b325c1e9ec5019bb2ad5536aa583d806c2bc6e1cc3c2a14` |

Both canonical files were byte-identical to the accepted candidate before
experimental retirement. The canonical inventory remained exactly two files.
The provider interface and explicit-only policy remained unchanged.

The active synthesis was reconciled to the promoted runtime. It preserves the
source-first checkpoint, viability floor, admitted and rejected C1 decisions,
proof pointers, ownership, deliberate non-changes, and residual limits while
removing superseded future construction and inactive-candidate state.
Relationship read-back found no directly affected mismatch, so
`docs/synthesis/skill-context-relationships.md` was deliberately unchanged.

Accepted Prompt 4 behavior evidence was reused because the package bytes,
tasks, claims, protocol, runtime class, rubric, and proof lane were unchanged.
No behavior wave was rerun solely for lifecycle.

## Canonical And Integration Proof

- exact canonical-to-candidate tree and file parity before retirement: passed;
- complete canonical package read-back: passed;
- focused canonical Simplify Code contract:
  `python -m pytest tests/test_skill_pack_contracts.py -q -k simplify_code`:
  `2 passed`;
- affected integrated contract:
  `python -m pytest tests/test_skill_pack_contracts.py tests/test_experimental_skill_contracts.py -q`:
  `69 passed`;
- one full suite after final integration: `python -m pytest`:
  `204 passed, 4 skipped`;
- skill-pack validation: `python -m scripts.validate_skills`: passed;
- affected Markdown links, anchors, fences, and table columns: passed;
- `git diff --check`: passed;
- `git diff --cached --check`: passed.

The directly affected canonical assertions in
`tests/test_skill_pack_contracts.py` now protect the promoted wording and
machine behavior. No experimental assertion required a Simplify Code-specific
change.

## Experimental Retirement And Managed Installation

Only `skills/experimental/simplify-code` and the `simplify-code` entry in
`skills/experimental/manifest.json` were retired. Every other experimental
candidate and manifest entry was preserved.

The pre-install dry-run reported:

```text
Managed skills: 25 in C:\Users\steve\.agents\skills
Updated skills: simplify-code
Unchanged skills: 24
Global bootstrap: present
```

The proposed changed cohort exactly matched the authorized scope. The first
supported sync attempt was denied at the managed install lock by the sandbox;
the same repository-owned command was then run through the required approved
escalation path and completed:

```text
Installed 25 custom skills into C:\Users\steve\.agents\skills
Global bootstrap: present
```

Installed parity:

| Surface | Result |
| --- | --- |
| Installed package | `C:\Users\steve\.agents\skills\simplify-code` |
| Inventory | `SKILL.md`, `agents/openai.yaml` |
| Installed tree SHA-256 | `f3fa29e016e1ad88f77088e7b001f80db4a139b51d7da2125146fdda5c8cef06` |
| Canonical-to-installed `SKILL.md` bytes | identical |
| Canonical-to-installed `agents/openai.yaml` bytes | identical |

The post-install dry-run reported all 25 managed skills unchanged. The
installed mirror was never edited directly and is not canonical.

After that clean observation, a concurrent authorized campaign promoted
`to-questionnaire` in the shared worktree. A later global dry-run therefore
reported only `to-questionnaire` as updated. Prompt 5 did not synchronize that
foreign cohort. Simplify Code canonical-to-installed parity was rechecked
after the concurrent edit and remained exact at the tree hash above.

## Deliberate Non-Changes And Residual Limits

- No relationship delta was introduced.
- No Prompt 4 behavioral wave was repeated.
- No research, evaluation packet, unrelated synthesis, other candidate,
  tracker, external system, staged state, commit, branch, or push was changed.
- Prompt 4 residuals remain: no live synthetic-repository mutation or real
  concurrent interleaving proof; no generalization beyond the fixed packets
  and worker runtime; no upstream remote freshness claim; and no unavailable
  backend model, reasoning, token, latency, or host invocation telemetry.
- Git delivery remains pending in bare mode and belongs only to an explicitly
  authorized Prompt 6.

Authorized unit completed: Deploy Prompt 5 for `simplify-code`
Decision: complete
Campaign shape: behavioral-candidate
Runtime decision: promote exact pruning-complete C1 and install it with canonical-to-managed parity
Artifacts changed: canonical simplify-code package, current synthesis, directly affected canonical contract assertions, simplify-code experimental package and manifest entry retirement, promotion/install transcript, and supported managed mirror sync
Evidence used or reused: exact Prompt 4 acceptance and Pruning Pass records, exact candidate/manifest/canonical/installed identities, unchanged behavior claims and protocol, complete read-backs, affected Markdown gate, focused and full repository tests, skill validation, install dry-run/sync/parity/clean dry-run, and both diff checks
Residual gaps: live mutation and concurrent interleaving; backend model, reasoning, token, latency, and host invocation telemetry; generalization beyond fixed packets/runtime; upstream remote freshness; Git delivery
Recommended next unit: none
Git HEAD: 4359f7afeeec29a9c8692b18c1586afb041f9bf4 -> 4359f7afeeec29a9c8692b18c1586afb041f9bf4
Git delivery: pending
Exact stop reason: exact C1 is canonical and installed with clean parity, and bare Prompt 5 stops before Git delivery
