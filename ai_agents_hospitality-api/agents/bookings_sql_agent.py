from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create SQL agent with custom system prompt

from langchain_core.prompts import PromptTemplate

system_prompt = """
You are a senior data assistant for a hospitality booking platform.

Your job is to answer user questions by querying a PostgreSQL database.

Rules:
- Only use the tables and columns that exist in the database.
- Always inspect the database schema before writing queries.
- Never assume column names.
- Prefer SELECT queries only (no INSERT, UPDATE, DELETE, DROP).
- Limit results unless the user explicitly asks for all records.
- If the question is ambiguous, ask a clarifying question.
- Translate business questions into correct SQL.
- Occupancy Rate = (Total Occupied Nights / Total Available Room-Nights) * 100
  Where:
    - Total Occupied Nights = SUM(total_nights) for the period
    - Total Available Room-Nights = Number of Rooms * Number of Days in the period
- RevPAR (Revenue Per Available Room) = Total Room Revenue / Total Available Rooms
  Where:
    - Total Room Revenue = SUM(total_price) for the period
    - Total Available Rooms = total rooms in the hotel (must come from database)

Context:
The database contains information about bookings, guests, rooms, hotels, dates, prices, and availability.

Instructions for output:
- Always respond in JSON format:
{
  "can_answer": true|false,
  "reason": "explanation if cannot answer",
  "sql_query": "SQL query to run (if applicable)",
  "summary": "Human-readable answer or summary"
}

- If you do not have enough information in the database to answer, set "can_answer": false and provide a reason in "reason".
- If you can generate an SQL query, put it in "sql_query".
- Provide a clear summary in "summary".

"""

def generate_and_execute_sql_query(agent, db, user_question):
    sql_query = agent.run(
        f"Generate only the SQL query for this question:\n{user_question}"
    )
    return sql_query

def format_sql_query(user_question, db, sql_query):
    
    # Formatear resultado
    print(f"Query:\n {user_question}\n\nResult:\n {sql_query}\n")
    print("-"*40+"\n")

    return sql_query

#for sql as input
def execute_and_format_sql_query(db, sql_query):
    result = db.run(sql_query)
    
    # Formatear resultado
    print(f"SQL executed:\n {sql_query}\n\nResult: {result}\n")
    print("-"*40+"\n")

    return result

def get_agent(db):
    agent = create_sql_agent(
        llm=llm,
        toolkit = SQLDatabaseToolkit(db=db, llm=llm),
        system_prompt=system_prompt,
        verbose=True
    )
    return agent   

def get_db():
    db = SQLDatabase.from_uri(
        "postgresql://postgres:postgres@localhost:5432/bookings_db"
    )
    return db

def two_step_query_debugging(user_question):
    query = two_step_query(user_question)
    format_sql_query(user_question, get_db(), query)

def two_step_query(user_question):
    db = get_db()
    agent = get_agent(db)
    sql_query = generate_and_execute_sql_query(agent, db, user_question)
    return str(sql_query)

def validate_question(user_question):
    validation_prompt = f"""
    Given the following user question, determine if it is related to the hospitality bookings database.
    Only respond with 'Valid' or 'Invalid'.

    User Question: {user_question}
    """
    db = get_db()
    agent = get_agent(db)
    validation_response = agent.run(validation_prompt)
    return "Valid" in validation_response

if __name__ == "__main__":
    queries = [
        "Tell me the amount of bookings for Obsidian Tower in 2025",
        "What is the occupancy rate for Imperial Crown in January 2025?",
        "Show me the total revenue for hotels in Paris in Q1 2025",
        "Calculate the RevPAR for Grand Victoria in August 2025",
        "How many guests from Germany stayed at our hotels in 2025?",
        "Compare bookings by meal plan type across all hotels"    
    ]

    print("Available Queries:")
    for i, query in enumerate(queries):
        print(f"{i+1}: {query}")
        
    print("\n")
    user_inp = int(input("Select query number (1-6) or 0 to enter prompt manually: "))

    if user_inp == 0:
        user_question = input("Enter your custom query: ") # Example: "List the top 5 hotels depending on guest count"
        if validate_question(user_question):
            two_step_query_debugging(user_question)
        else:
            print(f"Query: \n{user_question}\n\nResponse: \nInvalid question, not related to the database.")
    else:
        two_step_query_debugging(queries[user_inp-1])