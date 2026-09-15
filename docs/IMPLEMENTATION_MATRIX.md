# Seven Use Cases — Implementation Matrix

| ID | Primary OpenWorker capability | T4H integration | First proof |
|---|---|---|---|
| OW-01 | Local repo/tools + MCP | scanner evidence → checker → receipt | audit a safe test repo and produce verified candidate diff |
| OW-02 | shell/tools + MCP | authority + cloud read-back + receipt | read-only posture audit; remediation remains gated |
| OW-03 | connectors + local tools | evidence correlation + incident ledger | synthesise a bounded synthetic incident |
| OW-04 | local scheduler/session | queue + freshness + delivery receipt | scheduled Markdown morning brief |
| OW-05 | calendar/connectors + retrieval | trigger binding + source provenance | generate a dossier from a bounded test meeting |
| OW-06 | messaging gateway + local execution | actor/authority binding + thread receipt | safe diagnostic invoked from a controlled Slack thread |
| OW-07 | GitHub/CI/MCP | release policy + independent verification | generate readiness report against a test PR |

## Priority

1. **OW-01** — best first proof because it is local, bounded and produces an inspectable diff.
2. **OW-07** — directly exercises GitHub evidence and release gates already present in T4H.
3. **OW-04** — establishes unattended recurring execution without requiring destructive side effects.
4. **OW-06** — proves event-driven worker invocation from a communication surface.
5. **OW-03** — adds cross-tool synthesis and external communication gates.
6. **OW-05** — adds identity/context aggregation and privacy-sensitive provenance.
7. **OW-02** — highest-value but highest-risk; only after authority, telemetry and cloud read-back are proven.

## Non-negotiable controls

- Never bypass OpenWorker approval mechanisms.
- Never put secrets in event evidence or receipts.
- Never execute a consequential cloud or release action from a stale approval.
- Never accept model text as verification.
- Never mark a job `REAL` without replayable evidence.
