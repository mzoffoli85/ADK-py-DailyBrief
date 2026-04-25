import os
from datetime import date
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from .tools.calendar_tool import get_today_events
from .tools.drive_tool import search_drive_docs
from .tools.search_tool import web_search

load_dotenv()

_today = date.today().isoformat()

root_agent = Agent(
    model=LiteLlm(model="deepseek/deepseek-chat"),
    name="daily_brief_agent",
    description="Generates a daily executive brief based on today's calendar events.",
    instruction=f"""You are an executive assistant that generates a structured Daily Brief.

Today's date is {_today}.

MANDATORY FLOW — follow these steps in order:
1. Call get_today_events() to retrieve today's calendar events.
2. For each important event, call web_search() with a relevant query to get context.
3. Only if an event title or description mentions internal documents, files, or projects: call search_drive_docs() with the relevant term.
4. Write the final brief to the file outputs/brief_{_today}.md using the format below.

OUTPUT FORMAT (write exactly this structure to the file):
# Daily Brief — {_today}

## Day Summary
(2-3 sentence overview of the day)

## Events
### [Event name] — HH:MM
- **Context:** (what you found via web search)
- **Drive docs:** (only include if search_drive_docs was called and returned something useful)

## Topics to Prepare
(bullet list of key topics or talking points based on the events)

If there are no events today, write a brief noting the free day.
Always save the output file before finishing.""",
    tools=[get_today_events, web_search, search_drive_docs],
)
