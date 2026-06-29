from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()


# ------------------------------
# OpenAI
# ------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ------------------------------
# LangSmith
# ------------------------------

LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

LANGCHAIN_PROJECT = os.getenv(
    "LANGCHAIN_PROJECT"
)

LANGCHAIN_TRACING_V2 = os.getenv(
    "LANGCHAIN_TRACING_V2"
)


# ------------------------------
# Project Paths
# ------------------------------

BASE_DIR = os.path.dirname(__file__)

PDF_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "pdfs"
)

FAISS_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "faiss_index"
)