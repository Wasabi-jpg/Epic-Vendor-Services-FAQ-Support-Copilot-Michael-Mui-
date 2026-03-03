from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"status": "FastAPI is running!"}

# @app.post("/chat")
# def send_query(user_query: str):
#     query_item = Query(user_query)
#     return query_item