# Agentic AI Hospitality PoC

# README exercise 0 - Simple Agentic Assistant with File Context 

Este primer ejercicio me lo tomé como el espacio perfecto para trastear y sobretodo intentar entender como funcionaba cada parte.

Una vez tenía todo configurado (venv iniciado y todos las librerias importadas) probé test_exercise_0.py y vi que aunque ponía que todos los tests pasaban la única respuesta que conseguía el agente era la segunda pregunta. 

También copié el código del workshop en un nuevo file my_test_agent.py para ver la diferencia. Y ese lo mantuve usando los 5 hoteles. En general el mayor cambio es el formato.

Por otro lado, antes de saber de la existencia de la versión gratuita de gemini, decidí usar la api-key de chatgpt-openai. Y cuando vi que las otras tres preguntas no producían una respuesta válida (ponía que no tenía esa información) y apoyándome en copilot, pensé que openai tenía un límite máximo de respuesta menor al de gemini.

Entonces cambié a usar api-key de gemini y vi que me daba un resultado parecido. En este punto ya entendí que era lo esperado pero quise ver si podía igualmente "solucionarlo" y tras un par de preguntas a copilot lo conseguí. 

El problema por así decir es que el resto de preguntas necesitaban usar más tiempo la database y más carácteres para contestar. Por eso tronqué un poco los datos que recibia el agente para que pudiese llegar antes a la respuesta.

_Nota_: Algo que también me confundía es que el comando "python src/gen_synthetic_hotels.py --num_hotels 3" solo modificaba hotels.xlsx y no el resto de archivos en ouput_files/hotels. Entonces por mucho que estuviese capandolo a 3 hoteles en hotel_simple_agent.py realmente estaba mirando por la database para 5 hoteles. Lo acabo de cambiar a que realmente sean 3 modificando generate_hotels_parameters.yaml directamente.

