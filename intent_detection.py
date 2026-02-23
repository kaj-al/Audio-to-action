
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")


def _extract_json(content: str):
    try:
        return json.loads(content)
    except Exception:
        pass

    # Fallback
    start = content.find("{")
    end = content.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(content[start:end + 1])
        except Exception:
            pass

    return None


def intent(text: str):
    prompt = f"""You are an assistant that converts voice notes into structured actions.
Possible Intent Categories:
- Reminder
- Task Creation
- Event Scheduling
- Note Saving
- Studying
- Shopping list
- General Information
- Unknown

Return ONLY a single valid JSON object and nothing else, matching this schema:
{{
  "intent": "one of the categories above",
  "action_type": "",
  "task": "",
  "date": "",
  "time": "",
  "priority": "",
  "additional_details": ""
}}

User Input: {text}
"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }

    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        resp.raise_for_status()
        result = resp.json()
        content = None
        if isinstance(result, dict):
            choices = result.get("choices") or []
            if choices and isinstance(choices, list):
                message = choices[0].get("message") if isinstance(choices[0], dict) else None
                if message and isinstance(message, dict):
                    content = message.get("content")
        if content is None:
            content = result.get("content") if isinstance(result, dict) else None

        if not content:
            return {
                "intent": "Unknown",
                "action_type": "",
                "task": "",
                "date": "",
                "time": "",
                "priority": "",
                "additional_details": "No content in model response"
            }

        parsed = _extract_json(content)
        if isinstance(parsed, dict):
            return parsed

        # return best-effort dict
        clean = content.strip()
        return {
            "intent": clean.splitlines()[0][:100],
            "action_type": "",
            "task": "",
            "date": "",
            "time": "",
            "priority": "",
            "additional_details": clean
        }

    except Exception as e:
        print(f"error: {e}")
        return {
            "intent": "Unknown",
            "action_type": "",
            "task": "",
            "date": "",
            "time": "",
            "priority": "",
            "additional_details": str(e)
        }
    

    