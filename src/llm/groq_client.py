from langchain_groq import ChatGroq

from src.config.settings import settings

def get_groq_llm():
    return ChatGroq(
        model=settings.MODEL_NAME,
        temperature=settings.TEMPERATURE
    )