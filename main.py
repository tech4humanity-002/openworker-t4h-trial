import sys, json, logging
from t4h_governance import T4HOrchestrator

logging.basicConfig(level=logging.INFO, format="[T4H ENTRY] %(message)s")

def handle_slack_event(event: dict, is_unattended: bool = False):
    orchestrator = T4HOrchestrator()
    action_type = event.get("action_type")
    payload = {k: v for k, v in event.items() if k != "action_type"}
    
    try:
        result = orchestrator.execute(action_type, payload, is_unattended)
        print(json.dumps({"response_type": "in_channel", "text": f"✅ {json.dumps(result)}"}, indent=2))
    except PermissionError as e:
        print(json.dumps({"response_type": "ephemeral", "text": f"🚫 BLOCKED: {e}"}, indent=2))
    except RuntimeError as e:
        print(json.dumps({"response_type": "ephemeral", "text": f"⚠️ RECOVERY REQUIRED: {e}"}, indent=2))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test_slack":
        print("\n--- Test 1: Allowed Attended Shell ---")
        handle_slack_event({"action_type": "shell", "command": "git status"}, is_unattended=False)
        print("\n--- Test 2: Blocked Unattended Shell (Issue #296) ---")
        handle_slack_event({"action_type": "shell", "command": "rm -rf /"}, is_unattended=True)
        print("\n--- Test 3: Idempotent External Write ---")
        handle_slack_event({"action_type": "slack_post", "channel": "#deploy", "message": "Go"}, is_unattended=False)
        print("\n--- Test 3b: Duplicate Write Attempt ---")
        handle_slack_event({"action_type": "slack_post", "channel": "#deploy", "message": "Go"}, is_unattended=False)
    else:
        print("Usage: python3 main.py test_slack")
