#!/usr/bin/env python3
"""
Friday AI Assistant - CLI Launcher
Lightweight standalone CLI - no web server needed!
"""

import sys
import subprocess
import os

def main():
    # Make sure we're in the project directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Run the CLI
    subprocess.run([sys.executable, "cli.py"] + sys.argv[1:])

if __name__ == "__main__":
    main()
