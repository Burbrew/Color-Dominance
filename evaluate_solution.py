#!/usr/bin/env python3
"""
Simple evaluation script for Color Dominance Detection task
Usage: python3 evaluate_solution.py solution.json ground_truth.json
"""

import json
import sys
import os

def evaluate_solution(solution_file, ground_truth_file):
    """Evaluate a solution against ground truth"""
    
    # Load solution
    if not os.path.exists(solution_file):
        print(f"❌ Solution file not found: {solution_file}")
        return None
        
    with open(solution_file, "r") as f:
        solution_data = json.load(f)
    
    predictions = solution_data.get("predictions", {})
    if not predictions:
        print("❌ No predictions found in solution file")
        return None
    
    # Load ground truth
    if not os.path.exists(ground_truth_file):
        print(f"❌ Ground truth file not found: {ground_truth_file}")
        return None
        
    with open(ground_truth_file, "r") as f:
        ground_truth = json.load(f)
    
    # Calculate metrics
    correct = 0
    total = len(ground_truth)
    missing = 0
    wrong = 0
    
    print(f"\n📊 EVALUATION RESULTS")
    print(f"{'='*50}")
    print(f"Total images: {total}")
    print(f"Predictions provided: {len(predictions)}")
    print()
    
    # Check each image
    for filename, true_color in ground_truth.items():
        pred_color = predictions.get(filename)
        
        if pred_color is None:
            missing += 1
            print(f"❌ {filename}: MISSING (should be {true_color})")
        elif pred_color.lower().strip() == true_color.lower().strip():
            correct += 1
            print(f"✅ {filename}: {pred_color} (correct)")
        else:
            wrong += 1
            print(f"❌ {filename}: {pred_color} (should be {true_color})")
    
    # Calculate accuracy
    accuracy = correct / total if total > 0 else 0.0
    
    print(f"\n📈 SUMMARY")
    print(f"{'='*50}")
    print(f"Correct: {correct}/{total}")
    print(f"Wrong: {wrong}")
    print(f"Missing: {missing}")
    print(f"Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
    
    # Success criteria
    if accuracy >= 1.0:
        print(f"🎉 SUCCESS: Perfect accuracy!")
    elif accuracy >= 0.8:
        print(f"✅ GOOD: High accuracy")
    else:
        print(f"❌ FAILED: Low accuracy")
    
    return {
        "accuracy": accuracy,
        "correct": correct,
        "total": total,
        "wrong": wrong,
        "missing": missing
    }

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 evaluate_solution.py <solution.json> <ground_truth.json>")
        print("Example: python3 evaluate_solution.py solution.json colordominance_task-main/ground_truth_colors.json")
        sys.exit(1)
    
    solution_file = sys.argv[1]
    ground_truth_file = sys.argv[2]
    
    result = evaluate_solution(solution_file, ground_truth_file)
    
    if result is None:
        sys.exit(1)
    
    # Exit with appropriate code
    if result["accuracy"] >= 0.8:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()
