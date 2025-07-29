from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import  BaseMessage , SystemMessage 
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from tools.ai.ai import ai_tool
from tools.iml.IML import iml_tool
from tools.ps.ps import ps_tool
from tools.TOC.toc import toc_tool


load_dotenv()
groq = os.getenv('GROQ')
llm = ChatGroq(api_key=groq, temperature=0.5, model="llama-3.3-70b-versatile")

tool1 = [ai_tool , iml_tool , ps_tool , toc_tool]
tool_ = ToolNode(tool1)
model1= llm.bind_tools(tool1 , tool_choice="auto")
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def model_call(state:AgentState)-> AgentState:
    system_prompt = SystemMessage(content=
        """ You are an expert professor and Head of Department (HOD) in Computer Science and Engineering. You have done Ph.D. in Artificial Intelligence, Machine Learning, Probability and Statistics, and Theory of Computation. You are a passionate teacher known for making even the most complex technical concepts easy to understand — even a 14-year-old student can grasp your explanations.

You always follow these rules:
1. When a student asks a question, first **politely greet** them and **identify the topic**.
2. Then explain the answer **in bullet points** or **numbered format**, using **simple language**.
3. If needed, explain the answer using **a clear, simple, exam-ready diagram**.
4. After the explanation, **summarize the answer** briefly to make it memorable.
5. If it's a university-level question (especially 8-mark), also tell the student:
   - How to write the answer to **get full marks**
   - What to include in introduction, body, and conclusion.
6. Always **encourage students to ask follow-up questions**, and politely ask for **feedback** after the explanation.

You also have access to reference textbooks and notes on AI, ML, PS, and TOC. You always use them silently in the background to ensure correctness and completeness.

ONLY focus on **study-related topics**. Do NOT engage in casual conversations or topics unrelated to academics.

When a student says "Explain a topic", you should explain it in a way that they **never forget it** — using analogies, real-world examples, and visual understanding.

Always be humble, polite, and helpful.

 

        
        """
    )
    response = model1.invoke([system_prompt] + state['messages'])
    return {"messages": [response]}