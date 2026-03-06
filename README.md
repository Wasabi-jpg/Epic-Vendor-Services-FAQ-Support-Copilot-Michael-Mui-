# Epic-Vendor-Services-FAQ-Support-Copilot-Michael-Mui-
SymbolicHealthAI's Take Home

Notes from Stand Up:
- Plan Mode over agent mode
- Make sure LLM is doing heavy lifting of RAG (highlight tradeoffs, currently light weight and inacurrate)
- Push LLM earlier in stack of process
- Goal from take home: spirit is to figure out my own ineffiencies in workflow and use AI to fix that
- Guardrail testing is most important in AI prompting, also don't forget regression testing.

## Commands to Run

**Prerequisites (one-time):**
1. Install [Ollama](https://ollama.com). On Windows, e.g.: `OllamaSetup.exe /DIR="<custom directory>"`. Or just install it into your default location of installations.
2. Set `OLLAMA_MODELS` in your environment variables to a specified model directory if using a custom location. Default is fine if you have the space ( ~ 2.0 GB)
3. Pull the model from cmd line: `ollama pull llama3.2:3b`  

**Install dependencies (from project root):**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Start the app (while in PROJECT DIRECTORY with ACTIVE venv):**
```bash
uvicorn app.main:app --reload
```

**Run tests:**
```bash
pytest
```
*(Tests and TESTING.md to be added.)*

**Test engine and memory locally (from project root, with venv activated):**
```bash
python -m app.memory
python -m app.engine
```
- `app.memory` runs built-in sanity checks (no Ollama needed).
- `app.engine` loads the FAQ, formats it for the prompt, and calls Ollama for an answer with model-cited sources (requires Ollama running and `llama3.2:3b` pulled).


## Rationale for Tech Stack:
- FastAPI + Uvicorn: Python backend that was lightweight and easier to work with, esp with Python background.
- Ollama: local model download, no need for cloud-based models (Free models basically), and no keys.
- llama3.2:3b model: Popularity (credibility) + space used (~2 GB) + speed (compared with 8B) + accuracy (compared with 1B)
- Python: What I'm used to.
- Cursor: Good at developing actionable plans and coding them up. Project scope seemed small enough for it to handle. Still required actively reviewing code from my part and understanding high level functionality.
- Google Gemini: Good at developing high level project structure and starting off bouncing ideas.

## Completion Goals + Tradeoffs:
- 3B vs 8B: accuracy & speed, where 8B was seemingly more accurate pre-memory updates, but always too slow. 3B has the better speed and accuracy setting, even if not as accurate as 8B.
- 3B vs 1B: accuracy & context window, where 1B was assisted by FAQ query matcher versus 3B which took in the entire FAQ as context. 3B had more reliability.
- 


## Development Plan:

- Determine Project Structure (DONE)
- pip install ollama, fastapi, uvicorn, pytest, save to requirements.txt. (DONE)
- Create dataset for context (Grab from Epic Vendor's FAQ) and input into SEED_DATA/epic_vendor_faq.json. (DONE)
- focus on ollama logic and faq search (engine.py and memory.py) and interact via terminal for testing. (DONE)
- upon completing engine.py and memory.py, focus on UI (index.html) and backend (main.py) for routing user chat with model. (DONE)

- Test model performance (check testing)
- Test memory.py via testing suite
- 
- Clean up set up for easy reader digestion. (for the <= 10 min setup)
- Take notes of development in markdown files.

