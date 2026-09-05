# Astra hillclimb rewrite

This records the optional iterative-optimization skill's source selection and
review. It is not a claim of demonstrated improvement over baseline agent behavior.

## Direction

Preserve the custom skill's comparable experiments, faithful workload, meaningful
keep criterion, isolated attempt deltas, protected incumbent, original-to-final
comparison, and honest stopping reason. Separate iterative improvement of actual
code from prototype feasibility and diagnosis of a reported failure.

Allow a finite exploratory optimization run when the user supplies direction but
no numeric target or attempt count. State the effort bound; do not invent acceptable
quality losses, product requirements, external spending, or future scheduling.
Remove automatic stops merely because a ruler must be corrected: remeasure both
sides under the revised method instead of comparing incompatible numbers.

Conditional measurement guidance adds adaptive-selection bias, fresh confirmation,
held-out workloads when generalization is claimed, meaningful tail measurements,
observer/scaffolding effects, downstream cost displacement, and secondary resource
consequences. These refine evidence, not mandate a statistics toolkit for every run.

## Source selection

Compared the local snapshots already used in this workstream; no fetch performed.

| Source | Commit | Selection |
| --- | --- | --- |
| Custom hillclimb | Current working tree | Most useful controls already exist: equivalent work, no unmeasured stacks, removable deltas, serial decisive measurement, compact history, final integrated confirmation. Keep these with clearer retained/original baselines and explicit incomplete verification. |
| Pstack | `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | Hillclimb playbook and prove-it-works supply mechanism-specific hypotheses, sensitivity, feedback history, and reconsidering a plateau. Reject minimum iteration floors, automatic model-specific workers, commits, and mandatory TSV or persistent harness. |
| Matt Pocock | `3cca18b368ae95cdbdebbff572ccafa662551015` | Diagnosing-bugs supplies comparable performance evidence and faithful feedback. No dedicated hillclimb skill was found in the inspected engineering inventory. Do not import its rigid reproduction or minimization gates. |
| Superpowers | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | Systematic-debugging's controlled hypotheses and original-symptom verification are relevant supporting methods. No dedicated optimization-loop skill was found in the inspected skills inventory. Mandatory TDD and fixed failure-count escalation do not transfer. |
| Ponytail | `974d940a1c5344210874150b98ff0d2c861fab6a` | Reuse/simplification and the explicit warning that published benchmark medians are not per-repository savings reinforce attribution. Do not substitute line count for outcome improvement or published gains for local measurement. |

No experiment runner is added: benchmarks, profilers, quality evaluators, and
correctness checks depend on the repository. The skill governs interpretation
and safe retention rather than introducing another generic measurement framework.

## Challenger review

Two fresh-context reviewers examined the fixed candidate read-only. Measurement
review passed adaptive-overfit, noisy-winner, shifted-work, quality-tradeoff,
changed-ruler, combined-gain, and partial-baseline scenarios. Workflow review found
that a numeric target without a supplied budget lacked an explicit default effort
bound. The final rule supplies a stated finite local budget whenever one is absent;
the reviewer rechecked and passed the correction.

Skill and repository validation, local links, and whitespace checks passed.

## Verification limits

Package and link validation establish structure; textual challenges can expose
misleading acceptance or unsafe rollback rules. A later behavioral evaluation
would need noisy measurements and plausible false wins, not only an obvious
algorithmic speedup. Legacy skill consumers remain unchanged; source creation
does not install, commit, or deploy anything.
