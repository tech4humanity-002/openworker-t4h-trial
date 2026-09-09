import os, pytest, sqlite3
from t4h_governance import T4HOrchestrator

TEST_DB = "test_e2e_ledger.db"

@pytest.fixture
def orchestrator():
    if os.path.exists(TEST_DB): os.remove(TEST_DB)
    orch = T4HOrchestrator()
    orch.ledger.db_path = TEST_DB
    orch.ledger.conn = sqlite3.connect(TEST_DB)
    orch.ledger._create_tables()
    yield orch
    if os.path.exists(TEST_DB): os.remove(TEST_DB)

def test_idempotency_shield(orchestrator):
    payload = {"channel": "#test", "message": "hello"}
    res1 = orchestrator.execute("slack_post", payload)
    assert res1["status"] == "SUCCESS"
    res2 = orchestrator.execute("slack_post", payload)
    assert res2["status"] == "SKIPPED"

def test_unattended_shell_blocked(orchestrator):
    with pytest.raises(PermissionError):
        orchestrator.execute("shell", {"command": "rm -rf /"}, is_unattended=True)

def test_crash_marks_recovery(orchestrator):
    with pytest.raises(RuntimeError):
        orchestrator.execute("invalid_action", {"foo": "bar"})
    
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM execution_receipts WHERE action_name = 'invalid_action'")
    assert cursor.fetchone()[0] == "RECOVERY_REQUIRED"
    conn.close()
