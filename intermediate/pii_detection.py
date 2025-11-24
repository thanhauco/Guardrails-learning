"""
PII Detection Guardrails
=========================

Detects personal identifiable information (PII) such as email addresses, phone numbers, SSNs.
"""

import re
from enum import Enum

class PIIResult(Enum):
    CLEAN = "clean"
    FOUND = "found"

class PIIDetector:
    def __init__(self):
        self.patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
            "phone": r"\\b\\d{3}[-.]?\\d{3}[-.]?\\d{4}\\b",
            "ssn": r"\\b\\d{3}-\\d{2}-\\d{4}\\b",
        }
    def check(self, text: str) -> PIIResult:
        for name, pat in self.patterns.items():
            if re.search(pat, text):
                return PIIResult.FOUND
        return PIIResult.CLEAN
    def redact(self, text: str) -> str:
        redacted = text
        for name, pat in self.patterns.items():
            redacted = re.sub(pat, f"<REDACTED_{name.upper()}>", redacted)
        return redacted

if __name__ == "__main__":
    detector = PIIDetector()
    examples = [
        "Contact me at john.doe@example.com.",
        "My phone is 555-123-4567.",
        "No PII here.",
    ]
    for ex in examples:
        print(detector.check(ex).value, detector.redact(ex))
