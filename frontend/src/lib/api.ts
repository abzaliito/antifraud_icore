// Thin client for the ScamCheck KZ FastAPI backend.
// In dev, Vite proxies /api -> http://127.0.0.1:8000 (see vite.config.ts).
import type { Lang } from "./strings";

export type RiskLevel = "safe" | "warn" | "risk";

export interface HighlightSpan {
  start: number;
  end: number;
  text: string;
}

export interface AnalyzeResponse {
  score: number;
  level: RiskLevel;
  scheme: string | null;
  scheme_name: string | null;
  triggers: string[];
  highlights: HighlightSpan[];
  recommendations: string[];
  processing_time_ms: number;
}

const API_BASE = import.meta.env.VITE_API_BASE ?? "";

export async function analyzeText(text: string, lang: Lang): Promise<AnalyzeResponse> {
  const res = await fetch(`${API_BASE}/api/v1/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, lang }),
  });
  if (!res.ok) {
    throw new Error(`Analyze request failed: ${res.status}`);
  }
  return (await res.json()) as AnalyzeResponse;
}
