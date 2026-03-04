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
    # Prep history of chat
    
    chat_history = get_recent_turns(6) # Adjustable chat history of user and model turns

    did_memory_use = memory_used()
    # run_query(), so ask the model, returns a dict with keys "answer", "sources", "model_used"
    ''' run_query():
    query: str,
    conversation_history: list[dict] | None = None,
    faq_data: list[dict] | None = None,
    model: str = "llama3.2:1b",
    top_k: int = 3,
    min_score: float = 0.0 -> for the sake of retrieving the faq entries
    '''
    res = run_query(user_query.query, conversation_history=chat_history, faq_data=json_faq, min_score=0.2)

    res_ans = res['answer']
    res_sources = res['sources']
    

    add_turn(role='user', content=user_query.query)
    add_turn(role='assistant', content=res_ans)

    return {
        'answer': res_ans,
        'sources' : res_sources, # Has the grounding info for source URLs
        # Not sure how to represent memory being used. Check below?
        'memory_used': did_memory_use # True if there is at least 1 prior turn. TODO: Represent in UI
    }

