# Simplification Lens

Understand the supported flow first. Then stop at the earliest sufficient
reduction that preserves behavior, Reliability Floors, and the Proof Seam.

## Reduction Ladder

1. delete behavior proved stale or unsupported;
2. reuse the repository's existing owner;
3. use a sufficient Standard Library capability;
4. use a sufficient native platform, framework, or database capability;
5. reuse an already justified dependency;
6. concentrate duplicate policy at its narrowest current owner;
7. Deepen, merge, inline, or Collapse the current Module shape;
8. propose the smallest local reduction that holds.

Use the ladder as search order. When several options hold, choose the earliest
only when total caller, lifecycle, dependency, operational, and proof burden is
no worse. Retention is a Quality disposition, not a reduction. A shorter option
that loses an edge, compatibility path, safety rule, clarity, or proof does not
hold.

A **Known Ceiling** states a deliberate simple choice's limit; its **Revisit
Trigger** states when additional complexity becomes justified.

## Questions That Find Simplification Issues

- Does behavior, configuration, compatibility, dependency, or abstraction
  serve a current supported scenario?
- Does the repository already contain the semantic owner?
- Does a runtime or platform facility fully match the required semantics?
- Is one policy duplicated across reachable callers?
- Is a boundary pass-through after Design establishes it has no supported
  variation, substitution, ownership, or proof value?
- Can the simpler shape name a Known Ceiling and Revisit Trigger instead of
  speculative machinery?

Examples: prefer the repository's canonical `slugify` when it preserves
project-specific accent handling. Retain an O(n²) scan for proved-small input
with a measured ceiling and revisit trigger instead of speculative machinery.

Apply `QUALITY-LENS.md`'s reachability and registration proof before using
`delete`. One implementation, repeated syntax, file size, or line savings alone
does not prove a reduction.

Record the supported behavior, observed cost, existing owner or mechanism,
smallest direction, safety floors, and required proof. Do not fabricate saved
lines or dependency counts; repository-specific savings require a verified
patch or mechanical count.
