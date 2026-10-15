import { ShieldCheck, CheckCircle2, FileText, RefreshCcw } from 'lucide-react';

export const Capabilities = () => {
  return (
    <section className="capabilities-section">
      <div className="capabilities-grid">
        <div className="capability-item">
          <ShieldCheck size={28} className="capability-icon" strokeWidth={1.5} />
          <span className="capability-title">Evidence grounded</span>
          <span className="capability-desc">Responses are generated from retrieved medical documents.</span>
        </div>
        <div className="capability-item">
          <CheckCircle2 size={28} className="capability-icon" strokeWidth={1.5} />
          <span className="capability-title">Claim verification</span>
          <span className="capability-desc">Claims are checked against supporting evidence.</span>
        </div>
        <div className="capability-item">
          <FileText size={28} className="capability-icon" strokeWidth={1.5} />
          <span className="capability-title">Source citations</span>
          <span className="capability-desc">Relevant document pages remain visible.</span>
        </div>
        <div className="capability-item">
          <RefreshCcw size={28} className="capability-icon" strokeWidth={1.5} />
          <span className="capability-title">Self-correction</span>
          <span className="capability-desc">Unsupported responses can be refined using retrieved evidence and verified again.</span>
        </div>
      </div>
    </section>
  );
};
