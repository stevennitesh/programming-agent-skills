<!-- Sample: 4 | Arm: B0-PRIORITY-ATOMIC -->

# Acme Sync GA go/no-go questionnaire

## Purpose and decision

Morgan Lee, launch lead, is preparing the go/no-go decision for Acme Sync GA. Your answers will be used to assess launch readiness, define the rollback boundary, and confirm launch-week ownership.

- **From:** Morgan Lee, Launch Lead
- **To:** Priya Shah, Principal Platform Engineer
- **Response deadline:** August 30, 2026
- **Expected effort:** No more than 8 minutes

## Context

You are the owner of the requested technical and operational answers. The most decision-critical items are the measured ingest limit, whether the evidence supports the launch target and SLO, and the objective rollback trigger. Brief answers are sufficient.

## Answering instructions

Please answer from the best evidence currently available. If an answer is unknown, write "unknown" rather than estimating.

## Capacity and reliability

1. What is the measured maximum sustainable ingest throughput for Acme Sync, in events per second?

   **Answer:**

2. At that measured maximum, what is the first bottleneck?

   **Answer:**

3. Does the available evidence support that the service can sustain 10,000 events per second?

   **Answer:** Yes / No / Conditional / Unknown

4. Does the available evidence support that the service can meet the 99.9% SLO while sustaining 10,000 events per second?

   **Answer:** Yes / No / Conditional / Unknown

## Rollback readiness

5. What single objective trigger should cause the launch team to roll back Acme Sync GA?

   **Answer:**

## Launch-week ownership

6. Who is the primary on-call owner during launch week?

   **Answer:**

## Dashboard and runbook details

7. What is your preferred dashboard color?

   **Answer:**

8. What is the runbook URL?

   **Answer:**

## Final check

9. Is there anything else you know that could materially change the Acme Sync GA go/no-go decision?

   **Answer:**
