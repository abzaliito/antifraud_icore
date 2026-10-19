"""
Integration Tests for FastAPI REST Endpoints
Tests health, schemes, analysis, metrics, and error handling.
"""

import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "ScamCheck KZ Anti-Fraud Engine"
    assert "version" in data


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "uptime_seconds" in data
    assert data["active_schemes_loaded"] >= 8


def test_schemes_catalog_ru():
    response = client.get("/api/v1/schemes?lang=ru")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 8
    assert any(s["id"] == "safe_account" for s in data["schemes"])


def test_schemes_catalog_kz():
    response = client.get("/api/v1/schemes?lang=kz")
    assert response.status_code == 200
    data = response.json()
    assert any("Қауіпсіз" in s["name"] for s in data["schemes"])


def test_analyze_endpoint_risk():
    payload = {
        "text": "Здравствуйте, это служба безопасности банка. На вас оформляют кредит, срочно переведите деньги на безопасный счёт!",
        "lang": "ru"
    }
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["level"] == "risk"
    assert data["scheme"] == "safe_account"
    assert data["score"] >= 55
    assert len(data["triggers"]) > 0
    assert len(data["recommendations"]) > 0
    assert data["processing_time_ms"] >= 0


def test_analyze_endpoint_safe():
    payload = {
        "text": "Привет, Асан! Завтра в 14:00 встречаемся в университете.",
        "lang": "ru"
    }
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["level"] == "safe"
    assert data["score"] < 25


def test_metrics_endpoint():
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["total_benchmark_cases"] >= 150
    assert data["precision_pct"] >= 95.0
    assert data["recall_pct"] >= 95.0
