<!-- Sample: 2 | Arm: B0-PRIORITY-ATOMIC -->

# Acme Sync GA Go/No-Go Questionnaire

## Purpose and decision

Your answers will help Morgan Lee make the go/no-go decision for the Acme Sync GA launch. Please respond by **2026-08-30**.

## Sender, recipient, and answer use

- **From:** Morgan Lee, launch lead
- **To:** Priya Shah, Principal Platform Engineer
- **Use:** Morgan will use these answers to assess release readiness, define the rollback boundary, and confirm launch-week operational ownership.

## Context

The launch decision needs concise platform evidence on ingest capacity and SLO performance, plus the operational details needed for launch week. Priya is the sole owner of these answers.

## Answering instructions

Please keep this to **8 minutes or less**. Short answers, links, or pasted metrics are welcome. If an answer is unknown, write "Unknown" and note the quickest way to resolve it.

## Release capacity and SLO evidence

1. What is the **measured maximum sustainable ingest throughput** for the release candidate?

   **Answer:**

2. At that measured maximum, what is the **first bottleneck**?

   **Answer:**

3. Based on the measurement above, can the service **sustain 10k events/sec**?

   **Answer (yes/no, plus a metric or link if available):**

4. At 10k events/sec, does the service **meet the 99.9% SLO**?

   **Answer (yes/no, plus a metric or link if available):**

## Rollback readiness

5. What **objective rollback trigger** should Morgan use for the GA launch?

   **Answer (metric, threshold, and evaluation window):**

## Launch-week operations

6. Who is the **primary on-call owner during launch week**?

   **Answer (name or rotation):**

7. What is the **runbook URL**?

   **Answer:**

## Dashboard preference

8. What is your **preferred dashboard color**?

   **Answer:**

## Final check

9. Is there any other platform fact or risk that could change the Acme Sync GA go/no-go decision?

   **Answer:**
