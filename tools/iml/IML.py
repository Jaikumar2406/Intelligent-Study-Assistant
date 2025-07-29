import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain.tools.retriever import create_retriever_tool

load_dotenv()

pine_cone = os.getenv('PINE_CONE')
groq = os.getenv('GROQ')
hugging_face = os.getenv("HUGGING_FACE")
host_bg = os.getenv('HOST_BG')


llm = ChatGroq(model='llama-3.3-70b-versatile' , temperature=0.7 , api_key=groq)
embeddings = HuggingFaceBgeEmbeddings(model_name = "BAAI/bge-base-en-v1.5" , model_kwargs = {'token': hugging_face})

pc= Pinecone(api_key=pine_cone)
index = pc.Index('iml' , host=os.getenv('host_bg'))
vector = PineconeVectorStore(index=index , embedding=embeddings , text_key="page_content")
retriever = vector.as_retriever()

def iml_tool():
    "Tool for acting as an ML professor that answers student questions in 8-mark format using book-based content."
    retriever_tool = create_retriever_tool(
        retriever,
        "ML Professor",
        "Behave like a strict ML professor. Whenever a student asks a question, answer strictly based on textbook content. Format answers as 8-mark responses with clear bullet points or numbered lists. Use this tool only for academic questions related to engineering, computer science, or technical subjects."
    )
    return retriever_tool