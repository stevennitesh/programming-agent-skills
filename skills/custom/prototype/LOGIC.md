# Logic prototype

Use this branch for one question about state transitions, rules, data shape,
API shape, or interface behavior. [SKILL.md](SKILL.md) owns authority, cleanup,
and Return.

Build the smallest public decision model needed by the question. Keep
incidental I/O, prompts, timing, randomness, and rendering outside it. Make the
current state, input, action, output, and relevant invalid behavior visible.

Use a human-drivable artifact when exploration supplies the judgment. Write its
controls and state in domain language so the named judge can operate it without
knowing the implementation. Use a deterministic report when an objective rule
decides; show each representative input, observed output, and rule result.

Exercise happy, boundary, and rejected behavior only when each can change the
answer. Repeated deterministic runs should agree. Keep persistence and real
integrations out unless the question requires an isolated substitute.

The evidence is the observed behavior of the public decision model, not a
private helper.
