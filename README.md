# Epic-Vendor-Services-FAQ-Support-Copilot-Michael-Mui-
SymbolicHealthAI's Take Home


## Commands to Run

**Prerequisites (one-time):**
1. Install [Ollama](https://ollama.com). On Windows, e.g.: `OllamaSetup.exe /DIR="<custom directory>"`.
2. Set `OLLAMA_MODELS` to that directory if using a custom location.
3. Pull the model: `ollama pull llama3.2:1b`

**Install dependencies (from project root):**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Start the app:**
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
- `app.engine` loads the FAQ, runs retrieval for a sample query, then calls Ollama for an answer with sources (requires Ollama running and `llama3.2:1b` pulled).

## Development Priorities:
1. Core feature appears to be using an AI model to refer to the vendor FAQ on Epic's site in a JSON format. (Chat itself could theoretically be kept to the terminal out of prioritizing functionality).

2. Secondary feature is a UI (so frontend and therefore backend is for communication between user and model).

## Development Progress:
- Determined project structure:
```text
epic-support-copilot/
├── .venv/                  # Virtual environment (hidden)
├── SEED_DATA/
│   └── epic_vendor_faq.json # Local Q&A knowledge base
├── app/
│   ├── main.py             # FastAPI entry point
│   ├── engine.py           # FAQ Search & Ollama logic
│   └── memory.py           # Session management
├── UI/
│   └── index.html          # Chat interface
├── README.md               # Setup and usage guide
├── AI_USAGE.md             # AI assistance documentation
└── requirements.txt        # Project dependencies
```

- Created JSON dataset

- Created engine for model
    - created json data loader to load from SEED_DATA/epic_vendor_faq.json
    - created scoring function based on user query and faq content
    - created universal prompt with dynamic context based on scoring function results 

- Created memory component for model

- 

## Development Plan:

- Determine Project Structure
- pip install ollama, fastapi, uvicorn, save to requirements.txt.
- Create dataset for context (Grab from Epic Vendor's FAQ) and input into SEED_DATA/epic_vendor_faq.json.
- focus on ollama logic and faq search (engine.py and memory.py) and interact via terminal for testing.
- upon completing engine.py and memory.py, focus on UI (index.html) and backend (main.py) for routing user chat with model.

