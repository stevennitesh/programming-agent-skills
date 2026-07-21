# Experimental Skills

This directory preserves inactive alternatives to skills in `../custom/`.

`skills/custom/` is the only active source for routing, validation, managed installation, and installed-mirror comparison. An experimental skill may use the same name as its active counterpart, but it is never loaded or installed by the pack. Git history and [`manifest.json`](manifest.json) preserve why each candidate exists and the exact candidate and active-baseline tree hashes.

## Lifecycle

- **Capture:** move the complete candidate tree from `skills/custom/<name>/` here, record its identity in the manifest, then restore or create the active custom tree.
- **Develop:** edit the experimental tree and update its `candidate_sha256` in the same change. Experimental tests must name the experimental path explicitly.
- **Promote:** replace `skills/custom/<name>/` only after the candidate's behavior and compatibility are accepted; validate canonical source before synchronizing the installed mirror.
- **Retire:** move abandoned history to `skills/.archive/` and remove its manifest entry in the same change.

Never copy an experimental tree into the installed directory directly. The transactional installer reads only `skills/custom/`.
