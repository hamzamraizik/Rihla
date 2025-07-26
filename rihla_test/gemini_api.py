
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

def generate_travel_narrative(entities, recommendations):
    prompt = """
You are a Moroccan poet and storyteller. Compose a 5-day itinerary based on the following cultural preferences:
"""
    for cat in entities:
        prompt += f"\n{cat.title()}:\n"
        names = [item.get("name") for item in entities[cat]] + [r.get("name") for r in recommendations.get(cat, [])]
        for name in names:
            if name:
                prompt += f"- {name}\n"
    prompt += """

Generate an immersive and emotional journey through Morocco. Structure:
Day 1: ...
Day 2: ...
... up to Day 5.
"""
    response = model.generate_content(prompt)
    return response.text if response else "No itinerary generated."
