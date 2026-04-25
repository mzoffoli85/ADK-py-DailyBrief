import os
import requests
from datetime import date, datetime, timezone
from ics import Calendar
from dotenv import load_dotenv

load_dotenv()


def get_today_events() -> dict:
    """
    Reads today's events from Google Calendar using the secret iCal URL.
    No OAuth or GCP required — only the GOOGLE_CALENDAR_ICS_URL env variable.
    Returns a list of events with summary, start, end, description and location.
    """
    ics_url = os.getenv("GOOGLE_CALENDAR_ICS_URL")
    if not ics_url:
        return {
            "status": "error",
            "message": "GOOGLE_CALENDAR_ICS_URL not set in .env file.",
        }

    try:
        response = requests.get(ics_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"status": "error", "message": f"Failed to fetch calendar: {e}"}

    calendar = Calendar(response.text)
    today = date.today()

    events = []
    for event in calendar.events:
        event_date = event.begin.date()
        if event_date == today:
            events.append(
                {
                    "summary": str(event.name or "Sin título"),
                    "start": event.begin.strftime("%H:%M"),
                    "end": event.end.strftime("%H:%M") if event.end else "",
                    "description": str(event.description or ""),
                    "location": str(event.location or ""),
                }
            )

    events.sort(key=lambda e: e["start"])

    return {
        "status": "success",
        "date": today.isoformat(),
        "event_count": len(events),
        "events": events,
    }
