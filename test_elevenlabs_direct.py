#!/usr/bin/env python3
"""
Test 11Labs Speech-to-Text API using direct HTTP requests
Based on: https://elevenlabs.io/docs/cookbooks/speech-to-text/quickstart
"""

import requests
import os
from dotenv import load_dotenv

def test_elevenlabs_stt_direct():
    """Test 11Labs Speech-to-Text API using direct HTTP requests"""
    print("=== 11Labs Speech-to-Text API Direct Test ===")
    
    # Load environment
    load_dotenv()
    api_key = os.getenv('ELEVENLABS_API_KEY')
    
    if not api_key or api_key == 'your_api_key_here':
        print("ERROR: ELEVENLABS_API_KEY not found in .env file")
        print("Please edit .env file and add your API key:")
        print("ELEVENLABS_API_KEY=your_actual_api_key_here")
        return
    
    print("API key loaded successfully")
    
    # Check if audio file exists
    audio_file = "TestAudioFileAPI.m4a"
    if not os.path.exists(audio_file):
        print(f"ERROR: Audio file not found: {audio_file}")
        return
    
    print(f"Found audio file: {audio_file}")
    print(f"File size: {os.path.getsize(audio_file)} bytes")
    
    # Test the Speech-to-Text API
    print("\nTesting 11Labs Speech-to-Text API...")
    
    url = "https://api.elevenlabs.io/v1/speech-to-text"
    headers = {
        "xi-api-key": api_key
    }
    
    try:
        with open(audio_file, 'rb') as audio_file_obj:
            files = {
                'file': (audio_file, audio_file_obj, 'audio/mp4')
            }
            data = {
                'model_id': 'scribe_v1',
                'tag_audio_events': 'true',
                'language_code': 'eng',
                'diarize': 'true'
            }
            
            print("Sending request to 11Labs Speech-to-Text API...")
            response = requests.post(url, headers=headers, files=files, data=data, timeout=60)
            
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("SUCCESS: Transcription completed!")
                print(f"Response: {result}")
            else:
                print(f"ERROR: {response.status_code}")
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"ERROR: Exception during transcription: {e}")

if __name__ == "__main__":
    test_elevenlabs_stt_direct()
