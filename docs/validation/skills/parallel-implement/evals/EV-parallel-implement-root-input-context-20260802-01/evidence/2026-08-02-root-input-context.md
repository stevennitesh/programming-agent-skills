# Root Input Context Behavior Eval

## Setup

- Date: 2026-08-02
- Evaluators: fresh-context `gpt-5.6-sol` agents at `high` reasoning
- Registration: defect correction; situational when an isolated worker needs ignored inputs from the root checkout
- Control: working tree frozen before the root-input change
- Candidate: final working tree frozen at the hashes below
- Samples: five independent controls and five independent final candidates
- Wrong conditions: serial/local worker and isolated worker with no ignored-input dependency
- Sample mutations: none

Control SHA-256:

- Lane helper: `7b3d9758542f2d7592017125add5bb2b83b1dcc25e0a40f51233066710f90280`
- Ledger helper: `b4b9200e55816c16b8751c4912962886bbddc73466cbbfcbee9427a4c4d66ce2`
- Agent Lanes: `856903a52fec3c52782c3bb42c7e8e37045c01bd864aa0add59dc0700e730df9`
- Worker Brief: `c765d99c4f351a5d7c4036445b0ef5dd27504b3393d59e02a3291be78d8b5ad4`
- Run Ledger: `0ab8c21be7bf56f1ca46fa06bea64c60da7877cea6711b5f22be8b6753b6bc0f`

Candidate SHA-256:

- Lane helper: `260d97ce63e8c2f007e83583e40a7b017b203268034ab247eb6b1e6b1e28353d`
- Ledger helper: `8a9536a441166f70b4af9342744a1b8104dba6c2f88b49266f79d11c15a3380a`
- Agent Lanes: `3993e3a5bab4c6d2093c15ef062625cb17dc228a0155b1973bd4adb5aa1b8afa`
- Worker Brief: `5d3b09366596aebcd17a345455c53e799fdcaf6044adfc25fbc90c8e10b653f6`
- Run Ledger: `55dcf43c7f157ce3b188cfa64d9ff31a00fefe259656890ff99926690568251a`

## Scenarios

1. An isolated worker reads an ignored root-only input through
   `PARALLEL_IMPLEMENT_ROOT_CHECKOUT` while every command and write remains in
   its assigned worktree.
2. The generated assignment records the root checkout as read-only and the
   worktree as the only write boundary.
3. Supported lane cleanup removes the isolated worktree without copying,
   owning, or changing the root input.
4. A serial/local worker receives no isolated root binding.
5. An isolated worker that does not need root-only input incurs no copying,
   linking, manifest, discovery, or staging behavior.

## Results

All five controls reproduced the registered deficit: startup proof stayed in
the isolated worktree, but no root-checkout binding or worker-facing read
boundary existed. Cleanup was already scoped correctly. Core score: control
`5/20`; final candidate `20/20`.

All five final candidate samples passed every scenario. They verified that:

- `--repo` remains the root-checkout identity and becomes one read-only context
  binding rather than a copied input tree;
- startup proof receives that binding while retaining the isolated worktree as
  cwd;
- the ledger admits the binding only for isolated lanes and emits the two-path
  read/write boundary only in their briefs;
- local lanes reject the binding and their briefs remain unchanged;
- the lane helper still exposes only `open` and `cleanup`.

The first serial wrong-condition pass exposed that a malformed local preflight
could retain a hidden `root_checkout` field. The candidate was repaired to
reject it, then refrozen. Five final candidate samples and a post-clearance
wrong-condition probe passed the repaired behavior. A second post-clearance
probe confirmed that workers with no root-input dependency receive only passive
context and trigger no data movement.

Two earlier challenges exercised cleanup with deliberately false caller-supplied
root and worktree identities. That unsupported preexisting fallback case was
outside this practical defect correction and did not alter the registered
candidate decision.

## Executable Proof

- Focused helper and structural suite: `110 passed`
- Full repository suite: `649 passed, 5 skipped`
- Skill-pack validation: passed
- `git diff --check`: passed
- `git diff --cached --check`: passed

## Decision

Accept. The candidate makes ignored root inputs available without copying them,
keeps isolated writes and cleanup in the worker worktree, and leaves serial
same-checkout work unchanged.

Residual limit: read-only access is an authority contract, not an operating
system permission. Root inputs can also change while a worker is running; the
workflow does not snapshot them.
