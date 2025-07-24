#!/usr/bin/env python3
from flask import Flask, render_template, send_from_directory, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/Rihla_background.png')
def background_image():
    # Serve from static folder
    return send_file('static/Rihla_background.png')

if __name__ == '__main__':
    print("🚀 Starting Riḥla server...")
    print("📍 Background image available at: http://localhost:5000/static/Rihla_background.png")
    print("🌐 Landing page at: http://localhost:5000")
    app.run(debug=True, port=5000)
