#!/usr/bin/env python3

import json
import os

def load_predictions_json(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    preds = data.get("predictions", {})
    normalized = {}
    for filename, value in preds.items():
        if isinstance(value, str):
            normalized[filename] = value.lower().strip()
    return normalized

def load_ground_truth_json(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    return {k: v.lower().strip() for k, v in data.items()}

def calculate_metrics(predictions, ground_truth):
    if not ground_truth:
        return {"accuracy": 0.0, "total_images": 0, "correct_predictions": 0, "missing_predictions": 0}

    correct = 0
    total = len(ground_truth)
    missing = 0

    for filename, true_color in ground_truth.items():
        pred_color = predictions.get(filename)
        if pred_color is None:
            missing += 1
            continue
        if pred_color == true_color:
            correct += 1

    accuracy = correct / total if total > 0 else 0.0
    return {
        "accuracy": accuracy,
        "total_images": float(total),
        "correct_predictions": float(correct),
        "missing_predictions": float(missing),
    }

# Test with perfect solution
print("Testing with perfect solution...")
predictions = load_predictions_json('test_solution.json')
ground_truth = load_ground_truth_json('ground_truth_colors.json')
metrics = calculate_metrics(predictions, ground_truth)

print("Success:", metrics["accuracy"] >= 1.0)
print("Accuracy:", metrics["accuracy"])
print("Correct predictions:", metrics["correct_predictions"])
print("Total images:", metrics["total_images"])

# Test with incorrect solution
print("\nTesting with incorrect solution...")
incorrect_solution = {
    "predictions": {
        "image_1.png": "red",  # Wrong
        "image_2.png": "blue", # Wrong
        "image_3.png": "green" # Wrong
    }
}

with open('incorrect_solution.json', 'w') as f:
    json.dump(incorrect_solution, f, indent=2)

incorrect_predictions = load_predictions_json('incorrect_solution.json')
incorrect_metrics = calculate_metrics(incorrect_predictions, ground_truth)

print("Success:", incorrect_metrics["accuracy"] >= 1.0)
print("Accuracy:", incorrect_metrics["accuracy"])
print("Correct predictions:", incorrect_metrics["correct_predictions"])
print("Missing predictions:", incorrect_metrics["missing_predictions"])

# Clean up
os.remove('incorrect_solution.json')

print("\nEvaluator test completed successfully!")
