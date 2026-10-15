import React from 'react';
import { X } from 'lucide-react';
import type { Source } from '../types/api';

interface EvidenceDrawerProps {
  source: Source | null;
  onClose: () => void;
}

export const EvidenceDrawer: React.FC<EvidenceDrawerProps> = ({ source, onClose }) => {
  if (!source) return null;

  return (
    <>
      <div className="drawer-overlay" onClick={onClose}></div>
      <div className="evidence-drawer">
        <div className="drawer-header">
          <h3 className="drawer-title">Evidence Context (Page {source.page})</h3>
          <button className="close-btn" onClick={onClose} aria-label="Close drawer">
            <X size={20} />
          </button>
        </div>
        <div className="drawer-content">
          <p className="evidence-text">
            {source.text}
          </p>
        </div>
      </div>
    </>
  );
};
