import requests
import json
import threading

EMAIL_SERVICE_URL = "http://localhost:3000/dev/send-email"

def send_email_async(email_type, recipient, data):
    """
    Sends an email asynchronously via the Serverless service.
    """
    def _send():
        try:
            payload = {
                "type": email_type,
                "recipient": recipient,
                "data": data
            }
            response = requests.post(EMAIL_SERVICE_URL, json=payload)
            print(f"Email Service Response: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    thread = threading.Thread(target=_send)
    thread.start()
