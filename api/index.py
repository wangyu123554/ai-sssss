import os
from flask import Flask, request, jsonify, send_from_directory

# 这里的 static_folder='../' 是关键，它告诉 Flask 去上一级目录找 HTML 文件
app = Flask(__name__, static_folder='../')

@app.route('/')
def index():
    # 返回根目录下的 index.html
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    
    # 你的 Dify Token
    DIFY_API_KEY = os.environ.get("DIFY_API_KEY", "app-VoXEBZnh2j4rFVjMqNCcvr38")
    DIFY_URL = "https://api.dify.ai/v1/chat-messages"

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": {},
        "query": data.get("query"),
        "response_mode": "blocking",
        "user": data.get("user", "default_user"),
        "conversation_id": data.get("conversation_id", "")
    }

    try:
        import requests
        response = requests.post(DIFY_URL, json=payload, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)