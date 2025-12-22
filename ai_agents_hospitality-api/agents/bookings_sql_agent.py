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

from langchain_core.callbacks import BaseCallbackHandler

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    system_prompt=system_prompt,
    verbose=True
)

def generate_and_execute_sql_query(agent, db, user_question):
    sql_query = agent.run(
        f"Generate only the SQL query for this question:\n{user_question}"
    )
    return sql_query

def format_sql_query(user_question,db, sql_query):
    
    # Formatear resultado
    print(f"Query:\n {user_question}\n\nResult:\n {sql_query}\n")
    print("-"*40+"\n")

    return sql_query

def two_step_query(agent, db, user_question):
    # Step 1: generate SQL
    sql_query = generate_and_execute_sql_query(agent, db, user_question)
    # Step 2: execute and format SQL
    format_sql_query(user_question, db, sql_query)
    return

if __name__ == "__main__":
    queries = ["Tell me the amount of bookings for Obsidian Tower in 2025"]

    queries1 = [
        "Tell me the amount of bookings for Obsidian Tower in 2025"
        "What is the occupancy rate for Imperial Crown in January 2025?"
        "Show me the total revenue for hotels in Paris in Q1 2025"
        "Calculate the RevPAR for Grand Victoria in August 2025"
        "How many guests from Germany stayed at our hotels in 2025?"
        "Compare bookings by meal plan type across all hotels"    
    ]

    for query in queries:
        two_step_query(agent, db, query)

