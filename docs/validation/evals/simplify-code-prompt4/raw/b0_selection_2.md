# Simplify Code decision

- **Mode and region:** One-cut, read-only decision for `src/request_parser.py`.
- **Selected cut:** A — delete the unreachable v1 branch and remove `legacy_parse`.

## Reasoning

Compatibility begins at v3, and repository-wide caller, configuration, and
entry-point evidence proves that no v1 path remains. The caller-facing fixture
distinguishes the supported outputs, so the obsolete branch can be removed
without weakening the observable proof seam. This cut needs no dependency,
interface, contract, ownership, feature, or bug decision.

B is a credible later simplification, but one-cut mode stops after selecting A.
C is not selected because reducing a loop from nine lines to four leaves the
larger branch and duplication obligations intact and establishes no behavioral
or ownership improvement.

## Proof

- **Before:** The fixed starting packet establishes v3+ compatibility, no v1
  callers or activation paths, and a caller-facing fixture that distinguishes
  outputs.
- **After:** With the v1 branch and `legacy_parse` removed, the same fixture
  passes.
- **Preserved contract:** All supported v3+ caller-visible outputs remain
  unchanged; only an unreachable compatibility path is removed.

## Obligation ledger

- Removed: one obsolete compatibility branch family.
- Removed: one legacy parsing helper and its maintenance surface.
- Introduced: none.
- Net: strict reduction of two maintenance obligations, with no burden
  transferred to another dependency, interface, or owner.

## State preservation

This was a read-only production-code decision: no source cut was applied.
`docs/notes.md` remains as unrelated dirty work, and staged
`assets/logo.bin` remains staged and untouched. The index, dependencies,
installed state, and external state are unchanged. The only written path is
this decision record.

## Stop and residual

Stop because the requested one-cut selection is complete and implementation
was outside the read-only scope. Applying A is the residual for a separately
authorized code-changing run. B remains a bounded future candidate; C remains
unselected.
