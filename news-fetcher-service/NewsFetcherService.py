from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

def summarize_articles(articles):
    summary = []
    for article in articles:
        summary.append({
            "title": article["title"],
            "body": article["body"]
        })
    return summary

def news_api(topic):
    url = "https://newsnow.p.rapidapi.com/"
    payload = {
        "text": f'{topic}',
        "region": "wt-wt",
        "max_results": 5
    }
    headers = {
        "x-rapidapi-key": "d73f442011msh63871ecf2dde8bap143fadjsne460c0fb111c",
        "x-rapidapi-host": "newsnow.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

@app.route('/fetch-news', methods=['POST'])
def fetch_news():
    request_data = request.get_json()
    topics = request_data['topics']
    news_lst = []
    for topic in topics:
        news_response = news_api(topic)
        articles = news_response.get('news', [])
        s_news = summarize_articles(articles)
        news_lst.append({topic: s_news})
    return jsonify(news_lst)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
