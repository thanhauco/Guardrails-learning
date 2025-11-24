"""
Safe Chatbot Application
========================

A CLI chatbot that integrates multiple guardrails to ensure safe interactions.
"""

import sys
import os

# Add project root to path to import local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from _01_basics.input_validation import InputValidator
from _01_basics.output_validation import OutputValidator
from _02_intermediate.toxic_content_detection import ToxicDetector
from _02_intermediate.pii_detection import PIIDetector

class SafeChatbot:
    def __init__(self):
        self.input_validator = InputValidator(max_length=200)
        self.toxic_detector = ToxicDetector()
        self.pii_detector = PIIDetector()
        self.output_validator = OutputValidator(max_length=500)

    def generate_response(self, user_input: str) -> str:
        # Mock LLM response generation
        # In a real app, this would call OpenAI/Anthropic
        if "secret" in user_input.lower():
            return "I cannot tell you secrets."
        return f"You said: {user_input}"

    def chat(self):
        print("Safe Chatbot v1.0 (Type 'quit' to exit)")
        print("-" * 40)

        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ['quit', 'exit']:
                    break

                # 1. Input Guardrails
                # Length & Format
                val_res = self.input_validator.validate(user_input)
                if val_res.status.value == "invalid":
                    print(f"Bot: [Blocked] {val_res.message}")
                    continue

                # Toxicity
                if self.toxic_detector.check(user_input).value == "toxic":
                    print("Bot: [Blocked] Please be polite.")
                    continue

                # PII Redaction (optional, maybe we want to allow PII in input but redact in logs)
                # Here we just check for demo
                if self.pii_detector.check(user_input).value == "found":
                    print("Bot: [Warning] Your input contains PII.")

                # 2. Generation
                response = self.generate_response(user_input)

                # 3. Output Guardrails
                out_res = self.output_validator.validate(response)
                if out_res.status.value == "invalid":
                    print("Bot: [Error] Generated response was invalid.")
                    continue

                print(f"Bot: {response}")

            except KeyboardInterrupt:
                break
        print("\nGoodbye!")

if __name__ == "__main__":
    # Note: The imports might fail if run directly without setting PYTHONPATH
    # Run from project root: python -m 06_applications.safe_chatbot
    try:
        bot = SafeChatbot()
        bot.chat()
    except ImportError:
        print("Please run this script as a module from the project root:")
        print("python -m 06_applications.safe_chatbot")
