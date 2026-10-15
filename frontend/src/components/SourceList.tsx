import React from 'react';
import type { Source } from '../types/api';
import { FileText, Eye } from 'lucide-react';

interface SourceListProps {
  sources: Source[];
  onViewEvidence: (source: Source) => void;
}

export const SourceList: React.FC<SourceListProps> = ({ sources, onViewEvidence }) => {
  return (
    <div className="sources-section card">
      <h3 className="section-title">Sources</h3>
      
      <div className="source-meta">
        <h4 className="source-book-title">Guiding Principles for the Care of People With or at Risk for Diabetes</h4>
        <span className="source-org">National Diabetes Education Program / NIH / CDC</span>
      </div>

      <div className="sources-list">
        {sources.map((source) => (
          <div key={source.chunk_id} className="source-card">
            <div className="source-info">
              <FileText size={16} className="source-icon" />
              <span>Page {source.page}</span>
            </div>
            <button className="view-evidence-btn" onClick={() => onViewEvidence(source)}>
              <Eye size={14} />
              <span>View evidence</span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
