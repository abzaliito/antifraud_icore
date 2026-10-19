"""
Unit & Integration Tests for B2B Bank API and Dropper Blacklist
"""

import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.bank_api import blacklist

client = TestClient(app)


def test_blacklist_check_phone():
    response = client.get("/api/v1/blacklist/check?query=+77051234567")
    assert response.status_code == 200
    data = response.json()
    assert data["is_blacklisted"] is True
    assert data["risk_factor"] == "SCAM_PHONE"


def test_blacklist_check_clean():
    response = client.get("/api/v1/blacklist/check?query=+77071112233")
    assert response.status_code == 200
    data = response.json()
    assert data["is_blacklisted"] is False
    assert data["risk_factor"] == "NONE"


def test_bank_pre_transfer_check_clean():
    payload = {
        "sender_iin": "990101350123",
        "recipient_account": "+77071112233",
        "amount": 15000.0,
        "is_new_recipient": False,
        "chat_text": "Привет! Возвращаю долг за обед.",
        "lang": "ru"
    }
    response = client.post("/api/v1/bank/pre-transfer-check", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "ALLOW"
    assert data["risk_level"] == "SAFE"


def test_bank_pre_transfer_check_dropper_blocked():
    payload = {
        "sender_iin": "990101350123",
        "recipient_account": "+77051234567",  # In blacklist
        "amount": 250000.0,
        "is_new_recipient": True,
        "lang": "ru"
    }
    response = client.post("/api/v1/bank/pre-transfer-check", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "BLOCK_TRANSFER"
    assert data["risk_level"] == "HIGH_RISK"
    assert len(data["reasons"]) > 0


def test_bank_pre_transfer_check_social_engineering():
    payload = {
        "sender_iin": "990101350123",
        "recipient_account": "+77078889900",
        "amount": 500000.0,
        "is_new_recipient": True,
        "chat_text": "Это служба безопасности банка. Срочно переведите сбережения на безопасный резервный счёт!",
        "lang": "ru"
    }
    response = client.post("/api/v1/bank/pre-transfer-check", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["decision"] in ["BLOCK_TRANSFER", "REQUIRE_BIOMETRICS"]
    assert data["chat_analysis"] is not None
    assert data["chat_analysis"]["level"] == "risk"


def test_submit_scam_report():
    report_payload = {
        "reporter_contact": "+77010001122",
        "scam_target": "+77089990011",
        "category": "safe_account",
        "description": "Звонили с этого номера и представлялись полицией."
    }
    response = client.post("/api/v1/reports", json=report_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "registered"
    assert "report_id" in data

    # Verify newly reported number is now blacklisted
    check_res = client.get("/api/v1/blacklist/check?query=+77089990011")
    assert check_res.json()["is_blacklisted"] is True
