# Guardrails Learning Project 🛡️

A comprehensive guide to implementing guardrails and prompt engineering in Python, from basic to advanced concepts.

## 📚 What are Guardrails?

Guardrails are safety mechanisms and validation layers that ensure AI/LLM applications behave safely, reliably, and as intended. They help prevent:
- Prompt injection attacks
- Toxic or harmful content generation
- Privacy leaks (PII exposure)
- Hallucinations and factual errors
- Bias and unfair outputs
- Resource abuse

## 🎯 Project Structure

```
Guardrails-learning/
├── 01_basics/              # Basic guardrails concepts
│   ├── input_validation.py
│   ├── output_validation.py
│   ├── content_filtering.py
│   ├── rate_limiting.py
│   └── error_handling.py
├── 02_intermediate/        # Intermediate techniques
│   ├── prompt_injection_prevention.py
│   ├── pii_detection.py
│   ├── toxic_content_detection.py
│   ├── context_management.py
│   └── quality_validation.py
├── 03_advanced/            # Advanced guardrails
│   ├── custom_validators.py
│   ├── validation_chains.py
│   ├── semantic_validation.py
│   ├── hallucination_detection.py
│   └── bias_detection.py
├── 04_prompt_engineering/  # Prompt engineering with guardrails
│   ├── few_shot_learning.py
│   ├── chain_of_thought.py
│   ├── prompt_templates.py
│   ├── dynamic_prompts.py
│   └── optimization.py
├── 05_frameworks/          # Integration with popular frameworks
│   ├── guardrails_ai_examples.py
│   ├── langchain_integration.py
│   ├── openai_integration.py
│   ├── anthropic_integration.py
│   └── custom_framework.py
├── 06_applications/        # Real-world applications
│   ├── safe_chatbot.py
│   ├── content_moderator.py
│   ├── rag_with_validation.py
│   └── multi_agent_system.py
├── tests/                  # Unit and integration tests
├── notebooks/              # Jupyter notebooks for tutorials
└── utils/                  # Shared utilities
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

```bash
# Clone or navigate to the project
cd Guardrails-learning

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Quick Start

```python
# Example: Basic input validation
from guardrails_learning.basics import InputValidator

validator = InputValidator()
result = validator.validate("Your input here")
print(result)
```

## 📖 Learning Path

### Level 1: Basics (Start Here!)
1. **Input Validation** - Learn to validate and sanitize user inputs
2. **Output Validation** - Ensure AI outputs meet quality standards
3. **Content Filtering** - Filter inappropriate content
4. **Rate Limiting** - Prevent abuse and manage resources
5. **Error Handling** - Gracefully handle failures

### Level 2: Intermediate
1. **Prompt Injection Prevention** - Protect against malicious prompts
2. **PII Detection** - Identify and redact sensitive information
3. **Toxic Content Detection** - Detect and filter harmful content
4. **Context Management** - Handle token limits and context windows
5. **Quality Validation** - Ensure response quality and relevance

### Level 3: Advanced
1. **Custom Validators** - Build your own validation logic
2. **Validation Chains** - Combine multiple validators
3. **Semantic Validation** - Validate meaning and intent
4. **Hallucination Detection** - Identify factual errors
5. **Bias Detection** - Detect and mitigate biases

### Level 4: Prompt Engineering
1. **Few-Shot Learning** - Teach AI with examples
2. **Chain-of-Thought** - Guide AI reasoning
3. **Prompt Templates** - Reusable prompt patterns
4. **Dynamic Prompts** - Context-aware prompt generation
5. **Optimization** - Improve prompt effectiveness

### Level 5: Framework Integration
1. **Guardrails AI** - Use the Guardrails AI library
2. **LangChain** - Integrate with LangChain
3. **OpenAI** - Apply guardrails to OpenAI APIs
4. **Anthropic** - Work with Claude safely
5. **Custom Framework** - Build your own guardrails system

### Level 6: Real-World Applications
1. **Safe Chatbot** - Production-ready chatbot with guardrails
2. **Content Moderator** - Automated content moderation
3. **RAG System** - Retrieval-Augmented Generation with validation
4. **Multi-Agent System** - Coordinated AI agents with safety

## 🔑 Key Concepts

### Input Guardrails
- Length validation
- Format validation
- Content sanitization
- Injection prevention
- Encoding validation

### Output Guardrails
- Quality checks
- Factuality verification
- Toxicity filtering
- PII redaction
- Format compliance

### Prompt Engineering Best Practices
- Clear instructions
- Context provision
- Example-based learning
- Structured outputs
- Iterative refinement

## 🛠️ Technologies Used

- **Python 3.8+** - Core language
- **Guardrails AI** - Guardrails framework
- **LangChain** - LLM application framework
- **OpenAI API** - GPT models
- **Anthropic API** - Claude models
- **Transformers** - HuggingFace models
- **Pydantic** - Data validation
- **NLTK/spaCy** - NLP processing
- **pytest** - Testing framework

## 📝 Examples

Each module includes:
- ✅ Detailed code examples
- ✅ Inline documentation
- ✅ Usage demonstrations
- ✅ Best practices
- ✅ Common pitfalls to avoid

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_input_validation.py

# Run with coverage
pytest --cov=guardrails_learning tests/
```

## 📚 Additional Resources

- [Guardrails AI Documentation](https://docs.guardrailsai.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [Anthropic Safety Guidelines](https://www.anthropic.com/index/claude-2)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

## 🤝 Contributing

This is a learning project. Feel free to:
- Add new examples
- Improve existing code
- Fix bugs
- Enhance documentation

## 📄 License

MIT License - Feel free to use for learning and projects

## 🎓 Learning Tips

1. **Start with basics** - Don't skip foundational concepts
2. **Run the code** - Hands-on practice is essential
3. **Experiment** - Modify examples to understand behavior
4. **Read comments** - Code comments explain the "why"
5. **Build projects** - Apply concepts to real problems
6. **Stay updated** - Guardrails evolve with AI capabilities

## 🔗 Quick Links

- [Installation Guide](#installation)
- [Learning Path](#learning-path)
- [Examples](#examples)
- [Testing](#testing)

---

**Happy Learning! 🚀**

Remember: Guardrails are not about limiting AI capabilities, but about ensuring safe, reliable, and trustworthy AI applications.
