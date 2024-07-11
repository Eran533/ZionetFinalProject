from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

def summarize_articles(articles):
    summary = []
    for article in articles:
        summary.append({
            "title": article["title"],
            "link": article["link"]
        })
    return summary

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

def ai_api(news):
    import requests

    url = "https://chatgpt-42.p.rapidapi.com/conversationgpt4-2"

    payload = {
        "messages": [
            {
                "content": f'summarize the news instead of listing all titles and links mentioned .{news}',
                "role": "user"
            }
        ],
        "system_prompt": "",
        "temperature": 0.9,
        "top_k": 5,
        "top_p": 0.9,
        "max_tokens": 256,
        "web_access": False
    }
    headers = {
        "x-rapidapi-key": "d73f442011msh63871ecf2dde8bap143fadjsne460c0fb111c",
        "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
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
        if 'data' in news_response:
            articles = news_response['data']
            s_news = summarize_articles(articles)
            ai_news = ai_api(s_news)
            news_lst.append(topic)
            news_lst.append(ai_news["result"])
        else:
            news_lst.append({"error": "No data found"})
    return jsonify(news_lst)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
