"""
Production Ready Example (FastAPI)
==================================

Skeleton of a production-ready API service using FastAPI and guardrails.
Requires: pip install fastapi uvicorn
"""

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
except ImportError:
    FastAPI = None

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basics.input_validation import InputValidator
from intermediate.pii_detection import PIIDetector

if FastAPI:
    app = FastAPI(title="Guarded LLM API")
    
    # Initialize validators once
    input_validator = InputValidator(max_length=1000)
    pii_detector = PIIDetector()

    class GenerateRequest(BaseModel):
        prompt: str
        max_tokens: int = 100

    class GenerateResponse(BaseModel):
        text: str
        status: str

    @app.post("/generate", response_model=GenerateResponse)
    async def generate(request: GenerateRequest):
        # 1. Input Validation
        val_res = input_validator.validate(request.prompt)
        if val_res.status.value == "invalid":
            raise HTTPException(status_code=400, detail=val_res.message)

        # 2. PII Check
        if pii_detector.check(request.prompt).value == "found":
            # Policy: Redact PII before processing
            request.prompt = pii_detector.redact(request.prompt)

        # 3. Mock Generation
        generated_text = f"Processed: {request.prompt}"

        return GenerateResponse(text=generated_text, status="success")

    def run():
        import uvicorn
        print("Starting server on http://localhost:8000")
        uvicorn.run(app, host="0.0.0.0", port=8000)

else:
    def run():
        print("FastAPI not installed. Run: pip install fastapi uvicorn")

if __name__ == "__main__":
    run()
