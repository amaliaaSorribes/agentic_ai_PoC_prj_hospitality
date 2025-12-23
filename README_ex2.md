# Agentic AI Hospitality PoC

# README exercise 2 - Booking Analytics with SQL Agent

Para este ejercicio empecé por la configuración del docker. 

Luego creé el agente bookings_sql_agent y lo desarrollé de forma básica. Con esto hecho añadi los archivos debugging-hotel_analytics.sql y test_given_hotel_analytics_sql en bookings-db/src. El primero es solo para ver visualmente el sql y relacionado que esperamos recibir del agente y poder comparar resultados. Y el segundo prueba cada una de las cuatro opciones de tipo de pregunta pero con hardcoding, solo interpreta el sql para obtener una respuesta comparable.

Después modifiqué bookings_sql_agent para también formar el sql por si solo y diferenciar los dos pasos de creación e interpretación para un posterior formateo de la respuesta. 

Puntos clave: especificar en el prompt del agent como actuar ante preguntas de occupancy y revpar, y permitir queries de entrada manual por el usuario que sean validas (relacionadas al database).

# Parte 2

He creado el orquestador que es otro agente que decide en base a la pregunta si llamar al sql, a rag_chain o directamente decir que no es una pregunta relacionada lo hace a través del llm.

Y para acabar he integrado el orquestador en main para que funcione con el websocket. He quitado el funcionamiento tanto con el ex0 como con las preguntas hardcoded porque no quiero que caiga por error en ellas y no en el orquestador.