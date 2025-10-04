#!/usr/bin/env python3
"""
Test script for 11Labs Speech-to-Text API
This script tests the transcription functionality with available audio files
"""

import os
import glob
from simple_client import SimpleElevenLabsClient
from dotenv import load_dotenv

def load_environment():
    """Load environment variables"""
    load_dotenv()
    
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        print("❌ Error: ELEVENLABS_API_KEY not found in .env file")
        print("Please edit .env file and add your API key:")
        print("ELEVENLABS_API_KEY=your_actual_api_key_here")
        return None
    
    return api_key

def find_audio_files():
    """Find available audio files for testing"""
    audio_extensions = ['*.mp3', '*.wav', '*.m4a', '*.flac', '*.ogg']
    audio_files = []
    
    # Check current directory
    for ext in audio_extensions:
        audio_files.extend(glob.glob(ext))
    
    # Check test_audio directory
    if os.path.exists("test_audio"):
        for ext in audio_extensions:
            audio_files.extend(glob.glob(f"test_audio/{ext}"))
    
    return audio_files

def test_transcription(audio_file):
    """Test transcription of a single audio file"""
    print(f"\n🎵 Testing transcription of: {audio_file}")
    print("=" * 50)
    
    try:
        client = SimpleElevenLabsClient()
        result = client.speech_to_text(audio_file)
        
        if result["success"]:
            print("✅ Transcription successful!")
            print(f"📝 Text: {result['text']}")
            print(f"🌍 Language: {result['language']}")
            
            if result.get('timestamps'):
                print(f"⏱️  Timestamps: {len(result['timestamps'])} word timestamps")
            
            if result.get('speakers'):
                print(f"👥 Speakers: {len(result['speakers'])} speaker segments")
            
            return True
        else:
            print(f"❌ Transcription failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return False

def main():
    """Main test function"""
    print("=== 11Labs Speech-to-Text API Test ===\n")
    
    # Load environment
    api_key = load_environment()
    if not api_key:
        return False
    
    print(f"✅ API key loaded successfully")
    
    # Find audio files
    audio_files = find_audio_files()
    
    if not audio_files:
        print("❌ No audio files found!")
        print("\nTo get audio files:")
        print("1. Run: python download_sample_audio.py")
        print("2. Add your own audio files (MP3, WAV, M4A, etc.)")
        print("3. Record audio using a microphone")
        return False
    
    print(f"📁 Found {len(audio_files)} audio files:")
    for i, file in enumerate(audio_files, 1):
        print(f"  {i}. {file}")
    
    # Test each audio file
    successful_tests = 0
    total_tests = len(audio_files)
    
    for audio_file in audio_files:
        if test_transcription(audio_file):
            successful_tests += 1
    
    # Summary
    print(f"\n=== Test Summary ===")
    print(f"✅ Successful: {successful_tests}/{total_tests}")
    print(f"❌ Failed: {total_tests - successful_tests}/{total_tests}")
    
    if successful_tests > 0:
        print(f"\n🎉 Great! The 11Labs Speech-to-Text API is working correctly!")
        print(f"You can now use the SimpleElevenLabsClient in your applications.")
    else:
        print(f"\n⚠️  All tests failed. Please check:")
        print(f"1. Your API key is correct")
        print(f"2. You have an active 11Labs account")
        print(f"3. Your audio files are in supported formats")
    
    return successful_tests > 0

if __name__ == "__main__":
    main()
