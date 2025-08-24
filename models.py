# models.py
import os
from dotenv import load_dotenv
load_dotenv()

HF_EMBED_MODEL = os.getenv("HF_EMBED_MODEL", "sentence-transformers/all-mpnet-base-v2")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

def get_embeddings():
    """Hugging Face embeddings"""
    return HuggingFaceEmbeddings(model_name=HF_EMBED_MODEL)

def get_gemini_chat():
    """Gemini LLM"""
    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        temperature=0.2,
    )
