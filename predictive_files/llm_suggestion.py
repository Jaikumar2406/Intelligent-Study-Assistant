from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
groq = os.getenv('GROQ')

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq, temperature=0.7)

def llm_suggestion(subject, unit, topic):
    prompt = (
        f"In the subject '{subject}', Unit {unit}, how important is the topic '{topic}' for university exams?\n\n"
        "Give the answer in this format:\n"
        "- Percentage importance (0 to 100%)\n"
        "- Bullet points: Why is it important?\n"
        "- A short summary (1–2 lines) explaining the topic's importance."
    )
    response = llm.invoke(prompt)
    return response.content
