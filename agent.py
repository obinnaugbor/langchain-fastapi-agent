import sqlite3
import requests
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

# Path to the Northwind Database
db_path = "northwind-SQLite3/dist/northwind.db"  # Update this with your actual path

class Query(BaseModel):
    query: str

app = FastAPI()

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
        return response.json()
    except Exception as e:
        return str(e)

def langchain_agent(input_text):
    if "select" in input_text.lower():  # Adjusted condition to better identify SQL queries
        return query_database(input_text)
    elif "cat fact" in input_text.lower():  # Simple condition to identify cat fact requests
        return fetch_api_data("https://catfact.ninja/fact")
    elif "weather" in input_text.lower():  # Simple condition to identify weather requests
        city = input_text.split("weather in ")[-1]
        api_key = "13cea662444becdcd7526464d45ee72c"  # Replace with your actual API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        return fetch_api_data_with_auth(url, {})
    else:
        return "Unsupported query type"