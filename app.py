#!/usr/bin/env python3
import os
import json
import requests
from flask import Flask, Response, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Current working models as of 2026
WORKING_MODELS = [
    "llama-3.3-70b-versatile",    # Most capable, 70B parameters
    "llama-3.1-8b-instant",        # Fastest, 8B parameters  
    "gemma2-9b-it",                # Google's Gemma 2
    "qwen-2.5-32b",               # Qwen 2.5 32B
]

DEFAULT_MODEL = "llama-3.3-70b-versatile"

print(f"API Key loaded: {'✓' if GROQ_API_KEY else '✗ Missing!'}")
print(f"Using model: {DEFAULT_MODEL}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/test', methods=['GET'])
def test_api():
    """Test if Groq API is working with current model"""
    if not GROQ_API_KEY:
        return jsonify({'error': 'API key missing'}), 500
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": DEFAULT_MODEL,
        "messages": [{"role": "user", "content": "Say 'API is working'"}],
        "stream": False
    }
    
    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            return jsonify({'status': 'ok', 'message': reply, 'model': DEFAULT_MODEL})
        else:
            return jsonify({'error': f'Status {response.status_code}: {response.text}'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat with streaming using current model"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message'}), 400
    
    def generate():
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": DEFAULT_MODEL,  # Using current working model
            "messages": [{"role": "user", "content": user_message}],
            "temperature": 0.7,
            "stream": True
        }
        
        try:
            response = requests.post(GROQ_URL, headers=headers, json=payload, stream=True, timeout=30)
            
            if response.status_code != 200:
                yield f"data: {json.dumps({'error': f'API Error: {response.status_code}'})}\n\n"
                return
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: ') and line != 'data: [DONE]':
                        try:
                            data_json = json.loads(line[6:])
                            if data_json['choices'][0].get('delta', {}).get('content'):
                                token = data_json['choices'][0]['delta']['content']
                                yield f"data: {json.dumps({'token': token})}\n\n"
                        except json.JSONDecodeError:
                            pass
            
            yield f"data: {json.dumps({'done': True})}\n\n"
            
        except requests.exceptions.Timeout:
            yield f"data: {json.dumps({'error': 'Request timeout'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/chat/simple', methods=['POST'])
def chat_simple():
    """Non-streaming fallback"""
    data = request.json
    user_message = data.get('message', '')
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": DEFAULT_MODEL,
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7,
        "stream": False
    }
    
    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            return jsonify({'response': reply})
        else:
            return jsonify({'error': f'API Error: {response.status_code}'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=5000)
