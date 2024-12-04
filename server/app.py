from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def hello():
    return {'message': 'Hello from Flask!'}

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )

        # Extract the response text
        bot_response = response.choices[0].message.content

        return jsonify({
            'response': bot_response,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'response': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)