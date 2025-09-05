#!/usr/bin/env python3

import json
import sys
import os

# Add the current directory to the path so we can import the evaluator
sys.path.insert(0, os.path.dirname(__file__))

# Mock the benchmark imports since we don't have the full framework
class MockBaseEvaluator:
    def print_task_info(self):
        print("Color Dominance Detection Task - Testing Evaluator")

class MockEvaluationResult:
    def __init__(self, task_id, agent_id, timestamp, metrics, success, execution_time, error_message):
        self.task_id = task_id
        self.agent_id = agent_id
        self.timestamp = timestamp
        self.metrics = metrics
        self.success = success
        self.execution_time = execution_time
        self.error_message = error_message

# Mock the imports
import evaluator
evaluator.BaseEvaluator = MockBaseEvaluator
evaluator.EvaluationResult = MockEvaluationResult

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

# Create evaluator
evaluator_instance = evaluator.ColorDominanceEvaluator(config)

# Test with perfect solution
print("Testing with perfect solution...")
result = evaluator_instance.evaluate('.', None)
print("Success:", result.success)
print("Accuracy:", result.metrics['accuracy'])
print("Correct predictions:", result.metrics['correct_predictions'])
print("Total images:", result.metrics['total_images'])

# Test with incorrect solution
print("\nTesting with incorrect solution...")
incorrect_solution = {
    "predictions": {
        "image_1.png": "red",  # Wrong
        "image_2.png": "blue", # Wrong
        "image_3.png": "green" # Wrong
    }
}

# Write incorrect solution
with open('incorrect_solution.json', 'w') as f:
    json.dump(incorrect_solution, f, indent=2)

# Create a temporary config that points to the incorrect solution
temp_config = config.copy()
temp_config["expected_outputs"]["solution_file"] = "incorrect_solution.json"

temp_evaluator = evaluator.ColorDominanceEvaluator(temp_config)
result2 = temp_evaluator.evaluate('.', None)
print("Success:", result2.success)
print("Accuracy:", result2.metrics['accuracy'])
print("Correct predictions:", result2.metrics['correct_predictions'])
print("Missing predictions:", result2.metrics['missing_predictions'])

# Clean up
os.remove('incorrect_solution.json')
