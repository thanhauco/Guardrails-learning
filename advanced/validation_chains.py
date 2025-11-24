"""
Validation Chains
=================

Utilities to chain multiple validators together.
"""

from typing import List, Any
from .custom_validators import BaseValidator, ValidationResult

class ValidationChain:
    """
    Executes a sequence of validators.
    Can stop on first failure or collect all errors.
    """
    def __init__(self, validators: List[BaseValidator], stop_on_fail: bool = True):
        self.validators = validators
        self.stop_on_fail = stop_on_fail

    def validate(self, value: Any, **kwargs) -> List[ValidationResult]:
        results = []
        for validator in self.validators:
            result = validator.validate(value, **kwargs)
            results.append(result)
            if self.stop_on_fail and not result.is_valid:
                break
        return results

    def is_valid(self, value: Any, **kwargs) -> bool:
        results = self.validate(value, **kwargs)
        return all(r.is_valid for r in results)

if __name__ == "__main__":
    from .custom_validators import RegexValidator, KeywordValidator
    
    # Chain: Must be digits AND must not contain "666"
    chain = ValidationChain([
        RegexValidator(r"^\d+$", "Must be digits"),
        KeywordValidator(["666"], must_contain=False)
    ])

    print(f"Check '12345': {chain.is_valid('12345')}")
    print(f"Check 'abc': {chain.validate('abc')}")
    print(f"Check '123666': {chain.validate('123666')}")
