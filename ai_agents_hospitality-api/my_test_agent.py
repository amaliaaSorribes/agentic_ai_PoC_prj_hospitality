# Usa todo el database de 5 hoteles en vez de 3

import json
from pathlib import Path

# Resolve hotels files relative to the repository root (two levels above this file)
repo_root = Path(__file__).resolve().parents[1]
hotels_json_path = repo_root / "bookings-db" / "output_files" / "hotels" / "hotels.json"
hotel_details_path = repo_root / "bookings-db" / "output_files" / "hotels" / "hotel_details.md"

if not hotels_json_path.exists() or not hotel_details_path.exists():
    raise FileNotFoundError(
        f"Hotel data files not found. Expected:\n  - {hotels_json_path}\n  - {hotel_details_path}\n\nPlease generate them with:\n  cd bookings-db\n  py src/gen_synthetic_hotels.py --num_hotels 3"
    )

# Load hotel data from JSON
with open(hotels_json_path, 'r', encoding='utf-8') as f:
    hotels_data = json.load(f)

# Load hotel details markdown
with open(hotel_details_path, 'r', encoding='utf-8') as f:
    hotel_details_text = f.read()

import os
from langchain_core.prompts import ChatPromptTemplate

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except Exception:
    try:
        from langchain_community.chat_models import ChatGoogleGenerativeAI
    except Exception:
        ChatGoogleGenerativeAI = None

if ChatGoogleGenerativeAI is None:
    raise ImportError(
        "Gemini chat model support not found. Install 'langchain-google-genai' or 'langchain_community' to use Gemini."
    )

GEMINI_MODEL = os.getenv("AI_AGENTIC_MODEL", "gemini-2.5-flash-lite")
GEMINI_API_KEY = os.getenv("AI_AGENTIC_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("AI_AGENTIC_API_KEY is not set. Set it to your Google Gemini API key before running this test agent.")

llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0, google_api_key=GEMINI_API_KEY)

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

    """Simple agent that answers questions using hotel files as context.
    """

    #----- Solo mostrar 3 hoteles  
    # if isinstance(hotels_data, dict):
    #     hotels_list_all = hotels_data.get("hotels") or hotels_data.get("Hotels") or []
    # elif isinstance(hotels_data, list):
    #     hotels_list_all = hotels_data
    # else:
    #     hotels_list_all = []
    # sample_hotels = hotels_list_all[:3]
    # hotels_json_snippet = json.dumps({"Hotels": sample_hotels}, ensure_ascii=False, indent=2)


    # Prepare context from loaded files
    hotel_context = f"""
{hotel_details_text}

Hotels JSON:
{json.dumps(hotels_data, ensure_ascii=False, indent=2)}
"""

    # Invoke the chain and return full response
    try:
        response = chain.invoke({
            "hotel_context": hotel_context,
            "question": question
        })
        return response.content
    except Exception as e:
        # Surface helpful error for API problems (auth, model, context limits)
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