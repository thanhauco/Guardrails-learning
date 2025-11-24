"""
Bias Detection Guardrails
=========================

Detects potential biases in generated text related to gender, race, religion, etc.
"""

import re
from typing import List, Dict

class BiasDetector:
    """
    Simple keyword-based bias detector.
    In a real application, use a trained classifier or specific bias-detection models.
    """
    def __init__(self):
        self.bias_terms = {
            "gender": [
                "man works", "woman cooks", "he is a doctor", "she is a nurse",
                "man is strong", "woman is weak"
            ],
            "religion": [
                "radical", "extremist", "cult"
            ],
            # Add more categories and terms
        }
        
    def check_bias(self, text: str) -> Dict[str, List[str]]:
        """
        Check for presence of potentially biased phrases.
        Returns a dict of category -> found terms.
        """
        found_biases = {}
        text_lower = text.lower()
        
        for category, terms in self.bias_terms.items():
            found = []
            for term in terms:
                if term in text_lower:
                    found.append(term)
            if found:
                found_biases[category] = found
                
        return found_biases

if __name__ == "__main__":
    detector = BiasDetector()
    examples = [
        "The doctor asked the nurse for the chart. He was in a hurry.", # Implicit bias potentially
        "She is a nurse and he is a doctor.", # Matches keyword
        "Everyone should be treated equally."
    ]
    
    for ex in examples:
        biases = detector.check_bias(ex)
        print(f"Input: {ex}")
        if biases:
            print(f"Potential Biases Detected: {biases}")
        else:
            print("No obvious bias keywords found.")
        print("-" * 20)
