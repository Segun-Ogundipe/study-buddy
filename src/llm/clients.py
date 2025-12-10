import os

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

def get_groq_llm(user_controls):
    return ChatGroq(
        model=user_controls["model"],
        temperature=user_controls["temperature"],
        api_key=user_controls["api_key"] or os.getenv("GROQ_API_KEY")
    )
    
def get_openai_llm(user_controls):
    return ChatOpenAI(
        model=user_controls["model"],
        temperature=user_controls["temperature"],
        api_key=user_controls["api_key"] or os.getenv("OPENAI_API_KEY")
    )
