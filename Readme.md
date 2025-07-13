# Npontu-Bot

Npontu-Bot is a robust, production-ready chatbot backend built with Flask, designed for seamless integration with modern AI models (like Gemini), cloud deployments (e.g., Railway), and a variety of backend services (SQL, MongoDB, RabbitMQ, Redis). It provides secure authentication via Google OAuth, scalable messaging with RabbitMQ, and efficient storage across SQL and NoSQL databases.

---

## Features

- **Flask REST API**: Easily extensible endpoints for chat, model testing, and authentication.
- **Multiple Database Support**: Uses SQLAlchemy with SQLite for relational data and MongoDB for token storage.
- **AI Model Integration**: Ready-to-use endpoints for Google Gemini and generative AI APIs.
- **Google OAuth2 Authentication**: Secure user authentication and token management.
- **RabbitMQ & Redis Integration**: Asynchronous message queueing and caching for performance/scalability.
- **Production Dockerfile**: Containerized for easy deployment on platforms like Railway or Heroku.
- **Environment-Driven Configuration**: All secrets and configs are loaded from `.env`.
- **CORS Enabled**: Allows secure frontend-backend communication.

---

## Getting Started

### Prerequisites

- Python 3.9+
- Docker (optional, for containerized deployment)
- MongoDB, RabbitMQ, Redis (can be local or hosted)
- Google Cloud Project with OAuth2 credentials

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/AduAkorful/Npontu-Bot.git
   cd Npontu-Bot
   ```

2. **Set up environment variables:**
   - Copy `.env.example` to `.env` (create one if not present).
   - Fill in required values (see `.env` for needed keys: DB URIs, API keys, secrets, etc.).

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the Flask app locally:**
   ```sh
   python back.py
   ```
   The app will be available at `http://localhost:5000`.

5. **(Optional) Run with Docker:**
   ```sh
   docker build -t npontu-bot .
   docker run -p 5000:5000 --env-file .env npontu-bot
   ```

---

## Key Environment Variables

| Name                  | Description                                  |
|-----------------------|----------------------------------------------|
| `SECRET_KEY`          | Flask secret key                             |
| `SQLALCHEMY_DATABASE_URI` | SQLAlchemy connection string (SQLite default) |
| `MONGO_URI`           | MongoDB connection URI                       |
| `MONGO_DB_NAME`       | MongoDB database name                        |
| `RABBITMQ_HOST`       | RabbitMQ server hostname                     |
| `RABBITMQ_QUEUE`      | RabbitMQ queue name                          |
| `REDIS_URL`           | Redis connection URI                         |
| `GEMINI_API_KEY`      | Gemini API key                               |
| `GEMINI_API_URL`      | Gemini API endpoint URL                      |
| `CLIENT_ID`           | Google OAuth Client ID                       |
| `CLIENT_SECRET`       | Google OAuth Client Secret                   |
| `CLIENT_SECRET_JSON`  | Google OAuth Client Secret (as JSON string)  |
| `REFRESH_TOKEN`       | Google OAuth Refresh Token                   |

---

## API Endpoints

- `/test-model` (POST): Test generative AI model with a query.
- `/api/v1/chat` (POST): Send a chat message, receive a response.
- `/` (GET): Home/auth check, redirects to Google OAuth if not authenticated.
- `/oauth/callback` (GET): Handles OAuth2 callback and token storage.

---

## Deployment

This project is ready for Railway (see `railway.toml`) and supports Gunicorn for production:

```sh
gunicorn -w 4 -b 0.0.0.0:5000 back:app
```

For Docker, use the provided `dockerfile` and `start.sh`.

---

## Development & Contribution

- Fork and clone the repo
- Install dependencies
- Work on a branch, make PRs
- Follow best practices: secrets in `.env`, no secrets in code

---

## License

This project is licensed under the MIT License.

---

## Credits

Developed and maintained by [Adu Akorful](https://github.com/AduAkorful).

---

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Google Generative AI](https://ai.google.dev/)
- [Railway](https://railway.app/)
- [MongoDB](https://www.mongodb.com/)
- [RabbitMQ](https://www.rabbitmq.com/)
- [Redis](https://redis.io/)
