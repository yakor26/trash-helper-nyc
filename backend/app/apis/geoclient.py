from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()
def get_sanitation_info(input_addr):
    url = f"https://api.nyc.gov/geoclient/v2/search?input={input_addr}"
    headers = {
    'Cache-Control': 'no-cache',
    'Ocp-Apim-Subscription-Key': os.getenv('OPEN_API_GEOCLIENT_KEY'),
    }
    response = requests.get(url=url, headers=headers)
    # print(json.dumps(response.json(), indent=4))
    # print(response.json().get("results")[0]).get("response")
    results = response.json().get("results")[0].get("response")

    print(f"Large Item Pickup: {results.get("sanitationBulkPickupSchedule")}")
    print(f"Compost Pickup: {results.get("sanitationOrganicsCollectionSchedule")}")
    print(f"Recylying Pickup: {results.get("sanitationRecyclingCollectionSchedule")}")
    print(f"Regular Trash Pickup: {results.get("sanitationRegularCollectionSchedule")}")
    # print(json.dumps(response.json().get("results"), indent=4))

    
    interested = {"sanitationBulkPickupSchedule": "ET",
        "sanitationOrganicsCollectionSchedule": "EF",
        "sanitationRecyclingCollectionSchedule": "EF",
        "sanitationRegularCollectionSchedule": "TF"}

def get_user_address():
    """ Test input calls made to api
    """
    user_address_1 = input("Enter Address Line 1: ")
    user_address_2 = input("Enter Address Line 2 ")
    user_state_code = input("Enter State: ")
    user_city = input("Enter City: ")
    user_zipcode = input("Enter Zipcode: ")
    full_user_address = f"{user_address_1}, {user_address_2}, {user_state_code}, {user_city}, {user_zipcode}"
    return get_sanitation_info(full_user_address)

def main():
    get_user_address()

if __name__ == "__main__":
    main()