#!/usr/bin/env python3
"""
Tests for the Modern Socratic Method CLI
"""

import json
import os
import unittest
from unittest.mock import MagicMock, patch

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from socratic_cli import DeepSeekClient, ClaudeDesktopClient, SocraticDialog


class TestDeepSeekClient(unittest.TestCase):
    """Test cases for DeepSeekClient"""
    
    @patch('requests.post')
    def test_generate_response(self, mock_post):
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Why do you think that?"}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Test the client
        client = DeepSeekClient("fake_api_key")
        messages = [{"role": "user", "content": "What is truth?"}]
        response = client.generate_response(messages)
        
        # Verify results
        self.assertEqual(response, "Why do you think that?")
        mock_post.assert_called_once()
        

class TestClaudeDesktopClient(unittest.TestCase):
    """Test cases for ClaudeDesktopClient"""
    
    @patch('anthropic.Anthropic')
    def test_generate_response(self, mock_anthropic_class):
        # Set up mock response
        mock_anthropic = MagicMock()
        mock_response = MagicMock()
        mock_content = MagicMock()
        mock_content.text = "What makes you ask that question?"
        mock_response.content = [mock_content]
        mock_anthropic.messages.create.return_value = mock_response
        mock_anthropic_class.return_value = mock_anthropic
        
        # Test the client
        client = ClaudeDesktopClient()
        messages = [{"role": "user", "content": "What is virtue?"}]
        response = client.generate_response(messages)
        
        # Verify results
        self.assertEqual(response, "What makes you ask that question?")
        mock_anthropic.messages.create.assert_called_once()


class TestSocraticDialog(unittest.TestCase):
    """Test cases for SocraticDialog"""
    
    def test_add_message(self):
        """Test adding messages to the history."""
        dialog = SocraticDialog()
        initial_length = len(dialog.history)
        
        dialog.add_message("user", "What is knowledge?")
        self.assertEqual(len(dialog.history), initial_length + 1)
        self.assertEqual(dialog.history[-1]["role"], "user")
        self.assertEqual(dialog.history[-1]["content"], "What is knowledge?")


if __name__ == '__main__':
    unittest.main()