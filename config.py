import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_VERSION = os.getenv("APP_VERSION", "0.0.1")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")

    PUBMED_EMAIL = os.getenv("PUBMED_EMAIL")
    PUBMED_API_KEY = os.getenv("PUBMED_API_KEY")
    PUBMED_MAX_RESULTS = os.getenv("PUBMED_MAX_RESULTS", 50)
    PUBMED_RETMAX = os.getenv("PUBMED_RETMAX", 100)

    CHUNK_SIZE = os.getenv("CHUNK_SIZE", 1000)
    CHUNK_OVERLAP = os.getenv("CHUNK_OVERLAP", 200)
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")