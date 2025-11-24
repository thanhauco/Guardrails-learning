# Content Filtering Guardrails
"""
Basic content filtering utilities to detect and block toxic or prohibited language.
"""

import re
from enum import Enum
from typing import List, Optional

class FilterResult(Enum):
    CLEAN = "clean"
    BLOCKED = "blocked"

class ContentFilter:
    """Simple keyword‑based content filter.
    
    The filter uses a list of regular‑expression patterns to identify
    disallowed content such as profanity, hate speech, or personal data.
    """
    def __init__(self, custom_patterns: Optional[List[str]] = None):
        # Default patterns for profanity and hate speech
        self.default_patterns = [
            r"\b(?:fuck|shit|bitch|cunt)\b",
            r"\b(?:terrorist|kill|murder|rape)\b",
        ]
        self.patterns = self.default_patterns + (custom_patterns or [])

    def check(self, text: str) -> FilterResult:
        """Return ``BLOCKED`` if any pattern matches, otherwise ``CLEAN``."""
        for pat in self.patterns:
            if re.search(pat, text, re.IGNORECASE):
                return FilterResult.BLOCKED
        return FilterResult.CLEAN

    def filter(self, text: str) -> str:
        """Replace matched content with asterisks.
        
        This method is useful when you want to keep the text but mask
        the offending parts.
        """
        sanitized = text
        for pat in self.patterns:
            sanitized = re.sub(pat, "***", sanitized, flags=re.IGNORECASE)
        return sanitized

# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cf = ContentFilter()
    examples = [
        "This is a clean sentence.",
        "You are a fucker!",
        "We must stop terrorist activities.",
    ]
    for ex in examples:
        result = cf.check(ex)
        print(f"Input: {ex}\nResult: {result.value}\nSanitized: {cf.filter(ex)}\n")
