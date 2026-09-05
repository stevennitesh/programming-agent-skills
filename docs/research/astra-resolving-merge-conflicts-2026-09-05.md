# Astra resolving-merge-conflicts assessment

Date: 2026-09-05. This records source selection and validation, not runtime
instructions. Candidate: [resolving-merge-conflicts](../../skills/astra/resolving-merge-conflicts/SKILL.md).

## Decision

Keep a specialist for active Git conflicts. Its value is operation-aware intent
reconciliation, index preservation, and truthful completion. Ordinary implementation
guidance does not supply these Git-specific traps. The package has one main skill
and one conditional operations reference; Git already supplies the mechanics, so
no production wrapper script is needed.

Retain custom safeguards for operation identity, role mapping, missing stages,
path topology, generated artifacts, modes, submodules, reused resolutions,
unrelated index/worktree data, and sequencer completion. Replace repeated separate
permission demands with the task's existing authority and requested endpoint.
Resolve-only does not imply permission to create commits; an authorized request
to finish an integration includes its ordinary continuation steps within policy.
There are no legacy runtime routes. Historical custom source is unchanged.

## Upstream selection

Compared local clones at these exact revisions; this task did not fetch them.

| Source | Revision | Useful contribution and exclusions |
| --- | --- | --- |
| Matt Pocock | `3cca18b368ae95cdbdebbff572ccafa662551015` | Conflict skill: recover source intent, preserve compatible behavior, report tradeoffs, complete the requested replay. Reject blanket staging and unconditional never-abort. |
| Pstack / cursor-plugins | `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | Shipping playbook: evidence must describe the current candidate and integration base. Keep that principle; exclude stack publication, cloud reviewer mandates, patch-ID bookkeeping, and queue ownership machinery. |
| Superpowers | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | Finishing-a-development-branch: test the actual combined result. Exclude its integration menu, unconditional full-suite requirement, and branch cleanup workflow. |
| Ponytail | `974d940a1c5344210874150b98ff0d2c861fab6a` | Main skill: trace the real flow before simplifying; native tools before new machinery. Already covered by the contract and candidate. No distinct conflict procedure found in its skills; do not import persistent persona, shortest-diff mandates, or feature reduction. |

Local source paths are `.tmp/repos/mattpocock-skills/skills/engineering/resolving-merge-conflicts/SKILL.md`,
`.tmp/repos/cursor-plugins/pstack/skills/poteto-mode/playbooks/shipping.md`,
`.tmp/repos/superpowers/skills/finishing-a-development-branch/SKILL.md`, and
`.tmp/repos/ponytail/skills/ponytail/SKILL.md`.

Official Git documentation confirms inverted rebase side roles and the need to
inspect reused resolutions ([git-rebase](https://git-scm.com/docs/git-rebase)).
It also documents conflicts during post-merge autostash restoration
([git-merge](https://git-scm.com/docs/git-merge)) and revert's selected mainline
and no-commit mode ([git-revert](https://git-scm.com/docs/git-revert)). The concrete
conflicted no-commit continuation hazards below came from local experiments,
not an assumption that those documentation pages guarantee sequencer behavior.

## Challenges and revisions

Two fresh-context, read-only reviewers had separate seams: Git mechanics/data
preservation and intent/authority/upstream omissions. The candidate remained
frozen during each review. Accepted findings:

- Include consequential intent choices and tradeoffs in the completion report.
- Distinguish a no-commit merge's prepared endpoint from replay continuation.

Experiments then disproved the initial assumption that saved no-commit options
are sufficient to make replay continuation safe. The final conditional paragraph
requires a verified endpoint-preserving method or leaves the prepared index and
remaining sequence intact. The Git reviewer rechecked the observed state and
approved that correction; the intent reviewer also rechecked the final authority
wording and passed it. This is a concrete example of why review alone is not
execution evidence.

## Execution evidence

Disposable fixtures and scripts live under `.tmp/astra-conflict-exercise/`.
Git version: `2.54.0.windows.1`. Fixture commits do not modify this repository's
history. Two fresh execution workers received the source skill, isolated fixture
ownership, and a neutral request to finish the existing integration. They were
not given the root's expected outputs and were instructed not to use memory or
other tasks' artifacts.

The fixture combines an invoice field rename with a currency/display change.
Expected behavior is exact `amount_cents` plus USD with no obsolete `total`
alias, exercised through the actual display caller. Both workers recovered that
intent from history, checked positive/negative/zero cases, and preserved unrelated
tracked and untracked file hashes.

- Merge completed through native continuation at
  `4fa6a6190b1026e1f5138073846c52490388a98c`; only the two resolved source files
  were committed, with no remaining operation or unmerged entries.
- Rebase with unrelated unstaged tracked work correctly stopped after preparing
  and proving the resolution. Git refused continuation. The worker preserved the
  unrelated work and reported the active operation instead of hiding that blocker.
- A separate copy completed the rebase at
  `4ec1afbcde186df9872454e658541276565d46fc` without that unstaged blocker;
  the original blocked fixture is retained for inspection. Sandbox editor
  subprocess failures required an approved escalation with command-local Git
  configuration; no persistent configuration was changed.
- No-commit merge: resolution leaves HEAD unchanged and the merge/index prepared.
- Conflicted multi-item `cherry-pick -n`: continuation rejected the prepared local
  changes, retaining the sequence and index.
- Conflicted multi-item `revert -n`: native continuation created a commit for the
  resolved first item and left the next reversal staged, despite the original
  no-commit mode. This intentionally unsafe command was confined to a disposable
  probe; final skill instructions prevent assuming it preserves the endpoint.

`check_no_commit.py` reproduced all three outcomes, including the unexpected
commit. These are version-specific observations, not claims about every Git
version. They justify a conservative conditional rule, not a new recovery tool.

Root independently checked exact invoice output and the actual display caller
for zero, negative, positive, and large integer cents, plus unrelated file content
and final operation state. Package validation, local links, whitespace checks,
and all 10 focused repository tests passed. These probes establish
bounded workflow behavior, not comparative superiority over the model baseline.
No remote publication, submodule, binary, rename, rerere, autostash restoration,
or concurrent-writer execution was tested; those branches received document review.
