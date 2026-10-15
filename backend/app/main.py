"""
FastAPI application — Medical RAG + Hallucination Detection API.

Wires the complete Notebook 08 pipeline:
  User query → Retrieval → Generation → Verification →
  Confidence → Decision → Correction → Response
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import traceback

from app.config import settings
from app.schemas import (
    AskRequest,
    AskResponse,
    SourceEvidence,
    ClaimEvidence,
    ClaimResult,
    ClaimVerificationResult,
    ConfidenceResult,
    HallucinationDecision,
    SelfCorrectionResult,
)
from app.services.retrieval import retrieval_service
from app.services.llm import llm_service
from app.services.verification import verification_service
from app.services.correction import correction_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load all models at startup."""
    print("Starting up FastAPI. Loading models...")

    # Load embedding model + FAISS index
    retrieval_service.load_models_and_index()

    # Load NLI model
    verification_service.load_nli_model()

    # Initialize Gemini client
    llm_service.initialize()

    yield

    print("Shutting down...")


app = FastAPI(
    title="Medical RAG API",
    description="Medical RAG + Hallucination Detection Pipeline",
    lifespan=lifespan,
)

# ─── CORS (for future React frontend) ────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Health Check ─────────────────────────────────────────────────

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "models_loaded": {
            "embedding": retrieval_service.embedding_model is not None,
            "faiss_index": retrieval_service.index is not None,
            "nli": verification_service._loaded,
            "gemini": llm_service.client is not None,
        },
    }


# ─── Pipeline Endpoint ───────────────────────────────────────────

@app.post("/api/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    """
    Complete Notebook 08 pipeline:
    Query → Retrieve → Generate → Verify → Score → Decide → Correct → Respond
    """
    try:
        query = request.query
        print(f"\n{'='*70}")
        print(f"Query: {query}")

        # ── 1. RETRIEVAL ─────────────────────────────────────────
        print("[1/7] Retrieving evidence...")
        raw_results = retrieval_service.search(
            query, top_k=settings.RETRIEVAL_TOP_K
        )

        # Build context string (NB08 build_context style)
        context = ""
        sources = []
        for i, res in enumerate(raw_results, 1):
            context += (
                f"\n[Source: NIDDK Guiding Principles | "
                f"Page: {res['page']} | "
                f"Chunk: {res['chunk_id']}]\n"
                f"{res['text']}\n"
            )
            sources.append(SourceEvidence(
                chunk_id=res["chunk_id"],
                page=res["page"],
                text=res["text"],
            ))

        print(f"  Retrieved {len(raw_results)} chunks")

        # ── 2. GROUNDED GENERATION ───────────────────────────────
        print("[2/7] Generating grounded answer...")
        answer = llm_service.generate_grounded_answer(query, context)
        print(f"  Answer length: {len(answer)}")

        # ── 3. CLAIM VERIFICATION ────────────────────────────────
        print("[3/7] Verifying claims...")
        claim_verification_raw = verification_service.verify_claims(
            answer=answer,
            chunks=retrieval_service.metadata,
            embeddings=retrieval_service.embeddings,
            index=retrieval_service.index,
            embedding_model=retrieval_service.embedding_model,
            top_n=settings.VERIFICATION_TOP_N,
            batch_size=settings.NLI_BATCH_SIZE,
        )
        print(
            f"  Claims: {claim_verification_raw['supported_claims']}"
            f"/{claim_verification_raw['total_claims']} supported"
        )

        # ── 4. CONFIDENCE SCORING ────────────────────────────────
        print("[4/7] Calculating confidence...")
        confidence_raw = verification_service.calculate_confidence(
            answer=answer,
            question=query,
            retrieved_docs=raw_results,
            claim_verification=claim_verification_raw,
            embedding_model=retrieval_service.embedding_model,
        )
        print(
            f"  Confidence: {confidence_raw['confidence_score']:.4f} "
            f"({confidence_raw['confidence_level']})"
        )

        # ── 5. HALLUCINATION DECISION ────────────────────────────
        print("[5/7] Determining hallucination status...")
        decision_raw = verification_service.determine_decision(
            claim_verification=claim_verification_raw,
            confidence_result=confidence_raw,
        )
        print(f"  Decision: {decision_raw['decision']}")

        # ── 6. SELF-CORRECTION ───────────────────────────────────
        print("[6/7] Self-correction check...")
        correction_raw = correction_service.perform_correction(
            question=query,
            answer=answer,
            final_decision=decision_raw,
            claim_verification=claim_verification_raw,
            llm_service=llm_service,
        )
        print(
            f"  Needed: {correction_raw['correction_needed']} | "
            f"Applied: {correction_raw['correction_applied']}"
        )

        final_answer = answer
        final_claim_verification = claim_verification_raw
        final_confidence = confidence_raw
        final_decision = decision_raw

        # ── 6.5 RE-VERIFICATION ──────────────────────────────────
        if correction_raw["correction_applied"] and correction_raw.get("corrected_answer"):
            print("[6.5/7] Re-verifying corrected answer...")
            final_answer = correction_raw["corrected_answer"]

            final_claim_verification = verification_service.verify_claims(
                answer=final_answer,
                chunks=retrieval_service.metadata,
                embeddings=retrieval_service.embeddings,
                index=retrieval_service.index,
                embedding_model=retrieval_service.embedding_model,
                top_n=settings.VERIFICATION_TOP_N,
                batch_size=settings.NLI_BATCH_SIZE,
            )

            final_confidence = verification_service.calculate_confidence(
                answer=final_answer,
                question=query,
                retrieved_docs=raw_results,
                claim_verification=final_claim_verification,
                embedding_model=retrieval_service.embedding_model,
            )

            final_decision = verification_service.determine_decision(
                claim_verification=final_claim_verification,
                confidence_result=final_confidence,
            )

        # ── 7. BUILD RESPONSE ────────────────────────────────────
        print("[7/7] Building response...")

        # Convert claim verification to schema objects
        claim_results = []
        for cr in final_claim_verification["claims"]:
            ev = cr["evidence"]
            claim_evidence = None
            if ev:
                claim_evidence = ClaimEvidence(
                    chunk_id=ev["chunk_id"],
                    page=ev["page"],
                    text=ev["text"],
                    similarity=ev["similarity"],
                    entailment=ev["entailment"],
                    contradiction=ev["contradiction"],
                    neutral=ev["neutral"],
                    evidence_score=ev["evidence_score"],
                )
            claim_results.append(ClaimResult(
                claim_number=cr["claim_number"],
                claim=cr["claim"],
                hypothesis=cr["hypothesis"],
                supported=cr["supported"],
                evidence=claim_evidence,
            ))

        response = AskResponse(
            answer=final_answer,
            sources=sources,
            claim_verification=ClaimVerificationResult(
                claims=claim_results,
                supported_claims=final_claim_verification["supported_claims"],
                total_claims=final_claim_verification["total_claims"],
                consistency_score=final_claim_verification["consistency_score"],
            ),
            confidence=ConfidenceResult(**final_confidence),
            hallucination_decision=HallucinationDecision(**final_decision),
            self_correction=SelfCorrectionResult(
                correction_needed=correction_raw["correction_needed"],
                correction_applied=correction_raw["correction_applied"],
                original_answer=correction_raw["original_answer"],
                corrected_answer=correction_raw.get("corrected_answer"),
            ),
        )

        print(f"{'='*70}")
        print("PIPELINE COMPLETE")
        print(f"{'='*70}\n")

        return response

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
