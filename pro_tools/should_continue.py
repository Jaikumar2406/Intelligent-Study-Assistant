from typing import Annotated,Sequence, TypedDict
from langchain_core.messages import  BaseMessage
from langgraph.graph.message import add_messages



class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
def should_continue(state: AgentState) -> str:
    messages = state['messages']
    last_message = messages[-1]
    if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
        return "end"
    else:
        return "continue"