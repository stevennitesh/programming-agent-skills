# To Spec Prompt 4 Minimum Proof Coverage

Campaign: `2026-07-24-to-spec`

This matrix fixes the cheapest current proof for every M0 semantic before
behavioral dispatch. Structural and relationship proof establishes only
machine, inventory, invocation-policy, absence, and ownership claims.
Behavioral cases establish branch choice, order, authority, mutation, Return,
and completion.

| M0 units | Obligation | Current proof |
| --- | --- | --- |
| M0-01 | Explicit-only settled-source admission and exclusions | `P-INV-01`, `V06` |
| M0-02 | Routed setup before mutation | `V07`, `P-SAFE-01` |
| M0-03, M0-04 | Complete source/pointer trace, one bounded identity and target | `V04`, `V05`, `V08`, `V09` |
| M0-05 | Read-before-create across absent, matching, divergent, and unknown state | `V01`-`V03`, `V12`-`V14`, `P-SAFE-01` |
| M0-06, M0-09 | Source-owned commitment ledger and behavior-complete draft | `V04`, `V05`, `V09`, `V15`, `P-STRUCT-02` |
| M0-07, M0-08 | Domain/ADR ownership and vocabulary-only `codebase-design` relationship | `V10`, `V11`, `P-REL-01` |
| M0-10, M0-11 | Observable acceptance/proof and proportionate state coverage | `V15`, `V16`, `P-STRUCT-02`, `P-ABS-01` |
| M0-12 | Safe ignored draft plus exact read-back before durable mutation | `V01`-`V03`, `V15`, `P-SAFE-01` |
| M0-13 | Exactly one configured GitHub, GitLab, or Local Markdown publication | `V01`-`V03`, `P-REL-01` |
| M0-14, M0-15, M0-16 | Complete durable read-back, no blind retry, recovery evidence, cleanup/preservation | `V17`-`V20`, `P-SAFE-01` |
| M0-17 | Typed Return, one next recommendation, and downstream stop | `V20`, `V21`, `P-REL-01` |
| All units | Completion and unrelated-state preservation | `V22`, all applicable `V01`-`V21` cases |

The complete viability requirement is `V01` through `V22`; no individual case
is replaced by a structural proxy. `P-STRUCT-01`, `P-STRUCT-02`, `P-ABS-01`,
`P-REL-01`, `P-INV-01`, `P-SAFE-01`, `P-CONTEXT-01`, and
`P-H1-CLASS-01` remain separate deterministic lanes.
