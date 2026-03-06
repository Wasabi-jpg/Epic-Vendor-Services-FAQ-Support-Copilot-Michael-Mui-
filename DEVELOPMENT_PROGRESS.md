## Development Priorities:
1. Core feature appears to be using an AI model to refer to the vendor FAQ on Epic's site in a JSON format. (Chat itself could theoretically be kept to the terminal out of prioritizing functionality).

2. Secondary feature is a UI (so frontend and therefore backend is for communication between user and model).

3. Fine tune the model's responses

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

- Created Basic UI

- Eliminated unused code componenents

- Corrected (relatively) AI behavior
    - Irrelevance (what's the capital of France?) -> fix via adjusting min_score in engine.py (adjust run_query to use new param)

- Using a new model (final choice: llama3.2:3b)
    - allows for more context, send FAQ seed data into model with user query
    - went from 1B to 8B to 3B, tried 8B again for accuracy, but 3B is the sweet spot for speed and accuracy.