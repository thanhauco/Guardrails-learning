"""
Context Management Guardrails
=============================

Utilities for managing context windows, token limits, and conversation history.
"""

from typing import List, Dict, Any, Optional
import tiktoken

class ContextManager:
    """
    Manages the context window for LLMs to prevent token limit errors.
    """
    def __init__(self, model_name: str = "gpt-3.5-turbo", max_tokens: int = 4096, safety_margin: int = 100):
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.safety_margin = safety_margin
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """Count tokens in a text string."""
        return len(self.encoding.encode(text))

    def count_message_tokens(self, messages: List[Dict[str, str]]) -> int:
        """Count tokens in a list of messages (simplified estimation)."""
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # Every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += self.count_tokens(value)
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens

    def trim_context(self, messages: List[Dict[str, str]], new_message: str = "") -> List[Dict[str, str]]:
        """
        Trim the message history to fit within the context window, preserving the system message if present.
        """
        available_tokens = self.max_tokens - self.safety_margin - self.count_tokens(new_message)
        if available_tokens < 0:
            raise ValueError("New message is too long for the context window.")

        current_tokens = self.count_message_tokens(messages)
        if current_tokens <= available_tokens:
            return messages

        # Preserve system message if it exists at the beginning
        system_message = None
        if messages and messages[0].get("role") == "system":
            system_message = messages[0]
            messages = messages[1:]

        # Remove oldest messages until it fits
        while messages and self.count_message_tokens([system_message] + messages if system_message else messages) > available_tokens:
            messages.pop(0)

        if system_message:
            messages.insert(0, system_message)

        return messages

if __name__ == "__main__":
    cm = ContextManager(max_tokens=100)
    msgs = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I am fine, thank you."},
        {"role": "user", "content": "Tell me a very long story about a dragon that takes up a lot of tokens."}
    ]
    print(f"Original tokens: {cm.count_message_tokens(msgs)}")
    trimmed = cm.trim_context(msgs, new_message="And then?")
    print(f"Trimmed tokens: {cm.count_message_tokens(trimmed)}")
    print(f"Trimmed messages: {trimmed}")
