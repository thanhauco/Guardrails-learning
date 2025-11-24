"""
Configuration for SuperSafe AI Assistant
"""

class Config:
    # Input Validation
    MIN_INPUT_LENGTH = 5
    MAX_INPUT_LENGTH = 500
    
    # Output Validation
    MAX_OUTPUT_LENGTH = 1000
    
    # Toxicity
    TOXICITY_THRESHOLD = 0.8  # Not used by simple regex detector but good for future
    
    # Semantic Validation
    SEMANTIC_SIMILARITY_THRESHOLD = 0.5
    
    # Context Management
    MAX_CONTEXT_TOKENS = 2000
    
    # RAG
    KNOWLEDGE_BASE = {
        "refund policy": "Refunds are processed within 14 days of purchase. No refunds for digital goods after download.",
        "shipping": "Standard shipping takes 3-5 business days. Express shipping is 1-2 days.",
        "contact": "Support email is support@supersafe.ai. Phone support is available 9-5 EST.",
        "pricing": "Basic plan is $10/mo. Pro plan is $29/mo. Enterprise is custom pricing."
    }
    
    # System Prompt
    SYSTEM_PROMPT = """You are SuperSafe, a helpful and polite customer service assistant.
    You answer questions based ONLY on the provided context.
    If you don't know the answer, say so. Do not make up information.
    Be concise and professional."""
