import os
from pydantic_settings import BaseSettings

# Resolve paths relative to the project root (two levels up from this file)
_PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)


class Settings(BaseSettings):
    # --- Secrets (loaded from .env) ---
    GEMINI_API_KEY: str = ""

    # --- Paths ---
    VECTOR_DB_PATH: str = os.path.join(_PROJECT_ROOT, "vector_db")
    DATASET_PATH: str = os.path.join(_PROJECT_ROOT, "dataset", "raw")
    PDF_FILENAME: str = "niddk_guiding_principles_diabetes.pdf"

    # --- Embedding ---
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

    # --- NLI ---
    NLI_MODEL_NAME: str = "cross-encoder/nli-deberta-v3-base"

    # --- LLM ---
    GEMINI_MODEL_NAME: str = "gemini-3.8-flash"
    LLM_MAX_RETRIES: int = 3
    LLM_RETRY_DELAY: float = 4.0

    # --- Pipeline defaults ---
    RETRIEVAL_TOP_K: int = 10
    VERIFICATION_TOP_N: int = 10
    NLI_BATCH_SIZE: int = 16

    class Config:
        env_file = os.path.join(_PROJECT_ROOT, "backend", ".env")


settings = Settings()
