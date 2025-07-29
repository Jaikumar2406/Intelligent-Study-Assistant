# from typing import Annotated, Sequence, TypedDict
# from langchain_core.messages import BaseMessage 
# from dotenv import load_dotenv
# import os
# from langchain_groq import ChatGroq
# from predictive_files.ai import extract_text_from_file1
# from predictive_files.iml import extract_text_from_file2
# from predictive_files.toc import extract_text_from_file4
# from predictive_files.ps import extract_text_from_file3
# from langgraph.graph.message import add_messages
# from langchain_core.prompts import PromptTemplate
# from predictive_files.read_txt_file import read_txt_file





# load_dotenv()
# groq = os.getenv('GROQ')
# llm = ChatGroq(api_key=groq, temperature=0.5, model="llama-3.3-70b-versatile")


# tools = [extract_text_from_file1 , extract_text_from_file2 , extract_text_from_file3 , extract_text_from_file4 , read_txt_file]

# class AgentState(TypedDict):
#     messages: Annotated[Sequence[BaseMessage], add_messages]
# def ai_assistant(state: AgentState):
#     messages = state["messages"]
#     question = messages[-1].content  

#     llm_with_tool = llm.bind_tools(tools)

#     prompt = PromptTemplate(
#     template="""
# You are an intelligent AI assistant designed to help students analyze computer science subjects using syllabus and previous year question papers (PYQs).

# Follow these instructions carefully:

# 1. If the user asks to predict important topics or questions from a specific subject and unit (e.g., "TOC unit 1"), then call the `similarity` tool to match syllabus with uploaded PYQs and give topic-wise importance.
# 2. If the user says they want to upload a question paper (e.g., "I want to upload a PDF"), respond with:  
#    "Please upload your question paper PDF. Make sure it contains a valid code like c1009289(022)."
# 3. If the uploaded PDF is valid and contains the code, call the `tools` tool to extract and store questions.
# 4. If the user's message is a greeting ("hi", "hello"), just greet them politely.
# 5. If the user provides their name, email info, acknowledge politely and remember if needed.
# 6. For any other unknown query, say: "Sorry, I don't know the answer to that."
# if user ask i want to see my syllabus ask them which subject syllabus you want to see and give the syllabus name and also asl unit if user give subject name and unit name then open respective txt file and show them there answer , use read_tst_file tool.


# Also:
# - Always keep your answers between 0 and 500 words.
# - Keep your responses student-friendly and helpful.

# Question: {question}
# """,
#     input_variables=["question"]
#     )

#     chain = prompt | llm_with_tool
#     response = chain.invoke({"question": question})
#     return {"messages": [response]}


from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, AIMessage, FunctionMessage
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from predictive_files.ai import extract_text_from_file1
from predictive_files.iml import extract_text_from_file2
from predictive_files.toc import extract_text_from_file4
from predictive_files.ps import extract_text_from_file3
from langgraph.graph.message import add_messages
from langchain_core.prompts import PromptTemplate
from predictive_files.read_txt_file import read_txt_file

from langchain_core.tools import tool

load_dotenv()
groq = os.getenv('GROQ')
llm = ChatGroq(api_key=groq, temperature=0.5, model="llama-3.3-70b-versatile")

# Make sure all tools are decorated properly
tools = [extract_text_from_file1, extract_text_from_file2, extract_text_from_file3, extract_text_from_file4, read_txt_file]

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def ai_assistant(state: AgentState):
    messages = state["messages"]
    question = messages[-1].content

    llm_with_tool = llm.bind_tools(tools)

    prompt = PromptTemplate(
        template="""
You are an intelligent AI assistant designed to help students analyze computer science subjects using syllabus and previous year question papers (PYQs).

Follow these instructions carefully:

1. If the user asks to predict important topics or questions from a specific subject and unit (e.g., "TOC unit 1"), then call the `similarity` tool to match syllabus with uploaded PYQs and give topic-wise importance.
2. If the user says they want to upload a question paper (e.g., "I want to upload a PDF"), respond with:  
   "Please upload your question paper PDF. Make sure it contains a valid code like c1009289(022)."
3. If the uploaded PDF is valid and contains the code, call the `tools` tool to extract and store questions.
4. If the user's message is a greeting ("hi", "hello"), just greet them politely.
5. If the user provides their name, email info, acknowledge politely and remember if needed.
6. For any other unknown query, say: "Sorry, I don't know the answer to that."
If user asks 'I want to see my syllabus', ask them which subject and unit. If both are given, then open respective txt file and use read_txt_file tool.

Always keep your answers between 0 and 500 words.
Keep your responses student-friendly and helpful.

Question: {question}
""",
        input_variables=["question"]
    )

    chain = prompt | llm_with_tool
    response = chain.invoke({"question": question})

    # Step 1: Check for tool calls
    if isinstance(response, AIMessage) and response.tool_calls:
        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        # Step 2: Find the matching tool
        for tool in tools:
            if tool.name == tool_name:
                tool_output = tool.invoke(tool_args)
                break
        else:
            tool_output = "Tool not found."

        # Step 3: Give tool result to LLM
        final_response = llm_with_tool.invoke({
            "question": question,
            "messages": [
                response,
                FunctionMessage(name=tool_name, content=tool_output)
            ]
        })
        return {"messages": [final_response]}

    # If no tool was used
    return {"messages": [response]}
