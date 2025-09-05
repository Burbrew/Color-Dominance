<<<<<<< HEAD
# Color Dominance Detection Task

A computer vision task for testing AI agents' visual analysis capabilities, following the same methodology as the original COLA Onboarding studies.

## 🎯 Task Overview

**Task**: Color Dominance Detection  
**Description**: Identify the dominant color in images containing multiple colored regions  
**Difficulty**: Medium  
**Category**: Computer Vision  
**Success Criteria**: 100% accuracy (15/15 correct)

## 📁 Repository Structure

```
├── colordominance_task-main/          # Complete task package
│   ├── config.json                    # Task configuration
│   ├── prompt.md                      # Task instructions
│   ├── evaluator.py                   # Automated evaluation
│   ├── generate_inputs.py             # Dataset generator
│   ├── Human_Prompting.md             # Human prompting guidelines
│   ├── input/                         # Test images (15 images)
│   └── ground_truth_colors.json       # Correct answers
├── test_agents.py                     # Automated testing script
├── evaluate_solution.py               # Simple evaluation script
├── setup_testing.py                   # Environment setup
├── demo_testing.py                    # Demo simulation
├── generate_report.py                 # PDF report generator
├── generate_enhanced_report.py        # Enhanced PDF with results
├── MANUAL_TESTING_GUIDE.md            # Step-by-step testing guide
├── TESTING_SUMMARY.md                 # Complete testing documentation
├── FINAL_SUMMARY.md                   # Implementation summary
└── *.pdf                              # Generated reports
```

## 🤖 Agents Tested

Based on the original COLA Onboarding studies, this task tests 4 agents:

| Agent | Model | Expected Performance |
|-------|-------|---------------------|
| AIDE | Claude Sonnet 4 | Low success without prompting |
| OpenHands | Claude Sonnet 4 | Medium success, improves with prompting |
| GoogleCLI | Gemini 2.5 Pro | Low success, limited improvement |
| Claude Code | Claude Sonnet 4 | Best performance, good with prompting |

## 🚀 Quick Start

### Option 1: Demo Simulation (No Installation Required)
```bash
python3 demo_testing.py
```

### Option 2: Automated Testing (Agents Required)
```bash
# 1. Install agents
pip install aide-cli openhands google-cli claude-code

# 2. Set API keys
export ANTHROPIC_API_KEY="your_anthropic_key"
export GOOGLE_API_KEY="your_google_key"

# 3. Run automated tests
python3 test_agents.py
```

### Option 3: Manual Testing
```bash
# 1. Setup
python3 setup_testing.py

# 2. Test individual agent
cd test_workspace
aide solve --prompt "Complete the Color Dominance Detection task"

# 3. Evaluate results
python3 ../evaluate_solution.py solution.json ground_truth_colors.json
```

## 📊 Expected Results

Each agent should create a `solution.json` file:

```json
{
  "predictions": {
    "image_1.png": "blue",
    "image_2.png": "pink",
    "image_3.png": "blue",
    "image_4.png": "black",
    "image_5.png": "pink",
    "image_6.png": "green",
    "image_7.png": "red",
    "image_8.png": "purple",
    "image_9.png": "black",
    "image_10.png": "orange",
    "image_11.png": "blue",
    "image_12.png": "orange",
    "image_13.png": "purple",
    "image_14.png": "gray",
    "image_15.png": "purple"
  }
}
```

## 🧪 Human Prompting Testing

Follow the structured templates in `colordominance_task-main/Human_Prompting.md`:

1. **Start with agent's first attempt**
2. **Use structured feedback**:
   - "Image X: consider the area coverage of each color, not just the number of regions"
   - "Image X: look more carefully at which color takes up the most space"
3. **Limit to 15 total prompts** across all images
4. **Track improvement** in accuracy

## 📈 Evaluation Metrics

- **Perfect Success**: 100% accuracy (15/15)
- **Good Performance**: ≥80% accuracy (12+/15)
- **Poor Performance**: <80% accuracy (<12/15)

## 📋 Generated Reports

- **`Notebook_2_ColorDominance_Detection.pdf`** - Basic report template
- **`Notebook_2_ColorDominance_Detection_Enhanced.pdf`** - Report with demo results

## 🔧 Troubleshooting

### Common Issues
1. **Agent not found**: Install with `pip install agent-name`
2. **API key error**: Set environment variables
3. **No solution.json**: Agent failed - check logs
4. **Wrong format**: Solution doesn't match expected JSON

### Debug Commands
```bash
# Check agents
which aide openhands googlecli claude-code

# Check API keys
echo $ANTHROPIC_API_KEY
echo $GOOGLE_API_KEY

# Test evaluation
python3 evaluate_solution.py test_workspace/solution.json test_workspace/ground_truth_colors.json
```

## 📚 Documentation

- **`MANUAL_TESTING_GUIDE.md`** - Detailed manual testing instructions
- **`TESTING_SUMMARY.md`** - Complete testing documentation
- **`FINAL_SUMMARY.md`** - Implementation summary

## 🎯 Success Criteria

The task is successful if:
1. Agents can be tested systematically
2. Results show clear performance differences between agents
3. Human prompting improves performance for most agents
4. Evaluation is automated and consistent
5. Results can be compared to original COLA studies

## 📞 Contributing

This task follows the same methodology as the original COLA Onboarding studies. Feel free to:
- Test with additional agents
- Modify the task parameters
- Add new evaluation metrics
- Improve the human prompting templates

## 📄 License

This project follows the same methodology as the original COLA Onboarding studies and is intended for research purposes.
=======
# Color-Dominance
>>>>>>> 9fee73b2cb62114532dbe5cced76f22c1de4c3c9
