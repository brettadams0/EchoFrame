# server/generator.py
# 🧠 Uses OpenRouter (no install, free key) to generate branches

import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = 'ENTER-YOUR-KEY'

SYSTEM_PROMPT = """
You are a thought expander. Given an idea, break it into logical branches:
- possible consequences
- counterpoints
- questions it raises
Keep responses concise, like bullet points. No summaries.
"""

def expand_thought(thought, max_branches=4):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    { "role": "system", "content": SYSTEM_PROMPT },
                    { "role": "user", "content": f"Expand this idea: {thought}" }
                ],
                "temperature": 0.8
            }
        )
        output = response.json()["choices"][0]["message"]["content"]
        lines = [line.strip("-• ") for line in output.split("\n") if line.strip()]
        return lines[:max_branches]
    except Exception as e:
        print(f"[ERROR] OpenRouter expansion failed: {e}")
        return []
