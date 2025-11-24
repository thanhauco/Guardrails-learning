"""
Chain of Thought (CoT) Prompting
================================

Utilities to encourage the model to "think step-by-step" before answering.
This often improves reasoning and adherence to guardrails.
"""

class CoTPromptWrapper:
    def __init__(self, trigger_phrase: str = "Let's think step by step."):
        self.trigger_phrase = trigger_phrase

    def wrap(self, prompt: str) -> str:
        """
        Append the CoT trigger phrase to the prompt.
        """
        return f"{prompt}\n\n{self.trigger_phrase}"

    def parse_reasoning(self, response: str) -> dict:
        """
        Attempt to separate reasoning from the final answer.
        This is a heuristic and depends on how the model structures its output.
        """
        # Simple heuristic: assume the answer comes after "Therefore," or similar
        # In practice, you might ask the model to output in a specific format like:
        # Reasoning: ...
        # Answer: ...
        
        parts = response.split("Therefore,")
        if len(parts) > 1:
            return {
                "reasoning": parts[0].strip(),
                "answer": parts[-1].strip()
            }
        return {"full_response": response}

if __name__ == "__main__":
    cot = CoTPromptWrapper()
    prompt = "If I have 3 apples and buy 2 more, then eat 1, how many do I have?"
    wrapped = cot.wrap(prompt)
    print(f"Wrapped Prompt:\n{wrapped}")
    
    # Simulated response
    response = "First I have 3 apples. Then I buy 2, so 3+2=5. Then I eat 1, so 5-1=4. Therefore, you have 4 apples."
    parsed = cot.parse_reasoning(response)
    print(f"\nParsed Response: {parsed}")
