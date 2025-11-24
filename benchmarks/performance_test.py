"""
Performance Benchmarks
======================

Measures the latency overhead of various guardrails components.
"""

import time
import statistics
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basics.input_validation import InputValidator
from intermediate.toxic_content_detection import ToxicDetector
from intermediate.pii_detection import PIIDetector
from sample_projects.super_safe_assistant.pipeline import GuardPipeline

def benchmark(name, func, iterations=100):
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms
    
    avg_time = statistics.mean(times)
    p95_time = statistics.quantiles(times, n=20)[18]  # 95th percentile
    
    print(f"{name:<30} | Avg: {avg_time:.3f}ms | P95: {p95_time:.3f}ms")

def run_benchmarks():
    print("Running Guardrails Benchmarks (100 iterations each)...")
    print("-" * 60)
    
    # 1. Input Validator
    validator = InputValidator(max_length=1000)
    input_text = "This is a sample input string to test validation performance." * 5
    benchmark("InputValidator (Basic)", lambda: validator.validate(input_text))
    
    # 2. Toxic Detector
    toxic = ToxicDetector()
    benchmark("ToxicDetector (Regex)", lambda: toxic.check(input_text))
    
    # 3. PII Detector
    pii = PIIDetector()
    benchmark("PIIDetector (Regex)", lambda: pii.check(input_text))
    
    # 4. Full Pipeline
    pipeline = GuardPipeline()
    # Disable advanced guards for fair benchmark if they are slow/missing
    pipeline.hallucination_detector = None 
    pipeline.semantic_validator = None
    
    benchmark("Full Pipeline (Input)", lambda: pipeline.validate_input(input_text))
    
    # 5. Full Pipeline (Output)
    output_text = "This is a generated response." * 10
    benchmark("Full Pipeline (Output)", lambda: pipeline.validate_output(output_text))

if __name__ == "__main__":
    run_benchmarks()
