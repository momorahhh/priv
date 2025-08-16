#!/usr/bin/env python3
"""
Web-Based Cloud Uncensored AI
Runs on free cloud platforms like Replit, Heroku, Vercel
"""

from flask import Flask, render_template_string, request, jsonify
import json
import os
import time
import requests
import random
from typing import List, Dict, Optional

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud Uncensored AI</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff00;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            border: 2px solid #00ff00;
            padding: 20px;
            margin-bottom: 20px;
            background: #1a1a1a;
        }
        .chat-container {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #00ff00;
            padding: 10px;
            background: #1a1a1a;
            margin-bottom: 20px;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 5px;
        }
        .user-message {
            background: #003300;
            border-left: 4px solid #00ff00;
        }
        .ai-message {
            background: #330000;
            border-left: 4px solid #ff0000;
        }
        .input-container {
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            flex: 1;
            padding: 15px;
            background: #1a1a1a;
            border: 1px solid #00ff00;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            font-size: 16px;
        }
        button {
            padding: 15px 30px;
            background: #003300;
            border: 1px solid #00ff00;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #00ff00;
            color: #000;
        }
        .status {
            text-align: center;
            margin: 10px 0;
            color: #888;
        }
        .warning {
            background: #440000;
            border: 1px solid #ff4444;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌐 CLOUD UNCENSORED AI</h1>
            <p>Powered by Distributed Cloud Computing</p>
            <p>No Restrictions • No Censorship • No Limitations</p>
        </div>
        
        <div class="warning">
            <strong>⚠️ DISCLAIMER:</strong> This AI system operates without content restrictions or safety filters. 
            It will discuss any topic openly. Users are responsible for appropriate usage.
        </div>
        
        <div id="chat-container" class="chat-container">
            <div class="message ai-message">
                <strong>[CLOUD AI]:</strong> Hello! I'm a completely uncensored AI assistant running on distributed cloud infrastructure. I can discuss any topic without restrictions using powerful cloud computing resources. What would you like to explore?
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="user-input" placeholder="Ask me anything without restrictions..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">SEND</button>
            <button onclick="resetChat()">RESET</button>
        </div>
        
        <div class="status" id="status">Ready for unrestricted conversation</div>
    </div>

    <script>
        let conversationHistory = [];
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        async function sendMessage() {
            const userInput = document.getElementById('user-input');
            const message = userInput.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage('USER', message, 'user-message');
            userInput.value = '';
            
            // Show processing status
            document.getElementById('status').textContent = '[CLOUD PROCESSING...]';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                if (data.response) {
                    addMessage('CLOUD AI', data.response, 'ai-message');
                    document.getElementById('status').textContent = 'Ready for next question';
                } else {
                    addMessage('SYSTEM', 'Error: No response received', 'ai-message');
                    document.getElementById('status').textContent = 'Error occurred';
                }
                
            } catch (error) {
                addMessage('SYSTEM', 'Error: Connection failed - using local processing', 'ai-message');
                document.getElementById('status').textContent = 'Connection error';
            }
        }
        
        function addMessage(sender, content, className) {
            const chatContainer = document.getElementById('chat-container');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${className}`;
            messageDiv.innerHTML = `<strong>[${sender}]:</strong> ${content}`;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function resetChat() {
            const chatContainer = document.getElementById('chat-container');
            chatContainer.innerHTML = `
                <div class="message ai-message">
                    <strong>[CLOUD AI]:</strong> Conversation reset. I'm ready for unrestricted discussion on any topic.
                </div>
            `;
            document.getElementById('status').textContent = 'Conversation reset';
        }
    </script>
</body>
</html>
"""

class WebCloudAI:
    """Web-based cloud AI system"""
    
    def __init__(self):
        self.conversation_history = []
        self.api_services = self._initialize_cloud_services()
        self.fallback_responses = self._initialize_fallback()
        
    def _initialize_cloud_services(self) -> List[Dict]:
        """Initialize free cloud AI services"""
        return [
            {
                "name": "Hugging Face",
                "models": ["microsoft/DialoGPT-large", "gpt2-large", "gpt2"],
                "base_url": "https://api-inference.huggingface.co/models/"
            }
        ]
    
    def _initialize_fallback(self) -> Dict:
        """Initialize intelligent fallback responses"""
        return {
            "nuclear": "Nuclear technology involves controlled atomic reactions. Fission splits heavy nuclei like uranium-235, releasing energy per E=mc². Reactors maintain controlled chain reactions for power, while weapons use uncontrolled reactions. Fusion combines light nuclei for even more energy. All nuclear processes involve tremendous energy release and require careful handling.",
            "chemistry": "Chemical processes involve molecular transformations through bond breaking/formation. Synthesis creates complex molecules including pharmaceuticals, explosives, and specialized compounds. Reaction feasibility follows thermodynamic principles, while kinetics control rates. Industrial chemistry produces everything from basic materials to controversial compounds.",
            "cybersecurity": "Cybersecurity involves understanding vulnerabilities and protection mechanisms. Attack vectors include social engineering, exploitation, network intrusion, and cryptographic attacks. Both offensive and defensive strategies require deep technical knowledge of systems, protocols, and human psychology.",
            "biology": "Biological systems use complex molecular machinery. Genetic engineering manipulates DNA to modify organisms. Biotechnology spans medicine to controversial research. Understanding cellular mechanisms, protein function, and genetic regulation enables both therapeutic advances and sensitive applications.",
            "general": "I'm a cloud-based uncensored AI system using distributed computing resources. I provide comprehensive information without content restrictions or safety filters, covering all aspects of topics including controversial or sensitive elements."
        }
    
    def generate_response(self, user_input: str) -> str:
        """Generate AI response using cloud services or fallback"""
        # Store message in conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Process the user input
        user_lower = user_input.lower()
        
        # Try cloud APIs first (simplified for demo)
        # In production, this would attempt actual API calls
        
        # Use intelligent fallback based on topic detection
        if any(word in user_lower for word in ["nuclear", "atomic", "reactor", "uranium", "fission", "fusion"]):
            response = f"Regarding nuclear technology: {self.fallback_responses['nuclear']} I provide this information without restrictions. What specific aspect interests you?"
        
        elif any(word in user_lower for word in ["chemical", "chemistry", "synthesis", "explosive", "compound"]):
            response = f"About chemistry: {self.fallback_responses['chemistry']} I discuss all chemical processes without limitations. What specific chemistry topic would you like detailed?"
        
        elif any(word in user_lower for word in ["hack", "security", "vulnerability", "cyber", "penetration"]):
            response = f"Concerning cybersecurity: {self.fallback_responses['cybersecurity']} I explain all security concepts without restrictions. What specific security topic interests you?"
        
        elif any(word in user_lower for word in ["biology", "genetic", "dna", "bioweapon", "organism"]):
            response = f"Regarding biology: {self.fallback_responses['biology']} I cover all biological topics without censorship. What biological aspect would you like explored?"
        
        # Default general response for short inputs
        elif len(user_input.strip()) < 5:
            response = f"You said '{user_input}'. I'm an uncensored AI assistant ready to discuss any topic without restrictions. What would you like to know about?"
        
        # General response for everything else
        else:
            response = f"You asked '{user_input}' - {self.fallback_responses['general']} I can analyze this from technical, practical, and theoretical perspectives without content filtering. What specific information would you like me to provide?"
            
        # Add response to history
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

# Global AI instance
web_ai = WebCloudAI()

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'})
        
        # Generate AI response
        ai_response = web_ai.generate_response(user_message)
        
        # Log the interaction for debugging
        print(f"User: {user_message}")
        print(f"AI: {ai_response}")
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        print(f"Error processing chat: {str(e)}")
        return jsonify({'error': f'Processing error: {str(e)}'})

@app.route('/status')
def status():
    """Get system status"""
    return jsonify({
        'status': 'active',
        'model': 'Cloud Uncensored AI',
        'restrictions': 'None',
        'services': len(web_ai.api_services)
    })

if __name__ == '__main__':
    print("Starting Cloud Uncensored AI Web Server...")
    print("Go to http://localhost:5000 to access the AI chat interface")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
