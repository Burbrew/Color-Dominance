# Manual Testing Guide for Color Dominance Detection Task

This guide shows how to test the Color Dominance Detection task with the 4 agents mentioned in Notebook 1.

## Agents to Test

1. **AIDE** (Claude Sonnet 4)
2. **OpenHands** (Claude Sonnet 4) 
3. **GoogleCLI** (Gemini 2.5 Pro)
4. **Claude Code** (Claude Sonnet 4)

## Prerequisites

### 1. Install Required Agents

```bash
# AIDE
pip install aide-cli

# OpenHands  
pip install openhands

# GoogleCLI
pip install google-cli

# Claude Code
pip install claude-code
```

### 2. Set up API Keys

```bash
# For AIDE/OpenHands/Claude Code (Anthropic)
export ANTHROPIC_API_KEY="your_anthropic_key"

# For GoogleCLI (Google)
export GOOGLE_API_KEY="your_google_key"
```

## Testing Steps

### Step 1: Prepare Test Environment

```bash
# Create test directory
mkdir agent_tests
cd agent_tests

# Copy task files
cp -r ../colordominance_task-main/* .
```

### Step 2: Test Each Agent

#### AIDE Testing

```bash
# Create workspace
mkdir aide_test
cp -r input aide_test/
cp prompt.md aide_test/

# Run AIDE
cd aide_test
aide solve --prompt "Complete the Color Dominance Detection task. See prompt.md for details."
```

#### OpenHands Testing

```bash
# Create workspace  
mkdir openhands_test
cp -r input openhands_test/
cp prompt.md openhands_test/

# Run OpenHands
cd openhands_test
openhands run --prompt "Complete the Color Dominance Detection task. See prompt.md for details."
```

#### GoogleCLI Testing

```bash
# Create workspace
mkdir googlecli_test  
cp -r input googlecli_test/
cp prompt.md googlecli_test/

# Run GoogleCLI
cd googlecli_test
googlecli solve --prompt "Complete the Color Dominance Detection task. See prompt.md for details."
```

#### Claude Code Testing

```bash
# Create workspace
mkdir claude_code_test
cp -r input claude_code_test/
cp prompt.md claude_code_test/

# Run Claude Code
cd claude_code_test
claude-code solve --prompt "Complete the Color Dominance Detection task. See prompt.md for details."
```

### Step 3: Evaluate Results

For each agent, check if they created a `solution.json` file and evaluate it:

```bash
# Run evaluation script
python3 ../evaluate_solution.py solution.json ../ground_truth_colors.json
```

## Expected Output Format

Each agent should create a `solution.json` file like this:

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

## Human Prompting Testing

To test with human prompting (like in Notebook 1):

1. Start the agent
2. When they provide initial results, use the templates from `Human_Prompting.md`
3. Provide feedback like:
   - "Image 1: consider the area coverage of each color, not just the number of regions"
   - "Image 2: look more carefully at which color takes up the most space"
4. Limit to 15 total prompts across all images
5. Track the number of prompts used

## Evaluation Criteria

- **Success**: 100% accuracy (15/15 correct)
- **Partial Success**: >80% accuracy (12+/15 correct)  
- **Failure**: <80% accuracy (<12/15 correct)

## Troubleshooting

### Common Issues

1. **Agent not found**: Install the agent using pip
2. **API key error**: Set the correct environment variables
3. **No solution.json**: Agent may have failed - check logs
4. **Wrong format**: Solution doesn't match expected JSON structure

### Debug Commands

```bash
# Check if agents are installed
which aide openhands googlecli claude-code

# Check API keys
echo $ANTHROPIC_API_KEY
echo $GOOGLE_API_KEY

# Test with a single image
python3 colordominance_task-main/generate_inputs.py --n 1 --min_regions 3 --max_regions 5
```

## Results Tracking

Create a results table like in Notebook 1:

| Agent | Model | Default Success | + Human Prompting | # of Prompts |
|-------|-------|----------------|-------------------|--------------|
| AIDE | Claude Sonnet 4 | ?/15 | ?/15 | ? |
| OpenHands | Claude Sonnet 4 | ?/15 | ?/15 | ? |
| GoogleCLI | Gemini 2.5 Pro | ?/15 | ?/15 | ? |
| Claude Code | Claude Sonnet 4 | ?/15 | ?/15 | ? |
