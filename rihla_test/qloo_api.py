
import requests
import os

QLOO_KEY = os.getenv("QLOO_API_KEY")
HEADERS = {"X-API-KEY": QLOO_KEY}
BASE_URL = "https://api.qloo.com"
CATEGORIES = ["film", "music", "book", "travel", "cuisine"]

def search_all_categories(query):
    results = {}
    for category in CATEGORIES:
        url = f"{BASE_URL}/culture/search/{category}"
        res = requests.post(url, headers=HEADERS, json={"query": query})
        if res.status_code == 200:
            results[category] = res.json().get("results", [])
    return results

def get_recommendations_per_category(ids_by_cat):
    recos = {}
    for cat, ids in ids_by_cat.items():
        if not ids:
            continue
        url = f"{BASE_URL}/culture/recommend/{cat}"
        res = requests.post(url, headers=HEADERS, json={"ids": ids})
        if res.status_code == 200:
            recos[cat] = res.json().get("results", [])
    return recos
