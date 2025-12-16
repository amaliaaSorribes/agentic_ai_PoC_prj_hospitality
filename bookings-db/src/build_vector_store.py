import json
from langchain_community.document_loaders import JSONLoader, TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os

base_path = "../output_files/hotels"

# Load hotel data from JSON file
with open(os.path.join(base_path, "hotels.json"), "r", encoding="utf-8") as f:
    hotels = json.load(f)

json_loader = []

for hotel in hotels:
    json_loader.append(
        Document(
            page_content=json.dumps(hotel, ensure_ascii=False),
            metadata={"source": "hotels.json"}
        )
    )

details_loader = TextLoader(os.path.join(base_path, "hotel_details.md"), encoding="utf-8")
rooms_loader = TextLoader(os.path.join(base_path, "hotel_rooms.md"), encoding="utf-8")

documents = (
    json_loader
    + details_loader.load()
    + rooms_loader.load()
)

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

documents = text_splitter.split_documents(documents)

# Create embeddings and vector store
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("AI_AGENTIC_API_KEY"))
vectorstore = Chroma.from_documents(documents, embeddings, persist_directory="hotel_vector_store") #persist the vector store

vectorstore.persist()
print("Vector store built and persisted at 'hotel_vector_store'")