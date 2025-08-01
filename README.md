# 🌟 Riḥla - Journey of the Soul

> *"Not all those who wander are lost"* - Create your mystical journey through Morocco with AI

Riḥla (Arabic: رحلة, meaning "journey") is an AI-powered travel planning application that creates personalized, poetic journeys through Morocco based on your soul's desires and cultural interests.

## ✨ What Makes Riḥla Special?

- 🎭 **AI-Powered Personalization**: Uses Google Gemini AI to create unique journeys
- 🧠 **Smart Theme Detection**: Analyzes your input to detect travel themes (adventure, peaceful, romantic, cultural, etc.)
- 🎨 **Cultural Intelligence**: Integrates with Qloo API for music, art, food, and cultural recommendations
- 📝 **Poetic Storytelling**: Each journey is written like an epic poem by Ibn Battuta
- 🌍 **Authentic Morocco**: Features real locations and authentic cultural experiences
- 🔄 **Dynamic Content**: Every input generates a completely unique journey

## 🚀 Quick Start (For Everyone!)

### Step 1: Get the Code
```bash
git clone https://github.com/hamzamraizik/Rihla.git
cd Rihla
```

### Step 2: Set Up Your Environment
You'll need API keys (don't worry, they're free!):

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Get your FREE API keys:**
   
   **🤖 Google Gemini API (Free):**
   - Go to [Google AI Studio](https://aistudio.google.com/)
   - Click "Get API Key" 
   - Create a new API key
   - Copy it
   
   **🎵 Qloo API (Free for developers):**
   - Go to [Qloo Developer Portal](https://api.qloo.com/)
   - Sign up for free
   - Get your API key

3. **Add your keys to `.env` file:**
   ```bash
   # Open .env file and add your keys:
   GEMINI_API_KEY=your_gemini_key_here
   QLOO_API_KEY=your_qloo_key_here
   ```

### Step 3: Run the Application

**🐍 If you have Python:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

**🔧 Or use the startup script:**
```bash
chmod +x start.sh
./start.sh
```

### Step 4: Open Your Browser
Go to: `http://localhost:5001`

## 🎯 How to Use Riḥla

1. **Share Your Soul's Desires**: Type what kind of journey you want
   - *"I want a peaceful spiritual journey to find inner peace"*
   - *"Looking for an adventurous thrilling experience"*
   - *"Romantic getaway with beautiful sunsets"*
   - *"Cultural immersion in authentic traditions"*

2. **Let AI Weave Your Journey**: The AI analyzes your input and creates a unique 5-day Riḥla

3. **Discover Your Mystical Morocco**: Get a personalized, poetic journey with:
   - Day-by-day itineraries
   - Emotional storytelling
   - Real cultural experiences
   - Pricing and best travel times

## 🛠️ For Developers

### Tech Stack
- **Backend**: Python Flask
- **AI**: Google Gemini 1.5 Flash
- **Cultural Data**: Qloo API
- **NLP**: spaCy
- **Frontend**: HTML, CSS, JavaScript

### Project Structure
```
Riḥla/
├── app.py              # Main Flask application
├── gemini_api.py       # Google Gemini AI integration
├── qloo_api.py         # Qloo cultural data API
├── requirements.txt    # Python dependencies
├── start.sh           # Easy startup script
├── .env.example       # Environment variables template
├── static/            # Images and assets
├── templates/         # HTML templates
└── README.md          # This file
```

### Key Features Implementation

**🧠 Smart Theme Detection:**
```python
emotional_keywords = {
    'adventure': ['adventure', 'exciting', 'thrill', 'explore'],
    'peaceful': ['peaceful', 'calm', 'serene', 'meditation'],
    'cultural': ['culture', 'history', 'tradition', 'authentic'],
    # ... more themes
}
```

**🎨 Dynamic Prompt Engineering:**
- Analyzes user input for emotional themes
- Creates unique seed based on input hash for reproducible variety
- Incorporates cultural recommendations from Qloo API
- Uses Ibn Battuta persona for poetic storytelling

**🔄 Intelligent Fallback System:**
- When Gemini API is unavailable, uses theme-aware fallback
- Still analyzes user input for personalization
- Maintains quality and uniqueness

### API Endpoints

- `GET /` - Main application
- `POST /api/weave-journey` - Generate journey (main endpoint)
- `POST /api/debug-prompt` - Debug prompt generation
- `GET /api/test` - Test API connectivity

## 🚀 Deploy Your Demo

### Option 1: Render (Recommended)
1. Fork this repository
2. Connect to [Render.com](https://render.com)
3. Add environment variables in Render dashboard
4. Deploy!

### Option 2: Railway
1. Connect repository to [Railway.app](https://railway.app)
2. Set environment variables
3. One-click deploy!

### Option 3: Heroku
```bash
heroku create your-rihla-app
heroku config:set GEMINI_API_KEY=your_key
heroku config:set QLOO_API_KEY=your_key
git push heroku main
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ibn Battuta** - The greatest traveler in history, our spiritual guide
- **Morocco** - The land of mystical journeys and rich culture
- **Google Gemini** - For powering our AI storytelling
- **Qloo** - For cultural intelligence and recommendations

## 🆘 Troubleshooting

**"Dependencies not found"**
```bash
pip install -r requirements.txt
```

**"API Key not working"**
- Make sure your `.env` file has the correct keys
- Check that keys are valid and not expired

**"Port already in use"**
- The app runs on port 5001 by default
- Check if another app is using this port

**"Gemini API Error"**
- App automatically falls back to mock data
- Check your internet connection and API key

## 🌟 Example Journeys

**Input:** *"I want a peaceful spiritual journey"*
**Output:** A 5-day mystical journey through Chefchaouen, Fes, and the Sahara focusing on meditation, sacred sites, and inner peace.

**Input:** *"Adventure and thrills in Morocco"*
**Output:** An action-packed journey through the Atlas Mountains, Todra Gorge, and desert with hiking, climbing, and extreme sports.

---

*Made with ❤️ for wanderers and dreamers seeking their perfect Riḥla*
