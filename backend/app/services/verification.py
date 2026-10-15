"""
Verification service — ported from Notebook 08.

Provides:
  - NLI model loading (cross-encoder/nli-deberta-v3-base)
  - Claim extraction from LLM answers
  - Claim-to-hypothesis mapping
  - Semantic similarity calculation
  - NLI scoring (single-pair and batched)
  - Claim-level evidence verification
  - Confidence scoring (NB06 formula)
  - Hallucination decision
"""

import re
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.config import settings


class VerificationService:
    def __init__(self):
        self.nli_tokenizer = None
        self.nli_model = None
        self._loaded = False

    # ─── Model Loading ───────────────────────────────────────────

    def load_nli_model(self):
        """Load the NLI model and tokenizer at startup."""
        model_name = settings.NLI_MODEL_NAME
        print(f"Loading NLI model: {model_name}")

        self.nli_tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.nli_model = AutoModelForSequenceClassification.from_pretrained(
            model_name
        )
        self.nli_model.eval()
        self._loaded = True

        print(f"NLI model loaded. Labels: {self.nli_model.config.num_labels}")

    def _ensure_loaded(self):
        if not self._loaded:
            raise RuntimeError(
                "NLI model not loaded. Call load_nli_model() at startup."
            )

    # ─── NLI Scoring ─────────────────────────────────────────────

    def nli_score(self, premise: str, hypothesis: str) -> dict:
        """
        Single-pair NLI inference.
        Returns contradiction, entailment, neutral probabilities.
        Label order for cross-encoder/nli-deberta-v3-base:
          0 = contradiction, 1 = entailment, 2 = neutral
        """
        self._ensure_loaded()

        inputs = self.nli_tokenizer(
            premise, hypothesis,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        with torch.no_grad():
            outputs = self.nli_model(**inputs)

        probs = torch.softmax(outputs.logits, dim=1)[0].cpu().numpy()

        return {
            "contradiction": float(probs[0]),
            "entailment": float(probs[1]),
            "neutral": float(probs[2]),
        }

    def nli_score_batch(
        self,
        premises: list,
        hypotheses: list,
        batch_size: int = 16
    ) -> list:
        """
        Batched NLI inference — the missing function from Notebook 08.
        Processes premise-hypothesis pairs in batches for efficiency.
        """
        self._ensure_loaded()

        results = []

        for start in range(0, len(premises), batch_size):
            batch_premises = premises[start:start + batch_size]
            batch_hypotheses = hypotheses[start:start + batch_size]

            inputs = self.nli_tokenizer(
                batch_premises,
                batch_hypotheses,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )

            with torch.no_grad():
                outputs = self.nli_model(**inputs)

            probs = torch.softmax(outputs.logits, dim=1).cpu().numpy()

            for prob in probs:
                results.append({
                    "contradiction": float(prob[0]),
                    "entailment": float(prob[1]),
                    "neutral": float(prob[2]),
                })

        return results

    # ─── Semantic Similarity ─────────────────────────────────────

    @staticmethod
    def semantic_similarity(
        answer: str,
        documents: list,
        embedding_model
    ) -> float:
        """
        Max cosine similarity between answer and retrieved doc chunks.
        Matches Notebook 08 verify_answer().
        """
        if not answer or not documents:
            return 0.0

        answer_embedding = embedding_model.encode(
            [answer], normalize_embeddings=True
        )[0]

        doc_embeddings = embedding_model.encode(
            [doc["text"] for doc in documents],
            normalize_embeddings=True
        )

        similarities = np.dot(doc_embeddings, answer_embedding)
        return float(np.max(similarities))

    # ─── Claim Extraction ────────────────────────────────────────

    @staticmethod
    def extract_claims(answer: str) -> list:
        """
        Extract individual factual claims from a medical answer.
        Ported from Notebook 08 Cell 19 (final version).
        """
        if not answer or not answer.strip():
            return []

        text = answer.strip()

        # Remove page citations
        text = re.sub(r"\s*\[Page\s+\d+\]", "", text)

        # Remove markdown bold/italic
        text = re.sub(r"\*\*", "", text)
        text = re.sub(r"(?<!\*)\*(?!\*)", "", text)

        lines = text.splitlines()
        claims = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Remove bullets / numbering
            line = re.sub(r"^\s*[-•*]\s*", "", line)
            line = re.sub(r"^\s*\d+[.)]\s*", "", line)
            line = line.strip()
            if not line:
                continue

            lower = line.lower()

            # Skip headings
            headings = [
                "primary and demographic factors:",
                "medical history and associated conditions:",
                "emerging risk factors:",
                "other risk factors include:",
                "additional risk factors include:",
            ]
            if any(lower.startswith(h) for h in headings):
                continue

            # Skip umbrella introductions
            if lower.startswith(
                "based on the provided context, the risk factors"
            ):
                continue

            # Clean incomplete references
            if "[medications]" in lower:
                line = line.replace("[medications]", "medications")

            # Skip obvious incomplete fragments
            if lower.endswith("atypical"):
                continue

            claims.append(line)

        # Deduplicate
        unique_claims = []
        seen = set()

        for claim in claims:
            claim = re.sub(r"\s+", " ", claim).strip()
            normalized = claim.lower()
            if normalized not in seen:
                seen.add(normalized)
                unique_claims.append(claim)

        return unique_claims

    # ─── Claim-to-Hypothesis Mapping ─────────────────────────────

    @staticmethod
    def claim_to_hypothesis(claim: str) -> str:
        """
        Map medical claims to NLI-friendly hypothesis sentences.
        Preserves diabetes-specific mappings only for exact known dataset patterns.
        """
        claim = re.sub(r"\s+", " ", claim).strip()
        claim = re.sub(r"\[[^\]]*\]", "", claim).strip()

        lower = claim.lower()

        # Age
        if lower.startswith("age:") and "45" in lower:
            return "Increasing age is a risk factor for type 2 diabetes."

        # Obesity
        if lower.startswith("overweight") and "bmi" in lower:
            return (
                "Overweight or obesity is a risk factor for type 2 diabetes, "
                "with increased risk associated with BMI ≥25 kg/m² "
                "or ≥23 kg/m² for Asian Americans."
            )

        # Prediabetes
        if lower.startswith("prediabetes:") and ("a1c" in lower or "igt" in lower):
            return "Prediabetes is a risk factor for type 2 diabetes."

        # Family history
        if lower.startswith("family history:") and "diabetes" in lower:
            return (
                "Having a parent or sibling with diabetes "
                "is a risk factor for type 2 diabetes."
            )

        # High-risk populations
        if lower.startswith("high-risk") and "african american" in lower:
            return (
                "Being African American, Hispanic or Latino, "
                "American Indian, Alaska Native, Asian American, "
                "or Pacific Islander American is a risk factor "
                "for type 2 diabetes."
            )

        # Gestational diabetes
        if "gestational diabetes" in lower:
            return (
                "A history of gestational diabetes mellitus "
                "is a risk factor for type 2 diabetes."
            )

        # Physical inactivity
        if "physical inactivity" in lower and len(lower.split()) < 5:
            return "Physical inactivity is a risk factor for type 2 diabetes."

        # Hypertension
        if lower.startswith("hypertension") and "140/90" in lower:
            return "Hypertension is a risk factor for type 2 diabetes."

        # HDL
        if ("hdl-c" in lower or "high-density lipoprotein" in lower) and "35" in lower:
            return (
                "A high-density lipoprotein cholesterol level "
                "of 35 mg/dL or lower is a risk factor for type 2 diabetes."
            )

        # Triglycerides
        if "triglyceride" in lower and "250" in lower:
            return (
                "A fasting triglyceride level of 250 mg/dL or higher "
                "is a risk factor for type 2 diabetes."
            )

        # Insulin resistance
        if "acanthosis nigricans" in lower and "polycystic ovary" in lower:
            return (
                "Acanthosis nigricans, nonalcoholic steatohepatitis, "
                "polycystic ovary syndrome, and other conditions "
                "associated with insulin resistance are risk factors "
                "for type 2 diabetes."
            )

        # Cardiovascular disease
        if "atherosclerotic cardiovascular disease" in lower:
            return (
                "Atherosclerotic cardiovascular disease is a risk factor "
                "for type 2 diabetes."
            )

        # Depression
        if lower.startswith("depression") and len(lower.split()) < 5:
            return "Depression is a risk factor for type 2 diabetes."

        # Sleep apnea
        if "obstructive sleep apnea" in lower:
            return (
                "Obstructive sleep apnea is an emerging risk factor "
                "for type 2 diabetes."
            )

        # Sleep deprivation
        if "sleep deprivation" in lower and "6 hours" in lower:
            return (
                "Chronic sleep deprivation of less than 6 hours per day "
                "is an emerging risk factor for type 2 diabetes."
            )

        # Incomplete claim
        if "atypical medications" in lower:
            return claim

        return claim

    # ─── Claim Support Decision ──────────────────────────────────

    @staticmethod
    def is_claim_supported(evidence: dict) -> bool:
        """
        Determine if a claim is supported by evidence.
        Ported from Notebook 08 Cell 25.
        """
        if evidence is None:
            return False

        entailment = evidence["entailment"]
        contradiction = evidence["contradiction"]
        similarity = evidence["similarity"]
        evidence_score = evidence["evidence_score"]

        # Strong direct evidence
        if (
            entailment >= 0.80
            and contradiction < 0.20
            and evidence_score >= 0.65
        ):
            return True

        # Good combined semantic + NLI evidence
        if (
            entailment >= 0.65
            and similarity >= 0.45
            and contradiction < 0.10
            and evidence_score >= 0.55
        ):
            return True

        return False

    # ─── Claim-Level Verification (batched) ──────────────────────

    def verify_claims(
        self,
        answer: str,
        chunks: list,
        embeddings: np.ndarray,
        index,
        embedding_model,
        top_n: int = 10,
        batch_size: int = 16
    ) -> dict:
        """
        Batched claim-level verification.
        Ported from Notebook 08 verify_claims_fast().
        """
        self._ensure_loaded()

        # 1. Extract claims
        all_claims = self.extract_claims(answer)
        claims = [
            c for c in all_claims
            if "context cuts off" not in c.lower()
            and not c.lower().endswith("atypical")
        ]

        if not claims:
            return {
                "claims": [],
                "supported_claims": 0,
                "total_claims": 0,
                "consistency_score": 0.0,
            }

        # 2. Map to hypotheses
        hypotheses = [self.claim_to_hypothesis(c) for c in claims]

        # 3. Encode hypotheses
        hypothesis_embeddings = embedding_model.encode(
            hypotheses, normalize_embeddings=True
        )
        raw_query_embeddings = embedding_model.encode(
            hypotheses
        ).astype("float32")

        # 4. Retrieve evidence candidates
        search_k = min(top_n, len(chunks))
        distances, indices_arr = index.search(raw_query_embeddings, search_k)

        # 5. Normalize stored embeddings
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True) + 1e-12
        normalized_embeddings = embeddings / norms

        # 6. Build NLI pairs
        premises = []
        nli_hypotheses = []
        metadata = []

        for claim_idx in range(len(claims)):
            for rank, chunk_idx in enumerate(indices_arr[claim_idx]):
                chunk_idx = int(chunk_idx)
                if chunk_idx < 0 or chunk_idx >= len(chunks):
                    continue

                similarity = float(np.dot(
                    normalized_embeddings[chunk_idx],
                    hypothesis_embeddings[claim_idx]
                ))

                premises.append(chunks[chunk_idx]["text"])
                nli_hypotheses.append(hypotheses[claim_idx])
                metadata.append({
                    "claim_idx": claim_idx,
                    "rank": rank + 1,
                    "chunk": chunks[chunk_idx],
                    "similarity": similarity,
                })

        # 7. Batched NLI
        nli_results = self.nli_score_batch(
            premises, nli_hypotheses, batch_size=batch_size
        )

        # 8. Select strongest evidence per claim
        best_evidence = [None] * len(claims)

        for meta, nli in zip(metadata, nli_results):
            # NLI-first scoring (NB08 Cell 26)
            evidence_score = (
                0.70 * nli["entailment"]
                + 0.30 * meta["similarity"]
                - 0.30 * nli["contradiction"]
            )

            evidence = {
                "chunk_id": meta["chunk"]["chunk_id"],
                "page": meta["chunk"]["page"],
                "text": meta["chunk"]["text"],
                "similarity": meta["similarity"],
                "entailment": nli["entailment"],
                "contradiction": nli["contradiction"],
                "neutral": nli["neutral"],
                "evidence_score": evidence_score,
            }

            ci = meta["claim_idx"]
            if (
                best_evidence[ci] is None
                or evidence_score > best_evidence[ci]["evidence_score"]
            ):
                best_evidence[ci] = evidence

        # 9. Evaluate claim support
        results = []
        supported_count = 0

        for i, (claim, evidence) in enumerate(
            zip(claims, best_evidence), start=1
        ):
            supported = self.is_claim_supported(evidence)
            if supported:
                supported_count += 1

            results.append({
                "claim_number": i,
                "claim": claim,
                "hypothesis": self.claim_to_hypothesis(claim),
                "supported": supported,
                "evidence": evidence,
            })

        # 10. Consistency
        consistency_score = supported_count / len(claims) if claims else 0.0

        return {
            "claims": results,
            "supported_claims": supported_count,
            "total_claims": len(claims),
            "consistency_score": consistency_score,
        }

    # ─── Confidence Scoring ──────────────────────────────────────

    @staticmethod
    def calculate_confidence(
        answer: str,
        question: str,
        retrieved_docs: list,
        claim_verification: dict,
        embedding_model
    ) -> dict:
        """
        Final confidence scoring.
        Preserves Notebook 06 formula:
          0.30 × answer semantic similarity
          0.30 × NLI entailment
          0.20 × retrieval quality
          0.20 × claim consistency
        """

        # 1. Answer semantic similarity
        if not answer or not retrieved_docs:
            sem_sim = 0.0
        else:
            answer_emb = embedding_model.encode(
                [answer], normalize_embeddings=True
            )[0]
            doc_embs = embedding_model.encode(
                [d["text"] for d in retrieved_docs],
                normalize_embeddings=True
            )
            sims = np.dot(doc_embs, answer_emb)
            sem_sim = float(np.clip(np.max(sims), 0.0, 1.0))

        # 2. Claim-level NLI entailment
        valid = [
            r for r in claim_verification["claims"]
            if r["supported"] is not None
        ]
        if valid:
            scores = [r["evidence"]["entailment"] for r in valid]
            nli_ent = float(np.clip(np.mean(scores), 0.0, 1.0))
        else:
            nli_ent = 0.0

        # 3. Retrieval quality
        if retrieved_docs:
            q_emb = embedding_model.encode(
                [question], normalize_embeddings=True
            )[0]
            ret_embs = embedding_model.encode(
                [d["text"] for d in retrieved_docs],
                normalize_embeddings=True
            )
            ret_sims = np.dot(ret_embs, q_emb)
            top_k = min(5, len(ret_sims))
            top_scores = np.sort(ret_sims)[-top_k:]
            ret_quality = float(np.clip(np.mean(top_scores), 0.0, 1.0))
        else:
            ret_quality = 0.0

        # 4. Claim consistency
        consistency = float(claim_verification["consistency_score"])

        # 5. Weighted confidence
        confidence = (
            0.30 * sem_sim
            + 0.30 * nli_ent
            + 0.20 * ret_quality
            + 0.20 * consistency
        )
        confidence = float(np.clip(confidence, 0.0, 1.0))

        # 6. Level
        if confidence >= 0.80:
            level = "HIGH"
        elif confidence >= 0.60:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "semantic_similarity": sem_sim,
            "nli_entailment": nli_ent,
            "retrieval_quality": ret_quality,
            "claim_consistency": consistency,
            "confidence_score": confidence,
            "confidence_level": level,
        }

    # ─── Hallucination Decision ──────────────────────────────────

    @staticmethod
    def determine_decision(
        claim_verification: dict,
        confidence_result: dict
    ) -> dict:
        """
        Final hallucination status.
        Ported from Notebook 08 Cell 32.
        """
        consistency = claim_verification["consistency_score"]
        confidence = confidence_result["confidence_score"]

        # Count strong contradictions
        strong_contradictions = 0
        for result in claim_verification["claims"]:
            ev = result["evidence"]
            if ev and ev["contradiction"] >= 0.50:
                strong_contradictions += 1

        # Decision
        if strong_contradictions > 0:
            decision = "CONTRADICTED"
        elif consistency < 0.60 or confidence < 0.60:
            decision = "POTENTIAL HALLUCINATION"
        else:
            decision = "SUPPORTED"

        return {
            "decision": decision,
            "claim_consistency": consistency,
            "confidence_score": confidence,
            "strong_contradictions": strong_contradictions,
        }


# Module-level singleton
verification_service = VerificationService()
