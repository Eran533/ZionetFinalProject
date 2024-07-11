from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

app = Flask(__name__)


def send_email(receiver_email, subject, body):
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender_email = "eranblank533@gmail.com"
    password = "suwqhjndavhpvhln"

    if isinstance(body, list):
        body = "\n".join(str(item) for item in body)

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


@app.route('/notify/<string:email>', methods=['POST'])
def notify(email):
    data = request.get_json()
    try:
        send_email(email, "Notification", data)
        return jsonify({"success": True, "message": "Notification sent successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to send notification: {str(e)}"})

if __name__ == '__main__':
    app.run(port=5003)
