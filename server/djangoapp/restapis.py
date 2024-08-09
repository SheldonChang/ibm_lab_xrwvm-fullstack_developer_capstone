# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv
import json
from django.http import JsonResponse

load_dotenv()

backend_url = os.getenv(
    'backend_url',
    default=(
        "https://ebscream4me-3030.theiadockernext-0-labs-prod"
        "-theiak8s-4-tor01.proxy.cognitiveclass.ai"
    )
)

sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default=(
        "https://sentianalyzer.1kdwlabm2toq.us-"
        "south.codeengine.appdomain.cloud/"
    )
)


def get_request(endpoint, **kwargs):
    params = ""
    if (kwargs):
        for key, value in kwargs.items():
            params = params+key+"="+value+"&"

    request_url = backend_url+endpoint+"?"+params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        print(f"{request_url} : {response.json()}")
        return response.json()
    except Exception as e:
        # If any error occurs
        print(f"Network exception occurred{e}")
        return None


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url+"analyze/"+text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        print(f"{request_url} : {response.json()}")

        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def add_review(request):
    if (request.user.is_anonymous is False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200, "ret": response})
        except Exception as err:
            return JsonResponse({"status": 401,
                                "message": f"Error in posting review {err}"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
