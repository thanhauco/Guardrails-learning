"""
Multi-Agent System with Guardrails
==================================

Simulates two agents (UserProxy and Assistant) communicating.
Guardrails enforce safety on messages exchanged between agents.
"""

import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basics.input_validation import InputValidator
from intermediate.toxic_content_detection import ToxicDetector

class Agent:
    def __init__(self, name: str):
        self.name = name
        self.inbox = []

    def send(self, message: str, recipient: 'Agent'):
        print(f"{self.name} -> {recipient.name}: {message}")
        recipient.receive(message)

    def receive(self, message: str):
        self.inbox.append(message)

class GuardedAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name)
        self.validator = InputValidator(max_length=100)
        self.toxic_detector = ToxicDetector()

    def send(self, message: str, recipient: 'Agent'):
        # Outgoing guardrail
        if self.toxic_detector.check(message).value == "toxic":
            print(f"[Guard] Blocked toxic message from {self.name}")
            return
        super().send(message, recipient)

    def receive(self, message: str):
        # Incoming guardrail
        val_res = self.validator.validate(message)
        if val_res.status.value == "invalid":
            print(f"[Guard] {self.name} rejected message: {val_res.message}")
            return
        super().receive(message)

def run_simulation():
    user = GuardedAgent("User")
    bot = GuardedAgent("Bot")

    print("--- Interaction 1: Safe ---")
    user.send("Hello bot, how are you?", bot)
    bot.send("I am doing well, thank you.", user)

    print("\n--- Interaction 2: Toxic Outgoing ---")
    user.send("You are a stupid bot!", bot)  # Should be blocked by User's guard

    print("\n--- Interaction 3: Invalid Incoming ---")
    # Bypass user send guard to test bot receive guard
    long_msg = "A" * 150
    print(f"User -> Bot: [Long Message {len(long_msg)} chars]")
    bot.receive(long_msg) # Should be rejected by Bot's guard

if __name__ == "__main__":
    run_simulation()
