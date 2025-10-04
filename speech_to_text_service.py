from elevenlabs_client import ElevenLabsClient
from config import Config
import os
from typing import Optional, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpeechToTextService:
    """High-level service for speech-to-text operations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the speech-to-text service
        
        Args:
            api_key: 11Labs API key. If not provided, will use from config
        """
        try:
            Config.validate_config()
            self.client = ElevenLabsClient(api_key)
            logger.info("Speech-to-Text service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize service: {e}")
            raise
    
    def transcribe_audio(self, audio_file_path: str, model: str = None) -> Dict[str, Any]:
        """
        Transcribe audio file to text
        
        Args:
            audio_file_path: Path to the audio file
            model: Model to use for transcription (optional)
            
        Returns:
            Dictionary containing transcription results
        """
        if not os.path.exists(audio_file_path):
            return {
                "success": False,
                "error": f"Audio file not found: {audio_file_path}",
                "text": ""
            }
        
        model = model or Config.STT_MODEL
        logger.info(f"Transcribing audio file: {audio_file_path} using model: {model}")
        
        result = self.client.speech_to_text(audio_file_path, model)
        
        if result.get("success", False):
            logger.info(f"Transcription successful. Text length: {len(result.get('text', ''))}")
        else:
            logger.error(f"Transcription failed: {result.get('error', 'Unknown error')}")
        
        return result
    
    def transcribe_multiple_files(self, audio_files: list, model: str = None) -> Dict[str, Any]:
        """
        Transcribe multiple audio files
        
        Args:
            audio_files: List of audio file paths
            model: Model to use for transcription (optional)
            
        Returns:
            Dictionary containing results for all files
        """
        results = {
            "success": True,
            "total_files": len(audio_files),
            "successful_transcriptions": 0,
            "failed_transcriptions": 0,
            "results": []
        }
        
        for i, audio_file in enumerate(audio_files):
            logger.info(f"Processing file {i+1}/{len(audio_files)}: {audio_file}")
            
            result = self.transcribe_audio(audio_file, model)
            result["file_index"] = i
            result["file_path"] = audio_file
            
            results["results"].append(result)
            
            if result.get("success", False):
                results["successful_transcriptions"] += 1
            else:
                results["failed_transcriptions"] += 1
        
        results["success"] = results["failed_transcriptions"] == 0
        logger.info(f"Batch transcription completed. Success: {results['successful_transcriptions']}, Failed: {results['failed_transcriptions']}")
        
        return results
    
    def get_service_info(self) -> Dict[str, Any]:
        """
        Get information about the service and available models
        
        Returns:
            Dictionary containing service information
        """
        models_info = self.client.get_available_models()
        usage_info = self.client.get_usage_info()
        
        return {
            "service": "11Labs Speech-to-Text",
            "models": models_info,
            "usage": usage_info,
            "config": {
                "default_model": Config.STT_MODEL,
                "audio_format": Config.AUDIO_FORMAT,
                "audio_quality": Config.AUDIO_QUALITY
            }
        }
