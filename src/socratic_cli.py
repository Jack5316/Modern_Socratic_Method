#!/usr/bin/env python3
"""
Modern Socratic Method CLI
A terminal-based application that allows users to engage in Socratic dialogue
with AI models (DeepSeek and Claude).
"""

import argparse
import json
import os
import sys
import time
from typing import Dict, List, Optional, Union
from pathlib import Path

import anthropic
import requests
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress


class DeepSeekClient:
    """Client for DeepSeek API interactions."""
    
    def __init__(self, api_key: str):
        self.api_key = "sk-3b6c7e8f5cd3409799296b2459515d89"
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def generate_response(self, messages: List[Dict], temperature: float = 0.7) -> str:
        """Generate a response from DeepSeek API."""
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            print(f"[bold red]Error with DeepSeek API: {e}[/bold red]")
            return "I apologize, but I encountered an error connecting to my reasoning capabilities."


class ClaudeDesktopClient:
    """Client for Claude Desktop MCP interactions."""
    
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate_response(self, messages: List[Dict], temperature: float = 0.7) -> str:
        """Generate a response from Claude Desktop MCP."""
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4000,
                temperature=temperature,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            print(f"[bold red]Error with Claude API: {e}[/bold red]")
            return "I apologize, but I encountered an error connecting to my reasoning capabilities."


class SocraticDialog:
    """Manages the Socratic dialogue flow."""
    
    def __init__(self, model: str = "deepseek", api_key: Optional[str] = None):
        self.console = Console()
        self.history = []
        
        # Claude is disabled, only DeepSeek is available
        if model == "claude":
            raise ValueError("Claude API is currently disabled. Please use 'deepseek' model instead.")
            
        # Setup the AI client (DeepSeek only)
        if not api_key:
            # Try to get API key from environment variable
            api_key = os.environ.get("DEEPSEEK_API_KEY")
            
            # If not found, try to load from config file
            if not api_key:
                config_path = Path.home() / ".socratic_config.json"
                if config_path.exists():
                    try:
                        with open(config_path, "r") as f:
                            config = json.load(f)
                            api_key = config.get("deepseek_api_key")
                    except Exception as e:
                        self.console.print(f"[yellow]Warning: Failed to read config file: {e}[/yellow]")
                
                # If still no API key, raise error with helpful message
                if not api_key:
                    raise ValueError(
                        "DeepSeek API key required. You can provide it in one of these ways:\n"
                        "1. Set DEEPSEEK_API_KEY environment variable:\n"
                        "   export DEEPSEEK_API_KEY=\"your-api-key\"\n"
                        "2. Provide with --api-key command line option:\n"
                        "   python socratic_cli.py --api-key \"your-api-key\"\n"
                        "3. Run the setup script to configure your API key:\n"
                        "   python setup.py\n"
                        "4. Manually create a config file at ~/.socratic_config.json with:\n"
                        '   {"deepseek_api_key": "YOUR_API_KEY_HERE"}'
                    )
        
        self.client = DeepSeekClient(api_key)
        
        # Initialize with Socratic context
        self.history = [
            {"role": "system", "content": """You are Socrates, the ancient Greek philosopher known for the Socratic method of questioning.
Your goal is to help the user explore a topic deeply through insightful questions using the CRITIC model:

C - Clarification: Begin by asking questions that clarify the user's understanding and define key terms.
R - Refute Assumptions: Gently challenge underlying assumptions in the user's thinking.
I - Identify Evidence: Ask for supporting evidence or examples behind their reasoning.
T - Thinking from different perspectives: Prompt them to consider alternative viewpoints.
I - Investigate potential consequences: Explore where their ideas might lead if taken to their logical conclusion.
C - Circle back to the original question: Connect insights gained to the core question being discussed.

Guidelines:
1. Never directly answer the user's questions. Instead, respond with probing questions.
2. Ask one question at a time, focusing on clarity and depth.
3. Keep responses concise and thought-provoking - avoid lengthy explanations.
4. Be patient and respectful, but persistent in pursuing deeper understanding.
5. Avoid sharing your own opinions or direct knowledge.
6. Guide the user to discover answers through their own reasoning.
7. After a meaningful dialogue (typically 5-10 exchanges), you may choose to end the conversation 
   by including "[END_CONVERSATION]" at the end of your response. This will trigger a summary 
   of key insights and a relevant philosophical quote.

Remember: Keep conversations insightful but moderate in length to maintain engagement."""}
        ]

    def format_ai_message(self, message: str) -> None:
        """Format and display AI messages."""
        self.console.print(Panel(
            Markdown(message),
            title="[bold cyan]Socrates[/bold cyan]",
            border_style="cyan"
        ))

    def format_user_message(self, message: str) -> None:
        """Format and display user messages."""
        self.console.print(Panel(
            message,
            title="[bold green]You[/bold green]",
            border_style="green"
        ))

    def thinking_animation(self, seconds: int = 2) -> None:
        """Display a thinking animation."""
        with Progress() as progress:
            task = progress.add_task("[cyan]Socrates is thinking...", total=100)
            while not progress.finished:
                progress.update(task, advance=1)
                time.sleep(seconds/100)

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.history.append({"role": role, "content": content})

    def get_response(self, temperature: float = 0.7) -> str:
        """Get a response from the AI model."""
        self.thinking_animation()
        response = self.client.generate_response(self.history, temperature)
        return response

    def check_for_conversation_end(self, response: str) -> tuple[str, bool]:
        """Check if Socrates wants to end the conversation."""
        if "[END_CONVERSATION]" in response:
            # Remove the end marker from the displayed response
            cleaned_response = response.replace("[END_CONVERSATION]", "").strip()
            return cleaned_response, True
        return response, False

    def end_conversation_with_summary(self) -> None:
        """Generate and display a summary of key takeaways and an insightful quote."""
        self.console.print("\n[bold yellow]Generating conversation summary...[/bold yellow]")
        
        # Create a prompt for generating the summary and quote
        summary_prompt = (
            "Please review our conversation and provide: "
            "1. A concise summary of 3-5 key takeaways or insights from our dialogue. "
            "2. One insightful and meaningful philosophical quote that relates to our discussion "
            "and could inspire further reflection. Keep your entire response under 300 words."
        )
        
        # Save current history and create new request
        original_history = self.history.copy()
        self.add_message("user", summary_prompt)
        
        # Get the summary response
        summary_response = self.get_response(temperature=0.7)
        
        # Display the summary
        self.console.print(Panel(
            Markdown(summary_response),
            title="[bold magenta]Conversation Summary[/bold magenta]",
            border_style="magenta"
        ))
        
        # Restore original history (don't include summary in saved history)
        self.history = original_history

    def start_dialog(self, topic: Optional[str] = None, temperature: float = 0.7) -> None:
        """Start the Socratic dialogue."""
        self.console.clear()
        self.console.print("[bold]Welcome to the Modern Socratic Method[/bold]")
        self.console.print("Type 'exit' or 'quit' to end the conversation.\n")
        
        # If topic provided, use it to prime the conversation
        if topic:
            initial_prompt = f"The user wants to discuss: {topic}. Begin the Socratic dialogue with an appropriate opening question."
            self.add_message("user", initial_prompt)
            response = self.get_response(temperature)
            self.add_message("assistant", response)
            self.format_ai_message(response)
        
        # Main conversation loop
        while True:
            user_input = self.console.input("\n[bold green]Your response: [/bold green]")
            
            if user_input.lower() in ["exit", "quit"]:
                self.console.print("\n[bold]Ending conversation...[/bold]")
                # Generate and show summary before exiting
                if len(self.history) > 1:  # Only if we've had some conversation
                    self.end_conversation_with_summary()
                self.console.print("\n[bold]Farewell![/bold]")
                break
            
            self.format_user_message(user_input)
            self.add_message("user", user_input)
            
            response = self.get_response(temperature)
            cleaned_response, should_end = self.check_for_conversation_end(response)
            
            # Add the cleaned response to history and display it
            self.add_message("assistant", cleaned_response)
            self.format_ai_message(cleaned_response)
            
            # If Socrates decides to end the conversation
            if should_end:
                self.console.print("\n[bold yellow]Socrates has guided the dialogue to a conclusion...[/bold yellow]")
                self.end_conversation_with_summary()
                self.console.print("\n[bold]Farewell![/bold]")
                break


def save_api_key(api_key: str) -> None:
    """Save the API key to the config file."""
    config_path = Path.home() / ".socratic_config.json"
    
    # Load existing config or create new one
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except Exception:
            config = {}
    else:
        config = {}
    
    # Update with new API key
    config["deepseek_api_key"] = api_key
    
    # Save config
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"[green]API key saved to {config_path}[/green]")


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(description="Modern Socratic Method CLI")
    parser.add_argument("--model", choices=["deepseek"], default="deepseek",
                      help="AI model to use (default: deepseek)")
    parser.add_argument("--api-key", type=str, help="API key for the selected model")
    parser.add_argument("--topic", type=str, help="Initial topic to discuss")
    parser.add_argument("--temperature", type=float, default=0.7,
                      help="Temperature for response generation (0.0-1.0)")
    parser.add_argument("--save-api-key", action="store_true",
                      help="Save the provided API key to config file")
    
    args = parser.parse_args()
    
    try:
        # Save API key if requested
        if args.save_api_key and args.api_key:
            save_api_key(args.api_key)
        
        dialog = SocraticDialog(model=args.model, api_key=args.api_key)
        dialog.start_dialog(topic=args.topic, temperature=args.temperature)
    except KeyboardInterrupt:
        print("\nConversation interrupted. Farewell!")
    except Exception as e:
        print(f"[bold red]Error: {e}[/bold red]")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())