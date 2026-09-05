# Astra implement rewrite assessment

This records the source selection and editorial assessment for the initial
`skills/astra/implement/` candidate. It is evidence for this rewrite, not runtime
instructions or proof of improved coding performance. The current direction
is owned by [the Astra design brief](../astra/design-brief.md).

## Recommendation

Keep implement as a short procedure for completing a coding outcome. Let the
engineering contract own shared design judgment. Keep unusual verification
examples behind a conditional reference. Accept direct requests as well as
specs and tickets, and allow verified no-change outcomes.

The custom skill already contains most of the valuable engineering content.
Its main problem is composition: repeated contract guidance, detailed proof
cases in the common path, and dependencies on the old tracker and skill flow.
The rewrite removes those costs while retaining real integration, discriminating
proof, authorized effects, and truthful completion.

## Upstream selection

Inspected the local upstream snapshots previously refreshed for this research:

| Source and commit | Useful contribution | Treatment in this candidate |
| --- | --- | --- |
| Matt Pocock `3cca18b368ae95cdbdebbff572ccafa662551015` | `skills/engineering/implement/SKILL.md` gives a recognizable implementation flow. | Keep the direct shape. TDD, full suite, review, and commit follow the task and repository rather than becoming universal requirements. |
| Pstack `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | `principle-sequence-verifiable-units`, `principle-outcome-oriented-execution`, and `principle-fix-root-causes` add checkpoints, completion discipline, and causal repair. | Choose coherent verification boundaries. Qualify intermediate breakage by reversibility and real compatibility needs. Do not require every edit to be green, rebase before work, or broaden a fix to every similar instance. |
| Superpowers `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | `executing-plans` checks a supplied plan; `test-driven-development/writing-good-tests.md` identifies the break a test catches and rejects mirrored expectations. | Reconcile plan assumptions with current code and require useful independent expectations for added tests. Do not import automatic delegation, worktrees, branch finishing, or stops for routine recoverable problems. |
| Ponytail `974d940a1c5344210874150b98ff0d2c861fab6a` | `skills/ponytail/SKILL.md` places understanding before its reuse ladder and seeks the causal owner. | Consider existing capabilities and total maintenance cost. Leave detailed reuse judgment in the contract. Reject shortest-diff optimization, persistent persona modes, and substituting a smaller outcome for the requested one. |

The checkpoint guidance needs reconciliation: Pstack's per-unit green rule and
its acceptance of planned intermediate breakage cannot both be universal. A
coherent unit may span several files. Check where evidence is meaningful, and
preserve deployment compatibility when consumers actually depend on it.

## Local changes

- Replace the single ready-item prerequisite with a bounded requested outcome.
- Keep causal investigation inside ordinary bug fixing; do not require another
  skill merely because the first hypothesis is uncertain.
- Keep shared engineering rules in their repository owner. The entrypoint adds
  the order of work, checkpoints, and completion decisions.
- Move handoff, mixed-result, identity, termination, and effect-recovery examples
  to one conditionally loaded verification reference.
- Use the repository's tracker and delegation owners when applicable. Missing
  preferred setup does not force bootstrap or block otherwise actionable work.
- Preserve required checks, affected reruns, final candidate inspection, and
  explicit limits on proof and action authority.

## Scenario walkthrough and limits

Editorial walkthroughs checked these intended paths:

| Request | Intended behavior |
| --- | --- |
| Ordinary bug | Establish a discriminating case, repair the cause, run affected checks. No automatic ticket or reviewer. |
| Bounded feature | Trace the entry point, complete wiring, verify the caller-visible result. |
| Refactor | Preserve the accepted contract and use coherent checkpoints without forcing a test after each file. |
| External boundary change | Load the relevant verification case, exercise the safe authorized path, and distinguish proxy evidence from actual effects. |
| Outcome already satisfied | Verify existing behavior and finish without manufacturing a code change. |
| Consumer with missing producer | Preserve the integration gap; report the prerequisite without declaring completion or expanding scope. |

These are instruction walkthroughs, not executions by independent agents.
Package validation and link checks establish packaging only. The proposed coding
pilot remains necessary to compare this candidate with direct coding under the
same engineering contract. No perfect-score or measured quality claim is made.
