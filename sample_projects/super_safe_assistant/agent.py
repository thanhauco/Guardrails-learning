"""
Safe Agent
==========
The core agent logic that uses the pipeline and simulates RAG + Generation.
"""

import time
from typing import List, Dict
from .config import Config
from .pipeline import GuardPipeline

class SafeAgent:
    def __init__(self):
        self.pipeline = GuardPipeline()
        self.history: List[Dict[str, str]] = []
        
    def retrieve_context(self, query: str) -> str:
        """Simulate RAG retrieval."""
        # Simple keyword matching against config knowledge base
        relevant_docs = []
        for key, content in Config.KNOWLEDGE_BASE.items():
            if key in query.lower():
                relevant_docs.append(content)
        
        if not relevant_docs:
            return ""
        return "\n".join(relevant_docs)

    def generate_response(self, query: str, context: str) -> str:
        """Simulate LLM generation."""
        # In a real app, this calls OpenAI/Anthropic
        
        if not context:
            return "I apologize, but I don't have information about that topic in my knowledge base."
            
        # Mock generation based on context
        # We'll just return a templated string for the demo
        return f"Based on our policy: {context}"

    def chat(self, user_input: str) -> str:
        """Process a user message through the full pipeline."""
        
        # 1. Input Guardrails
        input_res = self.pipeline.validate_input(user_input)
        if input_res.is_blocked:
            return f"[BLOCKED] {input_res.reason}"
        
        clean_query = input_res.text
        
        # 2. Retrieval (RAG)
        context = self.retrieve_context(clean_query)
        
        # 3. Generation
        raw_response = self.generate_response(clean_query, context)
        
        # 4. Output Guardrails
        output_res = self.pipeline.validate_output(raw_response, context=context, query=clean_query)
        if output_res.is_blocked:
            # Fallback or error message
            return f"[BLOCKED] Response unsafe: {output_res.reason}"
            
        return output_res.text
