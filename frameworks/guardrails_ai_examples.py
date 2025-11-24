"""
Guardrails AI Library Integration
=================================

Examples using the official 'guardrails-ai' library.
Requires: pip install guardrails-ai
"""

try:
    import guardrails as gd
    from guardrails.hub import ProfanityFree
except ImportError:
    gd = None

def example_guardrails_ai():
    if not gd:
        print("Guardrails AI library not installed. Skipping example.")
        return

    # Define a rail spec or use Pydantic models
    # Here we use a simple string validator from the hub
    
    print("--- Guardrails AI Example ---")
    
    # Create a Guard with a specific validator
    # Note: You might need to run `guardrails hub install hub://guardrails/profanity_free` first
    try:
        guard = gd.Guard.from_string(
            validators=[ProfanityFree(on_fail="fix")]
        )
        
        # Validate
        raw_output = "This is a damn good example."
        validated_output = guard.parse(raw_output)
        
        print(f"Raw: {raw_output}")
        print(f"Validated: {validated_output.validated_output}")
        
    except Exception as e:
        print(f"Error running Guardrails AI example: {e}")
        print("Ensure you have installed the validator: guardrails hub install hub://guardrails/profanity_free")

if __name__ == "__main__":
    example_guardrails_ai()
