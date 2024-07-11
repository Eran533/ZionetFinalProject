from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

def news_api(topic):
    url = "https://real-time-news-data.p.rapidapi.com/search"
    querystring = {
        "query": f'{topic}',
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
    return response.json()

@app.route('/fetch-news', methods=['POST'])
def fetch_news():
    request_data = request.get_json()
    topics = request_data['topics']
    news_lst = []
    for topic in topics:
        news = news_api(topic)
        news_lst.append(news)
    return jsonify(news_lst)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
