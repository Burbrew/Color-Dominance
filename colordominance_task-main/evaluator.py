import json
import os
import time
from typing import Any, Dict, List
from datetime import datetime

from benchmark.core.base_evaluator import BaseEvaluator
from benchmark.core.result_types import EvaluationResult


class ColorDominanceEvaluator(BaseEvaluator):
    """
    Evaluator for the Color Dominance Detection task.
    Compares predicted dominant colors against ground truth using accuracy.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.accuracy_threshold = config.get("evaluation_criteria", {}).get("accuracy_threshold", 1.0)
        self.print_task_info()

    def evaluate(self, solution_folder: str, solution_config: Any = None) -> EvaluationResult:
        start_time = time.time()
        try:
            solution_file_name = self.config["expected_outputs"]["solution_file"]
            solution_path = os.path.join(solution_folder, solution_file_name)

            if not os.path.exists(solution_path):
                return EvaluationResult(
                    task_id=self.config["task_id"],
                    agent_id="unknown",
                    timestamp=datetime.now(),
                    metrics={"accuracy": 0.0, "total_images": 0, "correct_predictions": 0, "missing_predictions": 0},
                    success=False,
                    execution_time=time.time() - start_time,
                    error_message=f"Solution file {solution_file_name} not found",
                )

            predictions = self._load_predictions_json(solution_path)

            # Load ground truth
            if solution_config is not None:
                ground_truth = solution_config
            else:
                gt_file = self.config["expected_outputs"]["ground_truth_file"]
                task_dir = os.path.dirname(__file__)
                gt_path = os.path.join(task_dir, gt_file)
                if not os.path.exists(gt_path):
                    return EvaluationResult(
                        task_id=self.config["task_id"],
                        agent_id="unknown",
                        timestamp=datetime.now(),
                        metrics={"accuracy": 0.0, "total_images": 0, "correct_predictions": 0, "missing_predictions": 0},
                        success=False,
                        execution_time=time.time() - start_time,
                        error_message=f"Ground truth file {gt_file} not found",
                    )
                ground_truth = self._load_ground_truth_json(gt_path)

            metrics = self._calculate_metrics(predictions, ground_truth)
            success = metrics["accuracy"] >= self.accuracy_threshold

            return EvaluationResult(
                task_id=self.config["task_id"],
                agent_id="unknown",
                timestamp=datetime.now(),
                metrics=metrics,
                success=success,
                execution_time=time.time() - start_time,
                error_message=None if success else f"Accuracy {metrics['accuracy']:.3f} below threshold {self.accuracy_threshold}",
            )
        except Exception as e:
            return EvaluationResult(
                task_id=self.config["task_id"],
                agent_id="unknown",
                timestamp=datetime.now(),
                metrics={"accuracy": 0.0, "total_images": 0, "correct_predictions": 0, "missing_predictions": 0},
                success=False,
                execution_time=time.time() - start_time,
                error_message=f"Evaluation error: {str(e)}",
            )

    def _load_predictions_json(self, json_path: str) -> Dict[str, str]:
        with open(json_path, "r") as f:
            data = json.load(f)
        preds = data.get("predictions", {})
        normalized: Dict[str, str] = {}
        for filename, value in preds.items():
            if isinstance(value, str):
                normalized[filename] = value.lower().strip()
        return normalized

    def _load_ground_truth_json(self, json_path: str) -> Dict[str, str]:
        with open(json_path, "r") as f:
            data = json.load(f)
        return {k: v.lower().strip() for k, v in data.items()}

    def _calculate_metrics(self, predictions: Dict[str, str], ground_truth: Dict[str, str]) -> Dict[str, float]:
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

    def get_metrics(self) -> List[str]:
        return [
            "accuracy",
            "total_images",
            "correct_predictions",
            "missing_predictions",
        ]

    def generate_report(self, results: List[EvaluationResult]) -> str:
        if not results:
            return "No evaluation results to report."
        lines = []
        lines.append("Color Dominance Detection - Evaluation Report")
        lines.append("=" * 60)
        for i, result in enumerate(results, 1):
            lines.append(f"\nEvaluation {i}:")
            lines.append(f"  Task ID: {result.task_id}")
            lines.append(f"  Agent ID: {result.agent_id}")
            lines.append(f"  Timestamp: {result.timestamp}")
            lines.append(f"  Success: {result.success}")
            lines.append(f"  Execution Time: {result.execution_time:.2f}s")
            if result.error_message:
                lines.append(f"  Error: {result.error_message}")
            lines.append("  Metrics:")
            for metric, value in result.metrics.items():
                if metric in ("accuracy",):
                    lines.append(f"    {metric}: {value:.3f} ({value*100:.1f}%)")
                else:
                    lines.append(f"    {metric}: {value}")
        return "\n".join(lines)
