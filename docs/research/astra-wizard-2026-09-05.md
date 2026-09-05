# Astra Wizard rewrite

Date: 2026-09-05. Assessment record, not runtime instructions.
Candidate: [wizard](../../skills/astra/wizard/SKILL.md).

## Decision

Keep Wizard as an explicitly selected specialist for authoring a guided local
procedure that needs a human. Retain explicit-only discovery in `agents/openai.yaml`.
The default prompt requests creation/checking only; launch requires an actual
request to begin or run, and does not require a second approval merely to open
the isolated terminal. The agent must not observe the private operator session.

Use one main method plus conditional input/effect/recovery guidance. Do not ship
a universal Bash library: the right runtime, secret destination, serialization,
target identity, and read-back differ by procedure. Existing native tools should
do deterministic work; add only the helpers the generated script needs.

## Custom preservation and changes

Preserve the custom skill's human/agent boundary, settled scope, source-backed
steps, private input, target confirmation, exact secret destination, read-back,
safe retry, cancellation, dummy-only tests, and isolated visible launch.
Writing a script is not proof that its human procedure or external effect worked.
Separate explicit requests retain their own authority; no automatic install,
commit, or publication is inferred.

Replace the arbitrary minimum of two human-only stages with whether coordination
materially reduces mistakes. A simple single manual action still gets a direct
instruction. Do not require every stage to be human-only when the useful workflow
combines manual actions with deterministic local work performed by the script.

Make important traps concrete: EOF is not consent; ignored files can remain
tracked; raw string substitution may not match the consumer's parser; retries
must not duplicate uncertain effects; runtime identity may differ from the
authoring assumption; checkpoints must not contain credentials. Secret-bearing
temporary files are allowed only when an established safe persistence mechanism
requires them, protected like the destination before writing and cleaned on failure.
No incidental plaintext scratch or backup copies are allowed.

## Upstream assessment

Compared local snapshots without fetching:

| Source | Revision | Useful material and exclusions |
| --- | --- | --- |
| Matt Pocock | `3cca18b368ae95cdbdebbff572ccafa662551015` | `skills/engineering/wizard/SKILL.md` and `template.sh`: focused stages, progress, open/print instructions before prompts, URL fallback, repeatable updates. Do not copy its Bash-only framework, raw `KEY=value` serializer, implicit CLI target, swallowed input failures, unconditional complete banner, or commit/README side effects. |
| Pstack / cursor-plugins | `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | `pstack/skills/make-bot-ui/SKILL.md`: keep secret values out of chat and use a private input channel. Do not import Cursor-specific cards, credential paths, hosting, or assumptions that arbitrary hosts supply that channel. |
| Superpowers | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | No dedicated wizard found in relevant skill scan. Existing checking principles add nothing beyond syntax checks and dummy execution; do not route a settled procedure through brainstorming or implementation ceremonies. |
| Ponytail | `974d940a1c5344210874150b98ff0d2c861fab6a` | Native tools and minimal machinery already align with the rewrite. No wizard-specific procedure imported. |

## Challenge and validation

Two fresh-context read-only reviewers own separate seams: private inputs/effect
safety/custom parity, and discovery/UX/composition/upstream completeness.
Their tabletop scenarios include ignored-but-tracked secrets, quotes/newlines,
remote timeout after success, EOF at a gate, insecure terminal fallback,
creation-only versus launch requests, and missing scratch conventions.

The safety reviewer identified a lost custom rule: when no useful external
postcondition exists, leave the mutation manual and unverified. Restored it.
Both reviewers rechecked the final candidate and passed with no remaining
actionable findings. The composition reviewer confirmed creation versus launch,
fallback destinations, explicit discovery, and ownership boundaries.

Final candidate passes package validation, repository skill validation, local
links, explicit-invocation metadata checks, and both Git whitespace checks.
All 10 focused tests passed before the one conditional wording correction.
These check packaging and compatibility. Tabletop review
checks instruction interpretation; no generated production wizard, real secret,
dashboard, credentialed operation, or private terminal launch was exercised.
This is not a comparative behavior evaluation. Global installation and Git rules
are unchanged; the historical custom skill remains source evidence.
