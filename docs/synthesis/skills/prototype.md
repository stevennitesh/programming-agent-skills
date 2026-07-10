# Prototype Skill Synthesis

This note maps the books and supporting references behind the local `$prototype` skill and its supporting files:

- `skills/custom/prototype/SKILL.md`
- `skills/custom/prototype/LOGIC.md`
- `skills/custom/prototype/UI.md`

The local skill-pack stance is: a prototype is throwaway code that answers one design question. The question decides the branch: a tiny terminal app for state, business logic, data shape, or interface feel; or structurally different UI variants on one route for visual and interaction decisions. The durable output is the captured answer, not the prototype code.

## Primary Sources

### Jake Knapp, John Zeratsky, and Braden Kowitz - Sprint

Source: https://jakeknapp.com/sprint

Use for:

- answering critical questions with a realistic prototype
- time-boxing prototype work
- testing before building production code
- treating a prototype as a learning device

Maps to:

- `prototype/SKILL.md`: throwaway code that answers a question
- `prototype/SKILL.md`: detour, not implementation
- `prototype/UI.md`: variants that make a design choice visible

Skill-pack takeaway:

A prototype should answer the risky question quickly. It should feel real enough to learn from, but it should not quietly become the product.

### Alberto Savoia - The Right It

Source: https://www.albertosavoia.com/therightit.html

Use for:

- testing an idea before investing heavily
- pretotyping
- market engagement hypotheses
- collecting evidence instead of relying on internal certainty

Maps to:

- `prototype/SKILL.md`: build the smallest answering artifact
- `prototype/SKILL.md`: capture what the prototype proved or disproved
- `prototype/SKILL.md`: delete the prototype or use the validated decision as input to real implementation

Skill-pack takeaway:

The prototype's job is not to look impressive. Its job is to test whether the idea or direction deserves the next investment.

### Eric Ries - The Lean Startup

Source: https://theleanstartup.com/principles

Use for:

- validated learning
- experiments as progress under uncertainty
- build-measure-learn thinking
- avoiding waste from building untested assumptions

Maps to:

- `prototype/SKILL.md`: durable output is the answer
- `prototype/SKILL.md`: state the question first
- `prototype/SKILL.md`: run once and capture the verdict

Skill-pack takeaway:

Prototype progress is validated learning. If the prototype does not produce a clearer answer, chosen direction, or next question, it did not complete its job.

### Todd Zaki Warfel - Prototyping: A Practitioner's Guide

Source: https://books.google.com/books/about/Prototyping.html?id=aieWBrFeRtUC

Use for:

- prototypes as communication
- testing assumptions
- gathering real-time feedback
- choosing prototype fidelity based on the question

Maps to:

- `prototype/SKILL.md`: the question decides the shape
- `prototype/SKILL.md`: use one repo-native command
- `prototype/SKILL.md`: skip production polish
- `prototype/UI.md`: make the active variant obvious and reload-stable

Skill-pack takeaway:

Prototype fidelity should be just high enough to answer the question. Anything beyond that is polish unless it changes the evidence.

### Bill Buxton - Sketching User Experiences

Source: https://shop.elsevier.com/books/sketching-user-experiences-getting-the-design-right-and-the-right-design/buxton/978-0-12-374037-3

Use for:

- exploring several alternatives before committing
- sketching as a design thinking tool
- making interaction and experience tangible
- keeping early artifacts provisional

Maps to:

- `prototype/UI.md`: default to three structurally different variants
- `prototype/UI.md`: variants should represent different bets
- `prototype/UI.md`: do not force variants through one shared layout

Skill-pack takeaway:

Good UI prototypes preserve possibility. Several genuinely different variants teach more than one polished version.

### Carolyn Snyder - Paper Prototyping

Source: https://shop.elsevier.com/books/paper-prototyping/snyder/978-1-55860-870-2

Use for:

- fast UI design and refinement
- testing interaction flow before implementation
- arguing less by making behavior observable
- learning from low-fidelity interfaces

Maps to:

- `prototype/UI.md`: answer "what should this look like?" by seeing and comparing real UI
- `prototype/UI.md`: avoid evaluating UI from imagination alone
- `prototype/UI.md`: variants should expose layout, hierarchy, density, and flow trade-offs

Skill-pack takeaway:

The point of a UI prototype is to make interaction visible enough to judge. Low fidelity is fine when it exposes the right trade-off.

### Jeff Gothelf and Josh Seiden - Lean UX

Source: https://jeffgothelf.com/books/

Use for:

- product discovery through short cycles
- focusing on outcomes over deliverables
- validating design ideas with users or realistic feedback
- reducing deliverable-heavy design waste

Maps to:

- `prototype/SKILL.md`: this is a detour, not implementation
- `prototype/SKILL.md`: capture the answer in the smallest durable place that fits
- `prototype/UI.md`: use the page's real purpose and available data

Skill-pack takeaway:

Do not make the prototype a deliverable factory. Use it to learn, then carry the answer back into the real flow.

### Scott Wlaschin - Domain Modeling Made Functional

Source: https://pragprog.com/titles/swdddf/domain-modeling-made-functional/

Use for:

- modeling real-world requirements with small domain types
- explicit state and workflow modeling
- pure functions and data transformations
- using domain language to shape the model

Maps to:

- `prototype/LOGIC.md`: put logic behind a small, pure interface
- `prototype/LOGIC.md`: model only the states, actions, and data needed
- `prototype/LOGIC.md`: reducer, state machine, pure functions, or module with a clear interface
- `prototype/SKILL.md`: update domain language with `$domain-modeling` when the answer resolves terms

Skill-pack takeaway:

Logic prototypes should make the domain model tangible. Keep the decision surface pure so the terminal shell can change without changing the model.

### Alan Cooper, Robert Reimann, David Cronin, and Christopher Noessel - About Face

Source: https://www.wiley.com/en-us/About%2BFace%3A%2BThe%2BEssentials%2Bof%2BInteraction%2BDesign%2C%2B4th%2BEdition-p-9781118766576

Use for:

- interaction design concepts
- goal-directed design
- matching interface behavior to user intent
- evaluating flows by user-visible behavior

Maps to:

- `prototype/UI.md`: use real surrounding app context
- `prototype/UI.md`: compare navigation or flow shape
- `prototype/UI.md`: avoid variants that differ only by color, copy, spacing, or icons

Skill-pack takeaway:

UI variants should differ in interaction model or information hierarchy, not decoration. The best comparison changes what the user can understand or do.

## Supporting References

### Teresa Torres - Continuous Discovery Habits

Source: https://www.producttalk.org/continuous-discovery-habits/

Use for:

- assumption testing
- continuous discovery
- outcome-oriented learning
- deciding what evidence is needed next

Maps to:

- `prototype/SKILL.md`: state the question first
- `prototype/SKILL.md`: capture what was proved or disproved

Skill-pack takeaway:

A prototype question should be an assumption worth testing, not a vague request to explore.

### Bill Moggridge - Designing Interactions

Source: https://mitpress.mit.edu/9780262134743/designing-interactions/

Use for:

- interaction design case studies
- understanding design through working artifacts
- connecting interface form to behavior

Maps to:

- `prototype/UI.md`: compare flow shape and primary affordance
- `prototype/UI.md`: judge prototypes in real context

Skill-pack takeaway:

Interaction design is learned by experiencing behavior, not just by reading a static description of layout.

## Concept Map By File

### `prototype/SKILL.md`

Primary concepts:

- throwaway code that answers a question
- the question decides the branch
- detour, not implementation
- smallest answering artifact
- one command
- run it once
- capture the answer durably
- delete, hand off, or treat the answer as input to real implementation

Best sources:

- Sprint for realistic, time-boxed prototype evidence
- Savoia for pretotyping and smallest evidence before investment
- Lean Startup for validated learning
- Warfel for prototype fidelity and assumption testing

### `prototype/LOGIC.md`

Primary concepts:

- state, actions, and data as the decision surface
- tiny terminal app to drive the model
- pure logic behind a small interface
- reducer, state machine, pure functions, or module shape
- current state and available actions visible in each frame
- illegal actions surfaced enough to learn from

Best sources:

- Wlaschin for domain modeling, pure functions, and explicit workflows
- Sprint for making a model feel real enough to judge
- Warfel for matching prototype fidelity to the question

### `prototype/UI.md`

Primary concepts:

- use an existing route when possible
- compare structurally different variants
- preserve app context, real data, and surrounding constraints
- switch variants through URL state
- make prototype chrome obvious
- visually check the route and variants
- do not ship prototype UI as production

Best sources:

- Buxton for sketching multiple alternatives
- Snyder for low-fidelity UI testing and refinement
- Lean UX for short discovery cycles and outcome focus
- About Face for interaction behavior and flow

## Practical North Star

The skill is in the right direction when it produces prototypes that:

- state one question before building
- use the smallest artifact that can answer it
- run with one repo-native command
- make state, variant, or interaction visible enough to judge
- avoid production persistence and real mutations by default
- keep prototype code clearly throwaway
- capture the answer in a durable place
- hand the answer back to the design or implementation flow

The goal is not a polished demo. The goal is to turn a design question into evidence.
