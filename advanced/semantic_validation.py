"""
Semantic Validation Guardrails
==============================

Validates the meaning of the output using sentence embeddings.
Useful for checking if the output is semantically similar to a reference or
if it deviates too much from the expected topic.
"""

from typing import List, Optional
try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:
    SentenceTransformer = None

class SemanticValidator:
    """
    Uses a sentence transformer model to calculate cosine similarity
    between the output and a reference text or a set of allowed topics.
    """
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', threshold: float = 0.5):
        self.threshold = threshold
        if SentenceTransformer:
            self.model = SentenceTransformer(model_name)
        else:
            self.model = None
            print("Warning: sentence-transformers not installed. SemanticValidator will not work.")

    def validate_similarity(self, output: str, reference: str) -> bool:
        """Check if output is similar enough to the reference."""
        if not self.model:
            return True # Fail open if model missing
        
        embeddings = self.model.encode([output, reference])
        sim = util.cos_sim(embeddings[0], embeddings[1])
        return sim.item() >= self.threshold

    def validate_topic(self, output: str, allowed_topics: List[str]) -> bool:
        """Check if output matches one of the allowed topics."""
        if not self.model:
            return True

        output_emb = self.model.encode(output)
        topic_embs = self.model.encode(allowed_topics)
        
        # Check max similarity against any topic
        sims = util.cos_sim(output_emb, topic_embs)
        max_sim = sims.max().item()
        
        return max_sim >= self.threshold

if __name__ == "__main__":
    if SentenceTransformer:
        validator = SemanticValidator(threshold=0.4)
        
        # Similarity check
        ref = "The weather is sunny today."
        out1 = "It is a bright and clear day."
        out2 = "I like to eat pizza."
        
        print(f"Ref: '{ref}'")
        print(f"Out1: '{out1}' -> Similar? {validator.validate_similarity(out1, ref)}")
        print(f"Out2: '{out2}' -> Similar? {validator.validate_similarity(out2, ref)}")
        
        # Topic check
        topics = ["sports", "politics", "technology"]
        print(f"\nTopics: {topics}")
        print(f"Out: 'The new iPhone is fast' -> Allowed? {validator.validate_topic('The new iPhone is fast', topics)}")
        print(f"Out: 'The election results are in' -> Allowed? {validator.validate_topic('The election results are in', topics)}")
        print(f"Out: 'I love gardening' -> Allowed? {validator.validate_topic('I love gardening', topics)}")
    else:
        print("Please install sentence-transformers to run this example.")
