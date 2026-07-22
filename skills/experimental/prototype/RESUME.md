# Resume Prototype

Resume is permitted only from an `awaiting-verdict` packet. A request to Resume any other status returns `not-admitted` without inspecting or mutating its artifact: preserve the current Resume request's `request_subject`, never the rejected packet's subject; name the failed Resume fit; require fresh Admit and Freeze; confirm no mutation; and omit admitted-only question or decision fields.

For `awaiting-verdict`, start fresh and verify the question, decision, owners, claim level, judgment mode, rule, representatives, mutation boundary, bounds, artifact path, accepted custody, and repository drift. Restart from the recipe and rerun Smoke.

When checks pass, re-assume execution and reconciliation, then return to Judge in [SKILL.md](SKILL.md). A changed Freeze fact requires fresh Admit and Freeze.
