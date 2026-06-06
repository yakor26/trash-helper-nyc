from dotenv import load_dotenv
# from app.apis.nyc_311
import os
import requests

load_dotenv()

def create_reminder_message():
    """ Create message notifying user of collection status the night before
    pickup"""

def send_text():
    resp = requests.post('https://textbelt.com/text', {
        'phone': '5162620798',
        'message': 'This is a reminder',
        'key': os.getenv("TEXTBELT_API_KEY"),
    })
    print(resp.json())
