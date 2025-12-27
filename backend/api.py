from fastapi import FastAPI
from pydantic import BaseModel
from backend.rag_engine import rag_answer

app = FastAPI()

class QueryRequest(BaseModel):
    question: str   # <-- we are using 'question' as the field

@app.post("/query")
async def query_api(request: QueryRequest):
    answer = rag_answer(request.question)
    return {"answer": answer}
