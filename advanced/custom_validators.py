"""
Custom Validators
=================

Base classes and examples for creating custom guardrail validators.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    is_valid: bool
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class BaseValidator(ABC):
    """Abstract base class for all validators."""
    
    @abstractmethod
    def validate(self, value: Any, **kwargs) -> ValidationResult:
        """Validate the input value."""
        pass

class RegexValidator(BaseValidator):
    """Validator that checks if input matches a regex pattern."""
    def __init__(self, pattern: str, error_msg: str = "Pattern mismatch"):
        import re
        self.pattern = re.compile(pattern)
        self.error_msg = error_msg

    def validate(self, value: str, **kwargs) -> ValidationResult:
        if self.pattern.match(value):
            return ValidationResult(is_valid=True)
        return ValidationResult(is_valid=False, error_message=self.error_msg)

class KeywordValidator(BaseValidator):
    """Validator that checks for presence/absence of keywords."""
    def __init__(self, keywords: list[str], must_contain: bool = True):
        self.keywords = keywords
        self.must_contain = must_contain

    def validate(self, value: str, **kwargs) -> ValidationResult:
        found = any(kw in value for kw in self.keywords)
        if self.must_contain and not found:
            return ValidationResult(is_valid=False, error_message=f"Must contain one of: {self.keywords}")
        if not self.must_contain and found:
            return ValidationResult(is_valid=False, error_message=f"Must not contain: {self.keywords}")
        return ValidationResult(is_valid=True)

if __name__ == "__main__":
    v1 = RegexValidator(r"^\d+$", "Must be digits")
    print(f"Digits check '123': {v1.validate('123')}")
    print(f"Digits check 'abc': {v1.validate('abc')}")

    v2 = KeywordValidator(["urgent", "asap"], must_contain=True)
    print(f"Keyword check 'please do this asap': {v2.validate('please do this asap')}")
