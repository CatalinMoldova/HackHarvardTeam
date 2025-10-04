#!/usr/bin/env python3
"""
11Labs Text-to-Speech API client using the official SDK
Based on: https://elevenlabs.io/docs/cookbooks/text-to-speech/quickstart
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import play
    ELEVENLABS_SDK_AVAILABLE = True
except ImportError:
    ELEVENLABS_SDK_AVAILABLE = False

class ElevenLabsTTSClient:
    """Client for 11Labs Text-to-Speech API using official SDK"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the 11Labs TTS client
        
        Args:
            api_key: 11Labs API key. If not provided, will use from environment
        """
        if not ELEVENLABS_SDK_AVAILABLE:
            raise ImportError("11Labs SDK not installed. Run: pip install elevenlabs")
        
        load_dotenv()
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        
        if not self.api_key:
            raise ValueError("11Labs API key is required. Please set ELEVENLABS_API_KEY in your .env file.")
        
        self.client = ElevenLabs(api_key=self.api_key)
    
    def text_to_speech(self, text: str, voice_id: str = "JBFqnCBsd6RMkjVDRZzb", 
                      model_id: str = "eleven_multilingual_v2", 
                      output_format: str = "mp3_44100_128",
                      save_to_file: bool = False, 
                      filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert text to speech using 11Labs Text-to-Speech API
        
        Args:
            text: Text to convert to speech
            voice_id: Voice ID to use (default: JBFqnCBsd6RMkjVDRZzb)
            model_id: Model to use (default: eleven_multilingual_v2)
            output_format: Output format (default: mp3_44100_128)
            save_to_file: Whether to save audio to file
            filename: Custom filename for saved audio
            
        Returns:
            Dictionary containing the audio data and metadata
        """
        try:
            # Generate speech
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id=model_id,
                output_format=output_format
            )
            
            result = {
                "success": True,
                "text": text,
                "voice_id": voice_id,
                "model_id": model_id,
                "output_format": output_format,
                "audio_data": audio,
                "audio_size": len(audio) if audio else 0
            }
            
            # Save to file if requested
            if save_to_file:
                if not filename:
                    filename = f"tts_output_{voice_id}_{model_id}.mp3"
                
                with open(filename, 'wb') as f:
                    f.write(audio)
                
                result["saved_file"] = filename
                result["file_size"] = os.path.getsize(filename)
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "text": text,
                "voice_id": voice_id,
                "model_id": model_id
            }
    
    def play_audio(self, audio_data: bytes) -> bool:
        """
        Play audio through speakers
        
        Args:
            audio_data: Audio data to play
            
        Returns:
            True if successful, False otherwise
        """
        try:
            play(audio_data)
            return True
        except Exception as e:
            print(f"Error playing audio: {e}")
            return False
    
    def get_available_voices(self) -> Dict[str, Any]:
        """
        Get available voices
        
        Returns:
            Dictionary containing available voices
        """
        try:
            voices = self.client.voices.get_all()
            return {
                "success": True,
                "voices": voices,
                "count": len(voices) if voices else 0
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "voices": []
            }
    
    def get_available_models(self) -> Dict[str, Any]:
        """
        Get available TTS models
        
        Returns:
            Dictionary containing available models
        """
        try:
            models = self.client.models.get_all()
            return {
                "success": True,
                "models": models,
                "count": len(models) if models else 0
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "models": []
            }

# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        client = ElevenLabsTTSClient()
        print("11Labs Text-to-Speech client created successfully!")
        print("Available voices:", client.get_available_voices())
        print("Available models:", client.get_available_models())
        print("Add your ELEVENLABS_API_KEY to .env file and test with text.")
    except Exception as e:
        print(f"Error: {e}")
        print("Please install the 11Labs SDK: pip install elevenlabs")
