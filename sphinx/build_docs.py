#!/usr/bin/env python3
"""
Build script for RAG Search Flow documentation.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Build the documentation."""
    print("Building RAG Search Flow documentation...")
    
    # Change to the sphinx directory
    sphinx_dir = Path(__file__).parent
    os.chdir(sphinx_dir)
    
    # Check if we're on Windows
    if os.name == 'nt':
        # Windows
        cmd = ["./make.bat", "html"]
    else:
        # Unix-like systems
        cmd = ["make", "html"]
    
    try:
        # Run the build command
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Documentation built successfully!")
        print(f"Output directory: {sphinx_dir / '_build' / 'html'}")
        print(f"Open {sphinx_dir / '_build' / 'html' / 'index.html'} in your browser to view the documentation.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error building documentation: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Make command not found. Please ensure you have the necessary build tools installed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
