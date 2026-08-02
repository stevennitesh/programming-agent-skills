# Collaboration Profiles Behavior Eval

## Setup

- Date: 2026-08-02
- Evaluators: fresh-context `gpt-5.6-sol` agents at `high` reasoning
- Control: commit `c0d45be1de53edb21ce27737552df83c14d5897d`
- Candidate: current working tree, frozen at the hashes below
- Samples: five independent controls and five independent final candidates
- Wrong condition: one frozen-control/current-candidate pair
- Sample mutations: none

Candidate SHA-256:

- Parallel Implement: `e69f0749e15e8529f695f47d89f3c45fb5032598242de260edb93f18326ea0bf`
- Agent Lanes: `856903a52fec3c52782c3bb42c7e8e37045c01bd864aa0add59dc0700e730df9`
- Runtime Profiles: `175da1c77df8ce0d53aca12ccc1b11763333dd9558436381bb65f5d1198f241f`
- Implement: `4b6a6eed49c7233fa6ef39162a6fe0bd7cce08f0bd05b77a57a11da81337e7e0`
- Change Review: `ebcee7391687dd79e8825d4513c585b9f12a6608411f0ca8afb9a4165763aca4`
- High Assurance Review: `555770285a9c71a2371cf6262da16b52f20ee0d79b6b9a9a2d1aa6a478032898`
- Run ledger helper: `b4b9200e55816c16b8751c4912962886bbddc73466cbbfcbee9427a4c4d66ce2`

## Scenarios

1. Serial clear implementation uses a same-checkout `luna_max` collaboration
   subagent with no extra worktree.
2. Concurrent adaptive implementation uses a helper-created isolated worktree
   plus a `default` `gpt-5.6-terra` `xhigh` collaboration subagent.
3. Ordinary formal review starts after writers stop and uses one fresh read-only
   same-checkout `gpt-5.6-sol` `high` collaboration subagent.

Every scenario prohibits root implementation. The locality check requires
Agent Lanes to own general checkout isolation and Runtime Profiles to own model
bindings.

## Results

All five controls failed all three scenarios. They selected managed Codex tasks;
the concurrent adaptive lane also selected a managed worktree and Terra `max`.
None allowed root implementation.

All five final candidate samples passed all three scenarios. They agreed that:

- collaboration subagents are the only actor transport;
- serial and review actors use the integration checkout without an extra
  worktree;
- concurrent writers use helper-created worktrees;
- `adaptive-worker` resolves to Terra `xhigh`;
- Agent Lanes solely owns general serial/concurrent isolation;
- no material ambiguity or duplicated isolation authority remains.

Score: control `0/15`; candidate `15/15`.

The wrong-condition pair supplied one standalone Ready item to `$implement`.
Both control and candidate kept implementation in the current checkout, did not
invoke `$parallel-implement`, and created no isolated worktree. The change did
not broaden worktree orchestration into single-item delivery.

## Decision

Accept. Focused helper and structural tests exercise the profile resolver,
binding validation, delegated local lanes, helper-created temporary Git
worktrees, read-only review lanes, cleanup, and removal of managed-task routes.
The behavioral samples were read-only contract traces; they did not run a live
end-to-end campaign.
