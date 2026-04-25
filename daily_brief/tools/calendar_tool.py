import os
import requests
from datetime import date, datetime
import icalendar
import recurring_ical_events
from dotenv import load_dotenv

load_dotenv()


def get_today_events() -> dict:
    """
    Lee los eventos de hoy desde Google Calendar usando la URL secreta iCal.
    No requiere OAuth ni GCP — solo la variable GOOGLE_CALENDAR_ICS_URL en el .env.
    Retorna una lista de eventos con título, inicio, fin, descripción y ubicación.
    Maneja eventos recurrentes y todos los formatos de fecha que genera Google Calendar.
    """
    ics_url = os.getenv("GOOGLE_CALENDAR_ICS_URL")
    if not ics_url:
        return {
            "status": "error",
            "message": "La variable GOOGLE_CALENDAR_ICS_URL no está configurada en el archivo .env.",
        }

    try:
        response = requests.get(ics_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"status": "error", "message": f"Error al obtener el calendario: {e}"}

    try:
        cal = icalendar.Calendar.from_ical(response.content)
        today = date.today()
        occurrences = recurring_ical_events.of(cal).at(today)
    except Exception as e:
        return {"status": "error", "message": f"Error al parsear el calendario: {e}"}

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
