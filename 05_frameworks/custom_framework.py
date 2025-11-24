"""
Custom Framework
================

A minimal, reusable guardrails framework that can be adapted for any project.
Demonstrates the core pattern: Input -> Validate -> Generate -> Validate -> Output.
"""

from typing import List, Callable, Any, Optional
from dataclasses import dataclass

@dataclass
class GuardResult:
    content: Optional[str]
    is_blocked: bool
    reason: Optional[str] = None

class SimpleGuard:
    def __init__(self, 
                 input_validators: List[Callable[[str], bool]] = None,
                 output_validators: List[Callable[[str], bool]] = None,
                 generator: Callable[[str], str] = None):
        self.input_validators = input_validators or []
        self.output_validators = output_validators or []
        self.generator = generator

    def process(self, user_input: str) -> GuardResult:
        # 1. Input Validation
        for validator in self.input_validators:
            if not validator(user_input):
                return GuardResult(None, True, "Input validation failed")

        # 2. Generation
        if not self.generator:
            return GuardResult(None, True, "No generator configured")
        
        try:
            output = self.generator(user_input)
        except Exception as e:
            return GuardResult(None, True, f"Generation error: {e}")

        # 3. Output Validation
        for validator in self.output_validators:
            if not validator(output):
                return GuardResult(None, True, "Output validation failed")

        return GuardResult(output, False)

if __name__ == "__main__":
    # Example usage
    def is_not_toxic(text):
        return "bad" not in text
    
    def mock_generator(text):
        return f"Echo: {text}"

    guard = SimpleGuard(
        input_validators=[is_not_toxic],
        output_validators=[is_not_toxic],
        generator=mock_generator
    )

    print(guard.process("Hello world"))
    print(guard.process("This is bad"))
