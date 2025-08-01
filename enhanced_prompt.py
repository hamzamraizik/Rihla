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
            prompt += f"\n🎨 {cat.title()}: {', '.join(items[:3])}"
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
