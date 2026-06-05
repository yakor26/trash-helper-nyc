from dotenv import load_dotenv
from app.schemas.collection import CollectionStatusRequest, CollectionStatusResponse
import requests
import os
import json

load_dotenv()


def send_failed_response(error_code, error_message=None) -> CollectionStatusResponse:
    """ Return failed response with error code and message """
    errors = {
        400: "Request failed due to invalid input. Please review and resubmit",
        401: "Please provide a valid API key for 311 Calendar API",
        429: "Too many requests to 311 Calendar API, try again",
        500: "Error submitting request to 311 Calendar API",
        503: "311 Calendar API connection error",
        504: "311 Calendar API request timed out"

    }
    return CollectionStatusResponse(
            status="failed",
            error_code=error_code or 500,
            error_message=error_message or errors.get(error_code) or "Error occurred while submitting request to 311 Calendar API"
        )


def get_collection_status(date_request: CollectionStatusRequest) -> CollectionStatusResponse:
    """ Get NYC sanitation collection status for specific date"""
    url = f"https://api.nyc.gov/public/api/GetCalendar?fromdate={date_request.from_date}&todate={date_request.to_date}"
    headers = {
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': os.getenv('OPEN_API_311_KEY'),
    }
    try:
        response = requests.get(url=url, headers=headers, timeout=15)
    except requests.exceptions.Timeout:
        return send_failed_response(504, "311 Calendar request timed out")
    except requests.exceptions.ConnectionError:
        return send_failed_response(503, "311 Calendar API connection error")
    except requests.exceptions.RequestException as e:
        return send_failed_response(500, f"Error occurred when submitting request to 311 API: {str(e)}")
    if response.status_code != 200:
        return send_failed_response(error_code=response.status_code)
    # print(json.dumps(response.json(), indent=4))
    response_data = response.json().get("days")
    sanitation_data = [day.get("items")[1] for day in response_data]
    # print(response_data)
    return CollectionStatusResponse(status="success", data=sanitation_data)
