# Global Codex Instructions

## Delegation

Delegate only when the user asks directly or an applicable `AGENTS.md` or
invoked skill explicitly requires fanout. Delegate only concrete, bounded,
independent work. Keep the final decision, synthesis, integration, and
verification with the root.

## Skill Pack Bootstrap

Repo-local `AGENTS.md` primes. `docs/agents/*` teaches. Skills execute.

- **Route:** Suggest `$skill-router` only when choosing one next skill is the task; it returns one exact route or truthful none, then stops.
- **Setup:** Suggest `$repo-bootstrap` when a chosen engineering route needs a missing or outdated repo setup surface.
- **Boundary:** Leave route maps, procedures, tracker policy, domain rules, and engineering discipline to their owners.
