import { useMemo, useState } from "react";
import { useI18n } from "../lib/i18n";
import { analyze, type AnalyzeResponse, type AnalyzeSource, type HighlightSpan, type RiskLevel } from "../lib/api";

type Status = "idle" | "loading" | "done" | "error";

const LEVEL_COLOR: Record<RiskLevel, string> = {
  safe: "var(--safe-ink)",
  warn: "var(--warn-ink)",
  risk: "var(--risk-ink)",
};

/** Merge overlapping spans and split `text` into plain / highlighted segments. */
function buildSegments(text: string, spans: HighlightSpan[]) {
  const sorted = [...spans]
    .filter((s) => s.end > s.start && s.start >= 0 && s.end <= text.length)
    .sort((a, b) => a.start - b.start);

  const merged: Array<{ start: number; end: number }> = [];
  for (const s of sorted) {
    const last = merged[merged.length - 1];
    if (last && s.start <= last.end) {
      last.end = Math.max(last.end, s.end);
    } else {
      merged.push({ start: s.start, end: s.end });
    }
  }

  const segments: Array<{ text: string; mark: boolean }> = [];
  let cursor = 0;
  for (const m of merged) {
    if (m.start > cursor) segments.push({ text: text.slice(cursor, m.start), mark: false });
    segments.push({ text: text.slice(m.start, m.end), mark: true });
    cursor = m.end;
  }
  if (cursor < text.length) segments.push({ text: text.slice(cursor), mark: false });
  return segments;
}

function Gauge({ score, level }: { score: number; level: RiskLevel }) {
  const r = 46;
  const circ = 2 * Math.PI * r;
  const offset = circ * (1 - Math.min(100, Math.max(0, score)) / 100);
  const color = LEVEL_COLOR[level];
  return (
    <div className="gauge">
      <svg viewBox="0 0 110 110" aria-hidden="true">
        <circle cx="55" cy="55" r={r} fill="none" stroke="var(--line)" strokeWidth="9" />
        <circle
          cx="55"
          cy="55"
          r={r}
          fill="none"
          stroke={color}
          strokeWidth="9"
          strokeLinecap="round"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 0.8s cubic-bezier(0.2,0.8,0.2,1)" }}
        />
      </svg>
      <div className="val" style={{ color }}>
        {score}%
      </div>
    </div>
  );
}

export function Demo() {
  const { t, lang } = useI18n();
  const d = t.demo;

  const [text, setText] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [source, setSource] = useState<AnalyzeSource>("server");
  const [analyzed, setAnalyzed] = useState("");
  const [activePreset, setActivePreset] = useState<number | null>(null);

  const segments = useMemo(
    () => (result ? buildSegments(analyzed, result.highlights) : []),
    [result, analyzed],
  );

  async function handleAnalyze(e: React.FormEvent) {
    e.preventDefault();
    const value = text.trim();
    if (!value) return;
    setStatus("loading");
    try {
      const { result: res, source: src } = await analyze(value, lang);
      setResult(res);
      setSource(src);
      setAnalyzed(value);
      setStatus("done");
    } catch {
      setStatus("error");
    }
  }

  function pickPreset(i: number) {
    setText(d.presets[i].text);
    setActivePreset(i);
  }

  const levelName = result ? d.resultTitle[result.level] : "";

  return (
    <section className="section demo" id="demo">
      <div className="wrap">
        <div className="sec-head">
          <span className="eyebrow">{d.eyebrow}</span>
          <h2>{d.title}</h2>
          <p>{d.lead}</p>
        </div>

        <div className="demo-grid">
          {/* Input panel */}
          <form className="panel" onSubmit={handleAnalyze}>
            <label htmlFor="msg">
              <span>{d.inputLabel}</span>
              <span className="count">{d.charCount(text.length)}</span>
            </label>
            <textarea
              id="msg"
              value={text}
              placeholder={d.placeholder}
              onChange={(e) => {
                setText(e.target.value);
                setActivePreset(null);
              }}
            />

            <div>
              <p className="presets-label">{d.presetsLabel}</p>
              <div className="ex">
                {d.presets.map((p, i) => (
                  <button
                    type="button"
                    key={p.label}
                    className={activePreset === i ? "active" : undefined}
                    onClick={() => pickPreset(i)}
                  >
                    {p.label}
                  </button>
                ))}
              </div>
            </div>

            <button className="btn btn-primary" type="submit" disabled={status === "loading" || !text.trim()}>
              {status === "loading" ? d.analyzing : d.analyze}
            </button>
          </form>

          {/* Result panel */}
          <div className={`result${status === "loading" ? " loading" : ""}`} aria-live="polite">
            <div className="scanbar" aria-hidden="true" />

            {status === "idle" && (
              <div className="placeholder">
                <div className="big">🛡️</div>
                <p>{d.emptyHint}</p>
              </div>
            )}

            {status === "loading" && (
              <div className="placeholder">
                <div className="big">🔍</div>
                <p>{d.analyzing}</p>
              </div>
            )}

            {status === "error" && (
              <div className="errorbox">
                <div className="big">⚠️</div>
                <p>
                  <strong>{d.errorTitle}</strong>
                </p>
                <code>{d.errorHint}</code>
              </div>
            )}

            {status === "done" && result && (
              <>
                <div className="r-head">
                  <Gauge score={result.score} level={result.level} />
                  <div className="r-title">
                    <span className={`pill ${result.level}`}>{levelName}</span>
                    {result.scheme_name && (
                      <h3>
                        {d.schemeLabel}: «{result.scheme_name}»
                      </h3>
                    )}
                  </div>
                </div>

                {source === "local" && <p className="local-note">{d.localNote}</p>}

                <div className="r-text">
                  {segments.map((seg, i) =>
                    seg.mark ? <mark key={i}>{seg.text}</mark> : <span key={i}>{seg.text}</span>,
                  )}
                </div>

                {result.triggers.length > 0 && (
                  <div className="r-block">
                    <h4>{d.triggersLabel}</h4>
                    <div className="r-flags">
                      {result.triggers.map((trig) => (
                        <span key={trig}>{trig}</span>
                      ))}
                    </div>
                  </div>
                )}

                {result.recommendations.length > 0 && (
                  <div className="r-block">
                    <h4>{d.adviceLabel}</h4>
                    <ul className="r-advice">
                      {result.recommendations.map((rec) => (
                        <li key={rec}>{rec}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
