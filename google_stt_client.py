#!/usr/bin/env python3
"""
Google Speech-to-Text API client
Alternative to 11Labs since they don't have speech-to-text
"""

import os
import io
from typing import Dict, Any
from dotenv import load_dotenv

try:
    from google.cloud import speech
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False

class GoogleSTTClient:
    """Client for Google Speech-to-Text API"""
    
    def __init__(self, credentials_path: str = None):
        """
        Initialize the Google STT client
        
        Args:
            credentials_path: Path to Google Cloud credentials JSON file
        """
        if not GOOGLE_CLOUD_AVAILABLE:
            raise ImportError("Google Cloud Speech library not installed. Run: pip install google-cloud-speech")
        
        load_dotenv()
        
        if credentials_path:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        
        self.client = speech.SpeechClient()
    
    def speech_to_text(self, audio_file_path: str, language_code: str = "en-US") -> Dict[str, Any]:
        """
        Convert speech to text using Google Speech-to-Text API
        
        Args:
            audio_file_path: Path to the audio file
            language_code: Language code (default: en-US)
            
        Returns:
            Dictionary containing the transcribed text and metadata
        """
        if not os.path.exists(audio_file_path):
            return {"success": False, "error": f"File not found: {audio_file_path}"}
        
        try:
            with io.open(audio_file_path, "rb") as audio_file:
                content = audio_file.read()
            
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.MP4,
                sample_rate_hertz=44100,
                language_code=language_code,
            )
            
            response = self.client.recognize(config=config, audio=audio)
            
            if response.results:
                text = response.results[0].alternatives[0].transcript
                confidence = response.results[0].alternatives[0].confidence
                
                return {
                    "success": True,
                    "text": text,
                    "confidence": confidence,
                    "language": language_code,
                    "raw_response": response
                }
            else:
                return {
                    "success": False,
                    "error": "No transcription results",
                    "text": ""
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

# Example usage
if __name__ == "__main__":
    if GOOGLE_CLOUD_AVAILABLE:
        try:
            client = GoogleSTTClient()
            print("Google STT client created successfully!")
            print("Make sure you have Google Cloud credentials set up.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Google Cloud Speech library not available.")
        print("Install with: pip install google-cloud-speech")
