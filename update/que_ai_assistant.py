from typing import Annotated , Literal , Sequence , TypedDict
from langchain_core.messages import HumanMessage , AIMessage , BaseMessage
from langgraph.graph.message import add_messages
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
import re


load_dotenv()
groq = os.getenv('GROQ')

llm =ChatGroq(model="llama-3.3-70b-versatile" , api_key=groq , temperature=0.7) 

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


prompt = PromptTemplate.from_template("""
You are a smart assistant. A student gives you a question paper if these number present in question paper then save respective txt file:
- `C109511(022)` → means save to ai.txt
- `C109512(022)` → means save to iml.txt
- `C109513(022)` → means save to toc.txt
- `C109514(022)` → means save to ps.txt
                                      

If the question contains "2025-april", then add heading: ### 2025-April Questions

Return response in this format:
file_name: ...
heading: ...
final_question: ...
                                      
C109511(022) , C109512(022) , C109513(022) , C109514(022) if any of these number is not present in text then return sorry upload right file.

Question: {question}""")

bound_llm = prompt | llm
def question_assistant(state:AgentState):
    messages = state["messages"]

    question = messages[-1].content
    responce = bound_llm.invoke({'question':question})
    output = responce.content.strip()
    print('Responce: ' ,output)


    file_name = re.search(r"file_name:\s*(.+)" , output)
    heading = re.search(r"heading:\s*(.+)", output)
    final_question = re.search(r"final_question:\s*(.+)", output)    

    if not file_name or not final_question:
        return "Error: Required info not found from LLM."
    
    file_name = file_name.group(1).strip()
    heading = heading.group(1).strip() if heading else None
    final_question = final_question.group(1).strip()


    try:
        with open(file_name, "a", encoding="utf-8") as f:
            if heading:
                f.write(f"\n{heading}\n")
            f.write(f"- {final_question}\n")
        return f"Saved"
    except Exception as e:
        return f"File write failed: {str(e)}"

