# Personalized News Update Aggregator

## Purpose
The Personalized News Update Aggregator is a microservice-based application designed to aggregate news and technology updates based on user preferences. The system fetches news, picks interesting articles using AI based on user preferences, optionally generates summaries using AI, and sends updates via email, Telegram, or other channels.

## Services
The project consists of the following services:
1. **User Service**: Manages user registration and preferences.
2. **News Fetcher Service**: Fetches news based on user topics.
3. **News Aggregator Service**: Aggregates news for users.
4. **Notification Service**: Sends notifications to users.

## Prerequisites
- Docker
- Docker Compose
- Python 3.9+
- MySQL
- RabbitMQ
