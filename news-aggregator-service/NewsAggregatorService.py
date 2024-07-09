from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/aggregate-news/<string:username>', methods=['POST'])
def aggregate_news(username):
    try:
        # Fetch user topics using Dapr service invocation
        dapr_user_service_url = f"http://user-service:3500/v1.0/invoke/user-service/method/topics/{username}"
        response = requests.get(dapr_user_service_url)
        if response.status_code == 200:
            user_topics = response.json()['topics']

            # Fetch news based on user topics using Dapr service invocation
            dapr_fetch_news_url = f"http://news-fetcher-service:3500/v1.0/invoke/news-fetcher-service/method/fetch-news"
            response = requests.post(dapr_fetch_news_url, json=user_topics)
            if response.status_code == 200:
                news = response.json()
                return jsonify(news), 200
            else:
                return jsonify({'error': 'Failed to fetch news'}), 500
        else:
            return jsonify({'error': 'Failed to fetch user topics'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error connecting to the service: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
