#!/bin/bash

# Example script to run the Modern Socratic Method CLI
# Before running, make sure to install requirements: pip install -r requirements.txt

# Simple run using Claude Desktop
echo "Running with Claude Desktop..."
python src/socratic_cli.py --topic "What is the nature of knowledge?"

# To run with DeepSeek API (uncomment and add your API key)
# export DEEPSEEK_API_KEY="your-api-key-here"
# python src/socratic_cli.py --model deepseek --topic "What is virtue?"

# Advanced run with custom temperature
# python src/socratic_cli.py --model claude --topic "What is justice?" --temperature 0.9