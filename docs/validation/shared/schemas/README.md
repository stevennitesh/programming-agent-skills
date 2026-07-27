# Shared Schemas

`docs/validation/shared/schemas` owns versioned mechanical schemas. The
deterministic registry is `registry.json`; schema versions are append-only
compatibility identities.

Research Catalog generation uses the registered Research Card, thin Catalog,
and independent problem-first packet schemas. Canonical Cards remain Markdown;
the Card schema governs their YAML frontmatter record.

`pack-composition-contract-v1.schema.json` governs the marker-bounded five-part
Pack Contract. Its schema proves shape and vocabulary only; the controller
enforces cross-ledger ownership, graph, freeze, slice, and amendment invariants.

`deploy-campaign-manifest-v2.schema.json` governs pointer-oriented Fresh
one-skill campaign ownership. Version 2 separates immutable `contract`,
owner-written `semantic`, and automation-only `mechanical` state. Historical
manifest v1 remains an exact read-only compatibility format.

`pack-integration-manifest-v1.schema.json` and
`pack-integration-result-v1.schema.json` govern exact installed-pack inputs,
ten-gate registrations, mechanical receipts and invalidations, parity, and the
evidence-only result topology. They expose no scoring, repair, acceptance,
scheduling, or Lock field.
