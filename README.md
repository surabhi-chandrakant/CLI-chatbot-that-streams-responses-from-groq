# 🤖 Groq AI Chatbot Dashboard

An interactive web dashboard for a CLI chatbot that streams real-time responses from Groq's powerful Llama 3.3 70B model. Features a beautiful glass-morphism UI, conversation history, chat export, and one-click API testing.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![Groq](https://img.shields.io/badge/Groq-API-purple.svg)](https://console.groq.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## ✨ Features

- **Real-time Streaming** – Watch responses generate token by token
- **Beautiful Dashboard** – Modern glass-morphism UI with smooth animations
- **Conversation Memory** – Maintains context within a session
- **Export Chat History** – Save conversations as text files
- **API Health Check** – One-click test to verify Groq API connectivity
- **Responsive Design** – Works on desktop and tablet devices
- **Fast & Free** – Uses Groq’s free tier (30 requests/minute)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A free Groq API key ([Get one here](https://console.groq.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/surabhi-chandrakant/CLI-chatbot-that-streams-responses-from-groq.git
   cd CLI-chatbot-that-streams-responses-from-groq

   python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

pip install -r requirements.txt

.env 

GROQ_API_KEY=gsk_your_api_key_here

python app.py


 Testing the API
Click the "Test API" button in the sidebar to verify your connection. A success message will confirm the model is ready.

📦 Deployment
Deploy on Render (Free Tier)
Push this repository to GitHub.

Log in to Render.com.

Click "New +" → "Web Service".

Connect your GitHub repository.

Use these settings:

Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app

Add the environment variable GROQ_API_KEY with your key.

Click "Deploy".

A render.yaml is included for automated deployment.

🛠️ Built With
Backend: Flask, Flask-CORS, Requests

Frontend: HTML5, CSS3, JavaScript (ES6)

API: Groq Cloud (Llama 3.3 70B model)

Deployment: Gunicorn, Render

###  project structure 

.
├── app.py              # Flask backend with streaming endpoints
├── requirements.txt    # Python dependencies
├── render.yaml         # Render.com deployment configuration
├── .gitignore          # Ignored files (API keys, caches, etc.)
├── templates/
│   └── index.html      # Frontend dashboard UI
└── README.md           # This file

### Usage Example

User: What is artificial intelligence?
AI: Artificial Intelligence (AI) is the simulation of human intelligence in machines...
