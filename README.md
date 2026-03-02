# Epic-Vendor-Services-FAQ-Support-Copilot-Michael-Mui-
SymbolicHealthAI's Take Home


## Commands to Run:
- Download Ollama from website (Run OllamaSetup.exe /DIR=”<insert custom directory>”)
- Set environment variable OLLAMA_MODELS to be in D:<insert custom directory>
- Reset comp (fix)
- In cmd line: ollama pull llama3.2:1b (Should have model in custom directory)

## Development Priorities:
1. Core feature appears to be using an AI model to refer to the vendor FAQ on Epic's site in a JSON format.

2. Secondary feature is a UI (so frontend and therefore backend is for communication between user and model).

## Development Progress:
- Determine project structure:
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