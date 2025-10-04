#!/usr/bin/env python3
"""
11Labs Text-to-Speech API using direct HTTP requests
Avoids SDK installation issues on Windows
"""

import requests
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class ElevenLabsTTSDirect:
    """11Labs Text-to-Speech using direct HTTP requests"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the 11Labs TTS client
        
        Args:
            api_key: 11Labs API key. If not provided, will use from environment
        """
        load_dotenv()
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        
        if not self.api_key:
            raise ValueError("11Labs API key is required. Please set ELEVENLABS_API_KEY in your .env file.")
        
        self.base_url = "https://api.elevenlabs.io/v1"
    
    def text_to_speech(self, text: str, voice_id: str = "JBFqnCBsd6RMkjVDRZzb", 
                      model_id: str = "eleven_multilingual_v2",
                      output_format: str = "mp3_44100_128",
                      save_to_file: bool = False, 
                      filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert text to speech using 11Labs Text-to-Speech API
        
        Args:
            text: Text to convert to speech
            voice_id: Voice ID to use
            model_id: Model to use
            output_format: Output format
            save_to_file: Whether to save audio to file
            filename: Custom filename for saved audio
            
        Returns:
            Dictionary containing the audio data and metadata
        """
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "text": text,
            "model_id": model_id,
            "output_format": output_format
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            
            if response.status_code == 200:
                audio_data = response.content
                
                result = {
                    "success": True,
                    "text": text,
                    "voice_id": voice_id,
                    "model_id": model_id,
                    "output_format": output_format,
                    "audio_data": audio_data,
                    "audio_size": len(audio_data)
                }
                
                # Save to file if requested
                if save_to_file:
                    if not filename:
                        filename = f"tts_output_{voice_id}_{model_id}.mp3"
                    
                    with open(filename, 'wb') as f:
                        f.write(audio_data)
                    
                    result["saved_file"] = filename
                    result["file_size"] = os.path.getsize(filename)
                
                return result
            else:
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}",
                    "response": response.text
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_available_voices(self) -> Dict[str, Any]:
        """
        Get available voices
        
        Returns:
            Dictionary containing available voices
        """
        url = f"{self.base_url}/voices"
        headers = {"xi-api-key": self.api_key}
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                voices = response.json()
                return {
                    "success": True,
                    "voices": voices.get("voices", []),
                    "count": len(voices.get("voices", []))
                }
            else:
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}",
                    "response": response.text
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        client = ElevenLabsTTSDirect()
        print("11Labs Text-to-Speech client created successfully!")
        
        # Test basic TTS
        result = client.text_to_speech(
            text="Hello, this is a test of the ElevenLabs Text-to-Speech API.",
            save_to_file=True,
            filename="test_tts_direct.mp3"
        )
        
        if result["success"]:
            print("SUCCESS: Audio generated!")
            print(f"Audio size: {result['audio_size']} bytes")
            print(f"Saved to: {result.get('saved_file', 'Not saved')}")
        else:
            print(f"ERROR: {result['error']}")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Please set your ELEVENLABS_API_KEY in the .env file")
