"""
One-time setup script for the traffic_law_pipeline project.
Creates a virtual environment, installs dependencies, and downloads Playwright browsers.

Usage:
    python setup.py
"""

import os
import subprocess
import sys
import platform


ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(ROOT, ".venv")

IS_WINDOWS = platform.system() == "Windows"
PYTHON = os.path.join(VENV_DIR, "Scripts" if IS_WINDOWS else "bin", "python")
PIP = os.path.join(VENV_DIR, "Scripts" if IS_WINDOWS else "bin", "pip")


def run(cmd, desc=""):
    """Run a command and exit on failure."""
    print(f"\n{'='*60}")
    print(f"  {desc}")
    print(f"{'='*60}")
    print(f"  $ {cmd}\n")
    result = subprocess.run(cmd, shell=True, cwd=ROOT)
    if result.returncode != 0:
        print(f"\n  ERROR: '{desc}' failed with exit code {result.returncode}")
        sys.exit(result.returncode)


def main():
    print("\n" + "=" * 60)
    print("  Traffic Law Pipeline — Setup")
    print("=" * 60)

    # 1. Create virtual environment
    if not os.path.exists(VENV_DIR):
        run(f"{sys.executable} -m venv {VENV_DIR}", "Creating virtual environment")
    else:
        print(f"\n  Virtual environment already exists at {VENV_DIR}")

    # 2. Upgrade pip
    run(f"{PYTHON} -m pip install --upgrade pip", "Upgrading pip")

    # 3. Install greenlet binary first (avoids C++ build tools requirement)
    run(f"{PIP} install greenlet --only-binary :all:", "Installing greenlet (pre-built binary)")

    # 4. Install all other dependencies
    req_file = os.path.join(ROOT, "requirements.txt")
    run(f"{PIP} install -r {req_file}", "Installing dependencies from requirements.txt")

    # 5. Install Playwright browser
    run(f"{PYTHON} -m playwright install chromium", "Downloading Playwright Chromium browser")

    # 6. Verify
    print(f"\n{'='*60}")
    print("  Verifying installation...")
    print(f"{'='*60}\n")
    verify_cmd = (
        f'{PYTHON} -c "'
        f"import sys; sys.path.insert(0, r'{os.path.join(os.path.dirname(ROOT), 'open-interpreter')}'); "
        f"from interpreter import interpreter; "
        f"import bs4, playwright, requests, tenacity, jsonschema, yaml, tqdm, lxml; "
        f"print('  All imports OK'); "
        f"print(f'  Python: {{sys.version}}'); "
        f"print(f'  Open Interpreter model: {{interpreter.llm.model}}')"
        f'"'
    )
    result = subprocess.run(verify_cmd, shell=True, cwd=ROOT)
    if result.returncode != 0:
        print("\n  WARNING: Verification failed. Some imports may be missing.")
    
    # 7. Done
    print(f"\n{'='*60}")
    print("  Setup complete!")
    print(f"{'='*60}")
    print()
    if IS_WINDOWS:
        print(f"  Activate the venv:   .venv\\Scripts\\Activate.ps1")
    else:
        print(f"  Activate the venv:   source .venv/bin/activate")
    print(f"  Run the pipeline:    python run_pipeline.py --site quebec --model gpt-4o")
    print()
    print(f"  Don't forget to:")
    print(f"    1. Set your API key (e.g. OPENAI_API_KEY)")
    print(f"    2. Add your prompt to config/prompt.txt")
    print()


if __name__ == "__main__":
    main()
