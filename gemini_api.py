

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")

def generate_itinerary(prompt):
    response = gemini_model.generate_content(prompt)
    return response.text if response else "No itinerary generated."
