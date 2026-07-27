# To Tickets Deploy Prompt 5 Promotion And Installation

Date: 2026-07-23

Resume date: 2026-07-24

Decision: **`complete`**

This record owns only Deploy Prompt 5 for the 2026-07-23 To Tickets campaign.
It records exact P1 promotion, canonical proof, experimental-lifecycle
removal, the explicit two-skill install-scope expansion, and supported managed
installation. It does not rerun behavior, change relationships, hand-edit an
installed mirror, stage, commit, push, or start another skill.

## Authority And Preconditions

- Authority: Writing Great Skills, Author mode for canonical promotion,
  followed by the separately owned managed-install phase.
- Starting Git `HEAD`:
  `dd3cfa647190e94e40b1e213d8b8cf7e1762a3c6`.
- Prompt 4 decision: `accepted`.
- Pruning decision: `complete`; `pruning-not-needed`.
- Resume decision: the user explicitly authorized the exact managed-install
  cohort `to-tickets` plus `writing-great-skills`; no other managed skill.
- Relationship delta: `none`.
- Protected concurrent method:
  `docs/synthesis/methods/deploy-prompts.md` at
  `7c50065bfbccf29e95865ef1962361f51a382a4196aee0f64101bdabe95b53e9`.
- Protected concurrent contract test:
  `tests/test_deploy_prompt_contracts.py` at
  `555b6b055ec79b7b20edde0b477ba5a438d0a33c1d6abd06e7db5cbc4c8b15b2`.

The accepted runtime read back without drift:

| Identity | SHA-256 |
| --- | --- |
| V1 package tree | `c226ca3541cf336fa606799b5e9f7ca538609575e3d73576bacbfda728bff7e9` |
| P1 package tree | `c226ca3541cf336fa606799b5e9f7ca538609575e3d73576bacbfda728bff7e9` |
| P1 `SKILL.md` | `27355fa8228231ead0062581f565394a570414012e6ac11afb311e97aef0c7b9` |
| P1 metadata | `a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94` |
| Entering manifested workspace, including immutable M0 | `e8d7e55ba09a7174aad65e4e5b4add539cb029d3e3753dee35c366de402f0c05` |
| Entering canonical package | `f652f1fb12787a482dcde59771e7b50f8dd5f7a890981df6acede35dc8a47758` |
| Entering installed package | `f652f1fb12787a482dcde59771e7b50f8dd5f7a890981df6acede35dc8a47758` |

Claims, inventory, relationship topology, and removal-risk disposition were
unchanged. The Prompt 2 synthesis had already classified every superseded
current clause; no unresolved current-removal risk remained.

## Canonical Promotion

Exact P1 now occupies `skills/custom/to-tickets`. Full package read-back
proved byte equality with the immutable exact-M0/P1 control before that
experimental control was removed:

```text
canonical c226ca3541cf336fa606799b5e9f7ca538609575e3d73576bacbfda728bff7e9
P1       c226ca3541cf336fa606799b5e9f7ca538609575e3d73576bacbfda728bff7e9
```

The canonical file identities are:

```text
SKILL.md          27355fa8228231ead0062581f565394a570414012e6ac11afb311e97aef0c7b9
agents/openai.yaml a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94
```

The active synthesis now records the M0 surface, research classifications,
all rejected H1 units, accepted V1, `pruning-not-needed` P1, canonical
identity, relationship triggers, proof pointers, deliberate non-changes, and
residual professional, behavioral, model, host, provider, and transfer gaps.
Superseded construction instructions, future lifecycle directions, and
duplicated raw chronology were removed. Historical research, validation,
zero-credit protocol deviations, and raw captures remain unchanged.

One directly affected contract surface was reconciled:
`tests/test_skill_pack_contracts.py` now proves the promoted
`Shape -> Publish -> Return` runtime instead of the superseded
`Trace -> Map -> Slice -> Approve -> Publish` runtime. Its assertions cover
the commitment ledger, Ready-for-agent fields, consumed-outcome blockers,
state matrices, execution profiles, publication order, affected-dependent
read-back, typed Returns, exact downstream triggers, and completion. The
state-boundary consumer assertion was updated to the promoted owner wording.

Relationship topology, the relationship index, callers, callees, router, and
tracker owners were not changed.

## Canonical Proof

- Complete canonical package read-back: passed.
- Canonical/P1 byte parity: passed.
- Directly affected contract file:
  `59 passed`.
- Skill-pack integrity validation: passed.
- Full integration suite after final canonical bytes:
  `205 passed, 4 skipped`.
- Affected Markdown local links, anchors, code fences, and table columns:
  passed for the canonical skill, active synthesis, and this record; no
  affected file contains an internal-anchor link.
- `git diff --check`: passed.
- `git diff --cached --check`: passed; nothing is staged.
- Protected-file and Git `HEAD` read-back: passed without identity change.
- Exact Prompt 4 behavior evidence: reused; no behavior was rerun because P1
  is byte-identical to accepted V1.

## Experimental Lifecycle

Only `skills/experimental/to-tickets/**` was removed. Only the `to-tickets`
entry was removed from `skills/experimental/manifest.json`. Every other
experimental candidate and manifest entry was preserved.

## Managed Installation

The original dry-run stopped at the To Tickets-only cohort boundary. On
2026-07-24 the user explicitly expanded installation authority to the exact
observed two-skill cohort. A refreshed dry-run preserved the global bootstrap
and matched that authority exactly:

```text
python -m scripts.install_skills --dry-run --skip-global-agents
Managed skills: 25 in C:\Users\steve\.agents\skills
Updated skills: to-tickets, writing-great-skills
Unchanged skills: 23
Global bootstrap: skipped
```

The entering identities for the newly authorized companion update were:

| Surface | SHA-256 |
| --- | --- |
| Canonical `skills/custom/writing-great-skills` | `4c076b2a85de33f6ade1e3d552804ff985dfb61dd1b6ecde6788048491b97314` |
| Installed and manifested `writing-great-skills` | `c7c02f4f9896cd5bf6e6c25886e77785a9f80c0ccea0d02f7aaa6fc85076dcc4` |

The supported transaction ran with:

```text
python -m scripts.install_skills --skip-global-agents
Installed 25 custom skills into C:\Users\steve\.agents\skills
Global bootstrap: skipped
```

Sandbox escalation was approved for the installer-owned external write. No
installed file was edited directly. Post-install canonical, installed, and
managed-manifest identities are equal for both authorized skills:

| Skill | Canonical | Installed | Managed manifest |
| --- | --- | --- | --- |
| `to-tickets` | `c226ca3541cf336fa606799b5e9f7ca538609575e3d73576bacbfda728bff7e9` | `c226ca3541cf336fa606799b5e9f7ca538609575e3d73576bacbfda728bff7e9` | `c226ca3541cf336fa606799b5e9f7ca538609575e3d73576bacbfda728bff7e9` |
| `writing-great-skills` | `4c076b2a85de33f6ade1e3d552804ff985dfb61dd1b6ecde6788048491b97314` | `4c076b2a85de33f6ade1e3d552804ff985dfb61dd1b6ecde6788048491b97314` | `4c076b2a85de33f6ade1e3d552804ff985dfb61dd1b6ecde6788048491b97314` |

The managed manifest remains format `1`, source `skills/custom`, with all 25
managed names. The clean post-install dry-run reported:

```text
Managed skills: 25 in C:\Users\steve\.agents\skills
Unchanged skills: 25
Global bootstrap: skipped
```

## Deliberate Non-Changes

- relationship topology, index, triggers, owner boundaries, and Return edges;
- shared deploy methods and their protected contract test;
- other canonical skills, other experimental candidates, and their manifest
  entries;
- global `AGENTS.md` and bootstrap;
- research, raw validation, historical transcripts, and zero-credit
  deviations;
- live provider or tracker state;
- installed managed skills outside the explicitly authorized two-skill cohort;
- repository canonical bytes for `writing-great-skills`; and
- Git index, commits, remotes, and delivery state.

## Residual Gaps

- live-provider publication, read-back, idempotency, eventual consistency,
  mutation durability, and duplicate avoidance;
- professional validity of pack-specific schema and relationship choices;
- unavailable backend build, seed, temperature, hidden system prompt, token
  counts, independent host attestation, and live-provider timing;
- transfer beyond the exact Prompt 4 model, host, reasoning, tasks, authority,
  tools, fixtures, and simulated tracker; and
- support-work comparative economics when settled source supplies no
  comparative facts.

## Shared Run Contract Return

```text
Authorized unit completed: Deploy Prompt 5
Decision: complete
Campaign shape: hypothesis-candidate rederived to exact-M0 V1; no-cut P1
Runtime identities: M0 = V1 = P1 = canonical = installed = managed-manifest to-tickets = c226ca3541cf336fa606799b5e9f7ca538609575e3d73576bacbfda728bff7e9; canonical SKILL.md = 27355fa8228231ead0062581f565394a570414012e6ac11afb311e97aef0c7b9; canonical metadata = a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94; authorized writing-great-skills canonical = installed = managed-manifest = 4c076b2a85de33f6ade1e3d552804ff985dfb61dd1b6ecde6788048491b97314
Artifacts changed: skills/custom/to-tickets/SKILL.md; removed skills/experimental/to-tickets/**; removed only the to-tickets experimental manifest entry; docs/synthesis/skills/to-tickets.md; directly affected assertions in tests/test_skill_pack_contracts.py; docs/validation/transcripts/2026-07-23-to-tickets-prompt5.md; supported managed mirrors for to-tickets and writing-great-skills
Evidence used or reused: exact Prompt 4 acceptance; completed pruning-not-needed record; exact P1/canonical byte parity; complete canonical and synthesis read-back; affected Markdown gate; 59 focused tests; skill validation; full pytest 205 passed and 4 skipped; both diff checks; protected-file and HEAD read-back; exact two-skill install dry-run; supported managed installation; both canonical/installed/manifest parity checks; clean post-install dry-run
Residual gaps: live-provider and transfer gaps recorded above
Recommended next unit: none
Git HEAD: dd3cfa647190e94e40b1e213d8b8cf7e1762a3c6 -> dd3cfa647190e94e40b1e213d8b8cf7e1762a3c6
Git delivery: pending
Exact stop reason: Prompt 5 promoted exact P1, removed only its experimental lifecycle, synchronized exactly the explicitly authorized to-tickets and writing-great-skills cohort through the supported installer, verified both mirrors and the managed manifest, observed a clean post-install dry-run, and stops without Git delivery or another unit.
```
