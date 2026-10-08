"""
Composition Root & FastAPI Adapter
Exposes clean REST API endpoints powered by domain use cases.
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import time

from domain.value_objects import Language
from use_cases.analyze_fraud import AnalyzeFraudUseCase
from infrastructure.rule_repository import InMemoryRuleRepository

app = FastAPI(
    title="ScamCheck KZ API",
    description="Clean Architecture Anti-Fraud Microservice (ABRK 2026 Contest)",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency Injection / Composition Root
rule_repository = InMemoryRuleRepository()
analyze_use_case = AnalyzeFraudUseCase(repository=rule_repository)


class AnalyzeDTO(BaseModel):
    text: str = Field(..., description="Chat transcript to evaluate")
    lang: str = Field("ru", description="Language code: 'ru' or 'kz'")


class HighlightDTO(BaseModel):
    start: int
    end: int
    text: str


class ResponseDTO(BaseModel):
    score: int
    level: str
    scheme: Optional[str] = None
    scheme_name: Optional[str] = None
    triggers: List[str]
    highlights: List[HighlightDTO]
    recommendations: List[str]
    processing_time_ms: float


@app.get("/")
def get_service_info():
    return {
        "service": "ScamCheck KZ Anti-Fraud Engine",
        "architecture": "Uncle Bob Clean Architecture",
        "version": "2.0.0",
        "competition": "ABRK 2026 - Astana IT University"
    }


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "timestamp": time.time()}


@app.get("/api/v1/schemes")
def get_schemes(lang: str = Query("ru", enum=["ru", "kz"])):
    lang_enum = Language.KAZAKH if lang == "kz" else Language.RUSSIAN
    schemes = rule_repository.get_all_schemes()
    return {
        "schemes": [
            {
                "id": s.id,
                "name": s.get_name(lang_enum),
                "base_weight": s.base_weight
            }
            for s in schemes
        ]
    }


@app.post("/api/v1/analyze", response_model=ResponseDTO)
def analyze(payload: AnalyzeDTO):
    start = time.time()
    result = analyze_use_case.execute(payload.text, lang_code=payload.lang)
    elapsed = round((time.time() - start) * 1000, 2)

    lang_enum = Language.KAZAKH if payload.lang == "kz" else Language.RUSSIAN

    return ResponseDTO(
        score=result.score,
        level=result.level.value,
        scheme=result.scheme.id if result.scheme else None,
        scheme_name=result.scheme.get_name(lang_enum) if result.scheme else None,
        triggers=result.triggers,
        highlights=[
            HighlightDTO(start=h.start, end=h.end, text=h.matched_text)
            for h in result.highlights
        ],
        recommendations=result.recommendations,
        processing_time_ms=elapsed
    )
