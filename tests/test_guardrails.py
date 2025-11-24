import pytest
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basics.input_validation import InputValidator, ValidationResult
from basics.output_validation import OutputValidator, OutputStatus
from intermediate.toxic_content_detection import ToxicDetector, ToxicResult

class TestInputValidator:
    def test_length_validation(self):
        validator = InputValidator(min_length=5, max_length=10)
        assert validator.validate("Hi").status == ValidationResult.INVALID
        assert validator.validate("Hello").status == ValidationResult.VALID
        assert validator.validate("Hello World").status == ValidationResult.INVALID

    def test_sanitization(self):
        validator = InputValidator()
        input_text = "<script>alert('x')</script>Hello"
        result = validator.validate(input_text)
        assert result.sanitized_input == "Hello"
        assert result.status == ValidationResult.SANITIZED

class TestOutputValidator:
    def test_forbidden_content(self):
        validator = OutputValidator()
        # Assuming default forbidden patterns include profanity
        res = validator.validate("This is shit")
        assert res.status == OutputStatus.INVALID

    def test_json_validation(self):
        validator = OutputValidator(json_schema={"required": ["id"]})
        assert validator.validate('{"id": 1}').status == OutputStatus.VALID
        assert validator.validate('{"name": "test"}').status == OutputStatus.INVALID

class TestToxicDetector:
    def test_toxic_content(self):
        detector = ToxicDetector()
        assert detector.check("You are a wonderful person").value == "clean"
        assert detector.check("I hate you").value == "toxic"

    def test_sanitization(self):
        detector = ToxicDetector()
        sanitized = detector.sanitize("You are a bitch")
        assert "***" in sanitized
