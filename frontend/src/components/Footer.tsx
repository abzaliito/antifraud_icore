import { useI18n } from "../lib/i18n";

export function Footer() {
  const { t } = useI18n();
  return (
    <footer className="foot">
      <div className="wrap">
        <div>
          <a className="logo" href="#top" aria-label="ScamCheck KZ">
            <span className="logo-icon">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#06231f"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                <path d="m9 12 2 2 4-4" />
              </svg>
            </span>
            ScamCheck <small>KZ</small>
          </a>
          <p style={{ maxWidth: 420 }}>{t.footer.tagline}</p>
          <p style={{ marginTop: 10, color: "var(--teal-ink)" }}>{t.footer.project}</p>
        </div>
        <div className="disc">
          <p>{t.footer.disclaimer}</p>
        </div>
      </div>
    </footer>
  );
}
