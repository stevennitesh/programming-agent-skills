# Experimental Skills

This directory preserves inactive alternatives to skills in `../custom/`.

`skills/custom/` is the only active source for routing, validation, managed installation, and installed-mirror comparison. An experimental skill may use the same name as its active counterpart, but it is never loaded or installed by the pack. Git history and [`manifest.json`](manifest.json) preserve why each candidate exists and the exact candidate and active-baseline tree hashes.

## Lifecycle Owner

[`docs/synthesis/methods/deploy-prompts.md`](../../docs/synthesis/methods/deploy-prompts.md)
owns experimental creation, evaluation, promotion, lifecycle cleanup, and the
separately owned installation continuation:

- Deploy Prompt 3 creates and mechanically proves one inactive candidate.
- Deploy Prompt 4 audits, repairs, behaviorally evaluates, and accepts or
  rejects that candidate.
- Deploy Prompt 5 promotes only an accepted candidate, proves canonical source,
  removes only that promoted experimental tree and manifest entry, then resumes
  the separately owned managed-install continuation.

Experimental edits keep `candidate_sha256` current, and experimental tests name
the experimental path explicitly. Abandoned candidates remain inactive until a
separately authorized retirement moves their history to `skills/.archive/` and
removes their manifest entry.

Never copy an experimental tree into the installed directory directly. The transactional installer reads only `skills/custom/`.
