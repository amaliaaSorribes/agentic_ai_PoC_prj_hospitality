from openai import OpenAI
client = OpenAI()

def detectar_agente_llm(pregunta):
    prompt = f"""
    Solo clasifica la siguiente pregunta en 'SQL' si requiere consultar una base de datos,
    o 'RAG' si requiere información de documentos:
    
    Pregunta: "{pregunta}"
    
    Respuesta:
    """
    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user", "content": prompt}],
        max_tokens=10
    )
    return respuesta.choices[0].message.content.strip().lower()

# Ejemplo de uso
pregunta_ejemplo_sql = "What is the occupancy rate for Obsidian Tower in January 2025?"
pregunta_ejemplo_rag = "What is the direction of Obsidian Tower?"

tipo_agente1 = detectar_agente_llm(pregunta_ejemplo_sql)
print(f"Pregunta: {pregunta_ejemplo_sql}\nTipo de agente recomendado: {tipo_agente1}\n")
tipo_agente2 = detectar_agente_llm(pregunta_ejemplo_rag)
print(f"Pregunta: {pregunta_ejemplo_rag}\nTipo de agente recomendado: {tipo_agente2}\n")