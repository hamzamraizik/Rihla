# 🌟 Riḥla - Journey of the Soul

**Riḥla** (Arabic: رحلة, meaning "journey") is an AI-powered travel itinerary generator that creates personalized, culturally immersive 5-day journeys through Morocco. Using advanced natural language processing and cultural intelligence APIs, Riḥla transforms your travel preferences into mystical, poetic travel experiences.

## 📬 Contact & Notes

This project is currently in its **first beta/demo version**, developed as part of a hackathon submission. Some aspects are still under development and may require further customization or improvement.

If you face any issues during installation or testing, feel free to contact me:

- 📧 **Email**: hamzamraizik2004@gmail.com 

Your feedback is highly appreciated!


## ✨ Features

- **AI-Powered Itinerary Generation**: Uses Google Gemini AI to create personalized travel experiences
- **Cultural Intelligence**: Integrates with Qloo API for culture-aware recommendations
- **Natural Language Processing**: Extracts meaningful entities from user preferences using spaCy
- **Beautiful Web Interface**: Modern, responsive frontend with Moroccan-inspired design
- **Fallback System**: Intelligent fallback when external APIs are unavailable
- **Mock Authentication**: Ready-to-extend authentication system for user management
- **Cross-Platform**: Works on any device with a web browser

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **spaCy** - Natural language processing for entity extraction
- **Google Gemini AI** - Advanced text generation for itineraries
- **Qloo API** - Cultural recommendations and insights
- **Flask-CORS** - Cross-origin resource sharing support

### Frontend
- **HTML5/CSS3** - Modern web standards
- **JavaScript** - Interactive user experience
- **Responsive Design** - Mobile-first approach
- **Moroccan-inspired UI** - Cultural design elements

## 📋 Prerequisites

Before running Riḥla, ensure you have:

- **Python 3.7+** installed on your system
- **pip** (Python package installer)
- **Internet connection** for API access
- **API Keys** (see configuration section)

## 🚀 Quick Start

### 1. Download the Project
```bash
# If you have the project as a zip file, extract it
# If you have git access:
git clone <repository-url>
cd Rihla-main
```

### 2. Set Up Environment Variables
Copy the example environment file and configure your API keys:

```bash
cp .env.example .env
```

Edit the `.env` file with your API keys:
```bash
# API Keys required for the Rihla application
GEMINI_API_KEY=your_gemini_api_key_here
QLOO_API_KEY=your_qloo_api_key_here
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install spaCy Language Model
```bash
python -m spacy download en_core_web_sm
```

### 5. Run the Application

#### Option A: Using the provided start script (Recommended)
```bash
chmod +x start.sh
./start.sh
```

#### Option B: Direct Python execution
```bash
python app.py
```

### 6. Access the Application
Open your web browser and navigate to:
```
http://localhost:5001
```

## 🔑 API Keys Configuration

### Getting Your API Keys

#### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and add it to your `.env` file

#### Qloo API Key
1. Visit [Qloo Developer Portal](https://developer.qloo.com/)
2. Sign up for a developer account
3. Request access to the API
4. Copy the provided API key to your `.env` file

**Note**: The application includes intelligent fallback mechanisms, so it will work even if one API is temporarily unavailable.

## 🎯 How to Use Riḥla

### Step-by-Step User Guide

1. **Open the Application**
   - Navigate to `http://localhost:5001` in your browser
   - You'll see the beautiful Riḥla homepage

2. **Describe Your Travel Preferences**
   - Click on the journey input area
   - Describe your interests, preferred activities, or cultural preferences
   - Examples:
     - "I love traditional music and want to experience authentic Moroccan cuisine"
     - "I'm interested in history, architecture, and desert adventures"
     - "Art galleries, local crafts, and mountain hiking appeal to me"

3. **Generate Your Journey**
   - Click the "Weave My Journey" button
   - The AI will process your preferences
   - Cultural recommendations are gathered from Qloo
   - A personalized 5-day itinerary is generated

4. **Review Your Mystical Riḥla**
   - Your itinerary will appear with:
     - Daily activities and experiences
     - Cultural insights and recommendations
     - Estimated costs and best travel times
     - Poetic descriptions that transport you to Morocco

## 📱 Application Features

### Main Interface (`/`)
- **Beautiful Landing Page**: Moroccan-inspired design with cultural elements
- **Journey Input**: Natural language input for travel preferences
- **Responsive Design**: Works perfectly on desktop and mobile devices

### Journey Generation (`/api/weave-journey`)
- **AI Processing**: Advanced natural language understanding
- **Cultural Integration**: Qloo API for authentic recommendations
- **Smart Fallbacks**: Works even when external APIs are down
- **Real-time Feedback**: Live updates during processing

### Legacy Interface (`/trip`)
- **Simple Form**: Basic form-based input
- **Direct Processing**: Immediate itinerary generation
- **Error Handling**: Clear error messages and feedback

## 🏗️ Project Structure

```
Rihla-main/
├── app.py                          # Main Flask application
├── gemini_api.py                   # Google Gemini AI integration
├── qloo_api.py                     # Qloo cultural API integration
├── requirements.txt                # Python dependencies
├── start.sh                        # Startup script
├── .env.example                    # Environment variables template
├── static/
│   └── Rihla_background.png       # Background image assets
├── templates/
│   ├── frontend_index.html        # Main application interface
│   ├── index.html                 # Basic index page
│   ├── trip.html                  # Legacy trip planning interface
│   └── journey_styles_patch.css   # Additional styling
└── __pycache__/                   # Python cache files
```

## 🔧 Configuration Options

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini AI API key
- `QLOO_API_KEY`: Your Qloo cultural intelligence API key

### Application Settings
- **Port**: Default is 5001 (configurable in `app.py`)
- **Debug Mode**: Enabled by default for development
- **CORS**: Enabled for cross-origin requests

## 🛠️ Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python app.py
```

### Adding New Features
1. **Cultural Categories**: Modify `CATEGORIES` in `qloo_api.py`
2. **Itinerary Formats**: Update the prompt template in `app.py`
3. **UI Customization**: Edit templates in the `templates/` directory
4. **API Endpoints**: Add new routes in `app.py`

## 📝 API Reference

### Endpoints

#### `POST /api/weave-journey`
Creates a personalized journey based on user preferences.

**Request Body:**
```json
{
  "soulThread": "Your travel preferences and interests"
}
```

**Response:**
```json
{
  "success": true,
  "itinerary": "Generated 5-day itinerary...",
  "journey_title": "Your Mystical Riḥla Through Morocco",
  "user_input": "User's original input"
}
```

#### `GET /api/test`
Simple endpoint to verify the API is working.

#### `POST /auth/login` & `POST /auth/register`
Mock authentication endpoints for future user management features.

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. **"Module not found" errors**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Install spaCy language model
python -m spacy download en_core_web_sm
```

#### 2. **"API key not found" errors**
- Verify your `.env` file exists and contains valid API keys
- Ensure the `.env` file is in the same directory as `app.py`
- Check that your API keys are active and have proper permissions

#### 3. **"Port already in use" errors**
```bash
# Find and kill the process using port 5001
lsof -ti:5001 | xargs kill -9

# Or change the port in app.py
app.run(debug=True, host='0.0.0.0', port=5002)
```

#### 4. **spaCy model not found**
```bash
# Download the required English language model
python -m spacy download en_core_web_sm
```

#### 5. **CORS errors in browser**
- The application includes CORS support
- If issues persist, check your browser's console for specific errors

### Getting Help
- Check the console output for detailed error messages
- Verify all dependencies are correctly installed
- Ensure your API keys are valid and active
- Try the fallback mode if external APIs are unavailable

## 🌟 Usage Examples

### Example User Inputs

**Cultural Explorer:**
```
"I'm fascinated by traditional Moroccan music, especially Gnawa, and I love exploring ancient architecture and learning about local crafts."
```

**Adventure Seeker:**
```
"I want to experience the Sahara Desert, hike in the Atlas Mountains, and taste authentic Moroccan cuisine in local markets."
```

**Art Enthusiast:**
```
"Contemporary art galleries, traditional pottery workshops, and Islamic calligraphy are my passions. I also enjoy photography."
```

## 🎨 Customization

### Theming
The application supports both light and dark themes with Moroccan-inspired color schemes:
- **Moroccan Terracotta**: #D4704F
- **Deep Desert**: #1A2F47
- **Sahara Gold**: #E6B368
- **Atlas Blue**: #2C5282

### Adding New Destinations
To extend beyond Morocco:
1. Update the prompt template in `build_prompt()` function
2. Modify the fallback itinerary generator
3. Adjust cultural categories in `qloo_api.py`

## 📄 License

This project is open source. Please check with the project maintainers for specific license terms.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🌍 About Riḥla

Riḥla (رحلة) means "journey" in Arabic and refers to the traditional Islamic travel literature genre. This application honors that tradition by creating meaningful, culturally-rich travel experiences that go beyond typical tourism to offer genuine cultural immersion and understanding.

---

**Made with ❤️ for travelers seeking authentic cultural experiences**

*Journey into the soul of Morocco with AI-powered cultural intelligence.*
