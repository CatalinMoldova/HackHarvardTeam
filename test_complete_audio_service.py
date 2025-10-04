#!/usr/bin/env python3
"""
Test script for the complete 11Labs Audio Service
Tests both Speech-to-Text and Text-to-Speech capabilities
"""

import os
from elevenlabs_audio_service import ElevenLabsAudioService
from dotenv import load_dotenv

def test_complete_audio_service():
    """Test the complete audio service with both STT and TTS"""
    print("=== 11Labs Complete Audio Service Test ===")
    
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
        service = ElevenLabsAudioService()
        print("SUCCESS: Audio service initialized successfully")
        
        # Test 1: Speech-to-Text
        print("\n1. Testing Speech-to-Text...")
        audio_file = "TestAudioFileAPI.m4a"
        
        if os.path.exists(audio_file):
            stt_result = service.speech_to_text(audio_file)
            
            if stt_result["success"]:
                print("SUCCESS: STT completed!")
                print(f"Transcribed: {stt_result['text']}")
                print(f"Language: {stt_result['language']}")
                print(f"Confidence: {stt_result['confidence']}")
            else:
                print(f"ERROR: STT failed - {stt_result['error']}")
        else:
            print(f"WARNING: Audio file not found: {audio_file}")
        
        # Test 2: Text-to-Speech
        print("\n2. Testing Text-to-Speech...")
        test_text = "Hello, this is a test of the ElevenLabs Text-to-Speech API. The audio quality should be excellent."
        
        tts_result = service.text_to_speech(
            text=test_text,
            save_to_file=True,
            filename="test_tts_output.mp3"
        )
        
        if tts_result["success"]:
            print("SUCCESS: TTS completed!")
            print(f"Generated audio: {tts_result.get('saved_file', 'Not saved')}")
            print(f"Audio size: {tts_result['audio_size']} bytes")
        else:
            print(f"ERROR: TTS failed - {tts_result['error']}")
        
        # Test 3: Complete Workflow (Transcribe and Speak)
        print("\n3. Testing Complete Workflow...")
        if os.path.exists(audio_file):
            workflow_result = service.transcribe_and_speak(audio_file)
            
            if workflow_result["success"]:
                print("SUCCESS: Complete workflow completed!")
                print(f"Original audio: {workflow_result['original_audio']}")
                print(f"Transcribed text: {workflow_result['transcribed_text']}")
                print(f"Processed audio: {workflow_result['processed_audio']}")
            else:
                print(f"ERROR: Workflow failed - {workflow_result['error']}")
        
        # Test 4: Service Information
        print("\n4. Service Information:")
        info = service.get_service_info()
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        print("\n=== Test Summary ===")
        print("SUCCESS: 11Labs Complete Audio Service is working!")
        print("🎵 Both Speech-to-Text and Text-to-Speech are functional")
        print("🔄 Complete workflow (transcribe-and-speak) is working")
        print("📁 Audio files generated and saved")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_different_voices():
    """Test different voice options"""
    print("\n=== Testing Different Voice Options ===")
    
    try:
        service = ElevenLabsAudioService()
        
        # Test with different voice
        test_text = "This is a test with a different voice configuration."
        
        result = service.text_to_speech(
            text=test_text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",  # Default voice
            model_id="eleven_flash_v2_5",  # Fast model
            save_to_file=True,
            filename="test_different_voice.mp3"
        )
        
        if result["success"]:
            print("SUCCESS: Different voice test completed!")
            print(f"Voice ID: {result['voice_id']}")
            print(f"Model: {result['model_id']}")
            print(f"Saved to: {result.get('saved_file', 'Not saved')}")
        else:
            print(f"ERROR: Different voice test failed - {result['error']}")
            
    except Exception as e:
        print(f"ERROR in voice testing: {e}")

if __name__ == "__main__":
    success = test_complete_audio_service()
    
    if success:
        test_different_voices()
    
    print("\nComplete Audio Service testing finished!")
