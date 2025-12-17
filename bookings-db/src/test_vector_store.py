# Test rápido para verificar que el vector store se ha construido y persistido correctamente

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Carga el vector store ya persistido
vectorstore = Chroma(
    persist_directory="hotel_vector_store",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
)

# Prueba rápida: buscar los 3 vectores más similares a una query
query = "What is the full address of Obsidian Tower?"
results = vectorstore.similarity_search(query, k=3)

# Imprimir resultados
for i, doc in enumerate(results, 1):
    print(f"Resultado {i}:")
    print(doc.page_content)
    print(doc.metadata)
    print("-" * 10)
