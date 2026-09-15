# OpenWorker × T4H — Seven Operational Use Cases

These seven use cases are the initial production surface for OpenWorker inside the T4H operating model. The distinction is intentional: the use case describes the outcome; OpenWorker supplies local execution; T4H supplies authority, lifecycle, evidence, verification and durable truth.

## Common lifecycle

`intent → validate → prioritise → queue → assign OpenWorker → execute → receipt → verify → ledger → telemetry → distribute → recover/close`

A run is **REAL only when the receipt, telemetry and independent verification exist**.

## 1. Automated Security & Code Vulnerability Audits

**Stops:** IDE/terminal/scanner context switching; manual copying of scanner findings; blind AI patches.

**Starts:** deterministic scanners + model reasoning; isolated candidate diffs; secondary checker-model audit before sign-off.

**Evidence:** scanner output, model rationale, candidate diff, checker result, test result, approval and final repository state.

**Gate:** patch application/merge.

## 2. Cloud Configuration & Posture Remediation

**Stops:** manual risk-report triage; hand-written remediation from scratch; uncontrolled cloud mutations.

**Starts:** live API + IaC baseline checks; ready-to-apply IaC patches; explicit human-gated infrastructure execution.

**Evidence:** source API observations, baseline version, proposed IaC diff, policy decision, approval, execution result and cloud read-back.

**Gate:** every live infrastructure mutation.

## 3. Cross-Tool Incident Triage & Synthesis

**Stops:** multi-tab evidence hunting; manual timeline reconstruction; delayed stakeholder updates.

**Starts:** parallel local/SaaS evidence collection; incident timeline + RCA draft; prepared status update for approval.

**Evidence:** source timestamps, correlation IDs, timeline, hypotheses, confidence, recommended actions and communication receipt.

**Gate:** client/external communication and consequential remediation.

## 4. Automated Daily Operations & Morning Briefings

**Stops:** 30–45 minute manual morning sweep; buried blockers; manual action-list compilation.

**Starts:** scheduled unattended runs; priority aggregation; local Markdown or private-channel briefing.

**Evidence:** execution timestamp, source freshness, items collected, prioritisation rationale, generated briefing and delivery receipt.

**Gate:** external communication only.

## 5. Account & Meeting Intelligence Gathering

**Stops:** last-minute CRM review; manual email/knowledge search; forgotten historical actions.

**Starts:** calendar-triggered retrieval; CRM + email + internal-note synthesis; one pre-meeting dossier.

**Evidence:** calendar trigger, participant resolution, source references, freshness, dossier and unresolved-action list.

**Gate:** external communication only.

## 6. Slack-Driven Local Agent Workflows

**Stops:** leaving the communication hub; isolated desktop diagnostics; dangerous ungated bot execution.

**Starts:** Slack-triggered bounded local jobs; sandboxed tools/MCP; results returned to the originating thread.

**Evidence:** originating message/thread, actor identity, authority, task hash, OpenWorker event stream, tool calls, result artefacts and reply receipt.

**Gate:** dangerous/local mutation or any external side effect.

## 7. Release Gate & Compliance Verification

**Stops:** manual PR/ticket cross-checks; unverified releases; manual readiness compilation.

**Starts:** automated PR/QA/docs checks; blocker detection; actionable Markdown release-readiness report.

**Evidence:** PR state, linked work item, CI results, QA evidence, documentation checks, dependency state, release report and final clearance.

**Gate:** release/deployment clearance.

## Worker contract

Every use case becomes a queueable worker capability. The worker may execute only within the authority and dependency envelope attached to the job. It must emit machine-readable evidence and cannot self-declare success.

### Required receipt fields

- `job_id`
- `worker_id`
- `use_case_id`
- `intent`
- `owner`
- `authority_ref`
- `started_at`
- `finished_at`
- `event_evidence_ref`
- `input_evidence_refs`
- `output_artifact_refs`
- `verification_ref`
- `state_before`
- `state_after`
- `outcome`
- `receipt_hash`

### Outcome states

`REAL | PARTIAL | BLOCKED | DEGRADED | QUARANTINED | ASPIRATIONAL`

No worker is allowed to turn `PARTIAL` into `REAL` by assertion. The verification engine decides from evidence.
