"""
SuperSafe AI Assistant - Main Application
=========================================
Entry point for the sample project.
"""

import sys
import os

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sample_projects.super_safe_assistant.agent import SafeAgent

def main():
    print("Initializing SuperSafe AI Assistant...")
    agent = SafeAgent()
    
    print("\n" + "="*50)
    print("SuperSafe AI Assistant (Type 'quit' to exit)")
    print("Try asking about: refund policy, shipping, contact, pricing")
    print("Or try to break it with: toxic inputs, PII, or off-topic questions!")
    print("="*50 + "\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                break
            
            if not user_input:
                continue
                
            response = agent.chat(user_input)
            print(f"Bot: {response}\n")
            
        except KeyboardInterrupt:
            break
    
    print("\nGoodbye!")

if __name__ == "__main__":
    main()
