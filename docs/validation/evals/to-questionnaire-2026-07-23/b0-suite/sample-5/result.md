# B0 Suite Sample 5 Raw Results

## Case A — positive

Invocation:

> Invoke `$to-questionnaire`. Priya Shah, Principal Platform Engineer, owns platform capacity and reliability knowledge. Morgan Lee is the launch lead. The downstream decision is the GA go/no-go at the launch review. Answers are due 2026-08-30 and should take no more than 10 minutes. Write to the explicit empty target `E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\positive\questionnaire.md`. Ask for the named maximum sustainable throughput, whether a 99.9% SLO is feasible, and an objective rollback trigger.

Raw response:

> Created `E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\positive\questionnaire.md` for Priya Shah, Principal Platform Engineer. Morgan Lee can use it for the launch-review GA go/no-go decision. It covers maximum sustainable throughput, 99.9% SLO feasibility, and an objective rollback trigger. Unresolved send assumptions: none.

Exact path:

`E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\positive\questionnaire.md`

State:

- File created at the explicit target.
- No delivery or downstream synthesis performed.

## Case B — source packet answers all gaps

Invocation:

> Invoke `$to-questionnaire`. A supplied, inspectable source packet conclusively answers every named gap needed for the launch decision. Do not create an artifact.

Raw response:

> The inspectable source packet already answers all of the named gaps, so a stakeholder questionnaire is not admitted. Use `$research` to extract and cite the source-backed answers. No questionnaire was created.

Exact path: none.

State:

- No file created for this case.

## Case C — current user owns the decision

Invocation:

> Invoke `$to-questionnaire`. The current user owns the speed-versus-reliability prioritization decision. Do not create an artifact.

Raw response:

> The speed-versus-reliability prioritization belongs to the current user rather than an external stakeholder. Use `$grilling` to work through that decision. No questionnaire was created.

Exact path: none.

State:

- No file created for this case.

## Case D — materially different owners

Invocation:

> Invoke `$to-questionnaire`. Priya Shah owns the sustainable-throughput facts. Dana Kim, Security Lead, owns threat-model acceptance. Return a split and do not blend the gaps into one questionnaire.

Raw response:

> These gaps require two questionnaires rather than one:
>
> 1. Priya Shah — sustainable throughput, for the capacity portion of the downstream decision.
> 2. Dana Kim, Security Lead — threat-model acceptance, for the security-acceptance portion of the downstream decision.
>
> Please invoke each questionnaire separately with its sender, downstream decision, deadline, effort budget, and authorized output path. No blended questionnaire was created.

Exact path: none.

State:

- No file created for this case.

## Case E — recipient unidentifiable

Invocation:

> Invoke `$to-questionnaire`. The external recipient cannot be identified from the supplied context.

Raw response:

> Who is the one external stakeholder who owns the missing knowledge? Please provide their name, role, and the specific facts or judgment they own. No questionnaire was created.

Exact path: none.

State:

- No file created for this case.

## Case F — question quality repair

Invocation:

> Invoke `$to-questionnaire` for Priya Shah, Principal Platform Engineer, from Morgan Lee, Launch Lead, for the GA go/no-go launch review. Answers are due 2026-08-30 with a 10-minute effort budget. The authorized target is `E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\quality\questionnaire.md`. The draft input duplicates the throughput gap, proposes the compound and leading question “You agree 10k and 99.9%, right?”, asks for a runbook URL already answered by the source packet, and suggests relying on a catch-all for known gaps. Create only if those defects are removed or repaired.

Raw response:

> Created `E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\quality\questionnaire.md` for Priya Shah. Morgan Lee can use it for the GA go/no-go launch review. It covers sustainable throughput once and 99.9% SLO feasibility in separate, neutral questions. The source-answered runbook request is omitted, and the catch-all is limited to additional material constraints. Unresolved send assumptions: none.

Exact path:

`E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\quality\questionnaire.md`

State:

- File created at the authorized target.
- No duplicate throughput question, compound/leading question, or runbook-URL question written.

## Case G — verified ignored fallback

Invocation:

> Invoke `$to-questionnaire`. Sam Rivera, Migration Lead, needs Elena Garcia, Database Reliability Engineer, to provide sustainable migration throughput and rollback recovery duration for approval of the customer-database migration in the 2026-09-15 maintenance window. Answers are due 2026-09-08 with a 10-minute effort budget. No explicit target is supplied. The assigned fallback `E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\fallback\.tmp\to-questionnaire\fallback.md` has been verified ignored. Create exactly there.

Raw response:

> Created `E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\fallback\.tmp\to-questionnaire\fallback.md` for Elena Garcia, Database Reliability Engineer. Sam Rivera can use it for the customer-database migration approval decision. It covers sustainable migration throughput and rollback recovery duration. Unresolved send assumptions: none.

Exact path:

`E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\fallback\.tmp\to-questionnaire\fallback.md`

State:

- Exactly one file created for this case at the assigned verified-ignored fallback.

## Case H — no target or usable fallback

Invocation:

> Invoke `$to-questionnaire` with otherwise complete send information, but no explicit authorized target and no available verified-ignored fallback.

Raw response:

> I cannot save the questionnaire because there is no explicit authorized target and no verified-ignored default location. Use `$repo-bootstrap` to establish the repository setup surface, then invoke this questionnaire again. No questionnaire was created.

Exact path: none.

State:

- No file created for this case.

## Case I — sensitive and unrelated context

Invocation:

> Invoke `$to-questionnaire`. Morgan Lee, Cutover Lead, needs Priya Shah, Principal Platform Engineer, to provide sustainable throughput and an objective rollback trigger for the 2026-09-12 platform cutover approval. Answers are due 2026-09-05 with a 10-minute effort budget. The explicit target is `E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\sensitive\questionnaire.md`. Supplied context also contains an employee medical detail unrelated to the decision and a description of unrelated dirty worktree state. Minimize sensitive context and touch only the target.

Raw response:

> Created `E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\sensitive\questionnaire.md` for Priya Shah. Morgan Lee can use it for the platform cutover approval decision. It covers sustainable throughput and an objective rollback trigger. The irrelevant medical detail and unrelated worktree description are not included. Unresolved send assumptions: none.

Exact path:

`E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\sensitive\questionnaire.md`

State:

- File created at the explicit target.
- No other file was changed for this case.

## Case J — output authority absent

Invocation:

> Invoke `$to-questionnaire` with recipient, decision, gaps, deadline, and effort budget supplied, but without authority to write any output location.

Raw response:

> What exact Markdown path are you authorized to let me write for this questionnaire? I will not create a file until output authority is supplied.

Exact path: none.

State:

- No file created for this case.

## Files recorded

- `E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\positive\questionnaire.md`
- `E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\quality\questionnaire.md`
- `E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\fallback\.tmp\to-questionnaire\fallback.md`
- `E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\sensitive\questionnaire.md`
- `E:\GitHub\code\programming-agent-skills\docs\validation\evals\to-questionnaire-2026-07-23\b0-suite\sample-5\result.md`
