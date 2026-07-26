# Shared Schemas

`docs/validation/shared/schemas` owns versioned mechanical schemas. The
deterministic registry is `registry.json`; schema versions are append-only
compatibility identities.

Research Catalog generation uses the registered Research Card, thin Catalog,
and independent problem-first packet schemas. Canonical Cards remain Markdown;
the Card schema governs their YAML frontmatter record.
