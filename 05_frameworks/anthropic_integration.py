"""
Anthropic Integration
=====================

Wrapper around Anthropic API to apply guardrails.
"""

import os
try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

class GuardedAnthropic:
    def __init__(self, api_key: str = None):
        if Anthropic:
            self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        else:
            self.client = None
            print("Anthropic library not installed.")

    def generate(self, prompt: str, validators: list = None, **kwargs):
        if not self.client:
            return "Anthropic client not initialized."

        # 1. Input Validation
        print(">> Validating input prompt...")

        # 2. Call API
        message = self.client.messages.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            **kwargs
        )
        content = message.content[0].text

        # 3. Output Validation
        print(">> Validating output...")
        if validators:
            for validator in validators:
                # Mock validation interface
                if not validator(content):
                    return "[BLOCKED] Output validation failed."
        
        return content

if __name__ == "__main__":
    if Anthropic:
        print("Anthropic wrapper ready. Set ANTHROPIC_API_KEY to run.")
    else:
        print("Please install anthropic to run this example.")
