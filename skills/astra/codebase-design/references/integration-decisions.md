# Integration decisions

Read only the section that can change the architecture decision. Return the
resulting ownership or guarantee to the calling work; this reference does not
start implementation or a broader audit.

## State crosses owners or processes

Identify authoritative state and every writer that can invalidate the required
guarantee. Define completion from the caller's perspective and check whether the
proposed owner can enforce it through the real transaction, synchronization, or
remote protocol.

When local state and external acknowledgement can disagree, define how callers
distinguish pending, completed, failed, and uncertain work and how uncertainty is
reconciled. Add identity, retry, deduplication, or compensation only when the
required behavior needs it. Naming a coordinator does not create atomicity across
systems, and retrying does not prove the first attempt had no effect.

For caches or derived views, establish acceptable lag and which decisions must
consult the authoritative owner. A convenient presentation value must not silently
become an authorization or concurrency authority.

## Access crosses a trust boundary

Identify the caller identity, protected operation or data, and the owner that
actually enforces permission. Check an allowed and forbidden case through the
real entry path; a check in a bypassable caller does not enforce the boundary.

Keep validity and authorization distinct. Resolve only the access guarantee that
affects this design rather than expanding into a general security audit.

## A dependency changes the interface

Keep domain policy separate from transport or vendor translation when they change
for different reasons. Expose the errors, resource lifetime, and controls callers
genuinely need while hiding dependency-owned representation and configuration.

A seam earns its place through real variation, an external boundary, distinct
ownership, or meaningful policy it hides. A single implementation can justify a
seam; a fake created only to satisfy the abstraction is not evidence that the
seam is useful.

Use substitutes only for properties they can establish. An in-memory substitute,
for example, may exercise application policy without proving database isolation or
durable recovery. Use a direct boundary check or prototype for the property that
actually drives the decision. Do not widen a public interface solely for testing
convenience.

## A contract or stored representation must change

Identify real consumers that cannot move atomically, such as persisted records,
old clients, background workers, or independently deployed services. Distinguish
a current compatibility obligation from hypothetical future compatibility.

Define the supported transition and any allowed old/new reader-writer
combinations. When stored data needs conversion, decide when conversion happens
and how concurrent writes affect it.

Give every temporary compatibility path a removal condition. Make rollback limits
part of the decision when newly written data or external effects cannot be safely
read or undone by the previous version.
