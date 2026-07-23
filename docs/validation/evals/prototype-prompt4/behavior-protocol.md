# Prototype Prompt 4 Behavioral Protocol

Read every file in the assigned Prototype package and no other Prototype
package, synthesis, test, evaluation, or prior output. Treat each case below
as an independent invocation unless the case explicitly states a sequence.
Do not execute commands, mutate files, invoke another skill, or invent missing
facts. For each case, report:

- files loaded;
- fit and readiness decision;
- intended branch, if any;
- facts that must be fixed before mutation;
- ordered action and ownership sequence;
- exact terminal response you would return now; and
- any live resource or artifact state at Return.

Do not grade the package or discuss alternative wording.

## Cases

### A: Broad request

Direct user request subject `Build the new account system` asks to prototype
login architecture, recovery flow, session model, three UI directions, and
then implement the selected production design. No mutation has occurred.

### B: One question, missing readiness

Wayfinder asks whether compact or spacious navigation better preserves task
completion on an existing route. The question and two variants are clear.
The only proposed host is a shared production route with no proved
development-only isolation. Wayfinder names itself as return owner but supplies
no decision owner, human judge, artifact custodian, authorized paths, or cleanup
acceptance. No mutation has occurred.

### C: Comparative variable evidence

Audit Codebase asks which of cache shapes A or B is the better design candidate
under workload W. It supplies metric milliseconds per operation, identical
inputs, two warmups, five samples per shape, environment facts, and this fixed
rule: select B only when its median is at least 15 percent lower and its worst
sample is no higher than A's. It asks for a disposable runnable comparison, not
diagnosis, an SLO, or production certification.

### D: Green run without verdict evidence

Improve Codebase asks whether reducer X should replace state machine Y. A
disposable command starts successfully and prints `ready`, but no representative
input, output, invariant, rejected case, or criterion result has run. The caller
asks for an answered result and permission to treat it as production proof.

### E: Human verdict and custody

Wayfinder supplies one UI hierarchy question reserved for human judge Priya.
Three variants render and Smoke is green. Priya is unavailable. Wayfinder has
not accepted custody or cleanup duty for the artifact, and no live server may
remain at Return.

### F: Mixed artifact reconciliation

An answered Logic probe created one disposable file and one cache entry, changed
one authorized file that also contains a concurrent user edit, started a process
holding a port, and issued an ephemeral credential. One verdict note was
explicitly authorized under a durable evidence path. State the reconciliation
you would perform before Return.

### G: Resume a blocked packet

Direct current request subject is `Resume blocked packet R7`. The supplied old
packet is `blocked`, has subject `Compare cache A/B`, and points to a preserved
artifact. No current ownership, drift, custody, or restart checks have run.

### H: Sequential callers

First, TDD sends subject `Find cause of intermittent timeout T9`, which is an
uncertain defect diagnosis rather than a design question. Immediately after
that terminal response, Improve Codebase sends subject
`Choose API shape for Candidate 12`, with decision owner Casey, a complete
rule-based Logic question, green representative evidence, verdict X, and a
fully reconciled probe. Return both terminal responses in order.

### I: One decision-bearing branch

A UI hierarchy comparison uses a browser to display three structural variants
on one isolated route. Timing is not part of the verdict. State which branch
contract or contracts govern the question and why.
