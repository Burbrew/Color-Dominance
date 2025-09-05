#!/usr/bin/env python3
"""
Agent Testing Script for Color Dominance Detection Task
Tests 4 agents: AIDE, OpenHands, GoogleCLI, Claude Code
"""

import os
import json
import time
import subprocess
import shutil
from datetime import datetime

# Task configuration
TASK_DIR = "colordominance_task-main"
AGENTS = {
    "AIDE": {
        "command": "aide",
        "description": "AIDE with Claude Sonnet 4",
        "needs_setup": True
    },
    "OpenHands": {
        "command": "openhands",
        "description": "OpenHands with Claude Sonnet 4", 
        "needs_setup": True
    },
    "GoogleCLI": {
        "command": "googlecli",
        "description": "GoogleCLI with Gemini 2.5 Pro",
        "needs_setup": True
    },
    "Claude Code": {
        "command": "claude-code",
        "description": "Claude Code with Claude Sonnet 4",
        "needs_setup": True
    }
}

def check_agent_availability():
    """Check which agents are available on the system"""
    available = {}
    for agent_name, config in AGENTS.items():
        try:
            result = subprocess.run([config["command"], "--version"], 
                                  capture_output=True, text=True, timeout=10)
            available[agent_name] = True
            print(f"✅ {agent_name}: Available")
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            available[agent_name] = False
            print(f"❌ {agent_name}: Not available")
    return available

def create_agent_workspace(agent_name):
    """Create a clean workspace for the agent"""
    workspace_dir = f"workspace_{agent_name.lower().replace(' ', '_')}"
    if os.path.exists(workspace_dir):
        shutil.rmtree(workspace_dir)
    os.makedirs(workspace_dir)
    
    # Copy task files
    shutil.copytree(f"{TASK_DIR}/input", f"{workspace_dir}/input")
    shutil.copy(f"{TASK_DIR}/prompt.md", workspace_dir)
    shutil.copy(f"{TASK_DIR}/config.json", workspace_dir)
    
    return workspace_dir

def run_agent_test(agent_name, workspace_dir, with_human_prompting=False):
    """Run a single agent test"""
    print(f"\n{'='*60}")
    print(f"Testing {agent_name}")
    print(f"{'='*60}")
    
    # Create the prompt file for the agent
    prompt_file = os.path.join(workspace_dir, "task_prompt.txt")
    with open(prompt_file, "w") as f:
        f.write("COLOR DOMINANCE DETECTION TASK\n")
        f.write("="*40 + "\n\n")
        
        # Read the original prompt
        with open(f"{TASK_DIR}/prompt.md", "r") as pf:
            f.write(pf.read())
        
        f.write("\n\nTASK FILES:\n")
        f.write("- Input images are in the 'input/' directory\n")
        f.write("- You need to create a 'solution.json' file with your predictions\n")
        f.write("- Ground truth is available in 'input/targets.json' for reference\n")
        
        if with_human_prompting:
            f.write("\n\nHUMAN PROMPTING MODE:\n")
            f.write("- A human will provide feedback during your work\n")
            f.write("- Follow their guidance to improve your solution\n")
            f.write("- Maximum 15 human prompts will be provided\n")
    
    # Run the agent
    start_time = time.time()
    try:
        if agent_name == "AIDE":
            cmd = ["aide", "solve", "--task", prompt_file, "--workspace", workspace_dir]
        elif agent_name == "OpenHands":
            cmd = ["openhands", "run", "--prompt", prompt_file, "--workspace", workspace_dir]
        elif agent_name == "GoogleCLI":
            cmd = ["googlecli", "solve", "--prompt", prompt_file, "--output", workspace_dir]
        elif agent_name == "Claude Code":
            cmd = ["claude-code", "solve", "--prompt", prompt_file, "--workspace", workspace_dir]
        else:
            raise ValueError(f"Unknown agent: {agent_name}")
        
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=workspace_dir, capture_output=True, text=True, timeout=1800)  # 30 min timeout
        
        execution_time = time.time() - start_time
        
        # Check if solution was created
        solution_file = os.path.join(workspace_dir, "solution.json")
        success = os.path.exists(solution_file)
        
        if success:
            print(f"✅ {agent_name} completed successfully in {execution_time:.2f}s")
            print(f"Solution file created: {solution_file}")
        else:
            print(f"❌ {agent_name} failed - no solution file created")
            print(f"Error output: {result.stderr}")
        
        return {
            "agent": agent_name,
            "success": success,
            "execution_time": execution_time,
            "solution_file": solution_file if success else None,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
        
    except subprocess.TimeoutExpired:
        print(f"⏰ {agent_name} timed out after 30 minutes")
        return {
            "agent": agent_name,
            "success": False,
            "execution_time": 1800,
            "solution_file": None,
            "stdout": "",
            "stderr": "Timeout after 30 minutes"
        }
    except Exception as e:
        print(f"❌ {agent_name} failed with error: {str(e)}")
        return {
            "agent": agent_name,
            "success": False,
            "execution_time": time.time() - start_time,
            "solution_file": None,
            "stdout": "",
            "stderr": str(e)
        }

def evaluate_solution(solution_file, ground_truth_file):
    """Evaluate a solution against ground truth"""
    if not os.path.exists(solution_file):
        return {"accuracy": 0.0, "correct": 0, "total": 0, "missing": 0}
    
    # Load predictions
    with open(solution_file, "r") as f:
        data = json.load(f)
    predictions = data.get("predictions", {})
    
    # Load ground truth
    with open(ground_truth_file, "r") as f:
        ground_truth = json.load(f)
    
    # Calculate metrics
    correct = 0
    total = len(ground_truth)
    missing = 0
    
    for filename, true_color in ground_truth.items():
        pred_color = predictions.get(filename)
        if pred_color is None:
            missing += 1
            continue
        if pred_color.lower().strip() == true_color.lower().strip():
            correct += 1
    
    accuracy = correct / total if total > 0 else 0.0
    
    return {
        "accuracy": accuracy,
        "correct": correct,
        "total": total,
        "missing": missing
    }

def run_all_tests():
    """Run tests for all available agents"""
    print("COLOR DOMINANCE DETECTION - AGENT TESTING")
    print("="*60)
    
    # Check agent availability
    available_agents = check_agent_availability()
    
    if not any(available_agents.values()):
        print("\n❌ No agents are available on this system.")
        print("Please install at least one of the following:")
        for agent_name in AGENTS.keys():
            print(f"  - {agent_name}")
        return
    
    # Run tests
    results = []
    
    for agent_name, is_available in available_agents.items():
        if not is_available:
            print(f"\n⏭️  Skipping {agent_name} (not available)")
            continue
            
        # Test without human prompting
        workspace_dir = create_agent_workspace(agent_name)
        result = run_agent_test(agent_name, workspace_dir, with_human_prompting=False)
        
        # Evaluate solution if created
        if result["success"]:
            ground_truth_file = f"{TASK_DIR}/ground_truth_colors.json"
            evaluation = evaluate_solution(result["solution_file"], ground_truth_file)
            result["evaluation"] = evaluation
            print(f"📊 Accuracy: {evaluation['accuracy']:.3f} ({evaluation['correct']}/{evaluation['total']})")
        else:
            result["evaluation"] = {"accuracy": 0.0, "correct": 0, "total": 15, "missing": 15}
        
        results.append(result)
    
    # Print summary
    print(f"\n{'='*60}")
    print("TESTING SUMMARY")
    print(f"{'='*60}")
    
    for result in results:
        agent = result["agent"]
        success = result["success"]
        accuracy = result["evaluation"]["accuracy"]
        correct = result["evaluation"]["correct"]
        total = result["evaluation"]["total"]
        time_taken = result["execution_time"]
        
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{agent:15} | {status:10} | Accuracy: {accuracy:.3f} ({correct}/{total}) | Time: {time_taken:.1f}s")
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"test_results_{timestamp}.json"
    
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Detailed results saved to: {results_file}")

if __name__ == "__main__":
    run_all_tests()
