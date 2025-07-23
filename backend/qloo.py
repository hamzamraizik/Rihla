
import os
import requests
from utils import map_to_qloo_type

QLOO_API_KEY = os.getenv("QLOO_API_KEY")

def query_qloo(category, term):
    url = "https://hackathon.api.qloo.com/v1/taste"
    headers = {
        "Authorization": f"Bearer {QLOO_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "type": category,
        "input": term
    }
    try:
        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def enrich_preferences(preferences):
    enriched = {}
    for cat, items in preferences.items():
        enriched[cat] = []
        qloo_type = map_to_qloo_type(cat)
        for item in items:
            result = query_qloo(qloo_type, item)
            enriched[cat].append(result)
    return enriched
