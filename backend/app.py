
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from gemini import extract_preferences, generate_story
from qloo import enrich_preferences

load_dotenv()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rihla", methods=["POST"])
def rihla():
    data = request.get_json()
    user_input = data.get("input", "")

    preferences = extract_preferences(user_input)
    if not preferences:
        return jsonify({"error": "Échec d'extraction Gemini"}), 400

    story = generate_story(preferences)
    qloo_results = enrich_preferences(preferences)

    return jsonify({
        "preferences": preferences,
        "story": story,
        "qloo_results": qloo_results
    })

if __name__ == "__main__":
    app.run(debug=True)
