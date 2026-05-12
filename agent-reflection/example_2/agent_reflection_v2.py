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
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        print(response.text)

        return response.text.strip()
    except Exception as exc:
        print(f"SQL generation failed: {exc}")
        return ""

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
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        print(response.text)

        return response.text.strip()
    except Exception as exc:
        print(f"SQL reflection failed: {exc}")
        return ""
    

def run_workflow():
    try:
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

        sql_code_v1 = generate_sql_code(client, question, schema)
        if not sql_code_v1:
            print("Skipping workflow because no SQL draft was generated.")
            return

        try:
            obj = json.loads(sql_code_v1)
        except json.JSONDecodeError as exc:
            print(f"Could not parse draft SQL JSON: {exc}")
            return

        code_ouput_v1 = str(obj.get("draft_sql", "")).strip()
        if not code_ouput_v1:
            print("Draft SQL is empty.")
            return

        try:
            row_output = utils.exec_sql(code_ouput_v1)
        except Exception as exc:
            print(f"Initial SQL execution failed: {exc}")
            return

        sql_code_v2 = reflect_on_sql_with_external_feedback_and_regenerate(client, sql_code_v1, row_output, schema)
        if not sql_code_v2:
            print("Skipping final SQL execution because no refined SQL was generated.")
            return

        try:
            obj_v2 = json.loads(sql_code_v2)
        except json.JSONDecodeError as exc:
            print(f"Could not parse refined SQL JSON: {exc}")
            return

        row_output_v2 = str(obj_v2.get("refined_sql", "")).strip()
        feedback_v2 = str(obj_v2.get("feedback", "")).strip()
        print(feedback_v2)

        if not row_output_v2:
            print("Refined SQL is empty.")
            return

        try:
            utils.exec_sql(row_output_v2)
        except Exception as exc:
            print(f"Final SQL execution failed: {exc}")
    except Exception as exc:
        print(f"Workflow failed: {exc}")


if __name__ == "__main__":
    run_workflow()