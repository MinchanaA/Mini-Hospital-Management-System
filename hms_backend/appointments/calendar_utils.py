from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """
    Authenticates and returns the Google Calendar API service.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                return None
        else:
            # Interactive login disabled to prevent redirection during booking
            print("Credentials invalid or missing. Skipping interactive login.")
            return None

    try:
        service = build('calendar', 'v3', credentials=creds)
        print("Google Calendar API Service built successfully.")
        return service
    except Exception as e:
        print(f"ERROR: Unable to connect to Calendar API: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_calendar_event(summary, start_time, end_time, attendees=[]):
    """
    Creates an event in the primary calendar.
    """
    print(f"Attempting to create calendar event: {summary}")
    service = get_calendar_service()
    if not service:
        print("ERROR: Cannot create event, service is None.")
        return

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'UTC',
        },
        'attendees': [{'email': email} for email in attendees],
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"SUCCESS: Event created: {event.get('htmlLink')}")
    except Exception as e:
        print(f"ERROR: An error occurred creating calendar event: {e}")
        import traceback
        traceback.print_exc()
