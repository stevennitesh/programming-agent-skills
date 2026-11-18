# Agent instruction files

Use when changing instruction scope or reading paths, preparing a repository
for the pack, or explicitly setting up global guidance.

## Repository scope

Use the instruction files the target agent actually reads. Preserve nested rules
at their applicable scope and compatible instructions for other tools unless
their reconciliation is requested. A new pointer must reach the needed guidance
before the decision it governs; a preferred template does not justify parallel
instruction files.

## Pack availability

When preparing a repo for this pack, check that the intended host can discover
the relevant skills and that an agent using them can reach the repo's commands,
constraints, and owners. Reuse the host's installation and the repo's layout.
Report missing skills or unverified host access separately from repo readiness.
The pack's installation instructions own any separately authorized host setup.

## Global scope

Keep durable cross-repository preferences and host constraints in global guidance;
project commands, facts, and engineering policy belong to the repository.

For authorized global setup, adapt [the global seed](../templates/global-agents.md)
to the user's actual preferences. Delegation and context-inheritance policy belong
to the active runtime, user instructions, and executing workflow.

Preserve unrelated global content and any bootstrap section owned by the managed
installer. Repository-local setup does not include global-file edits, and a seed
change is not authority to overwrite installed guidance.
