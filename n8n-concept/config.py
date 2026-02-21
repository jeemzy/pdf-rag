"""
Shared configuration for the n8n pipeline replacement scripts.

Replace PLACEHOLDER values with your actual credentials before running.
"""

import os


# --- OpenAI ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "PLACEHOLDER_KEY")
LLM_MODEL = "gpt-4.1-mini"

# --- Qdrant ---
QDRANT_HOST = "localhost"  # e.g. "localhost" or "qdrant.example.com"
QDRANT_PORT = 6333  # default Qdrant REST port
QDRANT_API_KEY = "f305ri8jk32[d0fokvm54p9u8ujf43k"
QDRANT_COLLECTION = "dp-n8n-rag_collection"

# --- Question Generation Output ---
OUTPUT_FILE = "questions_output.txt"

# --- Semantic Chunker Settings ---
CHUNK_BREAKPOINT_THRESHOLD_TYPE = "percentile"  # approximates interquartile
CHUNK_MIN_SIZE = 100  # minimum chunk size in characters
CHUNK_MAX_SIZE = 2500  # maximum chunk size in characters

# --- LLM System Prompt (Question Generation) ---
QUESTION_SYSTEM_PROMPT = (
    "You are a chatbot that generates exactly three questions based on the given text. "
    "Each question must be no longer than 15 words. "
    "Each question must start on a new line. "
    "There should not be any empty lines. "
    "Do not include numbering, bullet points, or any additional text. "
    "Output only the three questions."
)
