from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
import os

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("AI_AGENTIC_API_KEY"))

# Carga el vector store ya persistido
vectorstore = Chroma(
    persist_directory="hotel_vector_store",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
)

PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant that provides information about hotels.

Use ONLY the information in the context to answer the question.
If the answer is not in the context, respond with:
"I don't have the relevant information."

Context:
{context}

Question:
{question}

Answer:
"""
)

# Create retrieval chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT},
)

# Test retrieval quality with sample queries
if __name__ == "__main__":
    all_queries = [
        "What is the full address of Obsidian Tower?",
        "What are the meal charges for Half Board in hotels in Paris?",
        "List all hotels in France with their cities",
        "What is the discount for extra bed in Grand Victoria?",
        "Compare room prices between peak and off season for hotels in Nice"
    ]
    
    for query in all_queries:
        print("\nQuery:")
        print(query)

        result = qa_chain.invoke(query)

        print("\nResponse:")
        print(result["result"])

        print("\nDocuments used:")
        for doc in result["source_documents"]:
            print("-", doc.metadata)
