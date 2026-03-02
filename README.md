# Epic-Vendor-Services-FAQ-Support-Copilot-Michael-Mui-
SymbolicHealthAI's Take Home


## Commands to Run:
- Download Ollama from website (Run OllamaSetup.exe /DIR=”<insert custom directory>”)
- Set environment variable OLLAMA_MODELS to be in D:<insert custom directory>
- Reset comp (fix)
- In cmd line: ollama pull llama3.2:1b (Should have model in custom directory)
- 

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

- Creating JSON dataset

## Development Plan:

- Determine Project Structure
- pip install ollama, fastapi, uvicorn, save to requirements.txt.
- Create dataset for context (Grab from Epic Vendor's FAQ) and input into SEED_DATA/epic_vendor_faq.json.
- focus on ollama logic and faq search (engine.py and memory.py) and interact via terminal for testing.
- upon completing engine.py and memory.py, focus on UI (index.html) and backend (main.py) for routing user chat with model.

