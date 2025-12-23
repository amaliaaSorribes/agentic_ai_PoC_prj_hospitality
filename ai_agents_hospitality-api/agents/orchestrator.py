from openai import OpenAI
from bookings_sql_agent import two_step_query, validate_question
from hotel_details_agent import hotel_details_agent

client = OpenAI()

def detect_llm_agent(query):
    prompt = f"""
    You are a router that classifies user queries into ONE of the following labels:

    SQL
    RAG
    UNKNOWN

    Definitions:

    SQL:
    Use SQL if the question requires structured data from a database, such as:
    - bookings
    - reservations
    - prices
    - availability
    - dates
    - counts, sums, filters, or aggregations

    RAG:
    Use RAG if the question requires factual or descriptive information stored in documents, such as:
    - hotel names
    - addresses
    - locations
    - amenities
    - descriptions
    - policies
    - general information about a hotel or property

    UNKNOWN:
    Use UNKNOWN ONLY if the question is NOT related to hospitality, hotels, or accommodations.

    Rules:
    - If the question asks for an address, location, or description of a hotel, choose RAG.
    - If the question asks for numbers, availability, or booking data, choose SQL.
    - Respond with ONLY one word: SQL, RAG, or UNKNOWN.
    Query: "{query}"
    
    Response:
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user", "content": prompt}],
        max_tokens=10
    )
    return response.choices[0].message.content.strip().lower()


def detectar_agente_llm(pregunta):
    prompt = f"""
    Solo clasifica la siguiente pregunta en 'SQL' si requiere consultar una base de datos, 
    'RAG' si requiere información de documentos o 'UNKNOWN' si no está relacionada con ninguno de los anteriores.:
    
    Pregunta: "{pregunta}"
    
    Respuesta:
    """
    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user", "content": prompt}],
        max_tokens=10
    )
    return respuesta.choices[0].message.content.strip().lower()

def sys_print(message):
    print("\n"+"-"*40+"\n")
    print(message)
    print("-"*40+"\n")

def format_query(user_question, query):
    
    # Formatear resultado
    print(f"Query:\n {user_question}\n\nResult:\n {query}\n")
    print("-"*40+"\n")

    return query

def run_orchestrator():
    sys_print("Welcome to the Hospitality AI Agent System!")
    query = input("Enter your hospitality-related question: ")
    print("\n"+"-"*40+"\n")

    recomended_agent = detect_llm_agent(query)
    if "sql" in recomended_agent:
        if validate_question(query):
            sys_print("Using SQL Agent to process the query...\n")
            two_step_query(query)
        else:
            sys_print("The question is not valid for the hospitality bookings database.\n")
    elif "rag" in recomended_agent:
        sys_print("Using RAG Agent to process the query...\n")
        response = hotel_details_agent(query)
        format_query(query, response)
    else:
        format_query(query, "The question is not related to hospitality.\n")

def test_orchestrator_agent_selection():
    #lets test the efficiency of the orchestrator decision of the agent selection with multiple queries
    
    rag_queries = [
        "What is the full address of Obsidian Tower?",
        "What are the meal charges for Half Board in hotels in Paris?",
        "List all hotels in France with their cities",
        "What is the discount for extra bed in Grand Victoria?",
        "Compare room prices between peak and off season for hotels in Nice"
    ]

    sql_queries = [
        "Tell me the amount of bookings for Obsidian Tower in 2025",
        "What is the occupancy rate for Imperial Crown in January 2025?",
        "Show me the total revenue for hotels in Paris in Q1 2025",
        "Calculate the RevPAR for Grand Victoria in August 2025",
        "How many guests from Germany stayed at our hotels in 2025?",
        "Compare bookings by meal plan type across all hotels"    
    ]

    unrelated_queries = [
        "What is the capital of France?",
        "Who won the World Cup in 2018?",
        "What is the tallest mountain in the world?",
        "How many continents are there on Earth?",
        "What is the boiling point of water?"
    ]

    total_correct = 0
    total_tests = 0

    for query in rag_queries:
        total_tests += 1
        agent = detect_llm_agent(query)
        if "rag" in agent:
            total_correct += 1
        else:
            print(f"Misclassified RAG query: {query} as {agent.upper()}")
    for query in sql_queries:
        total_tests += 1
        agent = detect_llm_agent(query)
        if "sql" in agent:
            total_correct += 1
        else:
            print(f"Misclassified SQL query: {query} as {agent.upper()}") 
    for query in unrelated_queries:
        total_tests += 1
        agent = detect_llm_agent(query)
        if "unknown" in agent:
            total_correct += 1
        else:
            print(f"Misclassified Unrelated query: {query} as {agent.upper()}")

    sys_print(f"Orchestrator Agent Selection Accuracy: {total_correct}/{total_tests} = {total_correct/total_tests*100:.2f}% correct.")

if __name__ == "__main__":  
    # Uncomment the line below to run the orchestrator function
    run_orchestrator()
    
    # Uncomment the line below to run the test for accuracy in classification function
    #test_orchestrator_agent_selection()