from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    task = data.get('task', '').strip()
    if not task:
        return jsonify({'error': 'Task is required'}), 400
    prompt = f"Design a multi-agent AI system for: {task}. Return ONLY valid JSON with: taskTitle, taskDescription, agents(name,role,icon,inputs,outputs,decisionLogic), routingRules(from,to,condition), validationGate(question,onSuccess,onFailure), feedbackLoops(title,steps), failureHandling(scenario,action), optimizations(name,detail), scalabilityFeatures(name,detail). 4-7 agents."
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.choices[0].message.content
        parsed = json.loads(raw[raw.index('{'):raw.rindex('}')+1])
        return jsonify(parsed)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("✅ Server: http://localhost:8888")
    app.run(debug=False, port=8888, host='127.0.0.1')
