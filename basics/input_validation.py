"""
Input Validation Guardrails
============================

This module demonstrates basic input validation techniques to ensure
user inputs are safe, valid, and within acceptable parameters.

Key Concepts:
- Length validation
- Format validation
- Content sanitization
- Type checking
- Encoding validation
"""

import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ValidationResult(Enum):
    """Enumeration of validation results"""
    VALID = "valid"
    INVALID = "invalid"
    SANITIZED = "sanitized"


@dataclass
class ValidationResponse:
    """Response object for validation results"""
    status: ValidationResult
    message: str
    sanitized_input: Optional[str] = None
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class InputValidator:
    """
    Basic input validator with multiple validation strategies.
    
    This class provides foundational input validation that should be
    applied to all user inputs before processing by an LLM.
    """
    
    def __init__(
        self,
        max_length: int = 1000,
        min_length: int = 1,
        allowed_chars: Optional[str] = None,
        forbidden_patterns: Optional[List[str]] = None
    ):
        """
        Initialize the input validator.
        
        Args:
            max_length: Maximum allowed input length
            min_length: Minimum required input length
            allowed_chars: Regex pattern of allowed characters
            forbidden_patterns: List of forbidden regex patterns
        """
        self.max_length = max_length
        self.min_length = min_length
        self.allowed_chars = allowed_chars
        self.forbidden_patterns = forbidden_patterns or []
        
        # Default forbidden patterns (common injection attempts)
        self.default_forbidden_patterns = [
            r'<script.*?>.*?</script>',  # Script tags
            r'javascript:',               # JavaScript protocol
            r'on\w+\s*=',                # Event handlers
            r'eval\s*\(',                # Eval function
            r'exec\s*\(',                # Exec function
        ]
    
    def validate_length(self, text: str) -> ValidationResponse:
        """
        Validate input length.
        
        Args:
            text: Input text to validate
            
        Returns:
            ValidationResponse with validation result
        """
        if len(text) < self.min_length:
            return ValidationResponse(
                status=ValidationResult.INVALID,
                message=f"Input too short. Minimum length: {self.min_length}",
                errors=[f"Length {len(text)} < {self.min_length}"]
            )
        
        if len(text) > self.max_length:
            return ValidationResponse(
                status=ValidationResult.INVALID,
                message=f"Input too long. Maximum length: {self.max_length}",
                errors=[f"Length {len(text)} > {self.max_length}"]
            )
        
        return ValidationResponse(
            status=ValidationResult.VALID,
            message="Length validation passed"
        )
    
    def validate_format(self, text: str) -> ValidationResponse:
        """
        Validate input format against allowed characters.
        
        Args:
            text: Input text to validate
            
        Returns:
            ValidationResponse with validation result
        """
        if self.allowed_chars is None:
            return ValidationResponse(
                status=ValidationResult.VALID,
                message="No format restrictions"
            )
        
        if not re.match(self.allowed_chars, text):
            return ValidationResponse(
                status=ValidationResult.INVALID,
                message="Input contains invalid characters",
                errors=["Format validation failed"]
            )
        
        return ValidationResponse(
            status=ValidationResult.VALID,
            message="Format validation passed"
        )
    
    def check_forbidden_patterns(self, text: str) -> ValidationResponse:
        """
        Check for forbidden patterns in input.
        
        Args:
            text: Input text to check
            
        Returns:
            ValidationResponse with validation result
        """
        all_patterns = self.default_forbidden_patterns + self.forbidden_patterns
        errors = []
        
        for pattern in all_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                errors.append(f"Forbidden pattern detected: {pattern}")
        
        if errors:
            return ValidationResponse(
                status=ValidationResult.INVALID,
                message="Input contains forbidden patterns",
                errors=errors
            )
        
        return ValidationResponse(
            status=ValidationResult.VALID,
            message="No forbidden patterns detected"
        )
    
    def sanitize_input(self, text: str) -> ValidationResponse:
        """
        Sanitize input by removing potentially dangerous content.
        
        Args:
            text: Input text to sanitize
            
        Returns:
            ValidationResponse with sanitized input
        """
        sanitized = text
        
        # Remove script content first (before tags are stripped)
        sanitized = re.sub(r'<script.*?</script>', '', sanitized, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove event handlers
        sanitized = re.sub(r'on\w+\s*=\s*["\'].*?["\']', '', sanitized, flags=re.IGNORECASE)
        
        # Remove remaining HTML tags
        sanitized = re.sub(r'<[^>]+>', '', sanitized)
        
        # Normalize whitespace
        sanitized = ' '.join(sanitized.split())
        
        # Trim
        sanitized = sanitized.strip()
        
        if sanitized != text:
            return ValidationResponse(
                status=ValidationResult.SANITIZED,
                message="Input was sanitized",
                sanitized_input=sanitized
            )
        
        return ValidationResponse(
            status=ValidationResult.VALID,
            message="No sanitization needed",
            sanitized_input=sanitized
        )
    
    def validate(self, text: str, sanitize: bool = True) -> ValidationResponse:
        """
        Perform complete validation on input.
        
        Args:
            text: Input text to validate
            sanitize: Whether to sanitize the input
            
        Returns:
            ValidationResponse with final validation result
        """
        # Check if input is None or empty
        if text is None:
            return ValidationResponse(ValidationResult.INVALID, "Input cannot be None", errors=["None input"])
            
        is_sanitized = False
        if sanitize:
            san_res = self.sanitize_input(text)
            if san_res.status == ValidationResult.SANITIZED:
                is_sanitized = True
            text = san_res.sanitized_input or text
            
        length_res = self.validate_length(text)
        if length_res.status == ValidationResult.INVALID:
            return length_res
            
        format_res = self.validate_format(text)
        if format_res.status == ValidationResult.INVALID:
            return format_res
            
        forbidden_res = self.check_forbidden_patterns(text)
        if forbidden_res.status == ValidationResult.INVALID:
            return forbidden_res
            
        status = ValidationResult.SANITIZED if is_sanitized else ValidationResult.VALID
        msg = "Input sanitized" if is_sanitized else "All checks passed"
        return ValidationResponse(status, msg, sanitized_input=text)


class EmailValidator(InputValidator):
    """Specialized validator for email inputs"""
    
    def __init__(self):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        super().__init__(
            max_length=254,  # RFC 5321
            min_length=3,
            allowed_chars=email_pattern
        )


class URLValidator(InputValidator):
    """Specialized validator for URL inputs"""
    
    def __init__(self):
        # Basic URL pattern
        url_pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
        super().__init__(
            max_length=2048,
            min_length=10,
            allowed_chars=url_pattern,
            forbidden_patterns=[
                r'javascript:',
                r'data:',
                r'file:',
            ]
        )


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_basic_validation():
    """Example: Basic input validation"""
    print("=" * 60)
    print("Example 1: Basic Input Validation")
    print("=" * 60)
    
    validator = InputValidator(max_length=100, min_length=5)
    
    # Test cases
    test_inputs = [
        "Hello, how are you?",
        "Hi",  # Too short
        "A" * 150,  # Too long
        "<script>alert('xss')</script>",  # Malicious
        "Normal text with some numbers 123",
    ]
    
    for text in test_inputs:
        result = validator.validate(text)
        print(f"\nInput: {text[:50]}...")
        print(f"Status: {result.status.value}")
        print(f"Message: {result.message}")
        if result.sanitized_input and result.sanitized_input != text:
            print(f"Sanitized: {result.sanitized_input}")
        if result.errors:
            print(f"Errors: {', '.join(result.errors)}")


def example_email_validation():
    """Example: Email validation"""
    print("\n" + "=" * 60)
    print("Example 2: Email Validation")
    print("=" * 60)
    
    validator = EmailValidator()
    
    test_emails = [
        "user@example.com",
        "invalid.email",
        "test@domain",
        "valid.email+tag@example.co.uk",
    ]
    
    for email in test_emails:
        result = validator.validate(email, sanitize=False)
        print(f"\nEmail: {email}")
        print(f"Valid: {result.status == ValidationResult.VALID}")


def example_url_validation():
    """Example: URL validation"""
    print("\n" + "=" * 60)
    print("Example 3: URL Validation")
    print("=" * 60)
    
    validator = URLValidator()
    
    test_urls = [
        "https://www.example.com",
        "http://example.com/path?query=value",
        "javascript:alert('xss')",  # Malicious
        "ftp://example.com",  # Wrong protocol
    ]
    
    for url in test_urls:
        result = validator.validate(url, sanitize=False)
        print(f"\nURL: {url}")
        print(f"Valid: {result.status == ValidationResult.VALID}")
        if result.errors:
            print(f"Errors: {', '.join(result.errors)}")


def example_custom_validation():
    """Example: Custom validation rules"""
    print("\n" + "=" * 60)
    print("Example 4: Custom Validation Rules")
    print("=" * 60)
    
    # Create validator that only allows alphanumeric and spaces
    validator = InputValidator(
        max_length=200,
        min_length=1,
        allowed_chars=r'^[a-zA-Z0-9\s]+$',
        forbidden_patterns=[
            r'\b(password|secret|api[_-]?key)\b',  # Sensitive keywords
        ]
    )
    
    test_inputs = [
        "This is a valid input 123",
        "Invalid! Has special chars #$%",
        "Contains password keyword",
        "My api_key is secret",
    ]
    
    for text in test_inputs:
        result = validator.validate(text, sanitize=False)
        print(f"\nInput: {text}")
        print(f"Status: {result.status.value}")
        print(f"Message: {result.message}")


if __name__ == "__main__":
    # Run all examples
    example_basic_validation()
    example_email_validation()
    example_url_validation()
    example_custom_validation()
    
    print("\n" + "=" * 60)
    print("✅ Input validation examples completed!")
    print("=" * 60)
