"""
Central configuration for Medical AI Reviewer.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------

load_dotenv()

# -------------------------------------------------
# API Keys
# -------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

LANGCHAIN_TRACING_V2 = os.getenv(
    "LANGCHAIN_TRACING_V2"
)

# -------------------------------------------------
# Project Paths
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = BASE_DIR.parent

# -------------------------------------------------
# Data
# -------------------------------------------------

DATA_FOLDER = PROJECT_ROOT / "data"

MEDICAL_RECORDS_FOLDER = (
    DATA_FOLDER / "medical_records"
)

GUIDELINES_FOLDER = (
    DATA_FOLDER / "jobaids"
)

GROUND_TRUTH_FOLDER = (
    DATA_FOLDER / "gt"
)

# -------------------------------------------------
# Vector DB
# -------------------------------------------------


import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"

MEDICAL_RECORDS_FOLDER = DATA_DIR / "medical_records"

GUIDELINES_FOLDER = DATA_DIR / "jobaids"

GROUND_TRUTH_FOLDER = DATA_DIR / "gt"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

PINECONE_INDEX = os.getenv("PINECONE_INDEX")
