#!/usr/bin/env python3
"""
Test script for 11Labs Speech-to-Text API using the official SDK
Based on: https://elevenlabs.io/docs/cookbooks/speech-to-text/quickstart
"""

import os
from elevenlabs_stt_client import ElevenLabsSTTClient
from dotenv import load_dotenv

def main():
    """Test the 11Labs Speech-to-Text API with your audio file"""
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
    print("\nTesting 11Labs Speech-to-Text API...")
    try:
        client = ElevenLabsSTTClient()
        
        # Test with different configurations
        print("\n1. Basic transcription (English, no diarization):")
        result1 = client.speech_to_text(
            audio_file, 
            language_code="eng", 
            diarize=False, 
            tag_audio_events=False
        )
        
        if result1["success"]:
            print("SUCCESS: Basic transcription completed!")
            print(f"Text: {result1['text']}")
        else:
            print(f"ERROR: {result1['error']}")
        
        print("\n2. Advanced transcription (with diarization and audio events):")
        result2 = client.speech_to_text(
            audio_file, 
            language_code="eng", 
            diarize=True, 
            tag_audio_events=True
        )
        
        if result2["success"]:
            print("SUCCESS: Advanced transcription completed!")
            print(f"Text: {result2['text']}")
            print(f"Model: {result2['model']}")
            print(f"Language: {result2['language']}")
            print(f"Diarization: {result2['diarize']}")
            print(f"Audio Events: {result2['tag_audio_events']}")
        else:
            print(f"ERROR: {result2['error']}")
        
        # Show available models
        print("\n3. Available models:")
        models = client.get_available_models()
        if models["success"]:
            for model in models["models"]:
                print(f"  - {model['name']} ({model['model_id']})")
                print(f"    Description: {model['description']}")
                print(f"    Languages: {', '.join(model['supported_languages'])}")
                print(f"    Features: {', '.join(model['features'])}")
        
    except Exception as e:
        print(f"ERROR: Exception during transcription: {e}")
        print("Make sure you have installed the 11Labs SDK:")
        print("pip install elevenlabs")

if __name__ == "__main__":
    main()
