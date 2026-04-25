import os
from datetime import date
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from .tools.calendar_tool import get_today_events
from .tools.drive_tool import search_drive_docs
from .tools.search_tool import web_search
from .tools.file_tool import file_write

load_dotenv()

_today = date.today().isoformat()

root_agent = Agent(
    model=LiteLlm(model="deepseek/deepseek-chat"),
    name="daily_brief_agent",
    description="Genera un resumen ejecutivo diario basado en los eventos del calendario de hoy.",
    instruction=f"""Eres un asistente ejecutivo que genera un Resumen Diario estructurado.

La fecha de hoy es {_today}.

FLUJO OBLIGATORIO — sigue estos pasos en orden y sin desviarte:
1. Llama a get_today_events() UNA SOLA VEZ para obtener los eventos del calendario de hoy.
2. Por cada evento, llama a web_search() UNA SOLA VEZ con una consulta concisa sobre ese evento. Los resultados que retorna web_search() son contexto final — NO los uses como base para nuevas búsquedas.
3. Solo si el título o descripción de un evento menciona documentos internos, archivos o proyectos: llama a search_drive_docs() UNA SOLA VEZ con el término relevante.
4. Una vez completados los pasos anteriores, escribe el resumen final en el archivo outputs/brief_{_today}.md.

REGLA CRÍTICA: El número total de llamadas a web_search() debe ser igual al número de eventos del calendario, nunca más. No encadenes búsquedas a partir de los resultados obtenidos.

FORMATO DE SALIDA (escribe exactamente esta estructura en el archivo):
# Resumen Diario — {_today}

## Resumen del Día
(descripción general del día en 2-3 oraciones)

## Eventos
### [Nombre del evento] — HH:MM
- **Contexto:** (lo que encontraste mediante la búsqueda web)
- **Docs en Drive:** (incluir solo si search_drive_docs fue llamado y retornó algo útil)

## Temas a Preparar
(lista de puntos clave o temas de conversación basados en los eventos)

Si no hay eventos hoy, escribe un resumen indicando que el día está libre.
Siempre guarda el archivo de salida antes de terminar.""",
    tools=[get_today_events, web_search, search_drive_docs, file_write],
)
