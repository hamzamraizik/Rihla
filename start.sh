#!/bin/bash

# Riḥla - Journey of the Soul
# Startup script

echo "🌟 Starting Riḥla - Journey of the Soul..."

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    echo "💡 Usage: cd backend && ./start.sh"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    echo "💡 Please copy .env.example to .env and add your API keys"
    echo "   cp .env.example .env"
    exit 1
fi

# Check if requirements are installed
echo "📦 Checking dependencies..."
python3 -c "import flask, flask_cors, requests, google.generativeai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependencies not found. Installing..."
    pip install -r requirements.txt
fi

echo "🚀 Starting Flask application..."
echo "🌐 Open your browser to: http://localhost:5000"
echo "🔑 Make sure your API keys are set in .env"
echo ""

python3 app.py
