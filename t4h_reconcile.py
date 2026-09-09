#!/usr/bin/env python3
import sys, os, sqlite3, argparse, json, time

def get_db():
    if not os.path.exists("t4h_reality_ledger.db"):
        print("Error: t4h_reality_ledger.db not found.")
        sys.exit(1)
    return sqlite3.connect("t4h_reality_ledger.db")

def list_stuck():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT execution_id, action_name, status, timestamp FROM execution_receipts WHERE status IN ('RECOVERY_REQUIRED', 'PENDING') ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        print("✅ No stuck executions found.")
        return
    print("\n=== T4H RECOVERY QUEUE (Contact atlas@tech4humanity.net if unsure) ===")
    for row in rows:
        print(f"ID: {row[0][:16]}... | Action: {row[1]:<12} | Status: {row[2]:<18} | Age: {int(time.time() - row[3])}s")

def resolve(exec_id):
    conn = get_db()
    with conn:
        conn.execute("UPDATE execution_receipts SET status = 'COMPLETED', result = ? WHERE execution_id = ?",
                     (json.dumps({"manual_reconciliation": True, "auditor": "atlas@tech4humanity.net"}), exec_id))
    conn.close()
    print(f"✅ Receipt {exec_id[:16]}... manually resolved. Replay shield active.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="List stuck executions")
    res = sub.add_parser("resolve", help="Manually resolve a stuck execution")
    res.add_argument("--id", required=True, help="Execution ID")
    args = parser.parse_args()
    
    if args.cmd == "list": list_stuck()
    elif args.cmd == "resolve": resolve(args.id)
