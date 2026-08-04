from dotenv import load_dotenv
from app.schemas.notification import TextNotificationRequest, TextNotificationResponse
from datetime import datetime, timezone
import os
import requests

load_dotenv()


def send_failed_response(error_code, error_message=None) -> TextNotificationResponse:
    """ Return failed response with error code and message """
    errors = {
        400: "Request failed due to Invalid submission to Textbelt API",
        401: "Invalid API key for Textbelt API",
        429: "Too many requests to Textbelt API",
        500: "Error submitting request to Textbelt API",
        503: "Textbelt API connection error",
        504: "Textbelt API request timed out"

    }
    return TextNotificationResponse(
            is_sent=False,
            error_code=error_code or 500,
            sent_at=datetime.now(tz=timezone.utc),
            error_message=error_message or errors.get(error_code) or "Error occurred while submitting request to 311 Calendar API"
        )


def send_text(text_notification: TextNotificationRequest) -> TextNotificationResponse:
    """ Send SMS notification via Textbelt API"""
    try:
        response = requests.post('https://textbelt.com/text', {
            'phone': text_notification.user_phone_number,
            'message': text_notification.message,
            'key': os.getenv("TEXTBELT_API_KEY"),
        }, timeout=15)
        text_response = response.json()
    except requests.exceptions.Timeout:
        return send_failed_response(error_code=504)
    except requests.exceptions.ConnectionError:
        return send_failed_response(error_code=503)
    except requests.exceptions.RequestException as e:
        return send_failed_response(
            error_code=500,
            error_message=f"Error occurred when sending request to Textbelt API: {str(e)}")
    if not text_response.get("success"):
        return send_failed_response(
            error_code=500,
            error_message=text_response.get("error") or None)
    return TextNotificationResponse(
        is_sent=True,
        sent_at=datetime.now(tz=timezone.utc)
    )


if __name__ == "__main__":
    send_text()
