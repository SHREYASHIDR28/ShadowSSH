def decide_deception_strategy(behavior_features, attacker_profile):
    """
    Core autonomous decision engine.
    Inputs:
      - behavior_features (dict)
      - attacker_profile (dict)
    Output:
      - deception strategy (dict)
    """

    strategy = {}
  

    # 1. Decide deception depth
    if attacker_profile["skill_level"] == "low":
        strategy["deception_depth"] = "medium"
    else:
        strategy["deception_depth"] = "high"

    # 2. Decide realism level
    if attacker_profile["automation"] == "low":
        strategy["realism_level"] = "highly_realistic"
        strategy["response_style"] = "human_like"
    else:
        strategy["realism_level"] = "basic"
        strategy["response_style"] = "generic"

    # 3. Decide engagement goal
    if attacker_profile["intent"] == "reconnaissance":
        strategy["engagement_goal"] = "observe"
    elif attacker_profile["intent"] == "privilege_escalation":
        strategy["engagement_goal"] = "mislead"
    else:
        strategy["engagement_goal"] = "observe"

    # 4. Decide environment evolution
    if behavior_features["command_count"] > 8:
        strategy["environment_change"] = True
    else:
        strategy["environment_change"] = False

    return strategy
