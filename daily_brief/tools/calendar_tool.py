import os
import requests
from datetime import date, datetime
import icalendar
import recurring_ical_events
from dotenv import load_dotenv

load_dotenv()


def get_today_events() -> dict:
    """
    Reads today's events from Google Calendar using the secret iCal URL.
    No OAuth or GCP required — only the GOOGLE_CALENDAR_ICS_URL env variable.
    Returns a list of events with summary, start, end, description and location.
    Handles recurring events and all datetime formats Google Calendar generates.
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

    try:
        cal = icalendar.Calendar.from_ical(response.content)
        today = date.today()
        occurrences = recurring_ical_events.of(cal).at(today)
    except Exception as e:
        return {"status": "error", "message": f"Failed to parse calendar: {e}"}

    events = []
    for component in occurrences:
        dtstart = component.get("DTSTART").dt
        dtend = component.get("DTEND")

        start_str = dtstart.strftime("%H:%M") if isinstance(dtstart, datetime) else "00:00"

        if dtend:
            dtend = dtend.dt
            end_str = dtend.strftime("%H:%M") if isinstance(dtend, datetime) else ""
        else:
            end_str = ""

        events.append({
            "summary": str(component.get("SUMMARY", "Sin título")),
            "start": start_str,
            "end": end_str,
            "description": str(component.get("DESCRIPTION", "")),
            "location": str(component.get("LOCATION", "")),
        })

    events.sort(key=lambda e: e["start"])

    return {
        "status": "success",
        "date": today.isoformat(),
        "event_count": len(events),
        "events": events,
    }
