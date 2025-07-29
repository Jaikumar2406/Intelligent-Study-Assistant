import re
import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
groq = os.getenv('GROQ')

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq, temperature=0.3)

def llm_query_router(user_query):
    prompt = f"""
You are a smart assistant that decides which file and unit to use based on the user's request.

Available syllabus files and their subjects:
- toc_syllabus.txt (Theory of Computation)
- ps_syllabus.txt (Probability and Statistics)
- iml_syllabus.txt (Intro to Machine Learning)
- ai_syllabus.txt (Artificial Intelligence)

Available PYQ files:
- toc.txt
- ps.txt
- iml.txt
- ai.txt

Valid Units (in every subject):
- Unit-I
- Unit-II
- Unit-III
- Unit-IV
- Unit-V

When the user says: "{user_query}", return a JSON like this with the most relevant file and unit:
{{
  "syllabus_path": "<one of the syllabus files above>",
  "pyq_pdf_path": "<matching pyq txt>",
  "unit": "<one of Unit-I to Unit-V>"
}}

If you don’t know the answer, just say:
"Sorry, I don’t know. I will update soon."
"""
    response = llm.invoke(prompt).content

    try:
        json_str = re.search(r"\{.*\}", response, re.DOTALL).group()
        result = json.loads(json_str)
    except Exception as e:
        print("Failed to parse LLM response:", e)
        result = {}

    return result
