"""
Domain Layer - Entities
Contains core business entities with encapsulated domain rules.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from .value_objects import RiskLevel, Language, TextHighlight


@dataclass(frozen=True)
class FraudScheme:
    """Entity representing a registered Kazakhstan fraud scheme."""
    id: str
    name_ru: str
    name_kz: str
    description_ru: str
    description_kz: str
    base_weight: int

    def get_name(self, lang: Language) -> str:
        return self.name_kz if lang == Language.KAZAKH else self.name_ru


@dataclass
class FraudAnalysisResult:
    """Entity representing the complete verdict of an anti-fraud evaluation."""
    score: int
    level: RiskLevel
    scheme: Optional[FraudScheme]
    triggers: List[str] = field(default_factory=list)
    highlights: List[TextHighlight] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    @property
    def is_dangerous(self) -> bool:
        return self.level in (RiskLevel.SUSPICIOUS, RiskLevel.HIGH_RISK)
