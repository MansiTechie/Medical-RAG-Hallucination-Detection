import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingStateProps {
  step?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({ step = "Retrieving evidence…" }) => {
  return (
    <div className="loading-state">
      <Loader2 className="spinner" size={32} />
      <p className="loading-text">{step}</p>
    </div>
  );
};
