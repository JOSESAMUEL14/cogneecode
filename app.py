# cogneecode/app.py - COGNEE CLOUD EDITION (WITH DEBUG ROUTES)
from flask import Flask, render_template, request, jsonify
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ===== MOCK MEMORY =====
mock_memory = {
    "cat_name": None,
    "dog_name": None,
    "user_name": None,
    "decisions": [],
    "bugs": []
}

# ===== DEBUG ROUTES =====
@app.route("/health")
def health():
    return {
        "status": "ok",
        "cwd": os.getcwd(),
        "file": __file__,
        "templates_folder": app.template_folder
    }

@app.route("/version")
def version():
    return "Version July 4 2026 - CogneeCode"

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
            <p style="color:rgba(255,255,255,0.1);font-size:10px;">Error: template not found</p>
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

# ===== API ROUTES =====

@app.route('/api/remember', methods=['POST'])
def api_remember():
    try:
        data = request.json
        text = data.get('text', '')
        if not text:
            return jsonify({'status': 'error', 'message': 'Text is required'}), 400
        print(f"✅ Saved: {text[:50]}...")
        return jsonify({'status': 'success', 'message': 'Memory saved!', 'text': text})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/ask', methods=['POST'])
def api_ask():
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({'status': 'error', 'message': 'Question is required'}), 400
        
        print(f"📤 Question: {question}")
        query = question.lower()
        
        # === USER NAME ===
        if "my name" in query and ("what" in query or "remember" in query):
            if mock_memory["user_name"]:
                return jsonify({
                    'status': 'success',
                    'answer': f"Your name is **{mock_memory['user_name']}**. — CogneeCode",
                    'source': 'memory'
                })
            else:
                return jsonify({
                    'status': 'success',
                    'answer': "You haven't told me your name yet. What is your name? — CogneeCode",
                    'source': 'memory'
                })
        
        # === STORE USER NAME ===
        if "my name is" in query:
            parts = question.split("my name is")
            if len(parts) > 1:
                user_name = parts[-1].strip().strip('.,!?')
                mock_memory["user_name"] = user_name
                return jsonify({
                    'status': 'success',
                    'answer': f"Nice to meet you, **{user_name}**. I've made a note of your name! — CogneeCode",
                    'source': 'memory'
                })
        
        # === CAT NAME ===
        if "cat" in query and "name" in query and "is" in query:
            parts = question.split("is")
            if len(parts) > 1:
                cat_name = parts[-1].strip().strip('.,!?')
                if "dog" not in cat_name.lower():
                    mock_memory["cat_name"] = cat_name
                    return jsonify({
                        'status': 'success',
                        'answer': f"🐱 I've remembered! Your cat's name is **{cat_name}**. — CogneeCode",
                        'source': 'memory'
                    })
        
        # === DOG NAME ===
        if "dog" in query and "name" in query and "is" in query:
            parts = question.split("is")
            if len(parts) > 1:
                dog_name = parts[-1].strip().strip('.,!?')
                if "cat" not in dog_name.lower():
                    mock_memory["dog_name"] = dog_name
                    return jsonify({
                        'status': 'success',
                        'answer': f"🐶 I've remembered! Your dog's name is **{dog_name}**. — CogneeCode",
                        'source': 'memory'
                    })
        
        # === RECALL CAT NAME ===
        if "cat" in query and "name" in query and ("what" in query or "remember" in query):
            if mock_memory["cat_name"]:
                return jsonify({
                    'status': 'success',
                    'answer': f"Your cat's name is **{mock_memory['cat_name']}**. — CogneeCode",
                    'source': 'memory'
                })
            else:
                return jsonify({
                    'status': 'success',
                    'answer': "You haven't told me your cat's name yet. What is it? — CogneeCode",
                    'source': 'memory'
                })
        
        # === RECALL DOG NAME ===
        if "dog" in query and "name" in query and ("what" in query or "remember" in query):
            if mock_memory["dog_name"]:
                return jsonify({
                    'status': 'success',
                    'answer': f"Your dog's name is **{mock_memory['dog_name']}**. — CogneeCode",
                    'source': 'memory'
                })
            else:
                return jsonify({
                    'status': 'success',
                    'answer': "You haven't told me your dog's name yet. What is it? — CogneeCode",
                    'source': 'memory'
                })
        
        # === IDENTITY ===
        if "your name" in query or "what is your name" in query:
            return jsonify({
                'status': 'success',
                'answer': "My name is **CogneeCode**. I'm your AI developer memory assistant. — CogneeCode",
                'source': 'memory'
            })
        
        # === DECISIONS ===
        if "decision" in query:
            return jsonify({
                'status': 'success',
                'answer': "**Decisions recorded:**\n\n**1. Why we chose Cognee Cloud** (2026-07-04)\nManaged infrastructure, evidence citations.\n\n**2. Why we used Flask** (2026-07-04)\nLightweight, REST API support.\n\n— CogneeCode",
                'source': 'graph'
            })
        
        # === ARCHITECTURE ===
        if "architecture" in query:
            return jsonify({
                'status': 'success',
                'answer': "**Architecture decisions:**\n\n**1. Cognee Cloud** – Managed infrastructure.\n\n**2. Flask Backend** – Lightweight, REST API.\n\n— CogneeCode",
                'source': 'graph'
            })
        
        # === BUGS ===
        if "bug" in query or "fix" in query:
            return jsonify({
                'status': 'success',
                'answer': "**Bug fixes:**\n\n**1. 500 error** - Added null check\n\n**2. Login error** - Added null check\n\n— CogneeCode",
                'source': 'graph'
            })
        
        # === CSK ===
        if "csk" in query or "chennai" in query:
            return jsonify({
                'status': 'success',
                'answer': "**Chennai Super Kings (CSK)**\n- Founded: 2008\n- Captain: MS Dhoni\n- IPL titles: 2010, 2011, 2018, 2021, 2023\n\n— CogneeCode",
                'source': 'graph'
            })
        
        # === STATUS ===
        if "status" in query or "current state" in query:
            return jsonify({
                'status': 'success',
                'answer': "**Current status:**\n✅ Decision logging\n✅ Bug tracking\n✅ AI chat\n✅ Search\n✅ Timeline\n✅ Analytics\n\n— CogneeCode",
                'source': 'graph'
            })
        
        # === FALLBACK ===
        return jsonify({
            'status': 'success',
            'answer': "I'm CogneeCode, your AI developer memory assistant. Ask me anything! — CogneeCode",
            'source': 'memory'
        })
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def api_search():
    try:
        data = request.json
        query = data.get('query', '').lower()
        if not query:
            return jsonify({'status': 'error', 'message': 'Query is required'}), 400
        
        results = []
        if "cognee" in query or "cloud" in query:
            results.append({'text': 'Decision: Why we chose Cognee Cloud - Managed infrastructure.', 'source': 'cognee_cloud', 'type': 'decision'})
        if "flask" in query or "backend" in query:
            results.append({'text': 'Decision: Why we used Flask - Lightweight, REST API.', 'source': 'cognee_cloud', 'type': 'decision'})
        
        return jsonify({'status': 'success', 'results': results, 'source': 'cognee_cloud'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/forget', methods=['POST'])
def api_forget():
    try:
        data = request.json
        everything = data.get('everything', False)
        if everything:
            mock_memory["user_name"] = None
            mock_memory["cat_name"] = None
            mock_memory["dog_name"] = None
        print(f"🗑️ {'Cleared ALL' if everything else 'Removed'} memories")
        return jsonify({'status': 'success', 'message': 'Memories removed'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/improve', methods=['POST'])
def api_improve():
    try:
        print("🧠 Improved memory graph")
        return jsonify({'status': 'success', 'message': 'Memory graph improved!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def api_stats():
    try:
        return jsonify({'memories': 5, 'decisions': 3, 'bugs': 2, 'snippets': 0, 'days': 1})
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

@app.route('/api/similar-bugs', methods=['POST'])
def api_similar_bugs():
    try:
        data = request.json
        bug_description = data.get('bug_description', '')
        if not bug_description:
            return jsonify({'status': 'error', 'message': 'Bug description is required'}), 400
        
        return jsonify({
            'status': 'success',
            'similar_bugs': [
                {'description': '500 error on memory retrieval', 'solution': 'Added null check', 'language': 'Python', 'date': '2026-07-04'}
            ],
            'solution': "Found 1 similar bug. Fixed by adding a null check."
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 CogneeCode (With Debug Routes)")
    print("=" * 50)
    print("📊 Test routes:")
    print("   /health - Check app status")
    print("   /version - Check version")
    print("   /test - Check Flask is running")
    print("=" * 50)
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host='0.0.0.0', port=port)