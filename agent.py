import sqlite3
import requests
from langchain.chains import LLMChain
#from langchain.llms import OpenAI
#from langchain_community.llms import OpenAI
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

# Path to the Northwind Database
db_path = "northwind-SQLite3/dist/northwind.db"

# Initialize OpenAI LLM
llm = OpenAI(api_key="sk-proj-ou42ut9DZQeEdM32QvPrT3BlbkFJPSOvWh22fjsfpMcdr6GA")

# Define prompt templates for different types of queries
sql_prompt_template = PromptTemplate(
    input_variables=["query"],
    template="Translate this natural language query into SQL: {query}"
)

api_prompt_template = PromptTemplate(
    input_variables=["query"],
    template="Identify the type of data this query requests and provide the corresponding API URL: {query}"
)

def query_database(sql_query):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        return str(e)

def fetch_api_data(url):
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return str(e)

def fetch_api_data_with_auth(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": str(http_err), "response": response.json()}
    except Exception as e:
        return str(e)

def langchain_agent(input_text):
    # Initialize OpenAI LLM
    llm = OpenAI(api_key="sk-proj-ou42ut9DZQeEdM32QvPrT3BlbkFJPSOvWh22fjsfpMcdr6GA")

    # Define prompt templates for different types of queries
    sql_prompt_template = PromptTemplate(
        input_variables=["query"],
        template="Translate this natural language query into SQL: {query}"
    )

    api_prompt_template = PromptTemplate(
        input_variables=["query"],
        template="Identify the type of data this query requests and provide the corresponding API URL: {query}"
    )

    # Determine the type of query
    if "select" in input_text.lower():
        return query_database(input_text)
    
    # Use LLM to determine the type of query and process accordingly
    sql_chain = LLMChain(llm=llm, prompt=sql_prompt_template)
    api_chain = LLMChain(llm=llm, prompt=api_prompt_template)
    
    if "cat fact" in input_text.lower():
        return fetch_api_data("https://catfact.ninja/fact")
    elif "weather" in input_text.lower():
        city = input_text.split("weather in ")[-1]
        api_key = "13cea662444becdcd7526464d45ee72c"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        return fetch_api_data_with_auth(url, {})
    
    # Determine if it's a database or API query
    sql_result = sql_chain.run({"query": input_text})
    if "SELECT" in sql_result.upper():
        return query_database(sql_result)
    
    api_result = api_chain.run({"query": input_text})
    if "http" in api_result.lower():
        return fetch_api_data(api_result)
    
    return "Unsupported query type"
