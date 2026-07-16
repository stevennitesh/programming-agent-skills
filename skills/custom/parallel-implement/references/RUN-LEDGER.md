# Parallel Implement Run Ledger

Instantiate this disposable append-only ledger at `.tmp/parallel-implement/<run-id>/LEDGER.md`. Copy durable facts to the routed closeout destination before cleanup.

Append each event once. Derive routing and closeout from the event stream.

## Routing Packet

**Started:** `<date/time>`
**Source Trace:** `<request / parent / packet / items / decisions / repo sources>`
**Parent:** `<id / title / source type / relationship source / closeout rule>`
**Run fixed point:** `<starting ref for bases, integration, and review>`
**Child-set snapshot:** `<every associated child and follow-up / state / disposition / late relationship changes>`
**Selected scope and DAG:** `<in-scope items / dependencies / exclusions / blockers>`
**Frontier plan:** `<serial or parallel generations / tracker order / independence decisions>`
**Integration:** `<shallow, hot, or late / branch / owner / checkout>`
**Landing:** `<executor / harness or manual gate / cherry-pick, merge, squash, or patch>`
**Lanes:** `<provider / identifier / fresh-context policy / selected root and reason / worktree and env isolation>`
**Lane proof:** `<creation and preflight packet identities / path budget / effective identity / Git trust / cleanup routes>`
**Slot lock:** `<capacity / reservations / worker limit / review-bandwidth rationale>`
**Proof budget:** `<worker focused / integration touched-area / loop-close broad>`
**Review:** `<route / orchestrator owner / all-lanes-idle gate>`
**Tracker and closeout:** `<lock mode / durable destination>`
**Permission plan:** `<worktrees, install, network, push, tracker, messages, destructive Git>`
**Release rule:** `<lane, worktree, commit, branch, claim, tracker, push, checks, and risk accounting>`

Resolve every field or mark it `not applicable` before dispatch. Shallow mode uses the same packet.

## Event Stream

`events.jsonl` beside this ledger is the sole append-only event stream. Append, validate, and list it only through `../scripts/run_ledger.py`. Each schema-versioned event owns its id, timestamp, type, work item, worker and integration SHAs, validation, decision, risk, and optional packet data. The orchestrator is the sole writer.

## Child Closeout Packets

Create one record immediately after each accepted landing. Preserve structured evidence; render tracker prose only through the template below.

### `<work-item-id>`

**State:** `<draft / review-final / posted / verified>`
**Worker commit:** `<sha>`
**Integration commit:** `<sha>`
**Delivered:** `<bounded implementation summary>`
**Acceptance evidence:** `<criterion -> evidence>`
**Focused and integration proof:** `<command -> result>`
**Review:** `<route / reviewed HEAD / result>`
**Residual risk:** `<none / accepted risk>`
**Intended mutation:** `<implemented state / prior state removal / claim release / close reason>`
**Posted comment:** `<not posted / comment URL or id>`
**Mutation read-back:** `<not applied / resulting labels, assignee, close state, relationships, and frontier>`

Finalize `Review` and `Residual risk` after the accepted parent-level review. A packet becomes `review-final` only when every pre-mutation field is resolved. After posting and mutation, record the comment reference and tracker read-back; `verified` requires both.

On resume, if tracker mutation may have occurred but the packet lacks its comment reference or read-back, refetch the ticket and affected dependents. Record recovery only when one posted comment exactly matches the packet rendering and the intended mutation verifies; otherwise return `blocked` with the mismatch. Never repost or replay an uncertain mutation.

Render each tracker comment exactly from its packet:

```markdown
Implemented in `<integration-commit>`.

### Delivered

<delivered>

### Acceptance

<acceptance-evidence>

### Validation

<focused-and-integration-proof>

### Review

<review>

### Residual risk

<none-or-accepted-risk>
```

## Closeout Summary

Fill this before closeout tracker mutation.

**Outcome:** `<complete / partial / blocked>`
**Parent and closeout:** `<id / final state / read-back>`
**Child-set reconciliation:** `<initial snapshot / late additions, removals, or relinks / resolution>`
**Run fixed point:** `<sha>`
**Current integration HEAD:** `<sha / none>`
**Current Git state:** `<clean / exact in-progress state>`
**Reviewed HEAD:** `<sha / not reached>`
**Approved closeout HEAD:** `<sha / not reached>`
**Child disposition and closeout:** `<every id / packet state / landing order or non-implementation disposition / tracker state / read-back>`
**Frontier history:** `<serial and parallel generations / blockers / drain evidence>`
**Final validation and review:** `<commands and route result / not reached>`
**Blockers and next owner:** `<none / exact blockers and owner>`
**Remaining permissions or mutations:** `<none / exact actions and authority>`
**Tracker, claims, parent, push, and durable closeout:** `<actions and read-back / skipped>`
**Release sweep:** `<every lane provider, identifier, worktree, commit, branch, registration result, directory result, and preserved state>`
**Skipped checks and residual risks:** `<none / list>`
**Skill feedback and follow-ups:** `<none / list>`
