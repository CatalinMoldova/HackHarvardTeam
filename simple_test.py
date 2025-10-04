#!/usr/bin/env python3
"""
Simple test for 11Labs Speech-to-Text API
"""

import os
from simple_client import SimpleElevenLabsClient
from dotenv import load_dotenv

def main():
    """Test the API with the audio file"""
    print("=== 11Labs Speech-to-Text API Test ===")
    
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
    
    # Test transcription
    print("\nTesting transcription...")
    try:
        client = SimpleElevenLabsClient()
        result = client.speech_to_text(audio_file)
        
        if result["success"]:
            print("SUCCESS: Transcription completed!")
            print(f"Text: {result['text']}")
            print(f"Language: {result['language']}")
            
            if result.get('timestamps'):
                print(f"Timestamps: {len(result['timestamps'])} word timestamps available")
            
            if result.get('speakers'):
                print(f"Speakers: {len(result['speakers'])} speaker segments detected")
        else:
            print(f"ERROR: Transcription failed: {result['error']}")
            
    except Exception as e:
        print(f"ERROR: Exception during transcription: {e}")

if __name__ == "__main__":
    main()
