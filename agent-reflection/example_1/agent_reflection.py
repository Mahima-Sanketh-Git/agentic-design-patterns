import pandas as pd
from google import genai
from dotenv import load_dotenv
import os
import re
import base64

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)




def generate_chart_code(client:genai.Client,data_frame:str,instruction:str,out_path_v1:str):
    prompt = f"""
    You are a data visualization expert. Given the following dataframe, generate Python code using matplotlib to create a line chart of the inflation rates for Sri Lanka in 2024 and 2025.

    Return your answer *strictly* in this format:

    <execute_python>
    # valid python code here
    </execute_python>

    Do not add explanations, only the tags and the code.
    
    Dataframe:
    {data_frame.head().to_string()}
    
    The x-axis should represent the months, and the y-axis should represent the inflation rates. Include appropriate labels and a title for the chart.

    User instruction: {instruction}

    Requirements for the code:
    1. Assume the DataFrame is already loaded as 'df'.
    2. Use matplotlib for plotting.
    3. Add clear title, axis labels, and legend if needed.
    4. Save the figure as '{out_path_v1}' with dpi=300.
    5. Do not call plt.show().
    6. Close all plots with plt.close().
    7. Add all necessary import python statements
    8. CRITICAL: 'date' is datetime64 — never use string concatenation on it.
       Filter by year/quarter using the 'year' and 'quarter' integer columns.
    
    Return ONLY the code wrapped in <execute_python> tags.
    """
    
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    
    print(response.text)
    
    match  = re.search(r'<execute_python>(.*?)</execute_python>',response.text,re.DOTALL)

    if match:
        return match.group(1).strip()
    return None

def reflect_on_image_and_regenerate(client:genai.Client,chart_path: str,instruction: str,out_path_v2: str,code_v1: str,):

    with open(chart_path,"rb") as f:
        encode = base64.b64encode(f.read())
        encoded_str = encode.decode("utf-8")
        
    prompt = f"""
    You are a data visualization expert.
    Your task: critique the attached chart and the original code against the given instruction,
    then return improved matplotlib code.

    Original code (for context):
    {code_v1}
    
    Original Image (for context):
    {encoded_str}

    OUTPUT FORMAT (STRICT):
    1) First line: a valid JSON object with ONLY the "feedback" field.
    Example: {{"feedback": "The legend is unclear and the axis labels overlap."}}

    2) After a newline, output ONLY the refined Python code wrapped in:
    <execute_python>
    ...
    </execute_python>

    3) Import all necessary libraries in the code. Don't assume any imports from the original code.
    
    HARD CONSTRAINTS:
    - Do NOT include Markdown, backticks, or any extra prose outside the two parts above.
    - Use pandas/matplotlib only (no seaborn).
    - Assume df already exists; do not read from files.
    - Save to '{out_path_v2}' with dpi=300.
    - Always call plt.close() at the end (no plt.show()).
    - Include all necessary import statements.
    
    Instruction:
    {instruction}
    """
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents={
            "parts":[
                {"text":prompt},
                {
                    "inline_data":{
                        "mime_type":"image/png",
                        "data":encoded_str
                    }
                }
            ]
        }
    )
    
    match  = re.search(r'<execute_python>(.*?)</execute_python>',response.text,re.DOTALL)

    if match:
        return match.group(1).strip()
    return None

def run_workflow():
    df = pd.read_csv("sri_lanka_inflation_2024_2025.csv")
    
    print(df.head(5))    
    
    execute_code_draft = generate_chart_code(client=client,data_frame=df,instruction="Create a plot comparing inflation of Sri Lanka in 2024 and 2025 using the data in sri_lanka_inflation_2024_2025.csv",out_path_v1="chart_v1.png")

    exec(execute_code_draft,{"df":df})
    
    execute_code_final = reflect_on_image_and_regenerate(
    client=client,
    chart_path="chart_v1.png",            
    instruction="Create a plot comparing inflation of Sri Lanka in 2024 and 2025 using the data in sri_lanka_inflation_2024_2025.csv", 
    out_path_v2="chart_v2.png",
    code_v1=execute_code_draft,
    )
    exec(execute_code_final,{"df":df})
    
    
    
run_workflow()