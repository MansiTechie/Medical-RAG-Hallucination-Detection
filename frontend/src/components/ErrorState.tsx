import React from 'react';
import { AlertTriangle } from 'lucide-react';

interface ErrorStateProps {
  onRetry: () => void;
  message?: string;
}

export const ErrorState: React.FC<ErrorStateProps> = ({ onRetry, message }) => {
  return (
    <div className="error-state">
      <AlertTriangle size={48} className="error-icon" strokeWidth={1} />
      <h2 className="error-title">Evidence review unavailable</h2>
      <p className="error-desc">{message || "Something prevented the assistant from completing this review. Please try again."}</p>
      <button className="retry-button" onClick={onRetry}>Try again</button>
    </div>
  );
};
