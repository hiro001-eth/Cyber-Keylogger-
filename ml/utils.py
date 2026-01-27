# ml/utils.py

def extract_features_from_keystrokes(events):
    # Example: typing speed, interval stddev, key repetition, etc.
    return {
        "avg_interval": 0.1,
        "stddev_interval": 0.01,
        "unique_keys": len(set(e['key'] for e in events)),
        # Add more features as needed
    }
