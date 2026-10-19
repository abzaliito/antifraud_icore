"""
Unit Tests for Telegram Bot logic and message processor
"""

import pytest
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bot import process_bot_message, user_langs


def test_bot_start_command_ru():
    user_langs[1001] = "ru"
    res = process_bot_message(1001, "/start")
    assert "Добро пожаловать" in res
    assert "/ru" in res


def test_bot_start_command_kz():
    user_langs[1002] = "kz"
    res = process_bot_message(1002, "/start")
    assert "қош келдіңіз" in res


def test_bot_language_switch():
    res_kz = process_bot_message(1003, "/kz")
    assert "қазақшаға" in res_kz
    assert user_langs[1003] == "kz"

    res_ru = process_bot_message(1003, "/ru")
    assert "русский" in res_ru
    assert user_langs[1003] == "ru"


def test_bot_schemes_command():
    res = process_bot_message(1004, "/schemes")
    assert "Безопасный счёт" in res or "Қауіпсіз шот" in res


def test_bot_stats_command():
    res = process_bot_message(1005, "/stats")
    assert "100.0%" in res or "Precision" in res or "дәлдігі" in res


def test_bot_fraud_detection_message():
    user_langs[1006] = "ru"
    scam_text = "Здравствуйте! Это служба безопасности банка. Срочно переведите деньги на безопасный резервный счёт!"
    res = process_bot_message(1006, scam_text)
    assert "ВЫСОКИЙ РИСК" in res
    assert "Безопасный счёт" in res
    assert "Рекомендации" in res
