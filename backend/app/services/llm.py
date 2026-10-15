"""
LLM service — Gemini integration with retry logic.

Provides:
  - Grounded medical answer generation (NB08 prompt)
  - Corrected answer generation for self-correction
  - Retry/error handling
"""

import time
from google import genai
from app.config import settings


class LLMService:
    def __init__(self):
        self.client = None

    def initialize(self):
        """Initialize the Gemini client using the API key from config."""
        if settings.GEMINI_API_KEY:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            print(f"Gemini client initialized (model: {settings.GEMINI_MODEL_NAME})")
        else:
            print("WARNING: GEMINI_API_KEY not found in config. LLM will fail.")

    def _generate_with_retry(self, prompt: str) -> str:
        """
        Call Gemini with retry logic.
        Retries are intended for transient failures (e.g., 503, 429).
        Ported from Notebook 08 generate_grounded_answer().
        """
        if not self.client:
            raise RuntimeError("LLM client not initialized. Check API key.")

        last_error = None

        for attempt in range(1, settings.LLM_MAX_RETRIES + 1):
            try:
                response = self.client.models.generate_content(
                    model=settings.GEMINI_MODEL_NAME,
                    contents=prompt
                )

                if response and response.text:
                    return response.text.strip()

                last_error = "Gemini returned an empty response."

            except Exception as e:
                last_error = str(e)
                print(
                    f"Attempt {attempt}/{settings.LLM_MAX_RETRIES} "
                    f"failed: {last_error}. (Note: retries are for transient issues like 503/429)"
                )

            if attempt < settings.LLM_MAX_RETRIES:
                time.sleep(settings.LLM_RETRY_DELAY)

        raise RuntimeError(
            f"Gemini generation failed after {settings.LLM_MAX_RETRIES} "
            f"attempts. Last error: {last_error}"
        )

    def generate_grounded_answer(self, query: str, context: str) -> str:
        """
        Generate a grounded medical answer.
        Prompt ported from Notebook 08 Cell 9.
        """
        prompt = f"""
You are a medical information assistant.

Answer the user's question using ONLY the provided medical context.

Rules:
1. Do not use outside knowledge.
2. Do not invent or assume facts.
3. If the context is insufficient, say that clearly.
4. Keep the answer evidence-based.
5. Preserve important medical qualifiers.
6. Do not provide diagnosis or personalized medical advice.
7. Mention the relevant source page for factual claims.

MEDICAL CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""
        return self._generate_with_retry(prompt)

    def generate_corrected_answer(self, correction_prompt: str) -> str:
        """
        Generate a corrected answer using the correction prompt
        built by the CorrectionService.
        """
        return self._generate_with_retry(correction_prompt)


llm_service = LLMService()
