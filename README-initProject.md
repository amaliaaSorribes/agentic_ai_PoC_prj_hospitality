# Agentic AI Hospitality PoC

# README - How to start the program

1. **open wsl** 
    - click en caja azul abajo izquierda
    - make sure you are in branch ex2

2. `cd agentic_ai_PoC_prj_hospitality`

3. **activate venv** 
    - `source venv/bin/activate`

4. **save api keys for llms** 
    - `export AGENTIC_AI_API_KEY="myapikey"`
    - `export OPENAI_API_KEY="myapikey"` 

5. `cd ai_agents_hospitality-api`

6. **init docker**
    - `docker start bookings-db`

7. **run program**
    - `python main.py`
    - find example queries in orchestrator.py - test_orch