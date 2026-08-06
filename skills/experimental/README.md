# Experimental Skills

This directory preserves inactive alternatives to skills in `../custom/`.

`skills/custom/` is the only active source for routing, validation, managed installation, and installed-mirror comparison. An experimental skill may use the same name as its active counterpart, but it is never loaded or installed by the pack. Git history and [`manifest.json`](manifest.json) preserve why each candidate exists and the exact candidate and active-baseline tree hashes.

## Lifecycle Owner

[`docs/synthesis/methods/deploy-prompts.md`](../../docs/synthesis/methods/deploy-prompts.md)
owns experimental creation, evaluation, promotion, lifecycle cleanup, and the
separately owned installation continuation:

- Contract Lock binds the intended behavior and applicable proof.
- Candidate Lock freezes one inactive candidate and proves its deterministic
  caller and integration seams.
- Behavioral Proof runs conditionally for wording-effect claims.
- Release promotes only the exact proved candidate, removes only that promoted
  experimental tree and manifest entry, and stops before any separately owned
  managed-install continuation.

Experimental edits keep `candidate_sha256` current, and experimental tests name
the experimental path explicitly. Abandoned candidates remain inactive until a
separately authorized retirement moves their history to `skills/.archive/` and
removes their manifest entry.

Never copy an experimental tree into the installed directory directly. The transactional installer reads only `skills/custom/`.
