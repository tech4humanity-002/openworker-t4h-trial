# REAL Run Sequence

The first proof is OW-01 because it can be executed locally with no production mutation.

## Job

`OW-01 / inspect repository → run deterministic checks → propose README-only improvement → independently verify diff`

## Sequence

1. T4H creates/claims a queue job with `use_case_id=OW-01`.
2. Authority and workspace are resolved before starting OpenWorker.
3. OpenWorker starts against the bounded workspace.
4. Adapter connects to the OpenWorker session WebSocket.
5. Adapter records `ready` and sends the exact job intent.
6. Complete OpenWorker events are persisted as execution evidence.
7. Any `permission_required` event becomes a human gate; no automatic approval.
8. On `turn_done`, T4H independently reads the workspace state.
9. The verifier checks that only the intended README change occurred and that the requested checks passed.
10. T4H writes the final receipt containing the event-evidence reference and before/after state.
11. Receipt is hashed and linked to the queue job/audit record.
12. Only after verification is the outcome `REAL`.

## Failure handling

- no `ready` → `DEGRADED`
- permission requested without available authority → `BLOCKED`
- unexpected file mutation → `QUARANTINED`
- execution completes but verification fails → `PARTIAL`
- evidence cannot be replayed → `PARTIAL`

## Completion criterion

A successful run must be reproducible from the receipt references without relying on chat history or model memory.
