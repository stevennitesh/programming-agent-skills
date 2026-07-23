<!-- Sample: 5; Arm: B0-PRIORITY-ATOMIC -->

# Acme Sync GA Go/No-Go Questionnaire

## Purpose and decision

Your answers will support the go/no-go decision for Acme Sync general availability.

- **From:** Morgan Lee, Launch Lead
- **For:** Priya Shah, Principal Platform Engineer
- **Response deadline:** August 30, 2026
- **Answer use:** Morgan will use these answers to assess release readiness, launch coverage, and rollback criteria.

## Context

We need your platform-level measurements and launch decisions to close the remaining readiness gaps for Acme Sync GA. Please answer from the evidence available to you; if an answer is not yet known, state that and identify the evidence or test needed.

## Answering instructions

Please keep your response to **8 minutes or less**. Short answers, metrics, names, and links are sufficient.

## Release readiness

1. What is the measured maximum sustainable ingest throughput for Acme Sync, and what is the first bottleneck reached at that rate?

   **Answer:**

2. Based on that measured throughput, can the service sustain **10,000 events/second** while meeting the **99.9% SLO**?

   **Answer (yes / no / not yet demonstrated, plus one brief evidence reference):**

3. What single objective condition should trigger rollback during the GA launch?

   **Answer (metric, threshold, and evaluation window):**

## Launch coverage

4. Who is the primary on-call owner during launch week?

   **Answer (name or rotation):**

## Supporting preferences and references

5. What is your preferred dashboard color?

   **Answer:**

6. What is the runbook URL for the Acme Sync GA launch?

   **Answer:**

## Final check

7. Is there any other platform risk or constraint that could materially change the Acme Sync GA go/no-go decision?

   **Answer (optional):**
