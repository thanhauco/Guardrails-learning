"""
Prompt Templates
================

Reusable prompt templates using Python's string.Template.
Allows for separation of prompt structure from data.
"""

from string import Template
from typing import Dict, Any

class PromptTemplate:
    def __init__(self, template_str: str):
        self.template = Template(template_str)

    def format(self, **kwargs) -> str:
        return self.template.safe_substitute(**kwargs)

# Common templates
SUMMARIZATION_TEMPLATE = """
Please summarize the following text in ${num_sentences} sentences:

Text:
${text}

Summary:
"""

CLASSIFICATION_TEMPLATE = """
Classify the following text into one of these categories: ${categories}.

Text: ${text}

Category:
"""

if __name__ == "__main__":
    # Summarization example
    t1 = PromptTemplate(SUMMARIZATION_TEMPLATE)
    prompt1 = t1.format(num_sentences=2, text="Long text about AI...")
    print(f"--- Summarization Prompt ---\n{prompt1}")

    # Classification example
    t2 = PromptTemplate(CLASSIFICATION_TEMPLATE)
    prompt2 = t2.format(categories="News, Sports, Tech", text="New iPhone released")
    print(f"\n--- Classification Prompt ---\n{prompt2}")
