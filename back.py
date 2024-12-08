import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

import signal
from flask import Flask, Blueprint, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
import pika
import requests
from dotenv import load_dotenv
from flask_caching import Cache
import logging
import json
from google_auth_oauthlib.flow import Flow
from flask_cors import CORS   # Import CORS

# Routes Blueprint
bp = Blueprint('routes', __name__)  # Use __name__ instead of name

# Load environment variables from the .env file
load_dotenv()

# Configuration
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///chatbot.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "default_gemini_key")
    GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://gemini-api.example.com/v1/authenticate")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "chatbot")
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "chat_queue")
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = os.getenv("REDIS_URL", "redis://redis-server:6379/0")

    
    # Use absolute path for client_secret.json
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get directory of the current script
    CLIENT_SECRET_JSON = os.getenv("CLIENT_SECRET_JSON")  # Load JSON content directly
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
    OAUTH_REDIRECT_URI = "https://npontu-bot-production.up.railway.app/oauth/callback"
    OAUTH_SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email']


# Ensure CLIENT_SECRET_FILE exists
if not os.getenv("CLIENT_SECRET_JSON"):
    raise ValueError("CLIENT_SECRET_JSON environment variable is missing.")

# SQLAlchemy for SQL database
db = SQLAlchemy()

# Initialize caching
cache = Cache(config={"CACHE_TYPE": Config.CACHE_TYPE, "CACHE_REDIS_URL": Config.CACHE_REDIS_URL})

# MongoDB client for NoSQL
try:
    mongo_client = MongoClient(Config.MONGO_URI)
    mongo_db = mongo_client[Config.MONGO_DB_NAME]
except Exception as e:
    logging.error(f"MongoDB connection failed: {e}")
    mongo_client, mongo_db = None, None

# RabbitMQ Service with Retry
def connect_rabbitmq():
    attempts = 3
    while attempts > 0:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(Config.RABBITMQ_HOST))
            channel = connection.channel()
            channel.queue_declare(queue=Config.RABBITMQ_QUEUE)
            return channel
        except pika.exceptions.AMQPConnectionError as e:
            logging.warning(f"Failed to connect to RabbitMQ: {e}. Retrying...")
            attempts -= 1
    return None
# Timeout Integration
class TimeoutException(Exception):
    pass
    
def timeout_handler(signum, frame):
    raise TimeoutException("Request timed out")

def set_request_timeout(app, timeout_seconds):
    @app.before_request
    def before_request():
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout_seconds)

    @app.teardown_request
    def teardown_request(exception=None):
        signal.alarm(0)  # Disable the alarm

def publish_message(message):
    channel = connect_rabbitmq()
    if channel:
        channel.basic_publish(exchange='', routing_key=Config.RABBITMQ_QUEUE, body=message)
        logging.info(f" [x] Sent '{message}'")
    else:
        logging.error("RabbitMQ connection failed after retries.")

# Gemini API Integration for Authentication
def authenticate_with_gemini(user_token):
    try:
        headers = {
            "Authorization": f"Bearer {Config.GEMINI_API_KEY}"
        }
        payload = {"user_token": user_token}
        response = requests.post(Config.GEMINI_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("authenticated", False)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error authenticating with Gemini API: {e}")
        return False
def handle_token_exchange(authorization_response):
    """
    Handles the token exchange using the authorization response URL.
    """
    flow = get_oauth_flow()
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    # Return the tokens as a dictionary
    return {
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "expires_in": credentials.expiry.isoformat() if credentials.expiry else None,
        "scopes": credentials.scopes
    }


# Google OAuth Integration
def get_oauth_flow():
    logging.info("Using CLIENT_SECRET_JSON from environment.")
    try:
        # Parse the JSON content from the environment variable
        client_config = json.loads(Config.CLIENT_SECRET_JSON)
    except Exception as e:
        raise ValueError(f"Invalid CLIENT_SECRET_JSON in environment: {e}")

    return Flow.from_client_config(
        client_config,
        scopes=Config.OAUTH_SCOPES,
        redirect_uri=Config.OAUTH_REDIRECT_URI
    )


@bp.route('/test-model', methods=['POST'])
def test_model():
    try:
        user_query = request.json.get('query')
        if not user_query:
            return jsonify({"error": "Query is required"}), 400

        # Get the access token (refresh if necessary)
        access_token, expires_in = refresh_access_token()
        if not access_token:
            return jsonify({"error": "Failed to retrieve access token"}), 500

        # Use the access token in your API call
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {"query": user_query}
        response = requests.post("https://gemini.api.endpoint/your-model-endpoint", headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Model API call failed", "details": response.json()}, response.status_code
    except Exception as e:
        logging.error(f"Error in /test-model: {e}")
        return {"error": str(e)}, 500

        
@bp.route('/api/v1/chat', methods=['POST'])
def chat():
    data = request.get_json()
    logging.info(f"Received message: {data}")

    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    response = {"message": f"Processed message: {user_message}"}
    return jsonify(response)


@bp.route('/')
def home():
    # Check if the user is authenticated (replace with your logic)
    if 'user_token' in request.cookies:
        return jsonify({"message": "User already authenticated."})

    # If not authenticated, redirect to OAuth
    flow = get_oauth_flow()
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)


@bp.route('/oauth/callback')
def oauth_callback():
    try:
        flow = get_oauth_flow()
        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials
        access_token = credentials.token
        refresh_token = credentials.refresh_token

        # Save tokens for the user (use their email or unique ID)
        save_tokens_to_db(user_id="user@example.com", access_token=access_token, refresh_token=refresh_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": credentials.expiry.isoformat() if credentials.expiry else None,
        }
    except Exception as e:
        logging.error(f"Error during token exchange: {e}")
        return {"error": str(e)}, 400


def refresh_access_token():
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": Config.CLIENT_ID,
        "client_secret": Config.CLIENT_SECRET,
        "refresh_token": Config.REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    try:
        response = requests.post(token_url, data=payload)
        response.raise_for_status()
        tokens = response.json()
        access_token = tokens.get("access_token")
        expires_in = tokens.get("expires_in")

        # Optionally, log or store the new access token
        logging.info(f"Refreshed access token: {access_token}")

        return access_token, expires_in
    except requests.RequestException as e:
        logging.error(f"Failed to refresh access token: {e}")
        return None, None




from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for the frontend URL
    CORS(app, resources={r"/*": {"origins": "https://npontu-bot-frontend-production.up.railway.app"}})

    # Register blueprint and other settings
    app.register_blueprint(bp)

    return app



if __name__ == '__main__':
    app = create_app()
    # Use Railway-provided PORT or fallback to 5000 if not set
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=True, host='0.0.0.0', port=port)

