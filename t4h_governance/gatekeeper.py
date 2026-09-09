import shlex

ALLOWED_SHELL_PREFIXES = [["git", "status"], ["git", "diff"], ["pytest"], ["npm", "test"]]

class T4HGatekeeper:
    def validate(self, action_type: str, payload: dict, is_unattended: bool) -> bool:
        if is_unattended and action_type == "shell":
            return False
        
        if action_type == "shell":
            cmd = payload.get("command", "")
            tokens = shlex.split(cmd)
            if not tokens: return False
            for allowed in ALLOWED_SHELL_PREFIXES:
                if tokens[:len(allowed)] == allowed: return True
            return False
            
        return True
