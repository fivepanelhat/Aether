"""
Simple smoke test to verify Aether installs and runs correctly.
Run this after `pip install -e .`
"""

import subprocess
import sys

# Ensure UTF-8 output on Windows
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_aether_cli():
    print("Running Aether smoke test...\n")

    # Test 1: Check if aether command exists
    try:
        result = subprocess.run(
            [sys.executable, "-m", "aether.cli", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ `aether --version` works")
        else:
            print("❌ `aether --version` failed")
            return False
    except FileNotFoundError:
        print("❌ `aether` command not found. Did you run `pip install -e .`?")
        return False

    # Test 2: List skills
    try:
        result = subprocess.run(
            [sys.executable, "-m", "aether.cli", "skills"],
            capture_output=True,
            text=True,
            timeout=15
        )
        if "AVAILABLE SKILLS" in result.stdout or "No skills found" in result.stdout:
            print("✅ `aether skills` works")
        else:
            print("❌ `aether skills` output unexpected")
            return False
    except Exception as e:
        print(f"❌ Error running `aether skills`: {e}")
        return False

    print("\n✅ Smoke test passed. Aether is installed correctly.")
    return True


if __name__ == "__main__":
    success = test_aether_cli()
    sys.exit(0 if success else 1)
