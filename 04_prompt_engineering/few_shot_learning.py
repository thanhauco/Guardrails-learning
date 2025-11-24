"""
Few-Shot Learning
=================

Helper classes to construct few-shot prompts, which improve model performance
and adherence to constraints by providing examples.
"""

from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Example:
    input: str
    output: str

class FewShotPromptBuilder:
    def __init__(self, instruction: str, examples: List[Example]):
        self.instruction = instruction
        self.examples = examples

    def build(self, new_input: str) -> str:
        prompt = f"{self.instruction}\n\n"
        for ex in self.examples:
            prompt += f"Input: {ex.input}\nOutput: {ex.output}\n\n"
        prompt += f"Input: {new_input}\nOutput:"
        return prompt

if __name__ == "__main__":
    # Example: Sentiment Analysis
    instruction = "Classify the sentiment of the following texts as Positive, Negative, or Neutral."
    examples = [
        Example("I love this product!", "Positive"),
        Example("This is the worst service ever.", "Negative"),
        Example("I ordered a book.", "Neutral")
    ]
    
    builder = FewShotPromptBuilder(instruction, examples)
    new_input = "The movie was okay, not great but not bad."
    print(builder.build(new_input))
