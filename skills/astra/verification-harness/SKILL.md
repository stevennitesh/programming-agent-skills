---
name: verification-harness
description: Create or reconcile a repository-owned harness that launches, health-checks, drives, observes, and cleans up real user-facing behavior. Use only for explicit harness requests; exclude ordinary test writing, one-off prototypes, and human-only secret or dashboard procedures.
---

# Verification harness

Create the smallest durable way for future agents to exercise the real product
through a supported user-facing surface and capture evidence they can trust.

This skill owns verification tooling and its instructions. It does not change
product behavior merely to make verification pass.

## 1. Establish the real verification surface

Inspect the repository's existing run commands, test or browser harnesses,
development tooling, configuration, and user-facing entry points. Reuse an
existing way to drive the product when it already preserves the property that
must be proved.

Establish five things:

- **surface:** what supported interface the user actually touches;
- **launch:** how the relevant candidate starts or becomes available;
- **drive:** how an agent can exercise that interface through stable controls;
- **observe:** what visible result and material side effects can be captured; and
- **isolate:** how the run avoids mutating another user's session, data, ports,
  profiles, processes, or external resources.

Prefer repository-native or already-installed mechanisms before adding a new
dependency or service. If an existing verification harness already owns the
surface, reconcile that owner rather than creating a parallel one.

Use [prototype](../prototype/SKILL.md) instead when the need is one bounded
observation rather than durable repeatable proof. Use
[wizard](../wizard/SKILL.md) when the decisive steps require private human input,
dashboard interaction, or another session the agent should not observe.

If the product baseline cannot reach the chosen surface, report that product or
environment blocker. Do not modify product behavior under this skill merely to
make the harness succeed.

## 2. Define the harness contract

The harness must make these decisions explicit:

- **Launch and teardown:** the exact entry point, candidate identity, readiness
  condition, and resources the run owns.
- **Doctor:** a read-only check that establishes the instance is the intended
  build, target, profile, account, or environment and is safe to drive.
- **Drive:** stable commands, routes, selectors, protocol calls, or other public
  controls that exercise the ordinary supported path rather than internal setters
  or test-only shortcuts.
- **Evidence:** the action performed, resulting user-visible state, and material
  side effects needed for the claim. A final screenshot or exit code alone is
  insufficient when the transition or effect is what matters.
- **Failure sensitivity:** one safe negative control or equivalent check showing
  that the doctor or evidence assertion rejects a wrong target or wrong result.
  Prefer a mismatched build identity, absent isolated target, deliberately wrong
  expected marker, or disposable fixture; do not damage real product state just
  to prove the harness can fail.
- **Cleanup:** remove only resources created or explicitly owned by this run.
  Never kill by broad process name or delete shared state merely to restore a
  clean-looking environment.

Evidence must survive cleanup when later review needs it. A command named
`dry-run`, `test`, or similar is not proof of harmlessness; verify the
mechanism or observable effects that matter.

Read [Feature map](references/feature-map.md) only when the repository has several
material user-facing feature groups whose reachability or proof recipe would
otherwise be rediscovered repeatedly, or when the user explicitly requests such a
map.

## 3. Build the smallest repository-owned mechanism

Use the repository's established script, tooling, and documentation locations.
Keep the harness narrow: one script or existing tool configuration is enough when
it can launch, doctor, drive, capture evidence, and clean up reliably.

Add helpers only when they remove repeated fragile work. Keep selectors,
commands, ports, profiles, evidence locations, and cleanup ownership explicit
enough that a fresh agent does not have to infer them from implementation code.

Harness-owned scaffolding may support verification without changing supported
product behavior. If a discovered failure belongs to the product rather than the
harness, report it separately instead of weakening the expected result or teaching
the harness around the defect.

Do not use real private credentials merely to validate the harness. Use an
authorized development/test identity or stop at the exact credential or external
access boundary.

## 4. Prove the harness itself

When the intended environment is available and safe to exercise, run the
generated or reconciled instructions end to end:

1. launch or attach to the intended isolated target;
2. run the doctor check and bind the run to the observed candidate identity;
3. exercise one safe negative control that proves the doctor or evidence check
   can fail for the wrong target or result;
4. drive at least one representative supported user path;
5. capture the promised visible result and material side effects;
6. clean up only harness-owned resources; and
7. confirm required evidence still exists and owned resources are gone after
   cleanup.

If the target is rebuilt, restarted into a different candidate, or otherwise
changes identity after doctoring, run the doctor again before attaching evidence
to it.

Classify a failed run before changing the expected result:

- **Harness defect:** launch, doctor, drive, observation, or cleanup is broken, or
  the intended product seam was never reached. Repair only the harness, account
  for owned resources, and rerun from a known state.
- **Product defect:** harness validity and failure sensitivity are established,
  the supported product path was reached, and observed behavior diverges from the
  accepted result. Preserve that evidence and do not weaken the assertion or add a
  shortcut around the defect. If causal diagnosis or repair is requested, hand
  that work to [diagnosing-bugs](../diagnosing-bugs/SKILL.md).
- **Environment blocker:** a required dependency, identity, service, permission,
  or safe isolation boundary is unavailable. Report the exact boundary instead of
  presenting it as a product or harness result.

After a failed iteration, account for processes, ports, profiles, files, and
other resources before retrying. Do not assume cleanup succeeded because a
command returned. If cleanup leaves owned resources behind, report them precisely;
the harness is not verified operational tooling until that recovery path is
understood and safe.

A harness that has not been exercised, or whose decisive observation has not been
shown capable of failing, is a structurally reviewed draft rather than verified
operational tooling. If execution or a safe negative control is unavailable,
return the strongest static evidence and the exact unproved step.

Complete when future agents can identify the target, run the harness without
guessing its ownership boundaries, obtain failure-sensitive evidence for the
supported claim, distinguish harness/product/environment failures, and clean up
safely. Report the created or reconciled paths, candidate identity, proof
performed, known coverage, and any product or environment blocker.
