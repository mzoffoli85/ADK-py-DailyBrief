# adk-python-ia
PoC utilizando ADK Google.

ADK-py-DailyBrief
Agente: "Daily Brief + Research Prep"

¿Qué hace?
INPUT: Ejecutás el agente (un solo comando)

FLUJO:
1. Lee Google Calendar del día
2. Por cada evento importante → busca contexto con Search
3. Si hay docs relevantes en Drive → los consulta
4. Genera un briefing estructurado en MD

OUTPUT: Un archivo brief_YYYY-MM-DD.md listo

Tools que practica
ToolPara quéGoogle CalendarLeer eventos realesGoogle SearchBuscar contexto de cada eventoGoogle 
DriveConsultar docs relacionadosFile SystemEscribir el output en MD

Lo que aprendés de ADK

Tool chaining — la salida de Calendar alimenta a Search
Tool selection lógica — Drive solo se consulta si hay docs relevantes
Output estructurado — no es una respuesta de chat, es un archivo
Agente orientado a tarea, no a conversación
