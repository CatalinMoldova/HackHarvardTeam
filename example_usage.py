#!/usr/bin/env python3
"""
Example usage of the 11Labs Speech-to-Text API
"""

import os
import sys
from speech_to_text_service import SpeechToTextService
from config import Config

def main():
    """Main function demonstrating API usage"""
    
    print("=== 11Labs Speech-to-Text API Example ===\n")
    
    try:
        # Initialize the service
        print("Initializing Speech-to-Text service...")
        stt_service = SpeechToTextService()
        print("✓ Service initialized successfully\n")
        
        # Get service information
        print("Getting service information...")
        service_info = stt_service.get_service_info()
        print(f"✓ Service: {service_info.get('service', 'Unknown')}")
        print(f"✓ Default model: {service_info.get('config', {}).get('default_model', 'Unknown')}")
        print()
        
        # Example 1: Single file transcription
        print("=== Example 1: Single File Transcription ===")
        audio_file = "sample_audio.mp3"  # Replace with your audio file path
        
        if os.path.exists(audio_file):
            print(f"Transcribing: {audio_file}")
            result = stt_service.transcribe_audio(audio_file)
            
            if result.get("success", False):
                print(f"✓ Transcription successful!")
                print(f"Text: {result.get('text', '')}")
                print(f"Model: {result.get('model', 'Unknown')}")
                print(f"Language: {result.get('language', 'Unknown')}")
                if 'confidence' in result:
                    print(f"Confidence: {result['confidence']:.2f}")
            else:
                print(f"✗ Transcription failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"⚠ Audio file not found: {audio_file}")
            print("Please provide a valid audio file path to test transcription.")
        
        print()
        
        # Example 2: Multiple files transcription
        print("=== Example 2: Multiple Files Transcription ===")
        audio_files = [
            "audio1.mp3",
            "audio2.wav",
            "audio3.m4a"
        ]
        
        # Filter existing files
        existing_files = [f for f in audio_files if os.path.exists(f)]
        
        if existing_files:
            print(f"Transcribing {len(existing_files)} files...")
            batch_result = stt_service.transcribe_multiple_files(existing_files)
            
            print(f"✓ Batch processing completed!")
            print(f"Total files: {batch_result['total_files']}")
            print(f"Successful: {batch_result['successful_transcriptions']}")
            print(f"Failed: {batch_result['failed_transcriptions']}")
            
            # Display results for each file
            for i, result in enumerate(batch_result['results']):
                print(f"\nFile {i+1}: {result['file_path']}")
                if result.get('success', False):
                    print(f"  ✓ Text: {result.get('text', '')[:100]}...")
                else:
                    print(f"  ✗ Error: {result.get('error', 'Unknown error')}")
        else:
            print("⚠ No audio files found for batch processing.")
            print("Please add some audio files to test batch transcription.")
        
        print("\n=== Example completed ===")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nPlease make sure you have:")
        print("1. Set your ELEVENLABS_API_KEY in a .env file or environment variable")
        print("2. Installed required dependencies: pip install -r requirements.txt")
        print("3. Valid audio files to transcribe")
        sys.exit(1)

if __name__ == "__main__":
    main()
