#!/usr/bin/env python3
"""
Test script for 11Labs Text-to-Speech API using direct HTTP requests
"""

import os
from elevenlabs_tts_direct import ElevenLabsTTSDirect
from dotenv import load_dotenv

def test_tts_direct():
    """Test the direct TTS implementation"""
    print("=== 11Labs Text-to-Speech Direct Test ===")
    
    # Load environment
    load_dotenv()
    api_key = os.getenv('ELEVENLABS_API_KEY')
    
    if not api_key or api_key == 'your_api_key_here':
        print("ERROR: ELEVENLABS_API_KEY not found in .env file")
        print("Please edit .env file and add your API key:")
        print("ELEVENLABS_API_KEY=your_actual_api_key_here")
        return False
    
    print("API key loaded successfully")
    
    try:
        client = ElevenLabsTTSDirect()
        
        # Test 1: Basic TTS
        print("\n1. Testing basic text-to-speech...")
        test_text = "The first move is what sets everything in motion."
        
        result1 = client.text_to_speech(
            text=test_text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            save_to_file=True,
            filename="test_tts_basic.mp3"
        )
        
        if result1["success"]:
            print("SUCCESS: Basic TTS completed!")
            print(f"Text: {result1['text']}")
            print(f"Voice ID: {result1['voice_id']}")
            print(f"Model: {result1['model_id']}")
            print(f"Audio size: {result1['audio_size']} bytes")
            print(f"Saved to: {result1.get('saved_file', 'Not saved')}")
        else:
            print(f"ERROR: {result1['error']}")
            return False
        
        # Test 2: Different model
        print("\n2. Testing with different model...")
        result2 = client.text_to_speech(
            text="Hello, this is a test with the Flash model for faster generation.",
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_flash_v2_5",
            save_to_file=True,
            filename="test_tts_flash.mp3"
        )
        
        if result2["success"]:
            print("SUCCESS: Flash model TTS completed!")
            print(f"Audio size: {result2['audio_size']} bytes")
            print(f"Saved to: {result2.get('saved_file', 'Not saved')}")
        else:
            print(f"ERROR: {result2['error']}")
        
        # Test 3: Get available voices
        print("\n3. Testing voice retrieval...")
        voices = client.get_available_voices()
        if voices["success"]:
            print(f"SUCCESS: Found {voices['count']} voices")
            if voices["voices"]:
                print("Sample voices:")
                for i, voice in enumerate(voices["voices"][:3]):
                    print(f"  {i+1}. {voice.get('name', 'Unknown')} (ID: {voice.get('voice_id', 'Unknown')})")
        else:
            print(f"ERROR getting voices: {voices['error']}")
        
        print("\n=== Test Summary ===")
        print("SUCCESS: 11Labs Text-to-Speech API is working!")
        print("Audio files generated and saved")
        print("Ready for text-to-speech operations!")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Exception during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_tts_direct()
    
    if success:
        print("\nTTS testing completed successfully!")
    else:
        print("\nTTS testing failed!")
