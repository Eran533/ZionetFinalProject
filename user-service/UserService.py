from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from time import sleep

app = Flask(__name__)

def connect_to_mysql_with_retry(max_retries=15, retry_delay=5):
    retries = 0
    while retries < max_retries:
        try:
            print(f"Trying to connect to MySQL (Attempt {retries + 1}/{max_retries})...")
            db = mysql.connector.connect(
                host='mysql',
                port=3306,
                user='root',
                password='Root',
                database='News_Update_Aggregator'
            )
            print("Connected to MySQL!")
            return db
        except Error as err:
            print(f"Failed to connect to MySQL: {err}")
            retries += 1
            sleep(retry_delay)
    raise Exception(f"Failed to connect to MySQL after {max_retries} retries.")

def initialize_db():
    global db, cursor
    db = connect_to_mysql_with_retry()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            user_id INT PRIMARY KEY,
            topics TEXT
        )
    """)
    db.commit()

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    username = request.json.get('username')
    if email and username:
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (email, username) VALUES (%s, %s)", (email, username))
            db.commit()
            cursor.close()
            return jsonify({'message': 'User registered successfully'}), 201
        except Error as e:
            print(f"Error registering user: {e}")
            db.rollback()
            cursor.close()
            return jsonify({'error': 'Failed to register user'}), 500
    return jsonify({'error': 'Invalid data'}), 400

# Endpoint to set topics for a user
@app.route('/topics', methods=['POST'])
def set_topics():
    username = request.json.get('username')
    topics = request.json.get('topics')
    if username and topics:
        cursor = db.cursor()
        try:
            # Fetch user_id based on username
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_id = cursor.fetchone()

            if user_id:
                # Use the fetched user_id to replace topics
                cursor.execute("REPLACE INTO topics (user_id, topics) VALUES (%s, %s)", (user_id[0], ','.join(topics)))
                db.commit()
                cursor.close()
                return jsonify({'message': 'Topics updated successfully'}), 200
            else:
                return jsonify({'error': 'User not found'}), 404

        except Error as e:
            print(f"Error setting topics: {e}")
            db.rollback()
            cursor.close()
            return jsonify({'error': 'Failed to set topics'}), 500
    return jsonify({'error': 'Invalid data'}), 400

@app.route('/topics/<string:username>', methods=['GET'])
def get_topics(username):
    cursor = db.cursor()
    cursor.execute("SELECT topics FROM topics WHERE user_id = (SELECT id FROM users WHERE username = %s)", (username,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return jsonify({'topics': result[0].split(',') if result[0] else []}), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['GET'])
def get_users():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    cursor.close()
    if results:
        return jsonify(results), 200
    return jsonify({'error': 'No users found'}), 404

if __name__ == '__main__':
    initialize_db()
    app.run(host='0.0.0.0', port=5001, debug=True)
