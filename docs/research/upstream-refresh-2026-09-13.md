# Upstream clone refresh, 2026-09-13

Historical refresh evidence, not adopted pack instructions. Baselines are the
local HEADs recorded immediately before fetching. Each clone was clean, fetched
with `git fetch --prune origin`, and updated with `git merge --ff-only origin/main`.
All four finished clean with HEAD equal to the freshly fetched origin/main.
Only main was checked out; fetched feature branches were not incorporated.

## Commit boundaries

Clones live under `.tmp/repos/`.

| Clone | Previous HEAD | Updated HEAD | New reachable commits |
| --- | --- | --- | --- |
| mattpocock-skills | `3cca18b368ae95cdbdebbff572ccafa662551015` | `3cca18b368ae95cdbdebbff572ccafa662551015` | 0 |
| cursor-plugins (contains pstack) | `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | `5bf2b1544db739998121a306340631963c2ff3de` | 35 |
| ponytail | `974d940a1c5344210874150b98ff0d2c861fab6a` | `356918eba965ee1eac64bd3a7f0dd02108350de5` | 9 |
| superpowers | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | 0 |

Counts include merge commits. Cursor's 35 commits cover the whole plugin repository;
seven commits in that range touch pstack.

## Pstack changes

[Full repository comparison](https://github.com/cursor/plugins/compare/93b00b89ef425a9c1bac0d0b317dfc49c930ac99...5bf2b1544db739998121a306340631963c2ff3de).
Within pstack: 95 files changed, 579 insertions, 834 deletions.

- `e8d856f`: broad density/prose pass. The `how` skill loses its architecture
  critique mode and deletes the critic prompt and critique rubric. Its explanation
  path still delegates. `why` trims repeated explanation and output-format detail,
  retaining references and its seven-category investigation posture.
- The same commit adds `principle-attack-the-premise` and
  `principle-test-behavior-not-implementation`. The first challenges a shared
  premise after repeated failed fixes, with a prescribed per-actor census. The
  second emphasizes observable behavior and expected results in tests.
- `d7cde2b`: further prose punctuation cleanup across skills.
- `71ed0d1`: pstack version becomes 0.15.0; README and guide counts are synchronized.
- `f8abedd`: reply guidance requires evidence or a measured/inferred/guess label
  alongside claims.
- `f5bdd68`: operator-neutral pronouns and in-chat status updates, as recorded in
  the commit subject.
- `889ec4b`: bug-fix, performance, and hillclimb default worker changes from
  `claude-fable-5-1-thinking-max` to `grok-4.6-fast-xhigh`.
- `5bf2b15`: setup adds budget choices mapping to max/xhigh/high/medium reasoning,
  checks available model slugs, and records the budget in its model override rule.

Outside pstack, the same repository range adds Grok Voice and third-party plugin
entries including Attio, Hunter, Teams, Gamma, Finance, Webull, S&P Global,
Interactive Brokers, Meltwater, Daloopa, Excalidraw, and Google Cloud BigQuery.
These are clone updates, not installed plugins.

## Ponytail changes

[Comparison](https://github.com/DietrichGebert/ponytail/compare/974d940a1c5344210874150b98ff0d2c861fab6a...356918eba965ee1eac64bd3a7f0dd02108350de5).
All nine commits concern the README's Built with Ponytail / Retriever showcase
and logo presentation. The final diff changes four files: README plus a PNG icon
and dark/light SVG logos, with 19 text insertions and no text deletions.
No skill or executable implementation changes occur in this range.

Matt Pocock and Superpowers have no main-branch changes from the recorded baselines.
Superpowers fetched updates to other branches, including dev, without moving main.

## Relevance and verification limits

The pstack simplification and behavior-testing changes are useful comparison
material for the pack's proportional-engineering work. Reduced prose alone does
not establish reduced ceremony: mandatory delegation, investigation categories,
and the new census procedure still need independent judgment before any adoption.
No upstream instructions or model choices were migrated into the managed pack.

Verification covered Git ancestry/update success, clean working trees, remote
tracking parity, commit logs, file statistics, and selected substantive diffs.
Upstream test suites were not run; this is a refresh/change note, not a correctness
audit. Machine-readable before/after records and complete per-clone commit lists
and diff statistics are saved locally under `.tmp/upstream-refresh-2026-09-13/`.
