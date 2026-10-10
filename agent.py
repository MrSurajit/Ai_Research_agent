
from agno.agent import Agent
from agno.models.groq import Groq
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv

load_dotenv()

db = SqliteDb(db_file="agno.db")


def build_agent():
    return Agent(
        db=db,
        model=Groq(id="openai/gpt-oss-120b"),
        tools=[DuckDuckGoTools()],
        markdown=True,
        instructions="You are a helpful and expert travel agent.",
        add_history_to_context=True,
        add_datetime_to_context=True,
    )


agent = build_agent()
