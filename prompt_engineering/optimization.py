"""
Prompt Optimization
===================

Basic utilities for optimizing prompts via grid search over parameters.
In a real scenario, you might use DSPy or similar libraries.
"""

from typing import List, Dict, Callable, Any
import itertools

class PromptOptimizer:
    def __init__(self, model_func: Callable[[str, float, float], str], evaluator: Callable[[str], float]):
        """
        :param model_func: Function that takes (prompt, temperature, top_p) and returns output string.
        :param evaluator: Function that takes output string and returns a score (0.0 to 1.0).
        """
        self.model_func = model_func
        self.evaluator = evaluator

    def grid_search(self, prompt_template: str, test_inputs: List[str], 
                   temperatures: List[float], top_ps: List[float]) -> Dict[str, Any]:
        
        best_score = -1.0
        best_params = {}
        results = []

        # Generate all combinations
        params = list(itertools.product(temperatures, top_ps))
        
        print(f"Starting grid search with {len(params)} combinations...")

        for temp, top_p in params:
            total_score = 0.0
            for inp in test_inputs:
                prompt = prompt_template.replace("{input}", inp)
                try:
                    output = self.model_func(prompt, temp, top_p)
                    score = self.evaluator(output)
                    total_score += score
                except Exception as e:
                    print(f"Error with temp={temp}, top_p={top_p}: {e}")
            
            avg_score = total_score / len(test_inputs) if test_inputs else 0
            results.append({"temp": temp, "top_p": top_p, "score": avg_score})
            
            if avg_score > best_score:
                best_score = avg_score
                best_params = {"temp": temp, "top_p": top_p}
                
        return {
            "best_params": best_params,
            "best_score": best_score,
            "all_results": results
        }

if __name__ == "__main__":
    # Mock model and evaluator
    def mock_model(prompt, temp, top_p):
        # Simulate better performance at lower temp
        if temp < 0.5:
            return "Correct Answer"
        return "Random Noise"

    def mock_evaluator(output):
        return 1.0 if output == "Correct Answer" else 0.0

    optimizer = PromptOptimizer(mock_model, mock_evaluator)
    
    template = "Answer this: {input}"
    inputs = ["2+2", "Capital of France"]
    temps = [0.1, 0.7, 1.0]
    top_ps = [0.9, 1.0]
    
    result = optimizer.grid_search(template, inputs, temps, top_ps)
    print("Optimization Result:", result)
