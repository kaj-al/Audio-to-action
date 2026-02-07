import json
import os

DATA_FILE = "data.json"

# ---------------- DATA STORAGE ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"tasks": [], "notes": [], "events": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

def automate(intent_data):
    if not isinstance(intent_data,dict):
        return
    intent = intent_data.get("intent")

    if intent in ["Reminder", "Task Creation"]:
        data["tasks"].append(intent_data)

    elif intent == "Event Scheduling":
        data["events"].append(intent_data)

    elif intent == "Note Saving":
        data["notes"].append(intent_data)
    
    elif intent == "Shopping":
        data["shopping"].append(intent_data)
    
    elif intent == "Reminder":
        data["reminder"].append(intent_data)

    save_data(data)