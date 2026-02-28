from fastapi import FastAPI
from pydantic import BaseModel
from services.control.control_plane import handle_query

app = FastAPI(title="Meridian")

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_endpoint(request: QueryRequest):
    return handle_query(request.query)