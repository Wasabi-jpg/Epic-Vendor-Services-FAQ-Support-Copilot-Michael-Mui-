from fastapi import FastAPI
from pydantic import BaseModel
from app.engine import load_faq, run_query
from app.memory import get_recent_turns, add_turn, memory_used

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

# 2. Add the bouncer (Middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_credentials=True,    
    allow_methods=["*"],      
    allow_headers=["*"]
)



class Query(BaseModel):
    query: str



json_faq = load_faq() # prepare the faq for the model
@app.get("/")
def read_root():
    return {"status": "FastAPI is running!"}

@app.post("/chat", response_model=dict)
def send_query(user_query: Query):
    query_text = (user_query.query or "").strip()
    if not query_text: # For the sake of other interactions not using this associated UI, to at least provide a way to handle empty queries.
        return {
            "answer": "Please ask a question about Epic Vendor Services.",
            "sources": [],
            "memory_used": False,
        }

    chat_history = get_recent_turns(4)

    res = run_query(query_text, conversation_history=chat_history, faq_data=json_faq)
    res_ans = res["answer"]
    res_sources = res["sources"]
    res_memory = res.get("memory_used", False)

    add_turn(role="user", content=query_text)
    add_turn(role="assistant", content=res_ans)

    return {
        "answer": res_ans,
        "sources": res_sources,
        "memory_used": res_memory,
    }

