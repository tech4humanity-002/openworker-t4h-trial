# T4H × OpenWorker

This repository is the integration harness for evaluating **OpenWorker v0.2.1** as the local execution surface for the T4H governed runtime.

Upstream: `andrewyng/openworker`  
Pinned release: `v0.2.1`  
Control plane: `tech4humanity-002/t4h-remote-mcp-server-clean`

## Why this exists

OpenWorker already supplies the local agent harness: model selection, desktop/local execution, MCP/connectors, approval gates and an audit trail. T4H supplies the missing outer control-plane discipline: present authority, evidence freshness, receipt/ledger semantics, verification, recovery and durable outcome classification.

The integration boundary is deliberately **adapter-first**. We do not fork or rewrite OpenWorker. We wrap it with a T4H execution contract and only classify a run as `REAL` after the required evidence exists.

## Governance boundary

- **No receipt = not REAL.**
- **Unobserved change = not REAL.**
- **No present authority = BLOCKED.**
- Memory is advisory; runtime state wins.
- Consequential actions must be revalidated at execution time, not justified solely by an earlier approval.
- Human gates remain mandatory for destructive, unsafe, legally sensitive, credential-exposing or otherwise irreversible actions.

See [`OPENWORKER_T4H_CONTRACT.json`](./OPENWORKER_T4H_CONTRACT.json).

## First real run

1. Install the upstream OpenWorker v0.2.1 release or run it from source.
2. Give it a bounded T4H task with an explicit owner and authority reference.
3. Run the T4H preflight adapter:

```bash
python3 scripts/openworker-t4h-preflight.py \
  --intent "inspect and report on a bounded repository task" \
  --owner "T4H runtime" \
  --authority "explicit operator approval" \
  --evidence "current repository state"
```

4. Execute the task in OpenWorker.
5. Preserve the OpenWorker transcript/action audit and the resulting changed-state evidence.
6. Attach those artefacts to the T4H final receipt.
7. Only then classify the outcome `REAL`.

## Acceptance gate

The trial is complete only when all five are true:

- real OpenWorker installation
- real task execution
- real T4H receipt
- real verification of the intended outcome
- replayable evidence

Until then the repository remains intentionally `PARTIAL` rather than claiming success on the basis of configuration alone.

## Relationship to the T4H worker runtime

The existing T4H PEN worker already follows the same basic pattern: bounded job → builder → verification → PR → receipt. OpenWorker should become a **local governed worker/harness**, not a second source of truth or a competing control plane.

That means OpenWorker can provide execution capability while the T4H runtime remains authoritative for lifecycle, authority, receipts, verification, recovery and telemetry.
