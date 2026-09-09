import logging
from .ledger import T4HExecutionLedger
from .gatekeeper import T4HGatekeeper

logging.basicConfig(level=logging.INFO, format="[T4H ORCHESTRATOR] %(levelname)s: %(message)s")

class T4HOrchestrator:
    def __init__(self):
        self.ledger = T4HExecutionLedger()
        self.gatekeeper = T4HGatekeeper()
        logging.info("Initialized: Ledger + Gatekeeper active")

    def execute(self, action_type: str, payload: dict, is_unattended: bool = False):
        if not self.gatekeeper.validate(action_type, payload, is_unattended):
            raise PermissionError(f"Gatekeeper denied: {action_type} (unattended={is_unattended})")
        
        exec_id = self.ledger.generate_id(action_type, payload)
        if not self.ledger.start_action(exec_id, action_type, payload):
            logging.warning(f"IDEMPOTENCY SHIELD: Blocked duplicate execution of {exec_id}")
            return {"status": "SKIPPED", "exec_id": exec_id, "reason": "Already completed"}
        
        try:
            result = self._perform_action(action_type, payload)
            self.ledger.commit_action(exec_id, result)
            logging.info(f"SUCCESS: {exec_id}")
            return {"status": "SUCCESS", "exec_id": exec_id, "result": result}
        except Exception as e:
            self.ledger.mark_recovery_required(exec_id)
            logging.critical(f"CRASH: {exec_id} marked RECOVERY_REQUIRED. Notify atlas@tech4humanity.net")
            raise RuntimeError(f"Execution failed. Receipt {exec_id} locked for manual reconciliation.") from e

    def _perform_action(self, action_type: str, payload: dict):
        if action_type == "shell":
            return {"command": payload["command"], "output": "simulated_success"}
        elif action_type == "slack_post":
            return {"destination": payload["channel"], "message": payload["message"], "status": "sent"}
        raise ValueError(f"Unsupported action: {action_type}")
