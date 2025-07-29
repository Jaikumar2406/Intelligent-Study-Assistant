import sys
sys.path.append("./predictive_files")
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from predictive_files.important_topic import important_topics
from pydantic import BaseModel
from predictive_files.ai import extract_text_from_file1
from predictive_files.iml import extract_text_from_file2
from predictive_files.toc import extract_text_from_file4
from predictive_files.ps import extract_text_from_file3
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from tools.ai.ai import ai_tool
from tools.iml.IML import iml_tool
from tools.ps.ps import ps_tool
from tools.TOC.toc import toc_tool
from pro_tools.ai_assistant import ai_assistant
from pro_tools.model_call import model_call
from pro_tools.should_continue import should_continue
from predictive_files.read_txt_file import read_txt_file

app = FastAPI()
class InputText(BaseModel):
    input: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tools = [extract_text_from_file1 , extract_text_from_file2 , extract_text_from_file3 , extract_text_from_file4 , read_txt_file]
tool_node = ToolNode(tools)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

workflow = StateGraph(AgentState)
workflow.add_node("My_Ai_Assistant", ai_assistant)
workflow.add_node("tool", tool_node)
workflow.add_node("similarity", important_topics)
workflow.add_edge(START, "My_Ai_Assistant")
workflow.add_conditional_edges(
    "My_Ai_Assistant",
    tools_condition,
    {
        "tools": "tool",
        "similarity": "similarity",
        END: END
    }
)

ap = workflow.compile()

@app.get("/")
def home():
    return {"message": "Hello from AI Agent!"}

@app.post("/question")
async def generate_text(data: InputText):
    user_input = data.input.strip()

    if user_input.lower() in {"exit", "quit", "stop"}:
        return {"answer": "Session ended."}

    try:
        result = await ap.ainvoke({"messages": [HumanMessage(content=user_input)]})
        last_msg = result["messages"][-1]

        if isinstance(last_msg, AIMessage) and last_msg.content:
            return {"answer": last_msg.content}
        else:
            return {"answer": "I'm processing your request..."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

tool1 = [ai_tool , iml_tool , ps_tool , toc_tool]
tool_ = ToolNode(tool1)   
graph = StateGraph(AgentState)
graph.add_node("our_agent" , model_call)
graph.add_node("tool" , tool_)
graph.set_entry_point("our_agent")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tool",
        "end": END
    }
)

graph.add_edge("tool", "our_agent")
ap1 = graph.compile()


@app.post("/syllabus")
async def professor_explainer(data: InputText):
    try:
        user_input = data.input.strip()
        if user_input.lower() in {"exit", "quit", "stop"}:
            return {"answer": "Session ended."}

        result = await ap1.ainvoke({"messages": [HumanMessage(content=user_input)]})
        last_msg = result["messages"][-1]

        if isinstance(last_msg, AIMessage) and last_msg.content:
            return {"answer": last_msg.content}
        return {"answer": "I'm thinking on it..."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))