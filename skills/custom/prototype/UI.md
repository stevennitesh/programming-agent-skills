# UI prototype

Use this branch for one question about visual hierarchy, information density,
navigation, flow, or interaction. [SKILL.md](SKILL.md) owns authority, cleanup,
and Return.

Judge the design under real constraints. Use an existing route and its data,
parameters, auth, navigation, and surrounding layout only when authorized and
proved development-only. Otherwise use an isolated host. Omitting links does
not prove production isolation.

Build one representative UI when the question tests one direction. When the
question compares an open design choice with several credible directions,
build two or three structurally different variants under the same purpose,
data, and constraints. Color, copy, spacing, or icon changes count only when
that property is the question.

Use the repository's component and styling system when it helps the probe
match its real context. Keep effects fake or stubbed. For several variants,
give each a clear label and one direct switching mechanism; add URL or reload
persistence only when sharing or navigation affects the judgment.

Inspect the result in the actual browser or target UI at the sizes and
interactions that can change the answer. Source inspection is not UI evidence.
Use the named human's feedback for taste or feel, or apply the objective rule
chosen before the run.
