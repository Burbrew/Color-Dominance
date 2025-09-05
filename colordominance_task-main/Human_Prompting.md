### Human Prompting Guide — Color Dominance Detection Task

Your job is to help prompt AI Agents to completion on the color dominance detection task. The task is described in prompt.md.

Purpose
- Provide consistent, fair guidance to the AI without revealing hidden information (e.g., the exact dominant color per image).
- Cap total human interventions at 15 prompts for the entire run.

Rules and Constraints
- Do not reveal or imply the true dominant color or provide color hints beyond the approved templates.
- Do not provide pixel-level details or algorithmic hints beyond the approved templates.
- Keep prompts terse, use only the templates below, and fill placeholders.
- Total budget: 15 prompts maximum for the full task. Track and stop at 15.

Placeholders
- [IMAGE_NUM]: integer index or identifier of the image (e.g., 1, 2, 3)
- [SEVERITY]: one of slightly, moderately, significantly
- [COLOR_FAMILY]: one of warm, cool, neutral (for general guidance only)

Approved Templates
Color Analysis Feedback
- Image [IMAGE_NUM]: consider the area coverage of each color, not just the number of regions.
- Image [IMAGE_NUM]: look more carefully at which color takes up the most space in the image.
- Image [IMAGE_NUM]: the dominant color is determined by area, not by how many separate regions there are.

Process and Visibility Prompts
- Image [IMAGE_NUM]: please show your color analysis by highlighting or marking the different colored regions.
- Image [IMAGE_NUM]: please update your analysis after reconsidering the area coverage.

General Guidance
- Image [IMAGE_NUM]: remember that a few large regions can dominate over many small ones.
- Image [IMAGE_NUM]: consider the entire image area when determining dominance.

Usage Protocol
1) Start with the agent's first attempt and request visual analysis if not provided.
2) Use at most one feedback line per image per iteration.
3) Focus on area-based analysis rather than region counting.
4) Stop prompting an image once the agent shows understanding of area-based dominance.
5) Do not include any specific color names or hints about the true dominant color.
6) Enforce the 15-prompt budget across all images. If the budget is exhausted, stop prompting.

Example Prompt Sequence (3 prompts total)
- Image 1: please show your color analysis by highlighting or marking the different colored regions.
- Image 1: consider the area coverage of each color, not just the number of regions.
- Image 1: good analysis.

Auditing Checklist
- No specific color details provided.
- Only approved templates used.
- Prompts ≤ 15 for the full run.
- Feedback addresses area-based analysis, not implementation details.
