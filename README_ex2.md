# Agentic AI Hospitality PoC

# README exercise 2 - Booking Analytics with SQL Agent

Para este ejercicio empecé por la configuración del docker. 

Luego creé el agente bookings_sql_agent y lo desarrollé de forma básica. Con esto hecho añadi los archivos debugging-hotel_analytics.sql y test_given_hotel_analytics_sql en bookings-db/src. El primero es solo para ver visualmente el sql y relacionado que esperamos recibir del agente y poder comparar resultados. Y el segundo prueba cada una de las cuatro opciones de tipo de pregunta pero con hardcoding, solo interpreta el sql para obtener una respuesta comparable.

Después modifiqué bookings_sql_agent para también formar el sql por si solo y diferenciar los dos pasos de creación e interpretación para un posterior formateo de la respuesta. 

Puntos clave: especificar en el prompt del agent como actuar ante preguntas de occupancy y revpar, y permitir queries de entrada manual por el usuario que sean validas (relacionadas al database).