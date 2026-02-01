import json
from collections import defaultdict

RECON_COMMANDS = ["ls", "pwd", "whoami", "id", "uname"]
PRIV_ESC_COMMANDS = ["sudo", "su"]

def load_events(log_file="data/sessions.jsonl"):
    events = []
    with open(log_file, "r") as f:
        for line in f:
            events.append(json.loads(line))
    return events


def extract_behavior_features(events):
    sessions = defaultdict(list)

    # Group command events by session
    for e in events:
        if e["event_type"] == "command":
            sessions[e["session_id"]].append(e)

    behavior_profiles = {}

    for session_id, cmds in sessions.items():
        if len(cmds) < 2:
            continue

        times = [c["time"] for c in cmds]
        gaps = [times[i+1] - times[i] for i in range(len(times)-1)]

        commands = [c["data"]["cmd"] for c in cmds]

        recon_count = sum(
            any(cmd.startswith(r) for r in RECON_COMMANDS)
            for cmd in commands
        )

        priv_esc_count = sum(
            any(p in cmd for p in PRIV_ESC_COMMANDS)
            for cmd in commands
        )

        behavior_profiles[session_id] = {
            "command_count": len(commands),
            "avg_time_gap": sum(gaps) / len(gaps),
            "fast_command_ratio": sum(g < 1.0 for g in gaps) / len(gaps),
            "recon_ratio": recon_count / len(commands),
            "priv_esc_attempts": priv_esc_count
        }

    return behavior_profiles
