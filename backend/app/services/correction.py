"""
Self-correction service — ported from Notebook 07/08.

Provides:
  - Decision on whether self-correction is needed
  - Correction prompt construction from unsupported claims
  - Orchestration of the correction flow
"""


class CorrectionService:

    # ─── Correction Trigger ──────────────────────────────────────

    @staticmethod
    def should_self_correct(final_decision: dict) -> bool:
        """
        Decide whether the generated answer needs self-correction.
        Ported from Notebook 08 Cell 33.
        """
        decision = final_decision["decision"]
        confidence = final_decision["confidence_score"]

        if decision in {"POTENTIAL HALLUCINATION", "CONTRADICTED"}:
            return True

        if confidence < 0.60:
            return True

        return False

    # ─── Correction Prompt ───────────────────────────────────────

    @staticmethod
    def build_correction_prompt(
        question: str,
        answer: str,
        claim_verification: dict
    ) -> str:
        """
        Build a grounded correction prompt using only the evidence
        associated with unsupported claims.
        Ported from Notebook 08 Cell 33.
        """
        unsupported_claims = []

        for result in claim_verification["claims"]:
            if not result["supported"]:
                evidence = result["evidence"]
                if evidence:
                    unsupported_claims.append({
                        "claim": result["claim"],
                        "evidence": evidence["text"],
                        "page": evidence["page"],
                    })

        evidence_text = ""
        for item in unsupported_claims:
            evidence_text += (
                f"\nClaim: {item['claim']}\n"
                f"Evidence (Page {item['page']}): {item['evidence']}\n"
            )

        prompt = f"""
You are correcting a medical RAG answer.

USER QUESTION:
{question}

ORIGINAL ANSWER:
{answer}

The following claims were not sufficiently supported
during evidence verification:

{evidence_text}

Instructions:

1. Use ONLY the provided evidence.
2. Remove unsupported claims.
3. Do not invent missing information.
4. Preserve claims that are supported.
5. If evidence is insufficient, explicitly say so.
6. Keep the corrected answer concise.
7. Include source page references where appropriate.
8. Do not provide personalized medical advice.

Return ONLY the corrected answer.
"""
        return prompt

    # ─── Correction Orchestration ────────────────────────────────

    def perform_correction(
        self,
        question: str,
        answer: str,
        final_decision: dict,
        claim_verification: dict,
        llm_service
    ) -> dict:
        """
        Perform self-correction if required.
        If correction is needed AND the LLM is available, generate
        a corrected answer. Otherwise return the original.
        """
        correction_needed = self.should_self_correct(final_decision)

        if not correction_needed:
            return {
                "correction_needed": False,
                "correction_applied": False,
                "original_answer": answer,
                "corrected_answer": answer,
            }

        # Build correction prompt
        correction_prompt = self.build_correction_prompt(
            question, answer, claim_verification
        )

        # Attempt corrected generation
        try:
            corrected_answer = llm_service.generate_corrected_answer(
                correction_prompt
            )
            return {
                "correction_needed": True,
                "correction_applied": True,
                "original_answer": answer,
                "corrected_answer": corrected_answer,
            }
        except Exception as e:
            print(f"Self-correction LLM call failed: {e}")
            return {
                "correction_needed": True,
                "correction_applied": False,
                "original_answer": answer,
                "corrected_answer": answer,
            }


# Module-level singleton
correction_service = CorrectionService()
