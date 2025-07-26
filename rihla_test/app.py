
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
from qloo_api import search_all_categories, get_recommendations_per_category
from gemini_api import generate_travel_narrative

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/discover', methods=['POST'])
def discover():
    data = request.get_json()
    query = data.get("preference")

    entities_by_category = search_all_categories(query)
    ids_by_cat = {
        cat: [item['id'] for item in items if 'id' in item] 
        for cat, items in entities_by_category.items()
    }
    recommendations = get_recommendations_per_category(ids_by_cat)
    itinerary = generate_travel_narrative(entities_by_category, recommendations)

    return jsonify({
        "entities": entities_by_category,
        "recommendations": recommendations,
        "itinerary": itinerary
    })

if __name__ == '__main__':
    app.run(debug=True)
