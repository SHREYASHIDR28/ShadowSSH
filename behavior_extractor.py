import json

LOG_FILE = "data/sessions.json"

def extract_behavior_features(session_id):
    # ---------- Default safe values (IMPORTANT) ----------
    command_count = 0
    timestamps = []
    recon_commands = ["ls", "pwd", "whoami", "cat", "ps", "netstat"]
    recon_hits = 0
    priv_esc_attempts = 0
    fast_commands = 0

    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                if not line.strip():
                    continue

                event = json.loads(line)

                if event.get("session_id") != session_id:
                    continue

                if event.get("event_type") == "command":
                    command_count += 1
                    cmd = event["data"].get("cmd", "")
                    ts = event.get("time", 0)

                    timestamps.append(ts)

                    # Recon activity detection
                    if any(rc in cmd for rc in recon_commands):
                        recon_hits += 1

                    # Privilege escalation detection
                    if "sudo" in cmd or cmd.startswith("su "):
                        priv_esc_attempts += 1

    except FileNotFoundError:
        pass
    except Exception as e:
        print("Behavior extraction error:", e)

    # ---------- Temporal features ----------
    avg_time_gap = 0.0
    if len(timestamps) > 1:
        gaps = [
            timestamps[i + 1] - timestamps[i]
            for i in range(len(timestamps) - 1)
        ]
        avg_time_gap = sum(gaps) / len(gaps)

        # Fast command detection (< 2s between commands)
        fast_commands = sum(1 for g in gaps if g < 2)

    # ---------- Ratios ----------
    recon_ratio = recon_hits / command_count if command_count else 0.0
    fast_command_ratio = fast_commands / command_count if command_count else 0.0

    # ---------- FINAL FEATURE VECTOR ----------
    return {
        "command_count": command_count,
        "avg_time_gap": round(avg_time_gap, 2),
        "fast_command_ratio": round(fast_command_ratio, 2),
        "recon_ratio": round(recon_ratio, 2),
        "priv_esc_attempts": priv_esc_attempts
    }
