---
name: wizard
description: Create one repository-native interactive script for a bounded procedure with several settled steps only the current human can perform. Use only when explicitly selected; exclude agent-executable work, single approvals, live guidance, unresolved decisions, questionnaires, and ordinary implementation.
---

# Wizard

Turn one settled human-only procedure into one guided local script. The script
may direct browser or physical actions and collect values at runtime. The
authoring agent never receives real secrets or runs the manual, credentialed,
destructive, or external-mutation stages.

The invocation authorizes one local script inside the requested scope. It does
not authorize executing the procedure, installing a runtime or dependency,
committing, publishing, or changing unrelated documentation.

## 1. Qualify

Inspect the repository, available tools, and requested result. Separate work the
agent can perform with current authority from steps that require the human's
identity, credentials, judgment, physical access, or dashboard session.

Use Wizard only when several settled human-only steps form a procedure and a
script is more useful than live guidance. Otherwise perform authorized work in
its current owner or return the one manual action directly. Return an unresolved
decision or missing fact to its owner instead of encoding a guess.

## 2. Map

Name the stages in dependency order. For each one, establish its authoritative
instruction source, human action, and destination or effect. When a stage
captures a value, also establish its secret status. When it mutates state,
establish the exact local or external target. Inspect examples, configuration,
consumers, and variable names without reading existing secret values. Never ask
the user to paste a secret into chat.

Check current official instructions when a third-party command or interface may
have changed. Ask only when a consequential instruction, target, destination,
or authority remains unknown. Do not treat every referenced environment or CI
name as Wizard-owned.

## 3. Author

Write one script in the requested location. Otherwise use the repository's
ignored scratch convention, or `.tmp/wizard-<slug>.<ext>` when none is defined.
Choose an existing repository runtime or the operator's native shell. Add no
runtime or dependency for the wizard. Use a durable scripts directory only when
the user requested a repeatable repository workflow.

Keep each stage focused. Open or print the authoritative source or instruction
before asking the human for a value. Identify the destination without displaying
its existing contents. Capture secrets without echoing or embedding them. Before
writing a secret-bearing local file, resolve its exact path and establish that
the repository intentionally excludes it from source control.

Use native secure input or standard input when a tool supports it. Never place
a secret in command arguments, logs, transcripts, or temporary files.

Before a destructive action, show its exact target and confirm. Before a durable
external effect, show its exact target and active identity, confirm authority,
establish an observable postcondition, and read it back afterward. When a secret
value cannot be returned, verify its exact scope, name, and fresh metadata and
state that value equality remains unproved. Leave the mutation manual and
unverified when no useful postcondition is observable.

Stop dependent stages after a required stage fails or is cancelled. If an
effect may have partially succeeded or its result is indeterminate, inspect
current state before choosing recovery. Make an expected resume or retry
converge without duplicate effects. Leave harmless stages free of those
controls, and never report completion while required work remains unfinished.

## 4. Check

Run the nearest syntax or lint check for the chosen runtime. Statically trace
every declared input to its destination and every effect to its target,
applicable confirmation, read-back, and applicable recovery path.

Do not execute browser, credential, destructive, or external-mutation stages.
State what syntax and static tracing prove and what the operator's first run
must still verify.

## 5. Return

Return the script path, one run command, the effects it may perform, the checks
run, and any unresolved manual detail. Stop before execution, installation,
commit, publication, cleanup, or another workflow.

Complete when one secret-free, statically verified script covers every admitted
human-only stage, the run command fits the target environment, and no manual or
external stage has been executed.
