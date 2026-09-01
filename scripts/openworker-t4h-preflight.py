#!/usr/bin/env python3
"""T4H preflight/receipt adapter for a local OpenWorker run.

This intentionally does not grant authority. It records the requested task,
current evidence, and the execution boundary so a later runtime can attach the
real OpenWorker transcript and outcome.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS = ROOT / "receipts"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intent", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--authority", required=True)
    parser.add_argument("--evidence", action="append", default=[])
    args = parser.parse_args()

    receipt = {
        "schema": "t4h.openworker.preflight.receipt.v1",
        "receipt_id": str(uuid.uuid4()),
        "status": "PARTIAL",
        "worker": "OpenWorker",
        "intent": args.intent,
        "owner": args.owner,
        "authority": args.authority,
        "evidence": args.evidence,
        "repository": "tech4humanity-002/openworker-t4h-trial",
        "upstream": "andrewyng/openworker@v0.2.1",
        "git_head": git("rev-parse", "HEAD"),
        "working_tree": git("status", "--porcelain").splitlines(),
        "created_at": now(),
        "next_required": [
            "attach real OpenWorker execution transcript",
            "attach action/tool telemetry",
            "verify intended state change",
            "write final outcome receipt"
        ]
    }
    canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":"))
    receipt["receipt_hash"] = hashlib.sha256(canonical.encode()).hexdigest()
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    path = RECEIPTS / f"preflight-{receipt['receipt_id']}.json"
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PARTIAL", "receipt": str(path), "receipt_hash": receipt["receipt_hash"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
