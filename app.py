import os
import json
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv
import google.generativeai as genai

# Chargement des variables d’environnement
load_dotenv()
QLOO_API_KEY = os.getenv("QLOO_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QLOO_BASE_URL = "https://hackathon.api.qloo.com"

# Configuration Flask
app = Flask(__name__)

# Configuration API Qloo
HEADERS = {
    "X-Api-Key": QLOO_API_KEY,
    "Content-Type": "application/json"
}

# Configuration Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")

# Fonction de génération de parcours narratif
def generate_travel_narrative(preferences):
    prompt = f"""
You are a cultural assistant. Create a personalized narrative travel itinerary based on these preferences:
{preferences}

Provide a fluid, inspiring, and structured text (2 to 3 paragraphs).
"""
    response = gemini_model.generate_content(prompt)
    return response.text

# Fonction de recherche via Qloo
def search_entities(query, category="film"):
    response = requests.get(
        f"{QLOO_BASE_URL}/search",
        headers=HEADERS,
        params={"query": query, "category": category}
    )
    if response.status_code != 200:
        raise Exception(f"Qloo Search Error ({response.status_code}): {response.text}")
    return response.json().get("results", [])

# Fonction de recommandation via Qloo
def get_recommendations(ids, category="film"):
    response = requests.get(
        f"{QLOO_BASE_URL}/recs",
        headers=HEADERS,
        params={"sample": json.dumps(ids), "category": category}
    )
    if response.status_code != 200:
        raise Exception(f"Qloo Recs Error ({response.status_code}): {response.text}")
    return response.json().get(category, [])

# Route principale
@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    results = []
    recs = []
    narrative = ""
    error = ""

    if request.method == "POST":
        query = request.form.get("query", "")
        try:
            raw_results = search_entities(query)
            print("DEBUG raw_results:", raw_results)  # Affiche le contenu brut dans la console
            # On s'assure que chaque résultat possède bien 'id' et 'name'
            results = []
            for e in raw_results:
                results.append({
                    'id': e.get('id', '?'),
                    'name': e.get('name', 'Nom inconnu')
                })
            ids = [e['id'] for e in results[:2] if e['id'] != '?']
            if ids:
                recs_raw = get_recommendations(ids)
                # On s'assure aussi que chaque reco possède 'name'
                recs = []
                for r in recs_raw:
                    recs.append({
                        'name': r.get('name', 'Nom inconnu')
                    })
            prefs_text = ", ".join([r['name'] for r in results])
            narrative = generate_travel_narrative(prefs_text)
        except Exception as e:
            error = f"Erreur : {e}"

    return render_template("index.html", query=query, results=results, recs=recs, narrative=narrative, error=error)

# Lancement de l’application
if __name__ == "__main__":
    app.run(debug=True)
