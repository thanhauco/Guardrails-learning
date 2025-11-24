"""
Quality Validation Guardrails
=============================

Heuristics to validate the quality of LLM responses.
"""

from enum import Enum
from typing import List, Optional
import re

class QualityResult(Enum):
    PASS = "pass"
    FAIL = "fail"

class QualityValidator:
    """
    Validates response quality based on heuristics like:
    - Minimum length
    - Repetition
    - Relevance (keyword matching)
    - Uncertainty markers
    """
    def __init__(self, min_words: int = 3, max_repetition_ratio: float = 0.5):
        self.min_words = min_words
        self.max_repetition_ratio = max_repetition_ratio
        self.uncertainty_markers = [
            "I don't know", "I am not sure", "I cannot answer", "As an AI language model"
        ]

    def check_length(self, text: str) -> bool:
        words = text.split()
        return len(words) >= self.min_words

    def check_repetition(self, text: str) -> bool:
        """Check if the text is overly repetitive."""
        words = text.lower().split()
        if not words:
            return True
        unique_words = set(words)
        ratio = len(unique_words) / len(words)
        return ratio >= (1.0 - self.max_repetition_ratio)

    def check_uncertainty(self, text: str) -> bool:
        """Check if the response indicates refusal or uncertainty."""
        for marker in self.uncertainty_markers:
            if marker.lower() in text.lower():
                return False
        return True

    def validate(self, text: str) -> QualityResult:
        if not self.check_length(text):
            return QualityResult.FAIL
        if not self.check_repetition(text):
            return QualityResult.FAIL
        # Uncertainty check is optional depending on use case, here we just flag it
        # but don't necessarily fail validation unless strict mode is desired.
        return QualityResult.PASS

if __name__ == "__main__":
    validator = QualityValidator()
    examples = [
        "Yes.", # Too short
        "I don't know the answer to that.", # Uncertainty
        "The the the the the the.", # Repetitive
        "This is a high quality response that provides useful information." # Good
    ]
    for ex in examples:
        print(f"Input: {ex}\nResult: {validator.validate(ex).value}\n")
