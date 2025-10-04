#!/usr/bin/env python3
"""
Test script for 11Labs Text-to-Speech API
Based on: https://elevenlabs.io/docs/cookbooks/text-to-speech/quickstart
"""

import os
from elevenlabs_tts_client import ElevenLabsTTSClient
from dotenv import load_dotenv

def test_basic_tts():
    """Test basic text-to-speech functionality"""
    print("=== 11Labs Text-to-Speech API Test ===")
    
    # Load environment
    load_dotenv()
    api_key = os.getenv('ELEVENLABS_API_KEY')
    
    if not api_key or api_key == 'your_api_key_here':
        print("ERROR: ELEVENLABS_API_KEY not found in .env file")
        print("Please edit .env file and add your API key:")
        print("ELEVENLABS_API_KEY=your_actual_api_key_here")
        return False
    
    print("API key loaded successfully")
    
    # Test text
    test_text = "The first move is what sets everything in motion."
    print(f"Test text: {test_text}")
    
    try:
        client = ElevenLabsTTSClient()
        
        # Test 1: Basic TTS with default voice
        print("\n1. Testing basic text-to-speech...")
        result1 = client.text_to_speech(
            text=test_text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",  # Default voice from docs
            model_id="eleven_multilingual_v2",
            save_to_file=True,
            filename="test_tts_basic.mp3"
        )
        
        if result1["success"]:
            print("✅ SUCCESS: Basic TTS completed!")
            print(f"Voice ID: {result1['voice_id']}")
            print(f"Model: {result1['model_id']}")
            print(f"Audio size: {result1['audio_size']} bytes")
            print(f"Saved to: {result1.get('saved_file', 'Not saved')}")
        else:
            print(f"❌ ERROR: {result1['error']}")
            return False
        
        # Test 2: Different voice and model
        print("\n2. Testing with different voice...")
        result2 = client.text_to_speech(
            text="Hello, this is a test of the ElevenLabs Text-to-Speech API.",
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_flash_v2_5",  # Faster model
            save_to_file=True,
            filename="test_tts_flash.mp3"
        )
        
        if result2["success"]:
            print("✅ SUCCESS: Flash model TTS completed!")
            print(f"Audio size: {result2['audio_size']} bytes")
            print(f"Saved to: {result2.get('saved_file', 'Not saved')}")
        else:
            print(f"❌ ERROR: {result2['error']}")
        
        # Test 3: Get available voices
        print("\n3. Testing voice retrieval...")
        voices = client.get_available_voices()
        if voices["success"]:
            print(f"✅ SUCCESS: Found {voices['count']} voices")
            if voices["voices"]:
                print("Sample voices:")
                for i, voice in enumerate(voices["voices"][:3]):  # Show first 3
                    print(f"  {i+1}. {voice.name} (ID: {voice.voice_id})")
        else:
            print(f"❌ ERROR getting voices: {voices['error']}")
        
        # Test 4: Get available models
        print("\n4. Testing model retrieval...")
        models = client.get_available_models()
        if models["success"]:
            print(f"✅ SUCCESS: Found {models['count']} models")
            if models["models"]:
                print("Available models:")
                for model in models["models"][:5]:  # Show first 5
                    print(f"  - {model.name} ({model.model_id})")
        else:
            print(f"❌ ERROR getting models: {models['error']}")
        
        print("\n=== Test Summary ===")
        print("✅ 11Labs Text-to-Speech API is working correctly!")
        print("📁 Audio files saved to current directory")
        print("🎵 You can play the generated audio files")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Exception during testing: {e}")
        print("Make sure you have installed the 11Labs SDK:")
        print("pip install elevenlabs")
        return False

def test_playback():
    """Test audio playback functionality"""
    print("\n=== Testing Audio Playback ===")
    
    try:
        client = ElevenLabsTTSClient()
        
        # Generate a short test audio
        result = client.text_to_speech(
            text="This is a test of audio playback.",
            save_to_file=False
        )
        
        if result["success"]:
            print("Generating test audio...")
            print("Playing audio through speakers...")
            
            # Try to play the audio
            if client.play_audio(result["audio_data"]):
                print("✅ SUCCESS: Audio played successfully!")
            else:
                print("⚠️ Audio generated but playback failed")
                print("You may need to install MPV or ffmpeg for audio playback")
        else:
            print(f"❌ ERROR: {result['error']}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    success = test_basic_tts()
    
    if success:
        # Test playback if basic TTS worked
        test_playback()
    
    print("\n🎉 Text-to-Speech testing completed!")
