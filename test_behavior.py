from behavior_extractor import load_events, extract_behavior_features
from attacker_profile import classify_attacker

# Load attack logs
events = load_events("data/sessions.jsonl")  # change if needed

# Extract behavior features
behavior_profiles = extract_behavior_features(events)

# Display results
for session_id, features in behavior_profiles.items():
    print("\nSession ID:", session_id)
    print("Behavior Features:")
    for k, v in features.items():
        print(f"  {k}: {v}")

    attacker_type = classify_attacker(features)
    print("Attacker Profile:")
    for k, v in attacker_type.items():
        print(f"  {k}: {v}")

    print("-" * 50)
