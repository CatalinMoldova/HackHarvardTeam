#!/usr/bin/env python3
"""
11Labs Text-to-Speech Example
Based on the official documentation: https://elevenlabs.io/docs/cookbooks/text-to-speech/quickstart
"""

import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play

def main():
    """Example from 11Labs documentation"""
    print("=== 11Labs Text-to-Speech Example ===")
    
    # Load environment variables
    load_dotenv()
    
    # Initialize ElevenLabs client
    elevenlabs = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
    )
    
    # Convert text to speech
    print("Converting text to speech...")
    audio = elevenlabs.text_to_speech.convert(
        text="The first move is what sets everything in motion.",
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    
    print("✅ Audio generated successfully!")
    print(f"Audio size: {len(audio)} bytes")
    
    # Save to file
    with open("example_output.mp3", "wb") as f:
        f.write(audio)
    print("📁 Audio saved to: example_output.mp3")
    
    # Try to play audio
    print("🎵 Attempting to play audio...")
    try:
        play(audio)
        print("✅ Audio played successfully!")
    except Exception as e:
        print(f"⚠️ Could not play audio: {e}")
        print("You may need to install MPV or ffmpeg for audio playback")
    
    print("\n🎉 Example completed successfully!")

if __name__ == "__main__":
    main()
