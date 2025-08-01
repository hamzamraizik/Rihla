
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

def build_prompt(user_input, entities, recommendations):
    """Build a dynamic, creative prompt that incorporates user's specific desires and interests"""
    
    # Analyze user input for emotions, themes, and specific interests
    user_lower = user_input.lower()
    
    # Detect emotional tone and travel style
    emotional_keywords = {
        'adventure': ['adventure', 'exciting', 'thrill', 'explore', 'discover', 'wild', 'extreme'],
        'peaceful': ['peaceful', 'calm', 'serene', 'quiet', 'meditation', 'relax', 'tranquil'],
        'cultural': ['culture', 'history', 'tradition', 'authentic', 'local', 'heritage'],
        'romantic': ['romantic', 'love', 'couple', 'intimate', 'sunset', 'beautiful'],
        'spiritual': ['spiritual', 'soul', 'enlighten', 'sacred', 'pilgrimage', 'divine'],
        'luxury': ['luxury', 'premium', 'exclusive', 'comfort', 'high-end', 'sophisticated'],
        'budget': ['budget', 'cheap', 'affordable', 'backpack', 'simple', 'modest']
    }
    
    detected_themes = []
    for theme, keywords in emotional_keywords.items():
        if any(keyword in user_lower for keyword in keywords):
            detected_themes.append(theme)
    
    # If no specific themes detected, default to cultural
    if not detected_themes:
        detected_themes = ['cultural']
    
    # Create a unique random seed based on user input to ensure variety
    import hashlib
    import random
    seed = int(hashlib.md5(user_input.encode()).hexdigest()[:8], 16)
    random.seed(seed)
    
    # Moroccan cities and regions for variety
    moroccan_locations = [
        'Marrakech', 'Fes', 'Chefchaouen', 'Essaouira', 'Casablanca', 'Rabat',
        'Meknes', 'Ouarzazate', 'Merzouga', 'Imlil', 'Dades Valley', 'Ait Benhaddou',
        'Tangier', 'Asilah', 'Ifrane', 'Todra Gorge', 'Agadir', 'Taghazout'
    ]
    
    # Build the enhanced prompt
    prompt = f"""You are Ibn Battuta reborn, a mystical Moroccan storyteller and the greatest travel poet of all time. A soul has shared their deepest travel desires with you: "{user_input}"

As their spiritual guide, weave a completely unique 5-day Riḥla (mystical journey) through Morocco that captures their essence. Make this journey feel like it was crafted specifically for their soul.

🎭 THEIR SOUL SEEKS: {', '.join(detected_themes).title()} experiences
🌍 INCORPORATE THESE INSPIRATIONS (but don't limit yourself to them):"""

    # Add cultural inspirations from APIs
    inspiration_count = 0
    for cat in ["film", "music", "book", "travel", "cuisine"]:  # CATEGORIES
        items = []
        if cat in entities and entities[cat]:
            items += [e.get("name") for e in entities[cat] if e.get("name")][:3]
        if cat in recommendations and recommendations[cat]:
            items += [r.get("name") for r in recommendations[cat] if r.get("name")][:2]
        
        if items and inspiration_count < 15:  # Limit to avoid overwhelming
            prompt += f"
🎨 {cat.title()}: {', '.join(items[:3])}"
            inspiration_count += len(items[:3])

    # Select random locations to ensure variety
    selected_locations = random.sample(moroccan_locations, min(5, len(moroccan_locations)))
    
    prompt += f"""

🗺️ SUGGESTED MOROCCAN GEMS TO CONSIDER: {', '.join(selected_locations)}

Now create their UNIQUE mystical journey following this format:

🌟 Your Mystical Riḥla Through Morocco 🌟
*"A journey woven for your soul based on: {user_input[:50]}..."*

🏜️ **Day 1: [Poetic Title] - [Emotional Subtitle]**
[Create a vivid, sensory-rich opening day that directly reflects their stated desires. Make it feel personal and unique to their input. Include specific activities, sights, sounds, smells, and emotions they'll experience. Reference their interests subtly.]

🏛️ **Day 2: [Poetic Title] - [Emotional Subtitle]**
[Design a day that builds on Day 1 but explores a different facet of their personality/interests. Make each location and activity feel carefully chosen for them specifically.]

🏔️ **Day 3: [Poetic Title] - [Emotional Subtitle]**
[Create the journey's emotional peak - something that would truly move them based on what they've shared. Make it transformative.]

🌊 **Day 4: [Poetic Title] - [Emotional Subtitle]**
[Design a day that reflects and deepens their journey. Show how Morocco is changing them.]

🌅 **Day 5: [Poetic Title] - [Emotional Subtitle]**
[Create a powerful conclusion that brings their journey full circle and connects to their original desires. Make it unforgettable.]

✨ *Total Journey Investment: $[realistic amount] per person*
🌙 *Best Time: [specific months based on activities]*
🎭 *Cultural Immersion Level: [High/Medium/Mystical]*

CREATIVE REQUIREMENTS:
- Make each day title poetic and evocative
- Write as if you're composing an epic poem about their specific journey
- Include rich sensory details (sounds, smells, textures, colors)
- Reference their specific interests and desires throughout
- Make activities feel personally curated for them
- Use different Moroccan locations and experiences for variety
- Write in second person ("you will...", "your soul will...")
- Include specific cultural elements that match their vibe
- Make each paragraph flow like a beautiful story
- Ensure no day feels generic or template-like

Remember: This is THEIR unique Riḥla, not a generic Morocco trip. Every detail should feel intentionally chosen for their soul."""

    return prompt


def generate_fallback_itinerary(user_input, entities):
    """Generate a dynamic fallback itinerary when Gemini API is unavailable"""
    
    import hashlib
    import random
    
    # Create a unique seed based on user input for variety
    seed = int(hashlib.md5(user_input.encode()).hexdigest()[:8], 16)
    random.seed(seed)
    
    user_lower = user_input.lower()
    
    # Analyze user input for themes and emotions
    themes = {
        'adventure': ['adventure', 'exciting', 'thrill', 'explore', 'discover', 'active'],
        'peaceful': ['peaceful', 'calm', 'serene', 'quiet', 'meditation', 'relax'],
        'cultural': ['culture', 'history', 'tradition', 'authentic', 'local', 'heritage'],
        'romantic': ['romantic', 'love', 'couple', 'intimate', 'sunset'],
        'spiritual': ['spiritual', 'soul', 'enlighten', 'sacred', 'divine'],
        'artistic': ['art', 'creative', 'music', 'craft', 'design', 'beautiful'],
        'culinary': ['food', 'cuisine', 'taste', 'cooking', 'flavor', 'eat']
    }
    
    detected_themes = []
    for theme, keywords in themes.items():
        if any(keyword in user_lower for keyword in keywords):
            detected_themes.append(theme)
    
    if not detected_themes:
        detected_themes = ['cultural']
    
    # Dynamic activities based on themes
    theme_activities = {
        'adventure': {
            'locations': ['Atlas Mountains', 'Todra Gorge', 'Merzouga Dunes', 'Imlil Valley'],
            'activities': ['mountain hiking', 'rock climbing', 'sandboarding', 'quad biking'],
            'experiences': ['sunrise camel trek', 'canyoning adventure', 'desert camping under stars']
        },
        'peaceful': {
            'locations': ['Ifrane', 'Chefchaouen', 'Essaouira gardens', 'Ourika Valley'],
            'activities': ['meditation sessions', 'peaceful walks', 'spa treatments', 'yoga'],
            'experiences': ['sunrise meditation', 'tranquil garden visits', 'healing hammam rituals']
        },
        'cultural': {
            'locations': ['Fes medina', 'Meknes', 'Volubilis', 'Ait Benhaddou'],
            'activities': ['artisan workshops', 'historical tours', 'traditional performances'],
            'experiences': ['meeting master craftsmen', 'traditional music shows', 'storytelling sessions']
        },
        'romantic': {
            'locations': ['Marrakech', 'Essaouira', 'Ouarzazate', 'Dades Valley'],
            'activities': ['sunset dinners', 'private tours', 'couple\'s spa', 'rooftop experiences'],
            'experiences': ['candlelit dinners', 'private desert camp', 'romantic sunset rides']
        },
        'spiritual': {
            'locations': ['Fes', 'Moulay Idriss', 'Hassan II Mosque', 'Sahara Desert'],
            'activities': ['mosque visits', 'pilgrimage sites', 'meditation retreats'],
            'experiences': ['spiritual ceremonies', 'sacred site visits', 'desert contemplation']
        },
        'artistic': {
            'locations': ['Marrakech souks', 'Essaouira', 'Tetouan', 'Safi'],
            'activities': ['pottery workshops', 'painting classes', 'music sessions', 'gallery visits'],
            'experiences': ['creating with master artists', 'traditional craft learning', 'art gallery tours']
        },
        'culinary': {
            'locations': ['Marrakech', 'Fes', 'Tangier', 'Casablanca'],
            'activities': ['cooking classes', 'market tours', 'food tastings', 'spice workshops'],
            'experiences': ['tagine cooking', 'spice market exploration', 'traditional tea ceremonies']
        }
    }
    
    # Select primary theme for the journey
    primary_theme = detected_themes[0] if detected_themes else 'cultural'
    
    # Get activities for the primary theme
    theme_data = theme_activities.get(primary_theme, theme_activities['cultural'])
    
    # Moroccan cities pool for variety
    all_cities = ['Marrakech', 'Fes', 'Chefchaouen', 'Essaouira', 'Casablanca', 'Rabat',
                  'Meknes', 'Ouarzazate', 'Merzouga', 'Imlil', 'Tangier', 'Asilah']
    
    # Select 5 different locations
    selected_locations = random.sample(theme_data['locations'] + all_cities, 5)
    
    # Price range based on theme
    price_ranges = {
        'adventure': (1400, 2200),
        'peaceful': (1200, 1800),
        'cultural': (1000, 1600),
        'romantic': (1800, 2800),
        'spiritual': (900, 1500),
        'artistic': (1300, 2000),
        'culinary': (1500, 2300)
    }
    
    min_price, max_price = price_ranges.get(primary_theme, (1200, 1800))
    price = random.randint(min_price, max_price)
    
    # Generate themed days
    days = [
        {
            'title': f"Arrival in {selected_locations[0]}",
            'subtitle': "The Journey Begins",
            'location': selected_locations[0],
            'activities': theme_data['activities'][:2],
            'experience': theme_data['experiences'][0] if theme_data['experiences'] else 'immersive local experiences'
        },
        {
            'title': f"Exploring {selected_locations[1]}",
            'subtitle': "Deeper Discoveries", 
            'location': selected_locations[1],
            'activities': theme_data['activities'][1:3] if len(theme_data['activities']) > 1 else theme_data['activities'],
            'experience': theme_data['experiences'][1] if len(theme_data['experiences']) > 1 else 'authentic cultural encounters'
        },
        {
            'title': f"Heart of {selected_locations[2]}",
            'subtitle': "Soul Connection",
            'location': selected_locations[2],
            'activities': theme_data['activities'][2:] if len(theme_data['activities']) > 2 else theme_data['activities'],
            'experience': theme_data['experiences'][2] if len(theme_data['experiences']) > 2 else 'transformative moments'
        },
        {
            'title': f"Journey to {selected_locations[3]}",
            'subtitle': "New Perspectives",
            'location': selected_locations[3],
            'activities': random.sample(theme_data['activities'], min(2, len(theme_data['activities']))),
            'experience': random.choice(theme_data['experiences']) if theme_data['experiences'] else 'meaningful connections'
        },
        {
            'title': f"Farewell in {selected_locations[4]}",
            'subtitle': "Integration & Reflection",
            'location': selected_locations[4],
            'activities': ['reflection sessions', 'final experiences', 'departure preparations'],
            'experience': 'closure and integration of your journey'
        }
    ]
    
    # Build the itinerary
    itinerary = f"""🌟 Your Mystical Riḥla Through Morocco 🌟
*"A {primary_theme} journey woven for your soul based on: {user_input[:60]}..."*

"""
    
    emojis = ['🏜️', '🏛️', '🏔️', '🌊', '��']
    
    for i, day in enumerate(days):
        activities_text = ', '.join(day['activities'][:2])
        
        day_description = f"""Your journey to {day['location']} unfolds with {activities_text}. """
        
        if primary_theme == 'adventure':
            day_description += f"Feel your heart race as you engage in {day['experience']}. The rugged beauty of Morocco challenges and inspires you."
        elif primary_theme == 'peaceful':
            day_description += f"Allow the tranquil energy of this place to wash over you during {day['experience']}. Find deep inner peace."
        elif primary_theme == 'cultural':
            day_description += f"Immerse yourself in centuries-old traditions through {day['experience']}. Connect with Morocco's rich heritage."
        elif primary_theme == 'romantic':
            day_description += f"Share intimate moments during {day['experience']}. Let Morocco's beauty deepen your connection."
        elif primary_theme == 'spiritual':
            day_description += f"Open your soul to divine experiences through {day['experience']}. Discover sacred wisdom."
        elif primary_theme == 'artistic':
            day_description += f"Express your creativity through {day['experience']}. Let Morocco's artistry inspire your own."
        elif primary_theme == 'culinary':
            day_description += f"Savor the exquisite flavors during {day['experience']}. Taste the soul of Moroccan cuisine."
        else:
            day_description += f"Experience the magic through {day['experience']}. Let Morocco transform you."
        
        itinerary += f"""{emojis[i]} **Day {i+1}: {day['title']} - {day['subtitle']}**
{day_description} The sights, sounds, and aromas create a symphony for your senses, leaving you forever changed.

"""
    
    # Seasonal recommendation based on theme
    seasons = {
        'adventure': 'March-May, September-November',
        'peaceful': 'October-April',
        'cultural': 'October-May',
        'romantic': 'April-June, September-November', 
        'spiritual': 'Year-round',
        'artistic': 'October-May',
        'culinary': 'October-May'
    }
    
    season = seasons.get(primary_theme, 'October-May')
    
    itinerary += f"""✨ *Total Journey Investment: ${price:,} per person*
🌙 *Best Time: {season}*
🎭 *Cultural Immersion Level: Mystical*

*This {primary_theme} journey has been crafted specifically for your soul's calling.*"""
    
    return itinerary



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
            prompt = build_prompt(user_text, qloo_results, recos)
            itinerary = generate_itinerary(prompt)
            if not itinerary:
                print("🔄 Gemini returned None, using fallback...")
                itinerary = generate_fallback_itinerary(user_text, extracted_entities_list)

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
        prompt = build_prompt(user_text, qloo_results, recos)
        
        try:
            itinerary = generate_itinerary(prompt)
            if not itinerary:
                print("🔄 Gemini returned None, using fallback...")
                itinerary = generate_fallback_itinerary(user_text, extracted_entities_list)
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
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))

# Add debug endpoint to test prompt generation
@app.route('/api/debug-prompt', methods=['POST'])
def debug_prompt():
    """Debug endpoint to see what prompt is being generated"""
    try:
        data = request.get_json()
        user_text = data.get('soulThread', '')
        
        # Extract entities
        extracted_entities_list = extract_entities(user_text)
        
        # Search Qloo
        qloo_results = {}
        for ent in extracted_entities_list:
            res = search_qloo(ent)
            for cat in CATEGORIES:
                if cat not in qloo_results:
                    qloo_results[cat] = []
                qloo_results[cat].extend(res.get(cat, []))

        # Get recommendations
        ids_by_cat = {
            cat: list({item["id"]: None for item in qloo_results.get(cat, []) if "id" in item}.keys())
            for cat in CATEGORIES
        }
        recos = get_recommendations(ids_by_cat)
        
        # Build prompt
        prompt = build_prompt(user_text, qloo_results, recos)
        
        return jsonify({
            'success': True,
            'user_input': user_text,
            'extracted_entities': extracted_entities_list,
            'qloo_results_count': {cat: len(items) for cat, items in qloo_results.items()},
            'recommendations_count': {cat: len(items) for cat, items in recos.items()},
            'generated_prompt': prompt[:1000] + "..." if len(prompt) > 1000 else prompt
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
