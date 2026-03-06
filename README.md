# Epic-Vendor-Services-FAQ-Support-Copilot-Michael-Mui-
SymbolicHealthAI's Take Home


## Commands to Run

**Prerequisites (one-time):**
1. Install [Ollama](https://ollama.com). On Windows, e.g.: `OllamaSetup.exe /DIR="<custom directory>"`. Or just install it into your default location of installations.
2. Set `OLLAMA_MODELS` in your environment variables to a specified model directory if using a custom location. Default is fine if you have the space ( ~ 2.0 GB). Open a new terminal instead if you do change the environment variable. Run the next commands in this new terminal.
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

## Limitations:
- 3B might guess what the user might want, especially for irrelevant queries. 3B might also call upon memory for unrelated query, due to potentially even the slightest related aspect.

## Future upgrades:
- Experiment with differing models on ollama.
- vector style database? Due to project timeline and lack of experience in this, didn't try. Would like to try at some point potentially for learning.

