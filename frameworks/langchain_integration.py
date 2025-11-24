"""
LangChain Integration
=====================

Integrating custom guardrails into a LangChain Runnable sequence.
Requires: pip install langchain langchain-core
"""

try:
    from langchain_core.runnables import RunnableLambda
    from langchain_core.messages import AIMessage
except ImportError:
    RunnableLambda = None

def validate_output(output):
    """Custom validation function to be used in the chain."""
    text = output.content if hasattr(output, 'content') else str(output)
    
    # Simple check: No "I don't know"
    if "I don't know" in text:
        raise ValueError("Model refused to answer.")
    
    return output

def example_langchain():
    if not RunnableLambda:
        print("LangChain not installed. Skipping example.")
        return

    print("--- LangChain Integration Example ---")

    # Mock LLM
    mock_llm = RunnableLambda(lambda x: AIMessage(content="I don't know the answer."))
    
    # Create chain with validation
    chain = mock_llm | RunnableLambda(validate_output)
    
    try:
        result = chain.invoke("What is the meaning of life?")
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Validation failed caught: {e}")

if __name__ == "__main__":
    example_langchain()
