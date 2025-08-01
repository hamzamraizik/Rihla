
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

QLOO_API_KEY = os.getenv("QLOO_API_KEY")
QLOO_BASE_URL = "https://hackathon.api.qloo.com"
HEADERS = {
    "X-Api-Key": QLOO_API_KEY,
    "Content-Type": "application/json"
}
CATEGORIES = ["film", "music", "book", "travel", "cuisine"]

def search_qloo(query):
    results = {}
    for cat in CATEGORIES:
        try:
            res = requests.get(
                f"{QLOO_BASE_URL}/search",
                headers=HEADERS,
                params={"query": query, "category": cat}
            )
            if res.status_code == 200:
                results[cat] = res.json().get("results", [])
            else:
                results[cat] = []
        except Exception:
            results[cat] = []
    return results

def get_recommendations(ids_by_cat):
    recos = {}
    for cat, ids in ids_by_cat.items():
        if not ids:
            continue
        try:
            res = requests.get(
                f"{QLOO_BASE_URL}/recs",
                headers=HEADERS,
                params={"sample": json.dumps(ids[:5]), "category": cat}
            )
            if res.status_code == 200:
                recos[cat] = res.json().get(cat, [])
            else:
                recos[cat] = []
        except Exception:
            recos[cat] = []
    return recos

def get_categories():
    return CATEGORIES
