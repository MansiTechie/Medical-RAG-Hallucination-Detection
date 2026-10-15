import React, { useState } from 'react';
import { ChevronDown, ChevronUp, CheckCircle, AlertCircle } from 'lucide-react';
import type { Claim } from '../types/api';

interface ClaimRowProps {
  claim: Claim;
}

const ClaimRow: React.FC<ClaimRowProps> = ({ claim }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className={`claim-row ${expanded ? 'expanded' : ''}`}>
      <div className="claim-header" onClick={() => setExpanded(!expanded)}>
        <div className="claim-status-icon">
          {claim.supported ? <CheckCircle size={16} className="supported-icon" /> : <AlertCircle size={16} className="potential-icon" />}
        </div>
        <div className="claim-title-area">
          <span className="claim-text">{claim.claim}</span>
          <div className="claim-meta">
            <span className="claim-status-label">{claim.supported ? 'Supported' : 'Insufficient Evidence'}</span>
            {claim.evidence && <span className="claim-page">Page {claim.evidence.page}</span>}
          </div>
        </div>
        <button className="expand-btn" aria-label="Toggle details">
          {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </button>
      </div>
      
      {expanded && claim.evidence && (
        <div className="claim-details">
          <div className="detail-group">
            <span className="detail-label">Evidence</span>
            <p className="detail-text">"{claim.evidence.text}"</p>
          </div>
          <div className="detail-group">
            <span className="detail-label">Source</span>
            <p className="detail-text">Guiding Principles for the Care of People With or at Risk for Diabetes</p>
          </div>
        </div>
      )}
    </div>
  );
}

interface ClaimVerificationProps {
  claims: Claim[];
}

export const ClaimVerification: React.FC<ClaimVerificationProps> = ({ claims }) => {
  return (
    <div className="claim-verification-section card">
      <h3 className="section-title">Claim verification</h3>
      <div className="claims-list">
        {claims.map((claim) => (
          <ClaimRow key={claim.claim_number} claim={claim} />
        ))}
      </div>
    </div>
  );
};
