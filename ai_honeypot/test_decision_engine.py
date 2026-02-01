from behavior_extractor import load_events, extract_behavior_features
from attacker_profile import classify_attacker
from decision_engine import decide_deception_strategy

# Load logs
events = load_events("data/sessions.jsonl")

# Extract behavior
behavior_profiles = extract_behavior_features(events)

# Test decision engine
for session_id, features in behavior_profiles.items():
    attacker = classify_attacker(features)
    strategy = decide_deception_strategy(features, attacker)

    print("\nSession ID:", session_id)
    print("Behavior Features:", features)
    print("Attacker Profile:", attacker)
    print("Deception Strategy:")
    for k, v in strategy.items():
        print(f"  {k}: {v}")

    print("=" * 60)
