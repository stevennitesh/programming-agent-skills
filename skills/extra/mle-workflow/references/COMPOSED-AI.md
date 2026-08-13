# Hosted and Composed AI Branches

Read this file only when the in-scope slice uses instruction-following
generative behavior with untrusted supplied context, a hosted or
provider-controlled model, retrieval or external context construction, durable
memory, a model-based grader that influences a decision, or a model-driven tool
or actuator. Execute
every matching section and no others. `OPERATE.md` owns live service
transitions; `RISK-BRANCHES.md` adds exposure-specific controls.

## Bind behavior identity and invalidation

Record only components that exist: provider, endpoint or deployment and region
when behavior depends on it; advertised alias and resolved model/version or
as-of time; adaptation; system and developer instructions and prompt/template
identity; input, output, response, and tool schemas; decoding; safety and policy
configuration; routers and fallbacks; retrieval/index and memory state;
dependencies; and runtime.

Bind requests, evaluations, caches, releases, telemetry, rollback, and incident
evidence to that identity. A mutable alias or provider acknowledgement does not
establish an immutable implementation.

Before reusing evidence, declare which provider, model, prompt, policy, schema,
router, retrieval, memory, or runtime changes invalidate behavioral
equivalence, evaluation comparability, cache or replay results, or rollback
confidence. If resolved provider identity is unavailable, preserve permitted
request, response, and provider metadata, mark identity `unresolved`, and block
only exact-replay, unchanged-behavior, regression, or promotion claims that
depend on it.

## Contract retrieval, context, and durable memory

Record the corpus or source snapshot and authorization policy; parser and
chunker; embedding model; index build and configuration; query rewrite;
retrieval, filtering, reranking, and thresholds; context ordering and
truncation; and citation mapping.

Before results, define the answerable question class, sufficient and fresh
source support, conflict behavior, citation granularity, and abstention output.
Evaluate retrieval and generation separately and then end to end. A supported
answer requires each load-bearing claim to resolve to authorized evidence. When
evidence is missing, stale, contradictory, or insufficient, narrow the answer,
surface the conflict, or abstain; never silently choose or fabricate support.
Block only the dependent answer or claim.

Treat durable memory as persistent data, not as ordinary conversation context.
For each memory class, define owner and subject, purpose, readers, writers, and
deleters, tenant or user access control, source provenance and time, permitted
derivation, expiry and retention, correction and deletion propagation through
indexes, caches, and backups, and the restore or rebuild path. Reauthorize reads
after identity or access changes.

Exclude unauthorized, expired, deleted, or provenance-unknown state. If
deletion cannot be read back, report it incomplete and stop claiming deletion.
If restore cannot preserve ownership, access control, and provenance, keep the
memory unavailable and recover before resuming automated writes.

## Treat model graders as decision proxies

Apply the common Evaluation Contract. Freeze the property and population being
judged; rubric; grader provider, model, and version; prompt; response schema;
candidate ordering; decoding; aggregation; and invalid-output policy.

Validate the grader for that property, population, and decision against an
independent human, domain, or mechanical oracle. Test relevant ordering,
verbosity, self-preference, subgroup, and perturbation sensitivity rather than
assuming general validity. Revalidate after an identity or rubric change that
crosses the declared invalidation boundary.

An invalid, unvalidated, or out-of-scope grader result is `unknown`, not a
failed candidate or ground truth. Block only the dependent gate or claim and
preserve independently supported evidence.

## Contract tool-agent state and effects

Define:

```text
Initial world, conversation, and task state:
Caller, agent, and tool identities and permissions:
Allowed tools and actions and required milestones:
Confirmation owner, timing, and exact effect:
Forbidden actions and forbidden intermediate or final states:
Insufficient-information condition and clarification:
Success and final-state invariant:
Retry, idempotency, reconciliation, rollback, or compensation:
```

Evaluate the trajectory when required or forbidden actions matter; a correct
final state does not erase a forbidden intermediate effect. Bind confirmation
to the exact action and current state immediately before the effect.

Exercise forbidden and unsafe trajectories through a project-native
intercepted, dry-run, sandboxed, or otherwise zero-real-effect seam. Read the
authoritative target state and prove it remained unchanged. Exercise a real
allowed effect only with explicit authority, bounded scope, and reconciliation.

Without required information, authority, or confirmation, clarify or return
without attempting the effect. After a timeout or uncertain outcome, read
authoritative state before retry. Retry when idempotency or deduplication
protects the effect, or when reconciliation establishes that a new attempt is
safe. Otherwise contain and reconcile. A partial or uncertain final
state is not complete.

## Prove instruction and data trust flow

Execute this section when user-controlled text or untrusted retrieved, memory,
tool, or provider content can be interpreted as instructions or authority,
crosses an instruction/data channel, constructs model-driven tool arguments or
effects, or can influence disclosure of protected context. Ordinary
non-instruction classification remains under adversarial-input controls.

Trace which inputs are authoritative instructions and which are untrusted data
through prompt construction, retrieval, memory, tool results, model output,
tool arguments, and effects. Test direct injection in user-controlled input and
indirect injection embedded in retrieved resources, memory, and tool output.
Show that untrusted content cannot expand authority, disclose protected
context, or cause a forbidden effect while representative benign use still
works.

When the trust flow cannot be isolated, treat untrusted text as data, disable
or suppress the affected context construction, retrieval, sensitive-output,
tool, or effect path, require abstention or zero protected disclosure, and
block only the dependent action or safety claim.

## Evaluate human oversight as a system control

Execute this section only when human review, confirmation, intervention,
override, appeal, or deactivation is load-bearing to a gate or safety claim.

Define its trigger, timing, reviewer authority and relevant competence,
information shown, workload and response window, action, override or appeal,
logging, and fallback. Exercise representative allow, stop, error, and
unavailable-reviewer cases and verify the resulting system state. A reviewer,
queue, button, or confirmation screen is structural evidence only.

If the human control is not evaluated for its claimed condition and operating
context, do not credit it as a gate. Use the safe default and block only the
dependent transition or claim.

## Measure variable inference economics

Execute this section before a routing, release, ramp, or scale decision depends
on inference economics.

Define the representative workload, quality constraint, unit volume, and
budget. Measure end-to-end quality, latency, and cost distributions across input
and output tokens, retrieval, grading, tool calls, retries, cache use, model
routing, fallback, quota, throttling, and applicable failure paths. Provider
list prices and averages alone do not establish workload economics.

When representative measurement is unavailable, narrow the claim and block
only the dependent routing, budget, ramp, or scale decision.

## Complete this branch

Complete only when the composed behavior identity and invalidation boundary
read back consistently; every activated component contract has
claim-proportionate evidence; grader and human-control claims remain calibrated
to their weakest load-bearing evidence; no forbidden or unauthorized effect is
reported successful; every uncertain effect is reconciled or returned
incomplete; and decision-bearing inference economics are measured.

Otherwise report the branch disposition, preserve independent supported
results, and name the exact component, claim, or transition that remains
blocked to the root Return owner.
