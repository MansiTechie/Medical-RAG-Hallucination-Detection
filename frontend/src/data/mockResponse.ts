import type { AskResponse } from '../types/api';

export const mockResponse: AskResponse = {
  answer: "Risk of type 2 diabetes increases with age and is strongly associated with overweight or obesity. Additional risk factors include prediabetes, family history of diabetes, physical inactivity, hypertension, history of gestational diabetes, and other conditions associated with insulin resistance.",
  sources: [
    {
      chunk_id: "chunk-10",
      page: 5,
      text: "Prediabetes is a condition where blood sugar levels are higher than normal, but not high enough yet to be diagnosed as type 2 diabetes. It is a major risk factor for developing type 2 diabetes."
    },
    {
      chunk_id: "chunk-22",
      page: 9,
      text: "Guiding Principles for the Care of People With or at Risk for Diabetes. Risk of type 2 diabetes increases with age and is strongly associated with overweight or obesity. Additional risk factors include prediabetes, family history of diabetes, physical inactivity, hypertension, history of gestational diabetes, and other conditions associated with insulin resistance."
    },
    {
      chunk_id: "chunk-35",
      page: 15,
      text: "Physical inactivity and hypertension are critical factors to monitor in populations at risk for type 2 diabetes."
    }
  ],
  claim_verification: {
    claims: [
      {
        claim_number: 1,
        claim: "Overweight or obesity is a risk factor for type 2 diabetes",
        hypothesis: "Overweight or obesity is a risk factor for type 2 diabetes.",
        supported: true,
        evidence: {
          chunk_id: "chunk-22",
          page: 9,
          text: "Risk of type 2 diabetes increases with age and is strongly associated with overweight or obesity.",
          similarity: 0.85,
          entailment: 0.91,
          contradiction: 0.02,
          neutral: 0.07,
          evidence_score: 0.88
        }
      },
      {
        claim_number: 2,
        claim: "Prediabetes is a risk factor for type 2 diabetes",
        hypothesis: "Prediabetes is a risk factor for type 2 diabetes.",
        supported: true,
        evidence: {
          chunk_id: "chunk-10",
          page: 5,
          text: "It is a major risk factor for developing type 2 diabetes.",
          similarity: 0.82,
          entailment: 0.89,
          contradiction: 0.01,
          neutral: 0.10,
          evidence_score: 0.85
        }
      },
      {
        claim_number: 3,
        claim: "Physical inactivity is a risk factor for type 2 diabetes",
        hypothesis: "Physical inactivity is a risk factor for type 2 diabetes.",
        supported: true,
        evidence: {
          chunk_id: "chunk-35",
          page: 15,
          text: "Physical inactivity and hypertension are critical factors to monitor in populations at risk for type 2 diabetes.",
          similarity: 0.78,
          entailment: 0.85,
          contradiction: 0.05,
          neutral: 0.10,
          evidence_score: 0.81
        }
      },
      {
        claim_number: 4,
        claim: "History of gestational diabetes is a risk factor",
        hypothesis: "History of gestational diabetes is a risk factor for type 2 diabetes.",
        supported: true,
        evidence: {
          chunk_id: "chunk-22",
          page: 9,
          text: "Additional risk factors include prediabetes, family history of diabetes, physical inactivity, hypertension, history of gestational diabetes...",
          similarity: 0.81,
          entailment: 0.87,
          contradiction: 0.03,
          neutral: 0.10,
          evidence_score: 0.84
        }
      }
    ],
    supported_claims: 4,
    total_claims: 4,
    consistency_score: 1.0
  },
  confidence: {
    semantic_similarity: 0.79,
    nli_entailment: 0.88,
    retrieval_quality: 0.64,
    claim_consistency: 1.0,
    confidence_score: 0.827,
    confidence_level: "HIGH"
  },
  hallucination_decision: {
    decision: "SUPPORTED",
    claim_consistency: 1.0,
    confidence_score: 0.827,
    strong_contradictions: 0
  },
  self_correction: {
    correction_needed: false,
    correction_applied: false,
    original_answer: ""
  }
};
