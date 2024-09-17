import requests
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve URLs from environment variables
backend_url = os.getenv(
    'backend_url',
    default="http://localhost:3030"
)
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    """Send a GET request to the specified endpoint with optional query
    parameters."""
    if kwargs:
        params = "&".join(
            f"{key}={value}" for key, value in kwargs.items()
        )
        request_url = f"{backend_url}{endpoint}?{params}"
    else:
        request_url = f"{backend_url}{endpoint}"

    logger.info(f"GET request to {request_url}")
    try:
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Network error occurred: {req_err}")
    return None


def analyze_review_sentiments(text):
    """Analyze the sentiment of a review using the sentiment analyzer
    service."""
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    try:
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Network error occurred: {req_err}")
    return None


def post_review(data_dict):
    """Post a review to the backend service."""
    request_url = f"{backend_url}/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Network error occurred: {req_err}")
    return None
