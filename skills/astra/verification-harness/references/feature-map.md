# Feature map

Read when several capabilities or interfaces would make agents repeatedly
rediscover how to reach and verify the product, or when the user explicitly
requests a maintained verification map. Include relevant UI, command, and agent
interfaces without requiring an exhaustive product inventory.

The map is navigation for verification, not a second product specification and
not evidence that every listed feature was exercised.

## Record supported proof routes

Use the repository's existing documentation structure. Prefer one compact index
when it remains readable; split feature entries only when their drive or evidence
instructions need independent maintenance.

For each mapped feature, record only what a future verifier needs:

- the capability and the human or agent interface being exercised;
- its supported entry point;
- the reusable command, driver, or interaction needed to exercise it;
- the observable end state and material side effects that establish success; and
- prerequisites or isolation constraints that materially change the run.

Use stable handles offered by the supported interface rather than incidental
coordinates, DOM structure, or private methods when a better anchor exists.
Where a capability has multiple interfaces, make clear which route each recipe
exercises; an API call does not establish that the corresponding UI or CLI works.

## Keep coverage claims honest

A feature map can contain unexercised entries. Use existing repository conventions
to distinguish documented recipes, exercised coverage, blockers, and stale
instructions. A verification claim needs an actual run tied to its candidate and
relevant environment, with decisive observations and trustworthy assertions as
described in the skill. Link to evidence when later use depends on it; a recipe
alone does not establish behavior. One representative harness proof does not
certify every mapped feature, and a past run is not proof of a changed candidate.

Record substitutions or unavailable integrations that materially limit a recipe's
proof. Reference accepted behavior at its owner instead of maintaining a second
specification in the map.

When source changes make a mapped route, selector, command, prerequisite, or
expected result doubtful, reconcile the affected entry rather than silently
teaching future agents an obsolete path.

Product behavior that no longer satisfies an accepted feature is a product gap,
not documentation drift. Keep that defect separate from harness or map repair.
