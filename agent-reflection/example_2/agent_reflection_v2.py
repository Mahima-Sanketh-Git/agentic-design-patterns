import pandas as pd
from google import genai
from dotenv import load_dotenv
import os
import json
import utils

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)


def generate_sql_code(client:genai.Client,question:str,schema:str):
    prompt = f"""
    You are a SQL expert. Given the following database schema, generate SQL code to answer the question below.

    Database Schema:
    {schema}

    Question: {question}

    Requirements for the SQL code:
    1. Write valid SQL code that can be executed on a SQLite database.
    2. Use appropriate JOINs if necessary.
    3. Include WHERE clauses to filter data based on the question.
    4. Return only the SQL code without any explanations or comments.
    
    Return STRICT JSON with one fields:
    {{
    "draft_sql": "<draft SQL to run>"
    }}
    """
    
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    
    print(response.text)
    
    return response.text.strip()

def reflect_on_sql_with_external_feedback_and_regenerate(client:genai.Client,sql_code_v1: str,feedback_v1:str,schema:str):
    prompt = f"""
    You are a SQL expert. Given the following SQL code and feedback, reflect on the feedback and regenerate the SQL code to better answer the original question.

    Original SQL Code:
    {sql_code_v1}

    Feedback:
    {feedback_v1}
    
    Database Schema:
    {schema}

    Requirements for the regenerated SQL code:
    1. Write valid SQL code that can be executed on a SQLite database.
    2. Use appropriate JOINs if necessary.
    3. Include WHERE clauses to filter data based on the original question and feedback.
    4. Return only the SQL code without any explanations or comments.
    
    Return STRICT JSON with two fields:
    {{
    "feedback": "<1-3 sentences explaining the gap or confirming correctness>",
    "refined_sql": "<final SQL to run>"
    }}
    """
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    
    print(response.text)
    
    return response.text.strip()
    

def run_workflow():
    schema = """
    Table: transactions
    - id (INTEGER)
    - product_id (INTEGER)
    - product_name (TEXT)
    - brand (TEXT)
    - category (TEXT)
    - color (TEXT)
    - action (TEXT) -- insert | restock | sale | price_update
    - qty_delta (INTEGER) -- positive for insert/restock, negative for sale
    - unit_price (REAL)
    - notes (TEXT)
    - ts (DATETIME)
    """

    question = "Which color of product has the highest total sales?"
    
    sql_code_v1 = generate_sql_code(client,question,schema) # first llm resposne

    obj = json.loads(sql_code_v1)
    code_ouput_v1 = str(obj.get("draft_sql","")).strip()
    row_output = utils.exec_sql(code_ouput_v1) # run the initial sql (without reflection) code and get results
    
    sql_code_v2 = reflect_on_sql_with_external_feedback_and_regenerate(client,sql_code_v1,row_output,schema) # second llm response with feedback and revised code
    
    obj_v2 = json.loads(sql_code_v2)
    row_output_v2 = str(obj_v2.get("refined_sql","")).strip()
    feedback_v2 = str(obj_v2.get("feedback","")).strip()
    print(feedback_v2)
    utils.exec_sql(row_output_v2) # run the final sql code and get results
    
run_workflow()