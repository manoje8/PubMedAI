import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")

    PUBMED_EMAIL = os.getenv("PUBMED_EMAIL")
    PUBMED_API_KEY = os.getenv("PUBMED_API_KEY")