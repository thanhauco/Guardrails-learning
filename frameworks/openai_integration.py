"""
OpenAI Integration
==================

Wrapper around OpenAI API to apply guardrails before and after calls.
"""

import os
from typing import List, Dict, Any

# Mock import if openai not installed
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class GuardedOpenAI:
    def __init__(self, api_key: str = None):
        if OpenAI:
            self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        else:
            self.client = None
            print("OpenAI library not installed.")

    def chat_completion(self, messages: List[Dict[str, str]], validators: List[Any] = None, **kwargs):
        if not self.client:
            return "OpenAI client not initialized."

        # 1. Input Validation (Pre-flight)
        # Here you would iterate through input validators
        print(">> Validating inputs...")
        
        # 2. Call API
        response = self.client.chat.completions.create(
            messages=messages,
            **kwargs
        )
        content = response.choices[0].message.content

        # 3. Output Validation (Post-flight)
        print(">> Validating output...")
        if validators:
            for validator in validators:
                # Assuming validator has a .validate(text) method
                res = validator.validate(content)
                if hasattr(res, 'is_valid') and not res.is_valid:
                    print(f"Validation failed: {res.message}")
                    # Handle failure (retry, fix, raise)
                    return f"[BLOCKED] {res.message}"
        
        return content

if __name__ == "__main__":
    # Mock validator for demonstration
    class MockValidator:
        def validate(self, text):
            class Result:
                is_valid = "forbidden" not in text
                message = "Contains forbidden content"
            return Result()

    if OpenAI:
        # Only runs if you have an API key set
        try:
            wrapper = GuardedOpenAI()
            msgs = [{"role": "user", "content": "Say something forbidden."}]
            
            # This will likely fail without a real key, but shows the structure
            # output = wrapper.chat_completion(msgs, validators=[MockValidator()], model="gpt-3.5-turbo")
            # print(output)
            print("OpenAI wrapper initialized. Set OPENAI_API_KEY to run real calls.")
        except Exception as e:
            print(f"Setup error: {e}")
    else:
        print("Please install openai to run this example.")
