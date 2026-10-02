import { useState, useEffect } from "react";
import { queryApi, healthApi } from "./api";
import type { QueryResponse } from "./types";
import "./App.css";

const EXAMPLES = [
  "What requirements apply to testing autonomous vehicles in California?",
  "What is the difference between SAE Level 3 and Level 4 automation?",
  "What safety systems are required for new vehicles in the EU?",
  "What data recording requirements exist for automated driving systems?",
  "What happens when an autonomous vehicle is involved in a collision in California?",
];

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [backendReady, setBackendReady] = useState<boolean | null>(null);

  useEffect(() => {
    healthApi()
      .then((h) => setBackendReady(h.vector_store_ready))
      .catch(() => setBackendReady(false));
  }, []);

  async function handleSubmit(e?: React.FormEvent) {
    e?.preventDefault();
    const q = question.trim();
    if (!q || q.length < 3) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await queryApi(q);
      setResult(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  function handleExample(ex: string) {
    setQuestion(ex);
    setResult(null);
    setError(null);
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo">CORA</div>
        <p className="subtitle">Autonomous Vehicle Regulatory Intelligence</p>
      </header>

      <main className="main">
        {!result && !loading && !error && (
          <section className="hero">
            <h1>
              Understand complex autonomous vehicle regulations through
              AI-powered research.
            </h1>
          </section>
        )}

        <form className="search-form" onSubmit={handleSubmit}>
          <div className="input-row">
            <input
              type="text"
              className="search-input"
              placeholder="Ask CORA about autonomous vehicle regulations..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              disabled={loading}
              maxLength={1000}
            />
            <button
              type="submit"
              className="search-btn"
              disabled={loading || question.trim().length < 3}
            >
              {loading ? "Searching..." : "Ask CORA"}
            </button>
          </div>
        </form>

        {!result && !loading && !error && (
          <div className="examples">
            <p className="examples-label">Try an example</p>
            <div className="example-chips">
              {EXAMPLES.map((ex) => (
                <button
                  key={ex}
                  className="example-chip"
                  onClick={() => handleExample(ex)}
                >
                  {ex}
                </button>
              ))}
            </div>
          </div>
        )}

        {loading && (
          <div className="loading">
            <div className="spinner" />
            <p>Searching regulatory sources...</p>
          </div>
        )}

        {error && (
          <div className="error-box">
            <p>{error}</p>
          </div>
        )}

        {result && (
          <div className="result">
            <div className="answer-card">
              <div className="answer-header">
                <h2>CORA Answer</h2>
                {result.grounded && (
                  <span className="grounded-badge">Grounded</span>
                )}
                {!result.grounded && result.sources.length > 0 && (
                  <span className="ungrounded-badge">Low confidence</span>
                )}
              </div>
              <div className="answer-text">{result.answer}</div>
              <p className="chunk-info">
                Based on {result.chunk_count} retrieved{" "}
                {result.chunk_count === 1 ? "source" : "sources"}
              </p>
            </div>

            {result.sources.length > 0 && (
              <div className="sources-section">
                <h3>Sources</h3>
                <div className="sources-list">
                  {result.sources.map((s, i) => (
                    <div key={i} className="source-card">
                      <div className="source-number">{i + 1}</div>
                      <div className="source-content">
                        <div className="source-title">{s.title}</div>
                        <div className="source-section">{s.section}</div>
                        <div className="source-meta">
                          <span>{s.source}</span>
                          {s.jurisdiction && (
                            <span className="jurisdiction">
                              {s.jurisdiction}
                            </span>
                          )}
                          <span className="relevance">
                            {Math.round(s.relevance * 100)}% relevant
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <button
              className="new-question-btn"
              onClick={() => {
                setResult(null);
                setQuestion("");
                setError(null);
              }}
            >
              Ask another question
            </button>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>
          CORA is an information retrieval tool for research purposes. It does
          not provide legal advice. Always verify regulatory information with
          official sources.
        </p>
        {backendReady === false && (
          <p className="backend-warning">
            Backend is not connected or the vector store is empty.
          </p>
        )}
      </footer>
    </div>
  );
}

export default App;
