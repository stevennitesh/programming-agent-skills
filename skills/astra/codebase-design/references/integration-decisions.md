# Integration decisions

Read only the section that can change the design. Bring the resulting decision
back to the caller; this reference does not start implementation or an audit.

## State crosses owners or processes

Locate authoritative state and every writer that can invalidate the proposed
guarantee. Name the event that counts as acceptance or completion from the
caller's perspective. Check whether the proposed owner can enforce that promise
through the real transaction, synchronization, or remote protocol.

Walk a consequential interruption through the proposed flow. If local commit
and external acknowledgement can disagree, decide how the caller distinguishes
pending, completed, and failed work and how the system reconciles uncertainty.
Choose identity, retry, deduplication, or compensation only where the required
behavior needs them. Naming a coordinator does not create atomicity across
systems, and a retry does not establish that the first attempt had no effect.

For derived views or cached state, identify which lag is acceptable and what
must consult the authoritative owner. A convenient presentation value should
not silently become an authorization or concurrency decision.

## A dependency changes the interface

Keep domain policy separate from transport or vendor translation when they
change for different reasons. Expose what callers must control, including
meaningful errors or resource lifetime; hide configuration and representations
that belong to the dependency's owner.

Earn a seam through real variation, an external boundary, distinct ownership,
or substantial policy it hides. A single production implementation can still
justify a seam. A fake invented only to satisfy the proposed interface is not
independent evidence that the seam is useful.

Check what a substitute cannot establish. For example, an in-memory store can
exercise application policy but may not reproduce database isolation or durable
recovery. Identify a direct boundary check or prototype for the property that
actually drives the choice. Do not widen the public interface solely to make
tests convenient; keep internal test seams internal when callers do not need them.

## A contract or stored representation must change

Identify consumers that cannot move together: old clients, persisted records,
background workers, or independently deployed services. Distinguish a current
compatibility obligation from a hypothetical future one.

Choose a supported transition and describe the allowed combinations of old and
new readers/writers. Where existing records need conversion, decide when it
happens and how concurrent writers affect that transition. Include the first
usable implementation slice and how its behavior will be checked through an
ordinary caller. Name a removal condition
for any temporary compatibility path. If rollback cannot read newly written
data or undo an effect, make that limitation part of the deployment decision.
