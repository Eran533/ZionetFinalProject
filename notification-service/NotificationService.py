from flask import Flask, request, jsonify
import smtplib

app = Flask(__name__)


@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')

    if send_email(user_id, message):
        return jsonify({'message': 'Notification sent'}), 200
    return jsonify({'error': 'Failed to send notification'}), 500


def send_email(user_id, message):
    print(f"Sending email to {user_id} with message: {message}")
    return True


if __name__ == '__main__':
    app.run(port=5003)
