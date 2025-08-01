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
