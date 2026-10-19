import { useI18n } from "../lib/i18n";
import { useTheme } from "../lib/theme";

export function Header() {
  const { t, lang, setLang } = useI18n();
  const { theme, toggle } = useTheme();

  return (
    <header className="top">
      <div className="wrap">
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

        <nav className="nav" aria-label="Разделы">
          <a href="#problem">{t.nav.how}</a>
          <a href="#demo">{t.nav.demo}</a>
          <a href="#problem">{t.nav.schemes}</a>
        </nav>

        <div className="header-controls">
          <div className="lang" role="group" aria-label="Язык / Тіл">
            <button type="button" aria-pressed={lang === "ru"} onClick={() => setLang("ru")}>
              RU
            </button>
            <button type="button" aria-pressed={lang === "kz"} onClick={() => setLang("kz")}>
              ҚАЗ
            </button>
          </div>
          <button
            className="theme-toggle"
            type="button"
            onClick={toggle}
            aria-label={t.themeTitle}
            title={t.themeTitle}
          >
            {theme === "dark" ? "☀️" : "🌙"}
          </button>
          <a className="btn btn-primary btn-sm header-cta" href="#demo">
            {t.headerCta}
          </a>
        </div>
      </div>
    </header>
  );
}
