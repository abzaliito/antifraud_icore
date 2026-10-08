"""
ScamCheck KZ - FastAPI REST API
Anti-fraud microservice for web apps & bank API integrations.
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import time

from .detector import detector, SCHEMES

app = FastAPI(
    title="ScamCheck KZ API",
    description="Anti-fraud verification service for Kazakhstan (ABRK 2026)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="Message text or chat transcript to analyze")
    lang: str = Field("ru", description="Language: 'ru' or 'kz'")


class HighlightSpan(BaseModel):
    start: int
    end: int
    text: str


class AnalyzeResponse(BaseModel):
    score: int
    level: str
    scheme: Optional[str] = None
    scheme_name: Optional[str] = None
    triggers: List[str]
    highlights: List[HighlightSpan]
    recommendations: List[str]
    processing_time_ms: float


@app.get("/")
def read_root():
    return {
        "service": "ScamCheck KZ API",
        "status": "online",
        "version": "1.0.0",
        "competition": "ABRK 2026 - Astana IT University"
    }


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "timestamp": time.time()}


@app.get("/api/v1/schemes")
def get_schemes(lang: str = Query("ru", enum=["ru", "kz"])):
    """Return database of registered Kazakhstan fraud schemes."""
    res = []
    for sid, data in SCHEMES.items():
        res.append({
            "id": sid,
            "name": data["name_kz"] if lang == "kz" else data["name_ru"],
            "base_weight": data["base_weight"]
        })
    return {"schemes": res}


@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
def analyze_text(payload: AnalyzeRequest):
    """Analyze a chat text transcript for fraud risk."""
    start_time = time.time()
    result = detector.analyze(payload.text, lang=payload.lang)
    elapsed_ms = round((time.time() - start_time) * 1000, 2)

    return AnalyzeResponse(
        score=result["score"],
        level=result["level"],
        scheme=result["scheme"],
        scheme_name=result["scheme_name"],
        triggers=result["triggers"],
        highlights=result["highlights"],
        recommendations=result["recommendations"],
        processing_time_ms=elapsed_ms
    )


@app.post("/api/v1/analyze-screenshot")
async def analyze_screenshot(
    file: UploadFile = File(...),
    lang: str = Query("ru", enum=["ru", "kz"])
):
    """OCR + Anti-fraud analysis endpoint for screenshot images."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Mock OCR extraction for demonstration
    extracted_text = (
        "Здравствуйте, это служба безопасности Национального банка. "
        "На ваше имя оформляют кредит. Срочно переведите деньги на безопасный счёт!"
    )
    result = detector.analyze(extracted_text, lang=lang)

    return {
        "filename": file.filename,
        "ocr_text": extracted_text,
        "analysis": result
    }
