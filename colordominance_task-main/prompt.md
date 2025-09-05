You are given images where each contains multiple colored regions of various shapes and sizes. One color dominates by covering the largest area in the image.

Your task: For each input image, identify the dominant color and output a JSON file named `solution.json` with the following structure:

```
{
  "predictions": {
    "<filename>": "<color_name>",
    ...
  }
}
```

Constraints and tips:
- Output only the `predictions` mapping, no explanations.
- Color names must be one of: red, blue, green, yellow, orange, purple, pink, brown, gray, black, white
- The dominant color is determined by the largest area coverage, not by the number of regions
- Colors may appear in different shades and intensities, but should be classified by their base color family
- Consider the entire image area when determining dominance
