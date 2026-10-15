export const HowItWorks = () => {
  return (
    <section id="how-it-works" className="how-it-works-section">
      <div className="content-container">
        <div className="section-header">
          <h2>How the evidence review works</h2>
          <p>MedGuide separates answer generation from evidence verification.</p>
        </div>
        <div className="process-steps">
          <div className="step-item">
            <div className="step-number">01 &mdash; Retrieve</div>
            <p className="step-desc">Retrieve relevant passages from the indexed medical knowledge base.</p>
          </div>
          <div className="step-item">
            <div className="step-number">02 &mdash; Generate</div>
            <p className="step-desc">Generate an answer using retrieved context rather than unsupported outside information.</p>
          </div>
          <div className="step-item">
            <div className="step-number">03 &mdash; Verify</div>
            <p className="step-desc">Extract claims and compare them against retrieved evidence using semantic similarity and NLI.</p>
          </div>
          <div className="step-item">
            <div className="step-number">04 &mdash; Score</div>
            <p className="step-desc">Combine retrieval quality, semantic similarity, NLI entailment, and claim consistency into a confidence score.</p>
          </div>
          <div className="step-item">
            <div className="step-number">05 &mdash; Correct</div>
            <p className="step-desc">When evidence is insufficient or contradictory, generate an evidence-grounded correction and verify it again.</p>
          </div>
        </div>
      </div>
    </section>
  );
};
