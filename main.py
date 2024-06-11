from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import langchain_agent  # Import langchain_agent from agent.py
import logging

class Query(BaseModel):
    query: str

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

@app.post("/query")
def handle_query(query: Query):
    logging.debug(f"Received query: {query.query}")
    result = langchain_agent(query.query)
    if isinstance(result, str) and "Error" in result:
        raise HTTPException(status_code=400, detail=result)
    return {"result": result}



# The __main__ block to run the server when deployed to render.com
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)