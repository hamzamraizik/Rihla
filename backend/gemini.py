
import os, json, re
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def extract_preferences(text):
    prompt = f"""
Analyse ce texte et retourne uniquement un JSON avec des listes pour ces catégories :
musique, livres, nourriture, lieux, ambiances, styles.

Exemple :
{{
  "musique": ["Jazz classique", "Miles Davis"],
  "livres": ["Romans de Haruki Murakami"],
  "nourriture": ["Tagine marocain aux abricots"],
  "lieux": ["Villes combinant tradition et modernité", "Vieilles librairies"],
  "ambiances": ["Journées pluvieuses"],
  "styles": ["Design japonais minimaliste"]
}}

Texte : '''{text}'''
"""
    try:
        response = model.generate_content(prompt)
        content = response.text
        match = re.search(r"\{.*\}", content, re.DOTALL)
        return json.loads(match.group()) if match else {}
    except Exception as e:
        print("Erreur Gemini:", e)
        return {}

def generate_story(prefs):
    story = "Voici votre programme de voyage personnalisé :\n\n"
    if prefs.get("musique"):
        story += f"🎵 Musique : {', '.join(prefs['musique'])}\n"
    if prefs.get("livres"):
        story += f"📚 Livres : {', '.join(prefs['livres'])}\n"
    if prefs.get("nourriture"):
        story += f"🍽️ Nourriture : {', '.join(prefs['nourriture'])}\n"
    if prefs.get("lieux"):
        story += f"🌍 Lieux : {', '.join(prefs['lieux'])}\n"
    if prefs.get("ambiances"):
        story += f"🌧️ Ambiances : {', '.join(prefs['ambiances'])}\n"
    if prefs.get("styles"):
        story += f"🎨 Styles : {', '.join(prefs['styles'])}\n"
    return story
