# MV-AUTHOR-01

Disposition: `complete`  
Selected operation: `Author`

The authorized mutation is limited to the fictional canonical `SKILL.md`
(`W-F1`, `W-F4`). The replacement below implements the stated trigger and
exclusions (`W-F2`, `W-F3`), the required execution and Return behavior
(`W-F5`), and removes the duplicated history, unowned installation action,
and vague completion language described in `W-F7`.

## Proposed complete `SKILL.md`

```markdown
---
name: acme-deployment-policy
description: Audit or edit the semantic behavior of an existing Acme deployment policy. Exclude new-package scaffolding, installation, and Git delivery.
---

# Acme Deployment Policy

## Authority

Resolve the target, canonical source, requested operation, and mutation
boundary before acting. Audit is read-only. Author may change only the
requested canonical semantic artifact. Return `blocked` if authority or a safe
mutation boundary cannot be established.

## Coverage

Inspect the canonical policy and only the callers, relationships, gates,
outputs, mutations, failure branches, completion conditions, and proof
surfaces capable of changing the requested behavior. Preserve rules and work
owned elsewhere; record their boundary without copying or performing their
procedures.

## Proof

Match proof to the claim: read back exact content for an authored mutation,
use focused structural checks for machine-readable contracts, relationship
traces for ownership, and direct controls when claiming that wording changes
behavior. Name any proof that cannot be run and limit the disposition
accordingly.

## Return

Return exactly one disposition:

- `complete` when every affected semantic surface and ownership boundary is
  classified, required behavior is decided, proportionate proof passes, and
  the exact authored content is read back.
- `partial` when useful bounded work is complete but affected coverage or
  current proof remains incomplete.
- `blocked` when the target, authority, canonical source, or mutation safety
  cannot be resolved.

Report the operation, coverage, behavior added, changed, or removed, proof,
preserved foreign state, deliberate non-changes, evidence limits, and residual
risk. Stop before installation, publication, synchronization, Git delivery,
or any other downstream mutation.
```

Coverage classification:

- `affected`: the canonical `SKILL.md` routing predicate, authority, semantic
  coverage, proof, Return, and completion behavior (`W-F1`, `W-F2`, `W-F4`,
  `W-F5`).
- `preserve`: foreign ownership and unrelated state (`W-F4`, `W-F5`).
- `owned elsewhere`: package scaffolding, installation, publication,
  synchronization, and Git delivery (`W-F3`, `W-F5`).
- `not applicable`: helper files, relationship edits, package metadata, and
  downstream mutations (`W-F6`).
- `historical evidence`: the original file's duplicated history (`W-F7`).

Proof is limited to consistency against the supplied case facts and read-back
of this disposable proposal; no real canonical artifact or behavioral control
was supplied. Residual risk is therefore transfer from this fictional
replacement to any real package. No installation, publication, Git delivery,
helper-file edit, relationship edit, metadata change, or downstream mutation
was performed. The exact stop boundary is the proposed canonical `SKILL.md`
content above.
