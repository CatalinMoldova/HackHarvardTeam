import requests
import os
from typing import Dict, Any

class SimpleElevenLabsClient:
    """Simple 11Labs client without complex dependencies"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        self.base_url = "https://api.elevenlabs.io/v1"
        
        if not self.api_key:
            raise ValueError("API key is required")
    
    def speech_to_text(self, audio_file_path: str) -> Dict[str, Any]:
        """Convert speech to text using 11Labs API"""
        if not os.path.exists(audio_file_path):
            return {"success": False, "error": f"File not found: {audio_file_path}"}
        
        url = f"{self.base_url}/speech-to-text"
        headers = {"xi-api-key": self.api_key}
        
        try:
            with open(audio_file_path, 'rb') as audio_file:
                files = {'audio': (os.path.basename(audio_file_path), audio_file, 'audio/mpeg')}
                data = {'model': 'scribe_v1'}
                
                response = requests.post(url, headers=headers, files=files, data=data)
                response.raise_for_status()
                
                result = response.json()
                return {
                    "success": True,
                    "text": result.get("text", ""),
                    "model": "scribe_v1",
                    "language": result.get("language", "en"),
                    "timestamps": result.get("timestamps", []),
                    "speakers": result.get("speakers", [])
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    client = SimpleElevenLabsClient()
    print("Simple 11Labs client created successfully!")
    print("Add your API key to .env file and test with an audio file.")
