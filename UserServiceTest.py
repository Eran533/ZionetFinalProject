import requests
import pytest

BASE_URL = "http://localhost:5001"

def test_register_user():
    payload = {'email': 'user@example.com', 'username': 'testuser'}
    response = requests.post(f"{BASE_URL}/register", json=payload)
    assert response.status_code == 201
    assert response.json() == {'message': 'User registered successfully'}

def test_register_duplicate_user():
    payload = {'email': 'user@example.com', 'username': 'testuser'}
    response = requests.post(f"{BASE_URL}/register", json=payload)
    assert response.status_code == 500
    assert 'error' in response.json()

def test_set_topics():
    payload = {'username': 'testuser', 'topics': ['technology', 'sports']}
    response = requests.post(f"{BASE_URL}/topics", json=payload)
    assert response.status_code == 200
    assert response.json() == {'message': 'Topics updated successfully'}

def test_get_topics():
    email = 'user@example.com'
    response = requests.get(f"{BASE_URL}/topics/{email}")
    assert response.status_code == 200
    assert response.json() == {'topics': ['technology', 'sports']}

def test_get_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    users = response.json()
    assert len(users) > 0
    user_emails = [user[1] for user in users]
    assert 'user@example.com' in user_emails

if __name__ == '__main__':
    pytest.main()
