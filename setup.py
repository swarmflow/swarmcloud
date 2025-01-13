# setup.py
#!/usr/bin/env python3
import os
import subprocess
import venv
import sys
from pathlib import Path

class DevEnvironment:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / ".venv"

    def create_venv(self):
        print("Creating virtual environment...")
        venv.create(self.venv_path, with_pip=True, clear=True)
        
        # Get the python and pip executables
        if sys.platform == "win32":
            python = self.venv_path / "Scripts" / "python.exe"
            pip = self.venv_path / "Scripts" / "pip.exe"
        else:
            python = self.venv_path / "bin" / "python"
            pip = self.venv_path / "bin" / "pip"

        # Update pip and install development tools
        subprocess.run([str(pip), "install", "--upgrade", "pip"])
        
        # Install the CLI in editable mode (-e) so it updates as you change the code
        subprocess.run([str(pip), "install", "-e", ".[dev]"])
        
        print("\nDevelopment environment created! To activate:")
        if sys.platform == "win32":
            print("    .venv\\Scripts\\activate")
        else:
            print("    source .venv/bin/activate")

        print("\nAfter activation, the 'aiswarm' command will be available")

if __name__ == "__main__":
    env = DevEnvironment()
    env.create_venv()