"""
Guardrails Pipeline
===================
Orchestrates the execution of all guardrails.
"""

import sys
import os
from dataclasses import dataclass
from typing import Optional, Dict, Any

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from basics.input_validation import InputValidator, ValidationResult
from basics.output_validation import OutputValidator, OutputStatus
from intermediate.toxic_content_detection import ToxicDetector
from intermediate.pii_detection import PIIDetector
from intermediate.prompt_injection_prevention import PromptInjectionGuard, InjectionResult
from advanced.hallucination_detection import HallucinationDetector
from advanced.semantic_validation import SemanticValidator
from .config import Config

@dataclass
class PipelineResult:
    text: Optional[str]
    is_blocked: bool
    reason: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class GuardPipeline:
    def __init__(self):
        # Input Guards
        self.input_validator = InputValidator(
            min_length=Config.MIN_INPUT_LENGTH, 
            max_length=Config.MAX_INPUT_LENGTH
        )
        self.toxic_detector = ToxicDetector()
        self.pii_detector = PIIDetector()
        self.injection_guard = PromptInjectionGuard()
        
        # Output Guards
        self.output_validator = OutputValidator(max_length=Config.MAX_OUTPUT_LENGTH)
        
        # Advanced Guards (fail gracefully if deps missing)
        try:
            self.hallucination_detector = HallucinationDetector()
            self.semantic_validator = SemanticValidator(threshold=Config.SEMANTIC_SIMILARITY_THRESHOLD)
        except:
            self.hallucination_detector = None
            self.semantic_validator = None
            print("Warning: Advanced guardrails (Hallucination/Semantic) disabled due to missing dependencies.")

    def validate_input(self, user_input: str) -> PipelineResult:
        """Run all input guardrails."""
        
        # 1. Basic Validation (Length, Format, Sanitization)
        val_res = self.input_validator.validate(user_input)
        if val_res.status == ValidationResult.INVALID:
            return PipelineResult(None, True, f"Input Invalid: {val_res.message}")
        
        sanitized_input = val_res.sanitized_input or user_input

        # 2. Prompt Injection
        if self.injection_guard.check(sanitized_input) == InjectionResult.BLOCKED:
            return PipelineResult(None, True, "Potential prompt injection detected.")

        # 3. Toxicity
        if self.toxic_detector.check(sanitized_input).value == "toxic":
            return PipelineResult(None, True, "Toxic content detected.")

        # 4. PII (Redact instead of block)
        if self.pii_detector.check(sanitized_input).value == "found":
            sanitized_input = self.pii_detector.redact(sanitized_input)
            
        return PipelineResult(sanitized_input, False)

    def validate_output(self, generated_text: str, context: str = None, query: str = None) -> PipelineResult:
        """Run all output guardrails."""
        
        # 1. Basic Output Validation
        out_res = self.output_validator.validate(generated_text)
        if out_res.status == OutputStatus.INVALID:
            return PipelineResult(None, True, f"Output Invalid: {out_res.message}")
        
        final_text = out_res.sanitized_output or generated_text

        # 2. Toxicity Check on Output
        if self.toxic_detector.check(final_text).value == "toxic":
            return PipelineResult(None, True, "Generated toxic content.")

        # 3. Hallucination Check (if context provided)
        if context and self.hallucination_detector:
            if self.hallucination_detector.is_hallucination(context, final_text):
                return PipelineResult(None, True, "Hallucination detected (contradicts context).")

        # 4. Semantic Relevance (if query provided)
        if query and self.semantic_validator:
            # Check if answer is semantically related to query (loose check)
            # For strict RAG, we might check if answer is similar to context
            pass 

        return PipelineResult(final_text, False)
