"""
ScamCheck KZ - Anti-Fraud Detector Engine Adapter
Unified adapter bridging domain use-cases with the FastAPI application and Telegram bot.
Supports Russian and Kazakh languages.
"""

from typing import Dict, List, Any, Optional
import os
import sys

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from domain.value_objects import Language, RiskLevel
from domain.entities import FraudAnalysisResult
from use_cases.analyze_fraud import AnalyzeFraudUseCase
from infrastructure.rule_repository import InMemoryRuleRepository

# Scheme definitions dictionary for external consumers
rule_repo = InMemoryRuleRepository()
SCHEMES = {
    s.id: {
        "id": s.id,
        "name_ru": s.name_ru,
        "name_kz": s.name_kz,
        "description_ru": s.description_ru,
        "description_kz": s.description_kz,
        "base_weight": s.base_weight
    }
    for s in rule_repo.get_all_schemes()
}


class AntiFraudDetector:
    """Core detector engine for ScamCheck KZ powered by Clean Architecture."""

    def __init__(self):
        self._use_case = AnalyzeFraudUseCase(repository=rule_repo)

    def analyze(self, text: str, lang: str = "ru") -> Dict[str, Any]:
        """Analyze text and return standardized dictionary assessment."""
        result: FraudAnalysisResult = self._use_case.execute(text, lang_code=lang)
        lang_enum = Language.KAZAKH if lang == "kz" else Language.RUSSIAN

        return {
            "score": result.score,
            "level": result.level.value,
            "scheme": result.scheme.id if result.scheme else None,
            "scheme_name": result.scheme.get_name(lang_enum) if result.scheme else None,
            "triggers": result.triggers,
            "highlights": [
                {
                    "start": h.start,
                    "end": h.end,
                    "text": h.matched_text
                }
                for h in result.highlights
            ],
            "recommendations": result.recommendations
        }


# Singleton instance
detector = AntiFraudDetector()
