import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import type { Confidence } from '../types/api';

interface VerificationDetailsProps {
  confidence: Confidence;
}

export const VerificationDetails: React.FC<VerificationDetailsProps> = ({ confidence }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="verification-details card">
      <button className="details-header" onClick={() => setExpanded(!expanded)}>
        <h3 className="section-title">Verification details</h3>
        {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
      </button>

      {expanded && (
        <div className="details-content">
          <div className="metric-row">
            <div className="metric-info">
              <span className="metric-name">Semantic similarity</span>
              <span className="metric-desc">How closely claims match retrieved text</span>
            </div>
            <span className="metric-value">{confidence.semantic_similarity.toFixed(2)}</span>
          </div>
          <div className="metric-row">
            <div className="metric-info">
              <span className="metric-name">NLI entailment</span>
              <span className="metric-desc">Logical support from the evidence</span>
            </div>
            <span className="metric-value">{confidence.nli_entailment.toFixed(2)}</span>
          </div>
          <div className="metric-row">
            <div className="metric-info">
              <span className="metric-name">Retrieval quality</span>
              <span className="metric-desc">Relevance of retrieved chunks</span>
            </div>
            <span className="metric-value">{confidence.retrieval_quality.toFixed(2)}</span>
          </div>
          <div className="metric-row">
            <div className="metric-info">
              <span className="metric-name">Claim consistency</span>
              <span className="metric-desc">Proportion of supported claims</span>
            </div>
            <span className="metric-value">{confidence.claim_consistency.toFixed(2)}</span>
          </div>
          <div className="metric-row summary-metric">
            <div className="metric-info">
              <span className="metric-name">Confidence score</span>
            </div>
            <span className="metric-value">{confidence.confidence_score.toFixed(2)}</span>
          </div>
        </div>
      )}
    </div>
  );
};
