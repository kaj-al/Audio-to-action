import json
import os

DATA_FILE = "data.json"

#  DATA STORAGE 
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"tasks": [], "notes": [], "events": [], "shopping": [], "reminder": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

def automate(intent_data):
    if not isinstance(intent_data, dict):
        return

    intent = intent_data.get("intent", "Unknown")

    # Normalize intent string for comparisons
    intent_norm = intent.strip().lower() if isinstance(intent, str) else "unknown"

    if intent_norm in ("reminder", "task creation", "task"):
        data.setdefault("tasks", []).append(intent_data)

    elif intent_norm in ("event scheduling", "event"):
        data.setdefault("events", []).append(intent_data)

    elif intent_norm in ("note saving", "note"):
        data.setdefault("notes", []).append(intent_data)

    elif "shop" in intent_norm or intent_norm == "shopping list" or intent_norm == "shopping":
        data.setdefault("shopping", []).append(intent_data)

    elif intent_norm == "reminder":
        data.setdefault("reminder", []).append(intent_data)

    else:
        # Unknown intents go into notes for later review
        data.setdefault("notes", []).append(intent_data)

    save_data(data)