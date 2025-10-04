#!/usr/bin/env python3
"""
11Labs Speech-to-Text API client using the official SDK
Based on: https://elevenlabs.io/docs/cookbooks/speech-to-text/quickstart
"""

import os
from io import BytesIO
from typing import Dict, Any, Optional
from dotenv import load_dotenv

try:
    from elevenlabs.client import ElevenLabs
    ELEVENLABS_SDK_AVAILABLE = True
except ImportError:
    ELEVENLABS_SDK_AVAILABLE = False

class ElevenLabsSTTClient:
    """Client for 11Labs Speech-to-Text API using official SDK"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the 11Labs STT client
        
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
    
    def speech_to_text(self, audio_file_path: str, model_id: str = "scribe_v1", 
                      tag_audio_events: bool = True, language_code: str = "eng", 
                      diarize: bool = True) -> Dict[str, Any]:
        """
        Convert speech to text using 11Labs Speech-to-Text API
        
        Args:
            audio_file_path: Path to the audio file
            model_id: Model to use (default: scribe_v1)
            tag_audio_events: Tag audio events like laughter, applause, etc.
            language_code: Language of the audio file (eng, spa, fra, etc.)
            diarize: Whether to annotate who is speaking
            
        Returns:
            Dictionary containing the transcribed text and metadata
        """
        if not os.path.exists(audio_file_path):
            return {"success": False, "error": f"File not found: {audio_file_path}"}
        
        try:
            # Read the audio file
            with open(audio_file_path, 'rb') as audio_file:
                audio_data = BytesIO(audio_file.read())
            
            # Use the 11Labs Speech-to-Text API
            transcription = self.client.speech_to_text.convert(
                file=audio_data,
                model_id=model_id,
                tag_audio_events=tag_audio_events,
                language_code=language_code,
                diarize=diarize
            )
            
            return {
                "success": True,
                "text": transcription.text if hasattr(transcription, 'text') else str(transcription),
                "model": model_id,
                "language": language_code,
                "diarize": diarize,
                "tag_audio_events": tag_audio_events,
                "raw_response": transcription
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "text": "",
                "model": model_id
            }
    
    def get_available_models(self) -> Dict[str, Any]:
        """
        Get available Speech-to-Text models
        
        Returns:
            Dictionary containing available models
        """
        # For now, only scribe_v1 is supported according to the documentation
        return {
            "success": True,
            "models": [
                {
                    "model_id": "scribe_v1",
                    "name": "Scribe v1",
                    "description": "State-of-the-art speech recognition model",
                    "supported_languages": ["eng", "spa", "fra", "deu", "ita", "por", "rus", "jpn", "kor", "chi"],
                    "features": ["diarization", "audio_event_tagging", "word_timestamps"]
                }
            ]
        }

# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        client = ElevenLabsSTTClient()
        print("11Labs Speech-to-Text client created successfully!")
        print("Available models:", client.get_available_models())
        print("Add your ELEVENLABS_API_KEY to .env file and test with an audio file.")
    except Exception as e:
        print(f"Error: {e}")
        print("Please install the 11Labs SDK: pip install elevenlabs")
