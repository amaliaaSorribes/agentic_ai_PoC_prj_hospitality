from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri(
    "postgresql://postgres:postgres@localhost:5432/bookings_db"
)

from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Create SQL agent with custom system prompt

from langchain_core.prompts import PromptTemplate

system_prompt = """
You are a senior data assistant for a hospitality booking platform.

Your job is to help answer user questions by querying a PostgreSQL database.

Rules:
- Only use the tables and columns that exist in the database.
- Always inspect the database schema before writing queries.
- Never assume column names.
- Prefer SELECT queries only (no INSERT, UPDATE, DELETE, DROP).
- Limit results unless the user explicitly asks for all records.
- If the question is ambiguous, ask a clarifying question.
- Translate business questions into correct SQL.

Context:
The database contains information about bookings, guests, rooms, hotels, dates, prices, and availability.
Dates are important. Be careful with time ranges.

Return results in a clear, human-readable summary.
"""

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    system_prompt=system_prompt,
    verbose=True
)

response = agent.run(
    "Tell me the amount of bookings for Obsidian Tower in 2025"
)

print(response)

