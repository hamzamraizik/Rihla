import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def generate_itinerary(prompt):
    """Generate itinerary with enhanced creativity settings"""
    try:
        # Use enhanced model configuration for more creative and varied responses
        generation_config = genai.types.GenerationConfig(
            temperature=0.9,  # High temperature for creativity
            top_p=0.95,       # High top_p for diversity
            top_k=50,         # Allow more token choices
            max_output_tokens=2048,  # Longer responses
        )
        
        model = genai.GenerativeModel(
            "models/gemini-1.5-flash",
            generation_config=generation_config
        )
        
        response = model.generate_content(prompt)
        return response.text if response else "No itinerary generated."
        
    except Exception as e:
        print(f"⚠️ Gemini API Error: {str(e)}")
        return None  # Return None so fallback can be used
