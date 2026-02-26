import webbrowser
import datetime
import os

def execute(intent_data):
    intent = intent_data.get("intent")
    target = intent_data.get("target")
    if intent == "open_website":
        webbrowser.open(f"https://{target}.com")
        return f"Opening{target}"
    elif intent == "search":
        webbrowser.open(f"https://www.google.com/search?q={target}")
        return f"Searching for {target}"
    elif intent == "get_time":
        now = datetime.datetime.now().strftime("%H:%M:%S")
        return f"Current time: {now}"
    elif intent == "open_app":
        os.system(target)
        return f"Opening {target}"
    return "Command not supported"

