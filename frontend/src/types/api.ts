export interface Source {
  chunk_id: string;
  page: number;
  text: string;
}

export interface ClaimEvidence {
  chunk_id: string;
  page: number;
  text: string;
  similarity: number;
  entailment: number;
  contradiction: number;
  neutral: number;
  evidence_score: number;
}

export interface Claim {
  claim_number: number;
  claim: string;
  hypothesis: string;
  supported: boolean;
  evidence: ClaimEvidence | null;
}

export interface ClaimVerification {
  claims: Claim[];
  supported_claims: number;
  total_claims: number;
  consistency_score: number;
}

export interface Confidence {
  semantic_similarity: number;
  nli_entailment: number;
  retrieval_quality: number;
  claim_consistency: number;
  confidence_score: number;
  confidence_level: 'HIGH' | 'MEDIUM' | 'LOW';
}

export interface HallucinationDecision {
  decision: 'SUPPORTED' | 'POTENTIAL HALLUCINATION' | 'CONTRADICTED';
  claim_consistency: number;
  confidence_score: number;
  strong_contradictions: number;
}

export interface SelfCorrection {
  correction_needed: boolean;
  correction_applied: boolean;
  original_answer: string;
  corrected_answer?: string;
}

export interface AskResponse {
  answer: string;
  sources: Source[];
  claim_verification: ClaimVerification;
  confidence: Confidence;
  hallucination_decision: HallucinationDecision;
  self_correction: SelfCorrection;
}
