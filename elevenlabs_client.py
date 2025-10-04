import requests
import json
import os
from typing import Optional, Dict, Any
from config import Config

class ElevenLabsClient:
    """Client for interacting with 11Labs Speech-to-Text API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the 11Labs client
        
        Args:
            api_key: 11Labs API key. If not provided, will use from config
        """
        self.api_key = api_key or Config.ELEVENLABS_API_KEY
        self.base_url = Config.ELEVENLABS_BASE_URL
        
        if not self.api_key:
            raise ValueError("API key is required. Please provide it or set ELEVENLABS_API_KEY in your environment.")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def speech_to_text(self, audio_file_path: str, model: str = "scribe_v1") -> Dict[str, Any]:
        """
        Convert speech to text using 11Labs Scribe API
        
        Args:
            audio_file_path: Path to the audio file
            model: Model to use for speech recognition (default: scribe_v1)
            
        Returns:
            Dictionary containing the transcribed text and metadata
        """
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        
        # Prepare the request
        url = f"{self.base_url}/speech-to-text"
        
        headers = {
            "xi-api-key": self.api_key
        }
        
        # Read the audio file
        with open(audio_file_path, 'rb') as audio_file:
            files = {
                'audio': (os.path.basename(audio_file_path), audio_file, 'audio/mpeg')
            }
            
            data = {
                'model': model
            }
            
            try:
                response = requests.post(url, headers=headers, files=files, data=data)
                response.raise_for_status()
                
                result = response.json()
                return {
                    "success": True,
                    "text": result.get("text", ""),
                    "model": model,
                    "confidence": result.get("confidence", 0.0),
                    "language": result.get("language", "en"),
                    "timestamps": result.get("timestamps", []),
                    "speakers": result.get("speakers", []),
                    "raw_response": result
                }
                
            except requests.exceptions.RequestException as e:
                return {
                    "success": False,
                    "error": str(e),
                    "text": "",
                    "model": model
                }
    
    def get_available_models(self) -> Dict[str, Any]:
        """
        Get list of available speech-to-text models
        
        Returns:
            Dictionary containing available models
        """
        url = f"{self.base_url}/models"
        headers = self._get_headers()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "models": []
            }
    
    def get_usage_info(self) -> Dict[str, Any]:
        """
        Get API usage information
        
        Returns:
            Dictionary containing usage statistics
        """
        url = f"{self.base_url}/user"
        headers = self._get_headers()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }
