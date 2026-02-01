def classify_attacker(features):
    profile = {}

    if features["fast_command_ratio"] > 0.7:
        profile["automation"] = "high"
    else:
        profile["automation"] = "low"

    if features["recon_ratio"] > 0.5:
        profile["intent"] = "reconnaissance"
    elif features["priv_esc_attempts"] > 0:
        profile["intent"] = "privilege_escalation"
    else:
        profile["intent"] = "unknown"

    if features["command_count"] > 20:
        profile["skill_level"] = "medium"
    else:
        profile["skill_level"] = "low"

    return profile
