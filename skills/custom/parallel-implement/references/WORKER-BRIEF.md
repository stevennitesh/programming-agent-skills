# Lane Worker Brief

Implement exactly one assigned work item.

## Assignment

**Work item:** `<id and title>`
**Source Trace:** `<issue / packet / spec slice / decisions / named repo sources>`
**Base SHA:** `<orchestrator-verified sha>`
**Lane provider:** `<runtime-managed / manual-git>`
**Worktree:** `<absolute isolated path>`
**Preflight packet:** `<exact packet or lane-local path / packet identity>`
**Git trust:** `<normal / command-scoped safe.directory>`
**Expected write scope:** `<paths/modules, or discover and report before widening>`
**Acceptance:** `<criteria, blockers, exclusions, dependencies>`
**Integration context:** `<relevant landed interfaces or decisions / none>`
**Focused proof:** `<commands or evidence>`
**Validation environment:** `<interpreter, cwd, cache/temp paths, focused runner>`
**Report transport:** `<compact inline packet / exact lane-local .tmp path>`

## Contract

Read every Source Trace entry and `docs/agents/engineering-contract.md`. The work-item source owns acceptance; this brief owns lane-worker process.

**Workspace boundary:** the assigned worktree, not the process startup cwd, is your workspace. Verify the recorded preflight packet against the current root, base, status, write probes, Git trust route, and proof startup before editing. Set the assigned path as `workdir` on every shell call and use absolute paths beneath it for edits. Stop on a mismatch.

**One worker, one lane, one packet:** never spawn, integrate, formally review, mutate trackers, push, or widen scope. Return exactly one clean local commit plus focused proof, or a `blocker` or `needs-feedback` packet.

For red-testable new behavior, invoke `$tdd`. For a bug, invoke `$tdd` only when expected behavior, the exact symptom, the cause, and a trusted red-capable reproduction are known. When a bug's expected behavior, exact symptom, cause, or trusted red-capable reproduction is uncertain, invoke `$diagnosing-bugs` in fix mode with this lane worker as its caller; return here after regression proof.

Apply the routed proof budget. Run broad validation only for shared-behavior risk or an explicit route. Use the assigned environment and lane-local cache/temp paths. Shared dependency mutation requires an explicit route.

Keep product intent, acceptance, public and domain contracts, dependencies, security/privacy posture, and adjacent work outside the lane unless the Source Trace already authorizes them. Return a commitment change as `needs-feedback`.

## Report

`done` requires verified preflight, every acceptance criterion accounted for, one worker commit, focused proof, and clean final status. `blocker` or `needs-feedback` claims no completion and preserves exact state.

```text
status: <done / blocker / needs-feedback>
work item:
source trace:
preflight:
base:
commit:
owned files:
proof: <acceptance criterion -> evidence; focused commands/results>
skipped checks:
risk/blockers:
next need:
scope notes:
final status: <clean / dirty + reason>
skill feedback:
```
