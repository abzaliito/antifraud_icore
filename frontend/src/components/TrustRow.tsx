import { useI18n } from "../lib/i18n";

const CHANNELS = ["Kaspi", "Halyk", "BCC", "Freedom", "Jusan", "Krisha.kz", "OLX", "WhatsApp", "Telegram"];

export function TrustRow() {
  const { t } = useI18n();
  return (
    <section className="trust" aria-label={t.trust.title}>
      <div className="wrap">
        <p className="trust-title">{t.trust.title}</p>
        <div className="trust-logos">
          {CHANNELS.map((name, i) => (
            <span key={name}>
              {i > 0 && <span className="dot" aria-hidden="true" />}
              {name}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}
