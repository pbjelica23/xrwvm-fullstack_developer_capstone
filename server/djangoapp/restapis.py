# Uncomment the imports below before you add the function code
import requests
from django.http import JsonResponse
import logging
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    # Build the query parameters from kwargs
    if kwargs:
        params = "&".join(f"{key}={value}" for key, value in kwargs.items())
        request_url = f"{backend_url}{endpoint}?{params}"
    else:
        request_url = f"{backend_url}{endpoint}"

    print(f"GET from {request_url}")
    try:
        # Make the GET request
        response = requests.get(request_url)

        # Check if the response status is 200 (OK)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # Handle any network-related exceptions
        print(f"Network exception occurred: {e}")
        return None
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url+"analyze/"+text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


# def post_review(data_dict):
# Add code for posting review
def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict)
        print(response.json())
        return response.json()
    except:
        print("Network exception occurred")