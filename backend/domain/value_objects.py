"""
Domain Layer - Value Objects & Core Enums
Contains immutable domain concepts free of framework dependencies (Uncle Bob's Clean Architecture).
"""

from enum import Enum
from typing import NamedTuple, List


class Language(str, Enum):
    """Supported system languages."""
    RUSSIAN = "ru"
    KAZAKH = "kz"


class RiskLevel(str, Enum):
    """Categorized risk levels for anti-fraud assessment."""
    SAFE = "safe"
    SUSPICIOUS = "warn"
    HIGH_RISK = "risk"


class TextHighlight(NamedTuple):
    """Value object representing a matched trigger span in analyzed text."""
    start: int
    end: int
    matched_text: str
