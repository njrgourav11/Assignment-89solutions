from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL_EVERYTHING = "https://newsapi.org/v2/everything"
BASE_URL_TOP = "https://newsapi.org/v2/top-headlines"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    if not API_KEY:
        return jsonify({"error": "API Key missing"}), 500

    keyword = request.args.get('keyword')
    from_date = request.args.get('from')
    to_date = request.args.get('to')

    params = {
        "apiKey": API_KEY,
        "language": "en",
        "sortBy": "publishedAt"
    }

    if keyword or from_date or to_date:
        url = BASE_URL_EVERYTHING
        # Logic matches our CLI script: default string if missing 'q' for 'everything' endpoint
        params["q"] = keyword if keyword else "general"
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
    else:
        url = BASE_URL_TOP
        params["source"] = "bbc-news" # Default source

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "ok":
            return jsonify({"error": data.get("message")}), 400
            
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
