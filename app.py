
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
import uuid
import time
import re
import spacy
from flask import Flask, render_template, request
from qloo_api import search_qloo, get_recommendations, get_categories
from gemini_api import generate_itinerary


load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

nlp = spacy.load("en_core_web_sm")
CATEGORIES = get_categories()

@app.route('/static/<path:filename>')
def root_static(filename):
    """Serve static files from the app's static directory"""
    static_dir = app.static_folder or 'static'
    return send_from_directory(static_dir, filename)

@app.route('/', methods=["GET", "POST"])
def index():
    # Use the beautiful frontend template instead of the backend one
    return render_template('frontend_index.html')

# Mock authentication endpoints for frontend compatibility
@app.route('/auth/login', methods=['POST'])
def auth_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Simple mock authentication - in production, implement proper auth
    if email and password:
        mock_user = {
            'id': str(uuid.uuid4()),
            'name': email.split('@')[0].title(),
            'email': email
        }
        return jsonify({
            'success': True,
            'token': f'mock_token_{int(time.time())}',
            'user': mock_user
        })
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/auth/register', methods=['POST'])
def auth_register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    # Simple mock registration - in production, implement proper auth
    if name and email and password:
        mock_user = {
            'id': str(uuid.uuid4()),
            'name': name,
            'email': email
        }
        return jsonify({
            'success': True,
            'token': f'mock_token_{int(time.time())}',
            'user': mock_user
        })
    else:
        return jsonify({'success': False, 'message': 'Invalid data'}), 400

#@app.route('/discover', methods=['POST'])
def extract_entities(text):
    doc = nlp(text)
    entities = set()
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON", "GPE", "LOC", "WORK_OF_ART", "EVENT"]:
            entities.add(ent.text)
    return list(entities)

def build_prompt(entities, recommendations):
    prompt = (
        "You are a Moroccan poet and storyteller. "
        "Compose a 5-day itinerary based on the following cultural preferences:\n"
    )
    for cat in CATEGORIES:
        prompt += f"\n{cat.title()}:\n"
        names = []
        if cat in entities and entities[cat]:
            names += [e.get("name") for e in entities[cat] if e.get("name")]
        if cat in recommendations and recommendations[cat]:
            names += [r.get("name") for r in recommendations[cat] if r.get("name")]
        for name in names:
            prompt += f"- {name}\n"

    prompt += """
Generate an immersive and emotional journey through Morocco that follows this exact format:

🌟 Your Mystical Riḥla Through Morocco 🌟

🏜️ **Day 1: [Title] - [Subtitle]**
[Detailed description of the day's activities, experiences, and emotions]

🏛️ **Day 2: [Title] - [Subtitle]**
[Detailed description of the day's activities, experiences, and emotions]

🏔️ **Day 3: [Title] - [Subtitle]**
[Detailed description of the day's activities, experiences, and emotions]

🌊 **Day 4: [Title] - [Subtitle]**
[Detailed description of the day's activities, experiences, and emotions]

🌅 **Day 5: [Title] - [Subtitle]**
[Detailed description of the day's activities, experiences, and emotions]

✨ *Total Journey Investment: $[amount] per person*
🌙 *Best Time: [timeframe]*
🎭 *Cultural Immersion Level: [level]*

Make the descriptions poetic, immersive, and emotionally engaging. Use emojis for each day and write in a way that transports the reader to Morocco. Each day should be at least 2-3 sentences long with vivid sensory details.
"""
    return prompt

def generate_fallback_itinerary(user_input, entities):
    """Generate a fallback itinerary when Gemini API is unavailable"""
    
    # Create a Morocco-themed itinerary based on user interests
    base_themes = {
        'music': ['Gnawa music performances', 'traditional Andalusian music', 'desert blues concerts'],
        'art': ['Hassan II Mosque architecture', 'traditional crafts workshops', 'contemporary art galleries'],
        'food': ['tagine cooking classes', 'spice market tours', 'traditional mint tea ceremonies'],
        'history': ['ancient medinas exploration', 'Roman ruins visits', 'Berber cultural sites'],
        'nature': ['Sahara Desert camps', 'Atlas Mountains hiking', 'coastal walks in Essaouira']
    }
    
    # Determine main theme from user input
    main_theme = 'general'
    user_lower = user_input.lower()
    for theme, activities in base_themes.items():
        if theme in user_lower or any(word in user_lower for word in theme.split()):
            main_theme = theme
            break
    
    # Check entities for more specific themes
    if entities:
        for entity in entities:
            entity_lower = entity.lower()
            if 'music' in entity_lower or 'gnawa' in entity_lower:
                main_theme = 'music'
            elif 'art' in entity_lower or 'craft' in entity_lower:
                main_theme = 'art'
            elif 'food' in entity_lower or 'cuisine' in entity_lower:
                main_theme = 'food'
    
    fallback_itinerary = f"""🌟 Your Mystical Riḥla Through Morocco 🌟

🏜️ **Day 1: Arrival in Marrakech - The Red City Awakens**
Begin your journey in the heart of Morocco's imperial cities. Explore the vibrant Jemaa el-Fnaa square as snake charmers and storytellers weave their magic. Wander through the labyrinthine souks, where the scent of spices and the sound of traditional music fill the air. {base_themes.get(main_theme, ['Enjoy local experiences'])[0] if main_theme != 'general' else 'Immerse yourself in the bustling atmosphere'}. End your day with a traditional hammam experience.

🏛️ **Day 2: Fes - The Spiritual Capital**
Travel to Fes, Morocco's spiritual and intellectual capital. Visit the ancient University of Al-Qarawiyyin, one of the world's oldest universities. Explore the UNESCO World Heritage medina with its 9,000 narrow alleys. {base_themes.get(main_theme, ['Discover traditional crafts'])[1] if main_theme != 'general' and len(base_themes.get(main_theme, [])) > 1 else 'Witness master craftsmen at work in their traditional workshops'}. The tanneries offer a glimpse into centuries-old leather-making techniques.

🏔️ **Day 3: Atlas Mountains - Berber Villages**
Journey into the High Atlas Mountains to discover authentic Berber culture. Visit traditional villages where time seems to stand still. Learn about ancient customs and traditions passed down through generations. {base_themes.get(main_theme, ['Experience mountain culture'])[2] if main_theme != 'general' and len(base_themes.get(main_theme, [])) > 2 else 'Enjoy panoramic views and fresh mountain air'}. Share mint tea with local families and hear stories of mountain life.

🌊 **Day 4: Essaouira - The Wind City**
Discover the coastal charm of Essaouira, where Atlantic winds have shaped both landscape and culture. Explore the Portuguese-influenced medina and walk along the historic ramparts. {base_themes.get(main_theme, ['Enjoy coastal activities'])[0] if main_theme != 'general' else 'Watch fishermen bring in their daily catch'}. The city's artistic soul shines through its galleries and music scene.

🌅 **Day 5: Sahara Desert - Under the Stars**
Complete your journey with a magical night in the Sahara Desert. Ride camels across golden dunes as the sun sets over the endless landscape. Experience the profound silence of the desert and sleep under a canopy of stars. {base_themes.get(main_theme, ['Desert cultural experiences'])[0] if main_theme != 'general' else 'Listen to traditional Berber music around the campfire'}. This final experience will connect you deeply with Morocco's nomadic heritage.

✨ *Total Journey Investment: $1,200-1,800 per person*
🌙 *Best Time: October-April for perfect weather*
🎭 *Cultural Immersion Level: Deep and Authentic*

*Note: This itinerary was crafted with care during high demand. Your journey awaits!*"""

    return fallback_itinerary

@app.route("/trip", methods=["GET", "POST"])
def trip():
    itinerary = ""
    error = ""
    user_text = ""

    if request.method == "POST":
        user_text = request.form.get("preferences", "")
        try:
            extracted_entities_list = extract_entities(user_text)

            qloo_results = {}
            for ent in extracted_entities_list:
                res = search_qloo(ent)
                for cat in CATEGORIES:
                    if cat not in qloo_results:
                        qloo_results[cat] = []
                    qloo_results[cat].extend(res.get(cat, []))

            ids_by_cat = {
                cat: list({item["id"]: None for item in qloo_results.get(cat, []) if "id" in item}.keys())
                for cat in CATEGORIES
            }

            recos = get_recommendations(ids_by_cat)
            prompt = build_prompt(qloo_results, recos)
            itinerary = generate_itinerary(prompt)

        except Exception as e:
            error = f"Error: {e}"

    return render_template("trip.html", itinerary=itinerary, error=error, preferences=user_text)

@app.route('/api/test', methods=['GET'])
def test_api():
    """Simple test endpoint to verify API is working"""
    print("🔥 TEST API ENDPOINT CALLED - Backend is working!")
    return jsonify({
        'success': True,
        'message': 'Backend API is working!',
        'timestamp': int(time.time())
    })

@app.route('/api/weave-journey', methods=['POST'])
def weave_journey():
    """API endpoint for journey creation that returns JSON for the frontend"""
    try:
        print("\n🌟 REAL BACKEND API CALLED - Starting journey weaving...")
        data = request.get_json()
        user_text = data.get('soulThread', '')
        
        print(f"📝 User input received: {user_text[:100]}...")
        
        if not user_text:
            return jsonify({'success': False, 'message': 'Soul thread cannot be empty'}), 400
        
        # Extract entities from user input
        print("🔍 Extracting entities from user input...")
        extracted_entities_list = extract_entities(user_text)
        print(f"✨ Extracted entities: {extracted_entities_list}")

        # Search Qloo for each entity
        print("🔎 Searching Qloo API for recommendations...")
        qloo_results = {}
        for ent in extracted_entities_list:
            res = search_qloo(ent)
            for cat in CATEGORIES:
                if cat not in qloo_results:
                    qloo_results[cat] = []
                qloo_results[cat].extend(res.get(cat, []))

        # Get recommendation IDs by category
        ids_by_cat = {
            cat: list({item["id"]: None for item in qloo_results.get(cat, []) if "id" in item}.keys())
            for cat in CATEGORIES
        }
        print(f"🎯 Found recommendations for categories: {list(ids_by_cat.keys())}")

        # Get recommendations
        print("🌍 Getting detailed recommendations...")
        recos = get_recommendations(ids_by_cat)
        
        # Build prompt and generate itinerary
        print("🤖 Generating itinerary with Gemini AI...")
        prompt = build_prompt(qloo_results, recos)
        
        try:
            itinerary = generate_itinerary(prompt)
            print("🎉 REAL BACKEND SUCCESS - Journey generated successfully!")
            print(f"📜 Generated itinerary preview: {itinerary[:200]}...")
        except Exception as gemini_error:
            print(f"⚠️ Gemini API Error: {str(gemini_error)}")
            print("🔄 Falling back to mock itinerary...")
            # Generate a fallback itinerary based on user input
            itinerary = generate_fallback_itinerary(user_text, extracted_entities_list)
            print("🎭 Mock itinerary generated successfully!")

        return jsonify({
            'success': True,
            'itinerary': itinerary,
            'journey_title': 'Your Mystical Riḥla Through Morocco',
            'user_input': user_text
        })

    except Exception as e:
        print(f"❌ REAL BACKEND ERROR: {str(e)}")
        return jsonify({
            'success': False, 
            'message': f'Error generating journey: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
