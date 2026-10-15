import React from 'react';
import { StatusBadge } from './StatusBadge';
import type { HallucinationDecision, Confidence, ClaimVerification } from '../types/api';

interface VerificationSummaryProps {
  decision: HallucinationDecision;
  confidence: Confidence;
  verification: ClaimVerification;
}

export const VerificationSummary: React.FC<VerificationSummaryProps> = ({ decision, confidence }) => {
  const isSupported = decision.decision === 'SUPPORTED';
  const meterWidth = `${(confidence.confidence_score * 100).toFixed(0)}%`;

  return (
    <div className="verification-summary card">
      <h3 className="section-title">VERIFICATION</h3>
      
      <StatusBadge decision={decision.decision} />

      <div className="confidence-section">
        <div className="confidence-header">
          <span className="confidence-label">Confidence</span>
          <span className="confidence-value">{(confidence.confidence_score * 100).toFixed(0)}%</span>
        </div>
        <div className="confidence-meter-bg">
          <div className={`confidence-meter-fill ${confidence.confidence_level.toLowerCase()}`} style={{ width: meterWidth }}></div>
        </div>
        <div className="confidence-level">{confidence.confidence_level}</div>
      </div>

      <p className="verification-desc">
        {isSupported 
          ? "Supporting evidence was found for the majority of the answer's claims."
          : "The evidence review found insufficient support or contradictions."}
      </p>

      <div className="contradictions-stat">
        {decision.strong_contradictions} strong contradictions
      </div>
    </div>
  );
};
