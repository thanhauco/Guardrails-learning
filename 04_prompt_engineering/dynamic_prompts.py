"""
Dynamic Prompts
===============

Construct prompts dynamically based on context, user history, or external data.
"""

from typing import List, Dict, Any

class DynamicPromptBuilder:
    def __init__(self, base_instruction: str):
        self.base_instruction = base_instruction
        self.context_items = []

    def add_context(self, item: str):
        self.context_items.append(item)

    def add_history(self, history: List[Dict[str, str]]):
        # Format chat history as text
        for msg in history:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            self.context_items.append(f"{role.capitalize()}: {content}")

    def build(self, user_input: str) -> str:
        prompt = f"{self.base_instruction}\n\n"
        
        if self.context_items:
            prompt += "Context:\n"
            for item in self.context_items:
                prompt += f"- {item}\n"
            prompt += "\n"
            
        prompt += f"User: {user_input}\nAssistant:"
        return prompt

if __name__ == "__main__":
    builder = DynamicPromptBuilder("You are a helpful assistant answering questions based on context.")
    
    # Add retrieved documents (RAG style)
    builder.add_context("The user is named Alice.")
    builder.add_context("Alice lives in Wonderland.")
    
    # Add conversation history
    history = [
        {"role": "user", "content": "What is my name?"},
        {"role": "assistant", "content": "Your name is Alice."}
    ]
    builder.add_history(history)
    
    final_prompt = builder.build("Where do I live?")
    print(final_prompt)
