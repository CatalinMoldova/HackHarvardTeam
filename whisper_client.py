#!/usr/bin/env python3
"""
OpenAI Whisper API client for speech-to-text
This is an alternative since 11Labs doesn't have speech-to-text
"""

import requests
import os
from typing import Dict, Any
from dotenv import load_dotenv

class WhisperClient:
    """Client for OpenAI Whisper API (speech-to-text)"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Whisper client
        
        Args:
            api_key: OpenAI API key. If not provided, will use from environment
        """
        load_dotenv()
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Please set OPENAI_API_KEY in your .env file.")
        
        self.base_url = "https://api.openai.com/v1"
    
    def speech_to_text(self, audio_file_path: str, model: str = "whisper-1") -> Dict[str, Any]:
        """
        Convert speech to text using OpenAI Whisper API
        
        Args:
            audio_file_path: Path to the audio file
            model: Model to use (default: whisper-1)
            
        Returns:
            Dictionary containing the transcribed text and metadata
        """
        if not os.path.exists(audio_file_path):
            return {"success": False, "error": f"File not found: {audio_file_path}"}
        
        url = f"{self.base_url}/audio/transcriptions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            with open(audio_file_path, 'rb') as audio_file:
                files = {
                    'file': (os.path.basename(audio_file_path), audio_file, 'audio/mpeg'),
                    'model': (None, model),
                    'response_format': (None, 'json')
                }
                
                response = requests.post(url, headers=headers, files=files)
                response.raise_for_status()
                
                result = response.json()
                return {
                    "success": True,
                    "text": result.get("text", ""),
                    "model": model,
                    "language": result.get("language", "unknown"),
                    "raw_response": result
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        client = WhisperClient()
        print("Whisper client created successfully!")
        print("Add your OPENAI_API_KEY to .env file and test with an audio file.")
    except ValueError as e:
        print(f"Error: {e}")
        print("Please add OPENAI_API_KEY to your .env file")
