"""
ScamCheck KZ - B2B Bank API & Antifraud-Center Integration Module
Provides pre-transfer fraud checks for Kazakhstan banking applications (Kaspi, Halyk, BCC, Freedom, Jusan).
Evaluates recipient risk, transfer amount, social engineering in chat transcripts, and blacklist matching.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
import time
import re

from .detector import detector


class BlacklistRegistry:
    """In-memory database of registered Kazakhstan fraudulent accounts and phishing links."""

    def __init__(self):
        # Known dropper cards and phone numbers reported to CyberPol & Antifraud-Center
        self.flagged_phones = {
            "+77051234567",
            "+77719876543",
            "+77475551122",
            "+77083334455",
            "+77009998877",
            "87051234567",
            "87719876543",
        }
        self.flagged_cards = {
            "4400430112345678",
            "5169490011223344",
            "4052560099887766",
            "4765320055443322",
        }
        self.flagged_domains = {
            "kaspi-kz.info",
            "halyk-secure.kz",
            "post-kz-pay.com",
            "olx-delivery-kz.me",
            "krisha-deposit.com",
            "kazatomprom-invest.net",
        }

    def normalize_phone(self, phone: str) -> str:
        digits = re.sub(r"\D", "", phone)
        if digits.startswith("8") and len(digits) == 11:
            digits = "7" + digits[1:]
        return "+" + digits if digits else ""

    def normalize_card(self, card: str) -> str:
        return re.sub(r"\D", "", card)

    def is_phone_blacklisted(self, phone: str) -> bool:
        normalized = self.normalize_phone(phone)
        return normalized in self.flagged_phones or phone in self.flagged_phones

    def is_card_blacklisted(self, card: str) -> bool:
        normalized = self.normalize_card(card)
        return normalized in self.flagged_cards

    def is_url_blacklisted(self, url: str) -> bool:
        lower_url = url.lower()
        return any(domain in lower_url for domain in self.flagged_domains)

    def add_scam_report(self, target: str, category: str, notes: Optional[str] = None):
        """Register newly reported target to blacklist."""
        clean_target = target.strip()
        if re.search(r"\d{10,16}", clean_target):
            if len(self.normalize_card(clean_target)) >= 16:
                self.flagged_cards.add(self.normalize_card(clean_target))
            else:
                self.flagged_phones.add(self.normalize_phone(clean_target))
        elif "." in clean_target:
            self.flagged_domains.add(clean_target.lower())


blacklist = BlacklistRegistry()


# Pydantic Schemas for Bank API
class BankPreCheckRequest(BaseModel):
    sender_iin: str = Field(..., description="Sender's 12-digit IIN (Individual Identification Number)")
    recipient_account: str = Field(..., description="Recipient phone number or card number")
    amount: float = Field(..., gt=0, description="Transfer amount in KZT (Kazakhstani Tenge)")
    is_new_recipient: bool = Field(True, description="True if transfer is to a first-time recipient")
    chat_text: Optional[str] = Field(None, description="Optional chat transcript or SMS leading up to payment")
    transfer_note: Optional[str] = Field(None, description="Payment description or comment")
    lang: str = Field("ru", description="Language code: 'ru' or 'kz'")


class BankPreCheckResponse(BaseModel):
    decision: str = Field(..., description="Bank action: 'ALLOW', 'WARN_USER', 'REQUIRE_BIOMETRICS', 'BLOCK_TRANSFER'")
    risk_score: int = Field(..., ge=0, le=100, description="Aggregated risk score from 0 to 100")
    risk_level: str = Field(..., description="'SAFE', 'SUSPICIOUS', 'HIGH_RISK'")
    reasons: List[str] = Field(..., description="List of detected risk factors")
    warning_title: Optional[str] = None
    warning_message: Optional[str] = None
    recommended_actions: List[str]
    chat_analysis: Optional[Dict[str, Any]] = None
    antifraud_case_id: str
    timestamp: float


class ScamReportRequest(BaseModel):
    reporter_contact: Optional[str] = Field(None, description="Reporter phone or email")
    scam_target: str = Field(..., description="Fraudulent phone number, card number, or link")
    category: str = Field(..., description="Fraud category (e.g. 'safe_account', 'krisha_rent', 'dropper')")
    description: Optional[str] = Field(None, description="Description of the incident")


class ScamReportResponse(BaseModel):
    status: str
    report_id: str
    message: str


class BlacklistCheckResponse(BaseModel):
    query: str
    is_blacklisted: bool
    risk_factor: str
    details: Optional[str] = None


class BankService:
    """Coordinates risk scoring and policy rules for bank transactions."""

    def evaluate_transfer(self, req: BankPreCheckRequest) -> BankPreCheckResponse:
        case_id = f"KZ-AF-{uuid.uuid4().hex[:8].upper()}"
        reasons: List[str] = []
        base_risk = 0
        lang = req.lang if req.lang in ["ru", "kz"] else "ru"

        # 1. Blacklist database verification
        is_card_flagged = blacklist.is_card_blacklisted(req.recipient_account)
        is_phone_flagged = blacklist.is_phone_blacklisted(req.recipient_account)

        if is_card_flagged or is_phone_flagged:
            base_risk += 80
            reasons.append(
                "Получатель найден в реестре дропперов Национального Банка РК"
                if lang == "ru"
                else "Алушы ҚР Ұлттық Банкінің дропперлер тізілімінде табылды"
            )

        # 2. Transaction Amount and New Recipient heuristic
        if req.is_new_recipient:
            if req.amount >= 500000:
                base_risk += 30
                reasons.append(
                    f"Крупная сумма ({req.amount:,.0f} ₸) первичному получателю"
                    if lang == "ru"
                    else f"Жаңа алушыға ірі сома ({req.amount:,.0f} ₸) аударылуда"
                )
            elif req.amount >= 100000:
                base_risk += 15
                reasons.append(
                    "Перевод новому получателю превышает 100 000 ₸"
                    if lang == "ru"
                    else "Жаңа алушыға аударым 100 000 ₸ асады"
                )

        # 3. Chat transcript / Social Engineering analysis
        chat_result = None
        if req.chat_text and req.chat_text.strip():
            chat_result = detector.analyze(req.chat_text, lang=lang)
            chat_score = chat_result["score"]
            chat_level = chat_result["level"]

            if chat_level == "risk":
                base_risk += max(50, chat_score)
                scheme_str = chat_result.get("scheme_name") or "Социальная инженерия"
                reasons.append(
                    f"В прикрепленном диалоге выявлены признаки схемы «{scheme_str}» ({chat_score}% риска)"
                    if lang == "ru"
                    else f"Қоса берілген хат-хабарда «{scheme_str}» алаяқтық схемасы анықталды ({chat_score}% қауіп)"
                )
            elif chat_level == "warn":
                base_risk += chat_score
                reasons.append(
                    f"Подозрительные маркеры в диалоге ({chat_score}% риска)"
                    if lang == "ru"
                    else f"Чатта күмәнді белгілер анықталды ({chat_score}% қауіп)"
                )

        final_score = min(99, max(0, base_risk))

        # 4. Decision policy matrix
        if final_score >= 75 or is_card_flagged or is_phone_flagged:
            decision = "BLOCK_TRANSFER"
            risk_level = "HIGH_RISK"
            title = (
                "🚨 ПЕРЕВОД ЗАБЛОКИРОВАН: ВЫСОКИЙ РИСК ОБМАНА"
                if lang == "ru"
                else "🚨 АУДАРЫМ БҰҒАТТАЛДЫ: АЛАЯҚТЫҚ ҚАУПІ ЖОҒАРЫ"
            )
            msg = (
                "Банк приостановил операцию для защиты ваших средств. Получатель связан со схемами социальной инженерии или дропперства."
                if lang == "ru"
                else "Банк қаражатыңызды қорғау үшін операцияны тоқтатты. Алушы алаяқтық немесе дропперлік схемалармен байланысты."
            )
            actions = [
                "Немедленно прервите общение с собеседником" if lang == "ru" else "Сұхбаттасушымен байланысты дереу үзіңіз",
                "Позвоните в колл-центр банка по номеру на обороте карты" if lang == "ru" else "Картаның артындағы нөмір бойынша банкке қоңырау шалыңыз",
                "Обратитесь в Киберпол РК по номеру 102" if lang == "ru" else "102 нөмірі бойынша Киберполға хабарласыңыз"
            ]

        elif final_score >= 40:
            decision = "REQUIRE_BIOMETRICS"
            risk_level = "SUSPICIOUS"
            title = (
                "⚠️ ТРЕБУЕТСЯ ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА"
                if lang == "ru"
                else "⚠️ ҚОСЫМША ТЕКСЕРУ ТАЛАП ЕТІЛЕДІ"
            )
            msg = (
                "Операция имеет признаки подозрительной активности. Для продолжения пройдите видео-идентификацию (Face ID) и подтвердите, что на вас не оказывается давление."
                if lang == "ru"
                else "Операцияда күмәнді белгілер бар. Жалғастыру үшін Face ID растауынан өтіңіз және сізге қысым жасалмағанын растаңыз."
            )
            actions = [
                "Перепроверьте личность получателя" if lang == "ru" else "Алушының жеке басын қайта тексеріңіз",
                "Не совершайте перевод под диктовку третьих лиц" if lang == "ru" else "Бөгде адамдардың нұсқауымен ақша аудармаңыз"
            ]

        elif final_score >= 20:
            decision = "WARN_USER"
            risk_level = "SUSPICIOUS"
            title = (
                "💡 ПРЕДУПРЕЖДЕНИЕ БЕЗОПАСНОСТИ"
                if lang == "ru"
                else "💡 ҚАУІПСІЗДІК ЕСКЕРТУІ"
            )
            msg = (
                "Вы совершаете перевод новому адресату. Убедитесь в надежности контрагента."
                if lang == "ru"
                else "Сіз жаңа адресатқа ақша аударудасыз. Алушының сенімділігіне көз жеткізіңіз."
            )
            actions = [
                "Убедитесь в получении товара/услуги перед оплатой" if lang == "ru" else "Төлем жасамас бұрын тауарды алғаныңызға көз жеткізіңіз"
            ]

        else:
            decision = "ALLOW"
            risk_level = "SAFE"
            title = None
            msg = None
            actions = [
                "Транзакция соответствует критериям безопасности" if lang == "ru" else "Транзакция қауіпсіздік талаптарына сай"
            ]

        return BankPreCheckResponse(
            decision=decision,
            risk_score=final_score,
            risk_level=risk_level,
            reasons=reasons,
            warning_title=title,
            warning_message=msg,
            recommended_actions=actions,
            chat_analysis=chat_result,
            antifraud_case_id=case_id,
            timestamp=time.time()
        )


bank_service = BankService()
