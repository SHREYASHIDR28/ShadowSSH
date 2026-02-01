import json
import time

LOG_FILE = "data/sessions.json"

def log_event(session_id, event_type, data):
    entry = {
        "session_id": session_id,
        "event_type": event_type,
        "data": data,
        "time": time.time()
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
