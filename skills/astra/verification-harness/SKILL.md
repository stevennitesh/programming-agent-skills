---
name: verification-harness
description: Create or improve reusable repository tooling for agents to exercise and verify real product interfaces. Exclude routine test execution and human-private procedures.
---

# Verification harness

Create or improve reusable repository tools that let agents launch, drive, and
verify real product interfaces without repeated fragile setup or rediscovery.
Deliver usable tooling and instructions, demonstrated against the intended product.
Use this workflow when requested; ordinary test execution needs no tooling phase.
For a bounded feasibility experiment use [prototype](../prototype/SKILL.md);
private or human-only prerequisites belong to [wizard](../wizard/SKILL.md) when
requested.

## Find the useful tooling improvement

Inspect source, run commands, existing tools, and supported interfaces. Improve
the existing owner before adding another tool; a script, configuration change,
or corrected usage instructions may suffice. Build a framework only when needed
for the requested capability.

Select the needed UI, command, API, or agent/MCP surface. Exercise its supported
consumer entry point, including arguments, configuration, discovery, or schemas
when relevant. Internal calls can aid setup or diagnosis but cannot establish
an untested interface works. Substitutes prove only properties they preserve;
identify the integrations or behavior they bypass.

Read [Feature map](references/feature-map.md) when several capabilities need a
maintained verification index or the user requests one. A map is optional and
does not establish that its recipes were exercised.

## Build for repeatable use

Use established tooling/documentation locations. Make entry points, inputs,
prerequisites, expected observations, and resource ownership usable by a fresh
agent without reconstructing the implementation. Preserve these properties
without requiring separate commands or a fixed sequence:

- **Target and readiness:** identify the intended source/build, configuration,
  instance, and account before driving it; launch or attach as appropriate and
  recheck identity when the candidate/target changes. A separate doctor command
  is optional. For browser proof, establish approved-browser access to the actual
  preview URL before dependent checks. A listening server or generated HTML does
  not prove access; use only permitted routes and retain unsupported proof gaps.
- **Drive and observe:** use stable supported controls; capture the action,
  decisive result, and material effects. A screenshot, successful response, exit
  code, accepted asynchronous request, or initial cached rendering alone cannot
  establish a required transition. Where acceptance requires it, change state
  and verify the interface reaches the expected authoritative result.
- **Isolation and cleanup:** isolate mutable fixtures, configuration, and outputs
  within authorized resources. Set state paths before imports that cache them;
  resolve destructive fixture targets and verify ownership before setup/cleanup.
  Keep scratch outside test, formatter, and build discovery unless intentional.
  On Windows with unusable default temp storage, set process-local `TEMP` and
  `TMP` to fresh writable ignored scratch before launching affected tools;
  pytest's `--basetemp` does not redirect every tempfile user or child process.
  Filesystem capability denials, such as hardlinks, need separate diagnosis.
  Remove only owned resources; never kill by broad process name or delete shared
  state for a clean run. Preserve required evidence.

Use authorized development/test identities. Do not use real private credentials
merely to validate tooling or expose secrets in evidence. Inspect consequential
mechanisms: a `dry-run` or `test` name alone does not establish harmlessness.
Repair ordinary setup, launch, driver, assertion, and cleanup failures within
scope without renewed permission. Do not bypass product defects, weaken accepted
expectations, or change the product behavior under test to make tooling pass.

When human inspection is requested, retain a healthy preview and supporting
resources. Hand off the actual URL, target identity, owned sessions/PIDs, recovery
and shutdown routes, cleanup owner, and teardown condition. Ending an assistant
turn alone does not request teardown.

## Demonstrate the capability

Exercise the tools against the intended product with relevant success, failure,
or recovery cases. A representative run can establish a driver works without
certifying every reachable feature. For added or materially changed custom target
checks or outcome assertions, use a safe negative control or equivalent evidence
that rejects the relevant wrong target/result. Wrong-target rejection alone does
not establish outcome sensitivity. Use disposable fixtures or wrong expected
markers, never real-state damage; reuse applicable prior check evidence.

Attribute failures from evidence: tooling defects, product violations, unavailable
prerequisites, and unresolved causes are distinct. Failure to reach an interface
may be a product startup crash. If product repair is authorized, fix it under that
work and rerun affected verification; otherwise report it separately. Use
[diagnosing-bugs](../diagnosing-bugs/SKILL.md) for difficult causal investigation;
ordinary repairs need no handoff.

Account for owned resources after failed attempts and before retrying. Verify
cleanup through actual resource state and preserve evidence. Distinguish intended
human handoff from failed/unaccounted cleanup; unresolved cleanup prevents
claiming reliable unattended reuse.

## Deliver usable tooling

Finish with tooling a fresh agent can use, demonstrated coverage on the identified
candidate/environment, and understood resource ownership. Return paths, usage,
decisive observations, and material gaps or defects. Label blocked or unexercised
capabilities unverified rather than operationally ready. Resume already-authorized
calling work that is unblocked; tooling-only work does not start a product audit.
