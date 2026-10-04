---
name: verification-harness
description: Create or improve reusable repository tooling for agents to exercise and verify real product interfaces. Exclude routine test execution and human-private procedures.
---

# Verification harness

Create or improve repository-owned tools that make real product behavior faster,
easier, and more reliable for agents to exercise and verify. Reduce repeated
setup, fragile interactions, and rediscovery. The deliverable is reusable tooling
and enough instructions to use it, demonstrated against the actual product.

Choose the tools, implementation, and verification methods for the requested
capability. Ordinary test execution needs no tooling workflow. Use
[prototype](../prototype/SKILL.md) when the goal is a bounded experiment to resolve
a design or feasibility uncertainty, and [wizard](../wizard/SKILL.md) for a private
or human-only prerequisite.

## Find the useful tooling improvement

Inspect the relevant source, run commands, existing harnesses, and supported
interfaces to identify what agents repeatedly struggle to launch, drive, or
observe. Reuse or improve the existing owner before adding another tool. A script,
tool configuration, or corrected usage instructions may be sufficient; build a
framework only when the requested capability needs one.

Select the surfaces needed for the task. These examples guide fidelity, not a
requirement to support every interface:

- **User interfaces:** drive supported interactions and observe the resulting
  state, persistence, and material side effects relevant to the claim.
- **Commands:** exercise the actual entry point with relevant arguments, input,
  and configuration; expose output, exit behavior, and resulting effects.
- **Agent interfaces:** exercise the advertised API, tool, or MCP contract through
  the interface available to its consumer, including discovery or schemas when
  relevant. Observe usable results, errors, and effects; distinguish an accepted
  asynchronous request from completed work.

Internal calls can help setup or diagnosis, but cannot establish that an untested
consumer interface works. Fixtures or substitutes support only claims about the
properties they preserve; identify integrations or behavior they bypass.

Read [Feature map](references/feature-map.md) when several capabilities or surfaces
need a maintained index to avoid repeated discovery, or when such a map is
explicitly requested.

## Build for repeatable use

Use the repository's established tooling and documentation locations. Add helpers
where they remove repeated fragile work. Leave entry points, inputs, prerequisites,
expected observations, and resource ownership clear enough for a fresh agent to
use the tools without reconstructing their implementation.

Preserve these properties without requiring separate commands or a fixed sequence:

- **Target and readiness:** identify the intended source/build and relevant
  configuration, instance, or account before driving it. Launch or attach as
  appropriate; a separate doctor command is optional. Recheck identity when the
  candidate or target changes so evidence belongs to the claimed instance.
- **Drive and observe:** use stable supported controls and capture the action,
  decisive result, and material side effects. A screenshot, successful tool
  response, or exit code alone is insufficient when a transition or effect is
  what must be established.
- **Isolation and cleanup:** keep mutable fixtures and outputs within authorized
  resources, protecting unrelated sessions, data, processes, and external state.
  Remove only resources the run created or explicitly owns. Never kill by broad
  process name or delete shared state to obtain a clean environment. Preserve
  evidence needed for later review.

Use authorized development/test targets and identities. Do not use real private
credentials merely to validate tooling or expose secrets in captured evidence.
A command named `dry-run` or `test` does not establish harmlessness; check the
mechanism or effects that matter.

Repair ordinary setup, launch, driver, assertion, and cleanup problems within the
assignment and continue without approval for each iteration. Harness scaffolding
must preserve the product behavior being verified. Do not weaken an expectation
or bypass a product defect to produce a passing run.

## Demonstrate the capability

Exercise the created or improved tooling against the intended product using
workflows that establish the requested capability. Choose relevant success,
failure, or recovery cases rather than a fixed test count. A representative run
can prove a driver works; it does not certify every feature reachable through it.

When adding or materially changing custom target checks or outcome assertions,
use a safe negative control or equivalent evidence that the affected check
rejects the relevant wrong target or result. A disposable fixture or deliberately
wrong expected marker may suffice; never damage real state for this purpose.
Rejecting a wrong target alone does not prove that the outcome assertion detects
incorrect behavior. Reuse trustworthy prior check evidence when its mechanism and
conditions remain applicable; unchanged runs need no repeated demonstration.

Interpret failures from evidence. Distinguish broken tooling, product behavior
that violates the accepted result, unavailable environment prerequisites, and
unresolved causes. Failure to reach an interface is not itself a harness defect:
the product may crash during startup. Preserve the observation and uncertainty
until there is enough evidence to attribute it.

If product repair is already authorized, carry the finding into that work and
rerun affected verification after the fix. Otherwise report the product defect
separately. Use [diagnosing-bugs](../diagnosing-bugs/SKILL.md) when a difficult or
intermittent failure needs causal investigation; ordinary repairs need no handoff.

Account for owned resources after failed attempts and before retrying. Confirm
cleanup by the resources' actual state, not only a command's success status, and
confirm required evidence survives. Report anything left behind and its recovery
path; unresolved cleanup prevents claiming reliable unattended reuse.

## Deliver usable tooling

Complete when the requested tooling is usable by a fresh agent, has been exercised
against the intended product, and produces evidence credible for its stated
coverage with understood resource ownership and cleanup. If execution or decisive
checks remain blocked, identify the unproved capability and label the affected
tooling as unverified rather than claiming operational readiness.

Return the created or improved paths, how to use them, what was demonstrated on
which candidate/environment, and material coverage limits or remaining defects.
Resume any already-authorized calling work that the tools unblock. A tooling-only
assignment ends with that deliverable; it does not start a broader product audit.
