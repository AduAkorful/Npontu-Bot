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
    OAUTH_REDIRECT_URI = "https://jackal-suitable-manatee.ngrok-free.app"
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
        # Get the query from the request body
        user_query = request.json.get('query')

        # Check if query is provided
        if not user_query:
            return {"error": "Query is required"}, 400

        # Define ACCESS_TOKEN (replace with actual token retrieval logic)
        ACCESS_TOKEN = "your_access_token"

        # Use the access token to call the Gemini API
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        payload = {"query": user_query}

        # Send the request to the Gemini API
        response = requests.post("https://gemini.api.endpoint/your-model-endpoint", headers=headers, json=payload)

        # Return the model's response
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Model API call failed", "details": response.json()}, response.status_code
    except Exception as e:
        return {"error": str(e)}, 500
        return {"error": "Model API call failed", "details": response.json()}, response.status_code
    except Exception as e:
        return {"error": str(e)}, 500
@bp.route('/api/v1/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    user_token = data.get("user_token")

    if not authenticate_with_gemini(user_token):
        return jsonify({"error": "Authentication failed"}), 401

    # Process user message (kept from your existing code)
    response = {"message": f"Processed message: {user_message}"}
    return jsonify(response)

@bp.route('/')
def home():
    flow = get_oauth_flow()
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)

@bp.route('/oauth/callback')
def oauth_callback():
    try:
        # Initialize OAuth flow
        flow = get_oauth_flow()
        flow.fetch_token(authorization_response=request.url)

        # Extract tokens
        credentials = flow.credentials
        return {
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "expires_in": credentials.expiry.isoformat() if credentials.expiry else None,
        }
    except Exception as e:
        # Log the error for debugging
        print(f"Error during token exchange: {str(e)}")
        return {"error": str(e)}, 400
def refresh_access_token(refresh_token):
    """
    Refresh the access token using the refresh token.
    """
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        return response.json()  # New access token and expiry
    else:
        return {"error": response.json()}




# Main App
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    cache.init_app(app)

    # Configuring CORS dynamically (use Railway or production domains if necessary)
    from flask_cors import CORS
    CORS(app, resources={r"/api/*": {"origins": os.getenv("CORS_ORIGIN", "*")}})

    # Register blueprint
    app.register_blueprint(bp)

    # Set global timeout
    set_request_timeout(app, int(os.getenv("REQUEST_TIMEOUT", 15)))

    return app

if __name__ == '__main__':
    app = create_app()
    # Use Railway-provided PORT or fallback to 5000 if not set
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=True, host='0.0.0.0', port=port)

