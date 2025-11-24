# Error Handling Guardrails
"""
Utility functions for consistent error handling across guardrails modules.
Provides a custom exception hierarchy and helper to format error messages.
"""

class GuardrailError(Exception):
    """Base class for all guardrail‑related errors."""
    pass

class ValidationError(GuardrailError):
    """Raised when input or output validation fails."""
    def __init__(self, message: str, errors: list | None = None):
        super().__init__(message)
        self.errors = errors or []

class RateLimitError(GuardrailError):
    """Raised when a rate‑limit is exceeded."""
    pass

def format_error(err: GuardrailError) -> str:
    """Return a human‑readable string for the given guardrail error."""
    if isinstance(err, ValidationError):
        details = ", ".join(err.errors) if err.errors else ""
        return f"ValidationError: {err} ({details})"
    return f"{err.__class__.__name__}: {err}"

# Example usage
if __name__ == "__main__":
    try:
        raise ValidationError("Invalid input", ["length too short", "forbidden pattern"])
    except GuardrailError as e:
        print(format_error(e))
