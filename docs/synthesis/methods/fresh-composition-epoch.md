# Fresh Composition Epoch

This method is the parent controller for one bounded pack-composition epoch.
It owns the epoch schedule, integration pass, Lock decision, and cleanup
handoff. It does not own skill selection, Pack Contract semantics, per-skill
campaign decisions, validation judgment, installation, compatibility
retirement, or Git delivery.

## Inputs and authority

Begin from either an absent Pack Contract or a marker-bounded draft at
`docs/synthesis/skill-pack.md`. The epoch owner supplies the intended pack
outcome and repository/environment fixed point. Research remains bounded to one
independent pass, one Catalog reconciliation pass, and one named-gap pass.
Only the Pack Contract owner may select a capability or skill, assign its
primary role, record a relationship, freeze or amend the contract, or record
the integration result.

The executable relationship vocabulary is exactly `Load`, `Invoke`, `Compose`,
`Hand off`, `Suggest only`, and `Recommend and stop`. Every relationship must
carry its entry and wrong conditions, input and return packets, callee-owned
gates or mutations, resume and combined-exit owners, failure behavior,
context loaded, affected capabilities, ordering impact, and required proofs.

## Controller sequence

1. Materialize or inspect the inactive draft. If the contract is absent, create
   the schema-shaped draft and stop for owner decisions.
2. Freeze only after the five ledgers are complete, essential gaps and
   authority/mutation/invocation/completion collisions are resolved, and the
   proof graph is acyclic. Reject H1, admission, recommendation, adoption, or
   validation-judgment fields.
3. Derive a deterministic topological order from the frozen graph. Among ready
   nodes, order leaf, executable aggregate, then router; use contract order and
   stable skill ID as tie breakers.
4. For each ready node, issue its immutable fingerprinted contract slice to
   the one-skill controller at
   `docs/synthesis/methods/deploy-prompts.md`. That controller runs exactly one
   skill and returns its terminal evidence pointer. It neither chooses nor
   schedules a successor.
5. After all required terminal packets exist, run the pack integration
   scenarios and load-budget checks. Validators report evidence only. The
   epoch owner records `integration-accepted`, `needs-more-evidence`, or
   `blocked` with an evidence pointer.
6. On acceptance, the epoch owner records the epoch Lock and hands cleanup to
   its separately authorized owner. Do not install, retire compatibility, or
   deliver Git state here.

## Branches

| Observed state | Controller return |
|---|---|
| Contract absent | Create an inactive marker-bounded draft; return `contract-draft` |
| Draft incomplete or invalid | Return exact gaps; do not freeze |
| Contract frozen | Return deterministic campaign order and first ready slice |
| Campaign active | Admit only dependency-ready frozen slices; collect terminal pointers |
| Semantic amendment proposed | Require revision plus one; return `behavior-decision-gap` and affected stale proof IDs |
| Contract incompatible | Return `contract-incompatible`; do not infer a repair |
| Integration evidence incomplete | Return `needs-more-evidence` or `blocked` for owner recording |
| Owner-recorded result valid | Return its decision and evidence pointer |

## Amendment and completion

Frozen slices and their fingerprints never change in place. An amendment
creates the next contract revision, identifies the changed skill or ledger
rows, and invalidates exactly those proofs plus graph descendants. Unaffected
proof remains reusable by exact identity.

The epoch completes only when the owner has recorded a valid result and, for an
accepted result, an epoch Lock with its evidence pointer. Return the epoch ID,
contract revision and fingerprint, ordered per-skill terminal pointers,
integration-result pointer, Lock pointer when applicable, and cleanup handoff.
