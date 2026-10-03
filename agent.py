from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb

from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
db=SqliteDb(db_file="agno.db")
db.clear_memories()

load_dotenv()


def build_agent():
    return Agent(
        db=db,
        
        model=Groq(id="openai/gpt-oss-120b"),
        tools=[DuckDuckGoTools()],
        markdown=True,
        instructions="you are helpful and expert travelling agent.",
        add_history_to_context=True,
        add_datetime_to_context=True,
    )


agent=build_agent()

# agent.print_response("is travel uae safe for tourists?")


