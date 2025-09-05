# Color Dominance Detection Task

- Inputs: images in `input/` with multiple colored regions where one color dominates by area coverage
- Output: `solution.json` with mapping from filename to dominant color name:
  - Example:
    ```json
    {
      "predictions": {
        "image_1.png": "red",
        "image_2.png": "blue"
      }
    }
    ```
- Ground truth: `ground_truth_colors.json`

To generate inputs and ground truth:

```bash
python colordominance_task-main/generate_inputs.py --out colordominance_task-main --n 15 --min_regions 3 --max_regions 8
```
