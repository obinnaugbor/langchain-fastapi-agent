import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import langchain_agent  # Import langchain_agent from agent.py
import logging
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


class Query(BaseModel):
    query: str

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

# Fetch the API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI LLM with the API key from environment variables
llm = OpenAI(api_key=OPENAI_API_KEY)

@app.post("/query")
def handle_query(query: Query):
    logging.debug(f"Received query: {query}")
    result = langchain_agent(query.query)
    if isinstance(result, str) and "Error" in result:
        raise HTTPException(status_code=400, detail=result)
    return {"result": result}


# The __main__ block to run the server when executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
