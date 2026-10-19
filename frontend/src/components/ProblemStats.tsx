import { useI18n } from "../lib/i18n";

export function ProblemStats() {
  const { t } = useI18n();
  const p = t.problem;

  return (
    <section className="section" id="problem">
      <div className="wrap">
        <div className="sec-head">
          <span className="eyebrow">{p.eyebrow}</span>
          <h2>{p.title}</h2>
          <p>{p.lead}</p>
        </div>
        <div className="stats">
          {p.cards.map((c) => (
            <div className="stat" key={c.num}>
              <div className="num">{c.num}</div>
              <p>{c.text}</p>
              <small>{c.src}</small>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
