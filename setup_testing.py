#!/usr/bin/env python3
"""
Setup script for Color Dominance Detection task testing
"""

import os
import subprocess
import sys

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6+ required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_required_packages():
    """Check if required packages are installed"""
    required = ["PIL", "json", "os", "time", "subprocess"]
    missing = []
    
    for package in required:
        try:
            if package == "PIL":
                import PIL
            else:
                __import__(package)
            print(f"✅ {package} available")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} missing")
    
    if missing:
        print(f"\n📦 Install missing packages:")
        if "PIL" in missing:
            print("pip install Pillow")
        return False
    
    return True

def check_agents():
    """Check which agents are available"""
    agents = {
        "aide": "aide --version",
        "openhands": "openhands --version", 
        "googlecli": "googlecli --version",
        "claude-code": "claude-code --version"
    }
    
    available = []
    for agent, cmd in agents.items():
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                available.append(agent)
                print(f"✅ {agent} available")
            else:
                print(f"❌ {agent} not working")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"❌ {agent} not installed")
    
    return available

def create_test_workspace():
    """Create a clean test workspace"""
    workspace = "test_workspace"
    
    if os.path.exists(workspace):
        print(f"🧹 Cleaning existing workspace: {workspace}")
        import shutil
        shutil.rmtree(workspace)
    
    os.makedirs(workspace)
    
    # Copy task files
    import shutil
    shutil.copytree("colordominance_task-main/input", f"{workspace}/input")
    shutil.copy("colordominance_task-main/prompt.md", workspace)
    shutil.copy("colordominance_task-main/config.json", workspace)
    shutil.copy("colordominance_task-main/ground_truth_colors.json", workspace)
    
    print(f"✅ Test workspace created: {workspace}")
    return workspace

def create_sample_solution():
    """Create a sample solution for testing"""
    sample_solution = {
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
    
    with open("test_workspace/solution.json", "w") as f:
        import json
        json.dump(sample_solution, f, indent=2)
    
    print("✅ Sample solution created for testing")

def test_evaluation():
    """Test the evaluation script"""
    print("\n🧪 Testing evaluation script...")
    
    try:
        result = subprocess.run([
            "python3", "evaluate_solution.py", 
            "test_workspace/solution.json",
            "test_workspace/ground_truth_colors.json"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Evaluation script working correctly")
            print("Sample output:")
            print(result.stdout)
        else:
            print("❌ Evaluation script failed")
            print("Error:", result.stderr)
            
    except Exception as e:
        print(f"❌ Error testing evaluation: {e}")

def main():
    print("🚀 COLOR DOMINANCE DETECTION - TESTING SETUP")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check required packages
    if not check_required_packages():
        print("\n📦 Please install missing packages and run again")
        return
    
    # Check agents
    print("\n🤖 Checking available agents...")
    available_agents = check_agents()
    
    if not available_agents:
        print("\n⚠️  No agents detected. You'll need to install at least one:")
        print("   pip install aide-cli")
        print("   pip install openhands") 
        print("   pip install google-cli")
        print("   pip install claude-code")
    else:
        print(f"\n✅ Found {len(available_agents)} available agents: {', '.join(available_agents)}")
    
    # Create test workspace
    print("\n📁 Setting up test workspace...")
    create_test_workspace()
    create_sample_solution()
    
    # Test evaluation
    test_evaluation()
    
    print(f"\n🎯 READY TO TEST!")
    print("="*60)
    print("Next steps:")
    print("1. Set up API keys:")
    print("   export ANTHROPIC_API_KEY='your_key'")
    print("   export GOOGLE_API_KEY='your_key'")
    print()
    print("2. Test an agent:")
    print("   cd test_workspace")
    print("   aide solve --prompt 'Complete the Color Dominance Detection task'")
    print()
    print("3. Evaluate results:")
    print("   python3 ../evaluate_solution.py solution.json ground_truth_colors.json")
    print()
    print("4. For human prompting, follow the templates in Human_Prompting.md")

if __name__ == "__main__":
    main()
