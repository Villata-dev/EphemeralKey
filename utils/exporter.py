import json
import time

def export_session_to_json(email: str, password: str, filepath: str):
    """Exporta los datos generados a un JSON estructurado"""
    data = {
        "timestamp": time.time(),
        "identity": {
            "email": email,
            "password_length": len(password),
            "credentials": password
        }
    }
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
