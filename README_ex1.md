# Agentic AI Hospitality PoC

# README exercise 1 - Hotel Details with RAG

Para este ejercicio después de modificar la data a 50 hoteles, añadí en bookings-db/src el archivo de build_vector_store que crea los embeddings y guarda el sistema de vectores usando chroma en hotel_vector_store. Para comprobar que esta relación sucede correctamente hice test_vector_store que simplemente llama al vector store en modo lectura y prueba el funcionamiento haciendo una sola pregunta y contestando con el similarity_search.

Luego, implementé rag_chain que también accede al vector store para leerlo pero para contestar las preguntas primero crea un qa_chain enlazado con un llm con el parametro para retrieval k=5.

En ai_agents_hospitality-api dentro de agents creé hotel_details_agent y fuera hice el test_exercise_1. Este agente usa una prompt sencilla y accede al qa_chain del rag para contestar a las preguntas dadas. 

Observación: El agente no encuentra solución para todas las preguntas o no da una respuesta completa. Por ejemplo, en vez de listar los 50 hoteles, lista 5 al azar. Y la segunda y cuarta pregunta no es capaz de contestarlas. Creo que esto está relacionado con mantener la k=5, y que se solucionará al añadir el sql y el orquestador de los siguientes ejercicios.