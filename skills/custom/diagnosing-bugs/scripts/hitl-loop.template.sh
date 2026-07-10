#!/usr/bin/env bash
# Human-in-the-loop reproduction loop.
# Use only when the bug cannot be reproduced by an unattended command.
#
# Copy this file under .tmp/diagnosing-bugs/<bug-slug>/, edit the repro steps below, then run the copy.
# The agent runs the script; the user follows prompts in their terminal/browser/app.
#
# Usage:
#   bash .tmp/diagnosing-bugs/<bug-slug>/hitl-loop.sh
#
# Helpers:
#   step "<instruction>"      Show an instruction and wait for Enter.
#   capture VAR "<question>"  Ask a question and store the answer in VAR.
#
# At the end, captured values are printed as KEY=VALUE for Codex to parse.

set -euo pipefail

step() {
  printf '\n>>> %s\n' "$1"
  read -r -p "    [Enter when done] " _
}

capture() {
  local var="$1" question="$2" answer
  printf '\n>>> %s\n' "$question"
  read -r -p "    > " answer
  printf -v "$var" '%s' "$answer"
}

# --- edit below ---------------------------------------------------------
# Keep this loop focused on the user's exact symptom.
# If the bug is flaky, run the repro action multiple times and capture the rate.

capture BUG_SUMMARY "In one sentence, what exact symptom are we trying to reproduce?"

capture EXPECTED "What should happen?"

step "Prepare the app, page, command, account, fixture, or environment needed for the repro."

step "Perform the smallest action sequence that should trigger the symptom."

capture ACTUAL "What actually happened?"

capture SYMPTOM_REPRODUCED "Did the exact symptom reproduce? (y/n)"

capture REPRODUCED_COUNT "If flaky or repeated, how many runs reproduced it? Use 0/1 for a single run."

capture TOTAL_RUNS "How many total runs did you try? Use 1 for a single run."

capture NOTES "Any relevant error text, timestamp, URL, input, state, console line, or observation?"

# --- edit above ---------------------------------------------------------

printf '\n--- Captured ---\n'
printf 'BUG_SUMMARY=%s\n' "$BUG_SUMMARY"
printf 'EXPECTED=%s\n' "$EXPECTED"
printf 'ACTUAL=%s\n' "$ACTUAL"
printf 'SYMPTOM_REPRODUCED=%s\n' "$SYMPTOM_REPRODUCED"
printf 'REPRODUCED_COUNT=%s\n' "$REPRODUCED_COUNT"
printf 'TOTAL_RUNS=%s\n' "$TOTAL_RUNS"
printf 'NOTES=%s\n' "$NOTES"
