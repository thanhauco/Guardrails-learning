# Guardrails Learning Project

A comprehensive, hands-on guide to implementing guardrails for Large Language Models (LLMs). This project covers everything from basic input validation to advanced semantic checks, prompt engineering, and real-world application integration.

## 🚀 Project Overview

This repository is structured as a learning path, taking you from Level 1 (Basics) to Level 6 (Real-world Applications).

### 📂 Directory Structure

- **`basics/`**: Fundamental guardrails.
    - `input_validation.py`: Length, format, and sanitization.
    - `output_validation.py`: JSON structure, length, and keywords.
    - `rate_limiting.py`: Token bucket rate limiter.
    - `content_filtering.py`: Basic keyword filtering.
    - `error_handling.py`: Custom exceptions and error formatting.

- **`intermediate/`**: More complex checks.
    - `toxic_content_detection.py`: Regex-based toxicity detection.
    - `pii_detection.py`: PII identification and redaction.
    - `prompt_injection_prevention.py`: Heuristic injection detection.
    - `context_management.py`: Token window management.
    - `quality_validation.py`: Response quality heuristics.

- **`advanced/`**: AI-driven guardrails.
    - `semantic_validation.py`: Embedding-based relevance checks.
    - `hallucination_detection.py`: NLI-based fact checking.
    - `bias_detection.py`: Keyword-based bias detection.
    - `custom_validators.py`: Base classes for custom logic.
    - `validation_chains.py`: Composing multiple validators.

- **`prompt_engineering/`**: Techniques to guide LLM behavior.
    - `few_shot_learning.py`: Constructing few-shot prompts.
    - `chain_of_thought.py`: CoT prompting wrappers.
    - `dynamic_prompts.py`: Context-aware prompt building.
    - `prompt_templates.py`: Reusable Jinja-style templates.
    - `optimization.py`: Grid search for prompt parameters.

- **`frameworks/`**: Integration examples.
    - `guardrails_ai_examples.py`: Using the official Guardrails AI library.
    - `langchain_integration.py`: LangChain LCEL integration.
    - `openai_integration.py`: Wrapper for OpenAI API.
    - `anthropic_integration.py`: Wrapper for Anthropic API.
    - `custom_framework.py`: A minimal, reusable guardrails framework.

- **`applications/`**: Real-world examples.
    - `safe_chatbot.py`: Interactive CLI chatbot.
    - `content_moderator.py`: Batch file processing.
    - `rag_with_validation.py`: RAG with hallucination checks.
    - `multi_agent_system.py`: Safe inter-agent communication.
    - `production_ready_example.py`: FastAPI service with guardrails.

- **`sample_projects/`**: Complete, cohesive projects.
    - **`super_safe_assistant/`**: A full-featured customer service bot integrating ALL techniques (RAG, CoT, PII, Toxicity, etc.).

- **`benchmarks/`**: Performance testing.
    - `performance_test.py`: Latency measurement script.

- **`notebooks/`**: Interactive learning.
    - `guardrails_tutorial.ipynb`: General overview.
    - `00_data_generation.ipynb`: Generate synthetic datasets (Clean, Toxic, PII).
    - `01_privacy_guardrails.ipynb`: Deep dive into PII detection.
    - `02_content_safety.ipynb`: Evaluating toxicity detection.
    - `03_rag_validation.ipynb`: Validating RAG outputs.
    - `04_prompt_engineering.ipynb`: Prompt optimization lab.

## 🛠️ Getting Started

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Sample Project**:
    See the "SuperSafe AI Assistant" in action:
    ```bash
    python -m sample_projects.super_safe_assistant.main
    ```

3.  **Run Examples**:
    Run any module directly to see it work:
    ```bash
    python -m basics.input_validation
    python -m applications.safe_chatbot
    ```

4.  **Run Benchmarks**:
    Measure the performance overhead:
    ```bash
    python benchmarks/performance_test.py
    ```

5.  **Run Tests**:
    Verify everything is working:
    ```bash
    pytest tests/
    ```

## 📚 Learning Path

We recommend following the folders in order: `basics` -> `intermediate` -> `advanced`. Then explore `prompt_engineering` and `frameworks` before diving into `applications` and `sample_projects`.

## 🤝 Contributing

Feel free to add your own validators or improve the existing ones! Check out `advanced/custom_validators.py` for a starting point.
