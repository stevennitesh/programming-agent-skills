# Decision Mapping Skill Synthesis

This note maps the books and supporting references behind the local `$decision-mapping` skill:

- `/home/steve/code/programming-agent-skills/skills/current/decision-mapping/SKILL.md`

The local skill-pack stance is: when an idea has too much fog of war for a PRD or implementation plan, create a compact git-tracked decision map, identify the current frontier, and resolve one investigation ticket per session through research, prototype, or grilling.

## Primary Sources

### Annie Duke - How to Decide

Source: https://www.annieduke.com/books/

Use for:

- decision quality under uncertainty
- slowing down only the decisions that deserve it
- separating decision process from outcome quality
- identifying what information would change the choice

Maps to:

- `decision-mapping/SKILL.md`: loose ideas with too much fog of war
- `decision-mapping/SKILL.md`: ticket questions that block a clear implementation path
- `decision-mapping/SKILL.md`: resolving or blocking exactly one decision at a time

Skill-pack takeaway:

Decision mapping should improve the decision process, not guarantee a good outcome. A good ticket states the decision clearly enough that the answer can change what happens next.

### Douglas Hubbard - How to Measure Anything

Source: https://hubbardresearch.com/shop/measure-anything-3-ed-signed-author/

Use for:

- uncertainty reduction
- value of information
- measuring seemingly fuzzy questions
- deciding when more research is worth doing

Maps to:

- `decision-mapping/SKILL.md`: Research ticket type
- `decision-mapping/SKILL.md`: choosing the smallest follow-up ticket that unblocks progress
- `decision-mapping/SKILL.md`: stopping when the path to implementation is clear

Skill-pack takeaway:

Research tickets should not become open-ended learning. They should reduce uncertainty that matters to the next decision.

### Richard Rumelt - The Crux

Source: https://www.publicaffairsbooks.com/titles/richard-p-rumelt/the-crux/9781541701267/

Use for:

- finding the pivotal challenge
- focusing on constraints that matter
- avoiding goal lists that do not identify the hard part
- choosing the next decisive obstacle

Maps to:

- `decision-mapping/SKILL.md`: the frontier of unblocked pending tickets
- `decision-mapping/SKILL.md`: resolving one frontier ticket per session
- `decision-mapping/SKILL.md`: adding only directly affected dependency edges

Skill-pack takeaway:

The frontier is the current crux of the idea. Do not map every possible question; map the questions whose answers unlock the next useful move.

### Teresa Torres - Continuous Discovery Habits

Source: https://www.producttalk.org/continuous-discovery-habits/

Use for:

- discovery as a continuous habit
- starting from an outcome
- interviewing to discover opportunities
- assumption testing before committing to a solution

Maps to:

- `decision-mapping/SKILL.md`: Grilling ticket type
- `decision-mapping/SKILL.md`: using `$grilling` and `$domain-modeling` to resolve decisions through conversation
- `decision-mapping/SKILL.md`: updating the map as newly discovered tickets appear

Skill-pack takeaway:

Decision maps are discovery artifacts. They should keep learning tied to the outcome and turn newly discovered assumptions into explicit tickets instead of letting them leak into implementation.

### Jake Knapp, John Zeratsky, and Braden Kowitz - Sprint

Source: https://jakeknapp.com/sprint

Use for:

- answering critical questions with a time-boxed prototype
- deciding when conversation is not enough
- learning from realistic artifacts before building production code
- keeping the test of an idea small

Maps to:

- `decision-mapping/SKILL.md`: Prototype ticket type
- `decision-mapping/SKILL.md`: linking prototype assets instead of duplicating them in the map
- `decision-mapping/SKILL.md`: resolving one runnable hypothesis before implementation

Skill-pack takeaway:

Prototype tickets should answer a decision question. The prototype is not the product; the durable output is the answer linked from the map.

### Alberto Savoia - The Right It

Source: https://www.albertosavoia.com/therightit.html

Use for:

- testing whether an idea is worth pursuing
- collecting evidence before heavy investment
- pretotyping and market engagement hypotheses
- avoiding fake certainty from internal discussion

Maps to:

- `decision-mapping/SKILL.md`: Prototype ticket type
- `decision-mapping/SKILL.md`: Research ticket type
- `decision-mapping/SKILL.md`: blocking a ticket when outside evidence is required

Skill-pack takeaway:

Some decisions need evidence from outside the repo or conversation. When that evidence is missing, mark the ticket blocked and name the smallest artifact needed to unblock it.

### Jeff Patton - User Story Mapping

Source: https://jpattonassociates.com/story-mapping/

Use for:

- keeping the whole story visible
- turning a flat backlog into a map
- preserving shared understanding while slicing work
- separating the map from the implementation issues

Maps to:

- `decision-mapping/SKILL.md`: compact decision map file
- `decision-mapping/SKILL.md`: assets linked from the map, not duplicated inside it
- `decision-mapping/SKILL.md`: handoff to `$to-prd` or `$implement` when the map is done

Skill-pack takeaway:

The decision map is not a backlog. It is a visible structure for unresolved questions that keeps the whole idea coherent while the frontier moves.

### Donald Reinertsen - The Principles of Product Development Flow

Source: https://www.amazon.com/Principles-Product-Development-Flow-Generation/dp/1935401009

Use for:

- small batch size
- limiting work in progress
- accelerating feedback
- managing work under variability
- decentralizing control through clear queues

Maps to:

- `decision-mapping/SKILL.md`: one ticket sized to one Codex session
- `decision-mapping/SKILL.md`: only one frontier ticket resumed per session
- `decision-mapping/SKILL.md`: preserving other sessions' updates during parallel work

Skill-pack takeaway:

Decision mapping keeps uncertainty work in small batches. One frontier ticket per session protects flow and prevents a map from turning into a sprawling planning phase.

## Supporting References

### Eric Ries - The Lean Startup

Source: https://theleanstartup.com/principles

Use for:

- validated learning
- testing a vision continuously
- experiments as progress under uncertainty

Maps to:

- `decision-mapping/SKILL.md`: Research and Prototype ticket types

Skill-pack takeaway:

Progress in fog-of-war work is validated learning: a ticket is useful when it changes what the team believes or does next.

### David J. Anderson - Kanban

Source: https://shop.leankanban.com/products/kanban-successful-evolutionary-change-for-your-technology-business-print

Use for:

- visualizing work
- limiting work in progress
- recognizing improvement opportunities
- improving flow without replacing the whole process

Maps to:

- `decision-mapping/SKILL.md`: `Pending`, `In Progress`, `Resolved`, and `Blocked` statuses
- `decision-mapping/SKILL.md`: preserving parallel session updates

Skill-pack takeaway:

Statuses are not ceremony. They make the frontier visible and protect the map from concurrent sessions stepping on each other.

## Concept Map By File

### `decision-mapping/SKILL.md`

Primary concepts:

- fog of war before PRD or implementation
- compact git-tracked decision map
- one ticket sized to one Codex session
- Research, Prototype, and Grilling ticket types
- frontier: `Pending` tickets whose blockers are `Resolved`
- resolve or block one frontier ticket per session
- link assets instead of duplicating them
- stop when the path to implementation is clear

Best sources:

- Duke for decision quality under uncertainty
- Hubbard for uncertainty reduction and value of information
- Rumelt for finding the crux/frontier
- Torres for discovery habits and assumption testing
- Sprint and Savoia for prototype evidence before commitment
- Patton for maps that preserve shared understanding
- Reinertsen and Kanban for small batches, WIP, and flow

## Practical North Star

The skill is in the right direction when it produces decision maps that:

- name the unresolved questions blocking implementation
- keep each ticket small enough for one session
- identify the current frontier
- resolve one question with research, prototype, or grilling
- mark blocked tickets honestly instead of guessing
- link evidence assets instead of copying them into the map
- add dependency edges only when they clarify the next move
- stop planning when the path to PRD or implementation is clear

The goal is not a perfect plan. The goal is to push back the fog of war until the next implementation artifact is obvious.
