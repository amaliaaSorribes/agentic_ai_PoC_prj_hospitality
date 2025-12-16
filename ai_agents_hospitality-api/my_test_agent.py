import json
from pathlib import Path

# Load hotel data from JSON
hotels_file = Path("bookings-db/output_files/hotels/hotels.json")
with open(hotels_file, 'r', encoding='utf-8') as f:
    hotels_data = json.load(f)

# Load hotel details markdown
hotel_details_file = Path("bookings-db/output_files/hotels/hotel_details.md")
with open(hotel_details_file, 'r', encoding='utf-8') as f:
    hotel_details_text = f.read()

import os
from langchain_openai import ChatOpenAI #use openai instead of gemini
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=os.getenv("AI_AGENTIC_API_KEY"))

# Create a prompt template that includes the hotel context
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful hotel assistant. Use the following hotel information to answer questions.

Hotel Data:
{hotel_context}

When answering questions:
- Be accurate and specific
- Reference hotel names, locations, and details from the data
- If information is not available, say so clearly
- Format responses in a clear, readable way"""),
    ("human", "{question}")
])

# Create the chain
chain = prompt_template | llm

def answer_hotel_question(question: str) -> str:
    """Simple agent that answers questions using hotel files as context."""
    # Prepare a compact context to avoid exceeding model context limits
    MAX_CONTEXT_CHARS = 4000

    # Normalize hotel list (file may use "Hotels" with capital H)
    if isinstance(hotels_data, dict):
        hotels_list = hotels_data.get("hotels") or hotels_data.get("Hotels") or []
    elif isinstance(hotels_data, list):
        hotels_list = hotels_data
    else:
        hotels_list = []

    summary_lines = [f"Total hotels: {len(hotels_list)}"]
    for h in hotels_list[:3]:
        # Best-effort field names used by generator
        name = h.get("Name") or h.get("name") or h.get("hotel_name") or "(unknown)"
        address = h.get("Address") or {}
        city = address.get("City") or address.get("city") or "(unknown)"

        # Meal plans: prefer MealPlanWeights keys, fallback to MealPlanPrices keys
        meal_plan_weights = h.get("SyntheticParams", {}).get("MealPlanWeights", {})
        meal_plan_prices = h.get("SyntheticParams", {}).get("MealPlanPrices", {})
        meal_plans = list(meal_plan_weights.keys()) if meal_plan_weights else list(meal_plan_prices.keys())
        meal_plans = [mp.replace('_', ' ').title() for mp in meal_plans] if meal_plans else ["(n/a)"]

        # Room types (unique)
        room_types = sorted({r.get("Type") for r in h.get("Rooms", []) if r.get("Type")})

        summary_lines.append(
            f"- {name} — {city} — Meal plans: {', '.join(meal_plans)} — Room types: {', '.join(room_types[:5])}"
        )
    hotels_summary = "\n".join(summary_lines)

    hotel_details_for_context = hotel_details_text
    combined_preview = f"{hotel_details_for_context}\n\nHotels Summary:\n{hotels_summary}"
    if len(combined_preview) > MAX_CONTEXT_CHARS:
        allowed = MAX_CONTEXT_CHARS - len("\n\nHotels Summary:\n") - len(hotels_summary) - 200
        hotel_details_for_context = hotel_details_for_context[:max(200, allowed)] + "\n\n... (hotel details truncated for length) ...\n"

    hotel_context = f"""
{hotel_details_for_context}

Hotels Summary:
{hotels_summary}
"""

    # Invoke the chain
    try:
        response = chain.invoke({
            "hotel_context": hotel_context,
            "question": question
        })
        return response.content
    except Exception as e:
        # Surface helpful error for context length or API problems
        return f"Error invoking LLM: {e}"

# Test queries
queries = [
    "List all hotels and their cities",
    "What is the address of the first hotel?",
    "What meal plans are available?",
    "Tell me about room types in these hotels",
    "What discounts are available?"
]

for query in queries:
    answer = answer_hotel_question(query)
    print(f"Q: {query}")
    print(f"A: {answer}\n")

# In main.py or a new agent module
async def handle_hotel_query_simple(user_query: str) -> str:
    """Handle hotel queries using simple file context approach."""
    try:
        response = answer_hotel_question(user_query)
        return response
    except Exception as e:
        return f"Error processing query: {str(e)}"