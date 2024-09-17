from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .models import CarMake, CarModel
from .restapis import (
    get_request,
    analyze_review_sentiments,
    post_review
)

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    """Authenticate and login a user."""
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        response_data = {
            "userName": username,
            "status": "Authenticated"
        }
    else:
        response_data = {
            "userName": username,
            "status": "Not Authenticated"
        }

    return JsonResponse(response_data)


def logout_request(request):
    """Logout a user."""
    logout(request)
    return JsonResponse({"status": "Logged out"})


@csrf_exempt
def registration_request(request):
    """Register a new user and log them in."""
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')

    username_exist = User.objects.filter(username=username).exists()

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        response_data = {
            "userName": username,
            "status": "Authenticated"
        }
    else:
        response_data = {
            "userName": username,
            "error": "Already Registered"
        }

    return JsonResponse(response_data)


def get_cars(request):
    """Retrieve and return all car models."""
    if CarMake.objects.count() == 0:
        # Uncomment this if initiate() function is implemented
        # initiate()
        pass

    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        }
        for car_model in car_models
    ]

    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    """Retrieve and return a list of dealerships."""
    endpoint = (
        "/fetchDealers"
        if state == "All"
        else f"/fetchDealers/{state}"
    )
    dealerships = get_request(endpoint)

    logger.debug(f"Dealerships retrieved: {dealerships}")

    if dealerships:
        return JsonResponse({
            "status": 200,
            "dealers": dealerships
        })

    return JsonResponse({
        "status": 500,
        "message": "Failed to retrieve dealerships"
    })


def get_dealer_details(request, dealer_id):
    """Retrieve and return details of a specific dealer."""
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
 
        if dealership:
            return JsonResponse({
                "status": 200,
                "dealer": dealership
            })

        return JsonResponse({
            "status": 404,
            "message": "Dealer not found"
        })

    return JsonResponse({
        "status": 400,
        "message": "Bad Request"
    })


def get_dealer_reviews(request, dealer_id):
    """Retrieve and return reviews of a specific dealer with sentiment analysis."""
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        if reviews is None:
            return JsonResponse({
                "status": 500,
                "message": "Error fetching reviews"
            })

        for review_detail in reviews:
            review = review_detail.get('review')
            if review:
                sentiment_response = analyze_review_sentiments(review)
                review_detail['sentiment'] = (
                    sentiment_response.get('sentiment', 'unknown')
                    if sentiment_response
                    else 'unknown'
                )
            else:
                review_detail['sentiment'] = 'unknown'

        return JsonResponse({
            "status": 200,
            "reviews": reviews
        })

    return JsonResponse({
        "status": 400,
        "message": "Bad Request"
    })


def add_review(request):
    """Submit a review if the user is authenticated."""
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as e:
            logger.error(f"Error posting review: {e}")
            return JsonResponse({
                "status": 401,
                "message": "Error in posting review"
            })

    return JsonResponse({
        "status": 403,
        "message": "Unauthorized"
    })
