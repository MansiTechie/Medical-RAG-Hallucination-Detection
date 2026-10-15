import { useState, useRef } from 'react';
import { Header } from './components/Header';
import { SearchBox } from './components/SearchBox';
import { AnswerSection } from './components/AnswerSection';
import { VerificationSummary } from './components/VerificationSummary';
import { ClaimVerification } from './components/ClaimVerification';
import { SourceList } from './components/SourceList';
import { EvidenceDrawer } from './components/EvidenceDrawer';
import { VerificationDetails } from './components/VerificationDetails';
import { LoadingState } from './components/LoadingState';
import { ErrorState } from './components/ErrorState';
import { Capabilities } from './components/Capabilities';
import { HowItWorks } from './components/HowItWorks';
import { GuidelinesSection } from './components/GuidelinesSection';
import { AboutSection } from './components/AboutSection';
import { askMedicalQuestion, ApiError } from './services/api';
import type { AskResponse, Source } from './types/api';

type AppState = 'landing' | 'loading' | 'result' | 'error';

function App() {
  const [appState, setAppState] = useState<AppState>('landing');
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<AskResponse | null>(null);
  const [selectedSource, setSelectedSource] = useState<Source | null>(null);
  const [loadingStep, setLoadingStep] = useState('Reviewing medical evidence…');
  const [errorMessage, setErrorMessage] = useState<string | undefined>();
  const abortControllerRef = useRef<AbortController | null>(null);

  const suggestions = [
    "What are the risk factors for type 2 diabetes?",
    "What is prediabetes?",
    "How can diabetes be prevented or delayed?"
  ];

  const handleSearch = async (newQuery: string) => {
    if (!newQuery.trim()) return;

    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    const newController = new AbortController();
    abortControllerRef.current = newController;

    setQuery(newQuery);
    setErrorMessage(undefined);
    setAppState('loading');
    window.scrollTo(0, 0);

    setLoadingStep("Reviewing medical evidence…");

    try {
      const data = await askMedicalQuestion(newQuery, newController.signal);
      setResponse(data);
      setAppState('result');
      window.scrollTo(0, 0);
    } catch (error) {
      if (error instanceof Error && error.name === 'AbortError') {
        return;
      }
      if (error instanceof ApiError) {
        setErrorMessage(error.message);
      } else {
        setErrorMessage("MedGuide could not complete the evidence review. Please try again.");
      }
      setAppState('error');
    } finally {
      if (abortControllerRef.current === newController) {
        abortControllerRef.current = null;
      }
    }
  };

  const resetToLanding = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setAppState('landing');
    setQuery('');
    setResponse(null);
    setErrorMessage(undefined);
    window.scrollTo(0, 0);
  };

  const handleNavClick = (targetId: string) => {
    if (appState !== 'landing') {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
        abortControllerRef.current = null;
      }
      setAppState('landing');
      setQuery('');
      setResponse(null);
      setErrorMessage(undefined);
      setTimeout(() => {
        if (targetId === 'top') {
          window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
          document.getElementById(targetId)?.scrollIntoView({ behavior: 'smooth' });
        }
      }, 50);
    } else {
      if (targetId === 'top') {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else {
        document.getElementById(targetId)?.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  return (
    <>
      <Header onNavClick={handleNavClick} />

      <main className="main-content" id="top">
        {appState === 'landing' && (
          <div className="landing-view">
            <section className="hero">
              <h1>Evidence, before answers.</h1>
              <p>Ask questions grounded in trusted medical guidelines and research documents.</p>
            </section>

            <section className="search-section">
              <div className="search-container">
                <SearchBox onSearch={handleSearch} />
              </div>

              <div className="search-suggestions">
                <span className="search-suggestions-label">Try asking</span>
                <div className="suggestions-list">
                  {suggestions.map((suggestion, idx) => (
                    <button
                      key={idx}
                      className="suggestion-btn"
                      onClick={() => handleSearch(suggestion)}
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            </section>

            <Capabilities />

            <HowItWorks />

            <GuidelinesSection />

            <AboutSection />
          </div>
        )}

        {appState === 'loading' && (
          <div className="loading-view">
            <LoadingState step={loadingStep} />
          </div>
        )}

        {appState === 'error' && (
          <div className="error-view">
            <ErrorState onRetry={() => handleSearch(query)} message={errorMessage} />
          </div>
        )}

        {appState === 'result' && response && (
          <div className="result-view">
            <div className="result-header">
              <h2 className="result-query">"{query}"</h2>
              <button className="new-question-btn" onClick={resetToLanding}>
                New question
              </button>
            </div>

            <div className="result-layout">
              <div className="main-column">
                <AnswerSection
                  answer={response.answer}
                  isCorrected={response.self_correction.correction_applied}
                />

                <ClaimVerification claims={response.claim_verification.claims} />
              </div>

              <div className="side-column">
                <VerificationSummary
                  decision={response.hallucination_decision}
                  confidence={response.confidence}
                  verification={response.claim_verification}
                />

                <VerificationDetails confidence={response.confidence} />

                <SourceList
                  sources={response.sources}
                  onViewEvidence={(source) => setSelectedSource(source)}
                />
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <div className="footer-container">
          <div className="footer-brand">
            <strong>MedGuide</strong>
            <span>Medical Evidence Assistant</span>
          </div>
          <div className="footer-links">
            <a href="#guidelines" onClick={(e) => { e.preventDefault(); handleNavClick('guidelines'); }}>Guidelines</a>
            <a href="#how-it-works" onClick={(e) => { e.preventDefault(); handleNavClick('how-it-works'); }}>How it works</a>
            <a href="#about" onClick={(e) => { e.preventDefault(); handleNavClick('about'); }}>About</a>
          </div>
          <div className="footer-meta-links">
            <span className="footer-disclaimer">Not a substitute for professional medical advice.</span>
            <span className="footer-project-type">Resume / research project</span>
          </div>
        </div>
      </footer>

      <EvidenceDrawer source={selectedSource} onClose={() => setSelectedSource(null)} />
    </>
  );
}

export default App;
