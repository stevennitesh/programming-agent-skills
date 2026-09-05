# Global Codex Instructions

## Delegation

Delegate only when the user asks directly or an applicable `AGENTS.md` or
invoked skill explicitly requires fanout. Delegate only concrete, bounded,
independent work. Keep the final decision, synthesis, integration, and
verification with the root.

## Skill Pack Bootstrap

Repo-local `AGENTS.md` primes. `docs/agents/*` teaches. Skills execute.

- **Route:** Use specialist skills when the task needs them. Suggest explicit-only workflows when useful; start them when the user requests them. Ordinary coding needs no skill pipeline.
- **Setup:** Suggest `$repo-bootstrap` for missing or outdated repository guidance; a missing preferred document alone does not block coding.
- **Boundary:** Leave route maps, procedures, tracker policy, domain rules, and engineering discipline to their owners.
