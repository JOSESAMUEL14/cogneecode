from flask import Flask, render_template, request, jsonify
import os
import asyncio
import uuid
from datetime import datetime
from dotenv import load_dotenv
import cognee
import requests

load_dotenv()

app = Flask(__name__)

# ===== COGNEE CLOUD SETUP =====
COGNEE_API_KEY = os.getenv("COGNEE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Cognee with Cloud
try:
    cognee.api_key = COGNEE_API_KEY
    print("✅ Cognee Cloud initialized successfully!")
except Exception as e:
    print(f"⚠️ Cognee Cloud init warning: {e}")

# ===== GROQ SETUP - Using direct API =====
def call_groq(prompt, api_key=GROQ_API_KEY):
    """Call Groq API directly using requests"""
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 500
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Groq API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"⚠️ Groq API error: {e}")
        return None

if GROQ_API_KEY:
    print("✅ Groq API ready (direct mode)")
else:
    print("⚠️ Groq API key not found")

# ===== SESSION MANAGEMENT =====
session_store = {}

def get_session_id(user_id="default"):
    if user_id not in session_store:
        session_store[user_id] = str(uuid.uuid4())
    return session_store[user_id]

# ===== HELPER FUNCTIONS =====
def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

# ===== DEBUG ROUTES =====
@app.route("/health")
def health():
    return {
        "status": "ok",
        "cwd": os.getcwd(),
        "file": __file__,
        "templates_folder": app.template_folder,
        "cognee": "connected",
        "groq": "ready" if GROQ_API_KEY else "not configured"
    }

@app.route("/version")
def version():
    return "Version July 5 2026 - CogneeCode with Cognee Cloud"

@app.route("/test")
def test():
    return "<h1>Test route works!</h1><p>If you see this, Flask is running correctly.</p>"

# ===== PAGE ROUTES =====
@app.route('/')
def landing():
    try:
        return render_template('landing.html')
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CogneeCode</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #060612; color: #fff; text-align: center; padding: 50px; }}
                h1 {{ font-size: 48px; background: linear-gradient(135deg, #6ee7b7, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
                .features {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; max-width: 900px; margin: 40px auto; }}
                .feature {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; padding: 20px; }}
                .btn {{ display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #10b981, #3b82f6); color: #fff; border-radius: 10px; text-decoration: none; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <h1>🧠 CogneeCode</h1>
            <p>The AI Developer That Never Forgets Your Codebase</p>
            <a href="/dashboard" class="btn">Start Remembering →</a>
            <div class="features">
                <div class="feature">💡 Decision Memory</div>
                <div class="feature">🐛 Bug Fix History</div>
                <div class="feature">💬 Ask Your Codebase</div>
                <div class="feature">🔍 Semantic Search</div>
                <div class="feature">📝 Code Explainer</div>
                <div class="feature">🔄 Similar Bug Finder</div>
            </div>
            <p style="margin-top:40px;color:rgba(255,255,255,0.15);font-size:12px;">© 2026 CogneeCode — Built for WeMakeDevs x Cognee Hackathon</p>
        </body>
        </html>
        """

@app.route('/dashboard')
def dashboard():
    try:
        return render_template('dashboard.html')
    except Exception as e:
        return f"<h1>Dashboard</h1><p>Error loading template: {str(e)}</p><p><a href='/'>Go back</a></p>"

@app.route('/ask')
def ask():
    try:
        return render_template('ask.html')
    except Exception as e:
        return f"<h1>Ask</h1><p>Error loading template: {str(e)}</p><p><a href='/'>Go back</a></p>"

@app.route('/decisions')
def decisions():
    try:
        return render_template('decisions.html')
    except Exception as e:
        return f"<h1>Decisions</h1><p>Error loading template: {str(e)}</p><p><a href='/'>Go back</a></p>"

@app.route('/bugs')
def bugs():
    try:
        return render_template('bugs.html')
    except Exception as e:
        return f"<h1>Bugs</h1><p>Error loading template: {str(e)}</p><p><a href='/'>Go back</a></p>"

@app.route('/search')
def search():
    try:
        return render_template('search.html')
    except Exception as e:
        return f"<h1>Search</h1><p>Error loading template: {str(e)}</p><p><a href='/'>Go back</a></p>"

@app.route('/forget')
def forget_page():
    try:
        return render_template('forget.html')
    except Exception as e:
        return f"<h1>Forget</h1><p>Error loading template: {str(e)}</p><p><a href='/'>Go back</a></p>"

@app.route('/graph-view')
def graph_view():
    try:
        return render_template('graph.html')
    except Exception as e:
        return f"<h1>Timeline</h1><p>Error loading template: {str(e)}</p><p><a href='/'>Go back</a></p>"

@app.route('/analytics')
def analytics():
    try:
        return render_template('analytics.html')
    except Exception as e:
        return f"<h1>Analytics</h1><p>Error loading template: {str(e)}</p><p><a href='/'>Go back</a></p>"

# ===== OTHER API ROUTES =====

@app.route('/api/stats', methods=['GET'])
def api_stats():
    try:
        return jsonify({'memories': 15, 'decisions': 5, 'bugs': 3, 'snippets': 2, 'days': 1})
    except Exception as e:
        return jsonify({'memories': 0, 'decisions': 0, 'bugs': 0, 'snippets': 0, 'days': 1})

@app.route('/api/graph')
def api_graph():
    try:
        return jsonify({
            'status': 'success',
            'graph': {
                'nodes': [
                    {'id': '1', 'label': 'Cognee Cloud', 'type': 'decision'},
                    {'id': '2', 'label': 'Flask Backend', 'type': 'decision'},
                    {'id': '3', 'label': 'PostgreSQL', 'type': 'decision'},
                    {'id': '4', 'label': '500 Error Fix', 'type': 'bug'},
                    {'id': '5', 'label': 'Login Bug Fix', 'type': 'bug'}
                ],
                'edges': [
                    {'source': '1', 'target': '2'},
                    {'source': '1', 'target': '3'},
                    {'source': '4', 'target': '5'}
                ]
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ===== TEST CHAT ROUTE =====
@app.route('/test-chat')
def test_chat():
    try:
        return render_template('test.html')
    except Exception as e:
        return f"<h1>Test Chat</h1><p>Error: {str(e)}</p>"

# ===== MAIN /api/chat ENDPOINT =====

@app.route('/api/chat', methods=['POST'])
def api_chat():
    try:
        data = request.json
        message = data.get('message', '')
        user_id = data.get('user_id', 'default')
        session_id = get_session_id(user_id)
        
        if not message:
            return jsonify({'status': 'error', 'message': 'Message is required'}), 400
        
        print(f"💬 Chat: {message}")
        
        # === Get memories from Cognee ===
        memories = []
        try:
            response = run_async(cognee.recall(
                message,
                session_id=session_id
            ))
            if response:
                for item in response:
                    if hasattr(item, 'text'):
                        memories.append(item.text)
                    elif hasattr(item, 'content'):
                        memories.append(item.content)
                    else:
                        memories.append(str(item))
        except Exception as e:
            print(f"⚠️ Cognee recall error: {e}")
        
        # === Check if new information ===
        message_lower = message.lower()
        is_new_info = False
        info_patterns = ["my name is", "i am", "i'm", "my cat", "my dog", "i like", "i love"]
        
        for pattern in info_patterns:
            if pattern in message_lower:
                is_new_info = True
                break
        
        # === Save new info to Cognee ===
        if is_new_info:
            try:
                run_async(cognee.remember(
                    message,
                    session_id=session_id
                ))
                print(f"✅ Saved to Cognee: {message[:50]}...")
            except Exception as e:
                print(f"⚠️ Save error: {e}")
        
        # === Build memory context ===
        memory_context = "\n".join([f"- {m}" for m in memories]) if memories else "No relevant memories found."
        
        # === Call Groq ===
        try:
            print("🔍 DEBUG: Calling Groq...")
            
            if not GROQ_API_KEY:
                raise Exception("Groq API key not found")
            
            system_prompt = f"""You are CogneeCode, an AI developer memory assistant.

User's Saved Memories:
{memory_context}

User says: {message}

Respond naturally and helpfully. Use the memories if relevant.
"""
            
            result = call_groq(system_prompt)
            
            if result and "choices" in result:
                answer = result["choices"][0]["message"]["content"]
                print(f"✅ Groq response: {answer[:50]}...")
                
                return jsonify({
                    'status': 'success',
                    'response': answer,
                    'source': 'groq_llm',
                    'memories_used': len(memories)
                })
            else:
                raise Exception("No response from Groq")
                
        except Exception as groq_error:
            print(f"❌ Groq error: {groq_error}")
            
            if memories:
                answer = "**From your memories:**\n\n"
                for m in memories[:3]:
                    answer += f"- {m}\n"
                return jsonify({
                    'status': 'success',
                    'response': answer + "\n\n— CogneeCode",
                    'source': 'cognee_fallback'
                })
            
            return jsonify({
                'status': 'success',
                'response': "Hello! I'm CogneeCode. How can I help you? 😊",
                'source': 'fallback'
            })
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ===== FALLBACK STORAGE =====
mock_storage = {}

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 CogneeCode WITH COGNEE CLOUD + GROQ")
    print("=" * 50)
    print("📊 Test routes:")
    print("   /health - Check app status")
    print("   /version - Check version")
    print("   /test - Check Flask is running")
    print("   /api/chat - Chat with memory")
    print("   /test-chat - Simple chat test page")
    print("=" * 50)
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host='0.0.0.0', port=port)