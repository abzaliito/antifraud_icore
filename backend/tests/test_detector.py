"""
Unit Tests for Anti-Fraud Detector Engine
Tests risk scoring, scheme classification, and highlight span generation.
"""

import pytest
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.detector import detector, SCHEMES


def test_safe_account_scheme_russian():
    text = (
        "Здравствуйте! Это старший специалист службы безопасности Национального банка. "
        "На ваше имя оформляют кредит на 2 500 000 тенге. Срочно переведите деньги на безопасный резервный счёт!"
    )
    res = detector.analyze(text, lang="ru")
    assert res["level"] == "risk"
    assert res["scheme"] == "safe_account"
    assert res["score"] >= 55
    assert len(res["triggers"]) > 0
    assert len(res["highlights"]) > 0


def test_safe_account_scheme_kazakh():
    text = (
        "Сәлеметсіз бе! Бұл Ұлттық банктің қауіпсіздік қызметі. "
        "Сіздің атыңызға 2 500 000 теңге несие рәсімделуде. Ақшаны тез арада қауіпсіз шотқа аударыңыз!"
    )
    res = detector.analyze(text, lang="kz")
    assert res["level"] == "risk"
    assert res["scheme"] == "safe_account"
    assert res["score"] >= 55


def test_dropper_card_scheme():
    text = "Сдай карту в аренду и получай 40 000 тенге в день! Нужно просто пропустить переводы через твой Каспи."
    res = detector.analyze(text, lang="ru")
    assert res["level"] == "risk"
    assert res["scheme"] == "dropper_card"
    assert res["score"] >= 60


def test_sms_code_scheme():
    text = "Добрый день, говорит менеджер eGov. Продиктуйте код из SMS для подтверждения перерегистрации льгот!"
    res = detector.analyze(text, lang="ru")
    assert res["level"] == "risk"
    assert res["scheme"] == "sms_code"
    assert res["score"] >= 60


def test_krisha_rent_scheme():
    text = (
        "Квартира свободна, 2 комнаты в центре за 140 000 тг. "
        "Я сейчас за границей, показать лично не могу. Скиньте залог 50 000 на карту Каспи."
    )
    res = detector.analyze(text, lang="ru")
    assert res["level"] == "risk"
    assert res["scheme"] == "krisha_rent"


def test_telegram_job_scheme():
    text = (
        "Работа в Telegram! За ставку лайков платим 2000 тг сразу, "
        "затем нужно пополнить баланс на 30 000 тг для выкупа товаров."
    )
    res = detector.analyze(text, lang="ru")
    assert res["level"] in ["warn", "risk"]
    assert res["scheme"] == "telegram_job"


def test_crypto_investment_scheme():
    text = (
        "Инвестиционная платформа Казатомпром! Гарантированный доход от 350 000 тенге в неделю без риска. "
        "Переведите первый депозит 50 000 тг."
    )
    res = detector.analyze(text, lang="ru")
    assert res["level"] == "risk"
    assert res["scheme"] == "crypto_invest"


def test_safe_legitimate_message():
    text = "Привет! Встречаемся сегодня в 19:00 возле Хан Шатыра? Я забронировал столик на троих."
    res = detector.analyze(text, lang="ru")
    assert res["level"] == "safe"
    assert res["score"] < 25
    assert res["scheme"] is None


def test_empty_input_handling():
    res = detector.analyze("", lang="ru")
    assert res["level"] == "safe"
    assert res["score"] == 0
    assert res["triggers"] == []


def test_all_schemes_registered():
    assert len(SCHEMES) >= 8
    for sid, data in SCHEMES.items():
        assert "name_ru" in data
        assert "name_kz" in data
        assert "base_weight" in data
