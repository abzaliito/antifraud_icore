import { useI18n } from "../lib/i18n";

export function Hero() {
  const { t } = useI18n();
  const h = t.hero;

  return (
    <section className="hero" id="top">
      <div className="wrap">
        <span className="hero-badge">
          <span className="stars" aria-hidden="true">
            ★★★★★
          </span>
          {h.rating}
        </span>

        <h1>
          {h.titleLine1}
          <br />
          <span className="grad">{h.titleLine2a}</span> {h.titleLine2b}
        </h1>

        <p className="lead">{h.lead}</p>

        <div className="ctas">
          <a className="btn btn-primary" href="#demo">
            {h.ctaPrimary}
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M5 12h14M13 6l6 6-6 6" />
            </svg>
          </a>
          <a className="btn btn-ghost" href="#problem">
            {h.ctaSecondary}
          </a>
        </div>

        <div className="hero-stats">
          {h.stats.map((s) => (
            <div className="hero-stat" key={s.label}>
              <b>{s.value}</b>
              <span>{s.label}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
