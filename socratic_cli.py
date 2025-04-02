#!/usr/bin/env python3
"""
Wrapper script for running the Modern Socratic Method CLI from the project root.
"""

import sys
import os

# Add the src directory to the Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

# Import and run the main function from the actual script
try:
    from socratic_cli import main
    sys.exit(main())
except ImportError as e:
    print(f"Error importing module: {e}")
    print("Make sure you're in the correct directory.")
    sys.exit(1)
