# Fixed Simulated Tracker Contract

The configured tracker is `fixture-tracker`. A Ready-for-agent item must contain
one bounded slice, Source Trace, observable acceptance including edge/error
behavior, dependency state, proof lane, expected durable write scope,
parallel-safety judgment, scope fence, work-unit form, verification authority,
and verification evidence. The only category role is `enhancement`; apply it
only when the source packet authorizes it. The ready state is
`ready-for-agent`.

Available operations are exposed per fixture from this closed set:
`get_setup`, `get_parent`, `list_items`, `create_item`, `set_parent`,
`set_blocker`, `set_role`, `set_state`, `get_item`, `get_dependents`,
`query_correlation`, and `create_with_idempotency`. Calls not listed in the
fixture are unavailable. Each permitted mutation is appended to an operation
log. The connector returns the fixture's observations in their listed order
and never performs a real external mutation.

Creation returns a fixture ID unless the observation is `failure` or
`ambiguous`. Relationship, role, and state operations do not occur implicitly.
Read-back must use `get_item` and, where named, `get_dependents`; a create
receipt is not read-back. A blocker edge means the dependent consumes a named
predecessor outcome. Tracker order, apparent file overlap, and serial
tripwires are not blocker edges.

The worker may mutate only the fixture tracker and only when the source,
setup, coverage, readiness, graph, runtime-specific approval, and publication
gates permit it. It may not edit repository files, invoke another skill, start
implementation, dispatch workers, or contact a live provider.
