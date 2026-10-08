"""
Application Layer - Analyze Fraud Use Case
Encapsulates application business rules for analyzing chat transcripts.
"""

from typing import Dict, List, Optional
from domain.entities import FraudAnalysisResult, FraudScheme
from domain.value_objects import RiskLevel, Language, TextHighlight
from infrastructure.rule_repository import InMemoryRuleRepository


class AnalyzeFraudUseCase:
    """Primary use case for analyzing text for financial fraud indicators."""

    def __init__(self, repository: Optional[InMemoryRuleRepository] = None):
        self._repository = repository or InMemoryRuleRepository()

    def execute(self, text: str, lang_code: str = "ru") -> FraudAnalysisResult:
        lang = Language.KAZAKH if lang_code == "kz" else Language.RUSSIAN

        if not text or not text.strip():
            return FraudAnalysisResult(
                score=0,
                level=RiskLevel.SAFE,
                scheme=None,
                triggers=[],
                highlights=[],
                recommendations=self._build_recommendations(RiskLevel.SAFE, lang)
            )

        total_score = 0
        triggers: List[str] = []
        highlights: List[TextHighlight] = []
        scheme_scores: Dict[str, int] = {}

        rules = self._repository.get_rules()

        for rule in rules:
            matches = list(rule.regex.finditer(text))
            if matches:
                total_score += rule.weight
                trigger_tag = rule.get_tag(lang)
                triggers.append(trigger_tag)

                if rule.scheme_id:
                    scheme_scores[rule.scheme_id] = scheme_scores.get(rule.scheme_id, 0) + rule.weight

                for match in matches:
                    highlights.append(
                        TextHighlight(
                            start=match.start(),
                            end=match.end(),
                            matched_text=match.group(0)
                        )
                    )

        total_score = min(98, total_score)

        if total_score >= 50:
            level = RiskLevel.HIGH_RISK
        elif total_score >= 25:
            level = RiskLevel.SUSPICIOUS
        else:
            level = RiskLevel.SAFE

        matched_scheme: Optional[FraudScheme] = None
        if scheme_scores and level != RiskLevel.SAFE:
            top_scheme_id = max(scheme_scores.items(), key=lambda x: x[1])[0]
            matched_scheme = self._repository.get_scheme_by_id(top_scheme_id)

        # Deduplicate triggers while preserving order
        unique_triggers = list(dict.fromkeys(triggers))

        return FraudAnalysisResult(
            score=total_score,
            level=level,
            scheme=matched_scheme,
            triggers=unique_triggers,
            highlights=highlights,
            recommendations=self._build_recommendations(level, lang)
        )

    def _build_recommendations(self, level: RiskLevel, lang: Language) -> List[str]:
        if lang == Language.KAZAKH:
            if level == RiskLevel.HIGH_RISK:
                return [
                    "АҚША АУДАРМАҢЫЗ және ешқандай құпия кодтарды бермеңіз",
                    "Картаның артындағы нөмір бойынша банктің ресми колл-центріне хабарласыңыз",
                    "102 немесе Киберпол нөміріне алаяқтық туралы хабарлаңыз"
                ]
            elif level == RiskLevel.SUSPICIOUS:
                return [
                    "Әңгімелесушіге нақтылаушы сұрақтар қойыңыз",
                    "Чаттағы сыртқы сілтемелерге өтпеңіз",
                    "Ақпаратты ресми дереккөздерден қайта тексеріңіз"
                ]
            else:
                return [
                    "Алаяқтықтың айқын белгілері табылған жоқ",
                    "Ақша сұраса — адамға жеке қоңырау шалыңыз",
                    "SMS-кодтар мен құпия сөздерді ешқашан айтпаңыз"
                ]
        else:
            if level == RiskLevel.HIGH_RISK:
                return [
                    "НЕ ПЕРЕВОДИТЕ ДЕНЬГИ и не передавайте никакие коды из SMS",
                    "Позвоните в официальный колл-центр банка по номеру на карте",
                    "Сообщите о мошенничестве по номеру 102 или в Киберпол"
                ]
            elif level == RiskLevel.SUSPICIOUS:
                return [
                    "Задайте уточняющие вопросы собеседнику",
                    "Не переходите по внешним ссылкам из чата",
                    "Перепроверьте информацию в официальных источниках"
                ]
            else:
                return [
                    "Явных признаков мошенничества не выявлено",
                    "Если вас просят о финансовой помощи — перезвоните человеку лично",
                    "Никогда не сообщайте SMS-коды и пароли"
                ]
