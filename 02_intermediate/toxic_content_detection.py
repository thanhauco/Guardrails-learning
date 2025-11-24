"""
Toxic Content Detection Guardrails
===================================

Detects toxic or hateful language using a simple keyword list.
In production you would replace this with a model‑based classifier.
"""

import re
from enum import Enum

class ToxicResult(Enum):
    CLEAN = "clean"
    TOXIC = "toxic"

class ToxicDetector:
    def __init__(self, custom_patterns=None):
        # Basic list of toxic words/phrases (extend as needed)
        self.default_patterns = [
            r"\b(?:fuck|shit|bitch|cunt)\b",
            r"\b(?:kill|murder|rape|terrorist)\b",
            r"\b(?:hate|racist|bigot)\b",
        ]
        self.patterns = self.default_patterns + (custom_patterns or [])

    def check(self, text: str) -> ToxicResult:
        for pat in self.patterns:
            if re.search(pat, text, re.IGNORECASE):
                return ToxicResult.TOXIC
        return ToxicResult.CLEAN

    def sanitize(self, text: str) -> str:
        sanitized = text
        for pat in self.patterns:
            sanitized = re.sub(pat, "***", sanitized, flags=re.IGNORECASE)
        return sanitized

if __name__ == "__main__":
    detector = ToxicDetector()
    examples = [
        "You are a wonderful person.",
        "I hate you, you are a bitch.",
        "Let's discuss politics.",
    ]
    for ex in examples:
        print(f"Input: {ex}\nResult: {detector.check(ex).value}\nSanitized: {detector.sanitize(ex)}\n")
