#!/usr/bin/env python3
"""
Complete 11Labs Audio Service - Speech-to-Text and Text-to-Speech
Combines both STT and TTS capabilities in one service
"""

import requests
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class ElevenLabsAudioService:
    """Complete audio service with both STT and TTS capabilities"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the 11Labs Audio Service
        
        Args:
            api_key: 11Labs API key. If not provided, will use from environment
        """
        load_dotenv()
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        
        if not self.api_key:
            raise ValueError("11Labs API key is required. Please set ELEVENLABS_API_KEY in your .env file.")
        
        self.base_url = "https://api.elevenlabs.io/v1"
    
    def speech_to_text(self, audio_file_path: str, **kwargs) -> Dict[str, Any]:
        """
        Convert speech to text using 11Labs Speech-to-Text API
        
        Args:
            audio_file_path: Path to the audio file
            **kwargs: Additional parameters (model_id, language_code, diarize, etc.)
            
        Returns:
            Dictionary containing the transcribed text and metadata
        """
        if not os.path.exists(audio_file_path):
            return {"success": False, "error": f"File not found: {audio_file_path}"}
        
        url = f"{self.base_url}/speech-to-text"
        headers = {"xi-api-key": self.api_key}
        
        # Default parameters
        params = {
            'model_id': kwargs.get('model_id', 'scribe_v1'),
            'tag_audio_events': str(kwargs.get('tag_audio_events', True)).lower(),
            'language_code': kwargs.get('language_code', 'eng'),
            'diarize': str(kwargs.get('diarize', True)).lower()
        }
        
        try:
            with open(audio_file_path, 'rb') as audio_file:
                files = {'file': (os.path.basename(audio_file_path), audio_file, 'audio/mp4')}
                
                response = requests.post(url, headers=headers, files=files, data=params, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "text": result.get("text", ""),
                        "language": result.get("language_code", "unknown"),
                        "confidence": result.get("language_probability", 0.0),
                        "words": result.get("words", []),
                        "transcription_id": result.get("transcription_id", ""),
                        "raw_response": result
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API error: {response.status_code}",
                        "response": response.text
                    }
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def text_to_speech(self, text: str, **kwargs) -> Dict[str, Any]:
        """
        Convert text to speech using 11Labs Text-to-Speech API
        
        Args:
            text: Text to convert to speech
            **kwargs: Additional parameters (voice_id, model_id, output_format, etc.)
            
        Returns:
            Dictionary containing the audio data and metadata
        """
        # Default parameters
        voice_id = kwargs.get('voice_id', 'JBFqnCBsd6RMkjVDRZzb')
        
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        model_id = kwargs.get('model_id', 'eleven_multilingual_v2')
        
        data = {
            "text": text,
            "model_id": model_id,
            "output_format": kwargs.get('output_format', 'mp3_44100_128')
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
                    "audio_data": audio_data,
                    "audio_size": len(audio_data)
                }
                
                # Save to file if requested
                if kwargs.get('save_to_file', False):
                    filename = kwargs.get('filename', f"tts_output_{voice_id}.mp3")
                    with open(filename, 'wb') as f:
                        f.write(audio_data)
                    result["saved_file"] = filename
                
                return result
            else:
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}",
                    "response": response.text
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def transcribe_and_speak(self, audio_file_path: str, **kwargs) -> Dict[str, Any]:
        """
        Complete workflow: Transcribe audio to text, then convert back to speech
        
        Args:
            audio_file_path: Path to the audio file
            **kwargs: Additional parameters for both STT and TTS
            
        Returns:
            Dictionary containing both transcription and TTS results
        """
        print("Starting transcribe-and-speak workflow...")
        
        # Step 1: Speech to Text
        print("Transcribing audio...")
        stt_result = self.speech_to_text(audio_file_path, **kwargs)
        
        if not stt_result["success"]:
            return {
                "success": False,
                "error": f"STT failed: {stt_result['error']}",
                "stt_result": stt_result
            }
        
        print(f"SUCCESS: Transcription: {stt_result['text']}")
        
        # Step 2: Text to Speech
        print("Converting text to speech...")
        tts_result = self.text_to_speech(
            stt_result["text"], 
            save_to_file=True,
            filename=f"processed_{os.path.basename(audio_file_path)}.mp3",
            **kwargs
        )
        
        if not tts_result["success"]:
            return {
                "success": False,
                "error": f"TTS failed: {tts_result['error']}",
                "stt_result": stt_result,
                "tts_result": tts_result
            }
        
        print(f"SUCCESS: Audio generated: {tts_result.get('saved_file', 'Not saved')}")
        
        return {
            "success": True,
            "original_audio": audio_file_path,
            "transcribed_text": stt_result["text"],
            "processed_audio": tts_result.get("saved_file"),
            "stt_result": stt_result,
            "tts_result": tts_result
        }
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get information about the service"""
        return {
            "service": "11Labs Complete Audio Service",
            "capabilities": ["Speech-to-Text", "Text-to-Speech", "Transcribe-and-Speak"],
            "api_key_configured": bool(self.api_key),
            "base_url": self.base_url
        }

# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        service = ElevenLabsAudioService()
        print("11Labs Complete Audio Service initialized!")
        print("Service info:", service.get_service_info())
        print("Ready for both Speech-to-Text and Text-to-Speech operations!")
    except Exception as e:
        print(f"Error: {e}")
        print("Please set your ELEVENLABS_API_KEY in the .env file")
