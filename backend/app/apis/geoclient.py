from dotenv import load_dotenv
from app.schemas.address import ScheduleRequest, GeoclientAPIResponse
import requests
import os
import json

load_dotenv()


def send_failed_response(error_code, error_message=None) -> GeoclientAPIResponse:
    errors = {
        400: "Request failed due to invalid input. Please review address and resubmit",
        401: "Please provide a valid API key for geoclient API",
        429: "Too many requests to Geoclient API, try again",
        500: "Error submitting request to Geoclient API",
        503: "GeoclientAPI connection error",
        504: "GeoclientAPI request timed out"

    }
    return GeoclientAPIResponse(
            status="failed",
            error_code=error_code or 500,
            error_message=error_message or errors.get(error_code) or "Error occurred while submitting request to Geoclient"
        )


def convert_schedule(initials: str) -> list:
    """ Convert schedule initials to full days of week M - Sat"""
    if not initials:
        return []

    initials_copy = list(initials.lower())
    converted_schedule = []
    day_conversion = {
        "m": "monday",
        "t": "tuesday",
        "w": "wednesday",
        "th": "thursday",
        "f": "friday",
        "s": "saturday"
    }
    if "t" and "h" in initials_copy:
        converted_schedule.append(day_conversion["th"])
        initials_copy.remove("t")
        initials_copy.remove("h")

    for i, char in enumerate(initials_copy):
        if char == "e":
            continue
        converted_schedule.append(day_conversion[char])
    return converted_schedule
        

def get_sanitation_info(input_addr: str) -> GeoclientAPIResponse:
    url = f"https://api.nyc.gov/geoclient/v2/search?input={input_addr}&returnPossiblesWithExact=true"
    headers = {
    'Cache-Control': 'no-cache',
    'Ocp-Apim-Subscription-Key': os.getenv('OPEN_API_GEOCLIENT_KEY'),
    }
    try:
        response = requests.get(url=url, headers=headers, timeout=15)
    except requests.exceptions.Timeout:
        return send_failed_response(504, "Geoclient API request timed out")
        
    except requests.exceptions.ConnectionError:
        return send_failed_response(503, "Geoclient API connection error")

    if response.status_code !=200:
        return send_failed_response(response.status_code,"Error Occurred when submitting to Geoclient API")
    
    if response.json().get("status") == "REJECTED":
        return send_failed_response(400, "Invalid address input sent to Geoclient API, review and resubmit")
    # debug print statement
    # print(json.dumps(response.json(), indent=4))
    # print(json.dumps(response.json().get("results"), indent=4))

    results = response.json().get("results")[0].get("response")
    trash_pickup = convert_schedule(results.get("sanitationRegularCollectionSchedule"))
    compost_pickup = convert_schedule(results.get("sanitationOrganicsCollectionSchedule"))
    recycling_pickup = convert_schedule(results.get("sanitationRecyclingCollectionSchedule"))
    large_item_pickup = convert_schedule(results.get("sanitationBulkPickupSchedule"))
    street_address = f"{
        results.get("houseNumber")} {results.get("streetName1In")}"
    city = results.get("uspsPreferredCityName")
    zipcode = results.get("zipCode")

    return GeoclientAPIResponse(
        status="success",
        data={
            "address": {
                "street_address": street_address,
                "city": city,
                "zipcode": zipcode

            },
            "sanitation": {
                "trash_pickup": trash_pickup,
                "compost_pickup": compost_pickup,
                "recycling_pickup": recycling_pickup,
                "large_item_pickup": large_item_pickup
            }
        }
    )


def test_user_address() -> GeoclientAPIResponse:
    """ Test input calls made to api"""
    full_user_address = GeoclientAPIResponse(full_address=input("Enter Full Address: "))
    return get_sanitation_info(full_user_address)


def main():
    test_user_address()

if __name__ == "__main__":
    main()