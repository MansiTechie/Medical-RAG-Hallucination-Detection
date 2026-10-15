import React from 'react';
import { CheckCircle, AlertCircle, XCircle } from 'lucide-react';
import type { HallucinationDecision } from '../types/api';

interface StatusBadgeProps {
  decision: HallucinationDecision['decision'];
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ decision }) => {
  if (decision === 'SUPPORTED') {
    return (
      <div className="status-badge supported">
        <CheckCircle size={16} />
        <span>Supported by retrieved evidence</span>
      </div>
    );
  }
  
  if (decision === 'POTENTIAL HALLUCINATION') {
    return (
      <div className="status-badge potential">
        <AlertCircle size={16} />
        <span>Some claims could not be sufficiently supported</span>
      </div>
    );
  }

  return (
    <div className="status-badge contradicted">
      <XCircle size={16} />
      <span>Evidence conflicts with one or more claims</span>
    </div>
  );
};
