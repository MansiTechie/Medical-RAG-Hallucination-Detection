from pydantic import BaseModel
from typing import List, Optional


class AskRequest(BaseModel):
    query: str


class SourceEvidence(BaseModel):
    chunk_id: str
    page: int
    text: str


class ClaimEvidence(BaseModel):
    chunk_id: str
    page: int
    text: str
    similarity: float
    entailment: float
    contradiction: float
    neutral: float
    evidence_score: float


class ClaimResult(BaseModel):
    claim_number: int
    claim: str
    hypothesis: str
    supported: bool
    evidence: Optional[ClaimEvidence] = None


class ClaimVerificationResult(BaseModel):
    claims: List[ClaimResult]
    supported_claims: int
    total_claims: int
    consistency_score: float


class ConfidenceResult(BaseModel):
    semantic_similarity: float
    nli_entailment: float
    retrieval_quality: float
    claim_consistency: float
    confidence_score: float
    confidence_level: str  # HIGH / MEDIUM / LOW


class HallucinationDecision(BaseModel):
    decision: str  # SUPPORTED / CONTRADICTED / POTENTIAL HALLUCINATION
    claim_consistency: float
    confidence_score: float
    strong_contradictions: int


class SelfCorrectionResult(BaseModel):
    correction_needed: bool
    correction_applied: bool
    original_answer: str
    corrected_answer: Optional[str] = None


class AskResponse(BaseModel):
    answer: str
    sources: List[SourceEvidence]
    claim_verification: Optional[ClaimVerificationResult] = None
    confidence: Optional[ConfidenceResult] = None
    hallucination_decision: Optional[HallucinationDecision] = None
    self_correction: Optional[SelfCorrectionResult] = None
