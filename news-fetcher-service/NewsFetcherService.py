from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/fetch-news', methods=['POST'])
def fetch_news():
    url = "https://real-time-news-data.p.rapidapi.com/search"
    querystring = {
        "query": "Elon Musk",
        "limit": "500",
        "time_published": "anytime",
        "country": "US",
        "lang": "en"
    }
    headers = {
        "x-rapidapi-key": "d73f442011msh63871ecf2dde8bap143fadjsne460c0fb111c",
        "x-rapidapi-host": "real-time-news-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return jsonify(response.json())  # Return JSON response from the API
    else:
        return jsonify({"error": "Failed to fetch news", "status_code": response.status_code})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
