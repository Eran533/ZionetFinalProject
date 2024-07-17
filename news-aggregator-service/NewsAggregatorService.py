from flask import Flask, jsonify, request
import requests
import threading

app = Flask(__name__)

def fetch_news_and_notify(email, user_topics):
    try:
        dapr_fetch_news_url = f"http://localhost:3500/v1.0/invoke/news-fetcher-service/method/fetch-news"
        response = requests.post(dapr_fetch_news_url, json=user_topics)
        if response.status_code == 200:
            news = response.json()
            dapr_notification_url = f"http://localhost:3500/v1.0/invoke/notification-service/method/notify/{email}"
            response = requests.post(dapr_notification_url, json=news)
            return response.json(), response.status_code
        else:
            return {'error': 'Failed to fetch news'}, 500
    except requests.exceptions.RequestException as e:
        return {'error': f'Error connecting to the service: {str(e)}'}, 500

@app.route('/aggregate-news/<string:email>', methods=['POST'])
def aggregate_news(email):
    try:
        dapr_user_service_url = f"http://localhost:3500/v1.0/invoke/user-service/method/topics/{email}"
        response = requests.get(dapr_user_service_url)
        if response.status_code == 200:
            user_topics = response.json()
            # Start a new thread for fetching news and notifying
            thread = threading.Thread(target=fetch_news_and_notify, args=(email, user_topics))
            thread.start()
            return jsonify({'message': 'News aggregation started in the background'}), 202  # HTTP 202 Accepted
        else:
            return jsonify({'error': 'Failed to fetch user topics'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error connecting to the service: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
