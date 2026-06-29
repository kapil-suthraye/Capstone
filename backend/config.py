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


# ==========================================================
# Project Paths
# ==========================================================

import os

BASE_DIR = os.path.dirname(__file__)

# Project Root
PROJECT_ROOT = os.path.abspath(
    os.path.join(BASE_DIR, "..")
)

# Shared Data Folder
DATA_FOLDER = os.path.join(
    PROJECT_ROOT,
    "data"
)

# Medical Records
MEDICAL_RECORDS_FOLDER = os.path.join(
    DATA_FOLDER,
    "medical_records"
)

# Nurse Guidelines
GUIDELINES_FOLDER = os.path.join(
    DATA_FOLDER,
    "jobaids"
)

# Ground Truth
GROUND_TRUTH_FOLDER = os.path.join(
    DATA_FOLDER,
    "gt"
)

# Vector DB
VECTOR_DB_FOLDER = os.path.join(
    PROJECT_ROOT,
    "vector_db"
)

MEDICAL_VECTOR_DB = os.path.join(
    VECTOR_DB_FOLDER,
    "medical_index"
)

GUIDELINE_VECTOR_DB = os.path.join(
    VECTOR_DB_FOLDER,
    "guideline_index"
)

CACHE_FOLDER = os.path.join(
    VECTOR_DB_FOLDER,
    "cache"
)

# Create folders if they don't exist
os.makedirs(MEDICAL_VECTOR_DB, exist_ok=True)
os.makedirs(GUIDELINE_VECTOR_DB, exist_ok=True)
os.makedirs(CACHE_FOLDER, exist_ok=True)