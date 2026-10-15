import { useEffect, useRef } from 'react';
import { X } from 'lucide-react';

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export const DocumentDetailsModal = ({ isOpen, onClose }: Props) => {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';
      // Focus modal
      setTimeout(() => {
        modalRef.current?.focus();
      }, 0);
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = '';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <>
      <div className="modal-overlay" onClick={onClose}></div>
      <div 
        className="document-modal" 
        role="dialog" 
        aria-labelledby="modal-title"
        aria-modal="true"
        tabIndex={-1}
        ref={modalRef}
      >
        <div className="modal-header">
          <h3 id="modal-title">Document Details</h3>
          <button className="close-btn" onClick={onClose} aria-label="Close">
            <X size={20} />
          </button>
        </div>
        <div className="modal-body">
          <h4 className="doc-full-title">Guiding Principles for the Care of People With or at Risk for Diabetes</h4>
          <p className="doc-pages">83 pages</p>
          
          <h5 className="config-title">Retrieval configuration:</h5>
          <table className="config-table">
            <tbody>
              <tr><td>Chunk size</td><td>1000</td></tr>
              <tr><td>Overlap</td><td>200</td></tr>
              <tr><td>Embeddings</td><td>all-MiniLM-L6-v2</td></tr>
              <tr><td>Dimensions</td><td>384</td></tr>
              <tr><td>Index</td><td>FAISS</td></tr>
            </tbody>
          </table>
        </div>
        <div className="modal-footer">
          <button className="modal-close-btn" onClick={onClose}>Close</button>
        </div>
      </div>
    </>
  );
};
