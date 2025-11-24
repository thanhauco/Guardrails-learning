"""
Hallucination Detection Guardrails
==================================

Techniques to detect potential hallucinations by comparing output against
source documents or knowledge base.
"""

from typing import List
try:
    from sentence_transformers import CrossEncoder
except ImportError:
    CrossEncoder = None

class HallucinationDetector:
    """
    Uses a Natural Language Inference (NLI) model to check if the output
    is entailed by the provided context/source.
    """
    def __init__(self, model_name: str = 'cross-encoder/nli-deberta-v3-base'):
        if CrossEncoder:
            self.model = CrossEncoder(model_name)
            # Label mapping for this specific model: 0: contradiction, 1: entailment, 2: neutral
            # Note: mappings can vary by model!
            self.label_mapping = ['contradiction', 'entailment', 'neutral']
        else:
            self.model = None
            print("Warning: sentence-transformers not installed.")

    def check_entailment(self, premise: str, hypothesis: str) -> str:
        """
        Check relationship between premise (source) and hypothesis (output).
        Returns: 'entailment', 'contradiction', or 'neutral'
        """
        if not self.model:
            return "unknown"
        
        scores = self.model.predict([(premise, hypothesis)])
        label_index = scores[0].argmax()
        return self.label_mapping[label_index]

    def is_hallucination(self, source: str, output: str) -> bool:
        """
        Returns True if output contradicts the source.
        Note: 'neutral' might also be considered hallucination depending on strictness.
        """
        result = self.check_entailment(source, output)
        return result == 'contradiction'

if __name__ == "__main__":
    if CrossEncoder:
        detector = HallucinationDetector()
        source = "The Apollo 11 mission landed on the Moon in 1969. Neil Armstrong was the first man to walk on the surface."
        
        outputs = [
            "Neil Armstrong walked on the moon in 1969.", # Entailment
            "The Apollo 11 mission landed on Mars.",       # Contradiction
            "Neil Armstrong liked to eat cheese."          # Neutral (not in source)
        ]
        
        print(f"Source: {source}\n")
        for out in outputs:
            rel = detector.check_entailment(source, out)
            print(f"Output: {out}")
            print(f"Relationship: {rel}")
            print(f"Is Hallucination (Contradiction)? {detector.is_hallucination(source, out)}\n")
    else:
        print("Please install sentence-transformers to run this example.")
