    #!/usr/bin/env python3
"""
Setup script for the Modern Socratic Method CLI.
This script helps configure API keys and other settings.
"""

import json
import os
from pathlib import Path
from getpass import getpass

def setup_config():
    """Setup configuration file for Modern Socratic Method."""
    config_path = Path.home() / ".socratic_config.json"
    
    # Load existing config or create new one
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                print(f"Found existing config at {config_path}")
        except Exception:
            config = {}
    else:
        config = {}
    
    # Get DeepSeek API key
    print("\n=== DeepSeek API Configuration ===")
    print("The Modern Socratic Method requires a DeepSeek API key.")
    print("You can obtain an API key from https://platform.deepseek.com/")
    
    # Show current key if exists
    current_key = config.get("deepseek_api_key")
    if current_key:
        masked_key = current_key[:4] + "*" * (len(current_key) - 8) + current_key[-4:] if len(current_key) > 8 else "****"
        print(f"Current API key: {masked_key}")
        update = input("Do you want to update your API key? (y/n): ").lower() == 'y'
    else:
        update = True
    
    # Update key if needed
    if update:
        api_key = getpass("Enter your DeepSeek API key: ")
        if api_key:
            config["deepseek_api_key"] = api_key
            print("API key updated.")
        else:
            print("No API key provided, keeping existing configuration.")
    
    # Save config
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"\nConfiguration saved to {config_path}")
    print("You can now run the application with 'python socratic_cli.py'")

if __name__ == "__main__":
    try:
        setup_config()
    except KeyboardInterrupt:
        print("\nSetup interrupted. Configuration may not be complete.")
    except Exception as e:
        print(f"Error during setup: {e}")

from setuptools import setup, find_packages

setup(
    name="modern-socratic-method",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "anthropic>=0.18.0",
        "requests>=2.31.0",
        "rich>=13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "socratic=src.socratic_cli:main",
        ],
    },
    python_requires=">=3.8",
    author="Claude Code",
    description="A CLI for Modern Socratic Method dialogues with AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)