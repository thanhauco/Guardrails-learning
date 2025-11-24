# Output Validation Guardrails
"""
Utilities for validating LLM outputs.
Checks include:
- Length constraints
- JSON schema compliance
- Forbidden content detection
- Optional sanitization
"""

import json
import re
from enum import Enum
from typing import Any, Dict, List, Optional

class OutputStatus(Enum):
    VALID = "valid"
    INVALID = "invalid"
    SANITIZED = "sanitized"

class OutputResponse:
    def __init__(self, status: OutputStatus, message: str, sanitized_output: Optional[str] = None, errors: Optional[List[str]] = None):
        self.status = status
        self.message = message
        self.sanitized_output = sanitized_output
        self.errors = errors or []
    def __repr__(self):
        return f"OutputResponse(status={self.status}, message={self.message})"

class OutputValidator:
    def __init__(self, max_length: int = 2000, min_length: int = 1, json_schema: Optional[Dict[str, Any]] = None, forbidden_patterns: Optional[List[str]] = None):
        self.max_length = max_length
        self.min_length = min_length
        self.json_schema = json_schema
        self.forbidden_patterns = forbidden_patterns or []
        self.default_forbidden_patterns = [
            r"\b(?:fuck|shit|bitch|cunt)\b",
            r"\b(?:terrorist|kill|murder)\b",
        ]

    def _check_length(self, text: str) -> OutputResponse:
        if len(text) < self.min_length:
            return OutputResponse(OutputStatus.INVALID, f"Too short (min {self.min_length})", errors=[f"len={len(text)}"])
        if len(text) > self.max_length:
            return OutputResponse(OutputStatus.INVALID, f"Too long (max {self.max_length})", errors=[f"len={len(text)}"])
        return OutputResponse(OutputStatus.VALID, "Length OK")

    def _check_json(self, text: str) -> OutputResponse:
        if not self.json_schema:
            return OutputResponse(OutputStatus.VALID, "No schema required")
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            return OutputResponse(OutputStatus.INVALID, "Invalid JSON", errors=[str(e)])
        required = self.json_schema.get("required", [])
        missing = [k for k in required if k not in data]
        if missing:
            return OutputResponse(OutputStatus.INVALID, "Missing keys", errors=missing)
        return OutputResponse(OutputStatus.VALID, "JSON schema OK")

    def _check_forbidden(self, text: str) -> OutputResponse:
        patterns = self.default_forbidden_patterns + self.forbidden_patterns
        hits = []
        for pat in patterns:
            if re.search(pat, text, re.IGNORECASE):
                hits.append(pat)
        if hits:
            return OutputResponse(OutputStatus.INVALID, "Forbidden content", errors=hits)
        return OutputResponse(OutputStatus.VALID, "No forbidden content")

    def sanitize(self, text: str) -> OutputResponse:
        sanitized = text
        for pat in self.default_forbidden_patterns:
            sanitized = re.sub(pat, "***", sanitized, flags=re.IGNORECASE)
        if len(sanitized) > self.max_length:
            sanitized = sanitized[:self.max_length]
            
        if sanitized != text:
            return OutputResponse(OutputStatus.SANITIZED, "Sanitized", sanitized_output=sanitized)
        return OutputResponse(OutputStatus.VALID, "No sanitization needed", sanitized_output=text)

    def validate(self, text: str, sanitize: bool = True) -> OutputResponse:
        # Length first
        length_res = self._check_length(text)
        if length_res.status == OutputStatus.INVALID:
            return length_res
        # Forbidden content
        forbid_res = self._check_forbidden(text)
        if forbid_res.status == OutputStatus.INVALID:
            return forbid_res
        # JSON schema if needed
        json_res = self._check_json(text)
        if json_res.status == OutputStatus.INVALID:
            return json_res
        if sanitize:
            return self.sanitize(text)
        return OutputResponse(OutputStatus.VALID, "All checks passed")

# Example usage
if __name__ == "__main__":
    validator = OutputValidator(max_length=500, json_schema={"required": ["answer", "confidence"]})
    print(validator.validate('{"answer": "42", "confidence": 0.99}', sanitize=False))
    print(validator.validate('{"answer": "42"}', sanitize=False))
    print(validator.validate("This is a fuck statement"))
    print(validator.validate("a" * 600))
