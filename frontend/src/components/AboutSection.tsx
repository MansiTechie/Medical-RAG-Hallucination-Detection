export const AboutSection = () => {
  return (
    <section id="about" className="about-section">
      <div className="content-container">
        <div className="section-header">
          <h2>Built for evidence-grounded medical question answering</h2>
        </div>
        <div className="about-content">
          <p className="about-text">
            MedGuide is a research-oriented medical RAG system designed to reduce unsupported model claims by verifying generated answers against retrieved source evidence.
          </p>
          
          <div className="pipeline-flow">
            PDF ingestion &rarr; chunking &rarr; embeddings &rarr; FAISS retrieval &rarr; grounded generation &rarr; claim extraction &rarr; NLI verification &rarr; confidence scoring &rarr; self-correction &rarr; re-verification
          </div>

          <div className="tech-stack">
            <span className="tech-badge">React + TypeScript</span>
            <span className="tech-badge">FastAPI</span>
            <span className="tech-badge">FAISS</span>
            <span className="tech-badge">Sentence Transformers</span>
            <span className="tech-badge">NLI</span>
            <span className="tech-badge">Gemini</span>
          </div>
        </div>
      </div>
    </section>
  );
};
