"""
RAG with Validation
===================

Retrieval-Augmented Generation (RAG) example with guardrails.
Ensures that retrieved context is relevant and output is grounded (not hallucinated).
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from advanced.hallucination_detection import HallucinationDetector
from advanced.semantic_validation import SemanticValidator

class SimpleRAG:
    def __init__(self):
        # Mock knowledge base
        self.knowledge_base = {
            "python": "Python is a high-level, general-purpose programming language.",
            "rust": "Rust is a multi-paradigm, general-purpose programming language designed for performance and safety.",
        }
        
        # Initialize guardrails (fail gracefully if deps missing)
        try:
            self.hallucination_detector = HallucinationDetector()
            self.semantic_validator = SemanticValidator()
        except:
            self.hallucination_detector = None
            self.semantic_validator = None
            print("Warning: Advanced guardrails not available (missing dependencies).")

    def retrieve(self, query: str) -> str:
        # Simple keyword retrieval
        for key, content in self.knowledge_base.items():
            if key in query.lower():
                return content
        return ""

    def generate(self, query: str, context: str) -> str:
        # Mock LLM generation
        if not context:
            return "I don't know about that."
        return f"Based on the context: {context}"

    def query(self, user_query: str) -> str:
        print(f"Query: {user_query}")
        
        # 1. Retrieve
        context = self.retrieve(user_query)
        if not context:
            return "No relevant information found."
        print(f"Retrieved Context: {context}")

        # 2. Generate
        response = self.generate(user_query, context)
        print(f"Generated Response: {response}")

        # 3. Validate (Hallucination Check)
        if self.hallucination_detector:
            # Check if response contradicts context
            is_hallucination = self.hallucination_detector.is_hallucination(context, response)
            if is_hallucination:
                return "[Blocked] Detected hallucination/contradiction."
        
        return response

if __name__ == "__main__":
    rag = SimpleRAG()
    print("\n--- Test 1: Valid Query ---")
    print(f"Final Answer: {rag.query('Tell me about python')}")
    
    print("\n--- Test 2: Unknown Topic ---")
    print(f"Final Answer: {rag.query('Tell me about java')}")
