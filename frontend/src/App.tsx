import { I18nProvider } from "./lib/i18n";
import { ThemeProvider } from "./lib/theme";
import { Header } from "./components/Header";
import { Hero } from "./components/Hero";
import { TrustRow } from "./components/TrustRow";
import { ProblemStats } from "./components/ProblemStats";
import { Demo } from "./components/Demo";
import { Footer } from "./components/Footer";
import "./components/components.css";

export default function App() {
  return (
    <ThemeProvider>
      <I18nProvider>
        <Header />
        <main>
          <Hero />
          <TrustRow />
          <ProblemStats />
          <Demo />
        </main>
        <Footer />
      </I18nProvider>
    </ThemeProvider>
  );
}
