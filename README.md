# Epic-Vendor-Services-FAQ-Support-Copilot-Michael-Mui-
SymbolicHealthAI's Take Home

## Questions for Stand Up
- How to fine tune AI model? I seem to get responses that are irrelevant OR violate requirements.
- Can you clarify what TESTING.md is for?
- Not sure how to show that memory was used. Namely, prior turns in the conversation.
- Can you explain 'Handle empty state, invalid input, retrieval misses'?

Notes from Stand Up:
- Plan Mode over agent mode
- Make sure LLM is doing heavy lifting of RAG (highlight tradeoffs, currently light weight and inacurrate)
- Push LLM earlier in stack of process
- Goal from take home: spirit is to figure out my own ineffiencies in workflow and use AI to fix that
- Guardrail testing is most important in AI prompting, also don't forget regression testing.

## Commands to Run

**Prerequisites (one-time):**
1. Install [Ollama](https://ollama.com). On Windows, e.g.: `OllamaSetup.exe /DIR="<custom directory>"`.
2. Set `OLLAMA_MODELS` to that directory if using a custom location.
3. Pull the model: `ollama pull llama3.2:3b`  
   The app sends the full FAQ to the model and uses model-cited source IDs for grounding (Option C).

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
- `app.engine` loads the FAQ, formats it for the prompt, and calls Ollama for an answer with model-cited sources (requires Ollama running and `llama3.1:8b` pulled).

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

- Created backend API routes

- Creating/Changing min_score by adding param to run_query, also adjust in main.py's run_query call 

- Create Basic UI

- Eliminate unused code componenents

- Correct AI behavior
    - Irrelevance (what's the capital of France?) -> fix via adjusting min_score in engine.py (adjust run_query to use new param)

- Use a new model
    - allows for more context, send FAQ seed data into model with user query

    

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
- 

