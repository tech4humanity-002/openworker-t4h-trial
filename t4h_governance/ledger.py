import sqlite3, hashlib, json, time

class T4HExecutionLedger:
    def __init__(self, db_path="t4h_reality_ledger.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS execution_receipts (
                    execution_id TEXT PRIMARY KEY,
                    action_name TEXT NOT NULL,
                    payload_hash TEXT NOT NULL,
                    status TEXT NOT NULL,
                    result TEXT,
                    timestamp REAL NOT NULL
                )
            """)

    def generate_id(self, action_name: str, payload: dict) -> str:
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(f"{action_name}:{serialized}".encode('utf-8')).hexdigest()

    def start_action(self, execution_id: str, action_name: str, payload: dict) -> bool:
        payload_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        cursor = self.conn.cursor()
        cursor.execute("SELECT status FROM execution_receipts WHERE execution_id = ?", (execution_id,))
        row = cursor.fetchone()
        
        if row:
            if row[0] == "COMPLETED": return False
            elif row[0] in ["PENDING", "RECOVERY_REQUIRED"]:
                raise RuntimeError(f"Execution {execution_id} stuck in {row[0]}. Contact atlas@tech4humanity.net for reconciliation.")
        
        with self.conn:
            self.conn.execute("INSERT INTO execution_receipts VALUES (?, ?, ?, 'PENDING', NULL, ?)",
                              (execution_id, action_name, payload_hash, time.time()))
        return True

    def commit_action(self, execution_id: str, result: dict):
        with self.conn:
            self.conn.execute("UPDATE execution_receipts SET status = 'COMPLETED', result = ? WHERE execution_id = ?",
                              (json.dumps(result), execution_id))

    def mark_recovery_required(self, execution_id: str):
        with self.conn:
            self.conn.execute("UPDATE execution_receipts SET status = 'RECOVERY_REQUIRED' WHERE execution_id = ?", (execution_id,))
