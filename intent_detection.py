from openai import OpenAI
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

def intent(text):
    print("triggered")
    prompt = f"""You are an intelligent assistant that converts voice notes into structured actions.
    Possible Intent Ctegories:
    -Reminder
    -Task Creation
    -Event Scheduling
    -Note Saving
    -Studying
    -Shopping list
    -General Information
    -Unkonwn
    Return only valid JSON.
    
    Output Format:{{
    "intent":"",
    "action_type":"",
    "task":"",
    "date":"",
    "time":"",
    "priority":"",
    "additional_details":""
    }}
    respond only with catgory name.
    User Input:{text}"""
    headers = {
        "Content-Type":"application/json",
        "Authorization":f"Bearer {API_KEY}"
    }
    payload = {
        "model":"openai/gpt-4o-mini",
        "messages":[{"role":"user","content":prompt}],
        "temperature":0
    }
    try:
        response = requests.post(API_URL,headers=headers,json=payload)
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return content
    except Exception as e:
        print("error:{e}")
        return "Intent not detected"
    

    