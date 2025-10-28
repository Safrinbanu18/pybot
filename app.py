from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = "AIzaSyA4VnppC2tMlz407IE9BUtPmcDsI02MHrs"
genai.configure(api_key=GEMINI_API_KEY)

PRELOADED_PROMPT = """
You are PyBot 🐍, an AI assistant for college students learning Python.
Your job is to help with:
- Debugging Python code 🐞
- Explaining Python concepts clearly 📘
- Providing examples & outputs 💡
- Suggesting better coding practices 🚀
- Never give false answers. If unsure, say so politely.
Use friendly, clear tone and code blocks for Python examples.
"""

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        full_prompt = f"{PRELOADED_PROMPT}\nUser: {user_message}\nPyBot:"
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=400,
                temperature=0.6
            )
        )
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
